# Thứ tự code tiếp theo

Giữ đúng phạm vi một người, bốn cử chỉ và một LSTM. Chưa làm thêm điều khiển con trỏ hoặc giao diện lớn.

1. **Camera và landmark — đã triển khai:** camera.py và landmarks.py, lệnh preview có hiển thị và thoát sạch. Người dùng đã xác nhận nhận được tay trên webcam của mình.
2. **Bộ thu đã triển khai, cần dữ liệu thật:** collect có nhãn/đếm ngược/retry/resume; lưu AVI sạch, NPZ [30,44], timestamp và metadata phiên. Chạy thu thử 10 clip/nhãn theo docs/COLLECTION.md.
3. **Chuẩn bị dữ liệu — đã thực hiện:** dataset-check xác nhận 150/50/50 clip trong train/validation/test.
4. **LSTM — đã triển khai:** lệnh train lưu checkpoint có validation loss thấp nhất.
5. **Đánh giá clip — đã triển khai:** lệnh evaluate tải checkpoint và xuất accuracy, F1, ma trận nhầm lẫn của test vào outputs/evaluation.json.
6. **Chạy webcam:** triển khai app.py ở chế độ chỉ nhận diện, sau đó control.py; F8/F9 toàn cục, nền ổn định và cooldown trước khi phát lệnh tiếp.
7. **Demo và báo cáo:** 40 lượt thao tác, năm phút nền; ghi kết quả thật và giới hạn.

CLI check/preview/collect/dataset-check/train/evaluate đã chạy được. Extract/run còn trả exit code 2. Collect đã trích đặc trưng trực tiếp; extract riêng chỉ cần khi bổ sung quy trình xử lý lại video.

Với mỗi thuật toán mới, thêm kiểm tra đúng lỗi cần phòng: sai chiều vuốt, mất quỹ đạo do chuẩn hóa, trộn phiên dữ liệu, lặp lệnh và lệnh chạy lại sau tạm dừng. Không cần test cho tệp giữ chỗ hoặc nội dung README.
