---
name: hn_search
track: bonus
kind: live_api
provider: Hacker News (Algolia Search API, free, no key)
requires_env: []
inputs: [query, limit]
outputs: [query, items, count]
side_effect: false
---
# hn_search

Tìm bài (story) trên Hacker News theo từ khóa qua API công khai miễn phí của Algolia
(`https://hn.algolia.com/api/v1/search`). Không cần API key.

- Mỗi item có `title`, `url` (link gốc, nếu không có thì là link thảo luận HN), `discussion_url`,
  `source`, `summary` (points · comments), `created_at`.
- `limit` được kẹp trong khoảng 1–20; chuỗi số như `"5"` được chấp nhận.
- Lỗi (query rỗng, limit sai kiểu, HTTP lỗi, timeout) trả về `{"error", "message"}`, không raise.
