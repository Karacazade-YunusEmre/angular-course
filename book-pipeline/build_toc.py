# -*- coding: utf-8 -*-
"""İçindekiler PDF'ini üretir (tüm müfredat, tamamlananlar vurgulu).

Kullanım:
    python build_toc.py

Tamamlanan modüllerin başlık ve ders listesini kendi PDF'lerinin yer
imlerinden okur; kalanları curriculum.FUTURE'dan alır.
Çıktı: ../modules/00-Icindekiler.pdf
"""
import html as _html
import sys
from pathlib import Path

import pypdf
from playwright.sync_api import sync_playwright

from browser import launch_chromium

from curriculum import DONE_FILES, FUTURE, LEVELS

ROOT = Path(__file__).parent
# Çıktı klasörleri depo kökünde durur; pipeline yalnızca üretir.
REPO = ROOT.parent
OUT_DIR = REPO / "modules"


def esc(s) -> str:
    return _html.escape(str(s))


def read_done() -> dict:
    """Tamamlanan modüllerin başlık + ders listesini PDF yer imlerinden okur."""
    done = {}
    for num, filename in DONE_FILES.items():
        path = OUT_DIR / filename
        if not path.exists():
            print(f"  ATLANDI (dosya yok): {filename}")
            continue

        reader = pypdf.PdfReader(str(path))
        title, lessons = filename, []
        outline = reader.outline
        if outline:
            if not isinstance(outline[0], list):
                title = outline[0].title
            for item in outline:
                if isinstance(item, list):
                    lessons = [c.title for c in item if not isinstance(c, list)]

        if "—" in title:
            title = title.split("—", 1)[1].strip()

        done[num] = {
            "title": title,
            "lessons": lessons,
            "file": filename,
            "pages": len(reader.pages),
        }
        print(f"  M{num:02d}: {title} ({len(lessons)} başlık, {len(reader.pages)} sayfa)")
    return done


CHECK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>')
LOCK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="4" y="10" width="16" height="10" rx="2"/>'
            '<path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>')


def build_html(done: dict) -> str:
    total_done = len(done)
    done_pages = sum(d["pages"] for d in done.values())
    percent = round(100 * total_done / 30)

    body = ""
    for level_name, numbers in LEVELS:
        body += f'<div class="level">{esc(level_name)}</div>'
        for n in numbers:
            if n in done:
                d = done[n]
                items = "".join(f"<li>{esc(x)}</li>" for x in d["lessons"])
                body += (
                    '<div class="mod done">'
                    f'<div class="mhead"><span class="mnum">Modül {n:02d}</span>'
                    f'<span class="mtitle">{esc(d["title"])}</span>'
                    f'<span class="chip ok"><i>{CHECK_SVG}</i>Tamamlandı</span></div>'
                    f'<div class="file">{esc(d["file"])} · {d["pages"]} sayfa</div>'
                    f"<ul>{items}</ul></div>"
                )
            elif n in FUTURE:
                title, lessons = FUTURE[n]
                items = "".join(f"<li>{esc(x)}</li>" for x in lessons)
                body += (
                    '<div class="mod soon">'
                    f'<div class="mhead"><span class="mnum">Modül {n:02d}</span>'
                    f'<span class="mtitle">{esc(title)}</span>'
                    f'<span class="chip wait"><i>{LOCK_SVG}</i>Sırada</span></div>'
                    f"<ul>{items}</ul></div>"
                )

    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:"Liberation Sans","DejaVu Sans",system-ui,sans-serif; color:#1f2430; }}
