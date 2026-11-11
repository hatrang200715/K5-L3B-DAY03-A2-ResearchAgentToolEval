# Báo cáo cá nhân — PhungThiNhai-2A202603725

## 1. Thông tin thành viên

- Họ tên: Phùng Thị Nhài
- MSSV: 2A202603725
- Email: nhaipt342k4@gmail.com
- Vai trong nhóm: **Tester**

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

Ghi chú: case route tới tool mới của nhóm sẽ thay một case ở trên sau khi tool mới được khai báo trong `tools.yaml` (contract test quét `eval_group.json`, nhắc tool chưa khai báo sẽ làm pytest đỏ cả nhóm).

### 3.2 Unit test — 14 stub tool có sẵn

clarify ×1, format ×3, send ×2, lookup ×1, fetch ×2, timeline ×1, social_search ×1, policy ×3. Mỗi test assert cả **request gửi đi** (URL, params/json, header) lẫn **kết quả trả về**; HTTP mock bằng `fake_http`, chạy offline.

### 3.3 Săn bug — 4 bug trong tool có sẵn, mỗi bug có regression test

| # | Tool | Input biên | Hành vi cũ | Sửa | Regression test |
|---|---|---|---|---|---|
| 1 | `send` | `confirmed="false"` (chuỗi) | **Gửi thật lên Telegram** — chuỗi khác rỗng là truthy, thủng guardrail xác nhận | Chỉ chấp nhận `confirmed is True` | `test_send_non_boolean_confirmed_does_not_send` |
| 2 | `format` | `items=["chuỗi", ...]` | Raise `AttributeError` (vi phạm quy ước "trả error dict, không raise") | Bỏ qua item không phải dict | `test_format_skips_non_dict_items_instead_of_raising` |
| 3 | `format` | item không có url/source | Dòng thừa `" - "` ở cuối | Bỏ separator khi không có nguồn | `test_format_item_without_source_has_no_dangling_dash` |
| 4 | `timeline`, `social_search` | `limit=-1` | `items[:-1]` → trả 19/20 tweet | `limit <= 0` → mặc định 5 | `test_tweet_tools_negative_limit_falls_back_to_default` |

Kiểm chứng: chạy 4 regression test (8 trường hợp tham số hoá) trên **code gốc** → 8 failed; sau khi sửa → pass. `pytest` toàn suite lúc commit: 88 passed, 0 failed (3 skipped là stub của tool mới do thành viên khác phụ trách). Sau khi merge phần tool mới vào `main`: **102 passed, 0 failed, 0 skipped**.

**Ví dụ lỗi unit test bắt được mà eval không bắt được:** bug #1. Eval chỉ chấm model có gọi `send(confirmed=true)` đúng lúc không; nếu model gửi `confirmed="false"` thì eval báo `wrong_arg_value` nhưng **tool vẫn gửi tin thật** — chỉ unit test mới thấy request POST đã đi ra.

## 4. Bằng chứng

