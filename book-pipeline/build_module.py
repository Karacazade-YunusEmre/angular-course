# -*- coding: utf-8 -*-
"""Tek bir modülün PDF'ini üretir.

Kullanım:
    python build_module.py 09

Ne yapar:
  1. content_m09.py dosyasını içe aktarır ve render() ile HTML üretir.
  2. İçindeki __SHOT_*__ yer tutucularını ../mockups/ klasöründeki PNG'lerle
     (base64 data-uri) değiştirir.
  3. Playwright ile A4 PDF basar (altbilgi: "Modül 9").
  4. Named destination'lardan modülün yerel yer imlerini kurar.
  5. ../modules/Modul-09-<Slug>.pdf olarak kaydeder.

ÖNEMLİ: Geçmiş modüllerin PDF'lerine DOKUNMAZ. Sadece verilen modülü üretir.
Bittikten sonra içindekiler için ayrıca `python build_toc.py` çalıştır.
"""
import argparse
import base64
import importlib
import re
import sys
from pathlib import Path

import pypdf
from playwright.sync_api import sync_playwright

from browser import launch_chromium

from assets import CSS
from curriculum import MODULE_SLUGS

ROOT = Path(__file__).parent
# Çıktı klasörleri depo kökünde durur; pipeline yalnızca üretir.
REPO = ROOT.parent
OUT_DIR = REPO / "modules"
MOCKUP_DIR = REPO / "mockups"
TMP_DIR = ROOT / ".tmp"


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def inject_screenshots(html: str, module_no: int) -> str:
    """__SHOT_XXX__ yer tutucularını ../mockups/mNN_xxx.png ile değiştirir."""
    placeholders = set(re.findall(r"__SHOT_[A-Z0-9_]+__", html))
    for ph in placeholders:
        key = ph.strip("_").replace("SHOT_", "", 1).lower()
        candidate = MOCKUP_DIR / f"m{module_no:02d}_{key}.png"
        if not candidate.exists():
            raise FileNotFoundError(
                f"{ph} için görsel bulunamadı: {candidate}\n"
                f"Önce `python build_mockup.py` ile ekran görüntüsünü üret."
            )
        html = html.replace(ph, data_uri(candidate))
    return html


def render_pdf(body_html: str, module_no: int, out_path: Path) -> None:
    page_html = (
        '<!doctype html><html lang="tr"><head><meta charset="utf-8">'
        f"<style>{CSS}</style></head><body>{body_html}</body></html>"
    )
    footer = (
        '<div style="width:100%;font-size:8px;color:#9aa0ab;text-align:center;'
        'font-family:sans-serif;padding:0 14mm;">'
        f"Angular v22 Eğitim Programı · Modül {module_no} · Hazırlayan: Claude</div>"
    )
    with sync_playwright() as pw:
        browser = launch_chromium(pw)
        page = browser.new_page()
        page.set_content(page_html, wait_until="load")
        page.pdf(
            path=str(out_path),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=footer,
            margin={"top": "12mm", "bottom": "16mm", "left": "14mm", "right": "14mm"},
        )
        browser.close()


def add_bookmarks(src: Path, dest: Path, module_no: int,
                  module_title: str, lessons: list[tuple[str, str]]) -> None:
    """lessons: [('m9l1', 'Ders 9.1 — Temel Routing'), ...] (anchor, başlık)"""
    reader = pypdf.PdfReader(str(src))
    names = reader.named_destinations

    def local_page(anchor: str):
        dest_obj = names.get("/" + anchor) or names.get(anchor)
        return reader.get_destination_page_number(dest_obj) if dest_obj is not None else None

    writer = pypdf.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    root_page = local_page(f"m{module_no}") or 0
    parent = writer.add_outline_item(
        f"Modül {module_no:02d} — {module_title}", root_page)

    missing = []
    for anchor, title in lessons:
        page_no = local_page(anchor)
        if page_no is None:
            missing.append(anchor)
            continue
        writer.add_outline_item(title, page_no, parent=parent)

    with open(dest, "wb") as fh:
        writer.write(fh)

    if missing:
        print(f"  UYARI: şu anchor'lar bulunamadı: {', '.join(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Modül PDF'i üretir.")
    parser.add_argument("module", help="Modül numarası, ör. 09")
    args = parser.parse_args()

    module_no = int(args.module)
    module_name = f"content_m{module_no:02d}"

    try:
        content = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"HATA: {module_name}.py bulunamadı.")
        print("Önce content_template.py dosyasını kopyalayıp içeriği yaz.")
        return 1

    for attr in ("render", "MODULE_TITLE", "LESSONS"):
        if not hasattr(content, attr):
            print(f"HATA: {module_name}.py içinde '{attr}' tanımlı değil.")
            return 1

    OUT_DIR.mkdir(exist_ok=True)
    TMP_DIR.mkdir(exist_ok=True)

    print(f"[1/4] {module_name}.render() çalıştırılıyor...")
    body = content.render()

    print("[2/4] Ekran görüntüleri gömülüyor...")
    body = inject_screenshots(body, module_no)

    print("[3/4] PDF basılıyor...")
    raw_pdf = TMP_DIR / f"m{module_no:02d}_raw.pdf"
    render_pdf(body, module_no, raw_pdf)

    slug = MODULE_SLUGS.get(module_no, "Modul")
    final_pdf = OUT_DIR / f"Modul-{module_no:02d}-{slug}.pdf"

    print("[4/4] Yer imleri ekleniyor...")
    add_bookmarks(raw_pdf, final_pdf, module_no, content.MODULE_TITLE, content.LESSONS)

    pages = len(pypdf.PdfReader(str(final_pdf)).pages)
    print(f"\nTAMAM: {final_pdf}  ({pages} sayfa)")
    print("Şimdi içindekiler tablosunu güncelle:  python build_toc.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
