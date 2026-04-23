# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio website for Martin Hendrych — UA & Ad Monetization Specialist. Static site, no build step. Open `index.html` directly in a browser or use a local server:

```
npx serve .
# or
python -m http.server 8080
```

## Architecture

Three files, no framework, no bundler:

- **index.html** — All markup. Single-page with anchor sections: `#hero`, `#stats`, `#about`, `#skills`, `#clients`, `#contact`.
- **styles.css** — All styles. CSS custom properties defined in `:root` control the entire color scheme (`--black`, `--white`, `--yellow`, `--yellow-hover`, `--gray-*`). Responsive breakpoints at 1024px, 768px, 480px.
- **script.js** — Four behaviors: AOS init, navbar scroll class toggle, mobile hamburger menu, animated stat counters (IntersectionObserver), active nav link highlighting.

## External Dependencies (CDN only)

- **AOS 2.3.1** — scroll-triggered fade/slide animations. Configured once in `script.js` (`duration: 700, once: true`). Add `data-aos="fade-up"` + optional `data-aos-delay` to any element.
- **Google Fonts** — Space Grotesk (headings) + Inter (body). Referenced via `--font-heading` / `--font-body` CSS vars.
- **FormSubmit.co** — handles the contact form POST with no backend. Target email set via `action="https://formsubmit.co/martin.naysik.hendrych@gmail.com"`.

## Key Design Decisions

- The hero image is currently an `MH` initials placeholder (`.image-placeholder`). A real photo would go inside it as an `<img>` tag.
- Stat counters (`data-target` attribute) animate from 0 on first scroll into view — change the displayed number by updating `data-target` on the `.counter` span.
- The yellow accent color (`#FFD600`) is the single brand color used for highlights, tags, hover states, and CTA buttons. Keep changes to this centralized in `--yellow`.

## Git Workflow

Commit and push after every meaningful change:

```
git add <specific files>
git commit -m "descriptive message"
git push
```

Remote: `https://github.com/nAysik/PersonalWeb.git` (branch: `main`)
