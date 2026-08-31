# -*- coding: utf-8 -*-
"""Playwright tarayıcısını başlatır — makineye göre esnek.

Normalde `playwright install chromium` ile inen paketli tarayıcı kullanılır.
Kurumsal ağ (TLS proxy'si) arkasında bu indirme başarısız olabilir; o durumda
sistemde kurulu Edge ya da Chrome'a düşeriz. Çıktı her iki yolda da aynıdır,
çünkü üçü de Chromium motorudur.
"""
from playwright.sync_api import Browser, Playwright

# Sırayla denenir: paketli chromium -> kurulu Edge -> kurulu Chrome
_CHANNELS: tuple[str | None, ...] = (None, "msedge", "chrome")


def launch_chromium(pw: Playwright) -> Browser:
    """Kullanılabilir ilk Chromium'u başlatır, hiçbiri yoksa açıklayıcı hata verir."""
    failures: list[str] = []
    for channel in _CHANNELS:
        try:
            return pw.chromium.launch(channel=channel) if channel else pw.chromium.launch()
        except Exception as exc:  # noqa: BLE001 - hepsini deneyip sonunda özet veriyoruz
            failures.append(f"  {channel or 'paketli chromium'}: {str(exc).splitlines()[0]}")

    raise RuntimeError(
        "Hiçbir Chromium başlatılamadı.\n"
        + "\n".join(failures)
        + "\n\nÇözüm: `playwright install chromium` çalıştır ya da makineye "
          "Edge/Chrome kur."
    )
