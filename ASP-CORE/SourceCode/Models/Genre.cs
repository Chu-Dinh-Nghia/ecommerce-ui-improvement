using System.ComponentModel.DataAnnotations;

namespace SourceCode.Models;

public class Genre
{
    public int Id { get; set; }
    [Required(ErrorMessage = "Vui lòng nhập tên thể loại.")]
    [StringLength(80)]
    [Display(Name = "Thể loại")]
    public string Name { get; set; } = "";
    public ICollection<Movie> Movies { get; set; } = new List<Movie>();
}
