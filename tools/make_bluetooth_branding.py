#!/usr/bin/env python3
"""Generate icon.png and logo.png for the Bluetooth Web Snapclient Proxy add-on.

Home Assistant picks these up by filename from the add-on folder: icon.png for
the Supervisor panel, logo.png for the add-on store. Generated rather than
hand-drawn so the artwork stays editable -- change a constant and re-run:

    python3 tools/make_bluetooth_branding.py

Needs Pillow (`pip install pillow`); nothing at runtime depends on this.
"""

from pathlib import Path

from PIL import Image, ImageDraw

OUT_DIR = Path(__file__).resolve().parent.parent / "bluetooth_web_proxy"
SIZE = 200
SS = 4  # supersample, then downsample for antialiased edges

BG_TOP = (18, 34, 66)
BG_BOTTOM = (10, 16, 32)
BT_BLUE = (56, 132, 255)
WAVE = (110, 231, 183)


def gradient(size):
    img = Image.new("RGB", (1, size), BG_TOP)
    px = img.load()
    for y in range(size):
        t = y / max(1, size - 1)
        px[0, y] = tuple(
            round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)
        )
    return img.resize((size, size))


def bluetooth_rune(draw, cx, cy, h, width):
    """The Bluetooth rune: a vertical stroke with two bowties crossing it."""
    top, bottom = cy - h / 2, cy + h / 2
    right = cx + h * 0.28
    draw.line([(cx, top), (cx, bottom)], fill=BT_BLUE, width=width)
    # upper bowtie
    draw.line([(cx, top), (right, cy - h * 0.22)], fill=BT_BLUE, width=width)
    draw.line([(right, cy - h * 0.22), (cx - h * 0.28, cy + h * 0.06)],
              fill=BT_BLUE, width=width)
    # lower bowtie
    draw.line([(cx, bottom), (right, cy + h * 0.22)], fill=BT_BLUE, width=width)
    draw.line([(right, cy + h * 0.22), (cx - h * 0.28, cy - h * 0.06)],
              fill=BT_BLUE, width=width)


def waves(draw, cx, cy, h, width):
    """Three arcs to the right: the audio half of the story."""
    for i, r in enumerate((0.42, 0.62, 0.82)):
        box = [cx - h * r, cy - h * r, cx + h * r, cy + h * r]
        draw.arc(box, start=-42, end=42, fill=WAVE, width=width - i)


def render(width, height, path):
    img = gradient(max(width, height) * SS).resize((width * SS, height * SS))
    draw = ImageDraw.Draw(img)

    h = height * SS * 0.52
    cx = width * SS * 0.40
    cy = height * SS * 0.5
    bluetooth_rune(draw, cx, cy, h, width=max(3, int(height * SS * 0.045)))
    waves(draw, cx + h * 0.30, cy, h, width=max(3, int(height * SS * 0.040)))

    img.resize((width, height), Image.LANCZOS).save(path)
    print("wrote", path)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    render(SIZE, SIZE, OUT_DIR / "icon.png")
    render(SIZE, SIZE, OUT_DIR / "logo.png")
