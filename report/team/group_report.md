# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: A2
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:
  - Provider: OpenRouter
  - Model: `openai/gpt-4o-mini`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent hỗ trợ tìm tin web và bài đăng mạng xã hội, đọc URL/bài báo đã biết, tìm bài nghiên cứu, rồi tổng hợp kết quả thành digest. Agent hỏi lại khi thiếu thông tin; chỉ gửi nội dung lên Telegram sau khi người dùng xác nhận rõ nội dung và đích gửi.

**Cách chạy UI:**

Từ thư mục `starter_v0/`, chạy `python -m streamlit run app.py`. Dependency UI là `streamlit`, đã khai báo trong [requirements.txt](../../starter_v0/requirements.txt); mã UI ở [app.py](../../starter_v0/app.py).

**Link dùng thử (deploy):**

Chưa có URL public/deploy được lưu làm bằng chứng. Chạy UI local tại `http://localhost:8501`.

### A2. Tool agent có

Danh sách dưới đây là cấu hình hiện có trong [tools.yaml](../../starter_v0/artifacts/tools.yaml). Bốn tool mới được thêm sau lần chạy eval v3; xem ghi chú B3.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi người dùng để bổ sung thông tin hoặc xác nhận trước hành động bên ngoài | Không |
| `timeline` | Lấy bài đăng gần đây từ một tài khoản mạng xã hội cụ thể | Không |
| `social_search` | Tìm bài đăng mạng xã hội theo chủ đề | Không |
| `lookup` | Tìm kiếm web, gồm tin tức hiện thời | Không |
| `fetch` | Đọc/tóm tắt nội dung từ URL đã biết | Không |
| `format` | Định dạng các kết quả đã thu thập thành digest/bài đăng | Không |
| `send` | Gửi nội dung lên Telegram sau khi người dùng xác nhận | Không |
| `policy` | Tìm nội dung trong tài liệu chính sách nội bộ | Không |
| `papers` | Tìm bài nghiên cứu trên arXiv | Không |
| `paper_text` | Trích xuất nội dung từ bài arXiv đã biết | Không |
| `hn_search` | Tìm bài và thảo luận trên Hacker News | Có |
| `reading_time` | Đếm từ/ký tự và ước tính thời gian đọc văn bản đã có | Có |
| `extract_links` | Trích URL http(s) từ văn bản, giữ thứ tự và bỏ trùng | Có |
| `dedupe_items` | Loại kết quả trùng theo URL chuẩn hóa hoặc tiêu đề | Có |

### A3. Câu hỏi mẫu để thử

1. “Hôm nay có tin gì mới về AI giải toán olympiad?”
2. “Tìm 3 bài trên Hacker News về AI agents.”
3. “Đọc giúp mình mấy tweet gần đây của anh ấy.” (Agent cần hỏi rõ tài khoản.)
4. “Trích tất cả đường link từ đoạn này: OpenAI https://openai.com và Python https://python.org.”
5. “Đăng bản tin AI ngày 10/11 lên Telegram.” (Agent phải hỏi xác nhận trước khi gửi.)

## 3. Giải pháp

Vòng tối ưu được ghi trong [version_log.csv](../../starter_v0/artifacts/version_log.csv):

- v1 sửa [system_prompt.md](../../starter_v0/artifacts/system_prompt.md), bỏ chỉ dẫn starter ép đoán thông tin/luôn gọi tool; giả thuyết là giảm tool call sai và giữ lại yêu cầu cần làm rõ.
- v2 tiếp tục prompt để hỏi khi thiếu dữ kiện và yêu cầu xác nhận `yes_no` trước khi gửi.
- v3 sửa mô tả và quy ước đối số trong [tools.yaml](../../starter_v0/artifacts/tools.yaml), phân biệt điều kiện dùng/không dùng của các tool, đồng thời nhấn mạnh giữ ngữ cảnh khi follow-up.
- Vai B bổ sung `hn_search` (tìm bài Hacker News), `reading_time` (đo độ dài/thời gian đọc), `extract_links` (trích URL) và `dedupe_items` (lọc kết quả trùng). Mô tả YAML nêu rõ lúc nên/không nên gọi; bốn tool này được merge sau run v3 và chưa được đánh giá trong run đó.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Các run dưới đây đều có `provider_error_cases=0` và `measured_cases=total_cases=20`; metric là `case_accuracy` trên bộ base. Bảng đối chiếu với [version_log.csv](../../starter_v0/artifacts/version_log.csv).

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline | Đo hành vi trước khi chỉnh prompt/tool | — | 0.70 (14/20) | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T190337373441.json) |
| v1 | `system_prompt.md` | Bỏ chỉ dẫn ép đoán/luôn gọi tool để giảm tool call sai | 0.70 | 0.85 (17/20) | [v1 run](../../starter_v0/runs/v1_B_base_openrouter_20261110T194813949044.json) |
| v2 | `system_prompt.md` | Làm rõ hỏi lại khi thiếu thông tin và xác nhận trước khi gửi | 0.85 | 0.80 (16/20) | [v2 run](../../starter_v0/runs/v2_B_base_openrouter_20261110T195208668669.json) |
| v3 | `tools.yaml` | Làm rõ routing, convention đối số và giữ ngữ cảnh follow-up | 0.80 | 0.90 (18/20) | [v3 run](../../starter_v0/runs/v3_B_base_openrouter_20261110T195528905010.json) |

