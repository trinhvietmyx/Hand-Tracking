from pathlib import Path
import json
S=Path(__file__).resolve().parent
O=S.parent
C=json.loads((S/'qa/package_checks.json').read_text(encoding='utf-8'))
assert C['qa_status']=='PASS'
qa='''# Kiểm tra bản chỉnh theo góp ý GVHD tuần 2

Ngày 07/11/2026; buổi báo cáo online theo lịch sinh viên cung cấp: 08/11/2026 từ 14:00, giờ Việt Nam.

## Phạm vi sửa và giữ nội dung người dùng

Chỉ thay nội dung slide **4, 8, 15, 16** để làm rõ bài IPN HandS, đối chiếu với code, giải thích các hàm và ưu tiên đọc hiểu trước khi mở rộng. **12 slide khác giữ nguyên XML từng byte**, gồm bìa và các chỉnh sửa người dùng đã thực hiện. File cũ `reports/progress/Bao_Cao_Tien_Do.pptx` không bị ghi đè, SHA-256 vẫn khớp bản đầu lượt.

Bìa giữ học vị **PGS.TS. Võ Đình Bảy** theo file hiện tại của người dùng; notes/báo cáo đồng bộ theo bìa, không coi đây là xác minh học vị từ nguồn công khai. Notes không còn mô tả hình bìa là ảnh webcam. Log giữ nguyên: `slide_sources/qa/user_edits_preservation.json`.

## Bài báo và mã nguồn

Đã đọc lại mục 5.1–5.3, trang 13–15, PDF IPN HandS: 42 tọa độ xy, ba tầng LSTM 256, dropout 0,3, phân loại 14 cử chỉ, bỏ nền, chia 37/13 người, tối đa 64 frame và stride 32 cho chuỗi dài, không padding/nội suy chuỗi ngắn. Bảng 6: accuracy 91,2 ± 1,4%, average recall 78,0 ± 1,2%. Đồ án dùng dữ liệu/cấu hình khác; không so sánh trực tiếp các tỷ lệ để khẳng định cải tiến.

Đã xem [README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) và [model.py của repo tác giả](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py). README mô tả dữ liệu HandS; model.py được xem thuộc benchmark CNN IPN Hand trước đó. **Chưa xác minh đường chạy LSTM tương ứng thí nghiệm 2025, chưa chạy lại thí nghiệm gốc.** MDPI có lúc trả HTTP 429; phương pháp và số liệu được đọc từ PDF đã cung cấp trong project.

Ghi chú và hướng dẫn phân biệt mã tác giả với mã đồ án; không ghi sinh viên đã hiểu/tái lập bài chỉ vì tài liệu đã được soạn. Giữ đánh số [1]–[7], nguồn gốc và các bảng của ba nghiên cứu trong references.md.

## Kiểm tra chạy code đồ án

Đã chạy `trace_current_model.py` trên một clip test BACKGROUND đã lưu:

```text
[1,30,44] → [1,30,64] → [1,64] → [1,5]
```

Đường tách từng bước trùng `model(x)`. Nhãn thật/dự đoán đều BACKGROUND; confidence khoảng 0,99244. Đây là kiểm tra luồng thực thi một mẫu, không phải phép đo accuracy mới, thử webcam trực tiếp hoặc tái lập IPN HandS. Không train hoặc ghi đè trọng số.

Các số liệu đã kiểm tra trước được giữ: 250 clip, train/validation/test 150/50/50, checkpoint epoch 23, 40/50 clip đúng, Macro-F1 0,7619; log 30 epoch và 60 test tự động đã qua. Dữ liệu biểu đồ khớp JSON/CSV/cache. Video nhúng khớp bytes với MP4 nguồn.

Snapshot trước có 539 tệp. **536 tệp còn hiện diện khớp mã băm.** Ba tệp `documents/Base/*.md` đã không còn tại vị trí cũ khi bắt đầu đọc kiểm tra lượt hiện tại, trước khi sửa báo cáo. Không khẳng định cả 539 tệp còn nguyên vị trí; không sửa snapshot cũ hoặc tạo lại tài liệu đã mất. Danh sách thiếu được ghi trong `qa/package_checks.json`. Các đoạn dẫn đặc tả từ bộ báo cáo trước thuộc snapshot trước.

## Kiểm tra trình chiếu và PDF

PowerPoint mở được **16 slide 16:9**, **7 bảng**, **2 biểu đồ kèm 2 workbook chỉnh được**, sơ đồ native và video **10.000 ms ở slide 12**. Đã render đủ 16 slide thành PNG 1.600 × 900 và xem từng slide; kiểm tra BoundHeight/BoundWidth không phát hiện phần tràn. Bản PDF có 16 trang, trích xuất được tên sinh viên/chữ Việt, render được các trang và kiểm tra các trang bổ sung.

Validator Office XML báo PASSED về XML, ID, relationships, content types, chart và không có lỗi XSD mới. Một số part không có schema được bỏ qua; mở/render PowerPoint là bước kiểm chứng thêm. PDF chỉ hiển thị poster video. Chưa thử phát bằng buổi Slide Show qua giao diện. Poppler cảnh báo font phụ Symbol/ArialUnicode; các trang đã xem vẫn hiện đúng chữ Việt và ký hiệu.

Log: `slide_sources/qa/office_validation.txt`, `powerpoint_checks.json`, `package_checks.json`. Ảnh: `qa/previews/`, `qa/pdf_previews/`.

## Phần chưa có thực nghiệm

Chưa có dữ liệu thực nghiệm về FPS toàn luồng, latency ổn định, 40 lượt điều khiển trực tiếp, 5 phút nền và người chưa xuất hiện trong train. Chưa tái lập mô hình LSTM gốc. Không diễn giải một lần trace code thành bằng chứng sinh viên đã hiểu toàn bộ chương trình.
'''
(O/'qa_report.md').write_text(qa,encoding='utf-8')
# Make this revision's archive independent of the previous delivery archive.
p=S/'package_outputs.py'
t=p.read_text(encoding='utf-8')
t=t.replace("'speaker_notes.md','references.md','qa_report.md'", "'speaker_notes.md','references.md','qa_report.md','Huong_dan_doc_bai_bao_va_code.md'")
t=t.replace("archive = output.parent/'Bao_Cao_Tien_Do_2026-11-08.zip'", "archive = output.parent.parent/'Bao_Cao_Theo_Gop_Y_GVHD_2026-11-08.zip'")
p.write_text(t,encoding='utf-8')
print('Revision QA and packaging instructions finalized.')
