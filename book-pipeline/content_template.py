# -*- coding: utf-8 -*-
"""ŞABLON — yeni modül içeriği böyle yazılır.

Kullanım:
  1. Bu dosyayı kopyala:  content_template.py -> content_m09.py
  2. MODULE_NO / MODULE_TITLE / LESSONS değerlerini güncelle.
  3. Dersleri yaz (aşağıdaki örnek ders yapısını izle).
  4. python build_module.py 09
  5. python build_toc.py

KURALLAR (kitabın pedagojisi — CLAUDE.md ile aynı):
  • Her konu "Nedir? → Neden? → Nasıl?" akışında.
  • Ders derinliği öneme göre değişir; her ders aynı uzunlukta OLMAZ.
    Teorik/ikincil konular kısa, çekirdek konular derin ve bol örnekli.
  • Eski Angular sürümlerine, kaldırılmış API'lere ATIF YAPMA
    (@Input/@Output, EventEmitter, NgModule, *ngIf, "eskiden şöyleydi").
    Güncel yolu tek doğru yol olarak öğret. (İstisna: konu tarihçe ise.)
  • Tüm kod tanımlayıcıları İNGİLİZCE; yalnızca UI metinleri Türkçe.
  • Modül 8'den itibaren KÜMÜLATİF: recall() kutusuyla önceki modüllere
    atıf yap, mini projede önceki modüllerin araçlarını da kullandır.
  • "Mutfak detayları"nı atlama: doğru kullanımın yanında sık yapılan
    YANLIŞ denemeyi ve neden çalışmadığını da göster.
"""
from components import (C, anti, callout, code, divider, h3, lesson_close,
                        lesson_open, p, quiz, recall, shot, table, takeaways,
                        tree)

# ---------------------------------------------------------------------------
# build_module.py bu üç değeri okur
# ---------------------------------------------------------------------------
MODULE_NO = 9
MODULE_TITLE = "Routing & Navigation"

# (anchor, yer imi başlığı) — anchor'lar aşağıdaki lesson_open ile aynı olmalı
LESSONS = [
    ("m9l1", "Ders 9.1 — Temel Routing"),
    ("m9l2", "Ders 9.2 — Route Parametreleri"),
    ("m9proje", "Mini Proje: ..."),
    ("m9ozet", "Modül 9 Özeti"),
]


def _divider() -> str:
    return divider(
        number=MODULE_NO,
        title=MODULE_TITLE,
        level="Gelişim · Junior → Mid-Level",
        objectives=[
            "Rotaların nasıl tanımlandığını ve eşleştiğini",
            C("routerLink") + " ve koddan gezinmeyi",
            "Guard ve resolver'larla rotaları korumayı",
        ],
        toc=[
            ("#m9l1", "9.1 Temel Routing"),
            ("#m9l2", "9.2 Route Parametreleri"),
            ("#m9proje", "Mini Proje"),
            ("#m9ozet", "Özet"),
        ],
    )


