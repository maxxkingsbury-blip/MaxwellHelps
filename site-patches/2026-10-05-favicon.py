"""Site patch 2026-10-05: add favicon links (favicon.ico, favicon.svg, apple-touch-icon.png)
to every page. The icon files live in the repo root.
Idempotent: safe to run more than once."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ANCHOR = '<link rel="stylesheet" href="styles.css">'
LINKS = ('<link rel="icon" href="favicon.ico" sizes="32x32">\n'
         '<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
         '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')

for page in ["index.html", "medicare-101.html", "privacy.html", "cookies.html", "terms.html"]:
    p = ROOT / page
    t = p.read_text(encoding="utf-8")
    if 'href="favicon.svg"' in t:
        continue
    if t.count(ANCHOR) != 1:
        raise SystemExit(f"{page}: expected exactly one match for {ANCHOR!r}")
    t = t.replace(ANCHOR, LINKS + ANCHOR)
    p.write_text(t, encoding="utf-8")
print("patch applied")
