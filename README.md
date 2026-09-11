# frank-dixon.github.io

Personal site for **Frank Dixon** — Senior Full-Stack Engineer (front-end focus).

Static, single-page site ready for GitHub Pages. No build step.

## Preview locally

From this directory:

```bash
# Python
python3 -m http.server 8000

# or Node
npx serve .
```

Then open [http://localhost:8000](http://localhost:8000).

Or simply open `index.html` in a browser (Tailwind loads from CDN, so you need network access).

## Deploy to GitHub Pages

1. Push this repo to `https://github.com/frank-dixon/frank-dixon.github.io`
2. In the repo: **Settings → Pages**
3. Source: **Deploy from a branch**
4. Branch: `main` (or `master`), folder: `/` (root)
5. Save — the site will be at **https://frank-dixon.github.io/**

User/organization sites served from `username.github.io` use the root of this repo; no `docs/` folder or Actions workflow is required for a plain static site.

### Custom domain (optional)

If you later want a custom domain, add a `CNAME` file at the repo root containing only your domain (e.g. `frankdixon.dev`), then configure DNS with your registrar. Do not add a CNAME file until you are ready.

## Placeholders to fill in

| Item | Where | Notes |
|------|--------|--------|
| **Email** | `index.html` — search for `YOUR_EMAIL_HERE@example.com` | Replace both the `mailto:` href and any visible placeholder text |
| **Resume** | Add `resume.pdf` in this folder | Contact section already links to `resume.pdf`; drop the file here when ready |

Until those are filled, LinkedIn remains the primary contact CTA.

## What’s included

- `index.html` — full page (hero, about, selected work, stack, contact)
- Tailwind CSS via CDN + small custom CSS for theme tokens, focus states, and dark mode (`prefers-color-scheme`)
- Minimal JS — copyright year only

## Design notes

- Mobile-first, calm senior aesthetic (Instrument Serif + DM Sans)
- Dark mode follows system preference
- Semantic HTML, skip link, visible focus rings, `prefers-reduced-motion` respected
- Professional work is outcome-framed and non-confidential; rabbit genetics projects are framed as personal experiments with live GitHub links

## License

Personal portfolio site. Content © Frank Dixon.
