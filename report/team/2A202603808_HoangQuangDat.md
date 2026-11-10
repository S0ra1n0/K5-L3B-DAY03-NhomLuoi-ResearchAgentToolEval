# Báo cáo cá nhân — Hoàng Quang Đạt - 2A202603808

## 1. Thông tin thành viên

- Họ tên: Hoàng Quang Đạt
- MSSV: 2A202603808
- Email: 26ai.dathq@vinuni.edu.vn
- Vai trò theo phân công nhóm: **Thành viên 2 — Tool Engineer & Unit Test Lead (CP3)** *(kiêm phối hợp hoàn thiện tối ưu `v2 → v3` ở CP2)*

## 2. Phần việc phụ trách

- **Phụ trách chính CP3 (C4 — Tool mới & Unit test):**
  - Thiết kế và triển khai code cho tool mới `github_repo` theo contract nhóm đã chốt (`repo` dạng `owner/name`, `max_releases` trong `0–10`).
  - Viết tài liệu đặc tả `TOOL.md` đúng chuẩn frontmatter trong `starter_v0/tools/README.md`.
  - Đăng ký `github_repo` vào `TOOL_FUNCTIONS` (`starter_v0/tools/__init__.py`) và khai báo ở cuối `starter_v0/artifacts/tools.yaml`.
  - Viết unit test offline cho `github_repo` trong `starter_v0/tests/test_tools_todo.py` và đảm bảo bộ `test_tool_contract.py` luôn xanh.
  - Điền phần bằng chứng TV2 (`A2`, bảng tool mới ở mục `3`, `B5a`, mục `5`) vào `report/team/group_report.md`.
- **Hỗ trợ khởi tạo CP1 & tối ưu `v2 → v3` (CP2):**
  - Cài đặt `.venv` và thư viện trong `starter_v0/requirements.txt`, chạy baseline `v0` hợp lệ (`provider_error_cases = 0`).
  - Rà soát kết quả `v0 → v1` từ TV1, chuẩn hóa format `starter_v0/artifacts/version_log.csv`, trực tiếp tối ưu và chạy eval vòng **`v2`** (`system_prompt.md`) và **`v3`** (`tools.yaml` tiếng Việt).
  - Soạn TODO list bàn giao cho TV3 và TV4 (`docs/TODO-TV3-TV4.md`) sau khi chốt `v3`.

## 3. Đóng góp cụ thể

1. **Xây dựng tool mới `github_repo` (`starter_v0/tools/github_repo/tool.py`):**
   - Cài đặt `get_github_repo(repo="", max_releases=3)` gọi GitHub REST API (`/repos/{owner}/{name}` và `/repos/{owner}/{name}/releases`).
   - Validate chặt tham số đầu vào:
     - `_validate_repo`: bắt buộc chuỗi `owner/name` hợp lệ; từ chối chuỗi rỗng, URL đầy đủ (`http://`, `https://`, `github.com/...`), ký tự `@`, đuôi `.git`, hoặc sai cấu trúc `owner/name`.
     - `_validate_max_releases`: bắt buộc số nguyên (loại `bool`) trong khoảng `0–10`; khi `max_releases=0` bỏ qua request lấy releases.
   - Chuẩn hóa dữ liệu trả về gồm metadata (`repo`, `url`, `description`, `stars`, `forks`, `language`, `license`, `pushed_at`, `releases`) và mảng `items` tương thích với tool `format`; xử lý an toàn trường hợp repo không có license (`license: None`) và hỗ trợ biến môi trường tùy chọn `GITHUB_TOKEN`.
   - Bọc toàn bộ luồng thực thi để mọi lỗi (validate input, HTTP 403/404, timeout) trả về error dict qua `tools._shared.err` thay vì `raise` exception.
2. **Viết tài liệu & đồng bộ registry/schema:**
   - Tạo `starter_v0/tools/github_repo/TOOL.md` với YAML frontmatter khớp contract (`name: github_repo`, `track: bonus`, `kind: live_api`, `requires_env: []`, `inputs: [repo, max_releases]`).
   - Đăng ký `"github_repo": get_github_repo` trong `starter_v0/tools/__init__.py` và bổ sung declaration ở cuối `starter_v0/artifacts/tools.yaml`.
