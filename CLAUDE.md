# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio website for Martin Hendrych — UA & Ad Monetization Specialist.
Live at **https://hendrych.me** (Cloudflare Pages, direct upload).

**`dist/` is the live site.** Everything in it is what gets deployed; nothing outside it ships.
Two languages: English at `/`, Czech at `/cs/`. Both are generated from one template, so
design and copy never drift apart. Build, then preview:

```
python src/build.py
python -m http.server 8123 --directory dist
```

## Architecture

### `src/` — the source of truth

- **template.html** — the page layout with `{{key}}` placeholders. All markup, CSS and JS.
- **strings.json** — every user-visible string, per language (`en`, `cs`). Copy changes go here.
- **build.py** — renders `dist/index.html` (EN) and `dist/cs/index.html` (CS) from the two files
  above, and regenerates `dist/sitemap.xml` with hreflang alternates.
- **make_og.py** — regenerates the social cards. Only needed if the headline copy or brand
  colours change.

### `dist/` — the deployed site, GENERATED

**Never edit `dist/*.html` by hand — the next build overwrites it.** Edit `src/` and rebuild.

- **index.html** (EN), **cs/index.html** (CS) — generated
- **sitemap.xml** — generated
- **404.html** — hand-maintained, English only, served for unknown paths in both languages
- **_headers** — Cloudflare header rules (security headers + long cache on images/SVG)
- **robots.txt**, **favicon.svg**, **favicon-32.png**, **apple-touch-icon.png**,
  **og.png** (EN), **og-cs.png** (CS)

### Root — legacy experiments, NOT deployed

`index.html` + `styles.css` + `script.js` are the original yellow-accent design. `index2.html`
(dark glassmorphism) and `prompts.html` are earlier explorations. Keep for reference; editing
them changes nothing on the live site.

## Languages

English at `/`, Czech at `/cs/`. English is the default and `x-default`.

Both pages carry the full hreflang set and a language switcher (in the nav on desktop, at the
bottom of the mobile menu below 768px). The contact form's `_subject` is tagged `(EN)` / `(CS)`
so you can tell which version a message came from.

**Adding a string:** add the key to BOTH `en` and `cs` in `strings.json`, then reference it as
`{{key}}` in `template.html`. The build fails loudly if the two languages define different keys,
or if a `{{placeholder}}` in the template has no value.

Czech copy deliberately keeps English industry terms (user acquisition, ad monetization, eCPM,
mediation, ASO) — that is how Czech ad-tech is actually written, and translating them reads as
amateurish to the audience.

## External Dependencies (CDN only)

- **GSAP 3.12.5 + ScrollTrigger** — all motion in `dist/index.html`. Everything is progressive
  enhancement: without JS, without GSAP, or under `prefers-reduced-motion`, the full content still
  renders (guarded by the `animate` flag and the `.js-anim` / `.no-anim` classes).
- **Google Fonts** — Bricolage Grotesque (display) + Hanken Grotesk (body), via `--font-display` /
  `--font-body`.
- **FormSubmit.co** — contact form POST, no backend. Target email is in the form `action`.

## Key Design Decisions

- Color scheme lives entirely in `:root` custom properties. `--teal` (`#00D1C1`) and `--teal-deep`
  (`#0B7E74`) are the single brand accent — change them there, not at call sites.
- Metric counters animate from 0 on scroll into view; the displayed number comes from `data-target`
  on the `.count` span, and the bar underneath from `data-fill` (0–1) on `.metric-bar i`.
- Motion is GPU-safe props only (transform / opacity / clip-path). Pointer-driven effects (tilt,
  magnetic buttons, mouse parallax) are gated behind `pointer: fine`.
- "Selected work" is a single full-width two-column card. If a second client is added, restore
  `grid-template-columns: 1fr 1fr` on `.work-grid`.

## Deployment

Cloudflare **Worker with static assets** (project `workwebhendrych`), **direct upload** — not
git-connected, so pushing to GitHub does NOT deploy.

1. Rebuild the pages, then the upload archive:
   ```
   python src/build.py
   python -c "import zipfile,os; z=zipfile.ZipFile('hendrych-me-site.zip','w',zipfile.ZIP_DEFLATED); [z.write(os.path.join(r,f), os.path.relpath(os.path.join(r,f),'dist')) for r,_,fs in os.walk('dist') for f in fs]; z.close()"
   ```
   Files must sit at the zip root, not nested under `dist/`.
2. Cloudflare dashboard → Workers & Pages → `workwebhendrych` → **New deployment** → upload the zip.

The zip is a build artifact and is gitignored.

## Domain & mail

- `hendrych.me` and `www.hendrych.me` both serve the site; SSL/TLS mode is Full (strict).
- `martin@hendrych.me` receives via Cloudflare Email Routing, forwarded to Gmail; sending uses
  Gmail "send mail as" over `smtp.gmail.com`.
- SPF covers both paths: `v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all`.
- DMARC stays at `p=none` — Gmail send-as signs as `gmail.com`, so a strict policy would
  quarantine Martin's own replies.

## Git Workflow

Commit and push after every meaningful change:

```
git add <specific files>
git commit -m "descriptive message"
git push
```

Remote: `https://github.com/nAysik/PersonalWeb.git` (working branch: `master`)
