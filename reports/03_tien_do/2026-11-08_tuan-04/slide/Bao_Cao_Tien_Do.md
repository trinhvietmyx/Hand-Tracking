# Báo cáo tiến độ nghiên cứu

## Nhận diện cử chỉ tay động và điều khiển máy tính không chạm

**Sinh viên**. Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3.  
**GVHD**. PGS.TS. Võ Đình Bảy.  
**Buổi báo cáo**. 08/11/2026, từ 14 giờ, online.  
**Phạm vi số liệu**. Rà soát ngày 07/11/2026, đến tuần 4 của kế hoạch 12/10–20/12/2026.  
**Repository**. `D:\Learn\Hutech\DACN\Hand-Tracking`.

## 1. Tổng quan đề tài

### 1.1. Bài toán và lý do lựa chọn

Đề tài xây dựng một nguyên mẫu dùng webcam RGB để nhận diện chuỗi chuyển động bàn tay và phát lệnh chuyển slide hoặc cuộn trang. Người dùng ngồi trước máy, đưa một bàn tay vào khung hình và thực hiện một trong bốn hướng cử chỉ. Chương trình cần phân biệt cử chỉ với trạng thái nền, xác nhận trước khi gửi lệnh và có cách bật/tạm dừng rõ ràng.

Nhận diện một chuỗi chuyển động đòi hỏi kết hợp thông tin tư thế và sự thay đổi theo thời gian. MediaPipe cung cấp điểm bàn tay từ ảnh [4], [7]. LSTM xử lý chuỗi đặc trưng để dự đoán nhãn [5], [6]. Bài toán đồ án còn bao gồm việc biến dự đoán thành một lệnh có thể dùng trong ứng dụng.

### 1.2. Mục tiêu và phạm vi

Mục tiêu tổng quát là tạo một nguyên mẫu nhận diện và điều khiển có thể trình diễn, kiểm tra lại số liệu và giải thích cách xử lý. Các mục tiêu cụ thể gồm thu dữ liệu có nhãn, xây dựng chuỗi đặc trưng, huấn luyện LSTM, đánh giá phân loại clip và thử nghiệm phát lệnh trực tiếp.

Phạm vi theo đặc tả 1.1 gồm một người và một bàn tay, webcam Windows, bốn hướng cử chỉ cùng lớp nền. Bản cơ bản dùng chuyển slide và cuộn trang, phím F8 để bật/tạm dừng, F9 để dừng toàn cục. Điều kiện mục tiêu là đủ sáng, bàn tay thấy rõ và cử chỉ thực hiện từng lần có thời gian nghỉ.

Giá trị ở quy mô đồ án nằm ở bộ dữ liệu tự thu, quy trình xử lý đồng nhất, mô hình nhỏ và phép thử điều khiển có ghi nhận. Kết luận về kiến trúc mới hoặc khả năng tổng quát cần nghiên cứu đối chứng và dữ liệu bổ sung.

## 2. Nghiên cứu liên quan

### 2.1. IPN HandS [1]

Gibran Benitez-Garcia, Jesus Olivares-Mercado, Gabriel Sanchez-Perez và Hiroki Takahashi công bố *IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition* trên Applied Sciences năm 2025, DOI 10.3390/app15116321. Công trình nghiên cứu chất lượng gán nhãn skeleton trong video cử chỉ RGB liên tục. Bảng 1 ghi 50 người, 14 lớp và 5.177 mẫu cử chỉ. Giao thức đánh giá chia người độc lập, 37 người train và 13 người test.

Mô hình dùng 42 tọa độ x/y của 21 điểm, ba tầng LSTM với 256 nút ẩn mỗi tầng và lớp phân loại 14 nhãn. Bảng 6 báo accuracy 91,2 ± 1,4% và average recall 78,0 ± 1,2% qua ba lần chạy. Các số này phải được đọc cùng giao thức và đơn vị phần trăm của bảng. Báo cáo dùng Bảng 6 làm nguồn định lượng.

Ưu điểm là kết hợp kiểm tra landmark, sửa bằng tay và đánh giá theo người chưa xuất hiện trong train. Hạn chế đối với việc áp dụng trực tiếp vào đồ án là quy mô, số lớp và mô hình lớn hơn, cùng yêu cầu kiểm tra nhãn. Tác động quan trọng đối với đề tài hiện tại là cần xem video và kiểm tra ý nghĩa cử chỉ, bên cạnh kiểm tra shape của NPZ.

### 2.2. SKETCH [2]

