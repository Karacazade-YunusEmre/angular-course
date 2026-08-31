# -*- coding: utf-8 -*-
"""İçerik yazarken kullanılan HTML yardımcıları.

Bu dosya da modüller arasında DEĞİŞMEZ. Modül içeriği yazarken
yalnızca bu fonksiyonları çağırırsın.
"""
import re

from assets import ICONS, lesson_icon


def esc(s) -> str:
    """Metni HTML'e güvenli hale getirir (başlıklar, düz metin için)."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def C(s) -> str:
    """Satır içi kod: C('signal()') -> <code class="inline">signal()</code>"""
    return f'<code class="inline">{esc(s)}</code>'


def _esc_code(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_HL = re.compile(r'(//[^\n]*|/\*[\s\S]*?\*/)|("[^"\n]*"|\'[^\'\n]*\')')


def highlight(text: str) -> str:
    """Çok basit sözdizimi renklendirme: yorumlar ve metin sabitleri."""
    s = _esc_code(text)

    def repl(m):
        if m.group(1):
            return f'<span class="c">{m.group(1)}</span>'
        return f'<span class="s">{m.group(2)}</span>'

    return _HL.sub(repl, s)


def code(text: str, lang: str = "") -> str:
    """Kod bloğu. lang: 'typescript' | 'html' | 'scss' | 'bash' ..."""
    return (
        '<div class="code"><div class="code-head">'
        '<span class="dots">&#9679; &#9679; &#9679;</span>'
        f'<span class="lang">{esc(lang.upper())}</span></div>'
        f'<pre><code>{highlight(text)}</code></pre></div>'
    )


def tree(text: str) -> str:
    """Klasör ağacı gibi sabit genişlikli blok."""
    return f'<pre class="tree">{_esc_code(text)}</pre>'


def callout(kind: str, title: str, body_html: str) -> str:
    """kind: 'info' | 'tip' | 'warn' | 'note'.

    DİKKAT: title HTML kabul eder (C() ile satır içi kod koyabilirsin),
    bu yüzden title'a kullanıcıdan gelen ham metin verme.
    """
    icon = {"info": "info", "tip": "tip", "warn": "warn", "note": "note"}.get(kind, "info")
    return (
        f'<div class="cal {kind}"><div class="cal-h">{ICONS[icon]} {title}</div>'
        f'<div class="cal-b">{body_html}</div></div>'
    )


def quiz(questions: list[str], answers: list[str]) -> str:
    """Ders sonu mini quiz (soru + cevap çiftleri)."""
    rows = ""
    for q, a in zip(questions, answers):
        rows += f'<li><div class="q">{q}</div><div class="a">&#8627; {a}</div></li>'
    return (f'<div class="box quiz"><div class="box-h">{ICONS["bulb"]} Mini Quiz</div>'
            f'<ol>{rows}</ol></div>')


def anti(items: list[str]) -> str:
    """Sık yapılan hatalar kutusu."""
    lis = "".join(f'<li>{ICONS["x"]}<span>{it}</span></li>' for it in items)
    return (f'<div class="box anti"><div class="box-h">{ICONS["x"]} Sık Yapılan Hatalar</div>'
            f'<ul>{lis}</ul></div>')


def takeaways(items: list[str]) -> str:
    """Ders sonu çıkarımlar kutusu."""
    lis = "".join(f'<li>{ICONS["check"]}<span>{it}</span></li>' for it in items)
    return (f'<div class="box take"><div class="box-h">{ICONS["check"]} '
            f'Bu Dersten Çıkarılacaklar</div><ul>{lis}</ul></div>')


def recall(items: list[str], title: str = "Önceki Modüllerden Hatırla") -> str:
    """KÜMÜLATİF ÖĞRENME kutusu — önceki modüllere geri dönük atıf.

    Modül 8'den itibaren her modülde en az bir kez kullanılmalı.
    """
    lis = "".join(f'<li>{ICONS["swap"]}<span>{it}</span></li>' for it in items)
    return (f'<div class="box recall"><div class="box-h">{ICONS["swap"]} {title}</div>'
            f'<ul>{lis}</ul></div>')


def table(headers: list[str], rows: list[list[str]]) -> str:
    """Tablo. Hücreler HTML kabul eder (C() kullanabilirsin)."""
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def lesson_open(num: str, title: str, anchor: str, order: int | None = None,
                icon: str | None = None) -> str:
    """Ders bölümü açar.

    num    : '9.1' gibi ders numarası; bölüm için '—' kullan
    anchor : PDF yer imi için benzersiz id (ör. 'm9l1')
    order  : ikon seçimi için dersin sırası
    """
    ic = lesson_icon(order=order, name=icon) if (order or icon) else ICONS["book"]
    kick = f"Ders {num}" if num != "\u2014" else "Bölüm"
    return (f'<section class="lesson" id="{anchor}">'
            f'<div class="lesson-head"><div class="kick">{kick}</div>'
            f'<h2>{ic} {esc(title)}</h2></div>')


def lesson_close() -> str:
    return "</section>"


def h3(text: str) -> str:
    return f"<h3>{text}</h3>"


def p(text: str) -> str:
    return f"<p>{text}</p>"


def shot(placeholder: str, caption: str) -> str:
    """Mini proje ekran görüntüsü.

    placeholder: build sırasında base64 ile değiştirilecek anahtar,
                 ör. '__SHOT_MAIN__'
    """
    return (f'<img class="shot" src="{placeholder}" />'
            f'<div class="shot-cap">{esc(caption)}</div>')


def divider(number: int, title: str, level: str, objectives: list[str],
            toc: list[tuple[str, str]]) -> str:
    """Modül kapak sayfası.

    number     : 9
    title      : 'Routing & Navigation'
    level      : 'Gelişim · Junior → Mid-Level'
    objectives : hedef maddeleri (HTML kabul eder)
    toc        : [('#m9l1', '9.1 Temel Routing'), ...]
    """
    lis = "".join(f'<li>{ICONS["check"]}<span>{o}</span></li>' for o in objectives)
    links = "".join(f'<a href="{href}">{esc(label)}</a>' for href, label in toc)
    return (
        f'<div class="mod-divider" id="m{number}">'
        f'<div class="mlabel">MODÜL {number:02d}</div>'
        f'<div class="mbig">{number:02d}</div>'
        f'<h1>{esc(title)}</h1>'
        f'<span class="levelchip">{ICONS["target"]} {esc(level)}</span>'
        '<div class="objbox">'
        f'<div class="h">{ICONS["compass"]} Bu modülde ne öğreneceğiz?</div>'
        f'<ul>{lis}</ul></div>'
        f'<div class="mtoc">{links}</div>'
        '</div>'
    )
