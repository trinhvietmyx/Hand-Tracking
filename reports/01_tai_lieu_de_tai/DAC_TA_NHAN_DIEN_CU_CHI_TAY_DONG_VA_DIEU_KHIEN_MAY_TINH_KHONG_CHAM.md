# ĐẶC TẢ ĐỀ TÀI — PHẠM VI CHO MỘT SINH VIÊN

**Nhận diện cử chỉ tay động và điều khiển máy tính không chạm**

Tên tiếng Anh: **Dynamic Hand Gesture Recognition for Touchless Computer Control**.

Phiên bản: 1.1 — điều chỉnh ngày 29/10/2026 theo điều kiện một sinh viên thực hiện.

Tài liệu này thay thế phạm vi phiên bản 1.0. Phương án tập trung vào bốn cử chỉ động, một mô hình nhận diện và một ứng dụng demo nhỏ. Các số lượng dữ liệu, chỉ tiêu và tiến độ là kế hoạch đề xuất, chưa phải kết quả thực nghiệm hoặc yêu cầu đã được giảng viên phê duyệt.

## 1. Mô tả và mục tiêu

Xây dựng chương trình sử dụng webcam để nhận diện chuyển động bàn tay và chuyển thành lệnh chuyển slide hoặc cuộn trang trên máy tính. Người dùng thực hiện bốn cử chỉ: vuốt trái, vuốt phải, vuốt lên và vuốt xuống.

Điểm chính của đề tài là nhận diện **chuỗi chuyển động**, không chỉ nhận biết tư thế từ một ảnh. Ví dụ, bàn tay mở có thể xuất hiện trong cả bốn lớp; hướng di chuyển theo thời gian quyết định lệnh.

Mục tiêu thực hiện:

- Đọc hình webcam và trích xuất các điểm đặc trưng bàn tay bằng công cụ có sẵn.
- Tự thu một bộ dữ liệu nhỏ, có nhãn bốn hướng vuốt và trạng thái nền.
- Huấn luyện một mô hình LSTM nhỏ để phân loại chuỗi đặc trưng.
- Kết nối kết quả nhận diện với lệnh chuyển slide và cuộn trang.
- Hạn chế phát lệnh lặp, có cách bật/tắt điều khiển rõ ràng.
- Đánh giá bằng dữ liệu giữ lại và một số lượt thử trực tiếp; trình bày cả trường hợp nhận diện sai.

Sản phẩm hướng đến một nguyên mẫu có thể trình diễn và giải thích được trong đồ án chuyên ngành. Phần lập trình, thu dữ liệu, huấn luyện và viết báo cáo do một sinh viên thực hiện.

## 2. Phạm vi thực hiện

### 2.1. Phần cần hoàn thành

- Chạy trên máy Windows đang dùng để làm đồ án, một webcam RGB và một màn hình chính.
- Một người và một bàn tay trong khung hình; chọn một tay sử dụng thống nhất trong đợt thử nghiệm.
- Nhận diện bốn cử chỉ động và một lớp nền, tổng cộng năm lớp.
- Chuyển slide trước/sau trong một ứng dụng thuyết trình đã chọn.
- Cuộn lên/xuống trong một trình duyệt hoặc trình đọc tài liệu đã chọn.
- Hiển thị hình camera, nhãn dự đoán và trạng thái điều khiển.
- Có phím bật/tạm dừng và phím dừng toàn cục.
- Lưu mô hình, dữ liệu kiểm thử và kết quả đánh giá để đưa vào báo cáo.

### 2.2. Điều kiện thử nghiệm

Người dùng ngồi trước webcam, bàn tay nhìn rõ, đủ sáng và không bị che khuất đáng kể. Dùng độ phân giải cố định, dự kiến 640 × 480. Bắt đầu với khoảng cách khoảng 0,5–0,8 m và điều chỉnh theo webcam thực tế.

Cho phép dùng chuột/bàn phím khi mở chương trình, chọn cửa sổ đích và bật điều khiển. Trong phần demo thao tác, người dùng chuyển slide hoặc cuộn trang bằng cử chỉ.