Sang Hoon Han và cộng sự công bố *Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition* tại NeurIPS 2025, DOI 10.52202/085713-4682. SKETCH chuyển skeleton có thời gian và tọa độ x/y/z thành biểu diễn đồ thị dạng ảnh, sử dụng Dynamic Range Embedding và backbone thị giác. Công trình đánh giá trên SHREC’19 và SHREC’22.

Bảng 1, cấu hình Swin-L có augmentation, ghi detection rate 0,93 và false positive 0,01 trên SHREC’19. Đây là DR/FP của giao thức phát hiện cử chỉ. Trong mục 5.1, tác giả nêu quyết định theo từng cửa sổ độc lập còn bỏ qua ngữ cảnh giữa các cửa sổ. Cơ chế tổng hợp dự đoán cũng đặt ra đánh đổi giữa giảm nhiễu và độ trễ.

Ưu điểm liên quan đến đồ án là cách kiểm tra thông tin chuyển động và vai trò của chuẩn hóa. Hạn chế khi chuyển trực tiếp sang nguyên mẫu là cần biểu diễn và backbone khác LSTM hiện tại. Đồ án có thể học cách đánh giá lỗi và chất lượng biểu diễn từ nghiên cứu này, trong khi việc tái lập phương pháp cần một thí nghiệm riêng.

### 2.3. ConvMixFormer [3]

Mallika Garg, Debashis Ghosh và Pyari Mohan Pradhan công bố *ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition* tại WACV 2025, trang 6156–6166. Phương pháp thay bộ trộn self-attention bằng convolution và dùng cơ chế gating. Nghiên cứu sử dụng NVGesture và Briareo, với cả đầu vào đơn phương thức và kết hợp cảm biến.

Bảng 1 cho RGB đơn phương thức báo accuracy 76,04% trên NVGesture và 98,26% trên Briareo. Bảng 6 ghi 13,57 triệu tham số, so với 24,30 triệu của Transformer được dùng làm đối chiếu trong bài. Các kết quả thể hiện đánh đổi độ chính xác và quy mô mô hình trong chính giao thức của nghiên cứu.

Ưu điểm là phân tích chi phí tham số cùng kết quả nhiều loại đầu vào. Hạn chế đối với đồ án là đầu vào ảnh và bộ dữ liệu khác, cùng chi phí mô hình lớn hơn LSTM nhỏ hiện tại. Bài học áp dụng là cần ghi cả hiệu năng đo trên máy và chất lượng phân loại trước khi chọn mở rộng kiến trúc.

### 2.4. So sánh và hướng tiếp cận

| Công trình | Phương pháp và dữ liệu | Kết quả gốc được dùng | Liên quan và giới hạn |
|---|---|---|---|
| IPN HandS [1] | Landmark 2D, LSTM 3 tầng; 50 người, 14 lớp | Accuracy 91,2 ± 1,4%; average recall 78,0 ± 1,2% | Kiểm tra chất lượng nhãn; giao thức chia theo người |
| SKETCH [2] | Skeleton thành ảnh, DRE, ViT/Swin; SHREC’19/22 | SHREC’19 DR 0,93; FP 0,01 | Biểu diễn chuyển động và chuẩn hóa; còn giới hạn cửa sổ độc lập |
| ConvMixFormer [3] | Convolution token mixer và gating; NVGesture, Briareo | RGB accuracy 76,04% và 98,26%; 13,57M tham số | Đánh đổi chi phí và độ chính xác; đầu vào khác đồ án |

Các chỉ số trên thuộc các tập dữ liệu và bài toán đánh giá khác nhau. Kết quả 80% của đồ án được diễn giải trong phạm vi 50 clip tự thu. Chưa có thí nghiệm chạy các phương pháp [1]–[3] trên cùng dữ liệu của đồ án.

Hướng tiếp cận hiện tại kế thừa landmark và mô hình chuỗi, tập trung vào năm nhãn và việc phát lệnh trên máy đang dùng. Những nội dung còn cần chứng minh gồm khả năng phân biệt lên/xuống, độ ổn định của phát lệnh, độ trễ và khả năng hoạt động với người hoặc điều kiện mới. Đây là khoảng trống thực nghiệm của nguyên mẫu cần hoàn thiện.

### 2.5. Trọng tâm theo góp ý GVHD ở tuần 2

