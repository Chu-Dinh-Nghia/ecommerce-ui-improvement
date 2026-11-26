# Bài tập Advance Front-end & Backend — Chu Đình Nghĩa

## Nội dung

- `Bai1.html`: bài thực hành giao diện và hiệu ứng.
- `Bai2.js`: ví dụ HTTP server ban đầu.
- `index.html`, `app.js`, `server.js`: ứng dụng TODO hoàn chỉnh với API Node.js.
- `todo.sqlite`: database SQLite của ứng dụng (ban đầu không có công việc).
- `Chu_Đình_Nghĩa.docx`: báo cáo và hình minh chứng.

## Chạy ứng dụng TODO

1. Cài Node.js 24.
2. Giải nén toàn bộ ZIP, rồi nhấp đúp `start.bat`. Giữ cửa sổ server mở khi sử dụng.
3. Nếu chạy thủ công, mở terminal trong thư mục này và chạy `node server.js`, sau đó mở `http://localhost:8080`.
4. Xem dữ liệu API tại `http://localhost:8080/api/tasks`.

Ứng dụng cần được mở qua server. Nếu `localhost:8080` báo từ chối kết nối, hãy chạy `start.bat` trước. Dữ liệu được lưu trong `todo.sqlite`.
