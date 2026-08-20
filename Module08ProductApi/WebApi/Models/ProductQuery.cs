namespace WebApi.Models;

/// <summary>
/// Tüm listeleme uçlarının ortak filtre/sayfalama nesnesi.
/// Böylece by-name / by-price / by-stock uçları aynı mantığı paylaşır.
/// </summary>
public sealed class ProductQuery
{
    public string? Name { get; init; }
    public decimal? MinPrice { get; init; }
    public decimal? MaxPrice { get; init; }
    public int? MinStock { get; init; }
    public int? MaxStock { get; init; }

    /// <summary>name | price | stock | createdAt (başına '-' koyulursa azalan: "-price")</summary>
    public string? Sort { get; init; }

    public int Page { get; init; } = 1;
    public int PageSize { get; init; } = 10;
    public const int MaxPageSize = 200;

    public ProductQuery Normalized() => new()
    {
        Name = string.IsNullOrWhiteSpace(Name) ? null : Name.Trim(),
        MinPrice = MinPrice,
        MaxPrice = MaxPrice,
        MinStock = MinStock,
        MaxStock = MaxStock,
        Sort = string.IsNullOrWhiteSpace(Sort) ? null : Sort.Trim(),
        Page = Page < 1 ? 1 : Page,
        PageSize = PageSize < 1 ? 10 : PageSize > MaxPageSize ? MaxPageSize : PageSize
    };
}