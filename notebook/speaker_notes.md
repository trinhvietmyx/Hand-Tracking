# Speaker notes — Báo cáo tiến độ Hand-Tracking với giảng viên hướng dẫn

Bản nói gợi ý khoảng **12–15 phút**, dùng cùng [notebook](hand_tracking.ipynb).
Các mục **1–7 đi theo đúng thứ tự trong notebook**. Phần hỏi đáp và tài liệu
tham khảo ở cuối dùng khi cần tra thêm.

**Cách dùng:** đọc phần **Lời nói gợi ý** theo cách nói của mình.
Phần **Thao tác** hướng dẫn mở notebook, PDF hoặc code, không đọc thành lời.
Khi thầy hỏi giữa chừng, trả lời vào câu hỏi rồi tiếp tục ở mục đang trình bày.

Số liệu đối chiếu ngày **08/11/2026**, lấy từ
`outputs/notebook/evaluation.json`. Nếu chạy lại với dữ liệu hoặc cấu hình
khác, cập nhật phần kết quả trước khi báo cáo.

## Chuẩn bị trước buổi gặp thầy

1. Mở PowerShell tại gốc dự án và khởi động JupyterLab:

   ```powershell
   cd D:\Learn\Hutech\DACN\Hand-Tracking
   .\.venv\Scripts\python.exe -m jupyterlab notebook
   ```

2. Mở `hand_tracking.ipynb`, chọn kernel **Python (Hand-Tracking)** và chạy
   **Run All Cells** từ trước. Notebook có phần huấn luyện 30 epoch.
3. Kiểm tra kết quả ở mục 5: epoch được chọn, accuracy, Macro-F1 và ma trận
   nhầm lẫn. Đối chiếu với số liệu đang ghi trong bản nói.
4. Mở sẵn PDF IPN HandS ở trang 13–15 và các tệp code cần giải thích.
5. Khi báo cáo, cuộn notebook từ trên xuống. Đến mục 5.3 và 5.5 có thể
   chạy lại ô minh họa từng bước tính và ô mô phỏng `GestureGate`.

PDF chính:
`reference/06_IPN_HandS_Applied_Sciences_2025/06_IPN_HandS_Applied_Sciences_2025.pdf`.

## Mở đầu — khoảng 30 giây

**Thao tác:** mở đầu notebook.

**Lời nói gợi ý**

“Dạ thưa thầy, hôm nay em xin báo cáo phần tìm hiểu tài liệu và phần code
hiện tại của đồ án nhận diện cử chỉ tay để chuyển slide, cuộn trang.

Theo góp ý của thầy, em bắt đầu từ các công trình đã có, sau đó chọn một
bài gần với hướng đồ án để đọc kỹ hơn. Từ bài đó, em đối chiếu với code,
chạy thử và xem kết quả đang đúng, sai ở đâu.

Đầu tiên, em xin trình bày các bài em đã tổng hợp.”

## 1. Các công trình đã nghiên cứu — khoảng 1 phút 30 giây

**Thao tác:** mở mục 1 của notebook. Chỉ lần lượt sáu dòng trong bảng
theo thứ tự **R1 → R6**. Khi cần xác nhận nguồn, mở thông tin bài ngay
bên dưới bảng.

**Lời nói gợi ý**

“Trong phần này, em tổng hợp sáu công trình có liên quan đến nhận diện
cử chỉ tay động. Mỗi bài em có ghi tên, nơi công bố, năm và đường dẫn
để đối chiếu.

Bài đầu tiên là S2Gest, công bố tại ECCV 2026. Bài này xử lý đặc trưng
video theo thời gian bằng mô hình trạng thái.

Bài thứ hai là SKETCH, tại NeurIPS 2025. Hướng của bài là chuyển chuỗi
điểm khớp thành ảnh quỹ đạo để đưa vào mô hình thị giác.

Bài thứ ba là GESTRO, trên Journal of Intelligent & Robotic Systems
năm 2026. Bài dùng chuỗi điểm đặc trưng và LSTM có attention cho bài toán
điều khiển robot.

Bài thứ tư là ConvMixFormer, tại WACV 2025. Bài nghiên cứu cách kết hợp
tích chập trong kiến trúc nhận diện cử chỉ từ video.

Bài thứ năm là bài tổng quan Continuous Hand Gesture Recognition,
trên Computer Vision and Image Understanding năm 2025. Em dùng bài này
để tìm hiểu các bộ dữ liệu và cách đánh giá nhận diện liên tục.