Cử chỉ được thực hiện từng lần, sau đó đưa tay về nghỉ ít nhất khoảng một giây. Chưa đặt yêu cầu nhận diện các cử chỉ nối nhau rất nhanh hoặc xử lý nhiều tay đồng thời.

### 2.3. Phần mở rộng nếu còn thời gian

Di chuyển con trỏ, nhấp chuột, thêm người thử, thêm cử chỉ hoặc làm giao diện có nút bấm. Các mục này không nằm trong điều kiện hoàn thành bản cơ bản.

Ưu tiên hoàn thành bốn cử chỉ và demo ổn định trước khi thêm chức năng.

## 3. Danh sách cử chỉ và lệnh điều khiển

Quy ước hướng theo hình xem trước đã bật chế độ gương, tương ứng góc nhìn của người sử dụng. Giữ cùng quy ước khi thu dữ liệu và chạy thật.

1. **G01 — Vuốt trái.** Di chuyển bàn tay mở từ phải sang trái để về slide trước bằng phím mũi tên trái.
2. **G02 — Vuốt phải.** Di chuyển bàn tay mở từ trái sang phải để sang slide tiếp theo bằng phím mũi tên phải.
3. **G03 — Vuốt lên:** bàn tay mở di chuyển từ dưới lên → cuộn trang lên một bước.
4. **G04 — Vuốt xuống:** bàn tay mở di chuyển từ trên xuống → cuộn trang xuống một bước.
5. **B00 — Nền:** có tay nhưng đang nghỉ, giữ tư thế hoặc chuyển động không thuộc bốn động tác đã quy định → không gửi lệnh.

Trạng thái không thấy tay được xử lý trực tiếp bằng bước theo dõi: không đưa chuỗi không hợp lệ vào nhận diện và không gửi lệnh. Không cần tự thu hàng loạt clip không có tay để làm lớp thứ sáu.

Mỗi cử chỉ là một lần vuốt rõ hướng, thời lượng dự kiến khoảng 0,5–1 giây. Động tác đưa tay trở lại vị trí chuẩn cần chậm và được thu thêm như dữ liệu nền để hạn chế nhầm thành vuốt ngược.

Lệnh chỉ có ý nghĩa khi đúng ứng dụng đích đang nhận focus. Khi demo, người dùng chọn sẵn cửa sổ PowerPoint hoặc trình duyệt; chưa cần tự phát hiện ứng dụng, tự đổi hồ sơ hoặc tự quản lý cửa sổ.

## 4. Các chức năng của chương trình

- **F01 — Mở camera:** lấy hình từ một webcam đã cấu hình, thông báo nếu không mở được.
- **F02 — Theo dõi bàn tay:** hiển thị các điểm đặc trưng và kiểm tra có đúng một tay hợp lệ.
- **F03 — Nhận diện chuỗi:** duy trì bộ đệm, chạy mô hình và hiển thị một trong năm nhãn hoặc trạng thái chưa đủ dữ liệu.
- **F04 — Thực thi lệnh:** ánh xạ bốn cử chỉ thành hai lệnh chuyển slide và hai lệnh cuộn.
- **F05 — Chống lặp:** một lần vuốt tạo tối đa một lệnh; tay giữ nguyên không phát lệnh liên tục.
- **F06 — Bật/tắt:** khởi động ở chế độ chỉ nhận diện; F8 bật/tạm dừng điều khiển, F9 dừng chương trình qua bộ nghe phím toàn cục.
- **F07 — Phản hồi và lỗi:** hiển thị trạng thái đang bật/tạm dừng, nhãn và lệnh gần nhất; không phát lệnh khi mất tay hoặc camera lỗi.

Phím toàn cục phải hoạt động khi ứng dụng thuyết trình hoặc trình duyệt đang nhận focus. Chỉ dùng kiểm tra phím trong cửa sổ camera sẽ không đáp ứng điều này.

## 5. Phương án kỹ thuật đơn giản

Luồng xử lý:

**Webcam → MediaPipe → chuỗi đặc trưng bàn tay → LSTM → kiểm tra điều kiện phát lệnh → thao tác máy tính.**

### 5.1. Công nghệ dự kiến