GVHD yêu cầu chỉ rõ nghiên cứu trước, đọc hiểu bài báo, hiểu code chạy như thế nào rồi mới mở rộng. Phần đọc sâu chọn IPN HandS [1] vì có mô hình cơ sở landmark + LSTM gần cách triển khai hiện tại. SKETCH [2] và ConvMixFormer [3] dùng để đối chiếu các hướng khác. Việc chọn này không khẳng định code đồ án bắt nguồn trực tiếp từ code tác giả.

Cần đọc Abstract/Introduction để xác định bài toán và đóng góp; mục 5.1–5.2, trang 13–14 để hiểu đầu vào, LSTM, phân chia và huấn luyện; Bảng 6 trang 15 để hiểu kết quả; phần hạn chế để biết phạm vi kết luận. Đầu ra của việc đọc là bản giải thích bằng lời của sinh viên, có chỉ đúng đoạn/bảng làm căn cứ.

Nguồn tác giả tại [README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) có mô tả dữ liệu. [model.py trong repo](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) đang được xem là bộ chọn mô hình CNN thuộc benchmark IPN Hand trước đó. Chưa xác minh được đường chạy LSTM của thí nghiệm 2025 và chưa tái lập kết quả gốc. Cần kiểm tra đúng phiên bản mã và dữ liệu trước khi nói đã chạy code bài báo.

## 3. Phương pháp nghiên cứu và cấu hình đã triển khai

### 3.1. Kiến trúc và trách nhiệm từng phần

| Thành phần | Đầu vào | Xử lý | Đầu ra |
|---|---|---|---|
| Camera | Webcam RGB | Đọc ảnh, hình gương một lần, timestamp tăng | Ảnh và thời gian |
| Hand Landmarker | Ảnh | Tìm 21 điểm, chấp nhận đúng một tay | Tọa độ x/y hoặc trạng thái mất tay |
| Đặc trưng | 21 điểm x/y | Cùng đơn vị ảnh, trừ cổ tay, chuẩn hóa lòng bàn tay | Vector 44 chiều |
| Bộ đệm | Vector và timestamp | Lấy mẫu 20 Hz, giữ 30 mẫu | Chuỗi 30 × 44 |
| LSTM và Linear | Chuỗi | LSTM 1 tầng, 64 nút ẩn, lớp phân loại | 5 logits và xác suất |
| Xác nhận lệnh | Nhãn, xác suất, trạng thái bật/tắt | Ngưỡng, giữ ổn định, chờ nền và cooldown | Một lệnh hoặc chờ |
| Điều khiển | Nhãn đã xác nhận | Gửi phím trái/phải hoặc cuộn | Thao tác ở ứng dụng có focus |

### 3.2. Thu thập và chuẩn hóa

Công cụ `collect` cho chọn nhãn, đếm ngược và lưu một động tác trong mỗi clip. Mỗi mẫu có AVI sạch, NPZ đặc trưng, mã phiên và dòng manifest. Mất tay, hai tay hoặc khoảng gián đoạn quá 100 ms làm lượt thu cần thực hiện lại. Kiểm tra dữ liệu xác nhận kiểu dữ liệu, kích thước, nhãn, phiên, video tham chiếu và tính hợp lệ số học. Ý nghĩa của động tác được kiểm tra bằng việc xem lại video.

Với ảnh rộng W, cao H, tọa độ ban đầu p được đổi thành q = p × [W, H] / max(W, H). Gọi w là điểm cổ tay và s là trung vị khoảng cách từ cổ tay tới các điểm 5, 9, 13, 17. Vector hình dạng là (q − w)/s, trải phẳng thành 42 giá trị. Nối thêm hai tọa độ cổ tay tạo vector 44 chiều. Hai giá trị cuối giữ quỹ đạo toàn cục trong ảnh.

Bộ đệm lấy mẫu cách 50 ms và nội suy khe hở ngắn khi đã có hai đầu mút hợp lệ. Chuỗi bị xóa khi mất dữ liệu hoặc khoảng hở quá 100 ms. 30 bước có khoảng từ mẫu đầu tới mẫu cuối là 1,45 giây, thường được mô tả gần 1,5 giây. Nhịp lấy mẫu 20 Hz là cấu hình dữ liệu, cần đo riêng FPS xử lý thực tế.

### 3.3. Huấn luyện và đánh giá

Đầu vào theo batch là [B, 30, 44]. LSTM trả chuỗi trạng thái ẩn, chương trình lấy trạng thái cuối, qua Linear 64 → 5. Mô hình có 28,485 tham số. CrossEntropyLoss nhận logits khi huấn luyện. Softmax dùng lúc suy luận để chọn nhãn và mức tin cậy.

