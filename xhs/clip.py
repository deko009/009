"""从网站剪贴素材：下载页面图片 + 抽取标题/正文文字，存到 materials/<名称>/。

用法:
    python -m xhs.clip https://example.com/product --name 春季新品
    python -m xhs.clip https://example.com --min-size 400   # 只要宽高都 >= 400px 的图
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"


def slugify(url: str) -> str:
    p = urlparse(url)
    return re.sub(r"[^\w\-]+", "_", (p.netloc + p.path).strip("/"))[:60] or "site"


def clip(url: str, name: str | None, min_size: int, scroll: int) -> Path:
    out = MATERIALS / (name or slugify(url))
    img_dir = out / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        # 可用环境变量 XHS_CHROMIUM 指定浏览器路径
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        browser = pw.chromium.launch(executable_path=os.environ.get("XHS_CHROMIUM") or None,
                                     proxy={"server": proxy, "bypass": os.environ.get("NO_PROXY", "localhost,127.0.0.1")}
                                     if proxy else None)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=60_000)
        # 滚动触发懒加载图片
        for _ in range(scroll):
            page.mouse.wheel(0, 1600)
            page.wait_for_timeout(600)

        data = page.evaluate(
            """(minSize) => {
                const imgs = [...document.images]
                  .filter(i => i.naturalWidth >= minSize && i.naturalHeight >= minSize)
                  .map(i => ({src: i.currentSrc || i.src, alt: i.alt || '',
                              w: i.naturalWidth, h: i.naturalHeight}));
                const text = sel => [...document.querySelectorAll(sel)]
                  .map(e => e.innerText.trim()).filter(Boolean);
                return {
                  title: document.title,
                  description: document.querySelector('meta[name=description]')?.content || '',
                  ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
                  headings: text('h1, h2, h3'),
                  paragraphs: text('p').filter(t => t.length > 15),
                  images: imgs,
                };
            }""",
            min_size,
        )
        page.screenshot(path=str(out / "screenshot.png"), full_page=True)

        seen, saved = set(), []
        sources = [i["src"] for i in data["images"]]
        if data["ogImage"]:
            sources.insert(0, urljoin(url, data["ogImage"]))
        for src in sources:
            if not src or src.startswith("data:") or src in seen:
                continue
            seen.add(src)
            try:
                resp = page.request.get(src, timeout=30_000)
                if not resp.ok:
                    continue
                ctype = resp.headers.get("content-type", "")
                ext = {"image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}.get(
                    ctype.split(";")[0], ".jpg")
                fname = f"{len(saved) + 1:02d}_{hashlib.md5(src.encode()).hexdigest()[:8]}{ext}"
                (img_dir / fname).write_bytes(resp.body())
                saved.append({"file": f"images/{fname}", "src": src})
            except Exception as e:  # 单张失败不影响整体
                print(f"  跳过 {src}: {e}")
        browser.close()

    data["source_url"] = url
    data["saved_images"] = saved
    (out / "material.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"已保存 {len(saved)} 张图片 + 文字素材 -> {out}")
    return out


def main():
    ap = argparse.ArgumentParser(description="从网站剪贴素材")
    ap.add_argument("url")
    ap.add_argument("--name", help="素材文件夹名，默认按网址生成")
    ap.add_argument("--min-size", type=int, default=300, help="图片最小宽高(px)")
    ap.add_argument("--scroll", type=int, default=8, help="向下滚动次数(加载懒加载图片)")
    a = ap.parse_args()
    clip(a.url, a.name, a.min_size, a.scroll)


if __name__ == "__main__":
    main()
