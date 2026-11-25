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
missing, not_applicable, actual = [], [], []

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
    elif why == "N/A":
        p = doc.add_paragraph(f"Hình {number}: Không áp dụng cho cách triển khai hiện tại; không có ảnh để chụp đúng nội dung Lab mẫu.")
        p.runs[0].italic = True
        not_applicable.append((number, description))
        caption = f"Hình {number}. {description} — không áp dụng cho dự án hiện tại."
    else:
        box = doc.add_table(rows=1, cols=1)
        box.style = "Table Grid"
        box.cell(0, 0).text = f"[CẦN CHỤP: {description}]"
        for run in box.cell(0, 0).paragraphs[0].runs:
            run.bold = True
            run.font.color.rgb = RGBColor(150, 36, 36)
        missing.append((number, description))
        caption = f"Hình {number}. Vị trí cần bổ sung ảnh chụp thật: {description}"
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
    "Lớp học phần: Phát triển ứng dụng TMĐT – 26C1INF50902702 – S5 (theo tiêu đề LMS đã quan sát)",
    "Ngày nộp dự kiến: 25/11/2026",
    "GitHub: " + GITHUB,
    "Website public: " + PUBLIC,
):
    text(line)
text("Báo cáo đối chiếu trực tiếp với dự án ASP-CORE/SourceCode. Ảnh đã chèn được chụp từ website, GitHub hoặc máy thực tế và giữ nguyên bản. Những màn hình không còn truy cập được có khung [CẦN CHỤP]; các bước thuộc mã Lab mẫu nhưng không tồn tại trong bản làm này được ghi không áp dụng.")
doc.add_page_break()
h("Mục lục")
field('TOC \\o "1-2" \\h \\z \\u')
h("Danh mục hình")
field('TOC \\h \\z \\t "Chú thích,1"')
doc.add_page_break()

h("1  Môi trường thực hiện")
text("Em thực hiện dự án trên Windows, dùng .NET SDK 10.0.203, ASP.NET Core MVC và Entity Framework Core 10.0.7. Mã nguồn có thể mở trong VS Code; các lệnh build và publish được chạy qua terminal. Cơ sở dữ liệu phát triển là SQL Server Express, còn website public dùng SQL Server trên Somee.")
text("Trong phiên kiểm tra này, dotnet --version trả 10.0.203; dotnet build -c Release chạy thành công với 0 cảnh báo và 0 lỗi. Chưa có ảnh chụp terminal chứa hai lệnh SDK và dotnet-ef, nên em để đúng khung chờ ảnh thay vì dựng ảnh lệnh.")
figures([
    ("1.1", "Terminal hiển thị dotnet --version và dotnet --list-sdks, có SDK 10.0.xxx.", None, None),
    ("1.2", "Terminal hiển thị dotnet ef --version.", None, None),
])

h("2  Khởi tạo dự án và cấu hình")
text("Dự án nằm trong ASP-CORE/SourceCode, dùng mẫu MVC và xác thực Individual Accounts. SourceCode.csproj đặt TargetFramework net10.0 và các package Entity Framework Core phiên bản 10.0.7. Bản này giữ Nullable=enable, khai báo dấu ? cho các thuộc tính tùy chọn; vì vậy không thể đưa ảnh Nullable=disable như bản Lab mẫu.")
text("Trong Program.cs em chuyển provider sang UseSqlServer, bật Identity, Session và mặc định vào Movies/Index. Mật khẩu kết nối production không được lưu trong GitHub. Trang local từng chạy tại 127.0.0.1:5168, ảnh còn lại chứng minh giao diện hoạt động nhưng không ghi được dòng terminal Now listening on.")
code('builder.Services.AddDbContext<ApplicationDbContext>(options =>\n    options.UseSqlServer(connectionString));')
figures([
    ("2.1", "Terminal sau lệnh tạo template MVC và restore thành công.", None, None),
    ("2.2", "Kết quả dotnet dev-certs https --trust trên máy thực hiện.", None, None),
    ("2.3", "Trang chủ dự án chạy local; cần thêm ảnh terminal Now listening on để đủ yêu cầu Lab.", "hinh_2_3_local.jpg", None),
    ("2.4", "Program.cs cấu hình UseSqlServer thay cho provider SQLite.", "hinh_2_4.jpg", None),
    ("2.5", "SourceCode.csproj thực tế với Nullable=enable và package EF Core 10.0.7.", "hinh_2_5.jpg", None),
    ("2.6", "Cây thư mục Controllers, Models, Views, Data, Services của dự án trên GitHub.", "hinh_2_6.jpg", None),
])

