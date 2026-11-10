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

...
