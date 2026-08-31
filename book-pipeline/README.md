# Kitap Pipeline — Angular v22 Türkçe Ders Kitabı

Her modül **ayrı bir PDF**tir. Yeni modül eklerken geçmiş modüller yeniden
üretilmez; yalnızca yeni modülün PDF'i basılır ve içindekiler tablosu güncellenir.

---

## Kurulum (her makinede bir kez)

```bash
pip install -r requirements.txt
playwright install chromium
```

> Windows'ta da aynı komutlar çalışır. `libsass` için ek derleyici gerekmez
> (hazır wheel gelir). Sorun çıkarsa `pip install --upgrade pip` deneyin.

---

## Klasör yapısı

Üretim hattı `book-pipeline/` içinde, **çıktılar depo kökündedir**:

```
angular-course/
├── book-pipeline/
│   ├── assets.py              # ikonlar + PDF CSS'i        (DEĞİŞMEZ)
│   ├── components.py          # içerik yazma yardımcıları  (DEĞİŞMEZ)
│   ├── browser.py             # tarayıcı seçimi            (DEĞİŞMEZ)
│   ├── curriculum.py          # 30 modüllük müfredat       (her modülde güncellenir)
│   ├── build_module.py        # tek modülün PDF'ini üretir
│   ├── build_toc.py           # içindekiler tablosunu üretir
│   ├── build_mockup.py        # mini proje ekran görüntüsünü üretir
│   ├── content_template.py    # yeni modül şablonu (örnek ders dahil)
│   └── content_mNN.py         # her modülün içeriği (sen yazarsın)
├── mockups/                   # mini proje materyalleri
│   ├── mNN/                   # kaynak: index.html + styles.scss + styles.css
│   └── mNN_main.png           # üretilen ekran görüntüleri
└── modules/                   # ÇIKTI: modül PDF'leri + içindekiler
```

Script'ler her zaman `book-pipeline/` içinden çalıştırılır; yolları kendileri
bir üst klasöre çözer.

---

## Yeni modül eklemek (adım adım)

### 1. İçerik dosyasını oluştur

```bash
cp content_template.py content_m09.py
```

Şablonun başındaki `MODULE_NO`, `MODULE_TITLE`, `LESSONS` değerlerini güncelle.
`LESSONS` içindeki anchor'lar (`m9l1` gibi) `lesson_open(...)` çağrılarındaki
anchor'larla **birebir aynı** olmalı; yoksa yer imi oluşmaz (build uyarı verir).

### 2. Mini proje referansını hazırla

`../mockups/m09/index.html` ve `../mockups/m09/styles.scss` yaz
(**JS YOK** — sadece statik HTML + SCSS; ayrıntı için aşağıdaki kurallara bak),
sonra:

```bash
python build_mockup.py 09 main
# birden çok ekran için:
python build_mockup.py 09 error --html error.html
```

Bu, `../mockups/m09_main.png` üretir. İçerikte `shot("__SHOT_MAIN__", "açıklama")`
yazdığında build bunu otomatik bulur (`__SHOT_MAIN__` → `m09_main.png`).

### 3. PDF'i bas

```bash
python build_module.py 09
```

