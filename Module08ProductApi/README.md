# Module08 Product API — .NET 10 Minimal API + SQL Server

Angular eğitim programının **Modül 8 (HTTP & Backend İletişimi)** dersi için yazılmış
küçük bir backend. Veriler **Docker'da çalışan bir SQL Server** örneğinde tutulur,
erişim **EF Core** üzerinden repository deseniyle yapılır.

- **238 hazır ürün**, 8 kategori (15 ürün stokta yok)
- Sayfalama, filtreleme, sıralama
- CORS açık: `http://localhost:4200` doğrudan çağırabilir
- Yükleniyor / hata ekranlarını denemek için yardımcı uçlar

---

## Çalıştırma

### 1. Veritabanını başlat

```bash
cd Module08ProductApi
docker compose up -d
```

İlk çalıştırmada ~1,5 GB imaj indirilir. Hazır olduğunu şöyle doğrularsın:

```bash
docker compose ps        # STATUS sütununda "(healthy)" görünmeli
```

### 2. Şemayı oluştur ve veriyi doldur

```bash
cd WebApi
dotnet ef database update
```

Bu komut `Module08Products` veritabanını, `Products` tablosunu oluşturur ve
`Data/products.json` içindeki 238 ürünü yükler. Tablo doluysa tekrar veri eklemez,
istediğin kadar çalıştırabilirsin.

### 3. API'yi çalıştır

```bash
dotnet run
```

Varsayılan adres: **http://localhost:5047**

| Adres | Ne var |
|---|---|
| `http://localhost:5047/scalar/v1` | Uçları tarayıcıdan gezip deneyebileceğin arayüz |
| `http://localhost:5047/openapi/v1.json` | OpenAPI dokümanı |
| `http://localhost:5047/api/products` | Ürün listesi (sayfalı) |

---

## Uç Noktalar

| Metot | Adres | Yanıt |
|---|---|---|
| GET | `/api/products` | `200` + `PagedResult<Product>` |
| GET | `/api/products/{id}` | `200` + `Product` · `404` |
| POST | `/api/products` | `201` + `Product` · `400` |
| PUT | `/api/products/{id}` | `200` + `Product` · `400` · `404` |
| DELETE | `/api/products/{id}` | `204` · `404` |
| GET | `/api/products/error-demo` | `500` (bilerek) |

### Sorgu parametreleri

Hepsi `GET /api/products` üzerinde çalışır.

| Parametre | Varsayılan | Açıklama |
|---|---|---|
| `page` | `1` | Sayfa numarası |
| `pageSize` | `10` | Sayfa boyutu (en fazla 200) |
| `sort` | `id` | `name`, `price`, `stock`, `createdAt`. Başına `-` → azalan (`-price`) |
| `name` | — | Ada göre süz (içerir, harf duyarsız) |
| `minPrice` / `maxPrice` | — | Fiyat aralığı (dahil) |
| `minStock` / `maxStock` | — | Stok aralığı (dahil) |

Örnekler:

```
/api/products?page=2&pageSize=12&sort=-price
/api/products?name=kahve
/api/products?minPrice=1000&maxPrice=2000
/api/products?minStock=0&maxStock=0      → tükenmiş ürünler
```

### Gövde (POST / PUT)

```json
{ "name": "Kahve Makinesi", "category": "Mutfak", "price": 2499.90, "stock": 12 }
```

`id` ve `createdAt` gönderilmez — ikisini de sunucu belirler.

**Doğrulama kuralları**

| Alan | Kural |
|---|---|
| `name` | Zorunlu, 2–120 karakter |
| `category` | Zorunlu |
| `price` | 0'dan büyük |
| `stock` | Negatif olamaz (0 geçerlidir — "tükendi") |

Hatalar `400` + `ValidationProblemDetails` olarak döner:

```json
{
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": { "price": ["Price must be greater than zero"] }
}
```

Bulunamayan kayıtlar `404` + `ProblemDetails` döner. Tüm hata yanıtlarının
`Content-Type` başlığı `application/problem+json`'dur.

### Geliştirme yardımcıları

| Ne | Nasıl |
|---|---|
| Yapay gecikme (loading ekranı için) | Herhangi bir uca `?delay=1500` ekle (ms, en fazla 10000) |
| Bilerek hata (error ekranı için) | `GET /api/products/error-demo` → 500 |

İkisi de yalnızca `Development` ortamında çalışır.

---

## Cevap Formatı

Listeleme ucu **sarmalayıcı** bir nesne döner:

