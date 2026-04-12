"""
Render Module 01 Suno Writer resource PDFs.

Generates 5 brand-styled PDFs into ./PDFs/:
  1. Interface Cheat Sheet
  2. Song Structure Card
  3. Cliché Blacklist Card
  4. Workflow Flowchart
  5. Module 1 Index Handout

Setup (one time):
    pip3 install reportlab

Run:
    python3 render_pdfs.py
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Brand palette
DARK = HexColor("#1A1A1A")
DARK_ALT = HexColor("#222222")
GOLD = HexColor("#FDB913")
ORANGE = HexColor("#FF8C00")
WHITE = HexColor("#FFFFFF")
RED = HexColor("#E63946")

# Register Inter (falls back to Helvetica if files missing)
FONTS_DIR = Path(__file__).parent / "fonts"
try:
    pdfmetrics.registerFont(TTFont("Inter", str(FONTS_DIR / "Inter-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Bold", str(FONTS_DIR / "Inter-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Black", str(FONTS_DIR / "Inter-Black.ttf")))
    FONT_BLACK = "Inter-Black"
    FONT_BOLD = "Inter-Bold"
    FONT_REG = "Inter"
except Exception as e:
    print(f"  ! Inter font not loaded ({e}), using Helvetica fallback")
    FONT_BLACK = "Helvetica-Bold"
    FONT_BOLD = "Helvetica-Bold"
    FONT_REG = "Helvetica"

OUT_DIR = Path(__file__).parent / "PDFs"
OUT_DIR.mkdir(exist_ok=True)


def fill_bg(c, w, h, color=DARK):
    c.setFillColor(color)
    c.rect(0, 0, w, h, fill=1, stroke=0)


def footer(c, w, text="Myind Sound Music Club  /  Suno Writer v2.0"):
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 9)
    c.drawCentredString(w / 2, 0.4 * inch, text)


# ─── 1. Interface Cheat Sheet ─────────────────────────────────
def interface_cheat_sheet():
    path = OUT_DIR / "01-interface-cheat-sheet.pdf"
    w, h = landscape(letter)
    c = canvas.Canvas(str(path), pagesize=landscape(letter))
    fill_bg(c, w, h)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 36)
    c.drawString(0.6 * inch, h - 0.9 * inch, "SUNO WRITER INTERFACE")

    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 14)
    c.drawString(0.6 * inch, h - 1.2 * inch, "Every panel, every button, one page")

    # Placeholder screenshot box
    box_x, box_y, box_w, box_h = 0.6 * inch, 3.8 * inch, w - 1.2 * inch, 3.0 * inch
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.rect(box_x, box_y, box_w, box_h, fill=0, stroke=1)
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 11)
    c.drawCentredString(box_x + box_w / 2, box_y + box_h / 2,
                        "[ Insert annotated dashboard screenshot here ]")

    callouts = [
        ("1", "Top Header", "App version label, home base"),
        ("2", "Mode Selector", "Songwriting / Instrumental / Sample / Analysis"),
        ("3", "View Tabs", "CHAT / ARRANGE / MOOD BOARD"),
        ("4", "New Chat", "Start a fresh session"),
        ("5", "Saved Works", "Filterable library"),
        ("6", "Templates", "Community library, fork or submit"),
        ("7", "Conversations", "Full chat history with sharing"),
        ("8", "User Profile", "Default mode and preferences"),
        ("9", "Header Icons", "Flow Viz / Help / Clear buffer"),
        ("10", "Parameters", "Complexity / Rating / H-Pads"),
    ]

    col_w = (w - 1.2 * inch) / 2
    row_h = 0.35 * inch
    for i, (n, label, desc) in enumerate(callouts):
        col = i // 5
        row = i % 5
        x = 0.6 * inch + col * col_w
        y = 3.4 * inch - row * row_h
        c.setFillColor(GOLD)
        c.setFont(FONT_BLACK, 16)
        c.drawString(x, y, n + ".")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 12)
        c.drawString(x + 0.3 * inch, y, label)
        c.setFillColor(WHITE)
        c.setFont(FONT_REG, 10)
        c.drawString(x + 1.7 * inch, y, desc)

    footer(c, w)
    c.showPage()
    c.save()
    print(f"  ✓ {path.name}")


# ─── 2. Song Structure Card ───────────────────────────────────
def song_structure_card():
    path = OUT_DIR / "02-song-structure-card.pdf"
    w, h = portrait(letter)
    c = canvas.Canvas(str(path), pagesize=portrait(letter))
    fill_bg(c, w, h)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 32)
    c.drawCentredString(w / 2, h - 1.0 * inch, "THE MYIND SOUND")
    c.drawCentredString(w / 2, h - 1.5 * inch, "SONG STRUCTURE")

    sections = [
        ("INTRO", 20),
        ("HOOK", 80),
        ("V1", 40),
        ("HOOK", 85),
        ("V2", 45),
        ("BRIDGE", 60),
        ("HOOK", 90),
        ("OUT", 25),
    ]

    chart_top = h - 2.5 * inch
    chart_bottom = h - 5.5 * inch
    chart_h = chart_top - chart_bottom
    bar_w = 0.7 * inch
    spacing = 0.15 * inch
    total_w = len(sections) * bar_w + (len(sections) - 1) * spacing
    start_x = (w - total_w) / 2

    for i, (label, energy) in enumerate(sections):
        x = start_x + i * (bar_w + spacing)
        bar_height = (energy / 100) * chart_h
        c.setFillColor(ORANGE)
        c.rect(x, chart_bottom, bar_w, bar_height, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 9)
        c.drawCentredString(x + bar_w / 2, chart_bottom - 0.2 * inch, label)
        c.setFillColor(GOLD)
        c.setFont(FONT_BLACK, 10)
        c.drawCentredString(x + bar_w / 2, chart_bottom + bar_height + 0.08 * inch, str(energy))

    # Rules box
    box_x = 0.8 * inch
    box_y = 1.2 * inch
    box_w = w - 1.6 * inch
    box_h = 2.0 * inch
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.setFillColor(DARK)
    c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=1)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 16)
    c.drawString(box_x + 0.3 * inch, box_y + box_h - 0.4 * inch, "HARD RULES")

    rules = [
        "Hook hits early",
        "Bridge always modulates with a key change",
        "Intro is always instrumental unless requested",
        "Target song length 2:30 to 3:30",
        "No background vocals unless requested",
    ]
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 12)
    for i, rule in enumerate(rules):
        c.drawString(box_x + 0.3 * inch, box_y + box_h - 0.8 * inch - i * 0.27 * inch,
                     "• " + rule)

    footer(c, w)
    c.showPage()
    c.save()
    print(f"  ✓ {path.name}")


# ─── 3. Cliché Blacklist Card ─────────────────────────────────
def cliche_blacklist():
    path = OUT_DIR / "03-cliche-blacklist-card.pdf"
    w, h = portrait(letter)
    c = canvas.Canvas(str(path), pagesize=portrait(letter))
    fill_bg(c, w, h)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 36)
    c.drawCentredString(w / 2, h - 1.0 * inch, "THE CLICHÉ BLACKLIST")

    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 13)
    c.drawCentredString(w / 2, h - 1.4 * inch,
                        "Words that make AI lyrics sound like AI lyrics")

    cliches = [
        ("in my chest", "Overused trope"),
        ("pressure makes me fold", "Tired metaphor"),
        ("flame", "Vague imagery"),
        ("light", "Vague imagery"),
        ("storm", "Cliché metaphor"),
        ("scars", "Cliché metaphor"),
        ("manifest", "Unless theological"),
    ]

    cols = 2
    card_w = 3.0 * inch
    card_h = 1.0 * inch
    h_gap = 0.4 * inch
    v_gap = 0.25 * inch
    grid_w = cols * card_w + (cols - 1) * h_gap
    start_x = (w - grid_w) / 2
    start_y = h - 2.2 * inch

    for i, (phrase, reason) in enumerate(cliches):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + h_gap)
        y = start_y - row * (card_h + v_gap)

        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.setFillColor(DARK)
        c.rect(x, y - card_h, card_w, card_h, fill=1, stroke=1)

        # Phrase with strikethrough
        c.setFillColor(WHITE)
        c.setFont(FONT_BLACK, 18)
        text_y = y - 0.45 * inch
        c.drawCentredString(x + card_w / 2, text_y, phrase)
        # Red strikethrough
        c.setStrokeColor(RED)
        c.setLineWidth(2.5)
        text_w = c.stringWidth(phrase, FONT_BLACK, 18)
        line_x1 = x + card_w / 2 - text_w / 2 - 4
        line_x2 = x + card_w / 2 + text_w / 2 + 4
        c.line(line_x1, text_y + 5, line_x2, text_y + 5)

        c.setFillColor(ORANGE)
        c.setFont(FONT_REG, 11)
        c.drawCentredString(x + card_w / 2, y - card_h + 0.2 * inch, reason)

    # Footer note
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 11)
    c.drawCentredString(w / 2, 1.1 * inch,
                        "Suno Writer enforces this list automatically.")
    c.drawCentredString(w / 2, 0.9 * inch,
                        "If one slips, type 'rewrite without the cliché in line X'.")

    footer(c, w)
    c.showPage()
    c.save()
    print(f"  ✓ {path.name}")


# ─── 4. Workflow Flowchart ────────────────────────────────────
def workflow_flowchart():
    path = OUT_DIR / "04-workflow-flowchart.pdf"
    w, h = landscape(letter)
    c = canvas.Canvas(str(path), pagesize=landscape(letter))
    fill_bg(c, w, h)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 32)
    c.drawString(0.6 * inch, h - 0.9 * inch, "IDEA TO RELEASED TRACK")
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 14)
    c.drawString(0.6 * inch, h - 1.2 * inch, "The Myind Sound workflow")

    steps = [
        ("1", "Mood Board", "Capture the vibe"),
        ("2", "Analysis", "Reference a track"),
        ("3", "Save DNA", "Lock the fingerprint"),
        ("4", "Sample Maker", "Drumless chop"),
        ("5", "Instrumental", "Build the beat"),
        ("6", "Songwriting", "Write the song"),
        ("7", "Arrange", "Section by section"),
        ("8", "Compile", "Paste into Suno"),
        ("9", "Clean & Prep", "Release ready"),
        ("10", "Ship", "Save and post"),
    ]

    # Two rows of 5
    cols = 5
    node_r = 0.35 * inch
    col_gap = (w - 1.2 * inch) / cols
    row1_y = h - 3.0 * inch
    row2_y = h - 5.0 * inch

    positions = []
    for i, (n, label, desc) in enumerate(steps):
        if i < 5:
            x = 0.6 * inch + col_gap * i + col_gap / 2
            y = row1_y
        else:
            # Second row reversed for U-shape
            x = 0.6 * inch + col_gap * (9 - i) + col_gap / 2
            y = row2_y
        positions.append((x, y))

        # Circle node
        c.setFillColor(GOLD)
        c.circle(x, y, node_r, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont(FONT_BLACK, 18)
        c.drawCentredString(x, y - 6, n)

        # Label
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 12)
        c.drawCentredString(x, y - node_r - 0.25 * inch, label)
        c.setFillColor(ORANGE)
        c.setFont(FONT_REG, 9)
        c.drawCentredString(x, y - node_r - 0.45 * inch, desc)

    # Arrows between nodes
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2.5)
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        if i == 4:
            # Drop down (5 → 6)
            c.line(x1 + node_r, y1, x1 + node_r + 0.2 * inch, y1)
            c.line(x1 + node_r + 0.2 * inch, y1, x1 + node_r + 0.2 * inch, y2)
            c.line(x1 + node_r + 0.2 * inch, y2, x2 + node_r, y2)
        elif i < 4:
            c.line(x1 + node_r, y1, x2 - node_r, y2)
        else:
            # Right to left in row 2
            c.line(x1 - node_r, y1, x2 + node_r, y2)

    footer(c, w)
    c.showPage()
    c.save()
    print(f"  ✓ {path.name}")


# ─── 5. Module 1 Index Handout ────────────────────────────────
def module_index():
    path = OUT_DIR / "05-module-1-index.pdf"
    w, h = portrait(letter)
    c = canvas.Canvas(str(path), pagesize=portrait(letter))
    fill_bg(c, w, h)

    c.setFillColor(GOLD)
    c.setFont(FONT_BLACK, 26)
    c.drawCentredString(w / 2, h - 0.9 * inch, "MODULE 01")
    c.setFont(FONT_BLACK, 22)
    c.drawCentredString(w / 2, h - 1.3 * inch, "SUNO WRITER BY MYIND SOUND")
    c.setFillColor(WHITE)
    c.setFont(FONT_REG, 13)
    c.drawCentredString(w / 2, h - 1.6 * inch, "Idea to released track in one module")

    lessons = [
        ("01", "Welcome to Suno Writer", "5 min"),
        ("02", "The Interface Tour", "8 min"),
        ("03", "Your First Login & Setup", "4 min"),
        ("04", "Songwriting Mode", "15 min"),
        ("05", "Instrumental / Remix Mode", "12 min"),
        ("06", "Sample Maker Mode", "10 min"),
        ("07", "Sample Analysis Mode", "12 min"),
        ("08", "The Arrange View", "10 min"),
        ("09", "The Mood Board View", "8 min"),
        ("10", "DNA Profiles", "12 min"),
        ("11", "Saved Works, Templates & Collab", "10 min"),
        ("12", "Release Prep & Clean Lyrics", "8 min"),
        ("13", "End-to-End Workflow (Capstone)", "20 min"),
        ("14", "Tips, Shortcuts & Troubleshooting", "8 min"),
        ("15", "Module Recap & Challenge", "5 min"),
    ]

    row_h = 0.32 * inch
    table_top = h - 2.1 * inch
    left = 0.8 * inch
    right = w - 0.8 * inch
    table_w = right - left

    for i, (n, title, dur) in enumerate(lessons):
        y = table_top - i * row_h
        if i % 2 == 0:
            c.setFillColor(DARK_ALT)
            c.rect(left, y - row_h + 0.05 * inch, table_w, row_h, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont(FONT_BLACK, 14)
        c.drawString(left + 0.15 * inch, y - 0.18 * inch, n)
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 12)
        c.drawString(left + 0.7 * inch, y - 0.18 * inch, title)
        c.setFillColor(ORANGE)
        c.setFont(FONT_REG, 11)
        c.drawRightString(right - 0.15 * inch, y - 0.18 * inch, dur)

    # Total run time
    total_y = table_top - len(lessons) * row_h - 0.2 * inch
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 11)
    c.drawCentredString(w / 2, total_y, "TOTAL RUN TIME: ~2 hr 27 min")

    # CTA box
    cta_h = 0.85 * inch
    cta_y = 0.85 * inch
    c.setFillColor(GOLD)
    c.rect(left, cta_y, table_w, cta_h, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont(FONT_BLACK, 16)
    c.drawCentredString(w / 2, cta_y + cta_h - 0.35 * inch, "START WITH LESSON 01")
    c.setFont(FONT_REG, 12)
    c.drawCentredString(w / 2, cta_y + 0.2 * inch, "Then ship the capstone in Lesson 13")

    footer(c, w)
    c.showPage()
    c.save()
    print(f"  ✓ {path.name}")


if __name__ == "__main__":
    print("Rendering Module 01 PDFs...")
    interface_cheat_sheet()
    song_structure_card()
    cliche_blacklist()
    workflow_flowchart()
    module_index()
    print(f"\nDone. Output: {OUT_DIR}")
