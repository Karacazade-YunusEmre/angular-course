using Microsoft.EntityFrameworkCore;
using WebApi.Models;

namespace WebApi.Data;

public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("Products");
            entity.HasKey(p => p.Id);
            entity.Property(p => p.Name).IsRequired().HasMaxLength(120);
            entity.Property(p => p.Category).IsRequired().HasMaxLength(60);
            entity.Property(p => p.Price).HasPrecision(18, 2);
            entity.Property(p => p.CreatedAt).HasDefaultValueSql("SYSUTCDATETIME()");
            entity.HasIndex(p => p.Category);
        });
    }
}