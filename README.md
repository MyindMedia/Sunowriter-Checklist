# Suno Writer Tutorials — Module 01

The complete Module 01 build for the Myind Sound Music Club community: 15 lessons covering Suno Writer v2.0, brand-styled PDFs, a Netlify-ready static site, and a master build checklist.

## Structure

```
Module-01-Suno-Writer/
├── 00-INDEX.md                  Module index and brand standards
├── 01..15-*.md                  15 lesson scripts (context, step guide, narration, shot list)
├── CHECKLIST.md                 10-phase build & ship checklist
├── Resources/
│   ├── 01..05-*.md              Resource design specs
│   ├── render_pdfs.py           Renders all 5 PDFs with Inter font
│   ├── fonts/                   Inter Regular / Bold / Black TTFs
│   └── PDFs/                    Generated brand PDFs
├── suno-writer-tutorials/       Netlify-ready static site
│   ├── index.html               Module landing page
│   ├── lessons/*.html           15 lesson pages (auto-built)
│   ├── assets/css/brand.css     Full brand kit
│   ├── resources/pdfs/          PDF copies for download links
│   ├── build_site.py            Rebuilds site from lesson markdown
│   └── 404.html
├── netlify.toml                 Netlify config (publishes the site folder)
└── .gitignore
```

## Quick Start

### Render PDFs
```bash
python3 Resources/render_pdfs.py
```

### Build the site
```bash
python3 suno-writer-tutorials/build_site.py
```

### Preview locally
```bash
cd suno-writer-tutorials
python3 -m http.server 8000
```
Open http://localhost:8000

### Deploy to Netlify
1. Push this repo to GitHub
2. Connect to Netlify (no build command, publish dir = `suno-writer-tutorials`)
3. Add custom domain and Netlify Identity for community gating

## Brand Standard
- Background `#1A1A1A`
- Headlines gold `#FDB913`
- Body white `#FFFFFF`
- Accents orange `#FF8C00`
- Inter typography
- No em dashes anywhere

## Author
Lawrence "ThaMyind" Berment / Myind Sound Music Club