h("3  Cơ sở dữ liệu Somee và kết nối")
text("Website public dùng database CineNghia409 trên Somee. Connection string production được đặt riêng trong cấu hình trên hosting; bản GitHub chỉ có cấu hình mẫu và cấu hình local không chứa mật khẩu Somee. Program.cs gọi MigrateAsync khi ứng dụng khởi động, nên migration tạo hoặc cập nhật bảng khi kết nối DB hợp lệ.")
text("Em đã chụp trang gói hosting miễn phí hiện tại của Somee. Ảnh thông tin kết nối chưa có và có thể lộ pwd. Các bước đăng ký, tạo DB, đăng ký tài khoản và lỗi trước khi migration không thể quay lại đúng trạng thái ban đầu; những mục đó được đánh dấu rõ để tránh trình bày như bằng chứng đã có.")
figures([
    ("3.1", "Trang Somee Free ASP.NET Hosting hiện tại: gói $0.00/Month và nút Order Now.", "hinh_3_1.png", None),
    ("3.2", "Trang MS SQL Databases trên Somee và nút CREATE.", None, None),
    ("3.3", "Form tạo database CineNghia409 trước khi xác nhận.", None, None),
    ("3.4", "Connection details của Somee, đã che mật khẩu và phần pwd trong chuỗi kết nối.", None, None),
    ("3.5", "Cấu hình DefaultConnection thực tế đã che mật khẩu.", None, None),
    ("3.6", "Data/Migrations cũ của template trước khi thay provider.", None, "N/A"),
    ("3.7", "Terminal chạy migration InitialCreate và database update thành công.", None, None),
    ("3.8", "Trang Register đã điền thông tin không chứa mật khẩu hiển thị.", None, None),
    ("3.9", "Trang xác nhận đăng ký tài khoản.", None, None),
    ("3.10", "SSMS Connect to Server đã che mật khẩu.", None, None),
    ("3.11", "Bảng Identity và dữ liệu AspNetUsers trong SQL Server.", None, None),
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
    ("4.4", "Danh sách bảng Genres, Movies, Orders và OrderItems trên SQL Server.", None, None),
    ("4.5", "Sơ đồ quan hệ Genre–Movie–OrderItem–Order do sinh viên tổng hợp từ Model.", None, "DIAGRAM"),
    ("4.6", "Mã Movie.cs với các trường và ràng buộc dữ liệu.", "hinh_4_6.jpg", None),
])

h("5  Các chức năng")
h("5.1  Quản lý thể loại", 2)
text("GenresController cho xem danh sách và cho tài khoản AdminOnly thêm, sửa, xóa thể loại. Ứng dụng kiểm tra tên trùng và không cho xóa thể loại đang được phim tham chiếu. Dữ liệu mẫu hiện có ba thể loại: Bí ẩn, Khoa học viễn tưởng, Phiêu lưu.")
figures([
    ("5.1", "Terminal scaffold GenresController theo lệnh Lab mẫu.", None, "N/A"),
    ("5.2", "Trang Genres/Create khi nhập một thể loại mới.", None, None),
    ("5.3", "Trang Genres/Index hiển thị ba thể loại thật.", "hinh_5_3.jpg", None),
    ("5.4", "Bảng Genres trong SQL Server với ba dòng dữ liệu.", None, None),
])

