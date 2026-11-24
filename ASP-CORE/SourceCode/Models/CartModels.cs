using System.ComponentModel.DataAnnotations;

namespace SourceCode.Models;

public record CartEntry(int MovieId, int Quantity);
public record CartLine(Movie Movie, int Quantity)
{
    public decimal Subtotal => Movie.Price * Quantity;
}
public class CartViewModel
{
    public List<CartLine> Lines { get; set; } = [];
    public decimal Total => Lines.Sum(x => x.Subtotal);
    public int Count => Lines.Sum(x => x.Quantity);
}
public class CheckoutViewModel
{
    [Required(ErrorMessage = "Vui lòng nhập họ tên."), StringLength(120)]
    [Display(Name = "Họ tên")]
    public string Name { get; set; } = "";
    [Required(ErrorMessage = "Vui lòng nhập địa chỉ."), StringLength(250)]
    [Display(Name = "Địa chỉ")]
    public string Address { get; set; } = "";
    [Required(ErrorMessage = "Vui lòng nhập email."), EmailAddress]
    public string Email { get; set; } = "";
    [Required(ErrorMessage = "Vui lòng nhập số điện thoại."), Phone]
    [Display(Name = "Số điện thoại")]
    public string Mobile { get; set; } = "";
    public CartViewModel Cart { get; set; } = new();
}
