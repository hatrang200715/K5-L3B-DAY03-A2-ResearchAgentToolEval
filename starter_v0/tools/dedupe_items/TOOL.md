---
name: dedupe_items
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items]
outputs: [items, count, removed, skipped_invalid]
side_effect: false
---
# dedupe_items

Lọc các item trùng nhau trong danh sách kết quả đã gom (ví dụ gộp từ `lookup` + `hn_search`) trước khi `format`.
Chạy local, không gọi mạng.

- So sánh theo URL đã chuẩn hoá: không phân biệt hoa thường ở scheme/host, bỏ `www.`, bỏ `/` cuối, bỏ `#fragment`, bỏ tham số `utm_*`.
- Item không có URL → so theo `title` (không phân biệt hoa thường). Không có cả hai → giữ nguyên.
- Giữ item xuất hiện đầu tiên. Phần tử không phải object bị bỏ qua và đếm ở `skipped_invalid`.
- `items` không phải list → `{"error", "message"}`, không raise.