Cấu hình mã nguồn gồm Adam, learning rate 0,001, batch size 16 và seed 42. Log đã lưu trong notebook có đủ 30 epoch. Checkpoint được chọn theo validation loss thấp nhất ở epoch 23, với loss 0.108522 và validation accuracy 94%. Hai checkpoint ứng dụng và notebook có trọng số trùng khớp khi kiểm tra từng tensor.

Mô hình dùng train để cập nhật trọng số, validation để chọn checkpoint, test để đo kết quả. Các chỉ số hiện được tính trong `evaluation.py` bằng NumPy. Ngưỡng phát lệnh khởi đầu 0,80, cần ít nhất ba dự đoán mới và ổn định 150 ms. Sau một lệnh, chương trình chờ ít nhất 1.000 ms và nền ổn định 300 ms trước lần tiếp.

### 3.4. Môi trường hiện tại

Python 3.11.0, Windows, PyTorch bản CPU. Đây là phiên bản đọc từ môi trường đang dùng trong lần rà soát.

| Thư viện | Phiên bản đã cài |
|---|---|
| numpy | 2.4.6 |
| torch | 2.15.0+cpu |
| mediapipe | 0.10.35 |
| opencv-contrib-python | 4.14.0.94 |
| pyautogui | 0.9.54 |
| pynput | 1.8.2 |
| matplotlib | 3.11.2 |
| scikit-learn | Chưa cài trong môi trường hiện tại |

### 3.5. Đối chiếu nghiên cứu với luồng code hiện có

Bài [1] dùng 42 tọa độ xy, LSTM ba tầng 256 nút ẩn, dropout 0,3 và 14 lớp có chủ đích; đồ án dùng 42 giá trị cục bộ nối hai tọa độ cổ tay, LSTM một tầng 64 và năm lớp gồm nền. Bài dùng cửa sổ dài tối đa 64 frame, stride 32 cho chuỗi dài và không padding/nội suy chuỗi ngắn; đồ án tạo chuỗi cố định 30 mẫu ở 20 Hz. Bài chia theo 37/13 người; đồ án hiện chia theo phiên thu. Các khác biệt này cần được giải thích và đánh giá riêng, chưa phải bằng chứng cải tiến.

Thứ tự đọc mã: `features.py:extract_features` → `SequenceBuffer.push` → `model.py:GestureLSTM.forward` → `predict_gesture` → `training.py:train_model` → `evaluation.py:evaluate_model` → luồng webcam trong `app.py` và xác nhận lệnh trong `control.py`.

Đã chạy tách các bước suy luận của một clip test: [1,30,44] → [1,30,64] → [1,64] → [1,5]. Kết quả trùng `model(x)`, nhãn BACKGROUND đúng với clip được chọn; đây là kiểm tra luồng thực thi, không thay đổi chỉ số của bộ test hoặc chứng minh tái lập nghiên cứu. Chi tiết tại `slide_sources/model_execution_trace.json`; cách tự học tại `Huong_dan_doc_bai_bao_va_code.md`.

## 4. Tiến độ triển khai thực tế

| Hạng mục | Trạng thái | Minh chứng | Vấn đề tồn tại |
|---|---|---|---|
| Nghiên cứu tài liệu | Đã có tài liệu và đối chiếu | 6 PDF trong reference; phân tích sâu [1]–[3] | Chưa tái lập benchmark công khai |
| Thu thập dữ liệu | Đã có 250 clip | manifest, video và NPZ; 150/50/50 clip | Cần thống nhất lại quy cách động tác |
| Tiền xử lý | Đã triển khai và kiểm tra | features.py, SequenceBuffer, dataset-check | Chưa đo ảnh hưởng của từng đặc trưng |
| Xây dựng mô hình | Đã triển khai | GestureLSTM, 1 tầng, 64 nút ẩn, 5 lớp | Chưa có mô hình đối chứng |
| Huấn luyện | Đã có log 30 epoch | notebook, checkpoint epoch 23 | Chưa có thống kê nhiều seed |
| Đánh giá clip | Đã đo trên 50 clip test | 40/50 đúng, Macro-F1 0,7619 | Vuốt lên chỉ đúng 1/10 |
| Tích hợp hệ thống | Đã có mã nguồn | app.py, control.py, F8/F9 và bộ xác nhận | Chưa có đo lường thao tác trực tiếp |
| Kiểm thử thực tế | Còn thiếu phép thử có ghi nhận | 60 test tự động qua; video phát lại clip | Chưa có dữ liệu thực nghiệm cho 40 lượt và 5 phút nền |

