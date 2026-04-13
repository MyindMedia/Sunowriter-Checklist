"""
Render the Module 01 course cover art on the Myind Sound brand kit.

Outputs:
  Resources/covers/module-01-cover-1280x720.png  (GHL course card)
  Resources/covers/module-01-cover-1080x1080.png (square / social)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "covers"
OUT.mkdir(exist_ok=True)

DARK = (26, 26, 26)
DARK_ALT = (34, 34, 34)
GOLD = (253, 185, 19)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
MUTED = (180, 180, 180)


def font(weight, size):
    name = {"black": "Inter-Black.ttf", "bold": "Inter-Bold.ttf", "reg": "Inter-Regular.ttf"}[weight]
    return ImageFont.truetype(str(FONTS / name), size)


def render(width, height, out_path):
    img = Image.new("RGB", (width, height), DARK)
    draw = ImageDraw.Draw(img)

    # Subtle diagonal accent stripe (orange) bleeding off the right edge
    stripe_w = int(width * 0.04)
    for i in range(stripe_w):
        x = width - i - 1
        alpha = 1 - (i / stripe_w)
        c = tuple(int(DARK[k] + (ORANGE[k] - DARK[k]) * alpha * 0.55) for k in range(3))
        draw.line([(x, 0), (x, height)], fill=c)

    # Gold left rule
    rail = int(width * 0.012)
    draw.rectangle([(0, 0), (rail, height)], fill=GOLD)

    # Layout grid
    pad_l = int(width * 0.07)
    pad_t = int(height * 0.14)

    # Top label: MODULE 01
    f_label = font("bold", int(height * 0.032))
    label = "MODULE 01"
    draw.text((pad_l, pad_t), label, font=f_label, fill=ORANGE)

    # Tag underline
    bbox = draw.textbbox((pad_l, pad_t), label, font=f_label)
    underline_y = bbox[3] + int(height * 0.012)
    draw.rectangle([(pad_l, underline_y), (pad_l + int(width * 0.08), underline_y + 3)], fill=ORANGE)

    # Headline: SUNO WRITER (gold, huge)
    headline_size = int(height * 0.18) if width >= height else int(height * 0.13)
    f_headline = font("black", headline_size)
    head_y = pad_t + int(height * 0.08)
    draw.text((pad_l, head_y), "SUNO", font=f_headline, fill=GOLD)

    head2_y = head_y + int(headline_size * 0.95)
    draw.text((pad_l, head2_y), "WRITER", font=f_headline, fill=GOLD)

    # Subtitle
    f_sub = font("bold", int(height * 0.038))
    sub_y = head2_y + int(headline_size * 1.05)
    draw.text((pad_l, sub_y), "From Blank Page to Release-Ready", font=f_sub, fill=WHITE)

    # Tagline
    f_tag = font("reg", int(height * 0.028))
    tag_y = sub_y + int(height * 0.06)
    draw.text((pad_l, tag_y), "15 lessons. Every mode. Every feature.", font=f_tag, fill=MUTED)

    # Footer brand
    f_brand = font("bold", int(height * 0.024))
    brand_text = "MYIND SOUND MUSIC CLUB"
    bb = draw.textbbox((0, 0), brand_text, font=f_brand)
    bw = bb[2] - bb[0]
    draw.text((pad_l, height - int(height * 0.07) - (bb[3] - bb[1])), brand_text, font=f_brand, fill=GOLD)

    # Top-right small mark: dot grid as visual texture (very subtle)
    dot_color = (60, 60, 60)
    grid_x0 = int(width * 0.62)
    grid_y0 = int(height * 0.12)
    for r in range(8):
        for c in range(10):
            x = grid_x0 + c * int(width * 0.025)
            y = grid_y0 + r * int(width * 0.025)
            draw.ellipse([(x, y), (x + 4, y + 4)], fill=dot_color)

    # Big right-side glyph: stylized "SW" monogram in a gold-outlined square
    box = int(min(width, height) * 0.32)
    bx = width - box - int(width * 0.08)
    by = int(height * 0.5) - box // 2
    draw.rectangle([(bx, by), (bx + box, by + box)], outline=GOLD, width=6)
    f_mono = font("black", int(box * 0.55))
    mono = "SW"
    mb = draw.textbbox((0, 0), mono, font=f_mono)
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    draw.text((bx + (box - mw) / 2 - mb[0], by + (box - mh) / 2 - mb[1]), mono, font=f_mono, fill=GOLD)

    # Orange tick under monogram
    tick_y = by + box + int(height * 0.025)
    draw.rectangle([(bx, tick_y), (bx + int(box * 0.4), tick_y + 4)], fill=ORANGE)

    img.save(out_path, "PNG")
    print(f"  ✓ {out_path.name}")


def render_banner(width, height, out_path):
    """Wide horizontal banner layout for GHL header / hero images."""
    img = Image.new("RGB", (width, height), DARK)
    draw = ImageDraw.Draw(img)

    # Gold left rail
    rail = max(10, int(height * 0.04))
    draw.rectangle([(0, 0), (rail, height)], fill=GOLD)

    # Subtle orange bleed on right edge
    stripe_w = int(width * 0.025)
    for i in range(stripe_w):
        x = width - i - 1
        alpha = 1 - (i / stripe_w)
        c = tuple(int(DARK[k] + (ORANGE[k] - DARK[k]) * alpha * 0.55) for k in range(3))
        draw.line([(x, 0), (x, height)], fill=c)

    # Dot grid texture on right
    dot_color = (55, 55, 55)
    dot_spacing = max(24, int(height * 0.08))
    grid_x0 = int(width * 0.55)
    grid_y0 = int(height * 0.18)
    for r in range(int((height * 0.65) / dot_spacing)):
        for c in range(int((width * 0.25) / dot_spacing)):
            x = grid_x0 + c * dot_spacing
            y = grid_y0 + r * dot_spacing
            draw.ellipse([(x, y), (x + 4, y + 4)], fill=dot_color)

    # Left content block
    pad_l = int(width * 0.05)
    center_y = height / 2

    # Label: MODULE 01 • SUNO WRITER
    f_tag = font("bold", int(height * 0.08))
    tag = "MODULE 01  •  SUNO WRITER NEURAL ENGINE"
    tag_bb = draw.textbbox((0, 0), tag, font=f_tag)
    tag_h = tag_bb[3] - tag_bb[1]

    # Headline: SUNO WRITER (single line, horizontal)
    f_headline = font("black", int(height * 0.34))
    headline = "SUNO WRITER"
    h_bb = draw.textbbox((0, 0), headline, font=f_headline)
    h_h = h_bb[3] - h_bb[1]

    # Subtitle
    f_sub = font("bold", int(height * 0.085))
    sub = "From Blank Page to Release-Ready"
    s_bb = draw.textbbox((0, 0), sub, font=f_sub)
    s_h = s_bb[3] - s_bb[1]

    gap1 = int(height * 0.04)
    gap2 = int(height * 0.04)
    total_h = tag_h + gap1 + h_h + gap2 + s_h
    start_y = (height - total_h) / 2

    # Draw stack
    draw.text((pad_l, start_y - tag_bb[1]), tag, font=f_tag, fill=ORANGE)
    tag_underline_y = start_y + tag_h + int(height * 0.01)
    draw.rectangle(
        [(pad_l, tag_underline_y), (pad_l + int(width * 0.05), tag_underline_y + 3)],
        fill=ORANGE,
    )

    h_y = start_y + tag_h + gap1
    draw.text((pad_l, h_y - h_bb[1]), headline, font=f_headline, fill=GOLD)

    s_y = h_y + h_h + gap2
    draw.text((pad_l, s_y - s_bb[1]), sub, font=f_sub, fill=WHITE)

    # Right-side SW monogram box
    box = int(height * 0.68)
    bx = width - box - int(width * 0.06)
    by = int((height - box) / 2)
    draw.rectangle([(bx, by), (bx + box, by + box)], outline=GOLD, width=max(4, int(box * 0.035)))
    f_mono = font("black", int(box * 0.55))
    mono = "SW"
    mb = draw.textbbox((0, 0), mono, font=f_mono)
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    draw.text(
        (bx + (box - mw) / 2 - mb[0], by + (box - mh) / 2 - mb[1]),
        mono,
        font=f_mono,
        fill=GOLD,
    )

    img.save(out_path, "PNG")
    print(f"  ✓ {out_path.name}")


def main():
    print("Rendering Module 01 covers...")
    render(1280, 720, OUT / "module-01-cover-1280x720.png")
    render(1080, 1080, OUT / "module-01-cover-1080x1080.png")
    render(1920, 1080, OUT / "module-01-cover-1920x1080.png")

    print("Rendering GHL banner images...")
    render_banner(1584, 396, OUT / "ghl-header-1584x396.png")
    render_banner(1920, 480, OUT / "ghl-header-1920x480.png")
    render_banner(2560, 640, OUT / "ghl-hero-2560x640.png")
    print("Done.")


if __name__ == "__main__":
    main()
