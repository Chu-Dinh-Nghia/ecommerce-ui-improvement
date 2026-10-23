# Bài tập cá nhân Buổi 2 — HTML5 và CSS3

## 1. Giới thiệu

Dự án tiếp tục phát triển giao diện giỏ hàng trống của **Supersports Vietnam** từ Buổi 1. Khu vực trọng tâm được cải thiện gồm thông báo giỏ hàng trống, thanh điều hướng và danh sách bốn sản phẩm gợi ý. Đây là giao diện tĩnh nhằm thực hành chuyên sâu HTML5 có ngữ nghĩa và CSS3 (Box Model, Flexbox, CSS Grid, Hover/Focus, Responsive); dữ liệu giỏ hàng chưa xử lý bằng JavaScript.

- **Sinh viên thực hiện:** Chu Đình Nghĩa — MSSV: 31241026950
- **Website tham khảo:** https://supersports.com.vn/
- **GitHub Repository:** https://github.com/Chu-Dinh-Nghia/ecommerce-ui-improvement

## 2. Hướng dẫn chạy website

Mở trực tiếp tệp `index.html` bằng trình duyệt hoặc chạy thư mục dự án qua máy chủ cục bộ (như Live Server trên VS Code). 
- Tệp định dạng được liên kết qua `css/style.css`; hình ảnh đặt trong thư mục `images/`.
- Khi mở qua máy chủ cục bộ, có thể mở **Chrome DevTools > Network** để xác nhận `style.css` tải thành công với trạng thái `HTTP 200`, sau đó kiểm tra các quy tắc của `body` và `img` trong tab **Styles / Computed**. Nếu mở trực tiếp qua giao thức `file://`, kiểm tra trực tiếp các kiểu dáng và bố cục đã áp dụng trên trang.

## 3. Rà soát vấn đề Buổi 1 và các thay đổi đã thực hiện

| Vấn đề trước chỉnh sửa | Hướng cải thiện | Kết quả đạt được |
| :--- | :--- | :--- |
| Trang bắt đầu bằng `h2`, thiếu tiêu đề chính `h1` | Đổi tiêu đề thông báo giỏ hàng trống thành `h1` | Thứ bậc tiêu đề `h1` → `h2` → `h3` hợp lý, đúng ngữ nghĩa |
| Logo và bốn nút sản phẩm dùng liên kết giả `href="#"` | Gắn URL trang chủ cho logo và URL trang chi tiết sản phẩm thật trên Supersports cho 4 sản phẩm | Tất cả liên kết đều hoạt động và dẫn tới đúng trang đích |
| Chưa có menu điều hướng để thực hành Flexbox và chỉnh `gap` | Bổ sung thanh điều hướng `<nav>` với 6 danh mục dùng danh sách `<ul>/<li>` theo mẫu tham khảo | Có vùng điều hướng chuẩn ngữ nghĩa, dễ dàng căn chỉnh bằng Flexbox |
| Liên kết chỉ có hiệu ứng rê chuột (`:hover`), thiếu trạng thái bàn phím | Bổ sung `:focus-visible` với đường viền `outline` màu cam rõ nét | Người dùng nhấn phím `Tab` nhận biết rõ vị trí phần tử đang chọn |

## 4. Các kỹ thuật HTML5 và CSS3 đã thực hành

- **Cấu trúc HTML5 ngữ nghĩa:** 
  - `<header>` chứa dải thông báo khuyến mãi The 1 và thanh điều hướng nền xanh đậm.
  - `<nav>` chứa 6 danh mục chính được tổ chức bằng `<ul>` và `<li>` (trên màn hình nhỏ thu gọn vào menu `<details>`).
  - `<main>` bao bọc hai `<section>` (khu vực giỏ hàng trống và khu vực gợi ý sản phẩm `#hot-products`); mỗi sản phẩm nằm trong một thẻ `<article class="product-card">` độc lập.
  - Thứ bậc tiêu đề phân cấp rõ: `h1` cho trạng thái giỏ hàng, `h2` cho tiêu đề mục gợi ý, `h3` cho tên từng đôi giày. Toàn bộ thẻ `<img>` đều có thuộc tính `alt` mô tả chi tiết.
- **Ba loại CSS Selector trong `css/style.css`:** 
  - *Element selector:* `body`, `img` (thiết lập font chữ, màu sắc và giới hạn khung ảnh toàn trang).
  - *Class selector:* `.product-card`, `.product-info`, `.product-btn` (định dạng thẻ và nút sản phẩm).
  - *Descendant selector:* `.product-info h3` (chỉ định dạng tiêu đề `h3` nằm bên trong vùng thông tin sản phẩm).
