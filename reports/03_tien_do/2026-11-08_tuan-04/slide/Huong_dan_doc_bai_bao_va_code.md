# Học và trình bày theo góp ý của thầy ở tuần 2

Thứ tự cần nắm: **nghiên cứu nào đã làm trước → bài đó làm như thế nào → code thực hiện điều đó ra sao → kết quả của mình → phần dự định mở rộng**.

Không cần bắt đầu bằng việc học hết mọi mô hình trong sáu bài. Đọc sâu một bài sát hướng đang làm, dùng hai bài còn lại để biết hướng khác và giới hạn so sánh. Góp ý của thầy được hiểu theo lời sinh viên cung cấp; “code” có thể bao gồm mã tác giả và mã đồ án. Cần phân biệt rõ hai nguồn này khi trình bày.

## 1. Bài chính cần đọc

**IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition.** Gibran Benitez-Garcia, Jesus Olivares-Mercado, Gabriel Sanchez-Perez, Hiroki Takahashi. *Applied Sciences*, 15(11), 6321, 2025. DOI: [10.3390/app15116321](https://doi.org/10.3390/app15116321).

PDF trong project: `reference/06_IPN_HandS_Applied_Sciences_2025/06_IPN_HandS_Applied_Sciences_2025.pdf`.

Mở PDF và đọc theo thứ tự sau. Sau mỗi bước, viết lại bằng lời của mình trước khi nhìn phần hướng dẫn tiếp.

1. **Abstract và Introduction:** xác định vấn đề và đóng góp. Bài quan tâm việc sửa chất lượng nhãn điểm bàn tay và khoảng thời gian cử chỉ. LSTM là mô hình dùng để đo ảnh hưởng của chất lượng dữ liệu. Chỉ nói “bài dùng LSTM” thì chưa giải thích được công trình.
2. **Mục 5.1, trang 13–14:** vẽ lại đầu vào là chuỗi 21 điểm xy, tức 42 giá trị mỗi bước; qua ba tầng LSTM, mỗi tầng 256 nút ẩn; trạng thái cuối qua lớp phân loại 14 cử chỉ. Có dropout 0,3 giữa các tầng.
3. **Mục 5.2, trang 14:** ghi rõ 50 người, chia 37 người train và 13 người test. Chuỗi dài được chia cửa sổ tối đa 64 frame, stride 32; chuỗi ngắn không padding/nội suy. Bài loại nền khỏi phép thử phân loại 14 cử chỉ. Huấn luyện 30 epoch, batch 64, Adam, learning rate 0,001, lặp ba lần.
4. **Bảng 6, trang 15:** giải thích accuracy 91,2 ± 1,4% và average recall 78,0 ± 1,2%. Hiểu tại sao bài có thể accuracy cao nhưng nhận một số lớp kém: số lượng các lớp khác nhau, nên cần xem recall trung bình theo lớp.
5. **Discussion/Limitations:** ghi phạm vi nào bài đã đánh giá và việc nào chưa thể suy ra khi đưa sang webcam/điều khiển của mình.

Sau khi đọc, tự trả lời sáu câu: Ai làm, công bố ở đâu? Họ giải quyết vấn đề gì? Dữ liệu từ đâu? Đầu vào và đầu ra là gì? Mô hình chạy từng bước ra sao? Kết quả nào trong bảng hỗ trợ kết luận của họ?

## 2. Kiểm tra đúng code của bài báo

[Repo tác giả](https://github.com/GibranBenitez/IPN-hand) hiện có [README riêng cho HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md). Trang này mô tả dữ liệu landmark và nhãn đã công bố. [model.py ở nhánh được kiểm tra](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) là bộ chọn mô hình CNN cho benchmark IPN Hand trước đó.

**Hiện chưa xác minh được đường chạy LSTM tương ứng thí nghiệm IPN HandS 2025 và chưa chạy lại kết quả gốc.** Việc này khác với việc code LSTM trong đồ án đã chạy được. Không nói đã chạy code tác giả hoặc đã tái lập bài báo khi mới chạy code riêng.

Nếu tiếp tục tái lập: xác minh file/commit đúng với bài 2025, đọc cách nạp landmark và nhãn, đối chiếu chia train/test và cấu hình, chạy một batch nhỏ rồi mới huấn luyện. Ghi lại phiên bản mã, dữ liệu, câu lệnh và log. Nếu chưa tìm thấy mã LSTM, trình bày rõ phần triển khai lại từ mô tả và phần chưa đủ thông tin để tái lập.

## 3. Đọc code đồ án theo đường đi dữ liệu

Mở thư mục `src/hand_tracking/` và đọc các hàm sau theo thứ tự.

**Bước 1 — `features.py`, hàm `extract_features`.** MediaPipe cung cấp 21 điểm, mỗi điểm lấy x/y. Hàm đổi tọa độ về cùng đơn vị ảnh, trừ vị trí cổ tay và chia kích thước lòng bàn tay. 21 × 2 = 42 giá trị mô tả hình dạng bàn tay; nối hai tọa độ cổ tay thành 44. Hãy giải thích được: nếu bỏ hết vị trí cổ tay thì thông tin bàn tay đi về đâu trong ảnh có thể bị giảm; hiệu quả thật của hai giá trị thêm cần thử bỏ/giữ để đo.

**Bước 2 — `features.py`, lớp `SequenceBuffer`, hàm `push`.** Hàm nhận một vector 44 số và thời gian. Cấu hình lấy mẫu cách 50 ms, đủ 30 mẫu thì trả chuỗi 30 × 44. Mất tay hoặc khoảng trống quá 100 ms thì xóa chuỗi. “30” là số bước của chuỗi, “44” là số đặc trưng mỗi bước. 20 Hz là nhịp lấy mẫu, chưa phải FPS đo toàn hệ thống.

**Bước 3 — `model.py`, `GestureLSTM.__init__` và `forward`.** Đọc ba dòng chính:

```python
sequence, _ = self.lstm(features)
last = sequence[:, -1, :]
logits = self.classifier(last)
```

Với một mẫu, các kích thước chạy thật là:

```text
[1, 30, 44] → [1, 30, 64] → [1, 64] → [1, 5]
```

Số 1 là batch đang kiểm tra; 30 là số bước thời gian; 44 là đặc trưng; 64 là kích thước trạng thái ẩn; 5 là số nhãn. `[:, -1, :]` chọn trạng thái ở thời điểm cuối cho từng mẫu. Lớp Linear biến 64 giá trị thành năm điểm số. Đừng gọi năm điểm số này là xác suất trước khi áp dụng softmax.

**Bước 4 — `model.py`, `predict_gesture`.** Đọc chỗ thêm chiều batch, gọi mô hình, tính softmax và lấy nhãn có điểm cao nhất. MediaPipe tìm vị trí điểm bàn tay; LSTM mới là phần phân loại chuỗi thành cử chỉ trong project này.

**Bước 5 — `training.py`, `train_model`.** Lần theo `load_split` → `DataLoader` → `model(features)` → `CrossEntropyLoss` → `loss.backward()` → `optimizer.step()` → validation → lưu checkpoint. Code dùng batch 16, Adam 0,001, seed 42; log có 30 epoch. Chỉ lưu khi validation loss giảm. Test không được dùng để chọn checkpoint.

**Bước 6 — `evaluation.py`, `evaluate_model`.** Xem cách lấy nhãn dự đoán, cộng ma trận với hàng thật/cột dự đoán, tính accuracy và F1. Kết quả 40/50 clip là đánh giá phân loại clip đã lưu. Hiểu riêng tại sao vuốt lên recall chỉ 0,1.

**Bước 7 — `app.py` và `control.py`.** Sau khi hiểu phân loại, mới đọc cách nạp webcam, ghép chuỗi và đưa dự đoán qua xác nhận lệnh. Cần giải thích ngưỡng 0,8, giữ ổn định, khoảng nghỉ, chờ nền, F8/F9. Có mã này chưa đủ chứng minh mọi thao tác trực tiếp đều thành công.

## 4. Một phép chạy để nhìn tận mắt kích thước tensor

Tại thư mục project, chạy:

```powershell
& .venv/Scripts/python.exe reports/03_tien_do/2026-11-08_tuan-04/slide/slide_sources/trace_current_model.py
```

Script chỉ đọc một clip test và checkpoint, tách từng bước tính rồi so với `model(x)`. Không huấn luyện hoặc ghi đè trọng số. Kết quả đã ghi trong `slide_sources/model_execution_trace.json`: đúng các kích thước trên, nhãn thật và dự đoán đều BACKGROUND. Đây là bài tập hiểu code, không phải kết quả tái lập code tác giả hoặc một phép đo accuracy mới.

## 5. Những khác biệt phải tự giải thích trước khi mở rộng

- Bài dùng 42 tọa độ; đồ án dùng 44 đặc trưng đã chuẩn hóa và giữ vị trí cổ tay.
- Bài dùng ba tầng 256; đồ án một tầng 64. Đây là khác cấu hình; hiện chưa có so sánh để kết luận cấu hình nào tốt hơn trên cùng dữ liệu.
- Bài phân loại 14 cử chỉ, bỏ nền; đồ án có bốn hướng và một lớp nền để phục vụ luồng điều khiển.
- Bài chia theo người; đồ án hiện chia theo phiên. Chưa có dữ liệu thực nghiệm về người chưa xuất hiện trong train.
- Các quy tắc phát lệnh thuộc ứng dụng của đồ án; không tự gán chúng thành đóng góp hoặc kết quả của IPN HandS.

Chỉ sau khi giải thích được các điểm này mới chọn một thay đổi có thể đo, ví dụ kiểm tra bỏ/giữ tọa độ cổ tay hoặc sửa quy cách thu động tác. Mỗi lần thay đổi một yếu tố, chọn bằng validation và giữ phiên đánh giá cuối riêng. Các phép so sánh này hiện là kế hoạch, chưa có số liệu thực nghiệm.

## 6. Cách nói trong buổi báo cáo

“Theo góp ý của thầy ở tuần 2, em tập trung đọc công trình IPN HandS, công bố trên Applied Sciences năm 2025. Bài sử dụng chuỗi điểm bàn tay và LSTM để đánh giá ảnh hưởng của chất lượng gán nhãn. Em xin trình bày đầu vào, mô hình, cách chia dữ liệu và kết quả ở Bảng 6; sau đó đối chiếu với các hàm trong code đồ án. Code hiện tại khác cấu hình và dữ liệu của bài. Phần chạy lại thí nghiệm gốc em chưa có minh chứng hoàn tất.”

Chỉ dùng các câu thể hiện mức độ đã hiểu sau khi bạn tự đọc và giải thích lại được. Nếu chưa đọc hết, nói đúng mục đã đọc và nội dung còn cần kiểm chứng. Khi được hỏi “code chạy thế nào”, mở `model.py` và đi qua ba dòng trên bằng kích thước tensor, rồi liên hệ với đầu ra của script trace.
