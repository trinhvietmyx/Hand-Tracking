# Kiểm tra bước camera → landmark → đặc trưng

Ngày: 30/10/2026. Môi trường Python 3.11/Windows của dự án; snapshot thư viện nằm ở requirements-vision.lock.txt.

## Đã thực hiện

- TDD: test mới fail trước triển khai; sau triển khai toàn bộ 26 test pass.
- Kiểm tra đặc trưng 44 chiều, tỷ lệ ảnh, tính bất biến hình dạng khi dịch/phóng tay và bảo toàn cổ tay toàn cục.
- Kiểm tra sampling 20 Hz, nội suy giữa mẫu đã nhận, không nhân đôi mẫu khi camera nhanh, reset khi mất tay/khoảng hở dài/dữ liệu lỗi.
- Kiểm tra camera release khi đọc lỗi, chiều gương, timestamp tăng và tracker release.
- Kiểm tra preview bằng biên I/O giả và thuật toán đặc trưng/buffer thật, bao gồm mất tay sau một chuỗi đầy.
- Kiểm tra lỗi truy vấn thuộc tính khi cửa sổ native đã đóng: preview thoát bình thường thay vì traceback; camera/tracker được giải phóng.
- Nạp model thật, suy luận ảnh đen: nhận `no_hand`.
- Ảnh mẫu một tay chính thức: nhận 21 điểm, tạo 44 đặc trưng hữu hạn; lặp đặc trưng tĩnh để xác nhận ghép được [30,44]. Đây không phải kiểm tra cử chỉ động.
- Ảnh mẫu hai tay với tracker mới: nhận hai tay và trả `multiple_hands`.
- Webcam thật, headless 30 frame: đọc thành công, khoảng 15,3 FPS trong lượt ngắn, không có tay được phát hiện.
- Webcam thật, cửa sổ OpenCV 15 frame: mở/đóng thành công, khoảng 12 FPS trong lượt ngắn, không có tay được phát hiện. Số đo gồm khởi động đọc camera, chưa phải benchmark ổn định.
- `pip check`: không có phụ thuộc hỏng.

Không lưu frame webcam, video hoặc ảnh mẫu tải về; ảnh mẫu chỉ được đọc vào RAM. Chưa thu dataset, huấn luyện LSTM hoặc gửi thao tác máy tính.

## Quan sát giới hạn tracker

Một phép thử ban đầu kỳ vọng model báo hai tay ngay ở frame đổi từ ảnh một tay sang ảnh hai tay đã thất bại. Kiểm tra tách biệt xác nhận tracker mới nhận hai tay ngay; cùng tracker VIDEO sau ảnh một tay báo một tay ở frame đổi cảnh đầu tiên, rồi hai tay từ frame kế tiếp. Đây là ảnh hưởng trạng thái theo dõi khi đổi cảnh đột ngột, không phải lỗi đếm hoặc chọn tay trong adapter.

Giữ VIDEO mode cho luồng camera liên tục. Ứng dụng xóa chuỗi ngay khi model báo nhiều tay; không khẳng định detector luôn thấy đủ số tay ngay lập tức.

## Chưa xác minh

- Chưa có bàn tay người dùng trong lượt chạy webcam nên chưa đánh giá chất lượng landmark thực tế, che ngón hoặc động tác vuốt trên camera này.
- Chưa đo dài hạn tốc độ/độ trễ khi có tay, chưa đánh giá phân loại cử chỉ vì chưa có mô hình LSTM.
- Chưa triển khai F8/F9 toàn cục; preview thoát bằng Q/Esc hoặc đóng cửa sổ đang nhận focus.

## Nguồn đối chiếu

- [Hướng dẫn MediaPipe Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python).
- [Test chính thức của MediaPipe](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/tasks/python/test/vision/hand_landmarker_test.py), dùng các mẫu `thumb_up.jpg` và `right_hands.jpg` từ bucket mediapipe-assets.