- **Box Model:** `.product-card` sử dụng `border: 1px solid #eeeeee` và `border-radius: 8px`; `.product-info` dùng `padding: 18px` tạo khoảng đệm bên trong; tiêu đề và vùng giá dùng `margin-bottom` tạo khoảng cách bên ngoài. Quy tắc `* { box-sizing: border-box; }` giúp kích thước khai báo đã tính gộp cả `padding` và `border`, giữ các thẻ nằm gọn trong cột Grid.
- **Flexbox:** 
  - `.header-inner` dùng `display: flex`, `justify-content: space-between`, `align-items: center` và `gap: 20px` để căn chỉnh logo, menu, ô tìm kiếm và nhóm biểu tượng trên cùng một hàng.
  - `.site-nav ul` dùng Flexbox để xếp ngang 6 danh mục điều hướng.
  - `.price` dùng Flexbox kết hợp `flex-wrap: wrap` và `gap: 8px` để căn giá bán cùng giá gốc, tự động xuống dòng khi khung thẻ thu hẹp.
- **CSS Grid & Hình ảnh:** `.product-grid` dùng `display: grid` với `grid-template-columns: repeat(4, minmax(0, 1fr))` và `gap: 24px` (chia 4 cột đều nhau trên máy tính và chuyển thành 2 cột ở màn hình dưới `900px`). Ảnh sản phẩm dùng `object-fit: contain` để giữ trọn vẹn mũi và đế giày trong khung mà không bị cắt góc.
- **Hiệu ứng Hover & Focus:** Các nút và thẻ sản phẩm có `:hover` kết hợp `transition` giúp đổi màu và nổi khối mượt mà khi rê chuột; quy tắc `a:focus-visible` tạo viền `outline: 3px solid #f59e0b` khi điều hướng bằng phím `Tab`.

## 5. Báo cáo kiểm thử và tự sửa lỗi độc lập

| Nội dung kiểm tra | Kết quả | Ghi chú thực tế |
| :--- | :--- | :--- |
| Trang HTML mở được | **Đạt** | Mở tốt trên trình duyệt ở các độ rộng 1898px, 1366px, 768px và 390px |
| CSS được áp dụng | **Đạt** | Máy chủ cục bộ trả `style.css` với HTTP 200; màu sắc và bố cục hiển thị đúng |
| Hình ảnh hiển thị đúng | **Đạt** | Logo và 4 ảnh giày hiển thị sắc nét, đúng tỷ lệ, đầy đủ `alt` |
| Liên kết hoạt động | **Đạt** | Nút "Tiếp tục mua sắm" cuộn tới `#hot-products`; 4 nút sản phẩm mở đúng trang đích trên Supersports |
| Bố cục không bị tràn nghiêm trọng | **Đạt** | Không xuất hiện thanh cuộn ngang ở 1898px, 1366px, 768px và 390px; menu điện thoại hoạt động tốt |
| Hover/focus hoạt động | **Đạt** | Rê chuột chuyển màu mượt; bấm phím `Tab` hiển thị rõ viền `:focus-visible` |
| Đã tự sửa ít nhất một vấn đề | **Đạt** | Tự phát hiện và sửa khoảng cách `gap` menu ở màn hình 1366px, sửa nhãn giảm giá `-50%` và cập nhật URL HOKA bị lỗi 404 |

**Chi tiết vấn đề tự phát hiện và tự sửa độc lập:**
1. **Điều chỉnh khoảng cách menu (`gap`) và nhãn giảm giá:** Khi tự kiểm tra giao diện ở độ rộng `1366px`, tôi nhận thấy khoảng cách giữa 6 mục menu khá sát nhau (`13px`) và nhãn giảm giá của giày HOKA đang ghi `-49%` (trong khi giá bán `1.800.000₫` so với giá gốc `3.599.000₫` làm tròn là `-50%`). Tôi đã trực tiếp mở `css/style.css` chỉnh `gap` của `.site-nav ul` trong `@media (max-width: 1500px)` từ `13px` lên `17px` để thanh menu thoáng hơn mà không chạm vào ô tìm kiếm, đồng thời sửa lại nhãn `-50%` trong `index.html`.
2. **Xử lý liên kết HOKA báo lỗi 404:** Khi bấm kiểm tra thực tế 4 nút "Xem sản phẩm", trang HOKA Mach 6 màu vàng trên Supersports đã ngừng hoạt động (trả về lỗi 404). Tôi đã tìm URL của phiên bản HOKA Mach 6 màu be đang hoạt động (cùng mẫu và mức giá) để thay thế vào `href`, đồng thời đổi nhãn nút thành *"Xem phiên bản màu be"* để đảm bảo tính minh bạch.

## 6. Sử dụng AI có kiểm soát

Quá trình sử dụng ChatGPT để hỗ trợ rà soát mã nguồn, danh sách các prompt tiêu biểu và cách kiểm chứng/điều chỉnh lại đề xuất của AI (như chọn `object-fit: contain` thay vì `cover` cho ảnh giày, kiểm tra liên kết thực tế) được ghi chép chi tiết trong tệp [AI_USAGE.md](AI_USAGE.md).

## 7. Cấu trúc thư mục dự án

```text
E-commerce UI Improvement/
├── index.html
├── README.md
├── AI_USAGE.md
├── css/
│   └── style.css
└── images/
    ├── supersports-logo.png
    ├── nike-pegasus-41.jpg
    ├── hoka-mach-6.jpg
    ├── asics-gel-nimbus.jpg
    └── puma-deviate-nitro-3.jpg
