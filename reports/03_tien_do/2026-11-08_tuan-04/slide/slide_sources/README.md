# Nguồn bản báo cáo hiện tại

Bản đang dùng nằm tại thư mục cha `slide/`: PowerPoint 16 slide, PDF 16 trang và ghi chú tương ứng. Bản này giữ bìa người dùng, dữ liệu, biểu đồ và video đã có; cải thiện cách đọc bài báo và giải thích code. Không có phần kế hoạch tuần tiếp theo.

**Quy trình hiện hành:** xem [README_revision.md](README_revision.md). Không chạy các bộ tạo cũ để ghi đè bản hiện tại.

- `build_improved_sections.cjs`: ba bố cục native cho phần IPN HandS, đối chiếu cấu hình và hai dòng forward.
- `improve_current_deck.py`: ghép vào bản người dùng đã chỉnh, bỏ lời hướng dẫn bước tiếp, đồng bộ số trang và 16 notes.
- `render_improved_deck.ps1`: xuất PNG/PDF bằng PowerPoint và kiểm tra tràn chữ/bảng.
- `finalize_improved_deck.py`: kiểm chứng và phát hành vào thư mục cha, có kiểm tra tránh ghi đè chỉnh sửa mới.
- `verify_package.py`: kiểm tra bộ đầu ra hiện tại, không huấn luyện.
- `qa/cai_thien_2026-11-08/`: bản nháp, PNG, log, thông tin bảo toàn dữ liệu và mã băm bản phát hành.
- `verified_metrics.json`, `training_history.csv`, `assets/`, `research/`: bằng chứng và nguồn tra cứu đã thu thập.

`build_deck.cjs`, `merge_preserve_user_edits.py`, `write_report.py`, `revise_content.py`, `finalize_revision_docs.py` là nguồn lịch sử. Chạy lại chúng có thể đưa nội dung/bố cục đã bỏ trở lại. Snapshot 539 tệp nguồn được giữ nguyên; ba tài liệu `documents/Base/` đã chuyển sang `reports/01_tai_lieu_de_tai/` và được ánh xạ khi kiểm tra mã băm.

`node_modules` là junction tới thư viện runtime, không đóng gói junction vào ZIP. Bản PDF không phát video; video nằm trong PowerPoint và `assets/demo_test.mp4`.
