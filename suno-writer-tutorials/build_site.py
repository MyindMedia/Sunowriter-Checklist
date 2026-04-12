"""
Build the Suno Writer Tutorials static site from the lesson markdown files.

Reads ../*.md (lessons 01-15) and renders Netlify-ready HTML into ./lessons/
plus an index.html landing page and a 404.html.

Setup:
    pip3 install --break-system-packages markdown

Run:
    python3 build_site.py
"""

from pathlib import Path
import re
import markdown

ROOT = Path(__file__).parent
LESSONS_SRC = ROOT.parent  # Module-01-Suno-Writer/
LESSONS_OUT = ROOT / "lessons"
LESSONS_OUT.mkdir(exist_ok=True)

LESSON_FILES = [
    ("01", "01-welcome.md", "Welcome to Suno Writer", "5 min"),
    ("02", "02-interface-tour.md", "The Interface Tour", "8 min"),
    ("03", "03-first-login.md", "Your First Login & Setup", "4 min"),
    ("04", "04-songwriting-mode.md", "Songwriting Mode", "15 min"),
    ("05", "05-instrumental-mode.md", "Instrumental / Remix Mode", "12 min"),
    ("06", "06-sample-maker.md", "Sample Maker Mode", "10 min"),
    ("07", "07-sample-analysis.md", "Sample Analysis Mode", "12 min"),
    ("08", "08-arrange-view.md", "The Arrange View", "10 min"),
    ("09", "09-mood-board.md", "The Mood Board View", "8 min"),
    ("10", "10-dna-profiles.md", "DNA Profiles", "12 min"),
    ("11", "11-saved-works-templates-collab.md", "Saved Works, Templates & Collab", "10 min"),
    ("12", "12-release-prep-clean-lyrics.md", "Release Prep & Clean Lyrics", "8 min"),
    ("13", "13-end-to-end-workflow.md", "End-to-End Workflow (Capstone)", "20 min"),
    ("14", "14-tips-troubleshooting.md", "Tips, Shortcuts & Troubleshooting", "8 min"),
    ("15", "15-recap-challenge.md", "Module Recap & Challenge", "5 min"),
]

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Suno Writer Tutorials</title>
  <link rel="stylesheet" href="../assets/css/brand.css">
</head>
<body>
  <header class="site-header">
    <div class="container brand">
      <a href="../index.html" class="logo">SUNO WRITER TUTORIALS</a>
      <nav>
        <a href="../index.html">All Lessons</a>
        <a href="../resources/pdfs/05-module-1-index.pdf">Module Index PDF</a>
      </nav>
    </div>
  </header>

  <main class="container lesson-page">
    <div class="breadcrumb"><a href="../index.html">Module 01</a> / Lesson {num}</div>
    <h1>{title}</h1>
    <div class="meta"><span>Duration:</span> {duration}</div>

    <div class="video-wrap">
      <div class="video-placeholder">[ Lesson video embeds here ]</div>
      <!-- Replace with: <iframe src="https://player.vimeo.com/video/XXXXXXXXX" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe> -->
    </div>

    <div class="content">
      {body}
    </div>

    <div class="resources">
      <h2>Resources</h2>
      <a href="../resources/pdfs/05-module-1-index.pdf">Module 01 Index PDF</a>
      <a href="../resources/pdfs/02-song-structure-card.pdf">Song Structure Card</a>
      <a href="../resources/pdfs/03-cliche-blacklist-card.pdf">Cliché Blacklist</a>
      <a href="../resources/pdfs/04-workflow-flowchart.pdf">Workflow Flowchart</a>
    </div>

    <nav class="pager">
      {prev_link}
      {next_link}
    </nav>
  </main>

  <footer class="site-footer">
    <div class="container">Myind Sound Music Club / Suno Writer v2.0</div>
  </footer>
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Module 01 — Suno Writer by Myind Sound</title>
  <link rel="stylesheet" href="assets/css/brand.css">
