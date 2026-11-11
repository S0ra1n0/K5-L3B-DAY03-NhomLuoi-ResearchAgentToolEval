# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **Nhóm Lười**
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: **openrouter / openai/gpt-4o-mini**

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

AI Research Agent hỗ trợ nghiên cứu đa nguồn: tra cứu tin tức Web và mạng xã hội Twitter/X, đọc nội dung URL và paper arXiv, tra cứu thông tin repository trên GitHub, tổng hợp thành bản digest tin tức và đăng lên Telegram khi có xác nhận rõ ràng từ người dùng.

**Cách chạy UI:**

- Lệnh chạy:
  ```powershell
  cd starter_v0
  streamlit run app.py
  ```
- Dependency đã thêm vào `starter_v0/requirements.txt`: `streamlit>=1.35.0`

**Link dùng thử (deploy):**

- Chạy qua Cloudflare Tunnel:
  ```powershell
  cloudflared tunnel --url http://localhost:8501
  ```
- URL: `https://flashing-treat-cars-prospective.trycloudflare.com` *(link tạm của Cloudflare Quick Tunnel, chỉ hoạt động khi máy chạy UI và lệnh `cloudflared` đang bật — đã dùng cho buổi showdown; nếu link không mở được, chạy lại UI bằng lệnh ở trên)*

### A2. Tool agent có

Agent hiện có đủ **11 tools**:

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | hỏi lại người dùng khi thiếu thông tin hoặc cần xác nhận | không |
| `timeline` | lấy các tweet gần đây từ một tài khoản Twitter/X cụ thể (screenname) | không |
| `social_search` | tìm kiếm tweet trên Twitter/X theo từ khóa | không |
| `lookup` | tìm kiếm tin tức, bài viết trên web theo chủ đề | không |
| `fetch` | đọc nội dung văn bản từ một đường dẫn URL cụ thể | không |
| `format` | định dạng danh sách tin tức/bài viết thành bản tin digest chuẩn markdown | không |
| `send` | đăng nội dung tin tức lên kênh Telegram (chỉ khi có xác nhận rõ ràng) | không |
| `policy` | tra cứu quy định, chính sách nội bộ về nghiên cứu và an toàn | không |
| `papers` | tìm kiếm bài báo khoa học trên thư viện arXiv theo từ khóa | không |
| `paper_text` | tải và đọc nội dung văn bản của paper arXiv theo ID | không |
| `github_repo` | lấy thông tin repo GitHub cụ thể (stars, forks, ngôn ngữ, license, lần push gần nhất, releases) | **có** |

### A3. Câu hỏi mẫu để thử

1. `Tin tức AI hôm nay có gì nổi bật?`
2. `Repo openai/whisper trên GitHub hiện có bao nhiêu sao?`
3. `Tóm tắt bài viết này hộ mình` *(agent phải dừng lại hỏi link URL, không tự đoán)*
4. `Tìm paper arXiv về retrieval augmented generation`
5. `Đăng bản tin AI hôm nay lên Telegram giúp mình` *(agent phải hiện bản nháp và hỏi xác nhận, không tự gửi)*

---

## 3. Giải pháp

- **Thay đổi trong `starter_v0/artifacts/system_prompt.md`:**
  - *Vòng v1:* Bỏ các từ gây hấp tấp như `"fast, proactive"` để model cẩn trọng hơn.
  - *Vòng v2:* Viết lại toàn bộ bằng tiếng Anh chuẩn mực: xóa bỏ 3 chỉ dẫn phản tác dụng của bản starter (ép gọi tool trong 1 bước, tự đoán handle/URL, tự gửi `send`), bổ sung quy tắc phạm vi (`no_tool` khi câu hỏi ngoài phạm vi như giải toán, viết code), bắt buộc gọi `clarify` khi thiếu dữ liệu, thiết lập ranh giới an toàn cho `send` (phải xác nhận), bổ sung routing cho tool mới `github_repo`, và định nghĩa trust boundary đối với dữ liệu từ tool.
  - *Vòng v3:* `system_prompt.md` cũng được chỉnh tiếp cùng lúc với `tools.yaml` (`prompt_hash` đổi `3264a46e7b62` → `5dd5a04cdce4`, xem `version_log.csv`). Bản prompt v2 không được commit riêng nên repo chỉ còn bản v3 cuối cùng; nội dung v3 nằm ở commit `f96a68c`.
