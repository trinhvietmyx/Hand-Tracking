# Kiểm tra bản thuyết trình cải thiện — 08/11/2026

Đã giữ yêu cầu không có phần kế hoạch tuần tiếp theo hoặc bảng đầu ra theo tuần. Bản hiện tại gồm **16 slide, 16 trang PDF và 16 mục ghi chú**.

## Nội dung thay đổi

- Đọc sâu IPN HandS: bổ sung tác giả, Applied Sciences 2025, DOI, sơ đồ ba nguồn annotation và Bảng 6. Các số mean/std thuộc bài báo, không phải thực nghiệm đồ án. Hiệu recall 78,0 − 62,7 = 15,3 điểm phần trăm được diễn giải rõ.
- Thêm một slide đối chiếu paper/code và ý nghĩa 44 đặc trưng, 30 mẫu ở 20 Hz, hidden size 64. Ghi rõ 64 là cấu hình cơ sở hiện có, chưa có đối chứng để kết luận tối ưu.
- Minh họa hai dòng forward đúng mã nguồn, tensor [B,30,44] → [B,30,64] → [B,64] → [B,5], vị trí softmax trong predict_gesture.
- Kết luận chỉ nêu kết quả và giới hạn đã ghi nhận. Các dòng bước tiếp/việc cần làm được đổi thành giới hạn hiện tại. Sửa toàn bộ số trang; bỏ mục kế hoạch theo tuần khỏi báo cáo viết đi kèm.
- Viết lại ghi chú đủ 16 slide và phần luyện trả lời câu hỏi; nguồn được đặt riêng để tra cứu.

## Giữ nguyên nội dung người dùng và thực nghiệm

Bản trước được sao lưu tại `reports/99_luu_tru/truoc_cai_thien_2026-11-08`. Bìa và bố cục các chỉnh sửa trực tiếp của người dùng được giữ. Nội dung chín slide cũ chỉ đổi số trang; ba slide được cải thiện nội dung nghiên cứu/code/kết luận, ba slide đổi lời hướng dẫn tiếp theo thành giới hạn hiện tại, và thêm một slide đối chiếu cấu hình. Toàn bộ 14 part ảnh/video/chart/workbook của bản vào giữ nguyên bytes. Có log `slide_sources/qa/cai_thien_2026-11-08/preservation_checks.json`.

Đối chiếu **539 tệp** nguồn/thực nghiệm/đặc tả trong snapshot, có ánh xạ ba tài liệu đã chuyển sang `reports/01_tai_lieu_de_tai/`: không có thay đổi. Không huấn luyện hoặc sửa số liệu; giữ 250 clip, 40/50 test đúng, Macro-F1 0,7619, lỗi lên/xuống và phần chưa đo.

## Kiểm tra kỹ thuật

PowerPoint mở được, render đủ 16 slide 1.600 × 900. Kiểm tra BoundHeight/BoundWidth của textbox và ô bảng không phát hiện tràn. Có 6 bảng native, 2 biểu đồ với workbook và video 10 giây ở slide 13. Đã xem từng slide; đã render PDF và kiểm tra các trang mới.

Validator của skill Anthropic pptx được chạy với `--original` là bản trước, báo PASSED về XML, relationships, IDs, content types, chart và không có lỗi XSD mới. Bản PDF có 16 trang, trích xuất được chữ Việt. Poppler cảnh báo font phụ Symbol/ArialUnicode; hình kiểm tra vẫn hiện đúng các ký hiệu/chữ Việt được xem.

Ghi chú trong PPTX và Markdown đều có đủ 16 mục, không lẫn ghi chú kế hoạch đã bỏ. Kiểm tra thứ tự và chân trang 01/16 đến 16/16. Các log và PNG hiện tại nằm trong `slide_sources/qa/cai_thien_2026-11-08/`.

## Phạm vi bằng chứng

Video là phát lại clip đã lưu. Chưa có dữ liệu thực nghiệm cho FPS/latency toàn hệ thống, 40 lượt trực tiếp, 5 phút nền hoặc người chưa thấy. Chưa tái lập LSTM gốc của IPN HandS. Kiểm tra media gồm bytes và thời lượng PowerPoint nhận; chưa chạy thử phát bằng buổi Slide Show qua giao diện. Tài liệu không tự chứng minh sinh viên đã hiểu code; phần câu hỏi hỗ trợ tập giải thích.
