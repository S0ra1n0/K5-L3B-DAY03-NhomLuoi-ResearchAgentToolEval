# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Anh Trung
- MSSV: 2A202603903


## 2.Phần việc phụ trách
Phần việc chính: Thiết lập môi trường(CP1), chạy `v0` và `v1`(CP2)
1. Thiết lập môi trường và cấu hình API provider ban đầu cho dự án.
2. Chạy đánh giá đo lường phiên bản baseline v0 (case_accuracy = 0.70).
3. Thử nghiệm giả thuyết vòng v1 (tinh chỉnh từ ngữ đầu prompt để giảm sự hấp tấp của agent) và lưu trữ run log vào version_log.csv.
## 3.Đóng góp cụ thể
1. Cài đặt các công cụ trong folder `starter_v0` và điền các key vào file `.env` 
2. Chạy baseline v0, thu được kết quả là file: `runs/v0_B_base_openrouter_20261110T180724056379.json`.
Kết quả như sau: `case_accuracy: 0.7`, `tool_routing_accuracy: 0.75`, `argument_accuracy: 0.7`
3. Chạy version 1, thu được kết quả là file: `runs/v1_B_base_openrouter_20261110T190117456928.json`
Kết quả: `case_accuracy: 0.7`, `tool_routing_accuracy: 0.8`, `argument_accuracy: 0.7`, 
4. Cập nhật dữ liệu hai hàng đầu tiên trong `artifacts/version_log.csv`.
5. Phối hợp cùng TV2 và TV3 phân tích nguyên nhân tại sao v1 không tăng điểm (do chỉ sửa nhẹ prompt, chưa giải quyết được 3 chỉ dẫn xấu của starter).
## 4. Bằng chứng
 - File / Commit: Commit 8d52781, 0f23405 trên nhánh NguyenVanAnhTrung.
- Run files: 
    - `starter_v0/runs/v0_B_base_openrouter_20261110T180724056379.json`
     - `starter_v0/runs/v1_B_base_openrouter_20261110T190117456928.json`

- AI/công cụ đã dùng và cách tự kiểm tra kết quả: **Claude** để phân tích các cột trong file `version_log.csv` và gợi ý các trường thông tin trong các run file để đưa vào `version_log.csv`

## 5. Tự đánh giá
Đã hoàn thành nhiệm vụ chạy v0 và v1 với kết quả thu được như trên. Một hạn chế trong quá trình làm nhiệm vụ là system prompt được đọc lướt trong quá trình thực hiện nên không xác định kĩ chỉ dẫn xấu của starter để loại bỏ.
