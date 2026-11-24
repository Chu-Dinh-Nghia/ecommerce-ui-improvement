using Microsoft.EntityFrameworkCore;
using SourceCode.Models;

namespace SourceCode.Data;

public static class DbInitializer
{
    public static async Task SeedAsync(ApplicationDbContext db)
    {
        if (await db.Movies.AnyAsync()) return;
        var adventure = new Genre { Name = "Phiêu lưu" };
        var mystery = new Genre { Name = "Bí ẩn" };
        var science = new Genre { Name = "Khoa học viễn tưởng" };
        db.Genres.AddRange(adventure, mystery, science);
        db.Movies.AddRange(
            new Movie { Title = "Đường Đến Sao Mai", Summary = "Một chuyến tàu xuyên các chòm sao đưa hai người bạn đi tìm tín hiệu cuối cùng của Trái Đất.", Genre = science, Price = 79000, Rated = 4.8, ReleaseDate = DateTime.Today.AddDays(40), PicturePath = "/images/duong-den-sao-mai.svg" },
            new Movie { Title = "Hải Đăng Cuối Biển", Summary = "Trên hòn đảo nhỏ, người giữ hải đăng phát hiện những bức thư gửi từ tương lai.", Genre = mystery, Price = 69000, Rated = 4.5, ReleaseDate = DateTime.Today.AddDays(55), PicturePath = "/images/hai-dang-cuoi-bien.svg" },
            new Movie { Title = "Mùa Gió Trên Cao", Summary = "Một nhóm bạn trẻ đi qua rặng núi để hoàn thành lời hứa còn dang dở.", Genre = adventure, Price = 59000, Rated = 4.6, ReleaseDate = DateTime.Today.AddDays(70), PicturePath = "/images/mua-gio-tren-cao.svg" },
            new Movie { Title = "Ký Ức Trong Mưa", Summary = "Từng cơn mưa mở ra một mảnh ký ức, dẫn cô gái về bí mật của thành phố cũ.", Genre = mystery, Price = 89000, Rated = 4.9, ReleaseDate = DateTime.Today.AddDays(85), PicturePath = "/images/ky-uc-trong-mua.svg" },
            new Movie { Title = "Vùng Trời Thứ Chín", Summary = "Phi hành đoàn trẻ tìm đường trở về sau khi khám phá một hành tinh không có trên bản đồ.", Genre = science, Price = 99000, Rated = 4.7, ReleaseDate = DateTime.Today.AddDays(100), PicturePath = "/images/vung-troi-thu-chin.svg" }
        );
        await db.SaveChangesAsync();
    }
}
