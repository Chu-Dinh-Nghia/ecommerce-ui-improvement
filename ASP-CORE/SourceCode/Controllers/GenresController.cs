using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SourceCode.Data;
using SourceCode.Models;

namespace SourceCode.Controllers;

public class GenresController(ApplicationDbContext db) : Controller
{
    public async Task<IActionResult> Index() => View(await db.Genres.AsNoTracking()
        .Include(x => x.Movies).OrderBy(x => x.Name).ToListAsync());

    [Authorize(Policy = "AdminOnly")]
    public IActionResult Create() => View(new Genre());

    [HttpPost, ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Create([Bind("Name")] Genre genre)
    {
        if (await db.Genres.AnyAsync(x => x.Name == genre.Name))
            ModelState.AddModelError(nameof(genre.Name), "Thể loại đã tồn tại.");
        if (!ModelState.IsValid) return View(genre);
        db.Genres.Add(genre);
        await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Edit(int id) => await db.Genres.FindAsync(id) is { } genre ? View(genre) : NotFound();

    [HttpPost, ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Edit(int id, [Bind("Id,Name")] Genre input)
    {
        if (id != input.Id) return NotFound();
        var genre = await db.Genres.FindAsync(id);
        if (genre is null) return NotFound();
        if (await db.Genres.AnyAsync(x => x.Id != id && x.Name == input.Name))
            ModelState.AddModelError(nameof(input.Name), "Thể loại đã tồn tại.");
        if (!ModelState.IsValid) return View(input);
        genre.Name = input.Name;
        await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Delete(int id) => await db.Genres.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id) is { } genre ? View(genre) : NotFound();

    [HttpPost, ActionName("Delete"), ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var genre = await db.Genres.FindAsync(id);
        if (genre is null) return NotFound();
        if (await db.Movies.AnyAsync(x => x.GenreId == id))
        {
            TempData["Notice"] = "Thể loại đang có phim, hãy chuyển phim sang thể loại khác trước.";
            return RedirectToAction(nameof(Index));
        }
        db.Genres.Remove(genre);
        await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }
}
