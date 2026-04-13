"""
Build the GHL Build Checklist site from CHECKLIST.md.

Parses ../CHECKLIST.md, extracts each lesson's title, length, build subtasks,
copy blocks, and resources, then renders an interactive single-page site
into ./index.html.

Run:
    python3 build_checklist.py
"""

from pathlib import Path
import re
import html
import json

ROOT = Path(__file__).parent
SOURCE = ROOT.parent / "CHECKLIST.md"
OUT = ROOT / "index.html"


def parse_checklist(md):
    """Return list of lesson dicts."""
    lessons = []
    # Split by lesson headers
    parts = re.split(r"\n## LESSON ", md)
    for part in parts[1:]:  # skip preamble
        # Skip "Final Pre-Launch" and others — only lesson sections
        if not re.match(r"^\d+", part):
            continue

        first_line, rest = part.split("\n", 1)
        m = re.match(r"^(\d+)\s*—\s*(.+?)\s*$", first_line)
        if not m:
            continue
        num = m.group(1)
        title = m.group(2).strip()

        # Length
        length_m = re.search(r"\*\*Length:\*\*\s*(.+)", rest)
        length = length_m.group(1).strip() if length_m else ""

        # Build subtasks (- [ ] items under "GHL build:")
        subtasks = []
        build_block = re.search(r"GHL build:\n((?:- \[ \].+\n)+)", rest)
        if build_block:
            for line in build_block.group(1).splitlines():
                tm = re.match(r"- \[ \] (.+)", line)
                if tm:
                    subtasks.append(tm.group(1).strip())

        # Copy blocks: **>>> COPY — Label:**\n```\n...\n```
        copy_blocks = []
        for cm in re.finditer(
            r"\*\*>>> COPY\s*—\s*(.+?):\*\*\n```\n(.*?)\n```",
            rest,
            re.DOTALL,
        ):
            label = cm.group(1).strip()
            content = cm.group(2).rstrip()
            copy_blocks.append({"label": label, "content": content})

        # Resources
        resources = []
        res_block = re.search(
            r"\*\*Resources to attach:\*\*\n((?:- .+\n?)+)", rest
        )
        if res_block:
            for line in res_block.group(1).splitlines():
                rm = re.match(r"- `?([^`\n]+?)`?\s*$", line)
                if rm and "(none)" not in rm.group(1).lower() and "to be created" not in rm.group(1).lower():
                    resources.append(rm.group(1).strip())

        lessons.append({
            "num": num,
            "title": title,
            "length": length,
            "subtasks": subtasks,
            "copy_blocks": copy_blocks,
            "resources": resources,
        })
    return lessons


def render_lesson(lesson):
    subtasks_html = "\n".join(
        f'        <li><input type="checkbox" data-task="L{lesson["num"]}-{i}"><label>{html.escape(t)}</label></li>'
        for i, t in enumerate(lesson["subtasks"])
    )

    copy_blocks_html = ""
    for i, cb in enumerate(lesson["copy_blocks"]):
        content_escaped = html.escape(cb["content"])
        content_attr = json.dumps(cb["content"])
        is_prose = "body" in cb["label"].lower()
        block_class = "prose-block" if is_prose else "code-block"
        copy_blocks_html += f'''
      <div class="copy-block">
        <div class="copy-block-head">
          <h3>{html.escape(cb["label"])}</h3>
          <button class="copy-btn" data-copy='{html.escape(content_attr, quote=True)}'>Copy</button>
        </div>
        <pre class="{block_class}"><code>{content_escaped}</code></pre>
      </div>'''

    resources_html = ""
    if lesson["resources"]:
        items = "\n".join(
            f'''          <li class="resource-row">
            <div class="resource-name">
              <span class="paperclip">📎</span>
              <a href="resources/pdfs/{html.escape(r)}" target="_blank">{html.escape(r)}</a>
            </div>
            <div class="resource-url">
              <input type="url" placeholder="Paste GHL media URL after upload..." data-url="L{lesson["num"]}-R{i}" />
              <button class="url-copy-btn" data-url-target="L{lesson["num"]}-R{i}">Copy</button>
            </div>
          </li>'''
            for i, r in enumerate(lesson["resources"])
        )
        resources_html = f'''
      <div class="resources">
        <h3>Resources to Attach <span class="hint">(upload PDF to GHL → paste URL → copy into lesson)</span></h3>
        <ul>
{items}
        </ul>
      </div>'''

    total = len(lesson["subtasks"])
    thumb_path = f"assets/thumbs/lesson-{lesson['num'].zfill(2)}.png"
    return f'''
  <article class="lesson" data-lesson="L{lesson["num"]}" data-total="{total}">
    <div class="lesson-header">
      <div class="left">
        <span class="num">LESSON {lesson["num"]}</span>
        <h2>{html.escape(lesson["title"])}</h2>
      </div>
      <div style="display:flex;gap:16px;align-items:center;">
        <span class="duration">{html.escape(lesson["length"])}</span>
        <span class="lesson-status" data-lesson-status="L{lesson["num"]}">
          <span class="lesson-status-text">0 / {total}</span>
          <span class="lesson-status-bar"><span class="lesson-status-fill"></span></span>
        </span>
        <span class="toggle">▼</span>
      </div>
    </div>
    <div class="lesson-body" style="display:none;">
      <div class="thumb-block">
        <h3>Lesson Thumbnail</h3>
        <div class="thumb-wrap">
          <img src="{thumb_path}" alt="Lesson {lesson["num"]} thumbnail" loading="lazy" />
          <a href="{thumb_path}" download class="thumb-download">Download PNG</a>
        </div>
      </div>
      <div class="subtasks">
        <h3>GHL Build Steps</h3>
        <ul>
{subtasks_html}
        </ul>
      </div>
      {copy_blocks_html}
      {resources_html}
    </div>
  </article>'''


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Suno Writer — GHL Build Checklist</title>
  <link rel="stylesheet" href="assets/css/brand.css">
