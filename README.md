# frank-dixon.github.io

Personal site for **Frank Dixon** — Senior Full-Stack Engineer (front-end focus).

Static site for GitHub Pages. No build step for the main page.

## Preview locally

```bash
python3 -m http.server 8000
# or: npx serve .
```

Open [http://localhost:8000](http://localhost:8000).

## Deploy

Push to `https://github.com/frank-dixon/frank-dixon.github.io`, then **Settings → Pages** → deploy from `main` `/` (root). Site: **https://frank-dixon.github.io/**

## Contact & resume

| Item | Status |
|------|--------|
| **Email** | `fdixon7@gmail.com` (mailto on the site) |
| **Resume** | `resume.pdf` (from `resume.html`) |
| **Rabbit visualizer** | Hosted at `/rabbit/` → https://frank-dixon.github.io/rabbit/ |

Regenerate the PDF after editing `resume.html`:

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --disable-dev-shm-usage \
  --no-pdf-header-footer --print-to-pdf=resume.pdf resume.html
```

## What’s included

- `index.html` — editorial personal site (hero, about, work, projects, stack, contact)
- `rabbit/` — built Rabbit Genetics Visualizer (live demo)
- `resume.html` / `resume.pdf` — printable resume
- Phone is on the resume PDF only; public site uses email + LinkedIn

## Design notes

- Editorial / magazine: warm cream paper (`#F3EEE4`), ink type, raspdark turquoise/wine accent (`#9A3458`)
- Type: Fraunces (display) + Source Sans 3 (body). Punch via hierarchy, pull quote, rules, and an asymmetric grid — no neon, marquees, or glow orbs
- Professional work is outcome-framed; rabbit projects are personal experiments with a live `/rabbit/` demo
- Featured stack: Django, Python, JavaScript, HTML/CSS, Tailwind, accessibility, performance, Git — no React or TypeScript advertising on the portfolio

## License

Personal portfolio site. Content © Frank Dixon.
