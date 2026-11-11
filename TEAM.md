# Team

## Thông tin nhóm

- Tên nhóm: A2
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-A2-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/hatrang200715/K5-L3B-DAY03-A2-ResearchAgentToolEval (main)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Lương Thị Hồng Hạnh | 2A202603748 | 26ai.hanhlth@vinuni.edu.vn | hatrang200715 | A — Nhóm trưởng, eval lead |
| 2 | Vũ Quang Huy | 2A202603782 | 26ai.huyvq6@vinuni.edu.vn | huyvu-03 | D — UI, demo và báo cáo |
| 3 | Phùng Văn Thanh Cao | 2A202603741 | ptc99998888@gmail.com | ththanh8888 | B — Tool builder |
| 4 | Phùng Thị Nhài | 2A202603725 | nhaipt342k4@gmail.com | nhaipt342k4 | C — Tester (eval nhóm và unit test) |

## Cá nhân

Mỗi thành viên có một báo cáo cá nhân theo dạng:

```text
report/team/MSSV_HoTen.md
```

### Lương Thị Hồng Hạnh — 2A202603748 (Vai A)

- **Phụ trách:** nhóm trưởng và eval lead; quản lý vòng thử nghiệm, đọc kết quả, đặt giả thuyết, chỉnh prompt/tool declaration và cập nhật version log.
- **Đóng góp:** chạy baseline v0 và các vòng v1–v3 trên OpenRouter với `openai/gpt-4o-mini`; chỉnh system prompt ở v1–v2, cải thiện mô tả và quy ước đối số trong tools YAML ở v3; tích hợp block khai báo 4 tool mới.
- **Bằng chứng:** [version log](starter_v0/artifacts/version_log.csv), [system prompt](starter_v0/artifacts/system_prompt.md), [tool declarations](starter_v0/artifacts/tools.yaml), các [run eval](starter_v0/runs/); commit `f22fa9a` và `e997898`.
- **Báo cáo cá nhân:** [2A202603748_LuongThiHongHanh.md](report/team/2A202603748_LuongThiHongHanh.md).

### Vũ Quang Huy — 2A202603782 (Vai D)

- **Phụ trách:** xây UI, demo/chat live và hỗ trợ tổng hợp báo cáo.
- **Đóng góp:** triển khai Streamlit UI chat nhiều lượt; hiển thị tool calls, arguments, kết quả và lỗi; bổ sung lựa chọn provider/model/version và xử lý lượt clarify.
- **Bằng chứng:** [UI](starter_v0/app.py), [dependency](starter_v0/requirements.txt), các [transcript chat](starter_v0/transcripts/); commit `7daa3e0`.
- **Ghi chú:** mã UI chạy local tại `http://localhost:8501`; repo chưa có URL deploy công khai được ghi nhận.
- **Báo cáo cá nhân:** [2A202603782_VuQuangHuy.md](report/team/2A202603782_VuQuangHuy.md).

### Phùng Văn Thanh Cao — 2A202603741 (Vai B)

- **Phụ trách:** xây tool mới, viết unit test và bàn giao khai báo YAML cho vai A.
- **Đóng góp:** tạo `hn_search`, `reading_time`, `extract_links`, `dedupe_items`; mỗi tool có `tool.py` và `TOOL.md`, đăng ký trong tools package; viết 14 unit test chạy offline và block YAML mô tả khi nào dùng/không dùng cùng quy ước tham số.
- **Bằng chứng:** [tool package](starter_v0/tools/), [YAML block](starter_v0/tools/NEW_TOOLS_FOR_A.yaml), [unit tests](starter_v0/tests/test_tools_todo.py); commit `56fd688`. Kết quả tại thời điểm làm: 76 passed, 14 skipped; contract test với YAML block: 75 passed.
- **Báo cáo cá nhân:** [2A202603741_PhungVanThanhCao.md](report/team/2A202603741_PhungVanThanhCao.md).

### Phùng Thị Nhài — 2A202603725 (Vai C)

- **Phụ trách:** eval nhóm, unit test cho tool có sẵn, regression test và phân tích lỗi.
- **Đóng góp:** viết 10 eval case (5 single-turn, 5 multi-turn); hoàn tất 14 stub test cho tool có sẵn; tìm và sửa 4 bug ở `send`, `format` (2 lỗi), `timeline`/`social_search`, mỗi bug có regression test; chạy group eval và tổng hợp kết quả.
- **Bằng chứng:** [eval cases](starter_v0/data/eval_group.json), [unit/regression tests](starter_v0/tests/test_tools_todo.py), [group eval run](starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json); commit `af8bcb8`. Run group đo đủ 10 case, provider errors bằng 0, kết quả 8/10 PASS. Test suite tại thời điểm merge: 102 passed, 0 failed, 0 skipped.
- **Báo cáo cá nhân:** [2A202603725_PhungThiNhai.md](report/team/2A202603725_PhungThiNhai.md).
