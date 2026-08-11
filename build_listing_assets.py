#!/usr/bin/env python3
"""Build deterministic 1200x1200 CurioNest cover PNGs from catalog.json.

The renderer uses an installed Chromium browser in headless mode, so cover text is
HTML/CSS rather than AI-generated raster text. Preview PDFs remain a separate build
step and are not modified by this command.

Usage:
    python build_listing_assets.py CN-CH01-MATH
    python build_listing_assets.py all
"""

import argparse
import html
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def browser_path():
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    for name in ("msedge", "chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise RuntimeError("ไม่พบ Microsoft Edge/Google Chrome สำหรับ render cover")


def load_catalog():
    with (ROOT / "catalog.json").open("r", encoding="utf-8") as stream:
        return json.load(stream)


def asset_uri(relative_path):
    if not relative_path:
        return None
    path = (ROOT / relative_path).resolve()
    if not path.is_file():
        raise RuntimeError("ไม่พบ cover figure: {}".format(relative_path))
    return path.as_uri()


def cover_html(product):
    config = product.get("cover", {})
    title = html.escape(config.get("title", product.get("title", "CurioNest")))
    kicker = html.escape(config.get("kicker", "HIGH SCHOOL CHEMISTRY"))
    subtitle = html.escape(config.get("subtitle", "Classroom-ready chemistry resources"))
    accent = html.escape(config.get("accent", "#ffb84d"))
    badges = "".join("<span>{}</span>".format(html.escape(str(badge)))
                     for badge in config.get("badges", []))
    figure = asset_uri(config.get("figure"))
    if figure:
        visual = """
        <div class="visual-card">
          <img src="{uri}" alt="Chemistry resource preview">
          <div class="visual-label">CLASSROOM VISUALS INCLUDED</div>
        </div>
        """.format(uri=html.escape(figure, quote=True))
    else:
        visual = """
        <div class="measure-card" aria-label="Measurement illustration">
          <div class="formula">ρ = m ÷ V</div>
          <div class="ruler">0&nbsp;&nbsp;1&nbsp;&nbsp;2&nbsp;&nbsp;3&nbsp;&nbsp;4&nbsp;&nbsp;5&nbsp;&nbsp;6&nbsp;&nbsp;7&nbsp;&nbsp;8&nbsp;&nbsp;9</div>
          <div class="notation">6.022 × 10²³</div>
          <div class="visual-label">WORKED EXAMPLES + PRACTICE</div>
        </div>
        """

    return """<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: 1200px; height: 1200px; overflow: hidden; }}
body {{ font-family: Arial, Helvetica, sans-serif; background: #0f2745; }}
.cover {{
  position: relative; width: 1200px; height: 1200px; overflow: hidden;
  color: #fff; padding: 74px 78px 68px;
  background:
    radial-gradient(circle at 88% 12%, {accent} 0 7px, transparent 8px),
    radial-gradient(circle at 93% 18%, transparent 0 17px, {accent} 18px 21px, transparent 22px),
    linear-gradient(145deg, #0f2745 0%, #174f7d 58%, #0d304f 100%);
}}
.cover::after {{
  content: ""; position: absolute; width: 620px; height: 620px; right: -270px; top: -270px;
  border: 2px solid rgba(255,255,255,.16); border-radius: 50%;
  box-shadow: 0 0 0 55px rgba(255,255,255,.035), 0 0 0 115px rgba(255,255,255,.025);
}}
.brand {{ display: flex; align-items: center; gap: 15px; font: 700 28px Georgia, serif; letter-spacing: 1.5px; }}
.brand-dot {{ width: 19px; height: 19px; border: 4px solid {accent}; border-radius: 50%; }}
.kicker {{ margin-top: 92px; color: {accent}; font-size: 25px; font-weight: 800; letter-spacing: 4px; }}
h1 {{ margin: 20px 0 18px; max-width: 1040px; font: 700 92px/1.02 Georgia, serif; letter-spacing: -2px; }}
.subtitle {{ max-width: 980px; min-height: 84px; color: #dbeafe; font-size: 31px; line-height: 1.35; font-weight: 500; }}
.content {{ display: grid; grid-template-columns: 1fr 430px; gap: 50px; align-items: center; margin-top: 60px; }}
.badges {{ display: flex; flex-direction: column; gap: 17px; }}
.badges span {{
  display: inline-flex; width: max-content; max-width: 100%; padding: 13px 22px;
  border: 1px solid rgba(255,255,255,.32); border-radius: 999px;
  background: rgba(8,30,54,.42); font-size: 24px; font-weight: 700;
}}
.visual-card, .measure-card {{
  position: relative; width: 430px; height: 330px; border-radius: 24px; overflow: hidden;
  background: #fff; color: #0f2745; padding: 24px; transform: rotate(1.5deg);
  box-shadow: 0 24px 54px rgba(0,0,0,.30); border: 6px solid rgba(255,255,255,.55);
}}
.visual-card img {{ width: 100%; height: 240px; object-fit: contain; }}
.visual-label {{ position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 16px; background: {accent}; color: #10233b; text-align: center; font-size: 18px; font-weight: 900; letter-spacing: 1px; }}
.measure-card {{ padding: 30px 28px; background: linear-gradient(160deg,#fff 0%,#eef6ff 100%); }}
.formula {{ font: 700 58px Georgia,serif; color: #174f7d; }}
.ruler {{ margin-top: 34px; padding: 18px 10px 10px; border-bottom: 8px solid {accent}; color: #263b54; font: 700 16px monospace; letter-spacing: 1px; }}
.notation {{ margin-top: 35px; font: 700 38px Georgia,serif; color: #263b54; }}
.footer {{ position: absolute; left: 78px; right: 78px; bottom: 54px; display: flex; justify-content: space-between; align-items: center; color: #dbeafe; font-size: 21px; }}
.footer strong {{ color: #fff; }}
.accent-line {{ position: absolute; left: 0; right: 0; bottom: 0; height: 16px; background: {accent}; }}
</style></head><body>
<main class="cover">
  <div class="brand"><i class="brand-dot"></i> CURIONEST</div>
  <div class="kicker">{kicker}</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
  <section class="content"><div class="badges">{badges}</div>{visual}</section>
  <footer class="footer"><strong>High School Chemistry</strong><span>Teacher-ready · Print + Edit</span></footer>
  <div class="accent-line"></div>
</main></body></html>""".format(
        accent=accent, kicker=kicker, title=title, subtitle=subtitle,
        badges=badges, visual=visual)


def render(product, browser):
    package_dir = ROOT / product["package_dir"]
    package_dir.mkdir(parents=True, exist_ok=True)
    output = package_dir / "cover.png"
    with tempfile.TemporaryDirectory(prefix="curionest-cover-") as temp_name:
        temp = Path(temp_name)
        source = temp / "cover.html"
        profile = temp / "browser-profile"
        rendered = temp / "cover.png"
        source.write_text(cover_html(product), encoding="utf-8")
        command = [
            str(browser), "--headless=new", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            "--window-size=1200,1200", "--user-data-dir={}".format(profile),
            "--screenshot={}".format(rendered), source.as_uri(),
        ]
        completed = subprocess.run(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, timeout=45)
        deadline = time.time() + 8
        while not rendered.exists() and time.time() < deadline:
            time.sleep(0.2)
        if completed.returncode != 0 or not rendered.is_file():
            error = completed.stderr.decode("utf-8", errors="replace")[-1000:]
            raise RuntimeError("cover render failed for {}: {}".format(product["id"], error))
        rendered.replace(output)
    print("cover saved: {}".format(output))


def main():
    parser = argparse.ArgumentParser(description="Build CurioNest cover PNGs")
    parser.add_argument("product", help="Product ID from catalog.json or 'all'")
    args = parser.parse_args()
    catalog = load_catalog()
    products = catalog.get("active_products", [])
    if args.product != "all":
        products = [product for product in products if product.get("id") == args.product]
        if not products:
            parser.error("ไม่พบ Product ID {} ใน catalog.json".format(args.product))
    browser = browser_path()
    for product in products:
        render(product, browser)


if __name__ == "__main__":
    main()
