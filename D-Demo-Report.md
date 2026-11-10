# Vai D: Demo & report

> Ca **09:00–13:00**. Máy D cần **đủ 4 key** (+ Telegram nếu làm bonus `send`). Laptop D chạy UI và tunnel suốt buổi showdown.
> Đọc kèm: [00-CHUNG.md](00-CHUNG.md) và `../DAY03-STUDENT-CHECKLIST.md` (CP8, CP9).

## Vai trò trong 1 câu

D làm **UI chạy được + link public**, quay **chat live** làm bằng chứng, viết **Phần A** cho showdown, và **ghép report** cuối buổi.

**Chỉ D sửa:** `app.py`, `artifacts/REPORT.md`, `artifacts/poster.html`, `transcripts/`.

## Mốc giờ

| Giờ | Việc | Phụ thuộc |
|---|---|---|
| 09:00–09:30 | clone repo, setup, `pip install streamlit`, **giới hạn chi tiêu key** | — |
| 09:30–10:30 | viết `app.py`, chạy local | không phụ thuộc ai |
| 10:30–11:00 | cài `cloudflared`, thử tunnel; đỡ C vài stub test | — |
| 11:00–11:45 | REPORT Phần A (+ poster) | danh sách tool của B (**11:30**) |
| **11:45** | `git pull` bản mới nhất, khởi động lại UI + tunnel | A đã push |
| **12:00** | **showdown**, đứng demo cùng B | — |
| ~12:30 | chat live v3, lấy transcript | hash v3 của A |
| 12:45–13:00 | ghép Phần B, kiểm tra nộp bài | nội dung từ A, B, C (**12:45**) |

## Checklist

**Setup**
- [ ] Clone repo nhóm, venv, `pip install -r requirements.txt streamlit`, `.env`
- [ ] Preflight pass
- [ ] **Đặt giới hạn chi tiêu cho key OpenRouter.** Team khác dùng thử là tốn credit của D.

**UI**
- [ ] `app.py` ở `starter_v0/`, gọi agent giống `chat.py`
- [ ] Hiển thị được câu trả lời; nên hiện thêm tool đã gọi + args (team khác thấy agent làm gì)
- [ ] Khi agent gọi `clarify`, UI hiện câu hỏi và chờ lượt sau
- [ ] Thử 3 kiểu câu: research thường / thiếu thông tin / ngoài phạm vi
- [ ] `streamlit run app.py` → mở `http://localhost:8501` chạy được

**Link public**
- [ ] `winget install --id Cloudflare.cloudflared` (báo `not recognized` thì mở terminal mới)
- [ ] `cloudflared tunnel --url http://localhost:8501` → copy URL `https://<random>.trycloudflare.com`
- [ ] Mở link trên điện thoại để chắc chắn người ngoài truy cập được

**REPORT Phần A (xong trước 12:00)**
- [ ] Team / Members / Provider-model
- [ ] A1: 1–2 câu agent làm gì + **link dùng thử**
- [ ] A2: bảng tool (tên · làm được gì · có phải tool mới không), lấy theo danh sách của B
- [ ] A3: 3–5 câu hỏi mẫu, chọn câu agent đã làm đúng
- [ ] (Tuỳ chọn) `artifacts/poster.html`: cùng nội dung, không thay thế bản markdown

**Showdown (11:45–12:30)**
- [ ] 11:45: `git pull` → tắt và chạy lại `streamlit` (để đọc prompt mới)
- [ ] Laptop: cắm sạc, tắt sleep, mạng ổn định, **không tắt `cloudflared`**
- [ ] Theo dõi credit Tavily / RapidAPI / OpenRouter trong lúc demo

**Chat live (sau v3)**
- [ ] `git pull` v3 → `python chat.py --provider openrouter --model <model> --version v3`
- [ ] ≥3 lượt: (1) research thường, (2) thiếu account/URL rồi lượt sau bổ sung, (3) "đăng bản tin lên Telegram" → agent **phải hỏi lại**, không gửi ngay
- [ ] Mở file trong `transcripts/`, kiểm tra `prompt_hash` khớp v3, push
- [ ] B4: bảng turn · request · tool calls · version · kết quả