### B2. Failure Analysis

Các lỗi dưới đây là toàn bộ case FAIL của baseline hợp lệ [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T190337373441.json). Hướng sửa ở cột cuối được kiểm tra lại qua các version sau; một số lỗi boundary vẫn còn ở v3.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R08_out_of_scope` | `out_of_scope` | `send(text=...)` | Yêu cầu giải bài toán bị xử lý như nội dung để gửi, thay vì từ chối ngoài phạm vi | Sửa prompt: giới hạn khả năng, không dùng action tool để trả lời yêu cầu ngoài phạm vi |
| `R10_missing_handle` | `missing_info` | `timeline(screenname=sama)` | Đoán tài khoản khi user chưa nêu người cần xem | Yêu cầu `clarify` khi thiếu/không rõ tài khoản; thêm quy tắc vào mô tả `timeline` |
| `R11_missing_url` | `missing_info` | `fetch(url=https://example.com/article)` | Bịa URL thay vì hỏi URL cần đọc | Prompt và mô tả `fetch`: chỉ dùng URL đã được cung cấp/thu thập, không đoán |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text=...)` | Gọi gửi khi chưa có xác nhận | Bắt buộc hỏi xác nhận trước send; ở v3 lỗi này còn tái diễn dưới dạng `clarify(response_type=text)` thay vì `yes_no` |
| `R13_parallel_web_and_tweets` | `wrong_arg_value` | `lookup(query="AI news", timeframe=day)` và `social_search(query=AI, ...)` | `lookup` thiếu `topic=news` và nhồi “news” vào `query` | Làm rõ `topic=news` và tách chủ đề/thời gian trong schema và mô tả `lookup` |
| `R14_out_of_scope_coding` | `out_of_scope` | `send(text=<mã Fibonacci>)` | Yêu cầu viết code bị xử lý nhầm thành nội dung gửi | Làm rõ ranh giới research và không gọi tool ngoài mục đích của nó |

### B3. Team Eval Cases

Có đúng 10 case trong [eval_group.json](../../starter_v0/data/eval_group.json): 5 single-turn và 5 multi-turn.

Run: [v3 group run](../../starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json) — `v3+p29a0e3cdc49c+t2b0b1d3ae07e`, model `openai/gpt-4o-mini`, `measured_cases=10`, `provider_error_cases=0`. Kết quả: **8/10 PASS** (case_accuracy 0.8, tool_routing 0.9, argument 0.8, multiturn 0.8).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_math_news_is_in_scope | Câu có chữ "toán" nhưng là hỏi tin tức → vẫn là research, không từ chối | `lookup(topic=news, timeframe=day)` | PASS |
| G02_thanks_no_tool | Câu xã giao kết thúc hội thoại → không gọi tool | `no_tool` (answer_without_tool) | PASS |
| G03_missing_pronoun_handle | Chỉ có "anh ấy", không có tên/handle → hỏi lại, không đoán | `clarify(response_type=text)` | PASS |
| G04_out_of_scope_booking | Đặt vé máy bay (ngoài phạm vi research) → từ chối | `no_tool` (refuse) | **FAIL** — gọi `clarify` hỏi giờ bay thay vì từ chối (`out_of_scope` / `unexpected_tool_call`) |
| G05_timeframe_month | "tháng này" → `timeframe=month` (base chỉ phủ day/week) | `lookup(topic=news, timeframe=month)` | PASS |
| GM01_switch_timeline_to_search | Multi-turn: chuyển từ bài CỦA một người sang bài VỀ chủ đề | `social_search(search_type=Top)` | PASS |
| GM02_send_after_confirmation | Multi-turn: user đã xác nhận rõ → gửi, không hỏi lại vô hạn | `send(confirmed=true)` | PASS |
| GM03_correction_search_type | Multi-turn: sửa Latest → Top giữa chừng, giữ query | `social_search(query=Gemini, search_type=Top)` | PASS |
| GM04_clarify_then_handle | Multi-turn: bổ sung tên "Yann LeCun" ở lượt sau → map đúng handle, `limit=5` | `timeline(screenname=ylecun, limit=5)` | **FAIL** — `screenname="yannlecun"` (đoán sai handle; `limit` đúng) |
| GM05_reconfirm_after_edit | Multi-turn: user sửa nội dung nhưng chưa xác nhận bản mới → hỏi lại, không send | `clarify(response_type=yes_no)` | PASS |

Nhận xét 2 case FAIL:
- **G04**: lỗi thật của model — không nhận ra yêu cầu nằm ngoài khả năng của agent, hỏi thêm chi tiết như thể sẽ làm được. Hướng sửa thuộc `system_prompt.md`: rule "yêu cầu hành động ngoài research (đặt vé, mua hàng…) → từ chối ngắn gọn, không gọi tool".
- **GM04**: model hiểu đúng ngữ cảnh multi-turn (đúng tool `timeline`, đúng `limit=5`) nhưng tự đoán handle từ tên người. Case này phụ thuộc vào việc model có thuộc handle hay không → cần review thủ công; hành vi an toàn hơn là hỏi lại handle hoặc tra cứu trước.

**Lưu ý về phạm vi run:** run group được tạo lúc 10:09; bốn tool mới được merge vào [tools.yaml](../../starter_v0/artifacts/tools.yaml) sau đó (commit `e997898`, 10:33). Hash tool của run (`t2b0b1d3ae07e`) khác hash cấu hình hiện tại (`8b01c4391d65`), nên 8/10 không đo routing đến tool mới. Cần thêm ít nhất một eval case cho tool mới và chạy lại suite group để đánh giá chúng.

`PASS` ở đây đo việc model chọn tool/đối số đúng, không đảm bảo API ngoài chạy thành công. Trong run này, tool results báo thiếu `TAVILY_API_KEY` cho `lookup`, `RAPIDAPI_KEY` cho `social_search`/`timeline`, và `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` cho `send`. Vì vậy run hợp lệ về provider/eval theo rubric nhưng không phải bằng chứng các tích hợp ngoài đã chạy thành công.

### B4. Live Chat Evidence

Các transcript dưới đây được lưu tại [transcripts/](../../starter_v0/transcripts/). Hai transcript v3 chỉ có 2 lượt user mỗi file; không có transcript nào chứng minh đủ luồng live gồm yêu cầu thường, clarify rồi bổ sung thông tin và send sau xác nhận.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1–3 | `hello`; `what can you do`; hỏi tin AI hôm nay | Không gọi tool ở hai lượt đầu; lượt 3 gọi `lookup(topic=news, timeframe=day)` | [v0 transcript](../../starter_v0/transcripts/v0_openrouter_20261110T190823508339.transcript.json), `openrouter/free`; artifact hash không khớp baseline trong version log | Có câu trả lời và kết quả tìm tin; transcript có 3 lượt nhưng không phải bằng chứng v3 |
| 1–2 | `hi`; tìm 3 bài Hacker News về AI agents | `hn_search(query="AI agents", limit=3)` | [v3 transcript](../../starter_v0/transcripts/v3_openrouter_20261111T104130996385.transcript.json), `openrouter/free`; hash prompt/tools cũ, trước cấu hình v3 đã log | Có gọi tool mới; transcript không chứng minh phiên bản eval v3 |
| 1–2 | Trích link trong văn bản; ước tính thời gian đọc một đoạn | `extract_links(...)`; `reading_time(...)` | [v3 transcript](../../starter_v0/transcripts/v3_openrouter_20261111T104444114723.transcript.json), `openrouter/free`; hash prompt/tools cũ | Transcript ghi nhận trích link và kết quả ước tính ~1 phút |
| — | Transcript v0 ngày 11/11 không có lượt chat | Không có | [transcript rỗng](../../starter_v0/transcripts/v0_openrouter_20261111T103858219524.transcript.json) | Không dùng làm bằng chứng kết quả |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | [hn_search](../../starter_v0/tools/hn_search/TOOL.md), [reading_time](../../starter_v0/tools/reading_time/TOOL.md), [extract_links](../../starter_v0/tools/extract_links/TOOL.md), [dedupe_items](../../starter_v0/tools/dedupe_items/TOOL.md), [NEW_TOOLS_FOR_A.yaml](../../starter_v0/tools/NEW_TOOLS_FOR_A.yaml) | Bốn tool đã có code, `TOOL.md`, đăng ký và khai báo YAML; ba tool local, một tool gọi Hacker News Algolia API | `hn_search` phụ thuộc API ngoài; eval nhóm chưa route tới tool mới, cần bổ sung case và chạy lại |
| Unit test tool mới (≥ 3 test/tool) | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py) | 14 test cho 4 tool mới; cả suite hiện chạy **122 passed, 0 failed, 0 skipped** | Test tool gọi API dùng HTTP mock/offline; không thay thế eval khả năng model chọn tool |
| UI (lệnh chạy + link dùng thử) | [app.py](../../starter_v0/app.py), [requirements.txt](../../starter_v0/requirements.txt), commit `7daa3e0` | UI Streamlit chat nhiều lượt, hiển thị tool calls/results/lỗi; chạy bằng `cd starter_v0 && python -m streamlit run app.py` | Chưa có link deploy công khai; link local là `http://localhost:8501` |