3. **Viết 5 hàm unit test offline (20 test case parametrize) trong `starter_v0/tests/test_tools_todo.py`:**
   - `test_github_repo_zero_releases_fetches_repo_only_and_maps_fields`: mock `fake_http`, kiểm tra `max_releases=0` chỉ gọi 1 GET tới `/repos/openai/whisper` (không gửi `Authorization` khi không có token) và map đủ field.
   - `test_github_repo_with_max_releases_fetches_releases_and_handles_null_license`: mock phân tách endpoint `/repos/...` và `/releases`, kiểm tra gửi `GITHUB_TOKEN`, truyền `params={"per_page": 2}`, xử lý `license: None` và map danh sách `releases`.
   - `test_github_repo_rejects_invalid_repo_without_network_call`: kiểm tra 9 dạng input `repo` sai (`""`, khoảng trắng, URL, `@`, `.git`, thiếu/dư `/`, số) → trả `ValueError` dict và không gọi HTTP (`calls == []`).
   - `test_github_repo_rejects_invalid_max_releases_without_network_call`: kiểm tra 6 giá trị `max_releases` sai (`-1`, `11`, `"3"`, `True`, `None`, `1.5`) → trả `ValueError` dict và `calls == []`.
   - `test_github_repo_http_error_or_timeout_returns_error_dict`: kiểm tra HTTP 404, HTTP 403 và `requests.Timeout` → trả về error dict (`HTTPError` / `Timeout`), không làm crash agent.
4. **Tối ưu vòng `v2 → v3` dựa trên bằng chứng log (`0.70 → 0.85 → 0.90`):**
   - **Vòng `v2` (`starter_v0/artifacts/system_prompt.md`):** Sau khi đọc 6 case FAIL của `v1` (`R03`, `R08`, `R10`, `R11`, `R12`, `R13`), viết lại toàn bộ `system_prompt.md` bằng tiếng Anh (xóa 3 chỉ dẫn sai của starter, thêm rule `no_tool` cho out-of-scope, `clarify` khi thiếu info, boundary xác nhận `send`, routing gồm `github_repo`, multi-turn context và trust boundary). Kết quả `case_accuracy` tăng từ **0.70 → 0.85** (`17/20`), `tool_routing_accuracy` tăng **0.80 → 0.95**.
   - **Vòng `v3` (`starter_v0/artifacts/tools.yaml`):** Giữ toàn bộ `tools.yaml` bằng tiếng Việt, viết lại rõ *khi nào dùng / không dùng* và quy ước tham số cho cả 11 tool (phân tách `lookup` với `social_search`, `query` của `lookup` không lặp `'news'`, `send` chỉ gửi khi `confirmed=true`). Kết quả `case_accuracy` tăng tiếp từ **0.85 → 0.90** (`18/20`), `multiturn_accuracy` đạt **1.00**.
   - Chuẩn hóa format `starter_v0/artifacts/version_log.csv` (xử lý lỗi ngoặc kép `"""` và 13 dòng trống), ghi đủ chuỗi `v0 → v1 → v2 → v3`, và viết phần đóng góp TV2 vào `report/team/group_report.md`.
5. **Cung cấp nội dung mục B5a (ví dụ lỗi unit test bắt được mà eval không bắt được):**
   - Eval chỉ chấm model có gọi `github_repo(repo="openai/whisper", max_releases=2)` hay không; nếu code tool crash `AttributeError` khi JSON trả `"license": None`, quên truyền `per_page=max_releases`, hoặc vẫn gọi mạng khi `repo` dính URL/`@` thì eval không bắt được — chỉ unit test mới phát hiện được.

## 4. Bằng chứng

- **Nhánh & Commit đã push:**
  - Nhánh cá nhân: `HoangQuangDat` (`origin/HoangQuangDat`), đã merge vào `main` (`47f1e73`, `8801872`).
  - Commit đã push: `a819a6d` (`done: tao tool, dang ky registry, viet 5 unit test offline`), `68f4401` (`docs: them file bao cao ca nhan 2A202603808-HoangQuangDat.md`).
  - *(Bổ sung commit hash mới sau khi push phần `v2–v3`, `group_report.md`, `TODO-TV3-TV4.md` và bản cập nhật này)*
