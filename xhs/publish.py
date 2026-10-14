"""小红书多账号图文发布（本地运行，浏览器可见）。

每个账号一个独立浏览器配置目录 accounts/<账号>/，首次扫码登录后长期复用。

用法:
    python -m xhs.publish login 账号A                 # 打开浏览器扫码登录，登录后关闭窗口即可
    python -m xhs.publish post posts/example          # 自动填好，你在浏览器里点「发布」
    python -m xhs.publish post posts/example --auto   # 不询问，直接发布
    python -m xhs.publish run                         # 按队列发布 posts/ 下所有未发布的帖子

帖子目录结构:
    posts/<帖子>/post.json   {"account": "账号A", "title": "...", "body": "...", "tags": ["穿搭"]}
    posts/<帖子>/1.png 2.png ...   # Figma 导出的图片，按文件名顺序上传(最多 18 张)
"""
import argparse
import json
import random
import subprocess
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeout

ROOT = Path(__file__).resolve().parent.parent
ACCOUNTS = ROOT / "accounts"
POSTS = ROOT / "posts"
PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"
LOGIN_URL = "https://creator.xiaohongshu.com/login"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TITLE_MAX = 20
BODY_MAX = 1000


def copy_to_clipboard(meta: dict) -> bool:
    """把正文和话题复制到系统剪贴板（Mac 用 pbcopy，Windows 用 clip）。"""
    text = meta.get("body", "") + "\n\n" + " ".join(f"#{t}" for t in meta.get("tags", []))
    for cmd in (["pbcopy"], ["clip"]):
        try:
            subprocess.run(cmd, input=text.encode("utf-16" if cmd == ["clip"] else "utf-8"), check=True)
            return True
        except (OSError, subprocess.CalledProcessError):
            continue
    return False


def human_pause(lo=0.8, hi=2.0):
    time.sleep(random.uniform(lo, hi))


def open_context(pw, account: str):
    profile = ACCOUNTS / account
    profile.mkdir(parents=True, exist_ok=True)
    return pw.chromium.launch_persistent_context(
        str(profile), headless=False, viewport={"width": 1400, "height": 900}, locale="zh-CN")


def login(account: str):
    with sync_playwright() as pw:
        ctx = open_context(pw, account)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(LOGIN_URL)
        print(f"[{account}] 请在浏览器里扫码登录，进入创作者中心后关闭浏览器窗口。")
        page.wait_for_event("close", timeout=0)
        ctx.close()


def load_post(post_dir: Path) -> dict:
    meta = json.loads((post_dir / "post.json").read_text("utf-8"))
    images = sorted(p for p in post_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS)
    if not images:
        raise SystemExit(f"{post_dir} 里没有图片")
    if len(meta["title"]) > TITLE_MAX:
        raise SystemExit(f"标题超过 {TITLE_MAX} 字: {meta['title']}")
    meta["images"] = images[:18]
    return meta


def click_onscreen(page: Page, text: str, timeout_ms: int = 30_000) -> bool:
    """点击屏幕范围内显示着 text 的元素。

    小红书页面里藏着一份放在屏幕外的同名标签，直接点第一个会一直报
    "element is outside of the viewport"，所以要挑坐标落在窗口里的那个。
    """
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        vw = page.viewport_size or page.evaluate("({width: innerWidth, height: innerHeight})")
        candidates = page.get_by_text(text, exact=True)
        for i in range(candidates.count()):
            el = candidates.nth(i)
            try:
                box = el.bounding_box()
            except Exception:
                box = None
            if box and box["width"] > 0 and box["x"] >= 0 and box["y"] >= 0 \
                    and box["x"] + box["width"] <= vw["width"] and box["y"] + box["height"] <= vw["height"]:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                return True
        page.wait_for_timeout(500)
    return False


def fill_post(page: Page, meta: dict):
    # 小红书页面会一直在后台请求数据，不能等 networkidle，改为等具体元素出现
    page.goto(PUBLISH_URL, wait_until="domcontentloaded", timeout=60_000)
    page.wait_for_timeout(3000)
    if "login" in page.url:
        raise RuntimeError("这个账号没登录或登录已过期，请先运行 2-登录账号 扫码")
    # 优先选接受图片的上传框，避免选到视频上传框
    file_input = page.locator("input[type=file][accept*='image'], input[type=file][accept*='jpg'], "
                              "input[type=file][accept*='png'], input[type=file][accept*='webp']")
    # 发布页默认停在「上传视频」，要点屏幕上的「上传图文」标签；
    # 平台改版后地址可能跳到别处，那就先点左上角「发布笔记」
    for _ in range(3):
        if not click_onscreen(page, "上传图文", timeout_ms=10_000):
            click_onscreen(page, "发布笔记", timeout_ms=10_000)
            human_pause(1.5, 2.5)
            continue
        human_pause(1.5, 2.5)
        try:
            file_input.first.wait_for(state="attached", timeout=8_000)
            break
        except PlaywrightTimeout:
            continue
    if file_input.count() == 0:
        raise RuntimeError("切换到「上传图文」失败，页面上还是视频上传框")
    file_input.first.set_input_files([str(p) for p in meta["images"]])
    # 等待上传完成：标题输入框出现
    title = page.locator("input[placeholder*='标题']").first
    title.wait_for(timeout=120_000)
    human_pause()
    title.fill(meta["title"])
    human_pause()

    editor = page.locator("div.tiptap.ProseMirror, div.ql-editor, #post-textarea").first
    editor.click()
    body = meta.get("body", "")[:BODY_MAX]
    page.keyboard.type(body, delay=random.randint(20, 60))
    for tag in meta.get("tags", []):
        page.keyboard.type(f" #{tag}", delay=60)
        human_pause(1.2, 2.0)
        page.keyboard.press("Enter")  # 选中话题联想的第一项，使其成为真正的话题
    human_pause()