</head>
<body>
  <header class="site-header">
    <div class="container brand">
      <a href="index.html" class="logo">SUNO WRITER TUTORIALS</a>
      <nav>
        <a href="resources/pdfs/05-module-1-index.pdf">Module Index PDF</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <div class="label">Module 01</div>
      <h1>SUNO WRITER<br>BY MYIND SOUND</h1>
      <p>Idea to released track in one module. 15 lessons, 4 modes, 3 views, one workflow that ships finished music.</p>
    </section>

    <section class="lesson-grid">
{cards}
    </section>

    <section class="cta">
      <h2>Ready to ship?</h2>
      <p>The capstone challenge in Lesson 13 takes you from idea to released track in 20 minutes.</p>
      <a href="lessons/13-end-to-end-workflow.html">Start the capstone</a>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">Myind Sound Music Club / Suno Writer v2.0</div>
  </footer>
</body>
</html>
"""

CARD_TEMPLATE = """      <a href="lessons/{slug}.html" class="lesson-card">
        <div class="number">LESSON {num}</div>
        <div class="title">{title}</div>
        <div class="duration">{duration}</div>
      </a>"""

NOT_FOUND_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Not Found — Suno Writer Tutorials</title>
  <link rel="stylesheet" href="/assets/css/brand.css">
</head>
<body>
  <main class="container hero" style="text-align:center;">
    <div class="label">404</div>
    <h1>Lost in the rack</h1>
    <p>That lesson does not exist. Head back to the module index.</p>
    <p><a href="/" style="color:#FDB913;font-weight:700;">← Back to Module 01</a></p>
  </main>
</body>
</html>
"""


def md_to_html(md_text):
    return markdown.markdown(md_text, extensions=["tables", "fenced_code"])


def extract_body(md_text):
    """Strip the YAML-style header (Duration / Outcome / Prerequisites lines) and the
    'Screen Recording Script' + 'Shot List' + 'Text Overlays' sections — those are
    for the producer, not the member."""
    lines = md_text.splitlines()
    out = []
    skip_until_next_h2 = False
    skip_sections = {
        "## Screen Recording Script",
        "## Shot List",
        "## Text Overlays (gold #FDB913)",
        "## Text Overlays",
        "## Resources to Link in the LMS",
    }
    for line in lines:
        if line.strip() in skip_sections or any(line.startswith(s) for s in skip_sections):
            skip_until_next_h2 = True
            continue
        if skip_until_next_h2:
            if line.startswith("## ") and line.strip() not in skip_sections:
                skip_until_next_h2 = False
            else:
                continue
        out.append(line)
    return "\n".join(out)


def slug(filename):
    return filename.replace(".md", "")


def build_lessons():
    for i, (num, fname, title, duration) in enumerate(LESSON_FILES):
        src = LESSONS_SRC / fname
        if not src.exists():
            print(f"  ! missing {fname}")
            continue
        md_text = src.read_text()
        body_md = extract_body(md_text)
        body_html = md_to_html(body_md)

        prev_link = ""
        next_link = ""
        if i > 0:
            p = LESSON_FILES[i - 1]
            prev_link = f'<a href="{slug(p[1])}.html" class="prev">← Lesson {p[0]}: {p[2]}</a>'
        else:
            prev_link = '<a href="../index.html" class="prev">← Module Home</a>'
        if i < len(LESSON_FILES) - 1:
            n = LESSON_FILES[i + 1]
            next_link = f'<a href="{slug(n[1])}.html" class="next">Lesson {n[0]}: {n[2]} →</a>'
        else:
            next_link = '<a href="../index.html" class="next">Back to Module Home →</a>'

        html = PAGE_TEMPLATE.format(
            num=num, title=title, duration=duration,
            body=body_html, prev_link=prev_link, next_link=next_link,
        )
        out = LESSONS_OUT / f"{slug(fname)}.html"
        out.write_text(html)
        print(f"  ✓ lessons/{out.name}")


def build_index():
    cards = "\n".join(
        CARD_TEMPLATE.format(slug=slug(f[1]), num=f[0], title=f[2], duration=f[3])
        for f in LESSON_FILES
    )
    html = INDEX_TEMPLATE.format(cards=cards)
    (ROOT / "index.html").write_text(html)
    print("  ✓ index.html")


def build_404():
    (ROOT / "404.html").write_text(NOT_FOUND_HTML)
    print("  ✓ 404.html")


if __name__ == "__main__":
    print("Building Suno Writer Tutorials site...")
    build_lessons()
    build_index()
    build_404()
    print(f"\nDone. Open {ROOT / 'index.html'} in a browser.")