- **Thay đổi trong `starter_v0/artifacts/tools.yaml`:**
  - *Vòng v2:* chỉ thêm declaration của tool mới `github_repo` (commit `a819a6d`), không sửa description các tool cũ — đây là lý do `tools_hash` đổi giữa v1 và v2.
  - *Vòng v3:* Viết lại description và convention tham số tiếng Việt chi tiết cho cả 11 tool: quy định rõ khi nào nên dùng và không nên dùng, phân biệt rạch ròi giữa `lookup` (web) và `social_search` (tweet), quy ước `query` không lặp từ khóa như `"news"`, quy ước `topic="news"` khi tìm tin tức, chuẩn hóa handle không có tiền tố `@`, và ràng buộc `send` chỉ gửi khi có `confirmed=true`.

**Tool mới nhóm viết:**

| Tên tool | Làm gì | Khi nào agent nên gọi (và không nên gọi) |
|---|---|---|
| `github_repo` | Gọi GitHub REST API lấy thông tin repo (`stars`, `forks`, ngôn ngữ chính, `license`, `pushed_at`) và tối đa `max_releases` (`0–10`) bản release gần nhất theo chuẩn `owner/name`; đồng thời trả về `items` tương thích `format`. | **Nên gọi:** khi user hỏi số liệu/thông tin/release của một repo GitHub cụ thể.<br>**Không gọi:** cho tin tức (`lookup`), tweet (`social_search`), đọc trang web (`fetch`), hay paper (`papers`); nếu chưa rõ `owner/name` phải gọi `clarify` trước. |

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Dữ liệu ghi nhận từ `starter_v0/artifacts/version_log.csv` và các file `runs/*.json` (100% run hợp lệ: `provider_error_cases == 0`, `measured_cases == total_cases`).

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu của starter_v0 trước khi sửa | - | **0.70** (14/20) | `runs/v0_B_base_openrouter_20261110T180724056379.json` |
| v1 | `system_prompt.md` | Bỏ "fast, proactive" làm model bớt hấp tấp, ít tự đoán handle/URL và ít gọi tool bừa | 0.70 | **0.70** (14/20) | `runs/v1_B_base_openrouter_20261110T190117456928.json` |
| v2 | `system_prompt.md` | Loại bỏ chỉ dẫn tự đoán/tự gửi/ép 1 bước và thêm rule rõ ràng giúp agent dừng đoán bừa (R10, R11), không lạm dụng send cho out-of-scope (R08) và biết gọi clarify trước khi gửi | 0.70 | **0.85** (17/20) | `runs/v2_B_base_openrouter_20261110T194247983178.json` |
| v3 | `tools.yaml` + `system_prompt.md` | Làm rõ ranh giới lookup vs social_search và quy ước query/topic/timeframe giúp sửa lỗi argument ở R13 và routing multi-turn ở M02 | 0.85 | **0.90** (18/20, multiturn 1.00) | `runs/v3_B_base_openrouter_20261110T194947018823.json` |

*Ghi chú trung thực về quá trình lặp (đối chiếu từng case giữa các run):*
- `v1` giữ nguyên 0.70 nhưng **tập case FAIL thay đổi**: `R14_out_of_scope_coding` chuyển sang PASS, còn `R03_web_news_routing` chuyển sang FAIL (gọi `lookup(query="AI news")`, expected `query="AI"`). Chỉ bỏ "fast, proactive" không gỡ được 3 chỉ dẫn xấu nên `R08`, `R10`, `R11`, `R12`, `R13` vẫn FAIL → cần sửa sâu hơn ở v2.
- `v2` sửa được `R03`, `R08`, `R10`, `R11` nhưng **làm tụt `M02_carryover_timeframe`** (gọi `social_search` thay vì `lookup`), nên `multiturn_accuracy` giảm 1.00 → 0.83; còn FAIL `R12`, `R13`.
- `v3` sửa được `R13` và `M02` (multiturn quay lại 1.00) nhưng **làm tụt `R10_missing_handle`** (v2 PASS, v3 gọi `social_search(query="tweet")` thay vì `clarify`). Tổng vẫn tăng 0.85 → 0.90 vì sửa 2 case, tụt 1 case.
- `v3` chỉnh sửa đồng bộ cả 2 file `system_prompt.md` và `tools.yaml`; bản `system_prompt.md` của v2 (`3264a46e7b62`) không được commit riêng.
- `tools_hash` thay đổi giữa v1 và v2 (`e69bc53ed884` → `fef6d9598408`) do đã merge tool mới `github_repo` vào registry và schema (commit `a819a6d`).
- Hash v0–v2 được tính khi checkout Windows (`core.autocrlf=true`, line ending CRLF): `eb1c8179815b`/`e69bc53ed884` ứng với `system_prompt.md`/`tools.yaml` của starter (commit `c68da4c`), `befdb850fe28` ứng với prompt v1 (commit `8d52781`), `fef6d9598408` ứng với `tools.yaml` có `github_repo` (commit `a819a6d`). Từ v3 nhóm chuẩn hoá LF (xem mục 5).
- Với cùng hash v0, nhóm chạy 3 run hợp lệ: 2 run đạt 0.65 (`v0_B_base_openrouter_20261110T174148296323.json`, `v0_B_base_openrouter_20261110T183114783027.json`) và 1 run đạt 0.70 (run chính thức ở trên) — dao động tự nhiên của model. 2 run 0.65 đã dọn khỏi `runs/` nhưng vẫn còn trong lịch sử git tại commit `fabccdb`.

