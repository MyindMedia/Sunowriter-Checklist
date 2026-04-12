# Module 01 — Build & Ship Checklist

Track everything end to end. Check items off as you go. Goal: Module 1 live on Netlify with all 15 lessons recorded, edited, captioned, and accessible to community members.

---

## Phase 1 — Pre-Production (do once before any recording)

- [ ] Read `00-INDEX.md` start to finish
- [ ] Skim every lesson script once so the flow is in your head
- [ ] Confirm Suno Writer login works on the machine you will record from
- [ ] Open a Suno account in a second browser tab for live demos
- [ ] Pick the reference track you will use across Lessons 04, 05, 13
- [ ] Pick the audio file you will upload in Lesson 07 (Sample Analysis)
- [ ] Set Help tooltips ON in Suno Writer for the entire recording session
- [ ] Set Default Mode to Songwriting
- [ ] Close every notification source (Slack, Discord, Mail, Messages)
- [ ] Test mic level and screen recorder (Screen Studio recommended)
- [ ] Set screen recording resolution to 1920×1080
- [ ] Apply your Screen Studio brand preset (dark background, gold accents)

---

## Phase 2 — Record the 15 Lessons

For each lesson: open the script file, screen record while reading the narration, save raw file as `lesson-NN-raw.mov`.

- [ ] Lesson 01 — Welcome to Suno Writer (5 min) — `01-welcome.md`
- [ ] Lesson 02 — The Interface Tour (8 min) — `02-interface-tour.md`
- [ ] Lesson 03 — Your First Login & Setup (4 min) — `03-first-login.md`
- [ ] Lesson 04 — Songwriting Mode (15 min) — `04-songwriting-mode.md`
- [ ] Lesson 05 — Instrumental / Remix Mode (12 min) — `05-instrumental-mode.md`
- [ ] Lesson 06 — Sample Maker Mode (10 min) — `06-sample-maker.md`
- [ ] Lesson 07 — Sample Analysis Mode (12 min) — `07-sample-analysis.md`
- [ ] Lesson 08 — The Arrange View (10 min) — `08-arrange-view.md`
- [ ] Lesson 09 — The Mood Board View (8 min) — `09-mood-board.md`
- [ ] Lesson 10 — DNA Profiles (12 min) — `10-dna-profiles.md`
- [ ] Lesson 11 — Saved Works, Templates & Collab (10 min) — `11-saved-works-templates-collab.md`
- [ ] Lesson 12 — Release Prep & Clean Lyrics (8 min) — `12-release-prep-clean-lyrics.md`
- [ ] Lesson 13 — End-to-End Workflow Capstone (20 min) — `13-end-to-end-workflow.md`
- [ ] Lesson 14 — Tips, Shortcuts & Troubleshooting (8 min) — `14-tips-troubleshooting.md`
- [ ] Lesson 15 — Module Recap & Challenge (5 min) — `15-recap-challenge.md`

---

## Phase 3 — Edit Each Lesson

For each lesson run this list:

- [ ] Trim head and tail
- [ ] Add cold-open hook from script
- [ ] Add gold `#FDB913` kinetic text overlays per Text Overlays section
- [ ] Add lower thirds where the script calls for face cam
- [ ] Add intro and outro brand sting (3 sec each)
- [ ] Color correct dark theme to match `#1A1A1A`
- [ ] Normalize audio to -16 LUFS
- [ ] Export H.264 MP4 at 1080p
- [ ] Save as `lesson-NN-final.mp4`

Per-lesson edit checkboxes:
- [ ] L01 edited
- [ ] L02 edited
- [ ] L03 edited
- [ ] L04 edited
- [ ] L05 edited
- [ ] L06 edited
- [ ] L07 edited
- [ ] L08 edited
- [ ] L09 edited
- [ ] L10 edited
- [ ] L11 edited
- [ ] L12 edited
- [ ] L13 edited
- [ ] L14 edited
- [ ] L15 edited

---

## Phase 4 — Captions & Transcripts

- [ ] Generate captions (Whisper, Descript, or Screen Studio captions)
- [ ] Review and clean captions for each lesson
- [ ] Export `.vtt` file per lesson for the LMS player
- [ ] Save full transcript as `lesson-NN-transcript.txt`

---

## Phase 5 — Copy-Paste Sections (LMS module pages)

For each lesson, copy the **Context** and **What You Will Learn** blocks from the lesson markdown into the LMS module page.

- [ ] L01 context pasted into LMS
- [ ] L02 context pasted into LMS
- [ ] L03 context pasted into LMS
- [ ] L04 context pasted into LMS
- [ ] L05 context pasted into LMS
- [ ] L06 context pasted into LMS
- [ ] L07 context pasted into LMS
- [ ] L08 context pasted into LMS
- [ ] L09 context pasted into LMS
- [ ] L10 context pasted into LMS
- [ ] L11 context pasted into LMS
- [ ] L12 context pasted into LMS
- [ ] L13 context pasted into LMS
- [ ] L14 context pasted into LMS
- [ ] L15 context pasted into LMS

For each lesson, also paste the **Step-by-Step Guide** as a member-facing checklist:

