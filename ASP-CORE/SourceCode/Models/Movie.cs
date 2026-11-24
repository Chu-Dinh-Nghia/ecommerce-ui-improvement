using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SourceCode.Models;

public class Movie
{
    public int Id { get; set; }
    [Required(ErrorMessage = "Vui lòng nhập tên phim.")]
    [StringLength(200, MinimumLength = 3)]
    [Display(Name = "Tên phim")]
    public string Title { get; set; } = "";
    [StringLength(2000)]
    [Display(Name = "Giới thiệu")]
    public string? Summary { get; set; }
    [DataType(DataType.Date)]
    [Display(Name = "Ngày phát hành")]
    public DateTime ReleaseDate { get; set; } = DateTime.Today.AddDays(1);
    [Range(5000, 10000000, ErrorMessage = "Giá phải từ 5.000đ đến 10.000.000đ.")]
    [Column(TypeName = "decimal(18,2)")]
    [Display(Name = "Giá")]
    public decimal Price { get; set; }
    [Range(1, 5)]
    [Display(Name = "Đánh giá")]
    public double Rated { get; set; } = 5;
    [Required(ErrorMessage = "Vui lòng chọn thể loại.")]
    [Display(Name = "Thể loại")]
    public int GenreId { get; set; }
    public Genre? Genre { get; set; }
    [Display(Name = "Poster")]
    public string PicturePath { get; set; } = "/images/no-image.svg";
    [NotMapped]
    [Display(Name = "Tải poster")]
    public IFormFile? PictureUpload { get; set; }
}
