using Microsoft.EntityFrameworkCore;
using WebApi.Models;

namespace WebApi.Data;

public class ProductRepository(AppDbContext context) : IProductRepository
{
    public async Task<PagedResult<Product>> GetPagedAsync(ProductQuery query, CancellationToken ct)
    {
        var q = query.Normalized();
        var queryable = context.Products.AsNoTracking();

        if (q.Name is not null)
        {
            queryable = queryable.Where(p => p.Name.Contains(q.Name));
        }

        if (q.MinPrice is not null)
        {
            queryable = queryable.Where(p => p.Price >= q.MinPrice.Value);
        }

        if (q.MaxPrice is not null)
        {
            queryable = queryable.Where(p => p.Price <= q.MaxPrice.Value);
        }

        if (q.MinStock is not null)
        {
            queryable = queryable.Where(p => p.Stock >= q.MinStock.Value);
        }

        if (q.MaxStock is not null)
        {
            queryable = queryable.Where(p => p.Stock <= q.MaxStock.Value);
        }

        // --- Sıralama ---
        // q.Sort örnekleri: "price" (artan), "-price" (azalan), null (varsayılan).
        // Baştaki '-' yönü belirtir; kalan kısım alan adıdır.
        var sort = q.Sort ?? string.Empty;
        var descending = sort.StartsWith('-');
        var field = sort.TrimStart('-').ToLowerInvariant();

        // Sıralama zorunlu: SQL Server'da OFFSET/FETCH (yani Skip/Take) bir ORDER BY
        // olmadan çalışmaz. Sıralama vermezsek EF araya "ORDER BY (SELECT 1)" koyar,
        // satır sırası tanımsız kalır ve aynı ürün iki farklı sayfada görünebilir.
        //
        // ThenBy(p => p.Id): eşit değerli kayıtların (ör. aynı fiyatlı iki ürün)
        // kendi aralarındaki sırasını sabitler. Bu olmadan sayfalar arası zıplama olur.
        queryable = (field, descending) switch
        {
            ("name", false) => queryable.OrderBy(p => p.Name).ThenBy(p => p.Id),
            ("name", true) => queryable.OrderByDescending(p => p.Name).ThenBy(p => p.Id),

            ("price", false) => queryable.OrderBy(p => p.Price).ThenBy(p => p.Id),
            ("price", true) => queryable.OrderByDescending(p => p.Price).ThenBy(p => p.Id),

            ("stock", false) => queryable.OrderBy(p => p.Stock).ThenBy(p => p.Id),
            ("stock", true) => queryable.OrderByDescending(p => p.Stock).ThenBy(p => p.Id),

            ("createdat", false) => queryable.OrderBy(p => p.CreatedAt).ThenBy(p => p.Id),
            ("createdat", true) => queryable.OrderByDescending(p => p.CreatedAt).ThenBy(p => p.Id),

            // Boş ya da tanınmayan sort değeri: eklenme sırası.
            // Id zaten clustered primary key olduğu için bu sıralama bedavaya gelir.
            _ => queryable.OrderBy(p => p.Id),
        };

        return new PagedResult<Product>
        {
            Total = await queryable.CountAsync(ct),
            Items = await queryable.Skip(q.PageSize * (q.Page - 1)).Take(q.PageSize).ToListAsync(cancellationToken: ct),
            Page = q.Page,
            PageSize = q.PageSize
        };
    }

    public async Task<Product?> GetByIdAsync(int id, CancellationToken ct)
    {
        return await context.Products.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id, ct);
    }

    public async Task<Product> AddAsync(CreateProductRequest request, CancellationToken ct)
    {
        var entityEntry = context.Add(new Product
        {
            Name = request.Name,
            Category = request.Category,
            Price = request.Price,
            Stock = request.Stock,
        });
        await context.SaveChangesAsync(ct);

        return entityEntry.Entity;
    }

    public async Task<bool> DeleteAsync(int id, CancellationToken ct)
    {
        var affected = await context.Products.Where(p => p.Id == id)
            .ExecuteDeleteAsync(ct);
        return affected > 0;
    }

    public async Task<Product?> UpdateAsync(int id, UpdateProductRequest request, CancellationToken ct)
    {
        var currentProduct = await context.Products.FindAsync([id], ct);

        if (currentProduct is null) return null;

        currentProduct.Name = request.Name;
        currentProduct.Category = request.Category;
        currentProduct.Price = request.Price;
        currentProduct.Stock = request.Stock;
        await context.SaveChangesAsync(ct);

        return currentProduct;
    }
}