```json
{
  "items": [
    { "id": 1, "name": "Terra Aroma Difüzör Max", "category": "Ev & Yaşam",
      "price": 1277.59, "stock": 471, "createdAt": "2026-04-30T09:11:00" }
  ],
  "page": 1,
  "pageSize": 10,
  "total": 238,
  "totalPages": 24,
  "hasPreviousPage": false,
  "hasNextPage": true
}
```

Angular tarafında tipleri şöyle kurarsın:

```typescript
export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
  createdAt: string;
}

export interface PagedResult<T> {
  items: T[];
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasPreviousPage: boolean;
  hasNextPage: boolean;
}
```

Servis tarafı (Modül 7 + 8):

```typescript
private readonly response = httpResource<PagedResult<Product>>(
  () => `http://localhost:5047/api/products?page=${this.page()}&pageSize=10`,
);

readonly products = computed(() => this.response.value()?.items ?? []);
readonly total = computed(() => this.response.value()?.total ?? 0);
```

---

## Proje Yapısı

```
Module08ProductApi/
├── compose.yaml                  → SQL Server container tanımı
├── Module08ProductApi.slnx
└── WebApi/
    ├── Program.cs                → servis kaydı, middleware, pipeline
    ├── appsettings.Development.json → bağlantı dizesi
    ├── Models/
    │   ├── Product.cs            → EF entity'si
    │   ├── PagedResult.cs        → sayfalama sarmalayıcısı
    │   ├── ProductQuery.cs       → ortak filtre/sayfalama nesnesi
    │   └── ProductRequest.cs     → create/update istekleri + doğrulama
    ├── Data/
    │   ├── AppDbContext.cs       → EF yapılandırması (Fluent API)
    │   ├── IProductRepository.cs → veri erişim sözleşmesi
    │   ├── ProductRepository.cs  → EF Core sorguları
    │   ├── DbSeeder.cs           → başlangıç verisi yükleyici
    │   └── products.json         → 238 ürün
    ├── Migrations/               → EF Core migration'ları
    └── Endpoints/
        └── ProductEndpoints.cs   → tüm uçlar
```

### Veritabanı ayarları

`AppDbContext` içinde Fluent API ile tanımlanır:

| Ayar | Neden |
|---|---|
| `Price` → `decimal(18,2)` | Açıkça belirtilmezse EF uyarı verir; kuruşlar kırpılabilir |
| `Name` → `nvarchar(120)` | `nvarchar(max)` index'lenemez ve satır dışı saklanır |
| `Category` → `nvarchar(60)` | Aynı sebep |
| `Category` üzerinde index | En sık filtrelenen alan |
| `CreatedAt` → `SYSUTCDATETIME()` varsayılanı | Tarihi veritabanı verir; `datetime2` ile hassasiyeti eşleşir |

`Id` sütunu `IDENTITY(1,1)` — EF bunu convention ile kurar, ayar gerekmez.

---

## Bağlantı Bilgileri

| | |
|---|---|
| Sunucu | `localhost,1433` |
| Veritabanı | `Module08Products` |
| Kullanıcı | `sa` |
| Şifre | `Passw0rd!2026` |
| Container | `module08-sql` |

Bağlantı dizesi `WebApi/appsettings.Development.json` içindedir ve
**`TrustServerCertificate=True`** içerir. Bu şart: container'daki SQL Server kendi
ürettiği self-signed sertifikayı kullanır, `Microsoft.Data.SqlClient` ise 4.0'dan beri
varsayılan olarak şifreli bağlantı ister. Bu ayar olmadan bağlantı sertifika hatasıyla
reddedilir. **Yalnızca yerel geliştirme içindir.**

> Bu şifre yerel bir geliştirme container'ına aittir. Gerçek projede bağlantı dizesi
> `dotnet user-secrets` ile saklanır, kaynak koda yazılmaz.

---

## Sık Karşılaşılanlar

**Bağlantı hatası alıyorum**
Container ayakta mı? `docker compose ps` ile kontrol et, `STATUS` sütununda `(healthy)`
yazmalı. Container "Up" görünse bile SQL Server'ın istek kabul etmesi ~30 saniye sürer.

**Veriyi sıfırlamak istiyorum**

```bash
docker compose down -v      # -v volume'ü de siler
docker compose up -d
cd WebApi && dotnet ef database update
```

**Tabloyu Rider'da göremiyorum**
Database penceresinde veri kaynağının yanındaki `1 of 5` rozetine tıkla,
`Module08Products` kutusunu işaretle. Rider yalnızca işaretli veritabanlarını tarar.
