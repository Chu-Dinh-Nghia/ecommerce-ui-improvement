"""Build a factual LMS report from original, unedited screenshots."""
from pathlib import Path
from datetime import date
from PIL import Image
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"
OUTPUT = ROOT / "BaiTap_CaNhan_ASP_CORE_LMS.docx"
PUBLIC = "http://cinenghia409.somee.com/"
GITHUB = "https://github.com/Chu-Dinh-Nghia/ecommerce-ui-improvement/tree/main/ASP-CORE"
omitted, not_applicable, actual = [], [], []

doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.top_margin = section.bottom_margin = Cm(2)
section.left_margin = section.right_margin = Cm(2.4)
styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(10)
styles["Normal"].paragraph_format.space_after = Pt(5)
for name, size in (("Title", 20), ("Heading 1", 14), ("Heading 2", 11.5), ("Caption", 9)):
    styles[name].font.name = "Arial"
    styles[name].font.size = Pt(size)
    styles[name].font.color.rgb = RGBColor(0, 0, 0)
styles["Caption"].font.italic = True


def text(value, style=None):
    return doc.add_paragraph(value, style=style)


def h(value, level=1):
    return doc.add_heading(value, level=level)


def field(code):
    para = doc.add_paragraph()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = code
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instruction, separate, end):
        para.add_run()._r.append(node)
    return para


def grid(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, label in zip(table.rows[0].cells, headers):
        cell.text = label
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for cell, value in zip(cells, row):
            cell.text = str(value)
    for row in table.rows:
        trpr = row._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))
    doc.add_paragraph()


def code(value):
    line = doc.add_paragraph()
    line.paragraph_format.left_indent = Cm(.5)
    for part in value.split("\n"):
        run = line.add_run(part)
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.add_break()


def figure(number, description, filename=None, why=None):
    path = IMAGES / filename if filename else None
    if (not path or not path.exists()) and why != "DIAGRAM":
        (not_applicable if why == "N/A" else omitted).append((number, description))
        return
    if path and path.exists():
        with Image.open(path) as im:
            w, ht = im.size
        width = min(15.0, w / ht * 11.5)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Cm(width))
        actual.append((number, filename, description))
        caption = f"Hình {number}. {description}"
    elif why == "DIAGRAM":
        grid(["Genre", "Movie", "OrderItem", "Order"], [
            ("Id (PK)\nName", "Id (PK)\nGenreId (FK)", "Id (PK)\nMovieId (FK)\nOrderId (FK)", "Id (PK)\nCustomerName\nTotal"),
            ("1 → nhiều Movie", "1 → nhiều OrderItem", "nhiều → 1 Order", "1 → nhiều OrderItem"),
        ])
        caption = f"Hình {number}. {description} Sơ đồ được tổng hợp từ Model của dự án, không phải ảnh chụp SSMS."
    cap = text(caption, "Caption")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER


def figures(items):
    for number, desc, file, status in items:
        figure(number, desc, file, status)