.cover {{ background:linear-gradient(135deg,#DD0031,#7A1FA2); color:#fff; padding:2.2cm 1.4cm 1.5cm; }}
.cover .kick {{ letter-spacing:3px; font-size:10.5pt; opacity:.85; font-weight:700; }}
.cover h1 {{ font-size:29pt; margin:.2cm 0 .1cm; font-weight:800; line-height:1.05; }}
.cover .sub {{ font-size:11.5pt; opacity:.9; }}
.stats {{ display:flex; gap:.5cm; margin-top:.7cm; }}
.stat {{ background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.3);
         border-radius:12px; padding:.35cm .55cm; }}
.stat .n {{ font-size:19pt; font-weight:800; line-height:1; }}
.stat .l {{ font-size:8.5pt; opacity:.85; margin-top:2px; }}
.bar {{ margin-top:.6cm; height:9px; border-radius:99px; background:rgba(255,255,255,.25); overflow:hidden; }}
.bar span {{ display:block; height:100%; width:{percent}%; background:#fff; border-radius:99px; }}
.barlabel {{ font-size:9pt; opacity:.9; margin-top:5px; }}
.tocword {{ margin-top:.8cm; font-size:15pt; font-weight:800; letter-spacing:1px; }}
.wrap {{ padding:.9cm 1.4cm 1cm; }}
.legend {{ display:flex; gap:.6cm; font-size:9pt; color:#6b7280; margin-bottom:.5cm; }}
.legend i {{ display:inline-block; width:10px; height:10px; border-radius:3px;
             margin-right:5px; vertical-align:-1px; }}
.legend .a i {{ background:#1f8a4c; }}
.legend .b i {{ background:#c9ced9; }}
.level {{ font-size:9.5pt; font-weight:800; letter-spacing:2px; text-transform:uppercase;
          color:#7A1FA2; margin:.55cm 0 .25cm; padding-bottom:3px; border-bottom:2px solid #efe9f3; }}
.mod {{ margin:0 0 .32cm; break-inside:avoid; padding-left:.3cm; border-left:3px solid #e6e8ee; }}
.mhead {{ display:flex; align-items:baseline; gap:8px; }}
.mnum {{ font-family:"DejaVu Sans Mono",monospace; font-size:8.5pt; font-weight:700; color:#8a7da0; }}
.mtitle {{ font-size:12pt; font-weight:800; flex:1; }}
.chip {{ font-size:8pt; font-weight:700; padding:2px 9px; border-radius:99px;
         display:inline-flex; align-items:center; gap:4px; white-space:nowrap; }}
.chip i {{ display:inline-flex; width:10px; height:10px; }}
.chip svg {{ width:10px; height:10px; }}
.chip.ok {{ background:#e7f7ee; color:#1f8a4c; border:1px solid #c9ecd5; }}
.chip.wait {{ background:#f3f4f7; color:#9aa0ab; border:1px solid #e6e8ee; }}
.file {{ font-family:"DejaVu Sans Mono",monospace; font-size:7.8pt; color:#8a7da0; margin:2px 0 0; }}
ul {{ margin:.12cm 0 0; padding-left:.75cm; }}
li {{ font-size:9.8pt; margin:1.5px 0; }}
.mod.done {{ border-left-color:#1f8a4c; }}
.mod.done .mtitle {{ color:#11151c; }}
.mod.done li {{ color:#2b2540; }}
.mod.soon {{ border-left-color:#e6e8ee; }}
.mod.soon .mtitle {{ color:#9aa0ab; font-weight:700; }}
.mod.soon .mnum {{ color:#c1c6d0; }}
.mod.soon li {{ color:#b6bcc6; }}
</style></head><body>
<div class="cover">
  <div class="kick">ANGULAR v22 EĞİTİM PROGRAMI</div>
  <h1>Sıfırdan Expert'e</h1>
  <div class="sub">Modül modül ilerleyen, uygulamalı Angular v22 ders kitabı</div>
  <div class="stats">
    <div class="stat"><div class="n">30</div><div class="l">Toplam modül</div></div>
    <div class="stat"><div class="n">{total_done}</div><div class="l">Tamamlanan</div></div>
    <div class="stat"><div class="n">{done_pages}</div><div class="l">Yazılan sayfa</div></div>
    <div class="stat"><div class="n">v22</div><div class="l">Angular sürümü</div></div>
  </div>
  <div class="bar"><span></span></div>
  <div class="barlabel">İlerleme: {total_done} / 30 modül (%{percent})</div>
  <div class="tocword">İÇİNDEKİLER</div>
</div>
<div class="wrap">
  <div class="legend">
    <span class="a"><i></i>Tamamlandı — ayrı PDF dosyası hazır</span>
    <span class="b"><i></i>Sırada — henüz işlenmedi</span>
  </div>
  {body}
</div>
</body></html>"""


def main() -> int:
    if not OUT_DIR.exists():
        print(f"HATA: {OUT_DIR} yok.")
        return 1

    print("Tamamlanan modüller okunuyor...")
    done = read_done()

    out_path = OUT_DIR / "00-Icindekiler.pdf"
    with sync_playwright() as pw:
        browser = launch_chromium(pw)
        page = browser.new_page()
        page.set_content(build_html(done), wait_until="load")
        page.pdf(path=str(out_path), format="A4", print_background=True,
                 margin={"top": "0", "bottom": "12mm", "left": "0", "right": "0"})
        browser.close()

    pages = len(pypdf.PdfReader(str(out_path)).pages)
    print(f"\nTAMAM: {out_path} ({pages} sayfa) — {len(done)}/30 modül tamamlandı")
    return 0


if __name__ == "__main__":
    sys.exit(main())
