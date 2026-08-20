using WebApi.Data;
using WebApi.Models;

namespace WebApi.Endpoints;

public static class ProductEndpoints
{
    public static IEndpointRouteBuilder MapProductEndpoints(this IEndpointRouteBuilder endpoints)
    {
        var group = endpoints.MapGroup("/api/products");


        group.MapGet("",
            async (IProductRepository repository, CancellationToken ct,
                string? name, decimal? minPrice, decimal? maxPrice, int? minStock, int? maxStock, string? sort, int page = 1, int pageSize = 10) =>
            {
                var query = new ProductQuery
                {
                    Name = name,
                    MinPrice = minPrice,
                    MaxPrice = maxPrice,
                    MinStock = minStock,
                    MaxStock = maxStock,
                    Sort = sort,
                    Page = page,
                    PageSize = pageSize
                };

                var pagedResult = await repository.GetPagedAsync(query, ct);
                return Results.Ok(pagedResult);
            });

        group.MapGet("{id:int}",
            async (IProductRepository repository, CancellationToken ct, int id) =>
            {
                var product = await repository.GetByIdAsync(id, ct);

                return product is null
                    ? Results.NotFound()
                    : Results.Ok(product);
            });

        group.MapPost("",
            async (IProductRepository repository, CancellationToken ct, CreateProductRequest request) =>
            {
                var errors = ProductValidation.Validate(request.Name, request.Category, request.Price, request.Stock);
                if (errors.Count != 0)
                {
                    return Results.ValidationProblem(errors);
                }

                var addedResult = await repository.AddAsync(request, ct);

                return Results.Created($"/api/products/{addedResult.Id}", addedResult);
            });

        group.MapPut("{id:int}",
            async (IProductRepository repository, CancellationToken ct, int id, UpdateProductRequest request) =>
            {
                var errors = ProductValidation.Validate(request.Name, request.Category, request.Price, request.Stock);
                if (errors.Count != 0)
                {
                    return Results.ValidationProblem(errors);
                }

                var updatedResult = await repository.UpdateAsync(id, request, ct);

                return updatedResult is null
                    ? Results.NotFound()
                    : Results.Ok(updatedResult);
            });

        group.MapDelete("{id:int}",
            async (IProductRepository repository, CancellationToken ct, int id) =>
            {
                var deletedResult = await repository.DeleteAsync(id, ct);

                return deletedResult
                    ? Results.NoContent()
                    : Results.NotFound();
            });

        group.MapGet("error-demo", Results.InternalServerError);

        return endpoints;
    }
}