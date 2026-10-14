"""给一个网址，自动找出网站的关键页面，每页截电脑版 + 手机版，并抽取页面文字。

用法:
    python -m xhs.shoot https://www.wwake.com --name wwake
    python -m xhs.shoot https://www.wwake.com --name wwake --pages 6

产出 materials/<名称>/:
    shots/01_home_desktop.png  shots/01_home_mobile.png ...
    pages.json   每页的网址、标题、小标题、段落、价格，给写文案用
"""
import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"

DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
# 截图最大高度（像素，按 CSS 尺寸）：太长的页面只截上半部分，够排版用
DESKTOP_MAX_H = 2400
MOBILE_MAX_H = 1600

# 按关键词给页面打分，挑出最能代表网站的几页（越靠前越优先）
PAGE_KINDS = [
    ("shop", r"shop|all|collection|catalog|products?/?$|store|category|分类|商品"),
    ("product", r"/products?/[^/]+|/item/|/p/|/goods/"),
    ("about", r"about|story|ethos|brand|journal|关于|品牌"),
    ("visit", r"visit|showroom|appointment|location|store-?locator|门店"),
    ("contact", r"contact|faq|help|support|联系"),
]

DISMISS_TEXTS = ["Accept", "Accept all", "Accept All", "Allow all", "I agree", "Agree",
                 "Got it", "OK", "同意", "接受", "我知道了", "关闭"]


def launch(pw):
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    return pw.chromium.launch(
        executable_path=os.environ.get("XHS_CHROMIUM") or None,
        proxy={"server": proxy, "bypass": os.environ.get("NO_PROXY", "localhost,127.0.0.1")}
        if proxy else None)


def settle(page):
    """关掉 cookie/弹窗，滚到底再回顶部，让懒加载图片都出来。"""
    page.wait_for_timeout(1500)
    for t in DISMISS_TEXTS:
        btn = page.get_by_role("button", name=t, exact=True)
        try:
            if btn.count() and btn.first.is_visible():
                btn.first.click(timeout=2000)
                page.wait_for_timeout(400)
        except Exception:
            pass
    page.keyboard.press("Escape")
    h = page.evaluate("document.body.scrollHeight")
    for y in range(0, min(h, 8000), 700):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(250)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1200)


def pick_pages(page, home: str, limit: int) -> list[tuple[str, str]]:
    host = urlparse(home).netloc
    links = page.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.href)")
    seen, picked = {home.rstrip("/")}, [("home", home)]
    for kind, pattern in PAGE_KINDS:
        for href in links:
            u = href.split("#")[0].split("?")[0].rstrip("/")
            if urlparse(u).netloc != host or u in seen:
                continue
            if re.search(pattern, urlparse(u).path, re.I):
                picked.append((kind, u))
                seen.add(u)
                break
        if len(picked) >= limit:
            break
    return picked


def extract_text(page) -> dict:
    return page.evaluate("""() => {
        const text = sel => [...document.querySelectorAll(sel)]
            .map(e => e.innerText.trim()).filter(Boolean);
        const body = document.body.innerText;
        return {
            title: document.title,
            description: document.querySelector('meta[name=description]')?.content || '',
            headings: text('h1, h2, h3').slice(0, 30),
            paragraphs: text('p').filter(t => t.length > 20).slice(0, 40),
            prices: [...new Set(body.match(/[$€£¥]\\s?[\\d,]+(\\.\\d{2})?/g) || [])].slice(0, 30),
        };
    }""")


def shoot_page(browser, url: str, viewport: dict, max_h: int, path: Path, mobile: bool):
    ctx = browser.new_context(viewport=viewport, device_scale_factor=2, is_mobile=mobile,
                              has_touch=mobile, locale="en-US")
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    settle(page)
    full_h = page.evaluate("document.documentElement.scrollHeight")
    page.screenshot(path=str(path), full_page=True,
                    clip={"x": 0, "y": 0, "width": viewport["width"], "height": min(full_h, max_h)})
    info = extract_text(page) if not mobile else None
    ctx.close()
    return info


def shoot(url: str, name: str, limit: int) -> Path:
    out = MATERIALS / name
    shots = out / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = launch(pw)
        ctx = browser.new_context(viewport=DESKTOP)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        settle(page)
        pages = pick_pages(page, url, limit)
        ctx.close()

        result = []
        for i, (kind, u) in enumerate(pages, 1):
            stem = f"{i:02d}_{kind}"
            print(f"[{i}/{len(pages)}] {kind}: {u}")
            try:
                info = shoot_page(browser, u, DESKTOP, DESKTOP_MAX_H, shots / f"{stem}_desktop.png", False)
                shoot_page(browser, u, MOBILE, MOBILE_MAX_H, shots / f"{stem}_mobile.png", True)
            except Exception as e:
                print(f"  跳过（{e.__class__.__name__}）")
                continue
            result.append({"kind": kind, "url": u, "desktop": f"shots/{stem}_desktop.png",
                           "mobile": f"shots/{stem}_mobile.png", **info})
        browser.close()

    (out / "pages.json").write_text(json.dumps(
        {"site": url, "pages": result}, ensure_ascii=False, indent=2), "utf-8")
    print(f"截好 {len(result)} 个页面 -> {out}")
    return out


def main():
    ap = argparse.ArgumentParser(description="自动截取网站关键页面（电脑版+手机版）")
    ap.add_argument("url")
    ap.add_argument("--name", required=True, help="品牌/素材名，比如 wwake")
    ap.add_argument("--pages", type=int, default=5, help="最多截几个页面（含首页）")
    a = ap.parse_args()
    shoot(a.url, a.name, a.pages)


if __name__ == "__main__":
    main()