- Python cho chương trình chính.
- OpenCV để lấy hình và làm cửa sổ hiển thị đơn giản.
- MediaPipe Hand Landmarker để trích xuất điểm đặc trưng bàn tay; đây là công cụ có sẵn, không phải phần tự huấn luyện của đồ án. [Hướng dẫn chính thức](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python).
- NumPy và PyTorch để xử lý đặc trưng, huấn luyện và chạy một mô hình LSTM. [Tài liệu LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html).
- PyAutoGUI để gửi phím và cuộn trang; một bộ nghe phím như pynput để nhận F8/F9 toàn cục. [Tài liệu PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/).

Chốt phiên bản thư viện sau khi chạy được thử nghiệm đầu tiên. Không cần giao diện PySide6, web app, cơ sở dữ liệu, tài khoản người dùng hoặc bộ cài riêng trong bản cơ bản.

### 5.2. Dữ liệu đầu vào

Dùng tọa độ x/y của 21 điểm bàn tay. Để bớt phụ thuộc vị trí đặt tay, tạo 42 giá trị tọa độ tương đối với cổ tay và chuẩn hóa theo kích thước lòng bàn tay; giữ thêm hai giá trị vị trí cổ tay trong ảnh để còn thông tin chuyển động toàn cục.

Mỗi bước thời gian có **44 đặc trưng**: 42 giá trị hình dạng bàn tay và hai giá trị vị trí cổ tay. Không chỉ trừ cổ tay rồi bỏ toàn bộ quỹ đạo, vì như vậy dễ làm mất thông tin phân biệt các hướng vuốt.

Dùng cùng cách trích xuất, chuẩn hóa và quy ước hình gương ở lúc thu dữ liệu, huấn luyện và chạy webcam. Phiên bản đầu chưa dùng tọa độ z, đặc trưng thân người hoặc nhiều bàn tay.

### 5.3. Chuỗi và mô hình

Phương án khởi đầu:

- Đồng bộ đặc trưng về nhịp mục tiêu 20 mẫu/giây theo timestamp.
- Bộ đệm 30 bước, tương ứng khoảng 1,5 giây dữ liệu; đầu vào `[30, 44]`.
- Một tầng LSTM có 64 nút ẩn, lấy đầu ra cuối và đưa qua lớp phân loại năm nhãn.
- Huấn luyện bằng cross-entropy, dùng validation để chọn checkpoint và ngưỡng.

Khi camera xử lý nhanh hơn 20 mẫu/giây thì lấy mẫu theo thời gian. Khi xử lý chậm hoặc có khoảng mất dấu dài, giữ trạng thái chưa đủ dữ liệu hoặc khởi tạo lại bộ đệm, không coi 30 kết quả đến chậm là cùng thời lượng 1,5 giây. Chỉ nội suy các khe hở ngắn giữa những kết quả hợp lệ đã nhận; không nội suy qua đoạn báo mất tay.

Các thông số trên là điểm xuất phát, có thể điều chỉnh sau khi chạy thử. Chỉ cần hoàn thành **một mô hình học**; chưa yêu cầu TCN, Transformer, so sánh nhiều kiến trúc, chạy nhiều seed hoặc tái lập các công trình tham khảo.

### 5.4. Xác nhận và chống lặp

Dùng quy tắc đơn giản, điều chỉnh bằng validation và thử nghiệm phát triển:

1. Chỉ xét khi đủ chuỗi hợp lệ và điều khiển đang bật.
2. Nhãn cử chỉ phải vượt ngưỡng ban đầu 0,80 và giữ ổn định khoảng 150 ms, đồng thời có ít nhất ba dự đoán mới hỗ trợ nhãn đó.
3. Phát một lệnh rồi khóa nhận lệnh mới.
4. Chỉ mở lại khi đã qua ít nhất một giây và nhận nền ổn định khoảng 300 ms.
5. Khi không thấy tay hoặc phát hiện nhiều tay, hủy ứng viên, xóa bộ đệm và không gửi lệnh. Trường hợp camera lỗi chuyển về tạm dừng, yêu cầu bật lại.

Đây là cơ chế điều khiển cơ bản trên luồng webcam, chưa phải hệ thống tìm biên cử chỉ chính xác từng frame. Không đặt yêu cầu dựng máy trạng thái nhiều tầng hoặc đánh giá biên thời gian bằng temporal IoU trong bản cơ bản.

