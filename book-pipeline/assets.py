# -*- coding: utf-8 -*-
"""Kitap render altyapısı — ikonlar + PDF CSS'i.

Bu dosya modüller arasında DEĞİŞMEZ. Yeni modül eklerken dokunma
(yeni bir ikon eklemek istersen ICONS sözlüğüne ekleyebilirsin).
"""


def _svg(inner: str) -> str:
    return ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
            + inner + '</svg>')


ICONS = {
    "book":    _svg('<path d="M4 5a2 2 0 0 1 2-2h12v18H6a2 2 0 0 1-2-2z"/><path d="M18 3v18"/>'),
    "compass": _svg('<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>'),
    "target":  _svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>'),
    "check":   _svg('<path d="M20 6L9 17l-5-5"/>'),
    "x":       _svg('<path d="M18 6L6 18M6 6l12 12"/>'),
    "info":    _svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>'),
    "warn":    _svg('<path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17h.01"/>'),
    "tip":     _svg('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 0 0-4-10z"/>'),
    "note":    _svg('<path d="M4 4h16v12H8l-4 4z"/>'),
    "bulb":    _svg('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 0 0-4-10z"/>'),
    "code":    _svg('<path d="M8 9l-3 3 3 3M16 9l3 3-3 3"/>'),
    "rocket":  _svg('<path d="M5 15c-1 2-1 4-1 4s2 0 4-1m1-3a8 8 0 0 1 9-9 8 8 0 0 1-9 9zm0 0l-2-2"/><circle cx="14.5" cy="9.5" r="1.5"/>'),
    "layers":  _svg('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>'),
    "list":    _svg('<path d="M8 6h12M8 12h12M8 18h12M3 6h.01M3 12h.01M3 18h.01"/>'),
    "flag":    _svg('<path d="M5 21V4h13l-2 4 2 4H5"/>'),
    "spark":   _svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18"/>'),
    "wand":    _svg('<path d="M15 4V2M15 10V8M11 6H9M21 6h-2M18 3l-1.5 1.5M18 9l-1.5-1.5M4 20l10-10"/>'),
    "cloud":   _svg('<path d="M17.5 19a4.5 4.5 0 0 0 .5-8.97A6 6 0 0 0 6.2 9.6 4 4 0 0 0 7 19z"/>'),
    "shield":  _svg('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'),
    "swap":    _svg('<path d="M4 8h13l-3-3M20 16H7l3 3"/>'),
    "route":   _svg('<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H14a4 4 0 0 1 0 8H9a4 4 0 0 0 0 8h6.5"/>'),
}

# Ders ikonları sırayla bu listeden atanır (modül numarasından bağımsız).
_LESSON_ICON_CYCLE = ["layers", "code", "spark", "rocket", "target", "wand", "cloud", "shield"]


def lesson_icon(order: int | None = None, name: str | None = None) -> str:
    """Ders ikonu döndürür.

    order : dersin modül içindeki sırası (1'den başlar) — döngüsel seçim
    name  : belirli bir ikon istiyorsan ICONS anahtarı
    """
    if name and name in ICONS:
        return ICONS[name]
    if order is None:
        return ICONS["book"]
    return ICONS[_LESSON_ICON_CYCLE[(order - 1) % len(_LESSON_ICON_CYCLE)]]


