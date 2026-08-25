#!/usr/bin/env python3
"""
Rooted plant wiki page generator.

Reads plant-template.html + plants_data.py, and for each plant writes:
  ../wiki/<slug>.html         (the page, served at growwithrooted.com/wiki/<slug>)
  ../assets/og/<slug>.png     (the Open Graph share image, 1200x630)

Usage:
  python3 make_plant_page.py            # all plants
  python3 make_plant_page.py sunflower  # just one (by slug)

PHASE 1 hero = branded tinted panel (in the template). PHASE 2 swaps that slot
for the user's uploaded photo; the og:image path stays the same variable.
"""

import os
import sys
from plants_data import PLANTS, CATEGORY_META

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)               # rooted-landing repo root
WIKI_DIR = os.path.join(ROOT, "wiki")
OG_DIR = os.path.join(ROOT, "assets", "og")
TEMPLATE = os.path.join(HERE, "plant-template.html")


def paras(items):
    return "".join(f"<p>{p}</p>" for p in items)


def fill_page(plant, tpl):
    meta = CATEGORY_META[plant["category"]]
    repl = {
        "NAME": plant["name"],
        "SCI": plant["sci"],
        "SLUG": plant["slug"],
        "CATEGORY_LABEL": meta["label"],
        "CATEGORY_TINT": meta["tint"],
        "CATEGORY_KICKER": meta["kicker"],
        "TYPE": plant["type"],
        "LEDE": plant["lede"],
        "SUN": plant["sun"],
        "WATER": plant["water"],
        "HARVEST": plant["harvest"],
        "HARDINESS": plant["hardiness"],
        "META_DESC": plant["meta_desc"],
        "ABOUT_HEADING": plant["about_heading"],
        "ABOUT_HTML": paras(plant["about"]),
        "CARE_HTML": paras(plant["care"]),
        "GTK_HEADING": plant["gtk_heading"],
        "GTK_HTML": paras(plant["gtk"]),
        "FAMILY": plant["family"],
        "HEIGHT": plant["height"],
        "BLOOM": plant["bloom"],
        "NATIVE": plant["native"],
        "PROPAGATION": plant["propagation"],
    }
    html = tpl
    for k, v in repl.items():
        html = html.replace("{{" + k + "}}", str(v))
    leftover = [seg.split("}}")[0] for seg in html.split("{{")[1:]]
    assert not leftover, f"{plant['slug']}: unfilled placeholders {leftover}"
    return html


# ---- OG image (1200x630) --------------------------------------------------
def _font(paths, size):
    from PIL import ImageFont
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


SERIF = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"]
SERIF_IT = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Italic.ttf"]
SANS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def make_og(plant):
    from PIL import Image, ImageDraw
    meta = CATEGORY_META[plant["category"]]
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), meta["tint"])
    d = ImageDraw.Draw(img)
    forest, terra, kicker = "#174038", "#C47454", meta["kicker"]

    pad = 90
    # kicker line
    d.text((pad, 92), f"{meta['label'].upper()}  ·  ROOTED FIELD GUIDE",
           font=_font(SANS, 26), fill=kicker)
    # name (wrap if long)
    name_font = _font(SERIF_IT, 118)
    name = plant["name"]
    if d.textlength(name, font=name_font) > W - 2 * pad:
        name_font = _font(SERIF_IT, 86)
    d.text((pad, 150), name, font=name_font, fill=forest)
    # scientific name
    d.text((pad, 302), plant["sci"], font=_font(SERIF_IT, 46), fill="#6f776d")
    # facts line
    facts = f"{plant['sun']}   ·   {plant['water']}   ·   {plant['harvest']}"
    d.text((pad, 470), facts, font=_font(SANS, 30), fill=kicker)
    # terracotta accent bar
    d.rectangle([pad, 430, pad + 62, 434], fill=terra)
    # Rooted chip bottom-right
    chip = 74
    cx, cy = W - pad - chip, H - 78 - chip
    d.rounded_rectangle([cx, cy, cx + chip, cy + chip], radius=18, fill=forest)
    rf = _font(SERIF_IT, 46)
    tw = d.textlength("R", font=rf)
    d.text((cx + (chip - tw) / 2, cy + 8), "R", font=rf, fill="#dfe7d3")

    os.makedirs(OG_DIR, exist_ok=True)
    out = os.path.join(OG_DIR, plant["slug"] + ".png")
    img.save(out, "PNG")
    return out


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with open(TEMPLATE) as f:
        tpl = f.read()
    os.makedirs(WIKI_DIR, exist_ok=True)
    n = 0
    for plant in PLANTS:
        if only and plant["slug"] != only:
            continue
        html = fill_page(plant, tpl)
        with open(os.path.join(WIKI_DIR, plant["slug"] + ".html"), "w") as f:
            f.write(html)
        og = make_og(plant)
        n += 1
        print(f"  ✓ {plant['slug']:<12} → wiki/{plant['slug']}.html  +  {os.path.relpath(og, ROOT)}")
    print(f"\nGenerated {n} plant page(s). Serve at growwithrooted.com/wiki/<slug>.")


if __name__ == "__main__":
    main()