- **File đã tạo / chỉnh sửa:**
  - Tool & test (CP3): `starter_v0/tools/github_repo/tool.py`, `starter_v0/tools/github_repo/TOOL.md`, `starter_v0/tools/__init__.py`, `starter_v0/tests/test_tools_todo.py`
  - Prompt, tools & log (CP2): `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/v2_B_base_openrouter_20261110T194247983178.json`, `starter_v0/runs/v3_B_base_openrouter_20261110T194947018823.json`
  - Báo cáo & bàn giao: `report/team/group_report.md` (phần `A2`, bảng tool mới mục `3`, `B5a`, mục `5`), `report/team/2A202603808_HoangQuangDat.md`, `docs/TODO-TV3-TV4.md`
- **Kết quả kiểm tra thực tế:**
  - `pytest tests/test_tool_contract.py -v`: **60 passed** (đồng bộ `tools.yaml` ↔ `TOOL_FUNCTIONS` ↔ `TOOL.md` ↔ signature sau khi sửa `tools.yaml` tiếng Việt).
  - `pytest -q` toàn suite: **87 passed, 14 skipped, 0 failed** (20/20 case `github_repo` pass; 14 stub tool sẵn có giữ `SKIPPED`).
  - Eval `v2`: `17/20` (`case_accuracy: 0.85`, `provider_error_cases: 0`, `v2+p3264a46e7b62+tfef6d9598408`).
  - Eval `v3`: `18/20` (`case_accuracy: 0.90`, `tool_routing_accuracy: 0.95`, `argument_accuracy: 0.90`, `multiturn_accuracy: 1.00`, `provider_error_cases: 0`, `v3+p5dd5a04cdce4+t6c5c91c5db73`).
  - Smoke test live `TOOL_FUNCTIONS["github_repo"]("openai/whisper", max_releases=2)`: trả về `{'tool': 'github_repo', 'error': 'HTTPError', 'message': '403 Client Error: rate limit exceeded for url: https://api.github.com/repos/openai/whisper'}` (xác nhận nhánh xử lý lỗi không raise exception khi gặp rate limit IP dùng chung).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - **Công cụ đã dùng:** Trợ lý AI **Antigravity** để phân tích đề lab, thiết kế/code tool `github_repo`, viết unit test offline, phân tích failure log `v1 → v2 → v3`, tinh chỉnh `system_prompt.md`/`tools.yaml`, và tổng hợp báo cáo.
  - **Cách tự kiểm tra kết quả:**
    1. Đối chiếu trực tiếp với `starter_v0/tools/README.md`, `starter_v0/tests/conftest.py` (`FakeResponse`, `fake_http`, `block_network`) và `starter_v0/tests/test_tools_examples.py`.
    2. Chạy `pytest tests/test_tool_contract.py -v` và `pytest -q` trong `.venv` (Python 3.10.11) sau mỗi lần chỉnh sửa `tools.yaml` / `tool.py` / `test_tools_todo.py`.
    3. Chạy thật `run_eval.py` cho `v2` và `v3` trên OpenRouter (`openai/gpt-4o-mini`), kiểm tra `provider_error_cases == 0`, đọc chi tiết từng case FAIL trong JSON để đặt giả thuyết vòng sau, và kiểm tra `version_log.csv` parse sạch bằng `csv.DictReader`.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Hoàn thành 100% phần việc của **Thành viên 2 (CP3 — C4)** (tool `github_repo` + 20 test case offline pass) và hỗ trợ hoàn thiện chuỗi tối ưu **`v0 → v3` đạt `18/20` (`0.90`)** ở CP2.
- **Hạn chế & điểm lưu ý:**
  - Ở `v3` còn 2 case biên (`R10_missing_handle` gọi `social_search(query="tweet")` thay vì `clarify`; `R12_confirm_before_send` chọn `clarify(response_type="text")` thay vì `"yes_no"`).
  - Khi chạy live `github_repo` trên mạng dùng chung IP lớp học, GitHub REST API ẩn danh giới hạn 60 request/giờ nên có thể gặp HTTP 403 rate limit nếu không cấu hình biến tùy chọn `GITHUB_TOKEN` trong `.env`.