Giữ fail-safe của thư viện điều khiển. Bật/tắt hoặc đổi phiên phải xóa trạng thái cũ; không chạy bù cử chỉ trong lúc tạm dừng.

## 6. Kế hoạch dữ liệu vừa sức

### 6.1. Dữ liệu tự thu

Tự thu trên chính người làm đồ án:

- Bốn cử chỉ × 50 clip/cử chỉ = **200 clip cử chỉ**.
- Thêm **50 clip nền** gồm tay đứng yên, giữ tư thế mở và di chuyển chậm không theo động tác lệnh.
- Tổng kế hoạch: **250 clip**, mỗi clip khoảng 1,5 giây.

Có thể ghi liên tiếp bằng một script có đếm ngược và chọn nhãn sẵn; không cần xây công cụ annotation chuyên dụng. Clip cử chỉ chứa một lần vuốt, có một ít thời gian nghỉ trước/sau; thay đổi nhẹ thời điểm bắt đầu động tác để mô hình không chỉ quen một vị trí thời gian cố định.

Lưu ý thời gian thao tác, làm lại mẫu và kiểm tra thường lớn hơn tổng thời lượng video. Có thể bắt đầu thử với 10 clip/lớp để kiểm tra toàn luồng, rồi mới thu đủ. Các clip thử trước chỉ đưa vào train nếu đạt quy cách.

### 6.2. Chia thành ba phiên riêng

Thu thành ba phiên độc lập, ưu tiên ở các thời điểm khác nhau:

- **Phiên train:** 30 clip mỗi nhãn × 5 nhãn = 150 clip.
- **Phiên validation:** 10 clip mỗi nhãn × 5 nhãn = 50 clip.
- **Phiên test:** 10 clip mỗi nhãn × 5 nhãn = 50 clip.

Tổng mỗi nhãn có 50 clip. Không lấy cửa sổ chồng lấp hoặc bản tăng cường của một clip đưa sang tập khác. Dùng validation để điều chỉnh mô hình và ngưỡng; giữ test đến lượt đánh giá cuối.

Do ba phiên chủ yếu từ một người, kết quả phản ánh khả năng hoạt động trên người dùng đã thu dữ liệu. Không khẳng định nhận diện tốt với mọi người hoặc coi đây là kiểm thử người dùng chưa từng xuất hiện.

Nếu thuận tiện, nhờ thêm một hoặc hai người thực hiện khoảng 10 lần/cử chỉ để thử bổ sung. Việc này là mở rộng, không bắt buộc tuyển một nhóm người tham gia lớn.

### 6.3. Cách lưu tối thiểu

Lưu video gốc hoặc đặc trưng tương ứng, nhãn, mã phiên và thông số lấy mẫu. Sau trích xuất, mỗi clip có một mảng `[30, 44]` và một nhãn; clip không đủ dữ liệu tay được ghi nhận để thu lại hoặc loại vì lỗi thu, không loại chỉ vì mô hình đoán sai.

Có thể dùng thư mục theo phiên/nhãn và một tệp CSV liệt kê dữ liệu. Chưa cần gán mốc bắt đầu/kết thúc từng frame, bộ dữ liệu hàng nghìn mẫu hoặc tải toàn bộ IPN HandS.

Các tài liệu trong Reference dùng để giải thích lựa chọn phương pháp và đối chiếu hướng nghiên cứu. Chưa yêu cầu tái lập benchmark công khai hoặc trộn taxonomy giữa các dataset.

## 7. Cách đánh giá phù hợp quy mô đồ án

### 7.1. Phân loại clip

Chạy 50 clip test đã giữ lại, gồm 10 clip mỗi nhãn. Báo cáo:

- Số clip dự đoán đúng/tổng số clip và accuracy.
- Precision, recall, F1 từng lớp và Macro-F1 trên năm lớp.
- Confusion matrix để thấy cặp hướng dễ nhầm và nhầm với nền.