</head>
<body>
  <header class="site-header">
    <div class="container row">
      <div class="logo">SUNO WRITER<small>GHL BUILD CHECKLIST</small></div>
      <div class="progress"><div class="progress-bar" id="progressBar"></div></div>
      <div class="progress-text" id="progressText">0 / 0</div>
      <button class="reset" id="expandAllBtn">Expand All</button>
      <button class="reset" id="collapseAllBtn">Collapse All</button>
      <button class="reset" onclick="resetAll()">Reset</button>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <div class="label">Module 01</div>
      <h1>Build Module 01 in GHL</h1>
      <p>Single source of truth for building Suno Writer Module 01 inside the Myind Sound Music Club community. Open a lesson, copy the blocks straight into the GHL lesson editor, attach the resources, check it off, move to the next.</p>
    </section>

    <div class="howto">
      <h3>How to use this</h3>
      <ol>
        <li>Open GHL → Memberships → Myind Sound Music Club → Suno Writer module</li>
        <li>For each lesson below: click to expand, click each Copy button to grab the title / description / body</li>
        <li>Paste into the matching GHL field, upload the video, attach the listed resources</li>
        <li>Check off each step as you complete it (your progress saves automatically)</li>
        <li>When all 15 lessons are checked off, publish the module</li>
      </ol>
    </div>

    {lessons}
  </main>

  <footer class="site-footer">
    <div class="container">Myind Sound Music Club / Suno Writer v2.0 / Lawrence "ThaMyind" Berment</div>
  </footer>

  <script>
    // Persistent state via localStorage (checkboxes + resource URLs)
    const STORAGE_KEY = 'suno-writer-checklist-v1';
    const URL_KEY = 'suno-writer-resource-urls-v1';
    const state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
    const urls = JSON.parse(localStorage.getItem(URL_KEY) || '{{}}');

    function saveUrls() {{
      localStorage.setItem(URL_KEY, JSON.stringify(urls));
    }}

    function save() {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      updateProgress();
    }}

    function updateProgress() {{
      const all = document.querySelectorAll('.subtasks input[type="checkbox"]');
      const done = Array.from(all).filter(x => x.checked).length;
      const total = all.length;
      document.getElementById('progressBar').style.width = total ? (done / total * 100) + '%' : '0%';
      document.getElementById('progressText').textContent = done + ' / ' + total;

      // Per-lesson progress + done state
      document.querySelectorAll('.lesson').forEach(lesson => {{
        const boxes = lesson.querySelectorAll('input[type="checkbox"]');
        const lDone = Array.from(boxes).filter(b => b.checked).length;
        const lTotal = boxes.length;
        const allChecked = lTotal > 0 && lDone === lTotal;
        lesson.classList.toggle('done', allChecked);

        const statusEl = lesson.querySelector('.lesson-status');
        if (statusEl && lTotal > 0) {{
          const txt = statusEl.querySelector('.lesson-status-text');
          const fill = statusEl.querySelector('.lesson-status-fill');
          txt.textContent = allChecked ? '✓ Done' : (lDone + ' / ' + lTotal);
          fill.style.width = (lDone / lTotal * 100) + '%';
          statusEl.classList.toggle('complete', allChecked);
          statusEl.classList.toggle('in-progress', lDone > 0 && !allChecked);
        }}
      }});
    }}

    function setLessonOpen(lesson, open) {{
      const body = lesson.querySelector(':scope > .lesson-body');
      if (!body) return;
      body.style.display = open ? 'block' : 'none';
      lesson.classList.toggle('open', open);
    }}

    function isLessonOpen(lesson) {{
      const body = lesson.querySelector(':scope > .lesson-body');
      return body && body.style.display !== 'none';
    }}

    // Force every lesson closed on load
    document.querySelectorAll('.lesson').forEach(l => setLessonOpen(l, false));

    // Attach click handlers to each lesson header
    document.querySelectorAll('.lesson-header').forEach(header => {{
      header.addEventListener('click', (e) => {{
        if (e.target.closest('button, a, input')) return;
        const lesson = header.parentElement;
        setLessonOpen(lesson, !isLessonOpen(lesson));
      }});
    }});

    // Expand / Collapse All
    const expandBtn = document.getElementById('expandAllBtn');
    const collapseBtn = document.getElementById('collapseAllBtn');
    if (expandBtn) expandBtn.addEventListener('click', () => {{
      document.querySelectorAll('.lesson').forEach(l => setLessonOpen(l, true));
    }});
    if (collapseBtn) collapseBtn.addEventListener('click', () => {{
      document.querySelectorAll('.lesson').forEach(l => setLessonOpen(l, false));
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});

    function resetAll() {{
      if (!confirm('Reset all checklist progress AND saved resource URLs? This cannot be undone.')) return;
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(URL_KEY);
      location.reload();
    }}

    // Wire up checkboxes
    document.querySelectorAll('.subtasks input[type="checkbox"]').forEach(box => {{
      const key = box.dataset.task;
      if (state[key]) box.checked = true;
      box.addEventListener('change', () => {{
        state[key] = box.checked;
        box.parentElement.classList.toggle('done', box.checked);
        save();
      }});
      if (box.checked) box.parentElement.classList.add('done');
    }});

    // Wire up copy buttons
    document.querySelectorAll('.copy-btn').forEach(btn => {{
      btn.addEventListener('click', async (e) => {{
        e.stopPropagation();
        let text;
        try {{ text = JSON.parse(btn.dataset.copy); }}
        catch (err) {{ text = btn.dataset.copy; }}
        try {{
          await navigator.clipboard.writeText(text);
          const original = btn.textContent;
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(() => {{
            btn.textContent = original;
            btn.classList.remove('copied');
          }}, 1500);
        }} catch (err) {{
          alert('Copy failed. Select the text manually.');
        }}
      }});
    }});

    // Wire up resource URL inputs
    document.querySelectorAll('input[data-url]').forEach(input => {{
      const key = input.dataset.url;
      if (urls[key]) input.value = urls[key];
      input.addEventListener('input', () => {{
        urls[key] = input.value.trim();
        if (!urls[key]) delete urls[key];
        saveUrls();
      }});
    }});

    // Wire up resource URL copy buttons
    document.querySelectorAll('.url-copy-btn').forEach(btn => {{
      btn.addEventListener('click', async (e) => {{
        e.stopPropagation();
        const key = btn.dataset.urlTarget;
        const val = urls[key] || '';
        if (!val) {{
          alert('No URL saved yet. Upload the PDF to GHL, then paste the media URL into this field.');
          return;
        }}
        try {{
          await navigator.clipboard.writeText(val);
          const original = btn.textContent;
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(() => {{
            btn.textContent = original;
            btn.classList.remove('copied');
          }}, 1500);
        }} catch (err) {{
          alert('Copy failed. Select the text manually.');
        }}
      }});
    }});

    updateProgress();
  </script>
</body>
</html>
"""


def render_ghl_customization():
    css_path = ROOT.parent / "ghl-customization" / "custom.css"
    js_path = ROOT.parent / "ghl-customization" / "custom.js"
    css_content = css_path.read_text() if css_path.exists() else ""
    js_content = js_path.read_text() if js_path.exists() else ""

    blocks = [
        ("Custom CSS", css_content),
        ("Custom JavaScript", js_content),
    ]
    blocks_html = ""
    for label, content in blocks:
        content_attr = json.dumps(content)
        content_escaped = html.escape(content)
        blocks_html += f'''
      <div class="copy-block">
        <div class="copy-block-head">
          <h3>{html.escape(label)}</h3>
          <button class="copy-btn" data-copy='{html.escape(content_attr, quote=True)}'>Copy</button>
        </div>
        <pre class="code-block"><code>{content_escaped}</code></pre>
      </div>'''

    return f'''
  <article class="lesson ghl-custom" data-lesson="GHL-CUSTOM">
    <div class="lesson-header">
      <div class="left">
        <span class="num">GHL</span>
        <h2>Course Customization (Custom CSS + JS)</h2>
      </div>
      <div style="display:flex;gap:16px;align-items:center;">
        <span class="duration">One-time setup</span>
        <span class="toggle">▼</span>
      </div>
    </div>
    <div class="lesson-body" style="display:none;">
      <div class="ghl-custom-howto">
        <p>Open GHL → Memberships → Suno Writer Neural Engine → <strong>Details → Advanced</strong>. Paste the CSS into <strong>Custom CSS</strong> and the JS into <strong>Custom Javascript</strong>, then Save.</p>
      </div>
      {blocks_html}
    </div>
  </article>'''


def main():
    md = SOURCE.read_text()
    lessons = parse_checklist(md)
    print(f"Parsed {len(lessons)} lessons")
    ghl_html = render_ghl_customization()
    lessons_html = ghl_html + "\n".join(render_lesson(l) for l in lessons)
    out = HTML_TEMPLATE.format(lessons=lessons_html)
    OUT.write_text(out)
    print(f"Built {OUT}")


if __name__ == "__main__":
    main()