def _lesson_1() -> str:
    """ÖRNEK DERS — tüm yardımcıların kullanımını gösterir."""
    h = [lesson_open("9.1", "Temel Routing", "m9l1", order=1)]

    # Giriş paragrafı: konuyu bağla
    h.append(p("Modül 5'te routing'i \u201cminimal\u201d kullanmıştık; şimdi tam hâlini "
               "öğreniyoruz."))

    # KÜMÜLATİF: önceki modüllere atıf (Modül 8'den itibaren zorunlu)
    h.append(recall([
        "Modül 5: " + C("httpResource") + " ile id'ye göre veri çekmek.",
        "Modül 7: Veriyi servis katmanında tutmak.",
    ]))

    # Nedir?
    h.append(h3("Nedir?"))
    h.append(p("<strong>Router, URL'e bakıp hangi component'i göstereceğine karar "
               "eden yapıdır.</strong>"))

    # Neden?
    h.append(h3("Neden var?"))
    h.append(p("Tek sayfa uygulamasında sayfa hissini, geri tuşunu ve "
               "paylaşılabilir adresleri sağlar."))

    # Nasıl?
    h.append(h3("Nasıl?"))
    h.append(code('''export const routes: Routes = [
  { path: '', component: ProductList, pathMatch: 'full' },
  { path: 'product/:id', component: ProductDetail },
];''', "typescript"))

    # Tablo
    h.append(table(["Yazım", "Anlamı"], [
        [C("path: ''"), "Kök adres"],
        [C("path: 'product/:id'"), "Parametreli rota"],
    ]))

    # Callout: info | tip | warn | note
    h.append(callout("warn", C("pathMatch: 'full'") + " neden gerekli?",
                     "<p>Boş yol " + C("'prefix'") + " modunda her URL ile eşleşir.</p>"))

    # Klasör ağacı (gerekirse)
    h.append(tree("""src/app/
├── app.routes.ts
└── pages/"""))

    # Ders sonu üçlüsü
    h.append(quiz(
        ["Router ne yapar?", C("pathMatch: 'full'") + " ne zaman gerekir?"],
        ["URL'e göre component seçer.", "Boş yol (" + C("path: ''") + ") tanımlarken."],
    ))
    h.append(anti([
        "<strong>" + C("href") + " kullanmak.</strong> Tam sayfa yeniler; " + C("routerLink") + " kullan.",
    ]))
    h.append(takeaways([
        "Rotalar " + C("app.routes.ts") + " içinde tanımlanır.",
        "Boş yolda " + C("pathMatch: 'full'") + " şart.",
    ]))

    h.append(lesson_close())
    return "".join(h)


def _lesson_2() -> str:
    h = [lesson_open("9.2", "Route Parametreleri", "m9l2", order=2)]
    h.append(p("..."))
    h.append(lesson_close())
    return "".join(h)


def _mini_proje() -> str:
    """Mini proje: ekran görüntüsü + gereksinimler + ipuçları.

    Ekran görüntüsünü önce üret:
        python build_mockup.py 09 main
    """
    h = [lesson_open("\u2014", "Mini Proje: ...", "m9proje", icon="rocket")]
    h.append(p("Bu modülün kavramlarını birleştiren uygulama."))

    # __SHOT_MAIN__ -> ../mockups/m09_main.png
    h.append(shot("__SHOT_MAIN__", "Ana ekran"))

    h.append(h3("Özellikler / Gereksinimler"))
    h.append("<ul><li>...</li></ul>")

    h.append(h3("Angular tarafı (sende) — ipuçları"))
    h.append("<ul><li>...</li></ul>")

    # KÜMÜLATİF: projede hangi modüller birleşiyor
    h.append(recall([
        "Modül 6: " + C("currency") + " pipe ve custom directive.",
        "Modül 7: Servis katmanı.",
    ], title="Bu Projede Birleşen Modüller"))

    h.append(callout("info", "Materyaller",
                     "<p>Statik referans ayrıca verildi (JS yok): index.html + "
                     "styles.scss + styles.css + ekran görüntüleri.</p>"))
    h.append(takeaways(["..."]))
    h.append(lesson_close())
    return "".join(h)


def _summary() -> str:
    h = [lesson_open("\u2014", f"Modül {MODULE_NO} Özeti", "m9ozet", icon="flag")]
    h.append("<ul><li><strong>Konu:</strong> ...</li></ul>")
    h.append(callout("info", "Sırada ne var?",
                     "<p><strong>Modül 10 — ...</strong></p>"))
    h.append(p("<strong>Takıldığın her yeri sor</strong> — mini projeyi yapıp "
               "gösterdiğinde birlikte gözden geçiririz."))
    h.append(lesson_close())
    return "".join(h)


def render() -> str:
    """build_module.py bu fonksiyonu çağırır."""
    return (_divider() + _lesson_1() + _lesson_2() + _mini_proje() + _summary())
