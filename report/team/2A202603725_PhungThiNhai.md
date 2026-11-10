# Báo cáo cá nhân — PhungThiNhai-2A202603725

## 1. Thông tin thành viên

- Họ tên: Phùng Thị Nhài
- MSSV: 2A202603725
- Email: nhaipt342k4@gmail.com
- Vai trong nhóm: **C — Tester** (xem [role/C-Tester.md](../../role/C-Tester.md))

## 2. Phần việc phụ trách

Đo agent theo 2 hướng:

- **Eval case** đo *model*: chọn đúng tool và args chưa → `starter_v0/data/eval_group.json`.
- **Unit test** đo *code tool*: nhận args đó thì chạy đúng chưa → 14 stub tool có sẵn trong `starter_v0/tests/test_tools_todo.py` + săn bug trong tool có sẵn.

## 3. Đóng góp cụ thể

### 3.1 Eval nhóm — 10 case (5 single + 5 multi turn)

| Case | Loại lỗi nhắm tới | Kiểm tra gì |
|---|---|---|
| G01_math_news_is_in_scope | wrong_tool | Câu có chữ "toán" nhưng là hỏi tin tức → vẫn research, gọi `lookup(topic=news, timeframe=day)` |
| G02_thanks_no_tool | unnecessary_tool | Câu xã giao → không gọi tool |
| G03_missing_pronoun_handle | missing_info | Chỉ có "anh ấy" → `clarify(text)`, không đoán |
| G04_out_of_scope_booking | out_of_scope | Đặt vé máy bay → không gọi tool |
| G05_timeframe_month | wrong_arg_value | "tháng này" → `timeframe=month` (base chỉ phủ day/week) |
| GM01_switch_timeline_to_search | wrong_tool | Hai tool gần nghĩa: chuyển từ `timeline` sang `social_search`, `search_type=Top` |
| GM02_send_after_confirmation | wrong_boundary | User đã xác nhận → `send(confirmed=true)` |
| GM03_correction_search_type | wrong_arg_value | Sửa Latest → Top giữa chừng, giữ query |
| GM04_clarify_then_handle | missing_info | Bổ sung tên ở lượt sau → map handle, `limit=5` |
| GM05_reconfirm_after_edit | wrong_boundary | User sửa nội dung nhưng chưa xác nhận bản mới → hỏi lại `yes_no`, không send |

Nguyên tắc viết `expect`: chỉ ghi key có đáp án duy nhất (handle, limit, topic, timeframe, search_type, confirmed), không ghi `query` dài để tránh FAIL oan.

Ghi chú: case route tới tool mới của B sẽ thay một case ở trên sau khi A merge tool mới vào `tools.yaml` (contract test quét `eval_group.json`, nhắc tool chưa khai báo sẽ làm pytest đỏ cả nhóm).

### 3.2 Unit test — 14 stub tool có sẵn

clarify ×1, format ×3, send ×2, lookup ×1, fetch ×2, timeline ×1, social_search ×1, policy ×3. Mỗi test assert cả **request gửi đi** (URL, params/json, header) lẫn **kết quả trả về**; HTTP mock bằng `fake_http`, chạy offline.

### 3.3 Săn bug — 4 bug trong tool có sẵn, mỗi bug có regression test

| # | Tool | Input biên | Hành vi cũ | Sửa | Regression test |
|---|---|---|---|---|---|
| 1 | `send` | `confirmed="false"` (chuỗi) | **Gửi thật lên Telegram** — chuỗi khác rỗng là truthy, thủng guardrail xác nhận | Chỉ chấp nhận `confirmed is True` | `test_send_non_boolean_confirmed_does_not_send` |
| 2 | `format` | `items=["chuỗi", ...]` | Raise `AttributeError` (vi phạm quy ước "trả error dict, không raise") | Bỏ qua item không phải dict | `test_format_skips_non_dict_items_instead_of_raising` |
| 3 | `format` | item không có url/source | Dòng thừa `" - "` ở cuối | Bỏ separator khi không có nguồn | `test_format_item_without_source_has_no_dangling_dash` |
| 4 | `timeline`, `social_search` | `limit=-1` | `items[:-1]` → trả 19/20 tweet | `limit <= 0` → mặc định 5 | `test_tweet_tools_negative_limit_falls_back_to_default` |

Kiểm chứng: chạy 4 regression test (8 trường hợp tham số hoá) trên **code gốc** → 8 failed; sau khi sửa → pass. `pytest` toàn suite: 88 passed, 0 failed (3 skipped là stub tool mới của B).

**Ví dụ lỗi unit test bắt được mà eval không bắt được:** bug #1. Eval chỉ chấm model có gọi `send(confirmed=true)` đúng lúc không; nếu model gửi `confirmed="false"` thì eval báo `wrong_arg_value` nhưng **tool vẫn gửi tin thật** — chỉ unit test mới thấy request POST đã đi ra.

## 4. Bằng chứng

- File: `starter_v0/data/eval_group.json`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/tools/{send,format,timeline,social_search}/tool.py`
- Branch: `c-tests` — commit: _(điền sau khi push)_
- Run suite group: _(điền sau khi A công bố hash v3 và chạy `run_eval.py --suite group`)_
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Claude Code (trợ lý AI) hỗ trợ đọc code tool, gợi ý input biên và viết test. Tự kiểm tra bằng: (1) chạy `pytest` sau mỗi thay đổi; (2) chạy regression test trên code gốc để xác nhận test thật sự bắt được bug (8 failed) rồi mới sửa; (3) validate `eval_group.json` bằng chính hàm kiểm tra schema của `run_eval.py` (10 case, 5 single + 5 multi). Không dùng AI để tạo số liệu run.

## 5. Tự đánh giá

_(TODO: tự viết — điều học được, phần làm tốt / chưa tốt)_
