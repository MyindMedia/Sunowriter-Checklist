"""
Render lesson thumbnails for Module 01 on the Myind Sound brand kit.

Reads ../CHECKLIST.md, pulls each lesson's number + title, and writes
1280x720 PNGs to ../suno-writer-tutorials/assets/thumbs/lesson-NN.png.
"""

from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
SOURCE = ROOT.parent / "CHECKLIST.md"
FONTS = ROOT / "fonts"
OUT = ROOT.parent / "suno-writer-tutorials" / "assets" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)

DARK = (26, 26, 26)
GOLD = (253, 185, 19)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
MUTED = (180, 180, 180)

W, H = 1280, 720


def font(weight, size):
    name = {"black": "Inter-Black.ttf", "bold": "Inter-Bold.ttf", "reg": "Inter-Regular.ttf"}[weight]
    return ImageFont.truetype(str(FONTS / name), size)


def parse_lessons(md):
    lessons = []
    parts = re.split(r"\n## LESSON ", md)
    for part in parts[1:]:
        if not re.match(r"^\d+", part):
            continue
        first_line = part.split("\n", 1)[0]
        m = re.match(r"^(\d+)\s*—\s*(.+?)\s*$", first_line)
        if m:
            lessons.append((m.group(1), m.group(2).strip()))
    return lessons


def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=fnt)
        if bbox[2] - bbox[0] <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def render(num, title, out_path):
    img = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(img)

    # Gold left rail
    rail = 16
    draw.rectangle([(0, 0), (rail, H)], fill=GOLD)

    # Subtle dot grid (top right)
    dot_color = (60, 60, 60)
    for r in range(7):
        for c in range(9):
            x = 820 + c * 36
            y = 80 + r * 36
            draw.ellipse([(x, y), (x + 5, y + 5)], fill=dot_color)

    # Right side: huge lesson number outlined
    f_num = font("black", 360)
    num_text = num.zfill(2)
    nb = draw.textbbox((0, 0), num_text, font=f_num)
    nw = nb[2] - nb[0]
    nh = nb[3] - nb[1]
    nx = W - nw - 90 - nb[0]
    ny = (H - nh) / 2 - nb[1] - 10
    # Drop shadow stroke effect — outline only via stroke_width
    draw.text((nx, ny), num_text, font=f_num, fill=GOLD, stroke_width=0)

    # Left content
    pad_l = 80
    pad_t = 100

    # Top tag MODULE 01
    f_tag = font("bold", 22)
    draw.text((pad_l, pad_t), "MODULE 01  •  SUNO WRITER", font=f_tag, fill=ORANGE)
    # underline
    bb = draw.textbbox((pad_l, pad_t), "MODULE 01  •  SUNO WRITER", font=f_tag)
    draw.rectangle([(pad_l, bb[3] + 10), (pad_l + 100, bb[3] + 13)], fill=ORANGE)

    # LESSON NN label
    f_lesson = font("bold", 28)
    lesson_y = pad_t + 70
    draw.text((pad_l, lesson_y), f"LESSON {num.zfill(2)}", font=f_lesson, fill=WHITE)

    # Title — wrap
    f_title = font("black", 64)
    title_y = lesson_y + 60
    max_w = 700
    lines = wrap_text(draw, title, f_title, max_w)
    if len(lines) > 3:
        f_title = font("black", 52)
        lines = wrap_text(draw, title, f_title, max_w)
    line_h = int(f_title.size * 1.05)
    for i, line in enumerate(lines):
        draw.text((pad_l, title_y + i * line_h), line, font=f_title, fill=GOLD)

    # Footer brand
    f_brand = font("bold", 18)
    draw.text((pad_l, H - 70), "MYIND SOUND MUSIC CLUB", font=f_brand, fill=GOLD)

    img.save(out_path, "PNG")


def main():
    md = SOURCE.read_text()
    lessons = parse_lessons(md)
    print(f"Rendering {len(lessons)} lesson thumbnails...")
    for num, title in lessons:
        path = OUT / f"lesson-{num.zfill(2)}.png"
        render(num, title, path)
        print(f"  ✓ {path.name}")
    print(f"Done. Saved to {OUT}")


if __name__ == "__main__":
    main()
