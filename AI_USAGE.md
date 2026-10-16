
## 1. Công cụ AI

Tên công cụ: ChatGPT

## 2. Mục đích sử dụng

AI được sử dụng để hỗ trợ:

- Phân tích website Supersports.
- Đề xuất cải tiến khu vực giỏ hàng.
- Xây dựng bố cục giao diện.
- Hỗ trợ viết HTML5 và CSS3.
- Hướng dẫn tổ chức thư mục dự án.
- Hỗ trợ sửa lỗi đường dẫn hình ảnh và CSS.
- Hướng dẫn làm giao diện responsive.

## 3. Prompt đã sử dụng

### Prompt phân tích

Tôi đang khảo sát website Supersports Vietnam.

Hãy phân tích các khu vực:
- Trang chủ
- Danh mục sản phẩm
- Chi tiết sản phẩm
- Tìm kiếm
- Giỏ hàng

Với mỗi khu vực, hãy nêu:
- Mục đích của chức năng
- Thành phần giao diện
- Điểm thuận tiện
- Vấn đề có thể phát sinh
- Đề xuất cải tiến

Không khẳng định các tính năng chưa được kiểm chứng.

### Prompt cải tiến giao diện

Tôi đang thực hiện bài tập phát triển giao diện website thương mại điện tử bằng HTML5 và CSS3.

Tôi muốn cải tiến khu vực giỏ hàng trống của Supersports Vietnam.

Yêu cầu:
- Có thông báo giỏ hàng trống.
- Có nút “Tiếp tục mua sắm”.
- Có phần gợi ý sản phẩm phía dưới.
- Có tối thiểu 4 sản phẩm.
- Mỗi sản phẩm có hình ảnh, tên, giá và nút thao tác.
- Giao diện phù hợp với máy tính và điện thoại.
- CSS tách thành file riêng.

## 4. Kết quả AI đề xuất

AI ban đầu đề xuất:

- Phần trên hiển thị trạng thái giỏ hàng trống.
- Nút “Tiếp tục mua sắm” làm nổi bật.
- Phần dưới hiển thị nội dung gợi ý.
- Dùng CSS Grid để sắp xếp các thẻ.
- Desktop hiển thị nhiều thẻ trên một hàng.
- Mobile giảm số lượng thẻ trên mỗi hàng.

Trong quá trình thực hiện, tôi đã điều chỉnh ý tưởng từ danh mục gợi ý sang 4 sản phẩm hot thực tế để giao diện trực quan hơn.

## 5. Kiểm tra và điều chỉnh

Tôi đã thực hiện các điều chỉnh sau:

- Kiểm tra lại thông tin với website Supersports.
- Tải 4 hình ảnh sản phẩm thực tế.
- Đổi tên file hình ảnh.
- Sửa lỗi khi chuyển `index.html` sang thư mục mới.
- Di chuyển thư mục CSS và images vào đúng project.
- Sửa lại đường dẫn tương đối.
- Thay logo chữ bằng logo hình ảnh.
- Kiểm tra giao diện bằng Live Preview.
- Điều chỉnh kích thước ảnh và bố cục trên màn hình nhỏ.

## 6. Phần tôi hiểu và có thể giải thích

### HTML

- `<header>`: chứa phần đầu trang.
- `<main>`: chứa nội dung chính.
- `<section>`: chia các khu vực nội dung.
- `<article>`: đại diện cho từng sản phẩm.
- `<img>`: hiển thị hình ảnh.
- `<a>`: dùng làm nút điều hướng.

### CSS

- `display: grid`: tạo bố cục sản phẩm.
- `grid-template-columns`: xác định số cột.
- `object-fit: contain`: giúp hình ảnh không bị méo.
- `:hover`: tạo hiệu ứng khi rê chuột.
- `@media`: điều chỉnh giao diện theo kích thước màn hình.
- `max-width`: giới hạn chiều rộng nội dung.