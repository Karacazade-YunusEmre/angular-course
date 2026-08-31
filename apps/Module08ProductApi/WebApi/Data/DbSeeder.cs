using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using WebApi.Models;

namespace WebApi.Data;

/// <summary>
/// Products tablosu boşsa, Data/products.json içindeki ürünlerle doldurur.
/// Program.cs'teki UseSeeding / UseAsyncSeeding tarafından çağrılır.
/// </summary>
public static class DbSeeder
{
    /// <summary>
    /// products.json içindeki bir ürünün şekli.
    /// Dosyadaki "id" ve "description" alanları bilerek yok:
    /// Id'yi SQL Server IDENTITY olarak üretiyor, Description ise modelde yok.
    /// System.Text.Json, karşılığı olmayan JSON alanlarını sessizce atlar.
    /// </summary>
    private sealed record ProductSeedItem(
        string Name,
        string Category,
        decimal Price,
        int Stock,
        DateTime CreatedAt);

    // JSON'da alan adları küçük harfle ("name"), C#'ta büyük harfle (Name).
    // Bu ayar olmadan hiçbir alan eşleşmez ve tüm ürünler boş gelir — üstelik hata da vermez.
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
    };

    public static void Seed(DbContext db)
    {
        var products = db.Set<Product>();

        // Bu metot her "dotnet ef database update" ve her Migrate() çağrısında çalışır.
        // Kontrol olmasaydı her seferinde 238 ürün daha eklenirdi.
        if (products.Any())
        {
            return;
        }

        // Çalışan .dll'in bulunduğu klasör (bin/Debug/net10.0/).
        // Directory.GetCurrentDirectory() kullanılsaydı dotnet run ile dotnet ef
        // farklı klasörleri gösterirdi; BaseDirectory her iki durumda da doğru.
        var path = Path.Combine(AppContext.BaseDirectory, "Data", "products.json");

        if (!File.Exists(path))
        {
            throw new FileNotFoundException(
                $"Seed dosyası bulunamadı: {path}. " +
                "WebApi.csproj içindeki CopyToOutputDirectory ayarını kontrol et.");
        }

        var json = File.ReadAllText(path);
        var items = JsonSerializer.Deserialize<List<ProductSeedItem>>(json, JsonOptions);

        if (items is null || items.Count == 0)
        {
            return;
        }

        var toInsert = items.Select(item => new Product
        {
            // Id atanmıyor: IDENTITY sütununu SQL Server dolduruyor.
            // Elle değer verilseydi "Cannot insert explicit value for identity column" hatası alınırdı.
            Name = item.Name,
            Category = item.Category,
            Price = item.Price,
            Stock = item.Stock,

            // CreatedAt'i açıkça veriyoruz ki ürünler farklı tarihlere yayılsın.
            // Atanmasaydı sütunun SYSUTCDATETIME() varsayılanı devreye girer,
            // 238 ürünün hepsi aynı saniyeyi alır ve tarihe göre sıralama anlamsızlaşırdı.
            CreatedAt = item.CreatedAt,
        }).ToList();

        products.AddRange(toInsert);
        db.SaveChanges();
    }
}
