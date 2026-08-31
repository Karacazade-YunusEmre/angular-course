using Microsoft.EntityFrameworkCore;
using Scalar.AspNetCore;
using WebApi.Data;
using WebApi.Endpoints;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();

// Hatalarin RFC 7807 "ProblemDetails" formatinda donmesi icin.
// UseExceptionHandler ve UseStatusCodePages bu servisi kullanir; kayitli
// olmazsa UseExceptionHandler baslangicta istisna firlatir.
builder.Services.AddProblemDetails();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))
        // "dotnet ef database update" ve Migrate() senkron olanı çağırır.
        .UseSeeding((db, _) => DbSeeder.Seed(db))
        // Uygulama içinden MigrateAsync() çağrılırsa bu çalışır.
        // İkisi de aynı metoda gidiyor, mantık tek yerde duruyor.
        .UseAsyncSeeding((db, _, _) =>
        {
            DbSeeder.Seed(db);
            return Task.CompletedTask;
        }));

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:4200", "https://localhost:4200")
            .AllowAnyMethod()
            .AllowAnyHeader();
    });
});

builder.Services.AddScoped<IProductRepository, ProductRepository>();


var app = builder.Build();

// Geliştirme ortamında bekleyen migration'ları uygular; veritabanı yoksa oluşturur.
// Olmadığı zaman, container'ın volume'ü silindiğinde ya da proje başka bir makinede
// ilk kez açıldığında istekler "Failed to open the explicitly specified database"
// hatasıyla düşer. Migrate() ayrıca DbContext'teki UseAsyncSeeding'i tetikler,
// yani tablo oluştuktan sonra products.json otomatik yüklenir.
// Üretimde bu kalıp önerilmez: migration'ı uygulamanın kendisi değil, ayrı bir
// dağıtım adımı çalıştırmalı — aksi halde her replika aynı anda şemayı değiştirmeye çalışır.
if (app.Environment.IsDevelopment())
{
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync();
}

app.UseExceptionHandler();

app.UseStatusCodePages();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.UseRouting();

app.UseCors();

// Yapay gecikme - Angular'da yukleniyor (loading) ekranini gorebilmek icin.
// Herhangi bir uca ?delay=1500 eklenince istegi 1,5 saniye bekletir.
// Sadece gelistirme ortaminda calisir; uretimde servis disi birakma araci olurdu.
if (app.Environment.IsDevelopment())
{
    app.Use(async (context, next) =>
    {
        if (context.Request.Query.TryGetValue("delay", out var raw)
            && int.TryParse(raw, out var ms))
        {
            // Ust sinir 10 saniye: kimse istegi sonsuza kadar tutamasin.
            // RequestAborted: istemci vazgecerse bekleme de iptal olsun.
            await Task.Delay(Math.Clamp(ms, 0, 10_000), context.RequestAborted);
        }

        await next();
    });
}

app.MapProductEndpoints();


app.Run();