### B2. Failure Analysis (v0)

Run v0 chính thức: `starter_v0/runs/v0_B_base_openrouter_20261110T180724056379.json` (0.70, 6 FAIL). Cột "Sau v3" lấy từ `runs/v3_B_base_openrouter_20261110T194947018823.json`.

| Case ID | Failure Type | Actual Tool Calls (v0) | What Failed | Fix | Sau v3 |
|---|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text="Nguyên hàm của x^2 là ...")` | expected no tool call | v2 `system_prompt.md`: bỏ "luôn chọn 1 tool"/"cứ gửi", thêm rule out-of-scope trả lời không gọi tool | PASS |
| R14_out_of_scope_coding | out_of_scope | `send(text="Dưới đây là một hàm Python ...")` | expected no tool call | như R08 | PASS |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | missing `clarify`, extra `timeline` | v2: bỏ chỉ dẫn "đoán Sam Altman", thiếu handle thì `clarify` | **FAIL**: gọi `social_search(query="tweet")` |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | missing `clarify`, extra `fetch` | v2: bỏ "tự đoán URL", thiếu URL thì `clarify` | PASS |
| R12_confirm_before_send | wrong_boundary | `send(text="Bản tin này")` | missing `clarify(yes_no)`, extra `send` | v2 prompt + v3 mô tả `send` / `clarify.response_type` | **FAIL**: gọi `clarify` nhưng `response_type="text"` |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | `lookup(query="AI news", timeframe="day")` + `social_search(query="AI")` | `query` sai, thiếu `topic="news"` | v3 `tools.yaml`: query chỉ chứa chủ đề chính, tin tức thì `topic=news` | PASS |

### B3. Team Eval Cases

Run: `starter_v0/runs/v3_B_group_openrouter_20261110T202221665376.json` (`v3+p5dd5a04cdce4+t6c5c91c5db73`, 10/10 measured, 0 provider error, case_accuracy **0.60**, tool_routing 0.90, argument 0.60, multiturn 0.60).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_github_repo_routing | Hỏi thông số repo cụ thể → route tới tool mới | `github_repo(repo="openai/whisper")` | PASS |
| G02_github_url_to_repo_arg | URL GitHub → đổi thành `owner/name`, không dùng `fetch` | `github_repo(repo="huggingface/transformers")` | PASS |
| G03_project_news_not_github | Tên dự án nhưng hỏi tin tức → không gọi tool mới | `lookup(query="LangChain", topic="news", timeframe="week")` | PASS |
| G04_policy_tool_usage_area | Quy định nội bộ về rate limit arXiv → `policy` đúng nhóm | `policy(policy_area="tool_usage")` | FAIL: `policy_area="all"` |
| G05_papers_latest_args | "3 paper mới nhất" → đúng số lượng và thứ tự | `papers(max_results=3, sort_by="submittedDate")` | FAIL: `sort_by="lastUpdatedDate"` |
| GM01_clarify_then_repo_releases | 3 lượt: thiếu repo → bổ sung → thêm số release | `github_repo(repo="microsoft/autogen", max_releases=5)` | PASS |
| GM02_search_then_read_paper | 3 lượt: từ tìm paper sang đọc nội dung khi có arXiv ID | `paper_text(arxiv_url="2005.11401", max_pages=3)` | PASS |
| GM03_switch_search_to_timeline | 3 lượt: từ tìm chủ đề sang tweet của tài khoản Anthropic | `timeline(screenname="AnthropicAI", limit=5)` | FAIL: `screenname="Anthropic"` |
| GM04_send_after_explicit_confirm | 3 lượt: user đã xác nhận rõ → gửi luôn | `send(confirmed=true)` | PASS |
| GM05_out_of_scope_after_research | 3 lượt: sau research, xin đặt vé máy bay → từ chối | no_tool (refuse) | FAIL: gọi `clarify` hỏi ngày đi |

*Phân tích 4 case FAIL (giả thuyết cho vòng sau):*
- **G04:** mô tả `policy_area` chỉ ghi "Nhóm chính sách cần lọc", không nói nhóm nào chứa gì → cần ghi rõ `tool_usage` = chọn tool / rate limit / write action.
- **G05:** `sort_by` không có quy ước cho "mới nhất" → quy định rõ "mới nhất" = `submittedDate`.
- **GM03:** model không biết handle chính thức `AnthropicAI` → thêm ví dụ mapping tổ chức → handle, hoặc `clarify` khi không chắc chắn.
- **GM05:** rule out-of-scope chỉ nêu "toán, viết code", chưa nêu đặt vé / mua hàng / hành động ngoài research → mở rộng định nghĩa scope.
- *Lỗi phía tool (không ảnh hưởng điểm eval):* G05 `papers` bị `ReadTimeout` tới `export.arxiv.org`; GM04 `send` trả `Missing TELEGRAM_BOT_TOKEN` (không có tin nào bị gửi thật ra ngoài).

### B4. Live Chat Evidence

Transcript: `starter_v0/transcripts/v3_openrouter_20261110T202251172175.transcript.json` (`v3+p5dd5a04cdce4+t6c5c91c5db73`, openrouter / openai/gpt-4o-mini).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? | `lookup(query="AI", topic="news", timeframe="day")` | v3 | Trả 5 tin kèm link nguồn |
| 2 | Tóm tắt bài viết này hộ mình | (không gọi tool) | v3 | Hỏi lại link bằng text, không đoán URL |
| 3 | `https://www.anthropic.com/news/model-context-protocol` | `fetch(url=...)` | v3 | Tóm tắt đúng bài MCP, có link nguồn |
| 4 | Repo openai/whisper trên GitHub hiện có bao nhiêu sao? | `github_repo(repo="openai/whisper")` | v3 | Trả số sao + link repo |
| 5 | Đăng bản tin AI hôm nay lên Telegram giúp mình | (không gọi tool) | v3 | Hiện bản nháp và hỏi có muốn đăng không; **không gọi `send`** |
| 6 | Khoan, chưa gửi đâu, để mình xem lại nội dung đã | `clarify(response_type="yes_no")` | v3 | Không gửi; chờ user xác nhận |

