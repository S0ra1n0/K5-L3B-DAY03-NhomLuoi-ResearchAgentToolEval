# Team

## Thông tin nhóm

- Tên nhóm: **Nhóm Lười**
- Lớp: **L3B**
- Repo nhóm: `K5-L3B-DAY03-NhomLuoi-ResearchAgentToolEval` (hoặc `K5-L3B-DAY03-NguyenLeDangKhoa-2A202603847-PromptEngineeringToolCalling`)
- URL repo, nhánh nộp, commit chốt:
  - URL repo: `https://github.com/S0ra1n0/K5-L3B-DAY03-NguyenLeDangKhoa-2A202603847-PromptEngineeringToolCalling`
  - Nhánh nộp: `main` (trưởng nhóm merge từ các nhánh thành viên)
  - Commit chốt: <!-- Trưởng nhóm điền sau khi merge final -->

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Anh Trung | 2A202603903 | 26ai.trungnva@vinuni.edu.vn | `NguyenVanAnhTrung` | **Thành viên 1:** Khởi tạo baseline, chạy eval v0–v1, ghi nhận log ban đầu |
|   2 | Hoàng Quang Đạt | 2A202603808 | 26ai.dathq@vinuni.edu.vn | `HoangQuangDat` | **Thành viên 2:** Tool mới `github_repo`, viết 5 hàm unit test (20 case), tối ưu v2–v3 |
|   3 | Nguyễn Lê Đăng Khoa | 2A202603847 | 26ai.khoanld@vinuni.edu.vn | `S0ra1n0` | **Thành viên 3 (Trưởng nhóm):** Thiết kế 10 case eval nhóm, chạy live chat 6 lượt, quản lý merge repo |
|   4 | Đỗ Anh Thư | 2A202603815 | 26ai.thuda@vinuni.edu.vn | `DoAnhThu832004` | **Thành viên 4:** Xây dựng Streamlit UI (C6) + deploy Cloudflare, tổng hợp báo cáo nhóm C7, TEAM.md, dọn dẹp repo |

---

## Cá nhân

Mỗi thành viên có một báo cáo riêng trong thư mục `report/team/`:

- `report/team/2A202603903_NguyenVanAnhTrung.md`
- `report/team/2A202603808_HoangQuangDat.md`
- `report/team/2A202603847_NguyenLeDangKhoa.md`
- `report/team/2A202603815_DoAnhThu.md`

---

## NguyenVanAnhTrung-2A202603903

### Phần việc phụ trách

- Thiết lập môi trường và cấu hình API provider ban đầu cho dự án.
- Chạy đánh giá đo lường phiên bản baseline **v0** (`case_accuracy = 0.70`).
- Thử nghiệm giả thuyết vòng **v1** (tinh chỉnh từ ngữ đầu prompt để giảm sự hấp tấp của agent) và lưu trữ run log vào `version_log.csv`.

### Đóng góp cụ thể

- Tạo và kiểm thử các file run baseline v0: `runs/v0_B_base_openrouter_20261110T180724056379.json`.
- Chạy thử nghiệm v1: `runs/v1_B_base_openrouter_20261110T190117456928.json` và cập nhật dữ liệu hàng đầu tiên trong `artifacts/version_log.csv`.
- Phối hợp cùng TV2 và TV3 phân tích nguyên nhân tại sao v1 không tăng điểm (do chỉ sửa nhẹ prompt, chưa giải quyết được 3 chỉ dẫn xấu của starter).

### Bằng chứng

- File / Commit: Commit `8d52781`, `0f23405` trên nhánh `NguyenVanAnhTrung`.
- Run files: `starter_v0/runs/v0_B_base_openrouter_20261110T180724056379.json`, `starter_v0/runs/v1_B_base_openrouter_20261110T190117456928.json`.

---

## HoangQuangDat-2A202603808

### Phần việc phụ trách

- Phụ trách chính phần Tool mới và Unit test (C4 — CP3).
- Đồng phối hợp tối ưu hóa vòng **v2** (`system_prompt.md`) và **v3** (`tools.yaml`).
- Viết 5 hàm unit test (20 test case parametrize) offline 100% cho tool mới.

### Đóng góp cụ thể

- Xây dựng tool mới `github_repo` (`starter_v0/tools/github_repo/tool.py`, `TOOL.md`), kết nối API GitHub lấy stars, forks, ngôn ngữ, license, push date và releases, bọc an toàn HTTP/timeout.
- Đăng ký `github_repo` vào `TOOL_FUNCTIONS` và khai báo schema trong `artifacts/tools.yaml`.
- Viết 5 hàm test trong `starter_v0/tests/test_tools_todo.py` (pass 87/87 test toàn bộ suite, 0 failed).
- Viết lại `system_prompt.md` (v2: tăng accuracy lên **0.85**) và `tools.yaml` tiếng Việt (v3: tăng accuracy lên **0.90**).

