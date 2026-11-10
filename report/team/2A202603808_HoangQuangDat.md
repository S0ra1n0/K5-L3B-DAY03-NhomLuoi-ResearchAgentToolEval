# Báo cáo cá nhân — Hoàng Quang Đạt - 2A202603808

## 1. Thông tin thành viên

- Họ tên: Hoàng Quang Đạt
- MSSV: 2A202603808
- Email: 26ai.dathq@vinuni.edu.vn
- Vai trò theo phân công nhóm: **Thành viên 2 — Tool Engineer & Unit Test Lead (CP3)**

## 2. Phần việc phụ trách

- **Phụ trách chính CP3 (C4 — Tool mới & Unit test):**
  - Thiết kế và triển khai code cho tool mới `github_repo` theo contract nhóm đã chốt (`repo` dạng `owner/name`, `max_releases` trong `0–10`).
  - Viết tài liệu đặc tả `TOOL.md` đúng chuẩn frontmatter trong `starter_v0/tools/README.md`.
  - Đăng ký `github_repo` vào `TOOL_FUNCTIONS` (`starter_v0/tools/__init__.py`) và khai báo ở cuối `starter_v0/artifacts/tools.yaml` (giữ nguyên 10 tool gốc do TV1 tối ưu để tránh xung đột khi merge).
  - Viết unit test offline cho `github_repo` trong `starter_v0/tests/test_tools_todo.py` và đảm bảo bộ `test_tool_contract.py` luôn xanh.
  - Chuẩn bị bằng chứng mục **B5a** cho `report/team/group_report.md`.
- **Hỗ trợ khởi tạo CP1:**
  - Cài đặt `.venv` và thư viện trong `starter_v0/requirements.txt`, chạy baseline `v0` hợp lệ (`provider_error_cases = 0`) và ghi nhận dòng `v0` vào `starter_v0/artifacts/version_log.csv`.

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
   - Đăng ký `"github_repo": get_github_repo` trong `starter_v0/tools/__init__.py` và bổ sung declaration + quy tắc routing/args vào cuối `starter_v0/artifacts/tools.yaml`.
3. **Viết 5 hàm unit test offline (20 test case parametrize) trong `starter_v0/tests/test_tools_todo.py`:**
   - `test_github_repo_zero_releases_fetches_repo_only_and_maps_fields`: mock `fake_http`, kiểm tra `max_releases=0` chỉ gọi 1 GET tới `/repos/openai/whisper` (không gửi `Authorization` khi không có token) và map đủ field.
   - `test_github_repo_with_max_releases_fetches_releases_and_handles_null_license`: mock phân tách endpoint `/repos/...` và `/releases`, kiểm tra gửi `GITHUB_TOKEN`, truyền `params={"per_page": 2}`, xử lý `license: None` và map danh sách `releases`.
   - `test_github_repo_rejects_invalid_repo_without_network_call`: kiểm tra 9 dạng input `repo` sai (`""`, khoảng trắng, URL, `@`, `.git`, thiếu/dư `/`, số) → trả `ValueError` dict và không gọi HTTP (`calls == []`).
   - `test_github_repo_rejects_invalid_max_releases_without_network_call`: kiểm tra 6 giá trị `max_releases` sai (`-1`, `11`, `"3"`, `True`, `None`, `1.5`) → trả `ValueError` dict và `calls == []`.
   - `test_github_repo_http_error_or_timeout_returns_error_dict`: kiểm tra HTTP 404, HTTP 403 và `requests.Timeout` → trả về error dict (`HTTPError` / `Timeout`), không làm crash agent.
4. **Cung cấp nội dung mục B5a (ví dụ lỗi unit test bắt được mà eval không bắt được):**
   - Eval chỉ chấm model có gọi `github_repo(repo="openai/whisper", max_releases=2)` hay không; nếu code tool crash `AttributeError` khi JSON trả `"license": None`, quên truyền `per_page=max_releases`, hoặc vẫn gọi mạng khi `repo` dính URL/`@` thì eval không bắt được — chỉ unit test mới phát hiện được.

