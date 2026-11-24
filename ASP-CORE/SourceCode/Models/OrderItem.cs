using System.ComponentModel.DataAnnotations.Schema;

namespace SourceCode.Models;

public class OrderItem
{
    public int Id { get; set; }
    public int OrderId { get; set; }
    public Order? Order { get; set; }
    public int MovieId { get; set; }
    public Movie? Movie { get; set; }
    public int Quantity { get; set; }
    [Column(TypeName = "decimal(18,2)")]
    public decimal UnitPrice { get; set; }
}