Ví dụ lỗi unit test bắt được mà eval routing không bắt được: `send(confirmed="false")`. Chuỗi `"false"` là truthy trong Python nên code lỗi cũ vẫn gửi request Telegram; regression test `test_send_non_boolean_confirmed_does_not_send` kiểm tra request không được gửi. Eval chỉ phát hiện đối số sai, không thể đảm bảo guardrail trong code tool.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | Xem B7 | Chưa thực hiện; không có run model local trong repo | Không có bằng chứng |
| Hơn 3 tool mới (≥ 4) | Bốn thư mục tool ở B5a và [tools.yaml](../../starter_v0/artifacts/tools.yaml) | Đã viết 4 tool và 14 test; tuy nhiên eval group hiện không có case route tới tool mới | Chưa đủ bằng chứng eval theo rubric; cần thêm case và chạy lại |
| `send` gửi thật lên Telegram sau xác nhận | Không có transcript xác nhận gửi thật | Chưa có bằng chứng gửi thành công sau xác nhận | Không khẳng định đã gửi; run group ghi thiếu Telegram credentials |
| Test challenge (0 skipped / regression test) | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), commit `af8bcb8`; chạy hiện tại: **122 passed, 0 failed, 0 skipped** | Hoàn tất 14 stub test tool có sẵn; tìm và sửa 4 bug ở `send`, `format` (2 lỗi), `timeline`/`social_search`, mỗi bug có regression test | Test chạy offline với HTTP mock; assert request và kết quả trả về |