Mục tiêu ban đầu: accuracy khoảng **85% trở lên** trên tập test nhỏ. Đây là mục tiêu phấn đấu; báo kết quả thực tế và nguyên nhân nếu chưa đạt. Với chỉ 50 clip, cần nêu rõ số lượng mẫu và phạm vi một người, không suy rộng thành hiệu quả phổ quát.

### 7.2. Thử trực tiếp trên webcam

Sau khi khóa mô hình/ngưỡng, thực hiện mỗi cử chỉ 10 lần, tổng **40 lượt**. Ghi số lượt đúng lệnh, bỏ sót, sai lệnh và lệnh bị lặp. Một lượt đúng cần có đúng một lệnh mong muốn trong khi làm cử chỉ hoặc trong một giây sau khi kết thúc, không có lệnh thừa trước khi bắt đầu lượt tiếp theo.

Thực hiện thêm **năm phút** để tay nghỉ, đưa tay vào/ra và di chuyển bình thường. Ghi nguyên số lệnh nhầm trong năm phút, không suy thành cam kết chất lượng trên nhiều giờ sử dụng.

Mục tiêu ban đầu: ít nhất **32/40 lượt đúng**. Bổ sung một video demo chuyển slide và một video cuộn trang, có thể gộp trong cùng một bản quay ngắn.

### 7.3. Tốc độ và kiểm tra lỗi

- Ghi tốc độ xử lý landmark/dự đoán thực tế trên máy chạy; mục tiêu khoảng **15–20 kết quả/giây**, không tính riêng FPS hình hiển thị hoặc mốc nội suy.
- Nếu đủ tài nguyên, ưu tiên đạt nhịp lấy mẫu 20 Hz; nếu chỉ đạt gần 15 Hz, điều chỉnh nhịp và tạo lại đầu vào train/runtime đồng nhất trước đánh giá cuối.
- Đo sơ bộ thời gian từ động tác đến lệnh qua log hoặc video demo và mô tả cách đo. Chưa đặt yêu cầu p95 dưới 350 ms.
- Kiểm tra bật/tạm dừng, F9 dừng khi ứng dụng khác đang có focus, không phát lệnh lúc mất tay, không chạy bù sau bật lại và không lặp khi giữ tư thế.

Chỉ cần một cấu hình mô hình cuối cùng và các kết quả trên. Không bắt buộc nghiên cứu người dùng quy mô lớn, đo độ mỏi tay, quét hàng loạt siêu tham số hoặc thí nghiệm loại bỏ từng thành phần.

## 8. Giao diện và cách sử dụng

Dùng một cửa sổ OpenCV, hiển thị hình camera, landmark nếu cần, nhãn dự đoán, trạng thái bật/tắt và lệnh vừa gửi. Không cần đăng nhập, màn hình quản trị hoặc trang cấu hình riêng.

Luồng sử dụng:

1. Mở chương trình; mặc định chỉ nhận diện, chưa gửi lệnh.
2. Chọn sẵn slide hoặc trang tài liệu cần điều khiển.
3. Nhấn F8 để bật điều khiển, chờ thu đủ bộ đệm mới.
4. Thực hiện một cử chỉ và đưa tay về nghỉ trước lần kế tiếp.
5. Nhấn F8 để tạm dừng hoặc F9 để dừng chương trình.

Độ nhạy, ngưỡng, camera và số nấc cuộn có thể đặt trong một tệp cấu hình đơn giản. Không cần xây thêm giao diện chỉnh mọi tham số.

## 9. Kế hoạch thực hiện sáu tuần

Tiến độ này là gợi ý tương đối; thay bằng mốc nộp thực tế khi đã biết lịch.

- **Tuần 1:** chạy được webcam và landmark; xác định quy cách bốn cử chỉ; thử 10 clip/lớp.
- **Tuần 2:** viết script thu dữ liệu, hoàn thành các phiên thu và trích xuất đặc trưng; kiểm tra nhãn và chia tập.
- **Tuần 3:** huấn luyện một LSTM nhỏ, điều chỉnh bằng validation và lưu mô hình chạy được.
- **Tuần 4:** ghép nhận diện webcam với phát lệnh, thêm chống lặp, bật/tạm dừng và cửa sổ hiển thị.
- **Tuần 5:** chạy test clip, 40 lượt trực tiếp và năm phút nền; hoàn thiện lỗi, ghi giới hạn và quay demo.
- **Tuần 6:** hoàn thành báo cáo, hướng dẫn chạy, slide và kiểm tra lại toàn bộ sản phẩm; dành thời gian dự phòng.

