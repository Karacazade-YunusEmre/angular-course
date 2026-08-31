# -*- coding: utf-8 -*-
"""Mini proje referansını derler ve ekran görüntüsünü üretir.

Kullanım:
    python build_mockup.py 09 main
    python build_mockup.py 09 main --selector ".card" --width 800

Ne yapar:
  1. mockups/m09/styles.scss  ->  mockups/m09/styles.css  (derler)
  2. mockups/m09/index.html   ->  mockups/m09_main.png    (ekran görüntüsü)

Üretilen PNG'yi content_m09.py içinde şu şekilde kullanırsın:
    shot("__SHOT_MAIN__", "Ana ekran: liste ve filtreler")
  (build_module.py, __SHOT_MAIN__ -> mockups/m09_main.png eşlemesini yapar.)

Birden fazla ekran için ayrı HTML dosyaları tut:
    python build_mockup.py 09 error --html error.html   ->  m09_error.png
"""
import argparse
import sys
from pathlib import Path

import sass
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
MOCKUP_DIR = ROOT / "mockups"


def main() -> int:
    parser = argparse.ArgumentParser(description="Mini proje ekran görüntüsü üretir.")
    parser.add_argument("module", help="Modül numarası, ör. 09")
    parser.add_argument("name", help="Ekran adı, ör. main / error / empty")
    parser.add_argument("--html", default="index.html", help="Kaynak HTML (varsayılan index.html)")
    parser.add_argument("--selector", default=".card", help="Kırpılacak eleman (varsayılan .card)")
    parser.add_argument("--width", type=int, default=760, help="Görüntü genişliği")
    parser.add_argument("--height", type=int, default=900, help="Görüntü yüksekliği")
    args = parser.parse_args()

    module_no = int(args.module)
    src_dir = MOCKUP_DIR / f"m{module_no:02d}"
    html_path = src_dir / args.html
    scss_path = src_dir / "styles.scss"
    css_path = src_dir / "styles.css"

    if not html_path.exists():
        print(f"HATA: {html_path} yok.")
        return 1

    css = ""
    if scss_path.exists():
        print(f"[1/2] SCSS derleniyor: {scss_path.name}")
        css = sass.compile(filename=str(scss_path), output_style="expanded")
        css_path.write_text(
            "/* styles.css — styles.scss'in derlenmiş hali. */\n\n" + css,
            encoding="utf-8",
        )
    else:
        print("[1/2] styles.scss yok, atlanıyor.")

    print(f"[2/2] Ekran görüntüsü alınıyor: {args.html}")
    html = html_path.read_text(encoding="utf-8")
    if css:
        # Harici stil bağlantısını gömülü stille değiştir (dosya yolu sorunu olmasın)
        html = html.replace('<link rel="stylesheet" href="styles.css" />', f"<style>{css}</style>")
        html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>")

    out_png = MOCKUP_DIR / f"m{module_no:02d}_{args.name}.png"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=2,
        )
        page.set_content(html, wait_until="load")
        target = page.locator(args.selector)
        if target.count() == 0:
            print(f"UYARI: '{args.selector}' bulunamadı, tam sayfa alınıyor.")
            page.screenshot(path=str(out_png), full_page=True)
        else:
            target.first.screenshot(path=str(out_png))
        browser.close()

    print(f"\nTAMAM: {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
