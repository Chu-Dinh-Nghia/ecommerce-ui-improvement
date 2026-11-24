using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SourceCode.Data;
using SourceCode.Models;
using SourceCode.Services;

namespace SourceCode.Controllers;

public class CartController(ApplicationDbContext db, CartService cart, OrderEmailService email) : Controller
{
    public async Task<IActionResult> Index() => View(await cart.GetAsync());

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Add(int id)
    {
        if (!await db.Movies.AnyAsync(x => x.Id == id)) return NotFound();
        cart.Add(id);
        return RedirectToAction(nameof(Index));
    }

    [HttpPost, ValidateAntiForgeryToken]
    public IActionResult Update(int id, int quantity)
    {
        cart.SetQuantity(id, quantity);
        return RedirectToAction(nameof(Index));
    }

    [HttpPost, ValidateAntiForgeryToken]
    public IActionResult Remove(int id)
    {
        cart.SetQuantity(id, 0);
        return RedirectToAction(nameof(Index));
    }

    public async Task<IActionResult> Checkout()
    {
        var current = await cart.GetAsync();
        if (current.Count == 0) return RedirectToAction(nameof(Index));
        return View(new CheckoutViewModel { Cart = current });
    }

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Checkout(CheckoutViewModel model)
    {
        model.Cart = await cart.GetAsync();
        if (model.Cart.Count == 0) ModelState.AddModelError("", "Giỏ hàng đang trống.");
        if (!ModelState.IsValid) return View(model);

        var order = new Order
        {
            CustomerName = model.Name.Trim(),
            Address = model.Address.Trim(),
            Email = model.Email.Trim(),
            Mobile = model.Mobile.Trim(),
            Total = model.Cart.Total,
            Items = model.Cart.Lines.Select(x => new OrderItem
            {
                MovieId = x.Movie.Id,
                Movie = x.Movie,
                Quantity = x.Quantity,
                UnitPrice = x.Movie.Price
            }).ToList()
        };
        // Only reference existing Movie rows; EF must not try to insert them again.
        foreach (var item in order.Items) item.Movie = null;
        db.Orders.Add(order);
        await db.SaveChangesAsync();
        cart.Clear();
        foreach (var item in order.Items)
            item.Movie = model.Cart.Lines.First(x => x.Movie.Id == item.MovieId).Movie;
        await email.SendAsync(order);
        return RedirectToAction(nameof(Completed), new { id = order.Id });
    }

    public async Task<IActionResult> Completed(int id)
    {
        var order = await db.Orders.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return order is null ? NotFound() : View(order);
    }
}