h("5.2  Quản lý phim", 2)
text("MoviesController có Index, Details, Create, Edit, Delete. Form chọn GenreId qua dropdown, kiểm tra giá và ngày phát hành. Tài khoản thường chỉ xem và mua; tài khoản quản trị mới tạo, sửa, xóa. Phim đã xuất hiện trong đơn hàng không bị xóa để giữ lịch sử mua hàng. Dự án nạp dữ liệu ngay lần đầu nên không có màn hình Index rỗng hay lỗi Invalid object name hiện tại.")
code('[Authorize(Policy = "AdminOnly")]\npublic async Task<IActionResult> Create() { ... }')
figures([
    ("5.5", "Terminal scaffold MoviesController theo lệnh Lab mẫu.", None, "N/A"),
    ("5.6", "Trang báo lỗi Invalid object name Movies trước migration.", None, "N/A"),
    ("5.7", "Movies/Index lúc chưa có dữ liệu.", None, "N/A"),
    ("5.8", "Program.cs có route mặc định controller=Movies, action=Index.", "hinh_5_8.jpg", None),
    ("5.9", "Form tạo phim thật; ảnh hiện tại chưa có dữ liệu đã nhập đầy đủ.", "hinh_5_9.jpg", None),
    ("5.10", "Form báo lỗi validation khi giá hoặc ngày phát hành không hợp lệ.", None, None),
    ("5.11", "Trang Edit của một phim sau khi quản trị viên đăng nhập.", None, None),
    ("5.12", "Trang Details của phim Vùng Trời Thứ Chín.", "hinh_5_12.jpg", None),
    ("5.13", "Trang xác nhận Delete; không xóa phim đã có đơn hàng.", None, None),
    ("5.14", "Bảng Movies trên SQL Server có ít nhất năm phim.", None, None),
])

h("5.3  Upload poster", 2)
text("SaveImageAsync chỉ nhận JPG, JPEG, PNG hoặc WebP, giới hạn 2 MB, dùng Guid đặt tên và ghi vào wwwroot/images/uploads. Khi không tải ảnh lên lúc Create, ứng dụng dùng /images/no-image.svg; lúc Edit không chọn ảnh mới thì giữ đường dẫn cũ. Mẫu hiện tại dùng poster SVG tự tạo cho năm phim, vì vậy chưa có ảnh chứng minh một lần upload file thật.")
code('var newPath = await SaveImageAsync(input.PictureUpload);\nif (newPath is not null) movie.PicturePath = newPath;')
figures([
    ("5.15", "Explorer thấy thư mục wwwroot/images/uploads sau một lần upload thật.", None, None),
    ("5.16", "Mã SaveImageAsync kiểm tra đuôi, dung lượng và lưu file tên Guid.", "hinh_5_16.jpg", None),
    ("5.17", "Create.cshtml có enctype multipart/form-data; PictureUpload nằm trong form dùng chung.", "hinh_5_17.jpg", None),
    ("5.18", "Form Create hoặc Edit đã chọn file poster hợp lệ.", None, None),
    ("5.19", "Index hiển thị cột PicturePath như bản Lab mẫu.", None, "N/A"),
    ("5.20", "Index dạng thẻ hiển thị poster của năm phim.", "hinh_5_22.jpg", None),
    ("5.21", "Edit không chọn ảnh mới và poster vẫn giữ nguyên sau lưu.", None, None),
])

