---
name: reading_time
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [text, words_per_minute]
outputs: [word_count, char_count, words_per_minute, minutes]
side_effect: false
---
# reading_time

Đếm số từ, số ký tự và ước tính số phút đọc của một đoạn văn bản đã có (chạy local, không gọi mạng).

- `minutes` làm tròn lên, tối thiểu 1 khi có ít nhất 1 từ.
- `words_per_minute` mặc định 200; phải là số nguyên > 0.
- Text rỗng / sai kiểu, hoặc `words_per_minute` không hợp lệ → `{"error", "message"}`, không raise.
