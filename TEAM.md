# Team

## Thông tin nhóm

- Tên nhóm: **Nhóm Lười**
- Lớp: **L3B**
- Repo nhóm: `K5-L3B-DAY03-NhomLuoi-ResearchAgentToolEval` (hoặc `K5-L3B-DAY03-NguyenLeDangKhoa-2A202603847-PromptEngineeringToolCalling`)
- URL repo, nhánh nộp, commit chốt:
  - URL repo: `https://github.com/S0ra1n0/K5-L3B-DAY03-NhomLuoi-ResearchAgentToolEval`
  - Nhánh nộp: `main` (trưởng nhóm merge từ các nhánh thành viên)
  - Commit chốt: 4c16be5

## Thành viên

| STT | Họ tên               | MSSV        | Email                       | GitHub / tác giả commit (nhánh)           | Vai trò                                                                                                           |
| --: | -------------------- | ----------- | --------------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
|   1 | Nguyễn Văn Anh Trung | 2A202603903 | 26ai.trungnva@vinuni.edu.vn | `FL.Trungocsdiogee` (`NguyenVanAnhTrung`) | **Thành viên 1:** Khởi tạo baseline, chạy eval v0–v1, ghi nhận log ban đầu                                        |
|   2 | Hoàng Quang Đạt      | 2A202603808 | 26ai.dathq@vinuni.edu.vn    | `Quang Dat` (`HoangQuangDat`)             | **Thành viên 2:** Tool mới `github_repo`, viết 5 hàm unit test (20 case), tối ưu v2–v3                            |
|   3 | Nguyễn Lê Đăng Khoa  | 2A202603847 | 26ai.khoanld@vinuni.edu.vn  | `S0ra1n0` (`NguyenLeDangKhoa`)            | **Thành viên 3 (Trưởng nhóm):** Thiết kế 10 case eval nhóm, chạy live chat 6 lượt, quản lý merge repo             |
|   4 | Đỗ Anh Thư           | 2A202603815 | 26ai.thuda@vinuni.edu.vn    | `DoAnhThu832004` (`DoAnhThu`)             | **Thành viên 4:** Xây dựng Streamlit UI (C6) + deploy Cloudflare, tổng hợp báo cáo nhóm C7, TEAM.md, dọn dẹp repo |

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

- File / Commit: Commit `8d52781` (run v0, run v1, prompt v1, `version_log.csv`) trên nhánh `NguyenVanAnhTrung`, merge vào `main` ở `0f23405`; báo cáo cá nhân ở commit `f8a737e` (đưa vào `main` bằng cherry-pick thành `fe07373`, giữ nguyên tác giả).
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
- Viết 5 hàm test (20 test case) trong `starter_v0/tests/test_tools_todo.py`; toàn suite `pytest`: 87 passed, 14 skipped (stub của tool có sẵn), 0 failed.
- Viết lại `system_prompt.md` (v2: tăng accuracy lên **0.85**), rồi viết lại `tools.yaml` tiếng Việt kèm chỉnh tiếp `system_prompt.md` (v3: tăng accuracy lên **0.90**).

### Bằng chứng

- File / Commit: Commit `a819a6d` (tool, registry, unit test), `68f4401` (báo cáo cá nhân), `f96a68c` (prompt v2/v3, `tools.yaml` v3, run v2/v3, sửa `version_log.csv`) trên nhánh `HoangQuangDat`, merge vào `main` ở `47f1e73` và `cd41ec5`.
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
- Bonus Small Local Model (Step 7): chạy base eval trên 2 model local (`qwen3.5:2b`, `qwen3:4b`) qua Ollama, 2 vòng tối ưu `v4-local` (`tools_local.yaml`) và `v5-local` (`system_prompt_local.md`), kiểm tra ngược trên cloud, điền mục B7.

### Bằng chứng

- File / Commit: Commit `2a3ccaf`, `b672c8e` trên nhánh `NguyenLeDangKhoa`; merge vào `main` ở `fabccdb`.
- Eval file: `starter_v0/data/eval_group.json`.
- Run group: `starter_v0/runs/v3_B_group_openrouter_20261110T202221665376.json`.
- Transcript: `starter_v0/transcripts/v3_openrouter_20261110T202251172175.transcript.json`.
- Bonus local model: `starter_v0/artifacts/system_prompt_local.md`, `starter_v0/artifacts/tools_local.yaml`, các run `starter_v0/runs/v3-qwen*`, `v4-local-*`, `v5-local-*`, `starter_v0/analysis/local_runs.csv`.

---

## DoAnhThu-2A202603815

### Phần việc phụ trách

- Xây dựng giao diện Streamlit Web UI (`starter_v0/app.py`) phục vụ chat nhiều lượt và demo (C6).
- Thiết lập Cloudflare Tunnel mở link dùng thử (`https://flashing-treat-cars-prospective.trycloudflare.com`) cho buổi showdown.
- Tổng hợp nội dung báo cáo nhóm `report/team/group_report.md` (Phần A + B) từ các thành viên (C7).
- Viết tài liệu `TEAM.md` và báo cáo cá nhân `report/team/2A202603815_DoAnhThu.md`.
- Dọn dẹp repo: xóa các run thừa không có log, transcript lỗi, cập nhật lại `analysis/base_runs.csv`.

### Đóng góp cụ thể

- Code giao diện Streamlit UI (`starter_v0/app.py`):
  - Tái sử dụng trực tiếp hàm `run_model_tool_loop` từ `chat.py`, giữ nguyên vẹn luồng gọi model.
  - Bọc mỗi tool call trong expander hiển thị rõ tên tool, arguments và kết quả JSON; highlight khung đỏ nếu tool trả về lỗi (không giấu lỗi tool).
  - Bắt trạng thái `waiting_for_user` khi agent gọi `clarify` để hiện thông báo chờ người dùng.
  - Hiện mã băm `artifact_version` (`v3+p5dd5a04cdce4+t6c5c91c5db73`) ở sidebar và thêm sẵn 5 nút câu hỏi mẫu A3.
- Tạo file `.gitattributes` ép kiểu `eol=lf` cho các file trong `artifacts/` trên Windows, tránh lệch mã hash SHA-256.
- Tổng hợp toàn bộ số liệu vào `group_report.md`: hoàn thiện Phần A, các bảng B1–B4, B5a, 5 khó khăn kỹ thuật và mục Reflection B6.
- Dọn repo: `git rm` 3 file run thừa và 1 transcript chào hỏi không có tool; chạy lại `scripts/parse_runs.py` cập nhật file phân tích 90 dòng.

### Bằng chứng

- File: `.gitattributes`, `starter_v0/app.py`, `starter_v0/requirements.txt`, `starter_v0/analysis/base_runs.csv`, `report/team/group_report.md`, `TEAM.md`, `report/team/2A202603815_DoAnhThu.md`.
- Nhánh làm việc: `DoAnhThu`; commit `3976e21` (UI + `.gitattributes`), `0de7f68` (dọn run/transcript, tạo lại analysis), `88b3fb3`, `4ac1a21`, `36686fc` (báo cáo nhóm, TEAM.md, báo cáo cá nhân), `4a477cc` (cập nhật UI); merge vào `main` ở `6a3ae8c`.