h("5.4  Danh sách sản phẩm dạng lưới", 2)
text("Movies/Index hiển thị năm phim thành thẻ gồm poster, thể loại, tên, mô tả ngắn, giá và nút Thêm vào giỏ. Phần đầu trang dùng nhận diện CINÉ NGHĨA và ghi tên sinh viên Chu Đình Nghĩa; footer ghi MSSV và họ tên.")
figures([("5.22", "Trang chủ dạng lưới với poster, thông tin phim và nút Thêm vào giỏ.", "hinh_5_22.jpg", None)])

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
    ("5.35", "Dữ liệu Orders và OrderItems của đơn số 2 trong SQL Server.", None, None),
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
text("Em đã chạy dotnet publish -c Release -o ./publish thành công; bản publish có web.config, DLL và wwwroot. Website đặt trên Somee tại cinenghia409.somee.com, kết nối database CineNghia409 bằng cấu hình production chỉ nằm trên hosting. Trang public hiển thị đủ năm phim và checkout thử nghiệm tạo trang Completed.")
text("Ảnh lúc tạo website, chọn ZIP và giải nén không còn trong phiên hiện tại. Em giữ các khung cần chụp thay vì mô phỏng thao tác cũ. Ảnh website đang chạy trên hosting có thanh địa chỉ là bằng chứng triển khai đã thành công.")
figures([
    ("6.1", "Terminal sau dotnet publish và thư mục publish có web.config.", None, None),
    ("6.2", "Nội dung publish được chọn và file publish.zip có web.config ở gốc.", None, None),
    ("6.3", "Danh sách Websites trên Somee với nút CREATE.", None, None),
    ("6.4", "Form tạo website cinenghia409 trên Somee.", None, None),
    ("6.5", "File manager chọn publish.zip và Upload and Unzip archives.", None, None),
    ("6.6", "File manager sau giải nén có web.config, wwwroot và DLL.", None, None),
    ("6.7", "Website CINÉ NGHĨA chạy trên Somee với URL công khai.", "hinh_6_7.png", None),
])

h("7  Tổ chức mã nguồn trên GitHub")
text("Repository ecommerce-ui-improvement là repository hiện có, không tạo mới. ASP-CORE chứa README và SourceCode; README hướng dẫn công nghệ, chức năng, cấu trúc và cách chạy. appsettings.example.json chứa giá trị mẫu, còn cấu hình production có mật khẩu không được commit. Report đã có trên máy nhưng chưa xuất hiện trong ảnh GitHub hiện tại.")
figures([
    ("7.1", "GitHub repository hiện có với thư mục ASP-CORE và README.", "hinh_7_1.jpg", None),
    ("7.2", "Thư mục ASP-CORE trên GitHub; ảnh hiện tại chưa có Report.", "hinh_7_2.jpg", None),
    ("7.3", "README của ASP-CORE hiển thị trên GitHub.", "hinh_7_3.jpg", None),
    ("7.4", "appsettings.example.json trên GitHub không chứa mật khẩu thật.", "hinh_7_4.jpg", None),
    ("7.5", "Repository truy cập công khai trong trình duyệt chưa đăng nhập GitHub.", "hinh_7_2.jpg", None),
])

h("8  Khó khăn và cách xử lý")
text("Báo cáo này chỉ ghi các vấn đề có dấu vết kiểm chứng được. Trong phiên kiểm tra mới nhất, build và publish đều thành công; không có ảnh lỗi NU1202, Invalid object name, chứng chỉ SQL hay Gmail 535. Các lỗi ví dụ trong đề không được trình bày như lỗi em đã gặp.")
grid(["Vấn đề thực tế", "Nguyên nhân", "Cách xử lý hoặc trạng thái"], [
    ("Không đủ ảnh thao tác lịch sử", "Một số màn hình chỉ xuất hiện khi khởi tạo hoặc khi có lỗi", "Đánh dấu khung cần chụp; không dựng ảnh giả"),
    ("Chưa xác minh email Gmail", "Chưa có App Password trong cấu hình", "Không ghi đã gửi thành công; giữ chức năng chờ cấu hình"),
    ("Somee console cần đăng nhập lại", "Phiên quản trị đã hết hạn", "Để khung ảnh bảng SQL và chụp khi đăng nhập lại"),
])

