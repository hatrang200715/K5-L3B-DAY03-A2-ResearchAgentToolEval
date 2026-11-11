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
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

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

Run: [`starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json`](../../starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json) — `v3+p29a0e3cdc49c+t2b0b1d3ae07e`, model `openai/gpt-4o-mini`, `measured_cases=10`, `provider_error_cases=0`. Kết quả: **8/10 PASS** (case_accuracy 0.8, tool_routing 0.9, argument 0.8, multiturn 0.8).

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

Ghi chú: bộ group hiện **chưa có case route tới tool mới** của nhóm vì 4 tool mới (`hn_search`, `reading_time`, `extract_links`, `dedupe_items`) chưa được khai báo trong `artifacts/tools.yaml` của v3; contract test và `run_eval.py` sẽ báo lỗi nếu case nhắc tới tool chưa khai báo.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output: **102 passed, 0 failed, 0 skipped**; [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) (commit `af8bcb8`) | Điền hết 14 stub tool có sẵn (clarify, format ×3, send ×2, lookup, fetch ×2, timeline, social_search, policy ×3); tìm và sửa 4 bug trong tool có sẵn, mỗi bug có regression test | Test chạy offline, HTTP mock bằng `fake_http`; mỗi test assert cả request gửi đi lẫn kết quả trả về |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

| # | Tool | Input biên | Hành vi cũ | Sửa | Regression test |
|---|---|---|---|---|---|
| 1 | `send` | `confirmed="false"` (chuỗi) | **Vẫn gửi thật lên Telegram** — chuỗi khác rỗng là truthy, thủng guardrail xác nhận | Chỉ chấp nhận `confirmed is True` | `test_send_non_boolean_confirmed_does_not_send` |
| 2 | `format` | `items=["chuỗi", ...]` | Raise `AttributeError` (vi phạm quy ước trả error dict) | Bỏ qua item không phải dict | `test_format_skips_non_dict_items_instead_of_raising` |
| 3 | `format` | item không có url/source | Dòng thừa `" - "` ở cuối | Bỏ separator khi không có nguồn | `test_format_item_without_source_has_no_dangling_dash` |
| 4 | `timeline`, `social_search` | `limit=-1` | `items[:-1]` → trả 19/20 tweet | `limit <= 0` → dùng mặc định 5 | `test_tweet_tools_negative_limit_falls_back_to_default` |

Kiểm chứng: chạy các regression test trên code gốc → failed; sau khi sửa → pass.

Ví dụ lỗi unit test bắt được mà eval không bắt được: bug #1. Eval chỉ chấm model có gọi `send(confirmed=true)` đúng lúc hay không; nếu model truyền `confirmed="false"` thì eval chỉ báo `wrong_arg_value`, nhưng **tool vẫn gửi tin thật**. Chỉ unit test (assert không có POST nào đi ra) mới phát hiện được.

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

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