Tuần 1 (12–18/10) nghiên cứu tài liệu. Tuần 2 (19–25/10) tìm hiểu MediaPipe và LSTM. Tuần 3 (26/10–01/11) thiết lập webcam và công cụ thu. Tuần 4 (02–08/11) đã có bộ 250 clip, mô hình và đánh giá clip. Trạng thái được đối chiếu với mã nguồn và artifact hiện tại. Một số đoạn README/ROADMAP vẫn ghi trạng thái cũ và cần đồng bộ khi cập nhật tài liệu dự án.

## 5. Dữ liệu và kết quả thực nghiệm

### 5.1. Quy mô và cách chia tập

| Nhóm | Số clip | Tỷ lệ | Mỗi nhãn | Phiên |
|---|---:|---:|---:|---|
| Train | 150 | 60% | 30 | pilot_01, train_02 |
| Validation | 50 | 20% | 10 | val_01 |
| Test | 50 | 20% | 10 | test_01 |
| Tổng | 250 | 100% | 50 | 4 phiên |

Cả năm lớp có số mẫu cân bằng. Kiểm tra không thấy chuỗi đặc trưng trùng tuyệt đối giữa các nhóm. Phân chia theo phiên giúp tách các lần thu. Manifest chưa ghi mã người tham gia, nên chưa có cơ sở xác nhận đánh giá theo người chưa xuất hiện trong train.

### 5.2. Đường cong huấn luyện

Biểu đồ trong slide 10 dùng 30 dòng output đã lưu ở notebook, được trích nguyên giá trị vào `slide_sources/training_history.csv`. Loss trong log được làm tròn bốn chữ số thập phân. Train loss đầu/cuối là 1,5541/0,1293. Validation loss đầu/cuối là 1,4313/0,1720. Validation loss thấp nhất là 0,1085 ở epoch 23. Giá trị cuối cùng không phải tiêu chí chọn mô hình trong mã.

Validation accuracy ở checkpoint là 94%, cao hơn test accuracy 80% là 14 điểm phần trăm. Đường validation dao động sau khi loss train giảm. Đây là bằng chứng cần kiểm tra thêm độ ổn định giữa các phiên và các lần chạy. Một lần chạy và một bộ test nhỏ chưa đủ để kết luận nguyên nhân của chênh lệch.

Notebook ghi thời gian huấn luyện 5,0 giây. Đây là thời gian được lưu của lần chạy notebook, chưa phải phép đo nhiều lần hoặc thời gian suy luận webcam.

### 5.3. Chỉ số phân loại trên test

Chạy lại checkpoint hiện tại trên đủ 50 clip test khớp với `outputs/evaluation.json` và báo cáo notebook. Accuracy 0,8000, macro precision 0,8000, macro recall 0,8000 và Macro-F1 0,7619. Precision, recall và F1 nằm trên thang 0–1.

| Nhãn | Số mẫu | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| BACKGROUND | 10 | 1.000 | 1.000 | 1.000 |
| SWIPE_LEFT | 10 | 1.000 | 1.000 | 1.000 |
| SWIPE_RIGHT | 10 | 1.000 | 1.000 | 1.000 |
| SWIPE_UP | 10 | 0.500 | 0.100 | 0.167 |
| SWIPE_DOWN | 10 | 0.500 | 0.900 | 0.643 |

Macro-F1 lấy trung bình F1 của từng lớp. Vì lỗi tập trung ở lớp vuốt lên, cần xem từng lớp và ma trận nhầm lẫn cùng accuracy.

### 5.4. Ma trận nhầm lẫn và ý nghĩa

Hàng là nhãn thật, cột là nhãn dự đoán. Mỗi ô là số clip.

| Thật / Dự đoán | Nền | Trái | Phải | Lên | Xuống |
|---|---:|---:|---:|---:|---:|
| Nền | 10 | 0 | 0 | 0 | 0 |
| Trái | 0 | 10 | 0 | 0 | 0 |
| Phải | 0 | 0 | 10 | 0 | 0 |
| Lên | 0 | 0 | 0 | 1 | 9 |
| Xuống | 0 | 0 | 0 | 1 | 9 |

Trong 10 lỗi, có chín clip lên bị nhận thành xuống và một clip xuống bị nhận thành lên. Nền, trái và phải đạt 10/10 trong phiên test hiện có. Một video 10 giây đã được tạo bằng cách phát lại năm clip test, có hiển thị nhãn thật và dự đoán. Riêng lớp lên sử dụng một clip sai để minh họa vấn đề.

