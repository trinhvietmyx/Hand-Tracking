# Kết quả đánh giá clip

Từ thư mục Hand-Tracking, chạy lệnh sau sau khi đã huấn luyện và có dữ liệu test.

```powershell
.\run.bat evaluate
```

Lệnh in báo cáo JSON và lưu tệp `evaluation.json` trong thư mục này theo cấu hình mặc định. Báo cáo gồm accuracy, Macro-F1, precision/recall/F1 từng nhãn, ma trận nhầm lẫn và danh sách clip dự đoán sai. Hàng của ma trận là nhãn thật, cột là nhãn dự đoán.

Mỗi lần chạy thành công cập nhật tệp báo cáo. Kết quả sinh ra được bỏ qua bởi .gitignore.
