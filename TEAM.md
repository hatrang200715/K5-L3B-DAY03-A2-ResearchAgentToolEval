# Team

## Thông tin nhóm

- Tên nhóm:A2
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Phùng Văn Thanh Cao    |2A202603741      |ptc99998888@gmail.com       |ththanh8888        |Thành viên làm B:Tool builder          |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## PhungVanThanhCao-2A202603741

### Phần việc phụ trách

- Vai B: Tool builder — thêm tool mới cho agent, viết unit test, block YAML khai báo tool gửi vai A.

### Đóng góp cụ thể

- 4 tool mới: `hn_search` (Hacker News API, miễn phí, không cần key), `reading_time`, `extract_links`, `dedupe_items` (chạy local).
- Mỗi tool có `tool.py` + `TOOL.md`, đăng ký trong `starter_v0/tools/__init__.py`; lỗi trả `{error, message}`, không raise.
- 14 unit test trong `starter_v0/tests/test_tools_todo.py` (happy path / input xấu / nhánh lỗi), chạy offline.
- Block YAML `starter_v0/tools/NEW_TOOLS_FOR_A.yaml` gửi A merge vào `tools.yaml`.

### Bằng chứng

- Commit `56fd688` trên nhánh `PhungVanThanhCao`; folder `starter_v0/tools/{hn_search,reading_time,extract_links,dedupe_items}/`.
- `pytest`: 76 passed, 0 failed; contract test với block YAML mới: 75 passed.
- Báo cáo cá nhân: [report/team/2A202603741_PhungVanThanhCao.md](report/team/2A202603741_PhungVanThanhCao.md)