Bài cuối là IPN HandS, trên Applied Sciences năm 2025. Em chọn bài này
để đọc kỹ hơn vì phần thực nghiệm dùng tọa độ bàn tay 2D và LSTM,
gần với cách xử lý trong đồ án hiện tại.”

**Nếu thầy hỏi rõ nguồn bài chính**

“Dạ, tên đầy đủ là *IPN HandS: Efficient Annotation Tool and Dataset for
Skeleton-Based Hand Gesture Recognition*, của Gibran Benitez-Garcia
và các đồng tác giả. Bài được đăng trên Applied Sciences năm 2025.
Em có để link công bố và DOI ở đây.”

**Thao tác:** chỉ mục **[R6]**; mở
[trang công bố IPN HandS](https://www.mdpi.com/2076-3417/15/11/6321)
nếu cần. Không cần đọc toàn bộ danh sách tác giả và DOI thành lời.

**Chuyển ý**

“Tiếp theo, em xin đi vào bài IPN HandS: tác giả giải quyết vấn đề gì,
dùng mô hình như thế nào và đánh giá ra sao.”

## 2. Nghiên cứu công trình IPN HandS — khoảng 3 phút

### 2.1. Vấn đề và đóng góp

**Thao tác:** mở mục 2.1 trong notebook; có thể chỉ phần Introduction
và mục 3 của PDF.

**Lời nói gợi ý**

“Điểm chính của bài này là chất lượng dữ liệu các điểm bàn tay.
Khi lấy điểm tự động, có những khung hình bị mất điểm hoặc đặt điểm
chưa đúng. Việc xác định lúc nào cử chỉ bắt đầu, kết thúc cũng ảnh hưởng
đến dữ liệu dùng để học.

Tác giả xây dựng công cụ hỗ trợ lấy điểm ban đầu, sửa bằng tay và nội suy,
rồi tạo bộ dữ liệu IPN HandS đã được tinh chỉnh.

Sau đó, tác giả dùng LSTM làm mô hình cơ sở, hay baseline, để xem chất
lượng gán nhãn ảnh hưởng đến kết quả nhận diện như thế nào.”

### 2.2. Kiến trúc

**Thao tác:** mở mục 2.2 trong notebook và mục 5.1 của PDF, trang 13–14.

**Lời nói gợi ý**

“Ở phần nhận diện, tác giả chọn một tay chính. Mỗi khung hình có 21 điểm,
mỗi điểm lấy hai tọa độ x và y, nên đầu vào có 42 giá trị.

Chuỗi tọa độ đi qua ba tầng LSTM một chiều, mỗi tầng có kích thước trạng
thái ẩn là 256. Sau đó, trạng thái ở bước cuối được đưa qua một lớp
phân loại để tạo điểm số cho 14 cử chỉ. Giữa các tầng có dropout.”

**Chỉ sơ đồ, giải thích ngắn**

```text
[B, T, 42] → LSTM 3 tầng, hidden 256 → [B, 256] → Linear → [B, 14]
```

“Trong sơ đồ này, B là số mẫu xử lý cùng lúc, còn T là số bước thời gian.”

### 2.3. Cách làm thí nghiệm

**Thao tác:** mở mục 2.3; chỉ mục 5.2 của PDF, trang 14.

**Lời nói gợi ý**

“Về dữ liệu, bài có 50 người và chia thành 37 người để huấn luyện,
13 người để kiểm tra, tương ứng 148 và 52 video. Như vậy, người ở tập
kiểm tra khác người ở tập huấn luyện.

Thí nghiệm này có 14 lớp cử chỉ và loại các đoạn không có cử chỉ.
Với chuỗi dài, tác giả chia thành các cửa sổ tối đa 64 khung hình,
dịch mỗi lần 32 khung hình. Chuỗi ngắn thì giữ độ dài.

Tác giả dùng Adam, learning rate 0,001, batch 64, huấn luyện 30 epoch
và chạy thí nghiệm ba lần.”

### 2.4. Kết quả trong bài

**Thao tác:** chỉ ảnh **Bảng 6** ở mục 2.4 hoặc mở PDF trang 15.

**Lời nói gợi ý**

“Đây là Bảng 6 trong bài. Với dữ liệu IPN HandS, accuracy đạt 91,2 phần
trăm, còn recall trung bình theo lớp là 78 phần trăm.

Accuracy cho biết tỷ lệ dự đoán đúng trên toàn bộ mẫu. Recall trung bình
giúp xem khả năng nhận ra các lớp khi mỗi lớp được tính ngang nhau.
Vì số mẫu giữa các lớp khác nhau, em cần xem cả hai chỉ số.”

**Nếu thầy hỏi ký hiệu ± trong bảng**

“Dạ, đây là độ lệch chuẩn qua ba lần chạy. Với accuracy là 1,4 điểm
phần trăm, còn recall trung bình là 1,2 điểm phần trăm.”

### 2.5. Điều tiếp thu cho đồ án

**Thao tác:** chuyển xuống mục 2.5.

**Lời nói gợi ý**

“Từ bài này, hướng em tham khảo là dùng chuỗi tọa độ bàn tay làm đầu vào
cho LSTM. Một điểm nữa là cần kiểm tra chất lượng dữ liệu và cách chia
tập trước khi nhìn vào kết quả.

Em cũng cần phân biệt kết quả tác giả công bố với kết quả em chạy trên
dữ liệu của đồ án. Hai bên có cách làm thí nghiệm khác nhau, nên chưa
thể dùng hai con số để kết luận mô hình nào tốt hơn.”

**Chuyển ý**

“Sau phần đọc bài, em kiểm tra tiếp mã nguồn tác giả công bố để xem có
thể đối chiếu phương pháp với code đến đâu.”

## 3. Mã nguồn công bố từ bài báo — khoảng 1 phút 30 giây

### 3.1. Chuẩn bị để đọc và chạy code

**Thao tác:** đi qua ô thiết lập ở mục 3.1. Nếu đã chạy từ trước thì chỉ
cần xác nhận kernel và đường dẫn dự án; không đọc từng dòng import.

**Nếu cần giải thích**

“Ô này chuẩn bị môi trường để các phần sau gọi đúng code của đồ án.
Phần huấn luyện trong notebook dùng checkpoint riêng.”

### 3.2. Đối chiếu code được công bố

**Thao tác:** chỉ phần kiểm tra mã nguồn IPN-hand, rồi đến ví dụ
`SwinWithRegressor.forward` của SKETCH ở mục 3.2.

**Lời nói gợi ý**

“Với IPN HandS, bản mã nguồn em đang có có README mô tả bộ dữ liệu HandS.
Tuy nhiên, tệp model.py em kiểm tra đang chọn các mạng CNN của benchmark
IPN Hand trước đó. Em chưa tìm được đầy đủ phần chạy LSTM tương ứng với
thí nghiệm HandS 2025 để chạy lại kết quả trong bài.

Vì vậy, ở phần này em trình bày những gì đã đối chiếu được từ PDF và code.

Để minh họa cách đọc code tác giả, em có thêm ví dụ từ SKETCH.
Trong hàm forward này, chuỗi tọa độ được xử lý qua MLP, kết hợp với ảnh
biểu diễn quỹ đạo, rồi đưa qua Swin và các đầu ra.

Khi đọc hàm này, em theo ba ý: đầu vào có dạng gì, đi qua các phép xử lý
nào và đầu ra dùng để làm gì. Hiện phần này là đọc code; em chưa chạy lại
toàn bộ thí nghiệm của SKETCH.”

### 3.3. Hướng đang dùng trong đồ án

**Thao tác:** mở bảng đối chiếu ở mục 3.3.

**Lời nói gợi ý**

“Quay lại đồ án, code hiện tại dùng hướng tọa độ bàn tay 2D và LSTM,
nhưng có một số khác biệt với bài IPN HandS.

Bài dùng 42 giá trị mỗi bước, ba tầng LSTM với hidden size 256 và
14 lớp. Đồ án đang dùng 44 giá trị, một tầng LSTM với hidden size 64
và năm nhãn: bốn hướng vuốt cùng lớp nền.

Đây là cấu hình khởi đầu đang dùng trong đồ án. Em chưa có thí nghiệm
so sánh nhiều cấu hình để kết luận đây là lựa chọn tối ưu.”

**Chuyển ý**

“Tiếp theo, em xin đi theo luồng dữ liệu của đồ án, từ lúc thu một clip
đến khi đưa được chuỗi vào mô hình.”

## 4. Code đồ án theo đường đi dữ liệu — khoảng 2 phút

### 4.1. Thu và kiểm tra dữ liệu

**Thao tác:** mở mục 4.1, chỉ danh sách nhãn và thống kê các tập dữ liệu.

**Lời nói gợi ý**

“Đồ án hiện có 250 clip tự thu, gồm 150 clip huấn luyện, 50 clip
validation và 50 clip test. Các tập được tách theo phiên thu.

Mỗi clip có một trong năm nhãn ở đây. Bốn nhãn là vuốt trái, phải,
lên, xuống; BACKGROUND là lớp nền, không thực hiện một lần vuốt cần
điều khiển.

Khi thu, chương trình lưu video để xem lại và lưu cả dữ liệu điểm bàn
tay cùng đặc trưng để đưa vào mô hình.”

### 4.2. Trích đặc trưng và ghép chuỗi

**Thao tác:** mở mục 4.2; chỉ hàm `extract_features()` và lớp
`SequenceBuffer` trong `src/hand_tracking/features.py`.

**Lời nói gợi ý**

“MediaPipe lấy ra 21 điểm bàn tay. Ở bước tạo đặc trưng, code đưa hai
trục về cùng đơn vị, lấy cổ tay làm gốc và chuẩn hóa theo kích thước
lòng bàn tay. Phần này tạo 42 giá trị mô tả hình dạng bàn tay.

Code giữ thêm hai tọa độ cổ tay trong ảnh, nên mỗi bước có tổng cộng
44 giá trị. Hai tọa độ này thể hiện bàn tay đang di chuyển đến đâu.
Hiện em chưa làm thí nghiệm bỏ và giữ hai tọa độ này để đo riêng mức
ảnh hưởng của chúng.”

**Thao tác:** chỉ hình các điểm bàn tay và quỹ đạo cổ tay, rồi đến phần bộ đệm.

“Sau khi có một vector 44 giá trị, code đưa nó cùng thời gian của khung
hình vào bộ đệm. Nhịp lấy mẫu là 20 lần mỗi giây, tức cách nhau
50 mili giây.

Khi đủ 30 bước, bộ đệm trả về một chuỗi kích thước 30 nhân 44,
tương ứng khoảng một giây rưỡi chuyển động.

Nếu không còn tay hợp lệ hoặc khoảng gián đoạn tracking dài hơn
100 mili giây thì bộ đệm được xóa. Các khoảng ngắn hơn được nội suy
giữa hai lần quan sát hợp lệ.”

**Thao tác:** chỉ kết quả phát lại landmark và kiểm tra đặc trưng khớp
với dữ liệu đã lưu trong NPZ.

### 4.3. Kiến trúc LSTM của đồ án

**Thao tác:** mở mục 4.3 và lớp `GestureLSTM` trong
`src/hand_tracking/model.py`.

**Lời nói gợi ý**

“Đến đây, một mẫu đã có 30 bước, mỗi bước 44 đặc trưng.
Mô hình có một tầng LSTM với 64 chiều trạng thái ẩn.
Trạng thái ở bước cuối được đưa qua Linear để tạo năm điểm số cho
năm nhãn.

Em sẽ minh họa cụ thể từng kích thước ở phần chạy forward phía dưới.
Trước đó, em xin trình bày cách mô hình được huấn luyện.”

## 5. Huấn luyện, chạy dự đoán và đọc kết quả — khoảng 3 phút 30 giây

### 5.1. Vòng lặp huấn luyện

**Thao tác:** mở mục 5.1 và hàm `train_model()` trong
`src/hand_tracking/training.py`.

**Lời nói gợi ý**

“Code huấn luyện đọc hai tập train và validation.
Mỗi batch có 16 mẫu, bộ tối ưu là Adam với learning rate 0,001,
và seed được đặt là 42.

Trong một batch, các bước chính nằm ở đoạn này.”

```python
optimizer.zero_grad()
logits = model(features)
loss = criterion(logits, labels)
loss.backward()
optimizer.step()
```

“Đầu tiên là xóa gradient của lượt trước, sau đó cho mô hình dự đoán
và tính cross-entropy so với nhãn đúng. Tiếp theo, backward tính
gradient, rồi optimizer cập nhật trọng số.

Sau mỗi epoch, code đo loss trên validation. Khi validation loss
giảm thì lưu lại trọng số, tức checkpoint.

Lượt chạy hiện tại có 30 epoch. Checkpoint được chọn ở epoch 23
vì có validation loss thấp nhất trong lượt chạy này.”

### 5.2. Tải checkpoint và dự đoán một clip

**Thao tác:** mở mục 5.2; chỉ `load_gesture_model()` và
`predict_gesture()` trong `model.py`, rồi xem kết quả một clip.

**Lời nói gợi ý**

“Huấn luyện xong, em tải checkpoint đã được chọn và chuyển mô hình
sang chế độ đánh giá.

Ở đây em lấy một clip để thử. Hàm predict_gesture đưa chuỗi vào mô hình,
dùng softmax để có phân bố xác suất dự đoán, rồi lấy nhãn có giá trị
cao nhất.

Kết quả một clip giúp em kiểm tra luồng dự đoán có chạy được.
Để biết mô hình làm tốt đến đâu thì cần xem toàn bộ tập test ở phần sau.”

### 5.3. Đi từng bước trong forward

**Thao tác:** mở và có thể chạy lại ô ở mục 5.3.
Chỉ lần lượt đầu ra của ba dòng chính.

```python
recurrent_outputs, _ = model.lstm(batch)
last_hidden = recurrent_outputs[:, -1, :]
logits = model.classifier(last_hidden)
```

**Lời nói gợi ý**

“Ở ô này, em tách forward ra để xem dữ liệu đổi kích thước như thế nào.

Ban đầu một clip có kích thước 30 nhân 44. Thêm chiều batch thì thành
1 nhân 30 nhân 44, vì đang dự đoán một clip.

Sau LSTM, đầu ra là 1 nhân 30 nhân 64. Dòng thứ hai chọn bước thời gian
cuối cùng, giữ 64 giá trị nên còn 1 nhân 64.

Linear chuyển thành 1 nhân 5, tương ứng năm điểm số đầu ra.
Sau softmax, em lấy nhãn có xác suất dự đoán cao nhất.

Code cũng kiểm tra kết quả tính tách từng bước có khớp với gọi
model(batch) hay không. Nhờ vậy, em đối chiếu được cách đọc forward
với kết quả chạy thực tế.”

### 5.4. Đánh giá toàn bộ tập test

**Thao tác:** mở mục 5.4, chỉ accuracy, Macro-F1 và ma trận nhầm lẫn.
Nguồn số liệu là `outputs/notebook/evaluation.json`.

**Lời nói gợi ý**

“Trên 50 clip test, mô hình dự đoán đúng 40 clip, tức accuracy
80 phần trăm. Macro-F1 khoảng 0,7619.

Trong ma trận này, hàng là nhãn thật, cột là nhãn dự đoán.
Ba lớp nền, vuốt trái và vuốt phải đều đúng 10 trên 10 clip
của từng lớp trong tập test hiện tại.

Lỗi tập trung ở hai hướng dọc. Vuốt lên chỉ đúng một clip,
còn chín clip bị đoán thành vuốt xuống.
Vuốt xuống đúng chín clip và có một clip bị đoán thành vuốt lên.

Như vậy, em đã thấy cụ thể nhóm mẫu nào đang sai.
Còn nguyên nhân thì em cần xem lại video, điểm bàn tay và nhãn.
Hiện em chưa đủ kiểm chứng để kết luận lỗi do dữ liệu hay do mô hình.”

**Nếu thầy hỏi thêm về Macro-F1**

“Dạ, Macro-F1 là trung bình F1 của từng lớp, mỗi lớp được tính ngang nhau.
Chỉ số này giúp em nhìn thêm chất lượng giữa các lớp bên cạnh tỷ lệ đúng
trên toàn bộ mẫu.”

### 5.5. Từ dự đoán clip đến ứng dụng webcam

**Thao tác:** mở mục 5.5 và ô mô phỏng `GestureGate`.
Chỉ `app.py`, `control.py` nếu thầy muốn xem code.

**Lời nói gợi ý**

“Khi chạy webcam bằng mục 7 trong run.bat, chương trình cũng lấy điểm
bàn tay, tạo đặc trưng rồi ghép chuỗi như phần vừa trình bày.

Ứng dụng bắt đầu ở trạng thái tắt điều khiển. F8 dùng để bật hoặc tạm
dừng, còn F9 để thoát.

Khi bật điều khiển, dự đoán phải qua GestureGate trước khi gửi lệnh.
Gate yêu cầu độ tin cậy từ 80 phần trăm, ít nhất ba dự đoán mới cùng
nhãn và ổn định ít nhất 150 mili giây.

Sau khi xác nhận một lần vuốt, gate khóa lại. Muốn nhận lần tiếp theo
thì phải qua một giây và thấy lớp nền đủ tin cậy, ổn định ít nhất
300 mili giây. Mục đích là tránh một lần vuốt gửi lệnh lặp nhiều lần.”

**Nếu minh họa bằng ô mô phỏng**

“Ở các mốc 0, 50 và 100 mili giây, tuy đã có ba dự đoán nhưng mới kéo dài
100 mili giây. Đến mốc 150 mili giây thì mới đủ cả điều kiện số lần
và thời gian.”

**Ánh xạ của code hiện tại khi demo**

- Vuốt trái → phím mũi tên trái → slide trước.
- Vuốt phải → phím mũi tên phải → slide tiếp theo.
- Vuốt lên hoặc xuống → cuộn lên hoặc cuộn xuống.

**Chuyển ý**

“Phần webcam đã có luồng nhận diện và gửi lệnh. Tuy nhiên, kết quả
50 clip vừa rồi mới đánh giá phân loại clip. Em vẫn cần đo thêm
khả năng điều khiển khi dùng liên tục.”

## 6. Giới hạn hiện tại và việc cần làm tiếp — khoảng 45 giây

**Thao tác:** mở mục 6 trong notebook.

**Lời nói gợi ý**

“Hiện tại, dữ liệu được chia theo phiên thu, nên em chưa dùng kết quả
này để kết luận khả năng nhận diện với người mới.

Việc em dự định làm trước là kiểm tra các clip vuốt lên và vuốt xuống
đang nhầm. Sau đó, em chọn một thay đổi để thử và đo lại, ví dụ so sánh
khi giữ hoặc bỏ hai tọa độ cổ tay.

Khi điều chỉnh, em dùng validation để chọn cấu hình. Vì tập test hiện
tại đã được xem kết quả, nếu tiếp tục cải tiến theo những lỗi này thì
em cần thêm một tập kiểm tra độc lập cho lần đánh giá cuối.

Với webcam, em cần đo thêm số lệnh đúng, lệnh sai, số lần bỏ sót,
lặp lệnh và độ trễ. Những phần này hiện vẫn cần thực nghiệm tiếp.”

## 7. Kết thúc và xin ý kiến hướng dẫn — khoảng 30 giây

**Thao tác:** chuyển đến mục 7; dừng ở dàn ý báo cáo.

**Lời nói gợi ý**

“Dạ, đó là phần em đã tìm hiểu và kết quả chạy hiện tại.
Bài em tập trung đọc là IPN HandS; hướng đang dùng trong đồ án là
chuỗi tọa độ bàn tay 2D đưa vào LSTM. Vấn đề em thấy rõ nhất ở lượt chạy
này là nhầm giữa vuốt lên và vuốt xuống.

Em muốn xin ý kiến thầy về bước tiếp theo: em dự định kiểm tra lại
nhóm dữ liệu đang nhầm trước, rồi mới thử điều chỉnh mô hình.
Hướng làm như vậy đã phù hợp chưa ạ?”

## Phụ lục A. Gợi ý trả lời khi thầy hỏi

Chỉ dùng câu trả lời phù hợp với phần đã hiểu và đã kiểm tra.
Nếu chưa giải thích được một đoạn code, có thể mở đoạn đó để cùng đối chiếu.

### “Em đang theo bài nào?”

“Dạ, em tham khảo hướng landmark 2D và baseline LSTM ở mục 5 của bài
IPN HandS, đăng trên Applied Sciences năm 2025. Code đồ án đang dùng
cấu hình riêng và dữ liệu tự thu, như bảng đối chiếu em đã trình bày.”

### “Đóng góp chính của bài là gì?”

“Dạ, bài tập trung vào công cụ gán nhãn và bộ dữ liệu điểm bàn tay
được tinh chỉnh. LSTM là mô hình cơ sở để đánh giá ảnh hưởng của
chất lượng gán nhãn đến kết quả nhận diện.”

### “Em đã chạy lại code tác giả chưa?”

“Dạ, em đã đọc PDF và đối chiếu bản mã nguồn đang có. Em chưa tìm được
đầy đủ phần chạy LSTM của HandS 2025 để chạy lại đúng thí nghiệm gốc.
Kết quả em vừa trình bày là từ code đồ án trên dữ liệu tự thu.”

### “Tại sao lại dùng 44 đặc trưng?”

“Dạ, có 42 tọa độ tương đối để biểu diễn hình dạng bàn tay và hai
tọa độ cổ tay trong ảnh để giữ thông tin vị trí di chuyển. Em chưa
làm thí nghiệm bỏ và giữ hai tọa độ này để đo mức ảnh hưởng riêng.”

### “Tại sao chọn 30 bước và hidden size 64?”

“Dạ, 30 bước ở nhịp 20 Hz tương ứng khoảng một giây rưỡi.
Hidden size 64 là cấu hình khởi đầu của mô hình hiện tại.
Em chưa có so sánh nhiều cấu hình để khẳng định đây là lựa chọn tốt nhất.”

### “64 có phải là số khung hình không?”

“Dạ, 64 là số chiều trạng thái ẩn của LSTM. Số bước thời gian là 30.
Với một clip, đầu ra của LSTM có kích thước 1 nhân 30 nhân 64.”

### “MediaPipe và LSTM làm hai việc gì?”

“Dạ, MediaPipe lấy vị trí các điểm bàn tay ở từng khung hình.
LSTM học sự thay đổi của chuỗi đặc trưng theo thời gian để phân loại
chuyển động thành nhãn.”

### “Logits và confidence khác nhau thế nào?”

“Dạ, logits là các điểm số đầu ra của mô hình. Sau softmax, code lấy
giá trị lớn nhất trong phân bố xác suất dự đoán làm confidence.
Confidence cao vẫn có thể đi cùng dự đoán sai.”

### “Validation khác test thế nào?”

“Dạ, validation dùng để chọn checkpoint và điều chỉnh cấu hình.
Test dùng cho đánh giá sau khi chốt. Nếu đã dùng lỗi trên test để
hướng dẫn cải tiến, em cần một tập kiểm tra độc lập cho đánh giá cuối.”

### “Tại sao em đạt 80%, còn bài là 91,2%?”

“Dạ, hai kết quả dùng dữ liệu, số lớp và cách chia tập khác nhau.
Bài có 14 lớp và chia theo người; đồ án có năm lớp và chia theo phiên.
Muốn so sánh trực tiếp thì phải dùng cùng dữ liệu và cùng cách đánh giá.”

### “Vì sao vuốt lên sai nhiều?”

“Dạ, em thấy chín clip vuốt lên bị đoán thành vuốt xuống.
Em cần xem lại video, điểm bàn tay và nhãn của nhóm này trước.
Hiện em chưa đủ kiểm chứng để chốt nguyên nhân.”

### “80% có nói lên việc điều khiển webcam tốt không?”

“Dạ, 80% là kết quả trên 50 clip đã lưu. Để đánh giá điều khiển thực tế,
em cần đo thêm lệnh đúng, lệnh sai, bỏ sót, lặp lệnh và độ trễ trên webcam.”

### “Đã dùng được với người mới chưa?”

“Dạ, phần đánh giá hiện tại chia theo phiên thu. Em cần thu thêm
dữ liệu người mới và chia tập theo người để đánh giá khả năng đó.”

### “Ít nhất ba dự đoán, sao ví dụ phải đợi đến lần thứ tư?”

“Dạ, gate kiểm tra cả số lần và thời gian. Ba dự đoán ở mốc 0, 50
và 100 mili giây mới kéo dài 100 mili giây. Lần thứ tư ở mốc
150 mili giây mới đủ yêu cầu thời gian của cấu hình.”

## Phụ lục B. Nguồn để mở khi thầy hỏi

Các mã **R1–R6** thống nhất với notebook. Thông tin tác giả, nơi công bố,
DOI và liên kết dưới đây dùng để tra cứu; không cần đọc hết khi nói.

Đường dẫn cục bộ tính từ gốc Hand-Tracking. Số trang IPN HandS là số trang PDF.

#### [R1] S2Gest

Kefan Chen, Yong Gu, Bo Li, Longjie Huang, Jiajun Zhang. **S2Gest: Split-Scan State Space Models for Dynamic Hand Gesture Recognition**. *Computer Vision – ECCV 2026, LNCS 17038, tr. 487–504*, 2026.

[Trang công bố](https://link.springer.com/chapter/10.1007/978-3-032-37447-9_27) · [DOI 10.1007/978-3-032-37447-9_27](https://doi.org/10.1007/978-3-032-37447-9_27) · [Repo tác giả](https://github.com/Chen-Ke-Fan/S2Gest)

PDF cục bộ — `reference/01_S2Gest_ECCV_2026/01_S2Gest_ECCV_2026.pdf`.

Vị trí cần đọc — Đối chiếu hướng xử lý video với hướng landmark; đọc phương pháp và models/S2Gest.py.

#### [R2] SKETCH

Sang Hoon Han, Seonho Lee, Hyeok Nam, Jae Hyeon Park, Min Hee Cha, Min Geol Kim, Hyunse Lee, Sangyeon Ahn, Moonju Chae, Sung In Cho. **Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition**. *Advances in Neural Information Processing Systems 38, NeurIPS 2025, Main Conference Track*, 2025.

[Trang công bố](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html) · [DOI 10.52202/085713-4682](https://doi.org/10.52202/085713-4682) · [Repo tác giả](https://github.com/capableofanything/SKETCH)

PDF cục bộ — `reference/02_SKETCH_NeurIPS_2025/02_SKETCH_Doodle_to_Detect_NeurIPS_2025.pdf`.

Vị trí cần đọc — Đối chiếu cách biểu diễn; đọc phương pháp và shrec22/train/model.py, SwinWithRegressor.forward.

#### [R3] GESTRO

Thorsten Hempel, Magnus Jung, Arman Ahmed Khan, Ayoub Al-Hamadi. **GESTRO: Skeleton-Based Dynamic Gesture Recognition for Robot Teleoperation**. *Journal of Intelligent & Robotic Systems, tập 112, bài 51*, 2026.

[Trang công bố](https://link.springer.com/article/10.1007/s10846-026-02395-9) · [DOI 10.1007/s10846-026-02395-9](https://doi.org/10.1007/s10846-026-02395-9) · [Repo tác giả](https://github.com/thohemp/gestro)

PDF cục bộ — `reference/03_GESTRO_JIRS_2026/03_GESTRO_JIRS_2026.pdf`.

Vị trí cần đọc — Gần hướng ứng dụng điều khiển; đọc mục 3–6. Bản mã nguồn đang lưu chỉ có README ghi Following soon.

#### [R4] ConvMixFormer

Mallika Garg, Debashis Ghosh, Pyari Mohan Pradhan. **ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition**. *IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), tr. 6156–6166*, 2025.

[Trang công bố](https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html) · [DOI 10.1109/WACV61041.2025.00600](https://doi.org/10.1109/WACV61041.2025.00600) · [Repo tác giả](https://github.com/mallikagarg/ConvMixFormer)

PDF cục bộ — `reference/04_ConvMixFormer_WACV_2025/04_ConvMixFormer_WACV_2025.pdf`.

Vị trí cần đọc — Đối chiếu tài nguyên và xử lý chuỗi; đọc phương pháp, src_convmixformer/models/temporal.py và src_convmixformer/models/attention.py.

#### [R5] Continuous HGR Survey

Marco Emporio, Amirpouya Ghasemaghaei, Joseph J. Laviola Jr., Andrea Giachetti. **Continuous hand gesture recognition: Benchmarks and methods**. *Computer Vision and Image Understanding, tập 259, bài 104435*, 2025.

[Trang công bố](https://www.sciencedirect.com/science/article/pii/S1077314225001584) · [DOI 10.1016/j.cviu.2025.104435](https://doi.org/10.1016/j.cviu.2025.104435)

PDF cục bộ — `reference/05_Continuous_HGR_Survey_CVIU_2025/05_Continuous_Hand_Gesture_Recognition_Benchmarks_and_Methods_CVIU_2025.pdf`.

Vị trí cần đọc — Dùng để phân biệt phân loại clip với phát hiện sự kiện trên webcam; đọc phần metric và discussion.

#### [R6] IPN HandS

Gibran Benitez-Garcia, Jesus Olivares-Mercado, Gabriel Sanchez-Perez, Hiroki Takahashi. **IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition**. *Applied Sciences, tập 15, số 11, bài 6321*, 2025.

[Trang công bố](https://www.mdpi.com/2076-3417/15/11/6321) · [DOI 10.3390/app15116321](https://doi.org/10.3390/app15116321) · [Repo tác giả](https://github.com/GibranBenitez/IPN-hand)

PDF cục bộ — `reference/06_IPN_HandS_Applied_Sciences_2025/06_IPN_HandS_Applied_Sciences_2025.pdf`.

Vị trí cần đọc — Bài đọc chính. Đọc mục 3; mục 5.1 tr. 13–14; mục 5.2 tr. 14; Bảng 6 tr. 15.

### Code đồ án cần mở

- `src/hand_tracking/features.py` — `extract_features()`, dòng 11;
  `SequenceBuffer`, dòng 36.
- `src/hand_tracking/model.py` — `GestureLSTM`, dòng 11;
  `forward()`, dòng 22; `load_gesture_model()`, dòng 27;
  `predict_gesture()`, dòng 65.
- `src/hand_tracking/training.py` — `train_model()`, dòng 11.
- `src/hand_tracking/evaluation.py` — `evaluate_model()`, dòng 16.
- `src/hand_tracking/app.py` — `run_preview()`, dòng 59.
- `src/hand_tracking/control.py` — `GestureGate`, dòng 7;
  `send_gesture_action()`, dòng 69.

Các số dòng là vị trí ở thời điểm soạn. Khi sửa source, tìm lại bằng tên
hàm. Đối chiếu các đường dẫn, nguồn và số liệu trong bản nói
với notebook đang mở trước buổi báo cáo.