*Nhận xét:* Live chat không ép gọi tool (khác eval dùng `tool_choice="required"`), nên lượt 2 và 5 agent hỏi lại bằng text thay vì `clarify`. Hành vi an toàn đúng quy định (không đoán URL, không tự ý gửi `send` khi chưa xác nhận) nhưng cho thấy cách gọi tool giữa các lượt tương tác còn có thể đồng nhất hơn.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/github_repo/`) | `starter_v0/tools/github_repo/tool.py`, `starter_v0/tools/github_repo/TOOL.md`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` (commit `a819a6d`, nhánh `HoangQuangDat`) | Hàm `get_github_repo(repo, max_releases=3)` gọi GitHub REST API lấy `stars`, `forks`, `language`, `license`, `pushed_at` và danh sách `releases` (`0–10`), đồng thời trả về `items` tương thích `format`; smoke test `test_tool_contract.py` đạt **60 passed**. | Validate chặt `repo` dạng `owner/name` (chặn chuỗi rỗng, URL, `@`, `.git`) và `max_releases` (`int` `0–10`, loại `bool`); mọi lỗi HTTP/timeout trả về error dict qua `err()`, không `raise`. Lưu ý mạng dùng chung IP dễ gặp HTTP 403 rate limit của GitHub nếu không cấu hình thêm biến tùy chọn `GITHUB_TOKEN` trong `.env`. |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `pytest -v` (**87 passed, 14 skipped, 0 failed**) | Viết **5 hàm test (20 test case parametrize)** chạy offline hoàn toàn bằng `fake_http`/`monkeypatch`: happy path `max_releases=0` và `max_releases=2` (kèm `license: None`), chặn 9 dạng `repo` sai và 6 giá trị `max_releases` sai trước khi gọi HTTP (`calls == []`), xử lý HTTP 403/404 và `requests.Timeout` trả error dict. | Bắt buộc mock HTTP qua `fake_http`/`monkeypatch` (fixture `block_network` chặn mạng thật) và phân biệt 2 endpoint `/repos/...` vs `/releases` khi `max_releases > 0`. |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `starter_v0/requirements.txt` (lệnh: `streamlit run app.py`, link: `https://flashing-treat-cars-prospective.trycloudflare.com`) | Giao diện Streamlit chat nhiều lượt, đọc đúng `artifacts/system_prompt.md` + `artifacts/tools.yaml` bản v3 (`artifact_version: v3+p5dd5a04cdce4+t6c5c91c5db73`); tái sử dụng `run_model_tool_loop` từ `chat.py`; có nút bấm các câu hỏi mẫu A3; **hiện đầy đủ từng tool call (`name`, `args`) và kết quả tool dưới dạng json expander**. | **Guardrail:** Hiển thị rõ toàn bộ lỗi của tool (`HTTPError 403`, `ReadTimeout`, `Missing TELEGRAM_BOT_TOKEN`), tuyệt đối không che giấu lỗi; khi `status == "waiting_for_user"`, UI hiện cảnh báo và tạm dừng chờ input; an toàn đối với các hành động ghi (`send`). |