Çıktı: `../modules/Modul-09-Routing.pdf` (dosya adı `curriculum.MODULE_SLUGS`'tan gelir).

### 4. Müfredatı güncelle ve içindekileri yenile

`curriculum.py` içinde modülü `FUTURE`'dan çıkar, `DONE_FILES`'a ekle:

```python
DONE_FILES = {
    ...,
    9: "Modul-09-Routing.pdf",
}
```

```bash
python build_toc.py
```

İçindekiler tablosu artık o modülü "Tamamlandı" (yeşil) olarak gösterir;
ders başlıklarını PDF'in kendi yer imlerinden okur.

---

## İçerik yazarken kurallar

Bunlar kitabın pedagojisidir; `content_template.py` başında da özetlenmiştir.

- Her konu **"Nedir? → Neden? → Nasıl?"** akışında.
- **Ders derinliği öneme göre değişir.** Her ders aynı uzunlukta olmaz:
  teorik/ikincil konular kısa, çekirdek konular derin ve bol örnekli.
- **Eski sürümlere atıf yok.** `@Input`/`@Output`, `EventEmitter`, `NgModule`,
  `*ngIf`, "eskiden şöyleydi" gibi ifadeler geçmez. Güncel yol tek doğru yoldur.
  (Tek istisna: konunun kendisi tarihçe ise.)
- **Tüm kod tanımlayıcıları İngilizce**; yalnızca kullanıcıya görünen UI metinleri Türkçe.
- **Kümülatif öğrenme (Modül 8'den itibaren):** her modülde en az bir
  `recall([...])` kutusu; mini projede önceki modüllerin araçlarını da kullandır
  (pipe, directive, servis...).
- **"Mutfak detayları"nı atlama:** doğru kullanımın yanında sık yapılan yanlış
  denemeyi ve **neden çalışmadığını** da göster.
- Her dersin sonunda `quiz(...)`, gerekiyorsa `anti([...])`, ve `takeaways([...])`.

### Mini proje formatı

- Verilen materyal: **ekran görüntüleri + statik `index.html` + `styles.scss` +
  derlenmiş `styles.css`**. Başka bir şey verilmez.
- **HTML'de JavaScript OLMAZ.** Liste içerikleri düzeni göstermek için elle yazılır.
- **Angular (.ts) kodu verilmez** — öğrenci kendi yazar, sonra incelenir.
- SCSS'te her blok hangi HTML etiketine/sınıfına ait olduğunu belirten yorum taşır.
- Yükleniyor/hata/boş durumlar HTML'de **yorum bloğu** olarak bulunur.

---

## Yardımcı fonksiyonlar (components.py)

| Fonksiyon | Ne için |
|---|---|
| `divider(...)` | Modül kapak sayfası |
| `lesson_open(num, title, anchor, order=)` / `lesson_close()` | Ders bölümü |
| `h3(...)`, `p(...)` | Başlık ve paragraf |
| `C("signal()")` | Satır içi kod |
| `code(text, "typescript")` | Kod bloğu |
| `table(headers, rows)` | Tablo (hücreler HTML kabul eder) |
| `callout("warn", başlık, gövde)` | info / tip / warn / note kutusu |
| `quiz(sorular, cevaplar)` | Ders sonu mini quiz |
| `anti([...])` | Sık yapılan hatalar |
| `takeaways([...])` | Bu dersten çıkarılacaklar |
| `recall([...])` | Önceki modüllere atıf (kümülatif) |
| `shot("__SHOT_X__", "açıklama")` | Mini proje ekran görüntüsü |
| `tree("...")` | Klasör ağacı |

`callout` ve `table` başlık/hücrelerinde HTML kabul edilir (`C()` kullanabilirsin);
`lesson_open` başlığı ise otomatik kaçışlanır (düz metin ver).

---

## Sorun giderme

**"UYARI: şu anchor'lar bulunamadı"** → `LESSONS` içindeki anchor ile
`lesson_open(..., anchor)` uyuşmuyor. İkisini eşitle.

**"__SHOT_X__ için görsel bulunamadı"** → önce `build_mockup.py` çalıştır;
dosya adı `../mockups/mNN_x.png` olmalı (küçük harf).

**Playwright hatası** → `playwright install chromium` çalıştırıldı mı?
Kurumsal ağ (TLS proxy'si) arkasında bu indirme başarısız olabilir; o durumda
`browser.py` sistemde kurulu Edge/Chrome'a düşer, ek bir şey yapman gerekmez.
Üçü de Chromium motoru olduğu için çıktı aynıdır.

**Türkçe karakterler bozuk** → dosyaları UTF-8 kaydet; Windows'ta
`PYTHONUTF8=1` ortam değişkeni yardımcı olur.
