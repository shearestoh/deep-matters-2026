#!/usr/bin/env python3
"""Generate site images from site/data/content.json.

    python3 tools/make_images.py          # all of the below
    python3 tools/make_images.py photos   # assets/people/<id>.* -> site/images/people/<id>.jpg (400x400)
    python3 tools/make_images.py gallery  # assets/gallery/* -> site/images/gallery/*.jpg (960x640)
    python3 tools/make_images.py og       # site/images/og-card.png (link preview, 1200x630)
    python3 tools/make_images.py cards    # share/<id>-{landscape,square}.png for each speaker

Requires Pillow (pip install pillow).
"""
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = json.loads((SITE / "data" / "content.json").read_text())
EVENT, VENUE = DATA["event"], DATA["venue"]

DARK, WHITE, GREY, FG = "#1f1f1f", "#ffffff", "#a3a3a3", "#1f2937"
GOLD, AMBER = "#fab22b", "#d97706"
FONTS = {
    True: ["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    False: ["DejaVuSans.ttf", "Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}


def font(size, bold=False):
    for path in FONTS[bold]:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_width(draw, text, f):
    if hasattr(draw, "textbbox"):
        l, _, r, _ = draw.textbbox((0, 0), text, font=f)
        return r - l
    return draw.textsize(text, font=f)[0]


def centred(draw, y, text, f, fill, width):
    draw.text(((width - text_width(draw, text, f)) // 2, y), text, font=f, fill=fill)


THEME_GRADIENT = ["#f5a623", "#e8890c", "#c2410c"]  # matches --theme-gradient in site/css/style.css


def centred_gradient(img, y, text, f, stops=THEME_GRADIENT):
    """Draw centred text filled with a left-to-right gradient."""
    draw = ImageDraw.Draw(img)
    w = text_width(draw, text, f)
    h = f.size * 2
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((0, 0), text, font=f, fill=255)
    rgb = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in stops]
    grad = Image.new("RGB", (w, h))
    gp = grad.load()
    for x in range(w):
        t = x / max(w - 1, 1) * (len(rgb) - 1)
        i = min(int(t), len(rgb) - 2)
        f_ = t - i
        col = tuple(round(rgb[i][k] + (rgb[i + 1][k] - rgb[i][k]) * f_) for k in range(3))
        for yy in range(h):
            gp[x, yy] = col
    img.paste(grad, ((img.width - w) // 2, y), mask)


def place_text():
    return f"{VENUE['name']} · {VENUE['city']}"


def date_text():
    d = date.fromisoformat(EVENT["date"])
    return f"{d.day} {d:%B %Y}"


def circle(img, size, ring=8):
    """Square-crop to a circle with a gold ring."""
    img = ImageOps.fit(img.convert("RGB"), (size, size), Image.LANCZOS, centering=(0.5, 0.4))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size + 2 * ring, size + 2 * ring), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse((0, 0, out.width - 1, out.height - 1), fill=GOLD)
    out.paste(img, (ring, ring), mask)
    return out


def header_band(canvas, height):
    """Dark band with logo, title/theme and date/venue — shared by every card."""
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, canvas.width, height), fill=DARK)
    logo = Image.open(SITE / "images" / "logo.png").convert("RGBA")
    logo = logo.resize((int(logo.width * 60 / logo.height), 60), Image.LANCZOS)
    plate = Image.new("RGBA", (logo.width + 24, 84), WHITE)
    plate.paste(logo, (12, 12), logo)
    canvas.paste(plate, (60, (height - 84) // 2))
    x = 60 + plate.width + 32
    draw.text((x, height // 2 - 44), f"{EVENT['title']}: {EVENT['theme']}", font=font(34, True), fill=WHITE)
    draw.text((x, height // 2 + 8), f"{date_text()}  ·  {place_text()}", font=font(22), fill=GREY)


def make_photos():
    out = SITE / "images" / "people"
    out.mkdir(parents=True, exist_ok=True)
    for src in sorted((ROOT / "assets" / "people").glob("*")):
        if src.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        img = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), (400, 400),
                           Image.LANCZOS, centering=(0.5, 0.4))
        img.save(out / f"{src.stem}.jpg", quality=85, optimize=True)
        print("photo", out / f"{src.stem}.jpg")


def make_gallery():
    """assets/gallery/* (full-size originals, not committed) -> site/images/gallery/*.jpg (960x640)."""
    out = SITE / "images" / "gallery"
    out.mkdir(parents=True, exist_ok=True)
    for src in sorted((ROOT / "assets" / "gallery").glob("*")):
        if src.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        img = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), (960, 640), Image.LANCZOS)
        img.save(out / f"{src.stem}.jpg", quality=78, optimize=True, progressive=True)
        print("gallery", out / f"{src.stem}.jpg")


def make_og():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    logo = Image.open(SITE / "images" / "logo.png").convert("RGBA")
    logo = logo.resize((int(logo.width * 130 / logo.height), 130), Image.LANCZOS)
    img.paste(logo, ((w - logo.width) // 2, 80), logo)
    centred(draw, 250, f"{EVENT['title']}:", font(72, True), FG, w)
    centred_gradient(img, 335, EVENT["theme"], font(72, True))
    centred(draw, 460, date_text(), font(32, True), FG, w)
    centred(draw, 508, place_text(), font(30), "#6b7280", w)
    draw.rectangle((0, h - 14, w, h), fill=GOLD)
    img.save(SITE / "images" / "og-card.png", optimize=True)
    print("og", SITE / "images" / "og-card.png")


def make_cards():
    out = ROOT / "share"
    out.mkdir(exist_ok=True)
    talks = [i for i in DATA["agenda"]["items"] if i["type"] == "talk"]
    ids = list(dict.fromkeys(s for t in talks for s in t.get("speakers", [])))
    if not ids:
        print("cards: no speakers in the agenda yet")
    for sid in ids:
        p = DATA["people"][sid]
        for name, (w, h, band, photo) in {"landscape": (1200, 627, 150, 300), "square": (1080, 1080, 170, 420)}.items():
            img = Image.new("RGB", (w, h), WHITE)
            header_band(img, band)
            draw = ImageDraw.Draw(img)
            top = band + (h - band - photo - 140) // 2
            if p.get("photo"):
                ring = circle(Image.open(SITE / p["photo"]), photo)
                img.paste(ring, ((w - ring.width) // 2, top), ring)
            centred(draw, top + photo + 40, p["name"], font(48, True), FG, w)
            centred(draw, top + photo + 104, p["affiliation"], font(28), "#6b7280", w)
            draw.rectangle((0, h - 12, w, h), fill=GOLD)
            img.save(out / f"{sid}-{name}.png", optimize=True)
            print("card", out / f"{sid}-{name}.png")


if __name__ == "__main__":
    steps = {"photos": make_photos, "gallery": make_gallery, "og": make_og, "cards": make_cards}
    for step in sys.argv[1:] or steps:
        steps[step]()
