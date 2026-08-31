# Proje Bağlamı — Angular v22 Öğrenme Projesi

Bu dosya, bu repoda çalışan Claude Code oturumları için kalıcı bağlamdır.
Birden çok makinede (Windows + Linux) çalışılıyor; bağlam git üzerinden taşınır.

---

## 1. Bu proje nedir?

Angular v22 öğrenen bir geliştiricinin (Efsane Emre) uygulama projeleri.
Paralel yürüyen bir **Türkçe ders kitabı** var; bu repodaki kod, o kitabın
modül sonu mini projelerini içerir.

Repo içeriği:
- `apps/` — modül sonu mini projeleri, her biri ayrı bir Angular v22 uygulaması
  (`module-01-hello-angular` … `module-08-products-app`)
- `Module08ProductApi/` — .NET 10 minimal API + SQL Server (Modül 8'den itibaren backend)
- `kitap-pipeline/` — ders kitabının PDF üretim hattı (modül PDF'leri burada üretilir)
- `tutorials/` — üretilmiş modül PDF'lerinin okuma kopyası

Bu repo hem **kodu** hem **ders kitabını** barındırır. Kitap modül modül
ilerler: önce modülün PDF'i hazırlanır, sonra ben mini projeyi yazarım,
sen incelersin, ardından bir sonraki modüle geçilir.

---

## 2. En önemli kural: ÖĞRETME MODU

Bu bir üretim projesi değil, bir **öğrenme** projesidir.

- **Kodu benim yerime yazma.** Ben yazarım, sen yol gösterirsin.
- Takıldığımda **tam çözüm değil, ipucu** ver. "Şu satıra bak, şu kavramı düşün."
- Kod incelemesi istediğimde: neyin yanlış olduğunu **ve nedenini** açıkla,
  düzeltilmiş kodu doğrudan uygulamak yerine önce anlat.
- İstisna: açıkça "sen yaz" dersem yazarsın.
- Bir şeyi düzeltirken **niçin** öyle olduğunu da söyle; kural ezberi değil,
  mantık istiyorum.

---

## 3. Dil kuralları

- **Açıklamalar, yorumlar, UI metinleri: Türkçe.**
- **Tüm kod tanımlayıcıları: İngilizce.** (class, interface, değişken, metot,
  signal, input/output adları, CSS sınıfları — hepsi.)
- Örnek: `productList`, `addToCart`, `OrderStatus` ✅ / `urunListesi` ❌
- Kullanıcıya görünen metinler Türkçe: `<button>Sepete Ekle</button>` ✅

---

## 4. Angular v22 konvansiyonları (ZORUNLU)

Bu proje Angular **v22** kullanır. Eski API'lere ait öneri verme.

### Servisler ve DI
- `@Service()` kullan — `@Injectable()` DEĞİL.
  - Sade `@Service()` = kök singleton (varsayılan, çoğu durumda doğru).
  - Component kapsamı gerekiyorsa: `@Service({ autoProvided: false })` +
    component'in `providers` dizisi.
- Bağımlılıklar **`inject()`** ile alınır. **Constructor injection YOK.**

### Signals
- Durum (state) signal'de tutulur: `signal()`, türetilmiş değer `computed()`.
- `effect()` yalnızca yan etki içindir (log, DOM, depolama) — değer üretmek için DEĞİL.
- Yazılabilir türetme gerekiyorsa `linkedSignal()`.
- **Immutability zorunlu:** dizi/nesne güncellemede yeni referans ver
  (`[...list, item]`, `map`, `filter`). `push`/alan mutasyonu signal'i tetiklemez.
- Servislerde desen: `private readonly _x = signal(...)` + dışarı `x = this._x.asReadonly()`
  + değişiklik yalnızca metotlarla.
- Her değişken signal olmak zorunda değil: sabitler, enjekte edilen servisler ve
  metot içi geçici değerler düz kalır.

### Template
- Control flow: `@if` / `@for` / `@switch` / `@let` / `@empty`. `*ngIf`, `*ngFor` YOK.
- `@for` her zaman `track` ile.
- Tek sınıf: `[class.x]="cond"`. Çok sınıf: `[class]="{ a: condA(), b: condB() }"`.
  Stil: `[style.prop]`, birim gerekiyorsa `[style.width.px]`.
- Yerleşik `[class]`/`[style]` tercih edilir; `ngClass`/`ngStyle` istisna.
- `[(ngModel)]` bir signal'e DOĞRUDAN bağlanmaz. Ya `model()` ile two-way,
  ya da `[value]` + `(input)="sig.set(...)"` ayrık yazımı.
- Şablon referansı `#name` aynı şablonda geçerlidir; TS'ten erişim `viewChild('name')`.

### Component API
- `input()` / `output()` / `model()` fonksiyonları. `@Input`/`@Output`/`EventEmitter` YOK.
- Sorgular signal tabanlı: `viewChild()`, `viewChildren()`, `viewChild.required()`.
- `NgModule` yok — her şey standalone.
- OnPush artık **varsayılan** (eski davranış için `ChangeDetectionStrategy.Eager`).

### HTTP
- Kurulum: `provideHttpClient(withInterceptors([...]))` — `app.config.ts`.
- **Okuma** ekrana bağlıysa `httpResource` (signal + `isLoading`/`error`/`hasValue`).
  Nesne formunu tercih et: `httpResource(() => ({ url, params }))`.
- **Yazma** (POST/PUT/DELETE) doğrudan `HttpClient` + `subscribe`; sonra `reload()`.
- `httpResource` hata durumundayken `value()` okumak istisna fırlatır → `hasValue()` ile koru.
- Interceptor'lar **fonksiyonel** yazılır (`HttpInterceptorFn`), `req.clone()` ile değiştirilir.

### Directive & Pipe
- Custom directive: `@Directive({ selector: '[appX]', host: { ... } })`.
  Host'a bağlanmak için **`host` metadata** kullan — `@HostBinding`/`@HostListener` DEĞİL.
- Directive'in tek bir "asıl" değeri varsa input adı selector ile aynı olsun
  (`ngClass`/`routerLink` kalıbı); iç kodda anlamlı ad için
  `input('default', { alias: 'appX' })`. İkincil ayarlar ayrı input'larda.
- Pipe kullanmadan önce component'in `imports`'ına eklenmeli
  (`CurrencyPipe`, `DatePipe`, `DecimalPipe`...). Unutulursa "No pipe found" hatası.

### Routing
- `provideRouter(routes, withComponentInputBinding())`.
- Rota parametresi, aynı adlı `input()` ile component'e otomatik bağlanır
  (`id = input.required<string>()`); `ActivatedRoute` aboneliği gerekmez.
- Boş yol (`path: ''`) için `pathMatch: 'full'` şart; dolu yollarda gereksiz.
- Şablondan gezinme `routerLink`, koddan gezinme `inject(Router).navigate([...])`.
- `loadComponent` yalnızca gerçek lazy loading içindir (dinamik `import()`);
  üstte import edilmiş component için `component:` kullan.

---

## 5. .NET API (`Module08ProductApi/`)

.NET 10 minimal API + **SQL Server** (Docker'da), EF Core üzerinden repository deseni.
238 ürün, 8 kategori (15'i stokta yok). Ayrıntı: `Module08ProductApi/README.md`.

- Çalıştırma: `docker compose up -d` → `cd WebApi && dotnet run`
  (şema ve tohum veri uygulama açılışında `MigrateAsync()` ile otomatik uygulanır;
  tablo doluysa tekrar veri eklemez)
- Adres: `http://localhost:5047` · gezinti arayüzü `/scalar/v1`
- CORS `http://localhost:4200` için açık

**Uçlar** (`/api/products` altında):

| Metot | Adres | Yanıt |
|---|---|---|
| GET | `` (liste) | `200` + `PagedResult<Product>` |
| GET | `/{id}` | `200` · `404` |
| POST | `` | `201` · `400` |
| PUT | `/{id}` | `200` · `400` · `404` |
| DELETE | `/{id}` | `204` · `404` |
| GET | `/error-demo` | `500` (bilerek) |

**Filtreleme ayrı uç değil, liste ucunun query parametreleridir:**
`page` (1), `pageSize` (10, max 200), `sort` (`id`/`name`/`price`/`stock`/`createdAt`,
başına `-` → azalan), `name` (içerir, harf duyarsız), `minPrice`/`maxPrice`,
`minStock`/`maxStock`.

- Cevap sarmalayıcısı: `{ items, page, pageSize, total, totalPages, hasPrevious, hasNext }`
  → **Angular tarafındaki interface bu adlarla birebir aynı olmalı.**
- Hatalar `application/problem+json`: `400` + `ValidationProblemDetails`,
  `404` + `ProblemDetails`.
- Test kolaylıkları (yalnızca `Development`): herhangi bir uca `?delay=1500`
  (yükleniyor ekranı, max 10000 ms), `GET /api/products/error-demo` (hata ekranı).
- Yazma işlemleri veritabanına **kalıcı** yazar. Sıfırlamak için
  `docker compose down -v` → yeniden `dotnet run`.

---

## 6. Kod stili

- Servis adları `Service` son ekiyle: `ProductService`, `CartService` (model adlarıyla
  çakışmasın diye). Tutarlılık şart — hepsi ya son ekli ya değil.
- Olay (output) adları eylem gibi: `taskAdded`, `productSelected` — değer gibi değil.
- Karşılaştırmalarda referans değil **id** kullan (`p.id === id`), çok elemanlıysa `Set`.
- Türetilmiş sayaç/toplam gibi değerler ait oldukları **serviste** `computed` olarak yaşar.
- SCSS: paylaşılan değişkenler ayrı bir partial'da (`_variables.scss`),
  kullanan dosyada en üstte `@use '../variables' as *;`.

---

## 7. Ders kitabı üretimi (`kitap-pipeline/`)

Kitap 30 modüllük bir müfredattır; her modül **ayrı bir PDF**tir.
Ayrıntılı kullanım: `kitap-pipeline/README.md`.

### Yeni modül üretme akışı

```bash
cd kitap-pipeline
cp content_template.py content_m09.py     # içeriği yaz
python build_mockup.py 09 main            # mini proje ekran görüntüsü
python build_module.py 09                 # modül PDF'i
# curriculum.py: modülü FUTURE'dan DONE_FILES'a taşı
python build_toc.py                       # içindekiler tablosu
```

**Geçmiş modüllerin PDF'lerini YENİDEN ÜRETME.** Sadece yeni modül basılır.
`moduller/` klasöründeki mevcut PDF'lere dokunulmaz.

### İçerik yazım kuralları (kitabın pedagojisi)

- Her konu **"Nedir? → Neden? → Nasıl?"** akışında.
- **Ders derinliği öneme göre değişir** — her ders aynı uzunlukta olmaz.
  Teorik/ikincil konular kısa; çekirdek konular derin ve bol örnekli.
- **Eski Angular sürümlerine atıf yok** (`@Input`, `EventEmitter`, `NgModule`,
  `*ngIf`, "eskiden şöyleydi"). Güncel yol tek doğru yol olarak öğretilir.
  Tek istisna: konunun kendisi tarihçe ise.
- **Kümülatif (Modül 8'den itibaren):** her modülde en az bir `recall([...])`
  kutusu ile önceki modüllere atıf; mini projede önceki modüllerin araçları da
  kullandırılır (pipe, directive, servis...).
- **Mutfak detayları atlanmaz:** doğru kullanımın yanında sık yapılan yanlış
  deneme ve **neden çalışmadığı** da gösterilir.
- Her ders sonunda `quiz(...)`, gerekiyorsa `anti([...])`, ve `takeaways([...])`.

### Mini proje formatı (DEĞİŞMEZ)

- Verilen materyal: **ekran görüntüleri + statik `index.html` + `styles.scss` +
  derlenmiş `styles.css`**. Başkası verilmez.
- **HTML'de JavaScript OLMAZ.** Liste içerikleri düzeni göstermek için elle yazılır.
- **Angular (.ts) kodu VERİLMEZ** — ben yazarım, sonra birlikte incelenir.
- SCSS'te her blok, hangi HTML etiketine/sınıfına ait olduğunu belirten yorum taşır.
- Yükleniyor/hata/boş durumlar HTML'de yorum bloğu olarak bulunur.

---

## 8. Çok makineli çalışma

- Windows + Linux karışık. Satır sonları için `.gitattributes` → `* text=auto eol=lf`.
- `node_modules/`, `bin/`, `obj/`, `.angular/` commit edilmez; makine değişince `npm ci`.
- Makineyi bırakmadan önce push, oturmadan önce pull. Yarım iş `wip/...` dalına.
- Yol ayracı varsayımı yapma; script yazarken iki platformda da çalışsın.

---

## 9. Sık düşülen tuzaklar (bu projede yaşandı)

- `{ ...arr, item }` bir NESNE üretir → `@for` patlar. Diziye ekleme `[...arr, item]`.
- `ngOnInit` senkron ve tek seferdir; asenkron veriyi orada yakalayamazsın →
  şablonda `@if (hasValue())` ya da `effect()`.
- API sarmalayıcı döndürüyorsa (`{ items: [...] }`) tipini sarmalayıcıya göre kur;
  doğrudan `Product[]` sanma.
- Alan adı uyuşmazlığı (ör. `hasNext` vs `hasNextPage`) sessizce `undefined` verir →
  buton hep disabled kalır. Network sekmesinden gerçek cevabı doğrula.
- `[src]="expr"` yerine `src="expr"` yazmak: düz metin sanılır, görsel gelmez.
- Custom pipe'ta kısa metne de "..." eklemek: `value.length > limit` kontrolü şart.