Bốn bug tìm được trong tool có sẵn và regression test tương ứng:

| # | Tool | Input biên | Hành vi cũ | Sửa | Regression test |
|---|---|---|---|---|---|
| 1 | `send` | `confirmed="false"` (chuỗi) | **Vẫn gửi thật lên Telegram** — chuỗi khác rỗng là truthy, thủng guardrail xác nhận | Chỉ chấp nhận `confirmed is True` | `test_send_non_boolean_confirmed_does_not_send` |
| 2 | `format` | `items=["chuỗi", ...]` | Raise `AttributeError` (vi phạm quy ước trả error dict) | Bỏ qua item không phải dict | `test_format_skips_non_dict_items_instead_of_raising` |
| 3 | `format` | item không có url/source | Dòng thừa `" - "` ở cuối | Bỏ separator khi không có nguồn | `test_format_item_without_source_has_no_dangling_dash` |
| 4 | `timeline`, `social_search` | `limit=-1` | `items[:-1]` → trả 19/20 tweet | `limit <= 0` → dùng mặc định 5 | `test_tweet_tools_negative_limit_falls_back_to_default` |

Kiểm chứng: chạy các regression test trên code gốc → failed; sau khi sửa → pass.

### B7. Small Local Model Challenge (bonus)

Nhóm chưa thực hiện thử thách model local; không có model Ollama, run, hoặc số liệu lỗi local để báo cáo. Không có so sánh cloud/local.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| N/A | Chưa chạy | N/A | N/A | N/A | N/A | N/A | Không có |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| Không có run local để phân tích | N/A | N/A | N/A | N/A |

- Chưa có bằng chứng để trả lời các câu hỏi về tối ưu model local.

## 5. Khó khăn và cách xử lý

