using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using SourceCode.Data;
using SourceCode.Models;

namespace SourceCode.Services;

public class CartService(ApplicationDbContext db, IHttpContextAccessor accessor)
{
    private const string Key = "CineNghia.Cart";
    private ISession Session => accessor.HttpContext!.Session;

    private List<CartEntry> Read() =>
        JsonSerializer.Deserialize<List<CartEntry>>(Session.GetString(Key) ?? "[]") ?? [];

    private void Write(List<CartEntry> entries) =>
        Session.SetString(Key, JsonSerializer.Serialize(entries));

    public async Task<CartViewModel> GetAsync()
    {
        var entries = Read().Where(x => x.Quantity > 0).ToList();
        var ids = entries.Select(x => x.MovieId).ToArray();
        var movies = await db.Movies.AsNoTracking().Where(x => ids.Contains(x.Id)).ToDictionaryAsync(x => x.Id);
        return new CartViewModel
        {
            Lines = entries.Where(x => movies.ContainsKey(x.MovieId))
                .Select(x => new CartLine(movies[x.MovieId], x.Quantity)).ToList()
        };
    }

    public void Add(int movieId)
    {
        var entries = Read();
        var current = entries.FindIndex(x => x.MovieId == movieId);
        if (current < 0) entries.Add(new CartEntry(movieId, 1));
        else entries[current] = entries[current] with { Quantity = Math.Min(99, entries[current].Quantity + 1) };
        Write(entries);
    }

    public void SetQuantity(int movieId, int quantity)
    {
        var entries = Read();
        entries.RemoveAll(x => x.MovieId == movieId);
        if (quantity > 0) entries.Add(new CartEntry(movieId, Math.Min(quantity, 99)));
        Write(entries);
    }

    public void Clear() => Session.Remove(Key);
}
