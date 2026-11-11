# Báo cáo cá nhân — LuongThiHongHanh-2A202603748

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Lương Thị Hồng Hạnh
- MSSV: 2A20263748
- Email: 26ai.hanhlth@vinuni.edu.vn

## 2. Phần việc phụ trách

### Vai A: Eval lead (nhóm trưởng)

A giữ **vòng lặp tối ưu**: chạy eval, đọc log, đặt giả thuyết, sửa prompt và tool declaration, ghi version. Đây là **đường găng** của nhóm (chuỗi việc không chạy song song được), nên A không nhận thêm việc nào khác.

**Chỉ A sửa:** `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`.

## 3. Đóng góp cụ thể

**Setup**
- [ ] Tạo repo nhóm (fork hoặc repo mới, push code starter), thêm B, C, D làm collaborator
- [ ] Tạo `.gitattributes` ở gốc repo, nội dung `* text=auto eol=lf` → `git add --renormalize .` → commit, push
- [ ] Chốt model (ví dụ `openai/gpt-4o-mini`), báo cả nhóm
- [ ] venv, `.env`, `python scripts/preflight_provider.py --provider openrouter` pass

**Baseline**
- [ ] `python run_eval.py --provider openrouter --model <model> --version v0 --suite base --eval-cases data/eval_base.json`
- [ ] Đọc `summary` + mỗi case FAIL (`failures`, `observed_mismatch`, `actual_tool_calls`)
- [ ] Lập bảng case FAIL → loại lỗi → nguyên nhân giả định, gửi cả nhóm
- [ ] Ghi dòng v0 vào `version_log.csv`, push `runs/`

**Tối ưu**
- [ ] v1: một giả thuyết → sửa → chạy → ghi log → push → báo hash
- [ ] v2: merge block YAML tool mới của B (chỉ việc này) → chạy → ghi log
- [ ] v3: một giả thuyết → chạy → ghi log → báo hash
- [ ] Sau mỗi lần sửa: `pytest tests/test_tool_contract.py` xanh
- [ ] (Tuỳ chọn) đọc các run thử `exp-*` của người khác trước khi chọn giả thuyết
- [ ] Nếu máy C không có key: chạy suite group bằng v3 giúp C

**Report**
- [ ] B1: bảng v0–v3 (khớp từng dòng `version_log.csv`)
- [ ] B2: case · loại lỗi · actual calls · sai gì · fix
- [ ] B6: fix nào thuộc prompt, fix nào thuộc tools.yaml, lỗi nào cần review tay, bước tiếp theo

## 4. Bằng chứng

- File/commit/PR: https://github.com/hatrang200715/K5-L3B-DAY03-A2-ResearchAgentToolEval/pull/3/changes/f22fa9adf135526d299a6b8974d72ec8d94ab0ab
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: chạy eval và xem kết quả `runs/*.json`
sửa lại system prompt cải thiện tools yaml
## 5. Tự đánh giá
Học được cách cải thiện system prompt để viết prompt tốt hơn. Nhóm làm việc phối hợp với nhau tốt
