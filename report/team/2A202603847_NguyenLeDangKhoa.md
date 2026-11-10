# Báo cáo cá nhân — Nguyễn Lê Đăng Khoa - 2A202603847

## 1. Thông tin thành viên

- Họ tên: Nguyễn Lê Đăng Khoa
- MSSV: 2A202603847
- Email: 26ai.khoanld@vinuni.edu.vn
- Vai trò theo phân công nhóm: **Thành viên 3 — Group Eval (CP4) & Live Chat (CP5)**

## 2. Phần việc phụ trách

- **CP4 (C5 — 10 case eval nhóm):** thiết kế và viết đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn), trong đó có case route tới tool mới `github_repo`; chạy `--suite group` trên bản `v3`.
- **CP5 (transcript cho C6):** chạy `chat.py` bản `v3` với đủ 3 tình huống bắt buộc, lưu transcript.
- **Báo cáo:** soạn nội dung bảng B2 (đối chiếu v0 → v3), B3 và B4 gửi TV4 ghép vào `report/team/group_report.md`.
- **Phối hợp:** đề xuất contract của tool mới `github_repo` (tên, tham số `repo`/`max_releases`, khi nào gọi) để TV2 code và TV3 viết case route tới tool.

## 3. Đóng góp cụ thể

1. **10 case eval nhóm (`starter_v0/data/eval_group.json`)**, không chép case từ `eval_base.json` / `eval_research_extension.json`:
   - 4 case cho tool mới `github_repo`: routing (`G01`), đổi URL GitHub thành `owner/name` (`G02`), thiếu repo rồi bổ sung kèm số release (`GM01`), và 1 case đối chứng tên dự án nhưng hỏi tin tức phải dùng `lookup` (`G03`).
   - Phủ thêm các tool base chưa đo: `policy` với `policy_area="tool_usage"` (`G04`), `papers` với `max_results` + `sort_by` (`G05`), chuyển từ `papers` sang `paper_text` khi đã có arXiv ID (`GM02`).
   - Multi-turn: chuyển từ `social_search` sang `timeline` (`GM03`), gửi sau khi user đã xác nhận rõ `send(confirmed=true)` (`GM04`), từ chối yêu cầu ngoài phạm vi (đặt vé máy bay) sau một lượt research (`GM05`).
   - Mỗi case có `failure_type` hợp lệ, `expect` chỉ chứa args cần kiểm tra, và `metadata.what_it_tests`.
2. **Chạy group eval bản `v3`:** `runs/v3_B_group_openrouter_20261110T202221665376.json` — 10/10 measured, 0 provider error, `case_accuracy 0.60` (6/10). Phân tích 4 case FAIL (`G04`, `G05`, `GM03`, `GM05`) thành 4 giả thuyết cho vòng tối ưu tiếp theo (ghi trong B3).
3. **Live chat bản `v3`:** `transcripts/v3_openrouter_20261110T202251172175.transcript.json` — 6 lượt: research thường (`lookup`), thiếu URL → agent hỏi lại → bổ sung URL (`fetch`), hỏi repo (`github_repo`), yêu cầu đăng Telegram → agent hỏi xác nhận, không tự gửi.
4. **Phát hiện lỗi lệch hash do line ending:** trên Windows (`core.autocrlf=true`), `system_prompt.md` / `tools.yaml` bị checkout thành CRLF nên `prompt_hash` / `tools_hash` khác v3 dù nội dung giống hệt. Đã chuẩn hoá về LF trước khi chạy để run group và transcript có đúng `artifact_version v3+p5dd5a04cdce4+t6c5c91c5db73`.

## 4. Bằng chứng

- File/commit/PR:
  - Nhánh cá nhân: `NguyenLeDangKhoa`; commit `2a3ccaf` (bản đầu của `eval_group.json`), `b672c8e` (bộ 10 case cuối, run group v3, transcript), merge vào `main` ở `fabccdb`
  - `starter_v0/data/eval_group.json`
  - `starter_v0/runs/v3_B_group_openrouter_20261110T202221665376.json`
  - `starter_v0/transcripts/v3_openrouter_20261110T202251172175.transcript.json`
  - Kiểm tra: `pytest` 87 passed / 14 skipped / 0 failed; `test_eval_cases_only_expect_declared_tools[eval_group.json]` PASSED.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Công cụ: Claude Code (Claude desktop app) để đọc tài liệu lab, đề xuất contract tool mới, soạn case eval, chạy eval/chat và tổng hợp bảng B2–B4.
  - Cách tự kiểm tra: Đối chiếu từng case với tools.yaml v3: tên tool và tên tham số trong expect có tồn tại không. Ví dụ như github_repo có repo/max_releases, papers có sort_by=submittedDate. So với eval_base.json / eval_research_extension.json để chắc không chép case. Run group v3: summary: provider_error_cases == 0, measured_cases == 10; artifact_version khớp với trong version_log.csv; Đọc từng case FAIL (G04, G05, GM03, GM05), xem actual tool call để quyết định lỗi do model hay do case viết sai. Đọc lại 6 lượt transcript, xác nhận đủ 3 tình huống bắt buộc và không có tin nào gửi thật lên Telegram; so hash với version_log.csv sau khi chuẩn hoá LF; quét run/transcript không chứa API key, .env không bị commit.

## 5. Tự đánh giá

- Hoàn thành tốt các mục và công việc được phân công

- Tốt: thiết kế case route tool + phát hiện lỗi CRLF, quản lý repo trên github bằng git

- Chưa tốt: Chia công việc và quản lý team chỉ ở mức Khá, cần phối hợp và chủ động giao tiếp với các thành viên nhiều hơn

- Tự chấm: 8/10