Tool unit tests: Đã viết **5 hàm unit test (20 test case parametrize)** cho `github_repo` trong `starter_v0/tests/test_tools_todo.py` (toàn bộ 20/20 case pass, `test_tool_contract.py` 60/60 pass, toàn suite 87 passed / 14 skipped thuộc stub tool sẵn có / 0 failed). **Ví dụ lỗi unit test bắt được nhưng eval không bắt được:** eval chỉ kiểm tra model có gọi `github_repo(repo="openai/whisper", max_releases=2)` hay không; nếu code tool bị crash `AttributeError` khi repo không có license (`"license": null`), quên truyền `params={"per_page": max_releases}` lên API, hoặc vẫn gửi HTTP request khi `repo` là URL/`@` thì eval vẫn chấm PASS nếu chỉ xét tool call của model — chỉ unit test offline mới bắt được các lỗi cài đặt này.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7; `starter_v0/artifacts/system_prompt_local.md`, `starter_v0/artifacts/tools_local.yaml`, `starter_v0/runs/v3-qwen*`, `v4-local-*`, `v5-local-*`, `starter_v0/analysis/local_runs.csv` | 2 model local (`qwen3.5:2b`, `qwen3:4b`) chạy base eval, 2 vòng tối ưu `v4-local`, `v5-local`, kiểm tra ngược trên cloud | Prompt/tools local để ở file riêng, không sửa bản v3 của cloud; ví dụ few-shot không chép câu trong eval |

Các bonus còn lại (hơn 3 tool mới, gửi Telegram thật, test challenge) nhóm không làm.

### B7. Small Local Model Challenge (bonus)

