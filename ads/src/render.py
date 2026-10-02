"""Render Facebook/Instagram ad images from ads/src/ads.json into ads/.

Runs automatically in GitHub Actions (.github/workflows/render-ads.yml)
whenever anything in ads/src/ changes. Each image is 1080x1080 PNG and is
served at https://maxwellhelps.com/ads/<file>.
"""
import json
import pathlib
import urllib.parse

from playwright.sync_api import sync_playwright

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent
TEMPLATE = (SRC / "template.html").as_uri()

ads = json.loads((SRC / "ads.json").read_text(encoding="utf-8"))

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1080})
    for ad in ads:
        query = urllib.parse.urlencode(
            {"h": ad["headline"], "s": ad.get("sub", ""), "c": ad["button"], "l": ad["layout"]}
        )
        page.goto(f"{TEMPLATE}?{query}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / ad["file"]))
        print("rendered", ad["file"])
    browser.close()