- File: `starter_v0/data/eval_group.json`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/tools/{send,format,timeline,social_search}/tool.py`
- Branch: `phungthinhai-03725` (merge vào `main` qua PR #4) — commit: `af8bcb8`
- Run suite group: [`starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json`](../../starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json) — `v3+p29a0e3cdc49c+t2b0b1d3ae07e` (khớp hash v3 trong `version_log.csv`), `openai/gpt-4o-mini`, 10/10 case đo được, `provider_error_cases=0`, **8/10 PASS**. FAIL: `G04_out_of_scope_booking` (gọi `clarify` thay vì từ chối), `GM04_clarify_then_handle` (đoán handle `yannlecun` thay vì `ylecun`). Chi tiết ở bảng "Team Eval Cases" của group report.
- Sự cố khi chạy: lần chạy đầu trên Windows cho hash `p002948ccb771+tc8ea06338214` lệch v3 dù nội dung giống hệt — do `core.autocrlf=true` đổi xuống dòng LF→CRLF khi checkout. Đã tắt `autocrlf`, đưa 2 file artifact về LF (hash khớp lại `29a0e3cdc49c` / `2b0b1d3ae07e`) rồi chạy lại; run có hash sai không dùng làm bằng chứng.
- Chưa làm được: case route tới tool mới — 4 tool mới chưa được khai báo trong `artifacts/tools.yaml` của v3 nên chưa thể thêm case mà không làm đỏ contract test.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Claude Code (trợ lý AI) hỗ trợ đọc code tool, gợi ý input biên và viết test. Tự kiểm tra bằng: (1) chạy `pytest` sau mỗi thay đổi; (2) chạy regression test trên code gốc để xác nhận test thật sự bắt được bug (8 failed) rồi mới sửa; (3) validate `eval_group.json` bằng chính hàm kiểm tra schema của `run_eval.py` (10 case, 5 single + 5 multi). Không dùng AI để tạo số liệu run.

## 5. Tự đánh giá

**Điều mình học được.** Trước buổi lab, mình nghĩ kiểm thử một agent chỉ đơn giản là hỏi vài câu rồi xem nó trả lời có hợp lý không. Khi bắt tay vào làm, mình mới thấy cần tách ra hai câu hỏi khác nhau: agent có chọn đúng việc cần làm không, và công cụ phía sau có làm đúng việc đó không. Có lúc agent chọn đúng nhưng công cụ vẫn làm sai, và nếu chỉ nhìn điểm eval thì sẽ không bao giờ phát hiện ra. Trường hợp mình nhớ nhất là chức năng gửi tin lên Telegram: chỉ cần một giá trị xác nhận bị truyền sai kiểu là tin nhắn vẫn được gửi đi dù người dùng chưa đồng ý. Điều đó làm mình hiểu vì sao bước "hỏi lại trước khi hành động" phải được kiểm tra cẩn thận chứ không thể chỉ tin vào câu chữ trong prompt.

**Phần mình thấy làm tốt.** Mình hoàn thành phần kiểm thử cho các công cụ có sẵn và tìm ra được 4 lỗi thật bằng cách thử những đầu vào dễ hiểu nhầm mà người dùng hay model có thể đưa vào. Với mỗi lỗi, mình kiểm tra lại để chắc chắn bài test thật sự bắt được lỗi rồi mới sửa, chứ không viết test cho có. Khi viết 10 tình huống đánh giá cho nhóm, mình cố gắng chọn những chỗ agent dễ nhầm: hai yêu cầu nghe na ná nhau, người dùng đổi ý giữa chừng, hay người dùng đã đồng ý gửi rồi lại sửa nội dung.

**Phần chưa tốt.** Bộ đánh giá của nhóm vẫn thiếu một tình huống dùng công cụ mới do nhóm tự xây, vì phải chờ công cụ đó được đưa vào cấu hình chung. Lẽ ra mình nên trao đổi với thành viên phụ trách phần này sớm hơn để không bị kẹt ở cuối buổi. Một tình huống mình viết cũng chưa thật sự tốt: nó phụ thuộc vào việc model có biết tên tài khoản hay không, nên khi agent trả lời sai thì khó nói đó là lỗi suy luận hay chỉ là thiếu kiến thức. Ngoài ra, lần chạy đánh giá đầu tiên của mình bị lệch phiên bản vì một khác biệt nhỏ về định dạng file trên Windows, mình mất thêm thời gian tìm nguyên nhân trước khi có kết quả hợp lệ.

**Nếu làm lại.** Mình sẽ chủ động thống nhất với các thành viên ngay từ đầu buổi về công cụ mới và thời điểm ghép phần việc của nhau, chuẩn bị môi trường kỹ hơn trước khi chạy, và viết tình huống đánh giá theo hướng kiểm tra cách agent hành xử thay vì kiểm tra agent biết bao nhiêu. Qua bài này mình cũng thấy làm việc nhóm hiệu quả hơn khi mọi người chia sẻ tiến độ thường xuyên thay vì chỉ ghép bài ở cuối.