## 4. Bằng chứng

- **Nhánh & Commit đã push:**
  - Nhánh: `HoangQuangDat` (`origin/HoangQuangDat`)
  - Commit kỹ thuật (CP1 + CP3): `a819a6d` (`done: tao tool, dang ky registry, viet 5 unit test offline`)
  - *(Bổ sung commit cho file báo cáo cá nhân này sau khi push)*
- **File đã tạo / chỉnh sửa:**
  - `starter_v0/tools/github_repo/tool.py`
  - `starter_v0/tools/github_repo/TOOL.md`
  - `starter_v0/tools/__init__.py`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/tests/test_tools_todo.py`
  - `starter_v0/artifacts/version_log.csv` (dòng `v0`) & `starter_v0/runs/v0_B_base_openrouter_20261110T174148296323.json`
- **Kết quả kiểm tra thực tế:**
  - `pytest tests/test_tool_contract.py -v`: **60 passed** (đồng bộ `tools.yaml` ↔ `TOOL_FUNCTIONS` ↔ `TOOL.md` ↔ signature).
  - `pytest tests/test_tools_todo.py -v`: **20/20 case** của `github_repo` **PASSED** (14 stub của các tool sẵn có giữ `SKIPPED`).
  - `pytest -v` toàn suite: **87 passed, 14 skipped, 0 failed**.
  - Smoke test live `TOOL_FUNCTIONS["github_repo"]("openai/whisper", max_releases=2)`: trả về `{'tool': 'github_repo', 'error': 'HTTPError', 'message': '403 Client Error: rate limit exceeded for url: https://api.github.com/repos/openai/whisper'}` (xác nhận nhánh xử lý lỗi không raise exception khi gặp rate limit IP dùng chung).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - **Công cụ đã dùng:** Trợ lý AI **Antigravity** để phân tích yêu cầu các file hướng dẫn lab, lập kế hoạch chia việc song song 4 người, hỗ trợ cài đặt tool `github_repo`, `TOOL.md`, bộ unit test offline và soạn báo cáo cá nhân.
  - **Cách tự kiểm tra kết quả:**
    1. Đối chiếu trực tiếp với `starter_v0/tools/README.md`, `starter_v0/tests/conftest.py` (`FakeResponse`, `fake_http`, `block_network`) và `starter_v0/tests/test_tools_examples.py` để đảm bảo đúng quy ước không gọi mạng thật trong test.
    2. Chạy `pytest tests/test_tool_contract.py -v` và `pytest -v` trong `.venv` (Python 3.10.11) để xác minh toàn bộ contract test và 20 test case của `github_repo` đều pass, assert cả request gửi đi lẫn kết quả trả về.
    3. Chạy smoke test live gọi `TOOL_FUNCTIONS["github_repo"]` để kiểm tra hành vi thực tế và xác nhận nhánh error dict hoạt động đúng khi API trả HTTP 403.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Đạt 100% yêu cầu kỹ thuật  theo đúng phân công nhóm: tool mới rõ ranh giới routing, đồng bộ contract, xử lý input xấu và lỗi mạng không raise exception, có 5 hàm test (20 case) chạy offline ổn định và đã commit/push lên nhánh `HoangQuangDat` (`a819a6d`).
- **Hạn chế & điểm lưu ý:** Khi chạy live trên mạng dùng chung IP lớp học, GitHub REST API ẩn danh giới hạn 60 request/giờ nên có thể gặp HTTP 403 rate limit nếu không cấu hình biến tùy chọn `GITHUB_TOKEN` trong `.env`. Nếu còn thời gian sẽ hỗ trợ nhóm hoàn thiện thêm các test stub trong `test_tools_todo.py` để hướng tới Bonus Test Challenge (`0 skipped`).
