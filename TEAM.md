# Team

## Thông tin nhóm

- Tên nhóm: A2
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-A2-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/hatrang200715/K5-L3B-DAY03-A2-ResearchAgentToolEval (main)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lương Thị Hồng Hạnh       | 2A202603748     |  26ai.hanhlth@vinuni.edu.vn     |    hatrang200715    |     team lead    |
|   2  Vũ Quang Huy | 2A202603782 | 26ai.huyvq6@vinuni.edu.vn | huyvu-03 |         |
|   3 | Phùng Văn Thanh Cao    |2A202603741      |ptc99998888@gmail.com       |ththanh8888        |Thành viên làm B:Tool builder          |
|   4 | Phùng Thị Nhài | 2A202603725 | nhaipt342k4@gmail.com | nhaipt342k4 | C — Tester (eval nhóm + unit test) |
## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## PhungThiNhai-2A202603725

Báo cáo cá nhân: [report/team/2A202603725_PhungThiNhai.md](report/team/2A202603725_PhungThiNhai.md)

### Phần việc phụ trách

- Vai C — Tester: `starter_v0/data/eval_group.json`, 14 stub tool có sẵn trong `starter_v0/tests/test_tools_todo.py`, sửa bug tool có sẵn kèm regression test, chạy suite group, nội dung B3 + B5 (unit test).

### Đóng góp cụ thể

- 10 eval case nhóm (5 single + 5 multi turn).
- 14 stub test của tool có sẵn → không còn skip.
- Tìm và sửa 4 bug trong tool có sẵn (`send`, `format` ×2, `timeline`/`social_search`), mỗi bug có regression test.
- Chạy suite group trên v3, điền bảng B3 và phần Test challenge (B5) trong group report.

### Bằng chứng

- Commit `af8bcb8` (merge vào `main` qua PR #4): `starter_v0/data/eval_group.json`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/tools/{send,format,timeline,social_search}/tool.py`.
- Run group: `starter_v0/runs/v3_B_group_openrouter_20261111T100954515130.json` (`v3+p29a0e3cdc49c+t2b0b1d3ae07e`, 8/10 PASS, `provider_error_cases=0`).
- `pytest`: 102 passed, 0 failed, 0 skipped.

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
