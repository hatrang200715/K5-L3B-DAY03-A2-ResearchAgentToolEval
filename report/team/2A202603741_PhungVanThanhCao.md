# Báo cáo cá nhân — PhungVanThanhCao-2A202603741

## 1. Thông tin thành viên

- Họ tên: Phùng Văn Thanh Cao
- MSSV: 2A202603741
- Email: ptc99998888@gmail.com
- GitHub: ththanh8888
- Vai trò trong nhóm: B — Tool builder

## 2. Phần việc phụ trách

Vai B (Tool builder):

- Thêm tool mới cho research agent (bắt buộc ≥ 1; nhóm làm 4 tool để đủ điều kiện bonus).
- Viết unit test cho tool mới (≥ 3 test/tool), chạy offline.
- Viết block YAML khai báo tool (description + quy ước tham số) gửi vai A merge vào `starter_v0/artifacts/tools.yaml`.
- Bàn giao tên tool + câu hỏi mẫu cho C (eval case), bảng tool (A2) và nội dung B5 cho D; đứng demo cùng D lúc showdown.

## 3. Đóng góp cụ thể

**4 tool mới:**

| Tool | Loại | Làm gì | Tham số |
|---|---|---|---|
| `hn_search` | live_api — Hacker News Algolia API (miễn phí, không cần key) | Tìm bài/thảo luận trên Hacker News theo từ khóa; trả tiêu đề, link, points, số comment | `query`, `limit` (kẹp 1–20) |
| `reading_time` | local | Đếm số từ, số ký tự, ước tính số phút đọc của một đoạn văn bản đã có | `text`, `words_per_minute` (mặc định 200) |
| `extract_links` | local | Trích các URL http(s) trong văn bản, giữ thứ tự, bỏ trùng, cắt dấu câu cuối | `text`, `limit` (kẹp 1–100) |
| `dedupe_items` | local | Lọc item trùng (URL đã chuẩn hoá hoặc tiêu đề) trước khi `format` | `items` |

- Mỗi tool có `tool.py` (mọi tham số có giá trị mặc định; lỗi trả `{"error", "message"}` thay vì raise) và `TOOL.md` (frontmatter đúng contract trong `starter_v0/tools/README.md`).
- Đăng ký cả 4 tool trong `starter_v0/tools/__init__.py` (`TOOL_FUNCTIONS`), không sửa tool có sẵn.
- Block YAML `starter_v0/tools/NEW_TOOLS_FOR_A.yaml`: mỗi description nêu **làm gì · khi nào dùng · khi nào KHÔNG dùng** để model phân biệt với `lookup` / `fetch` / `social_search`; mỗi tham số có quy ước. Không tự sửa `tools.yaml` trên branch của mình (tránh conflict với A).

**14 unit test** trong `starter_v0/tests/test_tools_todo.py` (chỉ sửa đoạn `YOUR NEW TOOL(S)` cuối file), chạy offline, không tốn chi phí:

| Tool | Số test | Hành vi kiểm tra |
|---|---:|---|
| `hn_search` | 5 | request đúng URL + params và map kết quả (link HN dự phòng khi không có url); query rỗng/sai kiểu → lỗi, không gọi mạng; `limit="5"`/`0`/`999` được kẹp, `limit="many"` → lỗi; HTTP 429 → error dict; timeout → error dict |
| `reading_time` | 3 | đếm từ + làm tròn phút lên; văn bản ngắn tối thiểu 1 phút, nhận `"100"`; text rỗng/None, wpm = 0 hoặc chữ → lỗi |
| `extract_links` | 3 | giữ thứ tự, bỏ trùng, cắt dấu câu; `limit` + không có link; text sai kiểu / limit sai → lỗi |
| `dedupe_items` | 3 | trùng URL sau chuẩn hoá (`www.`, `utm_*`, `/` cuối, `#`); không có URL thì so tiêu đề; `items` không phải list → lỗi, phần tử rác bị bỏ qua và đếm |

## 4. Bằng chứng