h("9  Kết luận và tự đánh giá")
text("Website đã có cấu trúc MVC, SQL Server và migration, quản lý phim/thể loại, giỏ hàng Session, checkout lưu đơn, giao diện cá nhân hóa, repository GitHub và URL public. Bản Release build và publish thành công trong phiên kiểm tra; website public hiển thị năm phim và trang Completed của đơn số 2. Email Gmail chưa được cấu hình/kiểm chứng và các khung ảnh ở cuối cần bổ sung trước khi khẳng định hồ sơ minh chứng hoàn chỉnh.")
grid(["Rubric", "Điểm tối đa", "Tự đối chiếu"], [
    ("Khởi tạo và cấu hình", 10, "Build đạt; thiếu ảnh terminal ban đầu"),
    ("Cơ sở dữ liệu", 15, "Có Model/Migration; thiếu ảnh bảng SQL"),
    ("Quản lý sản phẩm/thể loại", 15, "Có mã CRUD và giao diện; thiếu ảnh vài thao tác"),
    ("Upload hình ảnh", 10, "Có mã xử lý; chưa có ảnh thao tác upload thật"),
    ("Giỏ hàng", 15, "Có Add/Update/Remove và tổng; thiếu ảnh thử nhiều phim"),
    ("Checkout", 10, "Có form và Completed; thiếu ảnh bảng đơn"),
    ("Giao diện và triển khai", 10, "Có giao diện desktop/điện thoại và website public"),
    ("GitHub và README", 5, "Có mã nguồn và README; Report chưa lên GitHub"),
    ("Báo cáo và minh chứng", 10, "Có ảnh thật và khung thiếu minh bạch; chưa đủ ảnh"),
])

h("Phụ lục A  Đối chiếu ảnh bắt buộc")
grid(["Minh chứng chính theo đề", "Hình trong báo cáo", "Trạng thái"], [
    ("Cấu trúc dự án", "2.6, 4.1", "Có ảnh GitHub; thiếu ảnh VS Code"),
    ("Website local", "2.3", "Có ảnh trang local; thiếu terminal"),
    ("Danh sách và form phim", "5.9, 5.22", "Có ảnh; form chưa điền đầy đủ"),
    ("Upload và hiển thị ảnh", "5.16–5.21", "Có mã và poster; thiếu ảnh upload thật"),
    ("Thể loại và database", "5.3, 5.4", "Có trang web; thiếu bảng SQL"),
    ("Giỏ hàng", "5.26–5.28", "Có một phim; thiếu thử nhiều phim/Remove"),
    ("Checkout và xác nhận", "5.32–5.35", "Có form và Completed; thiếu bảng SQL"),
    ("Hosting và URL", "6.7", "Có ảnh thật"),
    ("GitHub và README", "7.1–7.4", "Có ảnh thật; chưa có Report trên GitHub"),
])

h("Phụ lục B  Các khung ảnh còn cần bổ sung")
for number, desc in missing:
    text(f"Hình {number}: {desc}")
h("Phụ lục C  Các hình Lab mẫu không áp dụng")
for number, desc in not_applicable:
    text(f"Hình {number}: {desc}")
text("Không áp dụng nghĩa là dự án dùng cách triển khai khác; không nên chụp ảnh của project khác để lấp chỗ này. Chỉ dùng ảnh từ chính project hoặc website này. Không công khai mật khẩu SQL, Gmail App Password hay chuỗi kết nối có pwd.")

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.add_run("Chu Đình Nghĩa · CINÉ NGHĨA")
doc.save(OUTPUT)
inventory = [
    "# Danh sách minh chứng của báo cáo",
    "",
    "Chỉ sử dụng ảnh chụp nguyên bản từ chính dự án và website. Những hình không có ảnh được giữ dưới dạng khung `[CẦN CHỤP]` trong Word.",
    "",
    f"- Vị trí đã chèn ảnh thật: {len(actual)}",
    f"- Khung cần chụp: {len(missing)}",
    f"- Hình Lab mẫu không áp dụng cho dự án này: {len(not_applicable)}",
    "",
    "## Ảnh thật đã chèn",
    "",
]
inventory += [f"- Hình {number}: `images/{filename}` — {desc}" for number, filename, desc in actual]
inventory += ["", "## Khung cần chụp bổ sung", ""]
inventory += [f"- Hình {number}: {desc}" for number, desc in missing]
inventory += ["", "## Hình Lab mẫu không áp dụng", ""]
inventory += [f"- Hình {number}: {desc}" for number, desc in not_applicable]
(ROOT / "ANH_CAN_CHUP.md").write_text("\n".join(inventory) + "\n", encoding="utf-8")
print(f"{OUTPUT.name}: {len(actual)} ảnh thật; {len(missing)} khung cần chụp; {len(not_applicable)} hình không áp dụng")
