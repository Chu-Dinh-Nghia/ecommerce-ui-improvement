# CINÉ NGHĨA

Website bán phim cho bài tập cá nhân ASP.NET Core MVC. Dự án nằm trong `SourceCode/`; các bài thực hành trước trong repository được giữ nguyên.

Website public: [cinenghia409.somee.com](http://cinenghia409.somee.com/). Hosting Somee miễn phí dùng SQL Server `CineNghia409`; cấu hình production có mật khẩu chỉ nằm trên hosting.

## Công nghệ

- ASP.NET Core MVC và Identity trên .NET 10
- Entity Framework Core 10, SQL Server, Migrations
- Razor Views, Bootstrap 5, CSS tùy chỉnh, Session cho giỏ hàng

## Chức năng

- Danh mục 5 phim và 3 thể loại mẫu với poster do dự án tự tạo; giao diện responsive và nhận diện CINÉ NGHĨA.
- Quản trị viên có thể thêm, xem, sửa, xóa phim và thể loại; upload JPG/PNG/WebP tối đa 2 MB, giữ ảnh cũ khi sửa, dùng ảnh mặc định khi không upload.
- Giỏ hàng thêm phim, đổi số lượng, xóa phim và tính tổng tiền. Checkout kiểm tra thông tin giao hàng, lưu đơn và chi tiết đơn trong SQL Server.
- Gửi email xác nhận qua Gmail SMTP khi đã cấu hình App Password; đơn vẫn lưu nếu gửi email thất bại.

## Cấu trúc

```text
ASP-CORE/
├── README.md
├── Report/                 Báo cáo Word và ảnh chụp thực tế
└── SourceCode/
    ├── Controllers/        Phim, thể loại, giỏ hàng
    ├── Data/               DbContext, migration, dữ liệu mẫu
    ├── Models/             Movie, Genre, Order, OrderItem
    ├── Services/           Giỏ hàng và email
    ├── Views/              Giao diện Razor
    └── wwwroot/images/     Poster mẫu và ảnh upload
```

## Chạy trên máy

1. Cài .NET 10 SDK và SQL Server. Mặc định `appsettings.json` dùng `Server=.\\SQLEXPRESS` với Windows Authentication và database `CineNghia_LMS`.
2. Nếu SQL Server của bạn khác, đặt biến môi trường `ConnectionStrings__DefaultConnection` hoặc dùng .NET User Secrets. Không lưu mật khẩu trong Git.
3. Trong `SourceCode/`, chạy `dotnet restore`, `dotnet build`, `dotnet run`. Lần chạy đầu tự áp dụng migration và thêm dữ liệu mẫu.
4. Mở URL được in ở dòng `Now listening on`. Đăng ký tài khoản bằng email cấu hình ở `Admin:Email`, xác nhận tài khoản qua trang Register confirmation, sau đó đăng nhập để quản lý dữ liệu.

Để chạy migration riêng: `dotnet ef database update`. Tool `dotnet-ef` cần dùng bản `10.0.*`.

## Triển khai

Tạo website .NET 10 và một database MSSQL trên hosting; đặt `ConnectionStrings__DefaultConnection` bằng chuỗi kết nối của database hosting, `Admin__Email` bằng email quản trị, và `Admin__Password` bằng mật khẩu mạnh chỉ lưu trong cấu hình hosting. Bản production sẽ từ chối khởi động nếu thiếu `Admin__Password`; khi khởi động lần đầu, ứng dụng tạo tài khoản quản trị đã xác nhận email. Có thể đặt `Email__Address` và `Email__AppPassword` để bật email xác nhận. Chạy `dotnet publish -c Release -o ./publish`, rồi upload **nội dung bên trong** `publish/` lên thư mục gốc của website. Ứng dụng tự áp dụng migration và thêm 5 phim mẫu khi database còn trống.

Nếu hosting không hỗ trợ biến môi trường, tạo `appsettings.Production.json` từ `appsettings.example.json` trên máy cá nhân, điền cấu hình thật trước khi publish/upload; file này đã được `.gitignore`. Kiểm tra kỹ bản publish trước khi chia sẻ. Không commit chuỗi kết nối có mật khẩu, Gmail App Password, thư mục `publish/`, `bin/`, `obj/` hay dữ liệu thử nghiệm có thông tin cá nhân.

## Kiểm tra

Sau triển khai, mở trang chủ, kiểm tra 5 poster và 3 thể loại; thêm phim vào giỏ, đổi số lượng, checkout với dữ liệu thử nghiệm và xác nhận đơn trong MSSQL. URL public cần được giữ hoạt động đến khi giảng viên công bố điểm; theo dõi điều kiện duy trì hoạt động của nhà cung cấp hosting miễn phí.