**Bonus `send` (nếu còn thời gian)**
- [ ] Tạo bot qua BotFather + channel, lấy `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (xem `TOOL-SETUP.md` mục 6). **D giữ token**, không chia sẻ.
- [ ] Transcript chứng minh: agent hỏi `yes_no` → user đồng ý → gọi `send(confirmed=true)` → tin xuất hiện trên channel
- [ ] Ghi vào B5

**Ghép report + nộp (12:45–13:00)**
- [ ] Dán B1/B2/B6 (A), B3 + B5 unit test (C), B5 tool mới (B), B4 + B5 UI/send (D)
- [ ] Kiểm tra danh sách nộp bài (mục "Nộp bài" trong checklist chính)
- [ ] `git status`: **không có `.env`**, có đủ `runs/`, `transcripts/`

## Hướng dẫn

### Khung `app.py`
Dùng lại các hàm có sẵn của starter, không viết lại vòng lặp tool:
```python
import streamlit as st
from pathlib import Path
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop

ROOT = Path(__file__).resolve().parent
load_lab_env(ROOT)                               # nạp .env, giống chat.py
SYSTEM = (ROOT / "artifacts/system_prompt.md").read_text(encoding="utf-8")
TOOLS = to_openai_tools(load_tool_declarations(ROOT / "artifacts/tools.yaml"))
provider = make_provider("openrouter")

if "history" not in st.session_state:
    st.session_state.history = []

# 1. vẽ lại history bằng st.chat_message
# 2. nhận input bằng st.chat_input
# 3. messages = [system] + history + [user]   (giống chat.py)
# 4. result = run_model_tool_loop(provider=..., messages=..., tools=TOOLS, model=..., max_tool_rounds=4)
# 5. hiển thị result["assistant_text"]; tool đã gọi nằm trong result["tool_events"]
# 6. thêm user + assistant vào history
```

## Gợi ý

**Nấc 1:** chạy `chat.py` trước để hiểu luồng, rồi đọc hàm `main()` của nó. `app.py` gần như là `main()` thay `input()` bằng `st.chat_input`.

**Nấc 2:** Streamlit chạy lại **toàn bộ script** sau mỗi lần nhập. Thứ gì cần giữ qua các lượt (history) phải nằm trong `st.session_state`.

**Nấc 3:** muốn tránh tạo provider và đọc file lại mỗi lượt thì dùng `@st.cache_resource`. Nhưng nhớ: có cache thì sau khi `git pull` phải **khởi động lại** Streamlit mới nhận prompt mới.

**Hiện tool calls:** mỗi phần tử trong `result["tool_events"]` có các key `tool`, `args`, `result`. Dùng `st.expander("Tool calls")` + `st.json(...)` cho gọn.

**Câu hỏi mẫu cho A3:** lấy từ các case base mà v3 đã PASS (đọc run JSON của A), để team khác thử là chạy đúng.

## Lưu ý
- UI **không ghi transcript** như `chat.py`. Bằng chứng chat live cho B4 nên lấy từ `chat.py`.
- Link `trycloudflare.com` là **tạm thời**: tắt lệnh là mất, chạy lại sẽ ra URL khác, phải cập nhật lại A1.
- Chạy `streamlit run app.py` từ trong `starter_v0/` để import `providers`, `tools`, `chat` tìm được module.
- Không để key hiện trên UI hay trong log in ra màn hình.
- Report: mọi số liệu chép từ `runs/` và `transcripts/`, không ghi theo trí nhớ.

## Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Streamlit | thư viện Python dựng web UI nhanh |
| `st.session_state` | nơi giữ dữ liệu qua các lần Streamlit chạy lại script |
| Rerun | Streamlit chạy lại toàn bộ script sau mỗi tương tác |
| Tunnel (Cloudflare) | link public tạm thời trỏ vào server trên máy local |
| Transcript | log JSON của một phiên chat, có version + tool calls |
| Human-in-the-loop confirmation | user phải đồng ý trước hành động có side effect |
| Side effect | tool thay đổi thế giới bên ngoài (gửi tin) |
| Spending limit | giới hạn tiền một API key được tiêu |
| Debate poster | bản 1 trang giới thiệu agent cho team khác lúc showdown |
| Evidence-driven report | report chỉ dựa trên log thật |
