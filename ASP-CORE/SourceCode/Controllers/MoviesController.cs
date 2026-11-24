using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using SourceCode.Data;
using SourceCode.Models;

namespace SourceCode.Controllers;

public class MoviesController(ApplicationDbContext db, IWebHostEnvironment env) : Controller
{
    public async Task<IActionResult> Index() => View(await db.Movies.AsNoTracking().Include(x => x.Genre)
        .OrderByDescending(x => x.Id).ToListAsync());

    public async Task<IActionResult> Details(int id)
    {
        var movie = await db.Movies.AsNoTracking().Include(x => x.Genre).FirstOrDefaultAsync(x => x.Id == id);
        return movie is null ? NotFound() : View(movie);
    }

    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Create()
    {
        await SetGenresAsync();
        return View(new Movie());
    }

    [HttpPost, ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Create([Bind("Title,Summary,ReleaseDate,Price,Rated,GenreId,PictureUpload")] Movie movie)
    {
        if (!await db.Genres.AnyAsync(x => x.Id == movie.GenreId))
            ModelState.AddModelError(nameof(movie.GenreId), "Thể loại không tồn tại.");
        if (movie.ReleaseDate.Date < DateTime.Today)
            ModelState.AddModelError(nameof(movie.ReleaseDate), "Ngày phát hành không được ở quá khứ.");
        if (ModelState.IsValid)
        {
            try
            {
                movie.PicturePath = await SaveImageAsync(movie.PictureUpload) ?? "/images/no-image.svg";
                db.Movies.Add(movie);
                await db.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (InvalidDataException ex) { ModelState.AddModelError(nameof(movie.PictureUpload), ex.Message); }
        }
        await SetGenresAsync(movie.GenreId);
        return View(movie);
    }

    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Edit(int id)
    {
        var movie = await db.Movies.FindAsync(id);
        if (movie is null) return NotFound();
        await SetGenresAsync(movie.GenreId);
        return View(movie);
    }

    [HttpPost, ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Edit(int id, [Bind("Id,Title,Summary,ReleaseDate,Price,Rated,GenreId,PictureUpload")] Movie input)
    {
        if (id != input.Id) return NotFound();
        var movie = await db.Movies.FindAsync(id);
        if (movie is null) return NotFound();
        if (!await db.Genres.AnyAsync(x => x.Id == input.GenreId))
            ModelState.AddModelError(nameof(input.GenreId), "Thể loại không tồn tại.");
        if (input.ReleaseDate.Date < DateTime.Today)
            ModelState.AddModelError(nameof(input.ReleaseDate), "Ngày phát hành không được ở quá khứ.");
        if (ModelState.IsValid)
        {
            try
            {
                var newPath = await SaveImageAsync(input.PictureUpload);
                movie.Title = input.Title;
                movie.Summary = input.Summary;
                movie.ReleaseDate = input.ReleaseDate;
                movie.Price = input.Price;
                movie.Rated = input.Rated;
                movie.GenreId = input.GenreId;
                if (newPath is not null) movie.PicturePath = newPath;
                await db.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (InvalidDataException ex) { ModelState.AddModelError(nameof(input.PictureUpload), ex.Message); }
        }
        input.PicturePath = movie.PicturePath;
        await SetGenresAsync(input.GenreId);
        return View(input);
    }

    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Delete(int id)
    {
        var movie = await db.Movies.AsNoTracking().Include(x => x.Genre).FirstOrDefaultAsync(x => x.Id == id);
        return movie is null ? NotFound() : View(movie);
    }

    [HttpPost, ActionName("Delete"), ValidateAntiForgeryToken, Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var movie = await db.Movies.FindAsync(id);
        if (movie is null) return NotFound();
        if (await db.OrderItems.AnyAsync(x => x.MovieId == id))
        {
            TempData["Notice"] = "Phim đã có trong đơn hàng, không thể xóa để giữ lịch sử mua hàng.";
            return RedirectToAction(nameof(Index));
        }
        db.Movies.Remove(movie);
        await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    private async Task SetGenresAsync(int? selected = null) =>
        ViewBag.GenreId = new SelectList(await db.Genres.OrderBy(x => x.Name).ToListAsync(), "Id", "Name", selected);

    private async Task<string?> SaveImageAsync(IFormFile? file)
    {
        if (file is null || file.Length == 0) return null;
        if (file.Length > 2 * 1024 * 1024) throw new InvalidDataException("Ảnh tối đa 2 MB.");
        var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
        if (ext is not (".jpg" or ".jpeg" or ".png" or ".webp"))
            throw new InvalidDataException("Chỉ nhận ảnh JPG, PNG hoặc WebP.");
        var folder = Path.Combine(env.WebRootPath, "images", "uploads");
        Directory.CreateDirectory(folder);
        var name = Guid.NewGuid().ToString("N") + ext;
        await using var stream = System.IO.File.Create(Path.Combine(folder, name));
        await file.CopyToAsync(stream);
        return "/images/uploads/" + name;
    }
}
