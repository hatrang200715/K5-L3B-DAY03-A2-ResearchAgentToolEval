---
name: extract_links
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [text, limit]
outputs: [links, count]
side_effect: false
---
# extract_links

Trích các URL `http(s)://` có trong một đoạn văn bản user dán vào (chạy local, không gọi mạng, không mở link).

- Giữ thứ tự xuất hiện, bỏ trùng, cắt dấu câu dính ở cuối (`.,;:!?`).
- `limit` kẹp trong 1–100, mặc định 20.
- Text không có link → `links: []`, `count: 0`. Sai kiểu → `{"error", "message"}`, không raise.
