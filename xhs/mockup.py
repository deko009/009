"""把截图拼成小红书 3:4 竖图：白底，左边电脑框，右下叠一个手机框。

用法:
    python -m xhs.mockup wwake            # 读 materials/wwake/pages.json，输出到 posts/wwake/1.png 2.png ...
    python -m xhs.mockup wwake --bg "#F5F3EF"   # 换背景色

第 1 张（首页）就是封面。
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"
POSTS = ROOT / "posts"

W, H = 1242, 1656            # 小红书推荐 3:4
FRAME = (190, 190, 190)      # 设备边框颜色
BORDER = 10                  # 边框粗细
# 设备位置（按画布比例），参照用户给的排版样例
DESKTOP_BOX = (0.03, 0.035, 0.72, 0.915)   # x, y, 宽, 高
MOBILE_BOX = (0.665, 0.13, 0.305, 0.835)
DESKTOP_RADIUS, MOBILE_RADIUS = 36, 44


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, fill=255)
    return m


def fit_top(img: Image.Image, size) -> Image.Image:
    """按宽度缩放截图，从顶部裁到目标高度（不够高就补白）。"""
    w, h = size
    scaled = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    if scaled.height < h:
        canvas = Image.new("RGB", (w, h), "white")
        canvas.paste(scaled, (0, 0))
        return canvas
    return scaled.crop((0, 0, w, h))


def device(canvas: Image.Image, shot: Image.Image, box, radius):
    x, y, bw, bh = (round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H))
    # 柔和阴影
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([x + 4, y + 10, x + bw + 4, y + bh + 10], radius,
                                             fill=(0, 0, 0, 40))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
    # 边框
    frame = Image.new("RGBA", (bw, bh), FRAME + (255,))
    canvas.paste(frame, (x, y), rounded_mask((bw, bh), radius))
    # 屏幕内容
    inner = (bw - 2 * BORDER, bh - 2 * BORDER)
    screen = fit_top(shot.convert("RGB"), inner)
    canvas.paste(screen, (x + BORDER, y + BORDER), rounded_mask(inner, radius - BORDER))


def compose(desktop: Path, mobile: Path, out: Path, bg: str):
    canvas = Image.new("RGBA", (W, H), bg)
    device(canvas, Image.open(desktop), DESKTOP_BOX, DESKTOP_RADIUS)
    device(canvas, Image.open(mobile), MOBILE_BOX, MOBILE_RADIUS)
    canvas.convert("RGB").save(out, quality=95)


def build(name: str, bg: str) -> list[Path]:
    src = MATERIALS / name
    pages = json.loads((src / "pages.json").read_text("utf-8"))["pages"]
    out_dir = POSTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("[0-9]*.png"):
        old.unlink()
    outs = []
    for i, p in enumerate(pages, 1):
        out = out_dir / f"{i}.png"
        compose(src / p["desktop"], src / p["mobile"], out, bg)
        outs.append(out)
        print(f"{out.name} <- {p['kind']} {p['url']}")
    print(f"拼好 {len(outs)} 张图 -> {out_dir}")
    return outs


def main():
    ap = argparse.ArgumentParser(description="把截图拼成小红书展示图")
    ap.add_argument("name", help="素材名，和 shoot 时的 --name 一样")
    ap.add_argument("--bg", default="#FFFFFF", help="背景色，默认白色")
    a = ap.parse_args()
    build(a.name, a.bg)


if __name__ == "__main__":
    main()