title = text("BÁO CÁO BÀI TẬP CÁ NHÂN ASP NET CORE MVC", "Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
ppr = title._p.get_or_add_pPr()
border = OxmlElement("w:pBdr")
bottom = OxmlElement("w:bottom")
bottom.set(qn("w:val"), "nil")
border.append(bottom)
ppr.append(border)
subtitle = text("Website bán phim CINÉ NGHĨA")
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.runs[0].bold = True
for line in (
    "Sinh viên: Chu Đình Nghĩa",
    "MSSV: 31241026950",
    "Ngày nộp dự kiến: 25/11/2026",
    "GitHub: " + GITHUB,
    "Website public: " + PUBLIC,
):
    text(line)
text("Báo cáo đối chiếu trực tiếp với dự án ASP-CORE/SourceCode. Toàn bộ ảnh minh chứng được chụp thật từ website, GitHub hoặc máy thực hiện và giữ nguyên bản. Các thao tác lịch sử không còn trạng thái để chụp được trình bày bằng kết quả hiện tại và mã nguồn, không dựng lại ảnh.")
doc.add_page_break()
h("Mục lục")
field('TOC \\o "1-2" \\h \\z \\u')
h("Danh mục hình")
field('TOC \\h \\z \\t "Chú thích,1"')
doc.add_page_break()

h("1  Môi trường thực hiện")
text("Em thực hiện dự án trên Windows, dùng .NET SDK 10.0.203, ASP.NET Core MVC và Entity Framework Core 10.0.7. Mã nguồn có thể mở trong VS Code; các lệnh build và publish được chạy qua terminal. Cơ sở dữ liệu phát triển là SQL Server Express, còn website public dùng SQL Server trên Somee.")
text("Trong phiên kiểm tra này, dotnet --version trả 10.0.203. Lệnh dotnet-ef chưa cài trên máy; migration được ứng dụng chạy bằng MigrateAsync khi khởi động. Bản Release đã publish thành công bằng dotnet publish -c Release -o ./publish --no-restore.")
figures([
    ("1.1", "Terminal thật hiển thị dotnet --version và dotnet --list-sdks, có SDK 10.0.203.", "hinh_1_1.png", None),
    ("1.2", "Terminal hiển thị dotnet ef --version.", None, None),
])

h("2  Khởi tạo dự án và cấu hình")
text("Dự án nằm trong ASP-CORE/SourceCode, dùng mẫu MVC và xác thực Individual Accounts. SourceCode.csproj đặt TargetFramework net10.0 và các package Entity Framework Core phiên bản 10.0.7. Bản này giữ Nullable=enable, khai báo dấu ? cho các thuộc tính tùy chọn; vì vậy không thể đưa ảnh Nullable=disable như bản Lab mẫu.")
text("Trong Program.cs em chuyển provider sang UseSqlServer, bật Identity, Session và mặc định vào Movies/Index. Mật khẩu kết nối production không được lưu trong GitHub. Trang local từng chạy tại 127.0.0.1:5168, ảnh còn lại chứng minh giao diện hoạt động nhưng không ghi được dòng terminal Now listening on.")
code('builder.Services.AddDbContext<ApplicationDbContext>(options =>\n    options.UseSqlServer(connectionString));')
figures([
    ("2.1", "Terminal sau lệnh tạo template MVC và restore thành công.", None, None),
    ("2.2", "Kết quả dotnet dev-certs https --trust trên máy thực hiện.", None, None),
    ("2.3", "Trang chủ dự án chạy tại địa chỉ local 127.0.0.1:5168.", "hinh_2_3_local.jpg", None),
    ("2.4", "Program.cs cấu hình UseSqlServer thay cho provider SQLite.", "hinh_2_4.jpg", None),
    ("2.5", "SourceCode.csproj thực tế với Nullable=enable và package EF Core 10.0.7.", "hinh_2_5.jpg", None),
    ("2.6", "Cây thư mục Controllers, Models, Views, Data, Services của dự án trên GitHub.", "hinh_2_6.jpg", None),
])

h("3  Cơ sở dữ liệu Somee và kết nối")
text("Website public dùng database CineNghia409 trên Somee. Connection string production được đặt riêng trong cấu hình trên hosting; bản GitHub chỉ có cấu hình mẫu và cấu hình local không chứa mật khẩu Somee. Program.cs gọi MigrateAsync khi ứng dụng khởi động, nên migration tạo hoặc cập nhật bảng khi kết nối DB hợp lệ.")
text("Em đã chụp trang gói hosting, danh sách database, thông tin kết nối không hiển thị mật khẩu và truy vấn bảng Identity trực tiếp trên Somee. Màn hình lúc đăng ký và tạo DB không còn trạng thái ban đầu; kết quả database và các bảng hiện tại là minh chứng tương ứng.")
figures([
    ("3.1", "Trang Somee Free ASP.NET Hosting hiện tại: gói $0.00/Month và nút Order Now.", "hinh_3_1.png", None),
    ("3.2", "Trang MS SQL Databases hiện tại có database CineNghia409; mục Create database nằm trên menu trái.", "hinh_3_2.png", None),
    ("3.3", "Form tạo database CineNghia409 trước khi xác nhận.", None, None),
    ("3.4", "Connection details trên Somee hiện địa chỉ máy chủ và login; mật khẩu chỉ có nút Copy to clipboard, không xuất hiện trong ảnh.", "hinh_3_4.png", None),
    ("3.5", "Cấu hình DefaultConnection thực tế đã che mật khẩu.", None, None),
    ("3.6", "Data/Migrations cũ của template trước khi thay provider.", None, "N/A"),
    ("3.7", "Terminal chạy migration InitialCreate và database update thành công.", None, None),
    ("3.8", "Trang Register đã điền thông tin không chứa mật khẩu hiển thị.", None, None),
    ("3.9", "Trang xác nhận đăng ký tài khoản.", None, None),
    ("3.10", "SSMS Connect to Server đã che mật khẩu.", None, None),
    ("3.11", "T-SQL console trên Somee truy vấn AspNetUsers, thấy tài khoản quản trị đã xác nhận email.", "hinh_3_11.png", None),
])

h("4  Thiết kế dữ liệu")
text("Em dùng bốn Model nghiệp vụ: Genre, Movie, Order, OrderItem. Genre có nhiều Movie; Order có nhiều OrderItem; mỗi OrderItem tham chiếu Movie và ghi UnitPrice tại lúc đặt. Thông tin giao hàng nằm trực tiếp trong Order, nên không có các class HoaDon, ChiTietHoaDon, ShippingDetail giống tài liệu Lab. Tên Model khác nhưng các quan hệ phục vụ cùng chức năng.")
text("Movie có Title, Summary, ReleaseDate, Price, Rated, GenreId và đường dẫn poster. DataAnnotations kiểm tra tên, giá, đánh giá; controller kiểm tra ngày phát hành không ở quá khứ và GenreId phải tồn tại. ApplicationDbContext kế thừa IdentityDbContext và khai báo bốn DbSet. Migration InitialCreate trong repository thể hiện schema SQL Server.")
code('public DbSet<Movie> Movies => Set<Movie>();\npublic DbSet<Genre> Genres => Set<Genre>();\npublic DbSet<Order> Orders => Set<Order>();\npublic DbSet<OrderItem> OrderItems => Set<OrderItem>();')
grid(["Model", "Khóa và dữ liệu chính", "Quan hệ"], [
    ("Genre", "Id, Name", "1–n Movie"),
    ("Movie", "Id, GenreId, Title, Price, PicturePath", "n–1 Genre; 1–n OrderItem"),
    ("Order", "Id, CustomerName, Address, Email, Mobile, Total", "1–n OrderItem"),
    ("OrderItem", "Id, OrderId, MovieId, Quantity, UnitPrice", "n–1 Order; n–1 Movie"),
])
figures([
    ("4.1", "Cây cấu trúc dự án thực tế; Model dùng Order và OrderItem thay cho tên class Lab mẫu.", "hinh_2_6.jpg", None),
    ("4.2", "ApplicationDbContext.cs chứa bốn DbSet và kế thừa IdentityDbContext.", "hinh_4_2.jpg", None),
    ("4.3", "Migration InitialCreate trong repository; dự án không có các migration Movie, HoaDon, Shipping riêng.", "hinh_4_3.jpg", None),
    ("4.4", "T-SQL console liệt kê 12 bảng thực tế gồm Genres, Movies, Orders, OrderItems và bảng Identity.", "hinh_4_4.png", None),
    ("4.5", "Sơ đồ quan hệ Genre–Movie–OrderItem–Order do sinh viên tổng hợp từ Model.", None, "DIAGRAM"),
    ("4.6", "Mã Movie.cs với các trường và ràng buộc dữ liệu.", "hinh_4_6.jpg", None),
])

h("5  Các chức năng")
h("5.1  Quản lý thể loại", 2)
text("GenresController cho xem danh sách và cho tài khoản AdminOnly thêm, sửa, xóa thể loại. Ứng dụng kiểm tra tên trùng và không cho xóa thể loại đang được phim tham chiếu. Dữ liệu mẫu hiện có ba thể loại: Bí ẩn, Khoa học viễn tưởng, Phiêu lưu.")
figures([
    ("5.1", "Terminal scaffold GenresController theo lệnh Lab mẫu.", None, "N/A"),
    ("5.2", "Trang Genres/Create đã nhập tên thể loại thử nghiệm trước khi lưu; không tạo dữ liệu mới.", "hinh_5_2.png", None),
    ("5.3", "Trang Genres/Index hiển thị ba thể loại thật.", "hinh_5_3.jpg", None),
    ("5.4", "T-SQL console truy vấn Genres, thấy ba dòng dữ liệu Phiêu lưu, Bí ẩn, Khoa học viễn tưởng.", "hinh_5_4.png", None),
])

h("5.2  Quản lý phim", 2)
text("MoviesController có Index, Details, Create, Edit, Delete. Form chọn GenreId qua dropdown, kiểm tra giá và ngày phát hành. Tài khoản thường chỉ xem và mua; tài khoản quản trị mới tạo, sửa, xóa. Phim đã xuất hiện trong đơn hàng không bị xóa để giữ lịch sử mua hàng. Dự án nạp dữ liệu ngay lần đầu nên không có màn hình Index rỗng hay lỗi Invalid object name hiện tại.")
code('[Authorize(Policy = "AdminOnly")]\npublic async Task<IActionResult> Create() { ... }')
figures([
    ("5.5", "Terminal scaffold MoviesController theo lệnh Lab mẫu.", None, "N/A"),
    ("5.6", "Trang báo lỗi Invalid object name Movies trước migration.", None, "N/A"),
    ("5.7", "Movies/Index lúc chưa có dữ liệu.", None, "N/A"),
    ("5.8", "Program.cs có route mặc định controller=Movies, action=Index.", "hinh_5_8.jpg", None),
    ("5.9", "Form Create đã nhập đủ dữ liệu thử nghiệm trước khi lưu; không tạo phim mới.", "hinh_5_9_filled.png", None),
    ("5.10", "Form Create báo lỗi validation khi nhập giá 1.000đ thấp hơn mức tối thiểu 5.000đ.", "hinh_5_10.png", None),
    ("5.11", "Trang Edit của phim Vùng Trời Thứ Chín khi quản trị viên đăng nhập.", "hinh_5_11.png", None),
    ("5.12", "Trang Details của phim Vùng Trời Thứ Chín.", "hinh_5_12.jpg", None),
    ("5.13", "Trang xác nhận Delete của Vùng Trời Thứ Chín; không bấm Xóa phim.", "hinh_5_13.png", None),
    ("5.14", "T-SQL console truy vấn bảng Movies tại thời điểm trước khi thêm phim thứ sáu.", "hinh_5_14.png", None),
])

h("5.3  Upload poster", 2)
text("SaveImageAsync chỉ nhận JPG, JPEG, PNG hoặc WebP, giới hạn 2 MB, dùng Guid đặt tên và ghi vào wwwroot/images/uploads. Khi không tải ảnh lên lúc Create, ứng dụng dùng /images/no-image.svg; lúc Edit không chọn ảnh mới thì giữ đường dẫn cũ. Em đã tạo poster PNG gốc cho phim thứ sáu Chuyến Tàu Cuối Mùa, upload thật trên website public và kiểm tra tệp trong Somee File manager. Lần đầu ảnh chưa hiển thị vì MapStaticAssets chỉ phục vụ ảnh đã có lúc build; em thêm UseStaticFiles() rồi publish và cập nhật DLL, sau đó ảnh hiển thị đúng.")
code('var newPath = await SaveImageAsync(input.PictureUpload);\nif (newPath is not null) movie.PicturePath = newPath;')
figures([
    ("5.15", "Somee File manager thấy tệp PNG vừa upload trong wwwroot/images/uploads, tên do Guid sinh ra.", "hinh_5_15.png", None),
    ("5.16", "Mã SaveImageAsync kiểm tra đuôi, dung lượng và lưu file tên Guid.", "hinh_5_16.jpg", None),
    ("5.17", "Create.cshtml có enctype multipart/form-data; PictureUpload nằm trong form dùng chung.", "hinh_5_17.jpg", None),
    ("5.18", "Form Create đã chọn tệp poster-chuyen-tau-cuoi-mua.png hợp lệ trước khi lưu.", "hinh_5_18.png", None),
    ("5.19", "Index hiển thị cột PicturePath như bản Lab mẫu.", None, "N/A"),
    ("5.20", "Trang Details hiển thị poster PNG đã upload thật sau khi sửa middleware.", "hinh_5_20_upload.png", None),
    ("5.21", "Sau khi lưu Edit không chọn file mới, trang Details vẫn hiển thị poster cũ.", "hinh_5_21.png", None),
])

h("5.4  Danh sách sản phẩm dạng lưới", 2)
text("Movies/Index hiện hiển thị sáu phim thành thẻ gồm poster, thể loại, tên, mô tả ngắn, giá và nút Thêm vào giỏ. Phần đầu trang dùng nhận diện CINÉ NGHĨA và ghi tên sinh viên Chu Đình Nghĩa; footer ghi MSSV và họ tên.")
figures([("5.22", "Trang chủ public dạng lưới với sáu phim, gồm poster vừa upload.", "hinh_5_22_six.png", None)])

h("5.5  Giỏ hàng Session", 2)
text("CartService lưu MovieId và Quantity dạng JSON trong Session. Khi hiển thị, dịch vụ đọc lại Movie từ database rồi tính Subtotal và Total, nên giỏ chưa tạo đơn trong SQL Server. Add tăng số lượng, Update đặt lại số lượng tối đa 99, Remove bỏ phim khỏi giỏ. Bản này dùng CartService thay cho SessionExtensions và action AddToCart trong tài liệu Lab.")
code('public decimal Total => Lines.Sum(x => x.Subtotal);\npublic void Clear() => Session.Remove(Key);')
figures([
    ("5.23", "Program.cs gọi UseSession và khai báo route Movies; phần AddSession ở phía trên file.", "hinh_5_8.jpg", None),
    ("5.24", "SessionExtensions.cs của bản Lab mẫu; dự án hiện dùng Services/CartService.cs.", None, "N/A"),
    ("5.25", "PartialAsync giỏ hàng trong _LoginPartial của bản Lab mẫu.", None, "N/A"),
    ("5.26", "Giỏ hàng thật hiển thị một phim, số lượng, đơn giá và tổng tiền.", "hinh_5_26.jpg", None),
    ("5.27", "Giỏ hàng có hai phim, Vùng Trời Thứ Chín số lượng 2 và tổng 287.000đ.", "hinh_5_27.jpg", None),
    ("5.28", "Giỏ hàng sau Remove còn một phim, tổng giảm về 198.000đ.", "hinh_5_28.jpg", None),
    ("5.29", "Menu có dòng Giỏ hàng của bạn như bản Lab mẫu.", None, "N/A"),
])

h("5.6  Checkout và xác nhận đơn", 2)
text("CheckoutViewModel yêu cầu tên, địa chỉ, email và số điện thoại hợp lệ. CartController từ chối giỏ rỗng; khi hợp lệ tạo Order và OrderItem, ghi Quantity và UnitPrice, gọi SaveChangesAsync, xóa Session rồi chuyển sang Completed. Email chỉ hoạt động khi cấu hình Gmail App Password; phiên này chưa cấu hình và chưa xác minh email được nhận.")
code('db.Orders.Add(order);\nawait db.SaveChangesAsync();\ncart.Clear();\nawait email.SendAsync(order);')
figures([
    ("5.30", "Google App passwords sau khi tạo khóa; chưa cấu hình nên không có ảnh.", None, "N/A"),
    ("5.31", "Email App Password đã che trong cấu hình hosting; hiện chưa cấu hình.", None, "N/A"),
    ("5.32", "Biểu mẫu Checkout đã nhập thông tin thử nghiệm.", "hinh_5_32.jpg", None),
    ("5.33", "Checkout hiển thị lỗi khi nhập email-sai không đúng định dạng.", "hinh_5_33.jpg", None),
    ("5.34", "Trang Completed xác nhận đơn hàng số 2.", "hinh_5_34.jpg", None),
    ("5.35", "T-SQL console truy vấn Orders và OrderItems của đơn số 2, thấy tổng 198.000đ và số lượng 2.", "hinh_5_35.png", None),
    ("5.36", "Email xác nhận đã nhận; chỉ bổ sung nếu gửi thành công.", None, "N/A"),
    ("5.34a", "Mã CartController lưu Order và OrderItem trước khi gửi email.", "hinh_5_34_code.jpg", None),
])

h("5.7  Giao diện và nhận diện cá nhân", 2)
text("Em tùy biến _Layout.cshtml, site.css và các Razor Views với nền tối, điểm nhấn vàng, logo chữ CINÉ NGHĨA và poster riêng. Footer công khai năm, MSSV và họ tên. Ảnh ở khung 390 × 844 pixel cho thấy bố cục thu hẹp trên điện thoại mà vẫn đọc được tiêu đề, điều hướng và thẻ phim.")
figures([
    ("5.37", "Footer website hiển thị © 2026, MSSV 31241026950 và Chu Đình Nghĩa.", "hinh_5_37.jpg", None),
    ("5.38", "Trang chủ sau tùy biến màu, poster và nhận diện CINÉ NGHĨA.", "hinh_5_22.jpg", None),
    ("5.39", "Trang chủ thật ở viewport 390 × 844 pixel.", "hinh_5_39.jpg", None),
])

h("6  Triển khai")
text("Em đã chạy dotnet publish -c Release -o ./publish --no-restore thành công; bản publish có web.config, DLL và wwwroot. Website đặt trên Somee tại cinenghia409.somee.com, kết nối database CineNghia409 bằng cấu hình production chỉ nằm trên hosting. Trang public hiển thị sáu phim và checkout thử nghiệm tạo trang Completed.")
text("Ảnh lúc tạo website, chọn ZIP và giải nén không còn trong phiên hiện tại. Danh sách Websites, File manager với web.config và DLL, cùng website public là bằng chứng trạng thái triển khai hiện nay. Bản sửa upload được cập nhật bằng DLL mới trên Somee mà không ghi đè cấu hình chứa mật khẩu.")
figures([
    ("6.1", "Terminal sau dotnet publish và thư mục publish có web.config.", None, None),
    ("6.2", "Nội dung publish được chọn và file publish.zip có web.config ở gốc.", None, None),
    ("6.3", "Danh sách Websites trên Somee hiện có cinenghia409.somee.com; mục Create website nằm trên menu trái.", "hinh_6_3.png", None),
    ("6.4", "Form tạo website cinenghia409 trên Somee.", None, None),
    ("6.5", "File manager chọn publish.zip và Upload and Unzip archives.", None, None),
    ("6.6", "File manager trên Somee có web.config, wwwroot và các DLL của ứng dụng.", "hinh_6_6.png", None),
    ("6.7", "Website CINÉ NGHĨA chạy trên Somee với URL công khai.", "hinh_6_7.png", None),
])

h("7  Tổ chức mã nguồn trên GitHub")
text("Repository ecommerce-ui-improvement là repository hiện có, không tạo mới. ASP-CORE chứa README, SourceCode và Report; README hướng dẫn công nghệ, chức năng, cấu trúc và cách chạy. appsettings.example.json chứa giá trị mẫu, còn cấu hình production có mật khẩu không được commit. Ảnh GitHub mới đã thể hiện thư mục Report công khai.")
figures([
    ("7.1", "GitHub repository hiện có với thư mục ASP-CORE và README.", "hinh_7_1.jpg", None),
    ("7.2", "Thư mục ASP-CORE trên GitHub công khai có Report, SourceCode và README.", "hinh_7_2_new.png", None),
    ("7.3", "README của ASP-CORE hiển thị trên GitHub.", "hinh_7_3.jpg", None),
    ("7.4", "appsettings.example.json trên GitHub không chứa mật khẩu thật.", "hinh_7_4.jpg", None),
    ("7.5", "Repository truy cập công khai trong trình duyệt chưa đăng nhập GitHub.", "hinh_7_2.jpg", None),
])

h("8  Khó khăn và cách xử lý")
text("Báo cáo này chỉ ghi các vấn đề có dấu vết kiểm chứng được. Trong phiên kiểm tra mới nhất, build và publish đều thành công; không có ảnh lỗi NU1202, Invalid object name, chứng chỉ SQL hay Gmail 535. Các lỗi ví dụ trong đề không được trình bày như lỗi em đã gặp.")
grid(["Vấn đề thực tế", "Nguyên nhân", "Cách xử lý hoặc trạng thái"], [
    ("Không đủ ảnh thao tác lịch sử", "Một số màn hình chỉ xuất hiện khi khởi tạo hoặc khi có lỗi", "Lược bỏ vị trí ảnh không thể chụp lại; dùng minh chứng hiện trạng"),
    ("Chưa xác minh email Gmail", "Chưa có App Password trong cấu hình", "Không ghi đã gửi thành công; giữ chức năng chờ cấu hình"),
    ("Poster upload bị lỗi hiển thị", "MapStaticAssets thiếu ảnh tạo lúc chạy", "Thêm UseStaticFiles, cập nhật DLL; ảnh đã hiện"),
])

h("9  Kết luận và tự đánh giá")
text("Website đã có cấu trúc MVC, SQL Server và migration, quản lý phim/thể loại, upload poster PNG thật, giỏ hàng Session, checkout lưu đơn, giao diện cá nhân hóa, repository GitHub và URL public. Bản Release publish thành công; website public hiển thị sáu phim và trang Completed của đơn số 2. Email Gmail chưa được cấu hình/kiểm chứng. Ảnh thao tác lịch sử không có sẵn nên báo cáo chỉ dùng ảnh trạng thái và kết quả thật.")
text("Giới hạn minh chứng: ảnh lúc tạo template, tạo database, đăng ký tài khoản và upload gói triển khai ban đầu không còn trên máy. Dự án dùng một migration InitialCreate và tên Model Order/OrderItem thay cho tên mẫu trong Lab. Các ảnh hiện trạng, dữ liệu SQL và mã nguồn được dùng để đối chiếu; không tái dựng màn hình lịch sử.")
grid(["Rubric", "Điểm tối đa", "Tự đối chiếu"], [
    ("Khởi tạo và cấu hình", 10, "Có SDK, mã cấu hình và publish; không có ảnh lúc tạo template"),
    ("Cơ sở dữ liệu", 15, "Có Model, migration và bảng SQL thật trên Somee"),
    ("Quản lý sản phẩm/thể loại", 15, "Có CRUD, form, validation và dữ liệu SQL thật"),
    ("Upload hình ảnh", 10, "Có form chọn file, tệp trên hosting và poster hiển thị"),
    ("Giỏ hàng", 15, "Có ảnh Add, Update, Remove và tổng tiền"),
    ("Checkout", 10, "Có form, Completed và bảng Orders/OrderItems"),
    ("Giao diện và triển khai", 10, "Có giao diện desktop/điện thoại và website public"),
    ("GitHub và README", 5, "Có mã nguồn, README và Report công khai"),
    ("Báo cáo và minh chứng", 10, "Ảnh thật; thao tác lịch sử không có ảnh được mô tả đúng thực tế"),
])

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.add_run("Chu Đình Nghĩa · CINÉ NGHĨA")
doc.save(OUTPUT)
inventory = [
    "# Danh sách minh chứng của báo cáo",
    "",
    "Chỉ sử dụng ảnh chụp nguyên bản từ chính dự án và website. Các thao tác lịch sử không có ảnh thật được lược bỏ trong Word.",
    "",
    f"- Vị trí đã chèn ảnh thật: {len(actual)}",
    f"- Vị trí ảnh lịch sử lược bỏ: {len(omitted)}",
    f"- Hình Lab mẫu không áp dụng cho dự án này: {len(not_applicable)}",
    "",
    "## Ảnh thật đã chèn",
    "",
]
inventory += [f"- Hình {number}: `images/{filename}` — {desc}" for number, filename, desc in actual]
inventory += ["", "## Vị trí ảnh lịch sử lược bỏ", ""]
inventory += [f"- Hình {number}: {desc}" for number, desc in omitted]
inventory += ["", "## Hình Lab mẫu không áp dụng", ""]
inventory += [f"- Hình {number}: {desc}" for number, desc in not_applicable]
(ROOT / "ANH_CAN_CHUP.md").write_text("\n".join(inventory) + "\n", encoding="utf-8")
print(f"{OUTPUT.name}: {len(actual)} ảnh thật; 0 khung trống; {len(omitted)} vị trí lịch sử lược bỏ; {len(not_applicable)} hình không áp dụng")