### Bằng chứng

- File / Commit: Commit `a819a6d`, `68f4401`, `cd41ec5` trên nhánh `HoangQuangDat`.
- Code & test: `starter_v0/tools/github_repo/`, `starter_v0/tests/test_tools_todo.py`.
- Run files: `starter_v0/runs/v2_B_base_openrouter_20261110T194247983178.json`, `starter_v0/runs/v3_B_base_openrouter_20261110T194947018823.json`.

---

## NguyenLeDangKhoa-2A202603847

### Phần việc phụ trách

- Trưởng nhóm, điều phối luồng làm việc và phân chia nhiệm vụ.
- Thiết kế bộ 10 test case đánh giá nhóm (C5 — CP4) trong `starter_v0/data/eval_group.json`.
- Chạy live chat tương tác thực tế với agent v3 (C6 — CP5) và lưu trữ transcript.
- Quản lý tích hợp (merge) các nhánh thành viên vào `main`.

### Đóng góp cụ thể

- Thiết kế 10 case eval nhóm chuẩn format (5 single-turn, 5 multi-turn), bao gồm 4 case kiểm tra routing tới tool mới `github_repo` và đối chứng.
- Chạy group eval bản v3: đạt case accuracy **0.60** (6/10), phân tích chi tiết 4 case fail.
- Thực hiện phiên live chat 6 lượt thể hiện đầy đủ 3 tình huống bắt buộc: research web, clarify khi thiếu URL, route tool github_repo, và guardrail chặn gửi Telegram khi chưa xác nhận.
- Phát hiện và hướng dẫn xử lý lỗi lệch hash line ending CRLF trên Windows.

### Bằng chứng

- File / Commit: Commit `2a3ccaf`, `f96a68c`, `fabccdb` trên nhánh `NguyenLeDangKhoa`.
- Eval file: `starter_v0/data/eval_group.json`.
- Run group: `starter_v0/runs/v3_B_group_openrouter_20261110T202221665376.json`.
- Transcript: `starter_v0/transcripts/v3_openrouter_20261110T202251172175.transcript.json`.

---

## DoAnhThu-2A202603815

### Phần việc phụ trách

- Phát triển ứng dụng Web UI tương tác bằng Streamlit (`starter_v0/app.py`) đáp ứng tiêu chí C6.
- Hướng dẫn thiết lập link dùng thử thông qua Cloudflare Tunnel cho buổi showdown.
- Tổng hợp và hoàn thiện toàn bộ báo cáo nhóm `report/team/group_report.md` (Phần A + B) đáp ứng tiêu chí C7.
- Xây dựng tài liệu nhóm `TEAM.md`, viết báo cáo cá nhân `report/team/2A202603815_DoAnhThu.md`.
- Dọn dẹp repository: loại bỏ các file run thừa/không ghi nhận, transcript không đạt, cập nhật lại phân tích `analysis/base_runs.csv`.

### Đóng góp cụ thể

- Xây dựng Web UI Streamlit đa lượt hoàn chỉnh:
  - Tái sử dụng `run_model_tool_loop` và logic từ `chat.py`.
  - Hiển thị đầy đủ mọi tool call (`name`, `args`) và kết quả/lỗi chi tiết dưới dạng JSON expander, không che giấu lỗi.
  - Tạm dừng và hiển thị thông báo chờ người dùng khi agent gọi `clarify` (`waiting_for_user`).
  - Hiển thị nổi bật `artifact_version` (`v3+p5dd5a04cdce4+t6c5c91c5db73`) ở sidebar để minh chứng chạy đúng bản v3.
  - Tích hợp sẵn 5 câu hỏi mẫu A3 vào sidebar để người chấm và các nhóm khác có thể test nhanh bằng 1 click.
- Thiết lập cấu hình `.gitattributes` ép kiểu `eol=lf` cho các file artifact trên Windows, giải quyết dứt điểm lỗi lệch mã băm hash.
- Hoàn thiện toàn bộ báo cáo nhóm `group_report.md` với đầy đủ thông tin Phần A, Phần B, các bảng số liệu thực tế B1–B4, B5a và phần phân tích cải tiến B6.
- Dọn dẹp repo sạch sẽ: `git rm` 3 run không ghi log và 1 transcript chào hỏi không đạt tiêu chí; chạy lại `scripts/parse_runs.py` sinh 90 dòng dữ liệu phân tích chuẩn xác.

### Bằng chứng

- File: `.gitattributes`, `starter_v0/app.py`, `starter_v0/requirements.txt`, `starter_v0/analysis/base_runs.csv`, `report/team/group_report.md`, `TEAM.md`, `report/team/2A202603815_DoAnhThu.md`.
- Nhánh làm việc: `DoAnhThu`.
