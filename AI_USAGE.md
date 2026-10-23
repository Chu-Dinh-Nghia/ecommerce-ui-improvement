# Nhật ký sử dụng AI trong bài tập cá nhân Buổi 2

## 1. Công cụ AI

- **Công cụ sử dụng:** ChatGPT.
- **Phạm vi hỗ trợ:** Rà soát yêu cầu HTML5 và CSS3, giải thích mã nguồn, đề xuất cách áp dụng Box Model / Flexbox / CSS Grid và hỗ trợ kiểm tra lỗi hiển thị. Bài tập Buổi 2 được phát triển tiếp nối trực tiếp trên repository đã xây dựng ở Buổi 1.

## 2. Mục đích sử dụng

Tôi sử dụng AI có kiểm soát để:

- Đối chiếu giao diện giỏ hàng trống hiện có với 8 bước yêu cầu trong đề bài Buổi 2.
- Rà soát các thẻ HTML5 ngữ nghĩa (`header`, `nav`, `main`, `section`, `article`), thứ bậc tiêu đề (`h1`, `h2`, `h3`) và thuộc tính `alt` cho hình ảnh.
- Xác định rõ ví dụ trong mã nguồn cho 3 loại bộ chọn: element selector, class selector và descendant selector.
- Áp dụng đúng Box Model, Flexbox (cho header/menu và vùng giá) và CSS Grid (cho danh sách 4 sản phẩm gợi ý).
- Bổ sung hiệu ứng `:hover`, `transition` và trạng thái `:focus-visible` hỗ trợ điều hướng bằng bàn phím (phím `Tab`).
- Kiểm tra đường dẫn tệp CSS, hình ảnh, liên kết sản phẩm và bố cục responsive ở các kích thước màn hình (`1366px`, `768px`, `390px`).

## 3. Prompt tiêu biểu đã sử dụng ở Buổi 2

### Prompt 1 – Rà soát cấu trúc HTML5 và định hướng cải thiện

> Tôi đang tiếp tục bài tập cá nhân Buổi 2 môn Phát triển ứng dụng WEB/TMĐT từ giao diện giỏ hàng trống ở Buổi 1.
> Đây là mã HTML và CSS hiện tại: `[Dán mã HTML và CSS]`
> Hãy đối chiếu từng yêu cầu của bài tập Buổi 2 và chỉ ra phần đã đạt, phần cần chỉnh sửa về: thẻ HTML5 ngữ nghĩa, thứ bậc tiêu đề `h1`-`h3`, thuộc tính `alt`, liên kết điều hướng và bố cục.
> Yêu cầu: Giữ nguyên phạm vi trang giỏ hàng và cấu trúc thư mục của Buổi 1, không viết lại toàn bộ website mới, giải thích rõ lý do từng thay đổi.

### Prompt 2 – Thực hành CSS Selector, Box Model, Flexbox và Grid

> Dựa trên mã HTML khu vực header, thẻ sản phẩm `.product-card` và danh sách `.product-grid` hiện tại: `[Dán đoạn mã HTML liên quan]`
> Hãy hướng dẫn tôi viết CSS trong tệp `css/style.css` để:
> 1. Sử dụng rõ element selector, class selector và descendant selector.
> 2. Áp dụng Box Model (`margin`, `padding`, `border`, `border-radius`, `box-sizing: border-box`) cho thẻ sản phẩm.
> 3. Dùng Flexbox (`display: flex`, `justify-content`, `align-items`, `gap`) để căn chỉnh header, menu điều hướng và vùng giá sản phẩm.
> 4. Dùng CSS Grid (`display: grid`, `grid-template-columns`, `gap`) chia 4 cột trên máy tính và 2 cột trên màn hình nhỏ.
> Yêu cầu: Chỉ dùng CSS3 thuần, không sử dụng Bootstrap hoặc Tailwind CSS, giải thích rõ tác dụng của từng thuộc tính để tôi trình bày báo cáo.

### Prompt 3 – Bổ sung Hover, Focus và kiểm tra lỗi giao diện

> Đây là mã CSS của các liên kết và nút thao tác trong trang: `[Dán mã CSS]`
> Hãy hướng dẫn tôi bổ sung hiệu ứng `:hover` kèm `transition` mượt mà và trạng thái `:focus-visible` (dùng `outline` và `outline-offset`) để nhận diện rõ khi nhấn phím `Tab`. Đồng thời hướng dẫn cách kiểm tra giao diện ở các độ rộng `1366px`, `768px` và `390px` bằng Chrome DevTools để đảm bảo bố cục không bị tràn ngang.

## 4. Kết quả AI hỗ trợ