def published_now(page: Page) -> bool:
    return "success" in page.url or page.get_by_text("发布成功").count() > 0


def wait_for_user_publish(page: Page) -> bool:
    """等用户在浏览器里点发布：看到发布成功返回 True，用户直接关窗口返回 False。"""
    while True:
        try:
            if published_now(page):
                page.wait_for_timeout(2000)
                return True
            page.wait_for_timeout(1000)
        except Exception:  # 浏览器窗口被关掉
            return False


def publish_post(post_dir: Path, account: str | None, auto: bool) -> bool:
    meta = load_post(post_dir)
    account = account or meta.get("account")
    if not account:
        raise SystemExit("请在 post.json 里写 account，或用 --account 指定")

    with sync_playwright() as pw:
        ctx = open_context(pw, account)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            fill_post(page, meta)
        except Exception as e:
            # 自动填写失败时不关浏览器，让用户在同一个窗口手动接着发
            shot = post_dir / "error.png"
            try:
                page.screenshot(path=str(shot))
            except Exception:
                pass
            copied = copy_to_clipboard(meta)
            print(f"\n[{account}] 自动填写卡住了：{e}")
            print(f"出错时的页面截图：{shot}（发给 Claude 可以帮你修）")
            if copied:
                print("正文和话题已复制到剪贴板，可以直接在浏览器里粘贴。")
            input("请在打开的浏览器里手动完成剩下的步骤，发完后按回车关闭...")
            ctx.close()
            return False
        if auto:
            try:
                page.get_by_role("button", name="发布", exact=True).last.click(timeout=15_000)
                page.wait_for_timeout(6000)
                ok = published_now(page)
            except PlaywrightTimeout:
                ok = False
        else:
            print(f"\n[{account}] 已填好《{meta['title']}》")
            print("👉 请在浏览器里检查，满意就点「发布」；不想发就直接关掉浏览器窗口。")
            ok = wait_for_user_publish(page)
        try:
            ctx.close()
        except Exception:
            pass

    if ok:
        (post_dir / "published.json").write_text(json.dumps(
            {"account": account, "at": datetime.now().isoformat(timespec="seconds")},
            ensure_ascii=False), "utf-8")
        print(f"[{account}] 已发布: {meta['title']}")
    else:
        print(f"[{account}] 浏览器已关闭，没有检测到发布成功。如果其实已经发了，去创作者中心「笔记管理」看看：{meta['title']}")
    return ok


def run_queue(auto: bool, gap_min: int, gap_max: int):
    pending = [d for d in sorted(POSTS.iterdir())
               if (d / "post.json").exists() and not (d / "published.json").exists()]
    print(f"待发布 {len(pending)} 篇")
    for i, d in enumerate(pending):
        publish_post(d, None, auto)
        if i < len(pending) - 1:
            wait = random.randint(gap_min, gap_max)
            print(f"间隔 {wait // 60} 分钟后发下一篇...")
            time.sleep(wait)


def main():
    ap = argparse.ArgumentParser(description="小红书多账号发布")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("login"); s.add_argument("account")
    s = sub.add_parser("post"); s.add_argument("post_dir", type=Path)
    s.add_argument("--account"); s.add_argument("--auto", action="store_true")
    s = sub.add_parser("run"); s.add_argument("--auto", action="store_true")
    s.add_argument("--gap-min", type=int, default=20 * 60, help="两篇之间最短间隔(秒)")
    s.add_argument("--gap-max", type=int, default=60 * 60, help="两篇之间最长间隔(秒)")
    a = ap.parse_args()

    if a.cmd == "login":
        login(a.account)
    elif a.cmd == "post":
        publish_post(a.post_dir, a.account, a.auto)
    else:
        run_queue(a.auto, a.gap_min, a.gap_max)


if __name__ == "__main__":
    main()
