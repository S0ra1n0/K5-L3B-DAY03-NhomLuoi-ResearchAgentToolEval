# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Anh Trung

- MSSV: 2A202603903

## 2. Phần việc phụ trách

Phần việc chính: thiết lập môi trường (CP1), chạy `v0` và `v1` (CP2).

## 3. Đóng góp cụ thể

1. Thiết lập môi trường và cấu hình API provider ban đầu cho dự án.
2. Chạy đánh giá baseline `v0`: `case_accuracy: 0.7`, `tool_routing_accuracy: 0.75`, `argument_accuracy: 0.7`.
3. Thử nghiệm `v1` bằng cách tinh chỉnh câu mở đầu của system prompt để giảm sự hấp tấp của agent. Kết quả: `case_accuracy: 0.7`, `tool_routing_accuracy: 0.8`, `argument_accuracy: 0.7`.
4. Cập nhật hai hàng đầu tiên trong `starter_v0/artifacts/version_log.csv`.
5. Phối hợp cùng TV2 và TV3 phân tích nguyên nhân `v1` chưa tăng case accuracy: chỉ sửa nhẹ prompt, chưa xử lý ba chỉ dẫn xấu của starter.

## 4. Bằng chứng

- File/commit: commits `8d52781` and `0f23405` on branch `NguyenVanAnhTrung`.
- Run files:
  - `starter_v0/runs/v0_B_base_openrouter_20261110T180724056379.json`
  - `starter_v0/runs/v1_B_base_openrouter_20261110T190117456928.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Claude hỗ trợ phân tích các cột trong `version_log.csv` và xác định thông tin cần lấy từ các run files.

## 5. Tự đánh giá

Đã hoàn thành nhiệm vụ chạy `v0` và `v1`. Một hạn chế là system prompt được đọc lướt nên chưa xác định kỹ các chỉ dẫn xấu của starter cần loại bỏ.