- **Về HTML5 (`index.html`):** Chuẩn hóa phần đầu trang với `<header>`, thanh điều hướng `<nav class="site-nav">` chứa danh sách `<ul>/<li>`. Phần nội dung chính `<main>` chia thành hai `<section>` (thông báo giỏ hàng trống và danh sách sản phẩm gợi ý `#hot-products`), mỗi sản phẩm được bọc trong một thẻ `<article class="product-card">`. Thứ bậc tiêu đề được sắp xếp đúng chuẩn `h1` -> `h2` -> `h3` và mọi thẻ `<img>` đều có `alt` mô tả chi tiết.
- **Về CSS3 (`css/style.css`):**
  - Phân tách rõ 3 loại selector: `body` (element selector), `.product-card` (class selector) và `.product-info h3` (descendant selector).
  - Áp dụng `box-sizing: border-box` giúp tổng chiều rộng của thẻ đã tính cả `padding` và `border`, không làm tràn cột khi chia lưới.
  - Áp dụng Flexbox trên `.header-inner`, `.site-nav ul` và vùng giá `.price` để căn chỉnh các phần tử theo hàng ngang và tự động xuống dòng (`flex-wrap: wrap`) khi khung hẹp.
  - Áp dụng CSS Grid trên `.product-grid` với `repeat(4, minmax(0, 1fr))` ở màn hình lớn và giảm xuống 2 cột ở màn hình dưới `900px`.

## 5. Kiểm tra thực tế và tự điều chỉnh đề xuất của AI

Sau khi nhận mã gợi ý từ AI, tôi không sao chép nguyên bản mà trực tiếp chạy thử trên trình duyệt và thực hiện các điều chỉnh sau:

1. **Điều chỉnh `object-fit: cover` thành `object-fit: contain` cho ảnh sản phẩm:**
   - *Đề xuất ban đầu:* Tài liệu mẫu và gợi ý CSS ban đầu thường dùng `object-fit: cover` cho ảnh trong lưới.
   - *Kiểm tra và điều chỉnh:* Khi quan sát trên trình duyệt với ảnh giày thể thao nằm ngang, `cover` có nguy cơ cắt mất phần mũi hoặc gót giày. Tôi đã chọn giữ `object-fit: contain` kết hợp `padding: 12px` để hiển thị trọn vẹn đôi giày trong khung mà không bị biến dạng.
2. **Kiểm tra và thay thế các liên kết `href="#"` / lỗi 404:**
   - *Đề xuất ban đầu:* Mã mẫu ban đầu sử dụng liên kết giả `href="#"` cho logo và các nút "Xem sản phẩm", sau đó một URL sản phẩm HOKA màu vàng bị trả về lỗi 404 trên website gốc.
   - *Kiểm tra và điều chỉnh:* Tôi đã bấm kiểm tra từng liên kết trên trình duyệt, gắn URL thật dẫn tới các trang sản phẩm Nike, ASICS, Puma trên Supersports. Riêng mẫu HOKA Mach 6 màu vàng đã hết trang, tôi đổi sang URL phiên bản màu be đang hoạt động (cùng mẫu và mức giá) đồng thời sửa nhãn nút thành *"Xem phiên bản màu be"* để thông tin minh bạch.
3. **Tự phát hiện và sửa mã độc lập (Bước 8):**
   - Trong quá trình tự rà soát giao diện ở độ phân giải `1366px`, tôi tự phát hiện nhãn giảm giá của giày HOKA đang ghi `-49%` (trong khi giá `1.800.000₫` so với `3.599.000₫` làm tròn là `-50%`) và khoảng cách giữa các mục menu còn hơi hẹp.
   - Tôi đã trực tiếp mở `index.html` sửa nhãn thành `-50%` và mở `css/style.css` điều chỉnh thuộc tính `gap` của `.site-nav ul` trong `@media (max-width: 1500px)` để các liên kết menu thoáng và cân đối hơn.

## 6. Nội dung kỹ thuật tôi nắm vững và có thể giải thích trực tiếp

- **HTML5 ngữ nghĩa:** `<header>` chứa phần đầu trang; `<nav>` xác định vùng điều hướng chính; `<ul>` và `<li>` nhóm danh sách liên kết menu; `<section>` phân chia khu vực nội dung; `<article>` đại diện cho một thẻ sản phẩm độc lập (khác với `<div>` chỉ dùng để gom nhóm trình bày).
- **Box Model:** `padding` tạo khoảng đệm bên trong giữa nội dung và viền (`.product-info { padding: 18px; }`); `border` tạo đường viền bao quanh thẻ; `margin` tạo khoảng cách bên ngoài đẩy các phần tử khác ra xa (`.product-info h3 { margin-bottom: 15px; }`).
- **Flexbox và CSS Grid:** Flexbox điều khiển bố cục 1 chiều (dùng cho `.header-inner`, `.site-nav ul`, `.price`), còn CSS Grid điều khiển bố cục 2 chiều gồm hàng và cột (dùng cho `.product-grid`). Nếu xóa `display: grid`, các thẻ `<article>` sẽ trở về luồng khối mặc định và xếp chồng dọc từ trên xuống dưới.
- **Tương tác & Kiểm thử:** `:hover` kích hoạt khi rê chuột lên phần tử; `:focus-visible` hiển thị viền `outline` khi điều hướng bằng phím `Tab`. Sử dụng Chrome DevTools (tab *Network*, *Styles*, *Computed* và chế độ *Device Toolbar*) để xác nhận tệp `style.css` tải thành công (HTTP 200) và kiểm tra giao diện không bị tràn ngang ở `1366px`, `768px`, `390px`.