- [ ] L01 step guide pasted
- [ ] L02 step guide pasted
- [ ] L03 step guide pasted
- [ ] L04 step guide pasted
- [ ] L05 step guide pasted
- [ ] L06 step guide pasted
- [ ] L07 step guide pasted
- [ ] L08 step guide pasted
- [ ] L09 step guide pasted
- [ ] L10 step guide pasted
- [ ] L11 step guide pasted
- [ ] L12 step guide pasted
- [ ] L13 step guide pasted
- [ ] L14 step guide pasted
- [ ] L15 step guide pasted

---

## Phase 6 — Resource Assets (PDFs and downloads)

PDF resources are already rendered to `Resources/PDFs/`. Verify each opens cleanly, then upload.

- [ ] `01-interface-cheat-sheet.pdf` opens, layout looks right
- [ ] `02-song-structure-card.pdf` opens, energy chart looks right
- [ ] `03-cliche-blacklist-card.pdf` opens, strikethroughs aligned
- [ ] `04-workflow-flowchart.pdf` opens, U-flow connects
- [ ] `05-module-1-index.pdf` opens, all 15 lessons listed

Optional polish on PDFs (only if a designer is hands-on):
- [ ] Replace placeholder dashboard screenshot in `01-interface-cheat-sheet.pdf` with a real annotated capture
- [ ] Re-export with embedded Inter font (currently uses Helvetica fallback)
- [ ] Add Myind Sound logo to footer of every PDF

Other assets to produce:
- [ ] Sample Chop Starter Pack (3 demo MP3 loops from Sample Maker Mode) saved as `sample-pack.zip`
- [ ] Module 1 thumbnail image (1920×1080) for LMS hero
- [ ] Module 1 vertical promo card (1080×1920) for IG Stories
- [ ] Lesson thumbnails (15 × 1280×720) for video player
- [ ] Welcome email graphic with Module 1 Index PDF attached

Asset upload checklist:
- [ ] All 5 PDFs uploaded to LMS
- [ ] Sample Pack zip uploaded
- [ ] Lesson thumbnails uploaded
- [ ] Module hero image uploaded

---

## Phase 7 — Build the Static Site (for Netlify hosting)

Goal: a brand-styled static site that hosts Module 1, embeds the videos, links the PDFs, and gates access via the Myind Sound community.

Structure:
```
suno-writer-tutorials/
├── index.html               (Module 1 landing page)
├── lessons/
│   ├── 01-welcome.html
│   ├── 02-interface-tour.html
│   └── ... (15 lessons)
├── resources/
│   └── pdfs/                (5 PDFs)
├── assets/
│   ├── css/
│   │   └── brand.css        (#1A1A1A, #FDB913, #FF8C00, Inter)
│   ├── js/
│   └── img/
└── netlify.toml
```

Tasks:
- [ ] Create `suno-writer-tutorials/` folder
- [ ] Build `brand.css` using palette `#1A1A1A` `#FDB913` `#FF8C00` `#FFFFFF`
- [ ] Build `index.html` Module 1 landing page (lesson grid)
- [ ] Build a lesson template `lesson-template.html`
- [ ] Generate 15 lesson HTML pages from the markdown
- [ ] Embed video player (Vimeo private, Bunny.net, or self-hosted MP4)
- [ ] Link the 5 PDFs in the resources section of each relevant lesson
- [ ] Add navigation (prev / next lesson)
- [ ] Add progress indicator (member can see what they have completed)
- [ ] Add the community challenge submission link in Lesson 15
- [ ] Test on mobile, tablet, desktop

---

## Phase 8 — Netlify Deployment

- [ ] Create a Git repo for `suno-writer-tutorials/`
- [ ] Push to GitHub (private repo recommended)
- [ ] Connect repo to Netlify
- [ ] Configure build settings (no build step needed for static HTML)
- [ ] Set custom domain (e.g. `tutorials.myindsound.com`)
- [ ] Add Netlify Identity or Netlify Edge Function for community access gating
- [ ] Connect access list to Myind Sound community membership (GHL webhook or magic link)
- [ ] Set up a 404 page (brand styled)
- [ ] Set up redirects for old URLs if needed
- [ ] Enable HTTPS (Netlify auto)
- [ ] Set up form for community challenge submissions (Netlify Forms)
- [ ] Test login flow with a real community member email
- [ ] Verify gated content is not accessible without auth
- [ ] Submit sitemap to search if not gated

Optional Netlify add-ons:
- [ ] Netlify Analytics for page views
- [ ] Netlify Forms for challenge submissions
- [ ] Netlify Functions for any dynamic gating

---

## Phase 9 — Soft Launch (internal)

- [ ] Walk the site yourself end to end
- [ ] Have one trusted community member walk it end to end
- [ ] Collect feedback and fix top 3 issues
- [ ] Verify all 15 lessons play
- [ ] Verify all 5 PDFs download
- [ ] Verify community challenge submission works

---

## Phase 10 — Public Launch

- [ ] Send announcement email to community list
- [ ] Post launch carousel on @thamyind and @myind.sound
- [ ] Post launch reel (60 sec, talking head + b-roll from Lesson 13 capstone)
- [ ] Pin announcement in Discord / community channel
- [ ] Tag the first 5 members who complete the capstone
- [ ] Schedule a live Q&A inside the community 7 days after launch

---

## Ongoing (after launch)

- [ ] Watch the community challenge hashtag daily for first 14 days
- [ ] Comment on every submission
- [ ] Feature the best 3 capstone tracks in a community spotlight
- [ ] Track completion rate and identify drop-off lessons
- [ ] Plan Module 2 based on feedback
