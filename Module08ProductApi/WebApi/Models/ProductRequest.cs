namespace WebApi.Models;

/// <summary> Yeni ürün oluşturma isteği </summary>
public sealed record CreateProductRequest(
    string Name,
    string Category,
    decimal Price,
    int Stock);

/// <summary> ürün güncelleme isteği </summary>
public sealed record UpdateProductRequest(
    string Name,
    string Category,
    decimal Price,
    int Stock
);

/// <summary>
/// Basit doğrulama yardımcıları. Hata varsa alan adı -> mesaj sözlüğü döner;
/// boş sözlük "geçerli" demektir.
/// </summary>
public static class ProductValidation
{
    public static Dictionary<string, string[]> Validate(string name, string category, decimal price, int stock)
    {
        var errors = new Dictionary<string, string[]>();

        if (string.IsNullOrWhiteSpace(name))
        {
            errors[nameof(name)] = ["Name is required"];
        }
        else if (name.Trim().Length < 2 || name.Trim().Length > 120)
        {
            errors[nameof(name)] = ["ürün adı 2-120 karakter arasında olmalıdır."];
        }

        if (string.IsNullOrWhiteSpace(category))
        {
            errors[nameof(category)] = ["Category is required"];
        }

        if (price <= 0)
        {
            errors[nameof(price)] = ["Price must be greater than zero"];
        }

        if (stock < 0)
        {
            errors[nameof(stock)] = ["Stock cannot be less than zero"];
        }

        return errors;
    }
}