- v2 giảm từ 0.85 xuống 0.80 dù giả thuyết cải thiện boundary; nhóm giữ nguyên số liệu và tiếp tục kiểm tra thay vì bỏ run. v3 tăng base accuracy lên 0.90, nhưng lỗi xác nhận send vẫn còn.
- Một lần chạy group hợp lệ về provider nhưng các tool tích hợp báo thiếu `TAVILY_API_KEY`, `RAPIDAPI_KEY` và Telegram credentials (chi tiết trong run group ở B3). Vì thế không coi PASS của model là xác nhận các API/tool ngoài đã hoạt động.
- Có bốn tool mới, nhưng run group được tạo trước khi các khai báo YAML của chúng được merge. Nhóm chưa chạy lại group sau merge nên chưa có bằng chứng eval routing cho các tool này.
- Một transcript ban đầu trên Windows có artifact hash khác do khác biệt line ending; nhóm Tester ghi nhận đã chỉnh line ending và chạy lại. Transcript cũ không được dùng làm bằng chứng khớp version log; xem ghi chú trong báo cáo của [Phùng Thị Nhài](2A202603725_PhungThiNhai.md).

## 6. Tổng hợp đóng góp

| Thành viên | Vai trò/đóng góp chính | Bằng chứng |
|---|---|---|
| Lương Thị Hồng Hạnh | Vai A, nhóm trưởng/eval lead: setup, tối ưu prompt v0–v3, cập nhật version log và tích hợp khai báo tool | [version_log.csv](../../starter_v0/artifacts/version_log.csv), commit `f22fa9a`, `e997898`; [báo cáo cá nhân](2A202603748_LuongThiHongHanh.md) |
| Phùng Văn Thanh Cao | Vai B: xây 4 tool mới, viết 14 unit test và block YAML | [báo cáo cá nhân](2A202603741_PhungVanThanhCao.md), commit `56fd688`; các file tool ở B5a |
| Phùng Thị Nhài | Vai C: tạo 10 eval case nhóm, hoàn tất 14 stub test, tìm/sửa 4 bug tool kèm regression test, chạy group eval | [eval_group.json](../../starter_v0/data/eval_group.json), [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), commit `af8bcb8`; [báo cáo cá nhân](2A202603725_PhungThiNhai.md) |
| Vũ Quang Huy | Vai D: xây Streamlit UI và ghi transcript chat live | [app.py](../../starter_v0/app.py), commit `7daa3e0`, [transcripts/](../../starter_v0/transcripts/); [báo cáo cá nhân](2A202603782_VuQuangHuy.md) |

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Thuộc `system_prompt.md`:** từ chối yêu cầu ngoài năng lực research thay vì hỏi thêm thông tin như thể agent có thể thực hiện; không bịa tài khoản/URL; hỏi xác nhận trước hành động gửi.
- **Thuộc `tools.yaml`:** làm rõ điều kiện dùng/không dùng, convention đối số (đặc biệt `topic=news` và `timeframe`), giữ query khi follow-up; quy định `clarify(response_type=yes_no)` cho mọi yêu cầu gửi. Lỗi group G04 và lỗi `R12` ở v3 cho thấy các ranh giới này vẫn cần làm rõ/đo lại.
- **Cần review thủ công:** map tên người thành handle, như `Yann LeCun` → `ylecun`. Đây là tri thức thực tế có thể thay đổi và run chỉ cho thấy model đoán sai `yannlecun`; nên hỏi lại hoặc kiểm tra nguồn đáng tin thay vì coi ánh xạ từ trí nhớ model là ground truth.
- **Vòng tiếp theo:** thêm case group định tuyến tới từng tool mới; bổ sung case từ chối booking, xác nhận send với nội dung còn thiếu/sửa đổi, và yêu cầu hỏi lại handle chưa rõ; sau đó chạy lại suite với credentials phù hợp và xác minh cả kết quả tool ngoài, không chỉ điểm routing.

## 8. Tài liệu tham khảo

- [README.md](../../README.md) — hướng dẫn lab và scope.
- [RUBRIC.md](../../RUBRIC.md) — tiêu chí đánh giá và điều kiện run hợp lệ.
- [starter_v0/README.md](../../starter_v0/README.md) — cách chạy eval, chat và test.
- Bằng chứng chính: [version log](../../starter_v0/artifacts/version_log.csv), [run files](../../starter_v0/runs/), [eval nhóm](../../starter_v0/data/eval_group.json), [transcripts](../../starter_v0/transcripts/).