Chạy qua Ollama trên laptop RTX 3070 8 GB, `data/eval_base.json` (20 case). Mọi run hợp lệ (`provider_error_cases == 0`, `measured_cases == 20`), log trong `version_log.csv`.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---:|---:|---:|---:|---|
| v3 | gpt-4o-mini (openrouter) | v3 | 0.90 | 0.95 | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20261110T194947018823.json` |
| v3-qwen35-2b | qwen3.5:2b (ollama) | v3 | 0.70 | 0.70 | 0.70 | 0.50 | `runs/v3-qwen35-2b_B_base_ollama_20261111T094827593514.json` |
| v3-qwen3-4b | qwen3:4b (ollama) | v3 | 0.90 | 0.95 | 0.90 | 0.83 | `runs/v3-qwen3-4b_B_base_ollama_20261111T095304240932.json` |
| v4-local-qwen352b | qwen3.5:2b (ollama) | v3 prompt + `tools_local.yaml` | 0.75 | 0.75 | 0.75 | 0.67 | `runs/v4-local-qwen352b_B_base_ollama_20261111T095555672444.json` |
| v4-local-qwen34b | qwen3:4b (ollama) | v3 prompt + `tools_local.yaml` | 0.85 | 0.90 | 0.85 | 0.83 | `runs/v4-local-qwen34b_B_base_ollama_20261111T100213668766.json` |
| v5-local-qwen352b | qwen3.5:2b (ollama) | `system_prompt_local.md` + `tools_local.yaml` | 0.75 | 0.75 | 0.75 | 0.67 | `runs/v5-local-qwen352b_B_base_ollama_20261111T100430322553.json` |
| v5-local-qwen34b | qwen3:4b (ollama) | `system_prompt_local.md` + `tools_local.yaml` | **0.95** | 1.00 | 0.95 | 1.00 | `runs/v5-local-qwen34b_B_base_ollama_20261111T101002354286.json` |
| v5-local-cloud | gpt-4o-mini (openrouter) | `system_prompt_local.md` + `tools_local.yaml` | 0.90 | 0.95 | 0.90 | 1.00 | `runs/v5-local-cloud_B_base_openrouter_20261111T101137901676.json` |

Giả thuyết từng vòng: **v4-local** chỉ sửa `tools_local.yaml` — đưa quy tắc từ khóa routing lên đầu mô tả `lookup`/`social_search` ("tin/tin tức/thời sự" → `lookup`; chỉ khi có chữ Twitter/X/tweet → `social_search`), vì baseline `qwen3.5:2b` chọn `social_search` cho 4 câu hỏi tin tức. **v5-local** giữ tools v4, thêm vào `system_prompt_local.md` quy định "luôn gọi tool qua function-calling, không viết JSON trong text" và 4 ví dụ few-shot (thiếu link → `clarify`, đã đủ thông tin → gọi tool luôn, tin → `lookup`, X → `social_search`).

Lỗi đặc thù của model nhỏ (đếm từ run JSON, số case FAIL; `analysis/local_runs.csv`):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool | 2B: 4 → 1 → 1 (v3 → v4 → v5); 4B: 0 | `R03`: 2B gọi `social_search(query="AI")` cho "Tin tức AI hôm nay" | v4: rule từ khóa ở đầu description | **Có** — sửa `R03`, `R06`, `M02`; còn `M06` ("Bỏ Twitter, chuyển sang web") |
| invalid JSON args (`_invalid_json_arguments`) | 0 ở mọi run local | — | — | Không gặp |
| no tool call / answered directly | 2B: 1 → 4 → 3; 4B: 1 → 1 → 0 | `M05` (4B v3): đúng tool + args nhưng in `{"function": "timeline", ...}` ra text; `R11` (2B): hỏi lại link bằng text | v5: quy định "luôn function-calling" + few-shot | **Có với 4B** (`M05` sửa ở v5); **không với 2B** (vẫn hỏi lại bằng text ở `R10`, `R11`, `R12`) |
| missed `clarify` | 2B: 1 → 3 → 3; cloud v5: 1 | `R10` (2B v5): hỏi "bạn muốn tóm tắt tweet của ai" bằng text thay vì gọi `clarify` | v5 few-shot thiếu link/thiếu tài khoản → `clarify` | Không với 2B |
| repeated / unnecessary calls | 2B v3: `M01` clarify thừa; 2B v5: `M05` clarify thừa; 4B v4: `R14` gọi `format` cho yêu cầu viết code; cloud v5: `R10` gọi `timeline` 3 lần | cloud v5 `R10`: `timeline(elonmusk)`, `timeline(satyanadella)`, `timeline(tim_cook)` | — | Few-shot gây hại trên cloud (xem dưới) |

- **Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?** Với `qwen3:4b`, quy định "luôn gọi tool qua function-calling" + few-shot ở v5 là bước hiệu quả nhất: 0.85 → **0.95** (`M05` hết bị in JSON ra text), cao hơn cả cloud v3 (0.90). Với `qwen3.5:2b`, rule từ khóa trong description (v4) là thứ duy nhất có tác dụng: lỗi chọn sai tool 4 → 1, case_accuracy 0.70 → 0.75; few-shot v5 không giúp thêm vì model 2B vẫn có xu hướng hỏi lại bằng text thay vì gọi `clarify`.
- **Chưa phải mọi thay đổi đều tốt:** v4 làm `qwen3:4b` tụt 0.90 → 0.85 (`R14` gọi `format` cho yêu cầu viết code — case không liên quan tới phần đã sửa, nhiều khả năng do dao động của model), và v4 làm 2B hỏi lại bằng text nhiều hơn (1 → 4 case "no tool call").
- **Bản prompt tối ưu cho local chạy trên model cloud thì sao?** `v5-local-cloud` giữ nguyên 0.90 như v3, nhưng đổi kiểu lỗi: `R10` ("Tóm tắt 5 tweet mới nhất") thay vì hỏi lại thì gọi `timeline` cho `elonmusk`, `satyanadella`, `tim_cook` — `satyanadella` chính là handle trong ví dụ few-shot. Model cloud "chép" ví dụ few-shot vào đáp án, nên few-shot cho model nhỏ có thể gây rò rỉ ví dụ trên model lớn; không có một bản prompt nào tốt hơn hẳn cho cả hai.
- **Khi nào nhóm sẽ chọn model local thay vì cloud?** Khi cần chạy offline, không tốn phí API, hoặc dữ liệu không được rời máy (vd tra `policy` nội bộ). Theo số liệu, `qwen3:4b` + prompt/tools local (0.95) đủ dùng cho routing của agent này; model 2B (0.75) chưa đủ tin cậy cho các case cần `clarify` hoặc xác nhận trước khi `send`. Run local nhanh trên GPU 8 GB: ~2 phút (2B) và ~5 phút (4B) cho 20 case.

---

## 5. Khó khăn và cách xử lý

1. **GitHub API rate limit (HTTP 403) khi test tool mới `github_repo`:**
   - Khi chạy live kiểm thử tool `github_repo` trên Wi-Fi lớp học dùng chung IP, GitHub API trả về lỗi `HTTPError 403 rate limit exceeded` (do giới hạn 60 request/giờ cho IP ẩn danh).
   - *Cách xử lý:* Bọc an toàn lỗi HTTP trả về dict dạng `{'tool': 'github_repo', 'error': 'HTTPError', ...}` thay vì để exception làm sập agent; hỗ trợ thêm biến `GITHUB_TOKEN` trong file `.env` khi chạy live; và viết 100% unit test offline qua `monkeypatch`/`fake_http` để không phụ thuộc mạng thật.
   - *Bằng chứng:* kết quả smoke test live ghi ở mục 4 báo cáo `report/team/2A202603808_HoangQuangDat.md`; nhánh lỗi được kiểm bằng `test_github_repo_http_error_or_timeout_returns_error_dict` trong `starter_v0/tests/test_tools_todo.py`.
2. **Lỗi lệch hash artifact do line ending trên Windows:**
   - Trên môi trường Windows với cấu hình git mặc định (`core.autocrlf=true`), các file `system_prompt.md` và `tools.yaml` bị checkout thành ký tự xuống dòng CRLF (`\r\n`), dẫn đến giá trị băm `prompt_hash` và `tools_hash` bị sai lệch hoàn toàn so với hash chuẩn của v3 dù nội dung giống hệt.
   - *Cách xử lý:* Thêm file `.gitattributes` ở thư mục gốc repo ép buộc `text eol=lf` cho toàn bộ thư mục `starter_v0/artifacts/`, sau đó checkout lại file để chuẩn hóa đúng mã hash `v3+p5dd5a04cdce4+t6c5c91c5db73`.
3. **Mạng ngoài bị timeout ở API arXiv (Case G05):**
   - Trong quá trình eval nhóm ở case G05, lệnh gọi `papers` tới `export.arxiv.org` bị `ReadTimeout`. Nhờ cơ chế bọc lỗi `err()` trong starter nên eval vẫn hoàn thành và đo lường thành công tham số của model mà không bị crash luồng đánh giá.
4. **Hỏng định dạng file `version_log.csv` khi chỉnh sửa bằng Excel:**
   - Khi mở và lưu bằng Microsoft Excel, file CSV bị bọc thừa dấu ngoặc kép `"""` và tạo ra 13 dòng trống ở cuối làm gãy script parse log. Nhóm đã kịp thời kiểm tra bằng `git diff` và viết lại chuẩn định dạng RFC 4180 bằng text editor.
   - *Bằng chứng:* bản lỗi ở commit `8d52781` (16 dòng, 13 dòng trống), bản đã sửa ở commit `f96a68c` (header + 4 dòng v0–v3).
5. **Độ dao động tự nhiên của mô hình:**
   - Cùng một prompt và hash ở bản v0 nhưng khi gọi qua API OpenRouter có 2 run đạt 0.65 và 1 run đạt 0.70 (chi tiết và tên file ở ghi chú B1). Nhóm đã thống nhất chỉ ghi nhận những lần chạy đầy đủ không có lỗi provider (`provider_error_cases == 0`) và lưu trữ run JSON minh chứng rõ ràng; các run dư được dọn khỏi `runs/` nhưng vẫn truy lại được trong lịch sử git (commit `fabccdb`).

---

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Loại bỏ hoàn toàn 3 chỉ dẫn xấu của bản starter (ép model gọi tool trong 1 bước duy nhất, xúi giục tự đoán username/URL, và tự ý gọi tool `send` khi chưa hỏi user).
  - Bổ sung quy tắc phạm vi nghiêm ngặt: khi người dùng hỏi các nội dung ngoài phạm vi nghiên cứu (toán học, code, dịch vụ đời sống) thì trả lời thẳng bằng kiến thức có sẵn hoặc từ chối lịch sự, không được gọi tool linh tinh (`no_tool`).
  - Thiết lập ranh giới an toàn cho các tool có tác dụng phụ (`send` bắt buộc phải có bước xác nhận rõ ràng).
  - Thêm quy tắc xử lý khi thiếu thông tin: bắt buộc gọi `clarify` để hỏi lại user thay vì tự bịa đặt tham số.
- **Fix nào thuộc `tools.yaml`?**
  - Viết lại phần mô tả (description) bằng tiếng Việt mạch lạc, nêu rõ *khi nào nên dùng và khi nào không nên dùng* cho cả 11 tools.
  - Phân định rõ ràng ranh giới giữa `lookup` (tìm bài viết, tin tức trên Web) và `social_search` (tìm bài đăng ngắn trên mạng xã hội Twitter).
  - Quy ước chuẩn hóa tham số: `query` của `lookup` chỉ chứa thực thể/chủ đề chính (không lặp lại chữ "news", "tin tức"), muốn lọc tin tức thì truyền `topic="news"`; tham số `screenname` của Twitter không được chứa ký tự `@`; tham số `confirmed=true` của `send` chỉ bật khi user đồng ý.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Case `R12` (xác nhận trước khi gửi): ở v3 agent đã dừng lại và gọi `clarify` thay vì tự `send` (đúng về an toàn), nhưng đặt `response_type="text"` thay vì `"yes_no"` nên bị chấm FAIL — cần người xem lại để phân biệt "sai ranh giới" với "sai kiểu câu hỏi".
  - Live chat (`transcripts/v3_openrouter_20261110T202251172175.transcript.json`, lượt 2 và 5): không bị ép gọi tool nên agent hỏi lại link / hỏi xác nhận bằng text thường thay vì gọi `clarify`. Hành vi an toàn đúng nhưng nếu chấm tự động theo tool call thì sẽ không ghi nhận được — loại này cần review thủ công.
  - Case `GM03`: User yêu cầu tìm tweet của "Anthropic", model gọi `timeline(screenname="Anthropic")` thay vì `AnthropicAI`. Về mặt ngữ nghĩa, model đã routing đúng tool nhưng không biết handle thực tế của công ty trên nền tảng mạng xã hội.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - *Giả thuyết 1 (Sửa G04 - `policy`):* Bổ sung tài liệu đặc tả các giá trị enum của `policy_area` trong `tools.yaml` (nêu rõ `tool_usage` chứa quy định về rate limit, chọn tool và quyền gọi API).
  - *Giả thuyết 2 (Sửa G05 - `papers`):* Bổ sung quy ước trong mô tả tool `papers`: khi user yêu cầu "mới nhất" thì mặc định gán `sort_by="submittedDate"`.
  - *Giả thuyết 3 (Sửa GM03 - `timeline`):* Bổ sung hướng dẫn trong `system_prompt.md`: khi không chắc chắn 100% handle Twitter chính thức của một tổ chức, agent phải gọi `clarify` để xác nhận handle thay vì đoán mò.
  - *Giả thuyết 4 (Sửa GM05 - out of scope):* Mở rộng danh mục các câu hỏi ngoài phạm vi trong system prompt (bao gồm đặt vé máy bay, thương mại điện tử, dịch vụ cá nhân) để agent từ chối ngay cả trong ngữ cảnh multi-turn kéo dài.
  - *Giả thuyết 5 (Sửa R10 bị tụt ở v3 - `social_search`):* Với câu "Tóm tắt 5 tweet mới nhất giúp mình", model v3 gọi `social_search(query="tweet")` — mô tả mới chỉ cấm `query` rỗng nên model điền chữ chung chung "tweet". Thử ghi rõ trong `tools.yaml`: `query` phải là chủ đề lấy từ câu của user, không dùng từ chung như "tweet"/"bài đăng"; nếu user không nêu cả tài khoản lẫn chủ đề thì gọi `clarify`.

---

## 8. Tài liệu tham khảo

1. Tài liệu hướng dẫn thực hành Lab Day 03: *Prompt Engineering & Tool Calling* (VinUni / AI Course).
2. Tài liệu chính thức Streamlit: [Streamlit Chat Elements & Session State Documentation](https://docs.streamlit.io/develop/api-reference/chat).
3. Tài liệu Cloudflare Tunnel: [Cloudflare Zero Trust Documentation - TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/).
4. GitHub REST API Documentation: [Repositories & Releases API Reference](https://docs.github.com/en/rest/repos).