Nếu lịch còn ít hơn, giữ bốn cử chỉ và một mô hình, giảm trang trí giao diện và hoãn phần mở rộng. Không bỏ đánh giá test để bù thời gian làm thêm tính năng.

## 10. Sản phẩm bàn giao và điều kiện hoàn thành

Bàn giao:

1. Mã nguồn thu dữ liệu, trích đặc trưng, huấn luyện và chạy webcam.
2. Bộ dữ liệu nhỏ có nhãn và cách chia phiên train/validation/test.
3. Tệp mô hình đã huấn luyện và cấu hình chạy.
4. Kết quả test, confusion matrix và thống kê 40 lượt thực hiện trực tiếp.
5. Hướng dẫn cài/chạy, báo cáo, slide và video demo.

Bản cơ bản hoàn thành khi bốn cử chỉ tạo được các lệnh đã quy định trong điều kiện thử nghiệm, có chống lặp và bật/tắt, có mô hình chuỗi do sinh viên huấn luyện và có số liệu đánh giá thật. Các mục tiêu 85% clip và 32/40 lượt là mốc định hướng ban đầu; nếu chưa đạt cần phân tích lỗi và ghi rõ mức đạt thay vì tự ghi thành kết quả đã hoàn thành.

Giá trị của đồ án nằm ở việc tích hợp nhận diện chuỗi chuyển động với ứng dụng điều khiển, tự tổ chức dữ liệu và đánh giá được sản phẩm. Chưa đặt mục tiêu đề xuất kiến trúc mạng mới hoặc vượt các công trình đã công bố.

## 11. Những hạng mục đã giảm so với bản 1.0

- Tám cử chỉ giảm còn bốn cử chỉ động và một lớp nền.
- Di chuyển con trỏ, nhấp trái/phải và zoom chuyển thành phần mở rộng; demo chính chỉ chuyển slide và cuộn trang.
- Kế hoạch 15 người/2.400 lần cử chỉ thay bằng 250 clip tự thu ở ba phiên; người thử thêm là tùy điều kiện.
- Nhiều mô hình và thí nghiệm so sánh thay bằng một LSTM nhỏ.
- Giao diện desktop riêng thay bằng một cửa sổ OpenCV.
- Đánh giá biên sự kiện bằng temporal IoU, nhiều seed, p95 nghiêm ngặt và thử nền 60 phút được thay bằng test clip, 40 lượt trực tiếp và năm phút nền.
- Giữ các phần thiết yếu: nhận diện động, lớp nền, chống lặp, dừng điều khiển và đánh giá trung thực.

## 12. Đoạn mô tả dùng cho đề cương

Đề tài “Nhận diện cử chỉ tay động và điều khiển máy tính không chạm” xây dựng chương trình sử dụng webcam RGB để nhận diện bốn cử chỉ vuốt tay gồm trái, phải, lên và xuống, từ đó thực hiện thao tác chuyển slide và cuộn trang. Hệ thống sử dụng MediaPipe để trích xuất điểm đặc trưng bàn tay và một mô hình LSTM nhỏ để phân loại chuỗi chuyển động. Sinh viên tự thu bộ dữ liệu khoảng 250 clip gồm các cử chỉ và trạng thái nền, chia theo các phiên thu riêng để huấn luyện, xác thực và kiểm thử. Chương trình có cửa sổ hiển thị kết quả, cơ chế chống phát lệnh lặp và phím bật/tắt điều khiển. Kết quả được đánh giá qua độ chính xác phân loại, confusion matrix, số lượt thực hiện đúng khi chạy webcam và tốc độ xử lý trên máy thử nghiệm. Sản phẩm gồm mã nguồn, mô hình, dữ liệu có nhãn, báo cáo và video demo.

Tài liệu đặc tả mới điều chỉnh phạm vi. Chưa thực hiện thu dữ liệu, huấn luyện hay kiểm thử ứng dụng trong phiên chỉnh sửa này.