CSS = r"""
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Bitstream Charter", "Liberation Serif", Georgia, serif;
  color: #1f2430;
  font-size: 11.4pt;
  line-height: 1.55;
}
h1, h2, h3, .mlabel, .levelchip, .code-head, th, .cal-h, .box-h {
  font-family: "Liberation Sans", "DejaVu Sans", system-ui, sans-serif;
}
.ic { width: 1em; height: 1em; vertical-align: -0.13em; }
p { margin: 0 0 .42cm; }
strong { color: #11151c; }
code.inline {
  font-family: "DejaVu Sans Mono", monospace;
  font-size: 9.5pt;
  background: #f4f2f7;
  color: #7A1FA2;
  padding: 1px 5px;
  border-radius: 5px;
  border: 1px solid #ece8f2;
}

/* ===== Modül ayraç (kapak) ===== */
.mod-divider {
  background: linear-gradient(135deg, #DD0031, #7A1FA2);
  color: #fff; border-radius: 16px; padding: 1.0cm 1.1cm 1.1cm;
  margin: 0 0 .9cm; page-break-after: always;
}
.mod-divider .mlabel { letter-spacing: 3px; font-size: 10pt; opacity: .85; font-weight: 700; }
.mod-divider .mbig { font-size: 58pt; font-weight: 800; line-height: 1; margin: .1cm 0; }
.mod-divider h1 { font-size: 23pt; margin: .1cm 0 .3cm; font-weight: 800; }
.levelchip {
  display: inline-block; background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.35); border-radius: 999px;
  padding: 4px 12px; font-size: 9.5pt; font-weight: 600;
}
.objbox {
  margin-top: .7cm; background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.28); border-radius: 12px; padding: .55cm .6cm;
}
.objbox .h { font-weight: 700; font-size: 11pt; margin-bottom: .3cm; }
.objbox ul { list-style: none; margin: 0; padding: 0; }
.objbox li { display: flex; gap: 9px; align-items: flex-start; margin: .16cm 0; font-size: 10.4pt; }
.mtoc { margin-top: .6cm; font-size: 10pt; }
.mtoc a { color: #fff; text-decoration: none; opacity: .9; margin-right: .5cm;
          border-bottom: 1px dotted rgba(255,255,255,.5); }

/* ===== Ders başlığı ===== */
.lesson { page-break-inside: auto; margin: 0 0 .5cm; }
.lesson-head { border-bottom: 2px solid #efe9f3; padding-bottom: .2cm; margin-bottom: .4cm; }
.lesson-head .kick { color: #DD0031; font-weight: 700; font-size: 10pt;
                     font-family: "Liberation Sans", sans-serif; letter-spacing: .5px; }
.lesson-head h2 { margin: .05cm 0 0; font-size: 18pt; font-weight: 800;
                  display: flex; align-items: center; gap: 9px; }
.lesson-head h2 .ic { color: #DD0031; }
h3 { font-size: 12.5pt; margin: .5cm 0 .2cm; color: #11151c; }

/* ===== Kod bloğu ===== */
.code { margin: .25cm 0 .45cm; border-radius: 10px; overflow: hidden; border: 1px solid #e7e3ee; }
.code-head { background: #f1eef6; padding: 5px 12px; display: flex;
             justify-content: space-between; align-items: center; }
.code-head .dots { color: #c9c2d6; letter-spacing: 2px; font-size: 10pt; }
.code-head .lang { color: #8a7da0; font-size: 8pt; font-weight: 700; letter-spacing: 1px; }
.code pre { margin: 0; padding: .35cm .45cm; background: #faf9fc; overflow-x: auto; }
.code code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt;
             line-height: 1.5; color: #2b2540; white-space: pre; }
.code .c { color: #9aa0ab; font-style: italic; }
.code .s { color: #b8740a; }

.tree { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; background: #faf9fc;
        border: 1px solid #e7e3ee; border-radius: 10px; padding: .35cm .45cm; line-height: 1.5; }

/* ===== Callout kutuları ===== */
.cal { border-radius: 10px; padding: .4cm .5cm; margin: .35cm 0 .45cm; border: 1px solid; }
.cal-h { font-weight: 700; font-size: 10.5pt; margin-bottom: .15cm;
         display: flex; align-items: center; gap: 8px; }
.cal-b { font-size: 10.4pt; }
.cal-b p { margin: 0; }
.cal.info { background: #eef5ff; border-color: #cfe1fb; } .cal.info .cal-h { color: #1d4ed8; }
.cal.tip  { background: #eefaf1; border-color: #c9ecd5; } .cal.tip .cal-h  { color: #1f8a4c; }
.cal.warn { background: #fff6ec; border-color: #f6dcb8; } .cal.warn .cal-h { color: #b8740a; }
.cal.note { background: #f6f3fb; border-color: #e4d9f3; } .cal.note .cal-h { color: #7A1FA2; }

/* ===== Liste kutuları ===== */
.box { border-radius: 10px; padding: .4cm .55cm; margin: .4cm 0 .45cm; border: 1px solid #e7e3ee; }
.box-h { font-weight: 700; font-size: 11pt; margin-bottom: .25cm;
         display: flex; align-items: center; gap: 8px; }
.box ol, .box ul { margin: 0; padding-left: .6cm; }
.box li { margin: .14cm 0; font-size: 10.3pt; }
.quiz { background: #f3f7ff; border-color: #d6e4fb; } .quiz .box-h { color: #1d4ed8; }
.quiz .q { font-weight: 600; }
.quiz .a { color: #1f8a4c; }
.anti { background: #fff5f5; border-color: #f7d6d6; } .anti .box-h { color: #c0314b; }
.anti li { list-style: none; display: flex; gap: 8px; }
.anti li .ic { color: #c0314b; flex: none; margin-top: 2px; }
.take { background: #eefaf1; border-color: #c9ecd5; } .take .box-h { color: #1f8a4c; }
.take li { list-style: none; display: flex; gap: 8px; }
.take li .ic { color: #1f8a4c; flex: none; margin-top: 2px; }
.recall { background: #fbf7ee; border-color: #ecdfc4; } .recall .box-h { color: #8a6d1f; }
.recall li { list-style: none; display: flex; gap: 8px; }
.recall li .ic { color: #8a6d1f; flex: none; margin-top: 2px; }

/* ===== Tablo ===== */
table { width: 100%; border-collapse: collapse; margin: .3cm 0 .45cm; font-size: 10pt; }
th, td { border: 1px solid #e7e3ee; padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #f4f2f7; font-weight: 700; }

/* ===== Mini proje ekran görüntüsü ===== */
.shot { display: block; width: 100%; max-width: 11cm; margin: .3cm auto .45cm;
        border: 1px solid #e7e3ee; border-radius: 10px; }
.shot-cap { text-align: center; font-size: 9pt; color: #8a7da0; margin: -.25cm 0 .5cm; }
"""