- File/commit/PR:
  - Commit `56fd688` trên nhánh `PhungVanThanhCao` — "B: add 4 new tools (hn_search, reading_time, extract_links, dedupe_items) + 14 unit tests".
  - Code: `starter_v0/tools/hn_search/`, `starter_v0/tools/reading_time/`, `starter_v0/tools/extract_links/`, `starter_v0/tools/dedupe_items/`, `starter_v0/tools/__init__.py`, `starter_v0/tools/NEW_TOOLS_FOR_A.yaml`.
  - Test: `starter_v0/tests/test_tools_todo.py` (đoạn `YOUR NEW TOOL(S)`).
  - Kết quả: `pytest` → **76 passed, 14 skipped, 0 failed** (14 skipped là stub của tool có sẵn, được phép); `pytest tests/test_tool_contract.py` khi dán tạm block YAML mới vào `tools.yaml` → **75 passed** (sau đó hoàn nguyên `tools.yaml`).
  - PR: https://github.com/hatrang200715/K5-L3B-DAY03-A2-ResearchAgentToolEval/pull/1
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng **Claude Code** (trong VS Code) để đọc đề, lên kế hoạch, viết code 4 tool, `TOOL.md`, block YAML và unit test.
  - Cách tự kiểm tra:
    1. Chạy thử từng tool bằng `python -c "from tools import TOOL_FUNCTIONS as T; ..."`: `hn_search` gọi API thật (miễn phí) trả về bài thật; 3 tool local trả kết quả đúng với input mẫu.
    2. Chạy `pytest` toàn bộ: 0 failed; chạy riêng 14 test của tool mới: 14 passed.
    3. Dán tạm block YAML vào `tools.yaml`, chạy contract test xanh, rồi `git checkout artifacts/tools.yaml` để không sửa file của A.
    4. Đọc lại code để giải thích được: vì sao trả error dict thay vì raise, mỗi test kiểm tra hành vi nào, vì sao description phải tách biệt với `lookup`/`fetch`.
  - Chỉ dùng API/model miễn phí (Hacker News Algolia API, OpenRouter model `:free`); unit test chạy offline.

## 5. Tự đánh giá

Trong vai B (Tool builder), tôi đã làm 4 tool mới: hn_search (gọi Hacker News API miễn phí), reading_time, extract_links và dedupe_items. Đề chỉ yêu cầu tối thiểu 1 tool, nên tôi đạt cả điều kiện bonus. Mỗi tool có ít nhất 3 unit test, tổng cộng 14 test, và toàn bộ pytest chạy 76 passed, contract test với block YAML mới đạt 75/75, chi phí 0đ (commit 56fd688). Phần khó nhất với tôi là lần chạy eval đầu báo provider_error cả 20 case vì key trong .env bị trống do lưu file chưa đúng. Tôi xử lý bằng cách kiểm tra và lưu lại file rồi chạy lại. Sau đó run v2 lại bị lỗi 429 do OpenRouter free giới hạn lượt gọi, nên tôi không dùng run đó làm bằng chứng. Điều tôi học được rõ nhất là unit test chỉ kiểm tra code của tool có chạy đúng không, còn eval mới đo việc model có chọn đúng tool hay không. Vì vậy một tool pass hết test vẫn có thể bị model dùng sai, và description cần ghi rõ cả “khi nào không dùng”. Tôi dùng Claude Code để viết code, test và block YAML, còn tôi tự chạy thử từng tool, chạy pytest và contract test, rồi đọc lại code để hiểu vì sao tool trả về error dict thay vì raise lỗi. Điểm tôi chưa làm tốt là code chủ yếu do AI viết, và hn_search mới chỉ được test bằng mock, chưa thử xem model có tự chọn tool này khi chạy thật không. Lần sau tôi sẽ tự viết ít nhất một tool từ đầu và phối hợp với C để thêm eval case kiểm tra model có gọi đúng tool mới không. Tôi tự đánh giá mức hoàn thành khoảng 8/10.
