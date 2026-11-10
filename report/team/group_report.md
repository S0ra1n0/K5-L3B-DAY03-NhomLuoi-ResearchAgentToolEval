# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| github_repo | lấy thông tin repo GitHub cụ thể (stars, forks, ngôn ngữ, license, lần push gần nhất, releases) | **có** |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **Thay đổi trong `system_prompt.md` và `tools.yaml`:** *(TV1 bổ sung sau khi hoàn tất v1–v3)*

**Tool mới nhóm viết:**

| Tên tool | Làm gì | Khi nào agent nên gọi (và không nên gọi) |
|---|---|---|
| `github_repo` | Gọi GitHub REST API lấy thông tin repo (`stars`, `forks`, ngôn ngữ chính, `license`, `pushed_at`) và tối đa `max_releases` (`0–10`) bản release gần nhất theo chuẩn `owner/name`; đồng thời trả về `items` tương thích `format`. | **Nên gọi:** khi user hỏi số liệu/thông tin/release của một repo GitHub cụ thể.<br>**Không gọi:** cho tin tức (`lookup`), tweet (`social_search`), đọc trang web (`fetch`), hay paper (`papers`); nếu chưa rõ `owner/name` phải gọi `clarify` trước. |

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/github_repo/`) | `starter_v0/tools/github_repo/tool.py`, `starter_v0/tools/github_repo/TOOL.md`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` (commit `a819a6d`, nhánh `HoangQuangDat`) | Hàm `get_github_repo(repo, max_releases=3)` gọi GitHub REST API lấy `stars`, `forks`, `language`, `license`, `pushed_at` và danh sách `releases` (`0–10`), đồng thời trả về `items` tương thích `format`; smoke test `test_tool_contract.py` đạt **60 passed**. | Validate chặt `repo` dạng `owner/name` (chặn chuỗi rỗng, URL, `@`, `.git`) và `max_releases` (`int` `0–10`, loại `bool`); mọi lỗi HTTP/timeout trả về error dict qua `err()`, không `raise`. Lưu ý mạng dùng chung IP dễ gặp HTTP 403 rate limit của GitHub nếu không cấu hình thêm biến tùy chọn `GITHUB_TOKEN` trong `.env`. |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `pytest -v` (**87 passed, 14 skipped, 0 failed**) | Viết **5 hàm test (20 test case parametrize)** chạy offline hoàn toàn bằng `fake_http`/`monkeypatch`: happy path `max_releases=0` và `max_releases=2` (kèm `license: None`), chặn 9 dạng `repo` sai và 6 giá trị `max_releases` sai trước khi gọi HTTP (`calls == []`), xử lý HTTP 403/404 và `requests.Timeout` trả error dict. | Bắt buộc mock HTTP qua `fake_http`/`monkeypatch` (fixture `block_network` chặn mạng thật) và phân biệt 2 endpoint `/repos/...` vs `/releases` khi `max_releases > 0`. |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: Đã viết **5 hàm unit test (20 test case parametrize)** cho `github_repo` trong `starter_v0/tests/test_tools_todo.py` (toàn bộ 20/20 case pass, `test_tool_contract.py` 60/60 pass, toàn suite 87 passed / 14 skipped thuộc stub tool sẵn có / 0 failed). **Ví dụ lỗi unit test bắt được nhưng eval không bắt được:** eval chỉ kiểm tra model có gọi `github_repo(repo="openai/whisper", max_releases=2)` hay không; nếu code tool bị crash `AttributeError` khi repo không có license (`"license": null`), quên truyền `params={"per_page": max_releases}` lên API, hoặc vẫn gửi HTTP request khi `repo` là URL/`@` thì eval vẫn chấm PASS nếu chỉ xét tool call của model — chỉ unit test offline mới bắt được các lỗi cài đặt này.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- **GitHub API rate limit (HTTP 403) khi smoke test tool mới `github_repo`:** Khi gọi live `TOOL_FUNCTIONS["github_repo"]("openai/whisper", max_releases=2)` trên mạng dùng chung IP lớp học, GitHub trả về `{'tool': 'github_repo', 'error': 'HTTPError', 'message': '403 Client Error: rate limit exceeded for url: https://api.github.com/repos/openai/whisper'}` (do giới hạn 60 req/giờ cho IP ẩn danh). **Cách xử lý:** Tool đã bọc lỗi để trả về error dict thay vì crash agent, hỗ trợ biến môi trường tùy chọn `GITHUB_TOKEN` (nâng hạn mức lên 5.000 req/giờ khi chạy live/demo), và toàn bộ unit test trong `starter_v0/tests/test_tools_todo.py` chạy offline 100% qua `fake_http`/`monkeypatch`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
