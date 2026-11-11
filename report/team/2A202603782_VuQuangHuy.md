# Báo cáo cá nhân — VuQuangHuy-2A202603782

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Vũ Quang Huy
- MSSV: 2A202603782
- Email: 26ai.huyvq6@vinuni.edu.vn

## 2. Phần việc phụ trách

- Vai D: Demo và report.
- Xây dựng Streamlit UI cho research agent.
- Chuẩn bị link public để nhóm khác dùng thử.
- Thực hiện chat live v3 và lưu transcript làm bằng chứng.
- Hỗ trợ tổng hợp báo cáo cuối cùng.

## 3. Đóng góp cụ thể

- Cài đặt Streamlit và thêm dependency vào `starter_v0/requirements.txt`.
- Xây dựng `starter_v0/app.py` bằng cách tái sử dụng vòng lặp agent trong `chat.py`.
- Cài đặt giao diện chat nhiều lượt bằng `st.session_state`.
- Hiển thị tool calls, arguments, tool results và lỗi provider/tool.
- Hỗ trợ luồng `clarify`, cho phép agent hỏi lại và chờ lượt trả lời tiếp theo.
- Thêm lựa chọn provider, model, artifact version và chức năng reload artifact.
- Kiểm tra UI chạy được tại `http://localhost:8501`.
- Chạy tool contract test: 55 tests passed.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/app.py`
  - `starter_v0/requirements.txt`
  - Commit: TODO sau khi commit/push
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Codex hỗ trợ phân tích source code, lập kế hoạch và triển khai Streamlit UI.
  - Tự kiểm tra syntax bằng `python -m py_compile app.py`.
  - Chạy `pytest tests/test_tool_contract.py -q`: 55 passed.
  - Khởi động bằng `python -m streamlit run app.py` và xác nhận server chạy tại `http://localhost:8501`.

## 5. Tự đánh giá

Trong vai D (Demo và report), tôi đã hoàn thành phần chính là xây dựng Streamlit UI chạy trên vòng lặp agent có sẵn thay vì viết lại logic gọi model và tool. UI giữ được hội thoại nhiều lượt bằng `st.session_state`, hiển thị tool call, arguments, kết quả và lỗi, hỗ trợ luồng `clarify`, tự nạp các tool khai báo trong `tools.yaml`, và mặc định chọn version mới nhất trong `version_log.csv`. Tôi cũng kiểm tra UI với các tool mới như `hn_search`, `extract_links` và `reading_time`.

Phần khó nhất là giữ UI đồng bộ với prompt, tool declaration và version liên tục thay đổi khi các thành viên merge code. Tôi học được rằng mỗi phiên demo phải dùng một artifact snapshot nhất quán; sau khi prompt hoặc tools thay đổi cần reload phiên chat và kiểm tra lại hash/version. Tôi cũng hiểu rõ hơn sự khác nhau giữa eval đo quyết định của model, unit test đo code tool, và transcript làm bằng chứng cho hành vi nhiều lượt thực tế. Ngoài ra, quá trình setup giúp tôi xử lý các vấn đề thực tế như tương thích Python/PyYAML, giới hạn quota của OpenRouter và việc không để API key xuất hiện trên UI hoặc Git.

Tôi dùng Codex để hỗ trợ đọc code, lập kế hoạch và triển khai, nhưng đã tự kiểm tra bằng syntax check, pytest, khởi động Streamlit và thử các yêu cầu thật trên UI. Điểm chưa hoàn thiện là link public và transcript chat v3 chính thức phụ thuộc vào artifact cuối cùng của nhóm; tôi cần kiểm tra lại trên thiết bị khác sau khi mở Cloudflare Tunnel. Nếu làm lại, tôi sẽ bổ sung test tự động cho trạng thái Streamlit, chỉ tạo transcript sau tin nhắn đầu tiên để tránh log rỗng, và chuẩn bị một môi trường demo ổn định hơn thay vì phụ thuộc vào tunnel tạm thời. Tôi tự đánh giá mức hoàn thành hiện tại khoảng **8/10**.
