using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SourceCode.Models;

public class Order
{
    public int Id { get; set; }
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    [Column(TypeName = "decimal(18,2)")]
    public decimal Total { get; set; }
    [Required, StringLength(120)]
    public string CustomerName { get; set; } = "";
    [Required, StringLength(250)]
    public string Address { get; set; } = "";
    [Required, EmailAddress, StringLength(160)]
    public string Email { get; set; } = "";
    [Required, Phone, StringLength(30)]
    public string Mobile { get; set; } = "";
    public ICollection<OrderItem> Items { get; set; } = new List<OrderItem>();
}