### 5.5. Tích hợp, kiểm thử và phần chưa đo

Lệnh `run` đã nối dự đoán với hiển thị và cơ chế phát lệnh. Mã nguồn có F8/F9 toàn cục, khởi đầu điều khiển tắt, xác nhận cử chỉ và chống lặp. Bộ test hiện có chạy qua 60 trường hợp trong lần rà soát. Các test tự động sử dụng dữ liệu hoặc đối tượng giả tại biên camera/điều khiển và kiểm tra thuật toán thực ở phần tương ứng.

| Phép đo | Trạng thái | Cách bổ sung |
|---|---|---|
| Latency suy luận ổn định | Chưa có dữ liệu thực nghiệm | Warm-up, đo nhiều lần với timestamp và ghi cấu hình máy |
| FPS toàn luồng có tay và LSTM | Chưa có dữ liệu thực nghiệm | Đo sau warm-up trên webcam thật, chỉ đếm kết quả mới |
| 40 lượt thao tác trực tiếp | Chưa có dữ liệu thực nghiệm | Mỗi hướng 10 lượt, ghi đúng/sai/bỏ sót/lặp |
| 5 phút nền và chuyển động thường | Chưa có dữ liệu thực nghiệm | Ghi nguyên số lệnh phát nhầm trong 5 phút |
| Người chưa xuất hiện trong train | Chưa có dữ liệu thực nghiệm | Thu người mới, giữ riêng phiên đánh giá |

## 6. Khó khăn, hạn chế và cách kiểm chứng

| Vấn đề | Bằng chứng và mức chắc chắn | Hướng xử lý | Kiểm chứng |
|---|---|---|---|
| Lên/xuống bị nhầm | Đã quan sát 10 lỗi trong test | Xem video sai, kiểm tra quy ước và thu bù train/validation | So sánh recall từng lớp trên phiên đánh giá được khóa |
| Tư thế giữa nhãn khác nhau | Quan sát các clip mẫu, còn cần GVHD xác nhận quy cách | Thống nhất mô tả cử chỉ và cách đưa tay về nghỉ | Xem mẫu trước khi thu hàng loạt, lưu tiêu chí nhận mẫu |
| Khái quát hóa còn giới hạn | Bộ tự thu nhỏ, tách phiên, chưa có mã người | Bổ sung metadata và người/điều kiện mới theo phạm vi được duyệt | Tập người mới hoặc phiên mới độc lập |
| Validation và test chênh 14 điểm phần trăm | Đã quan sát ở checkpoint hiện tại | Giữ giao thức và ghi nhiều lần chạy nếu thời gian cho phép | Báo mean/std và kết quả từng phiên khi đã đo |
| Độ ổn định điều khiển còn thiếu đo lường | Có mã nguồn, thiếu bảng thử trực tiếp | Thực hiện 40 lượt, 5 phút nền và kiểm tra F8/F9 | Báo đúng/sai/bỏ sót/lặp và log thời gian |

Các khả năng mô hình học tư thế thay vì hướng chuyển động, sai lệch giữa các phiên hoặc overfitting là giả thuyết cần thí nghiệm. Dữ liệu hiện có xác nhận lỗi phân loại, chưa xác định nguyên nhân duy nhất. Chưa có bằng chứng bộ dữ liệu mất cân bằng số lượng vì mỗi lớp đều có 50 clip.

## 7. Kết luận

Đồ án đã có bộ dữ liệu 250 clip, cách xử lý chuỗi 30 × 44, LSTM 28.485 tham số, log huấn luyện và checkpoint. Kết quả kiểm tra lại trên 50 clip đạt accuracy 80% và Macro-F1 0,7619. Mã nguồn đã nối nhận diện với hiển thị, phím điều khiển và xác nhận lệnh.

Kết quả hiện tại chứng minh chương trình có thể học và đánh giá năm nhãn trên bộ clip đã thu. Lỗi lên/xuống và phần kiểm thử điều khiển trực tiếp còn cần xử lý. Công việc ưu tiên là thống nhất quy cách cử chỉ, củng cố dữ liệu và ghi nhận các phép thử ứng dụng trước khi chốt kết quả cuối.

Danh mục tài liệu tham khảo theo số [1]–[7] nằm trong `references.md`. Dữ liệu dùng dựng biểu đồ, nguồn tạo slide và ghi chú thuyết trình đi cùng thư mục `slide_sources/` và `speaker_notes.md`.
