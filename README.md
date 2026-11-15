# Hand-Tracking

Đồ án một sinh viên: nhận diện bốn cử chỉ vuốt để chuyển slide và cuộn trang.

Bộ khung bám theo [đặc tả 1.1](reports/01_tai_lieu_de_tai/DAC_TA_NHAN_DIEN_CU_CHI_TAY_DONG_VA_DIEU_KHIEN_MAY_TINH_KHONG_CHAM.md).

## Trạng thái hiện tại

Đã chạy được **camera → landmark → 44 đặc trưng → bộ đệm [30,44]** qua lệnh `preview`. Có cửa sổ xem bàn tay, số mẫu đã tích lũy, trạng thái mất tay/hai tay và FPS xử lý. Chế độ này không ghi hình và không gửi thao tác chuột/phím.

Đã có **collect** để thu clip có nhãn, **dataset-check** để kiểm tra dữ liệu, **train** để huấn luyện LSTM và **evaluate** để đánh giá các clip test. Lệnh **run** nhận diện qua webcam và gửi lệnh sau khi cử chỉ vượt qua GestureGate. Điều khiển bắt đầu ở OFF; F8 bật/tạm dừng, F9 thoát.

[Notebook](notebook/hand_tracking.ipynb) trình bày sáu công trình tham khảo, đọc bài IPN HandS, luồng code và thực nghiệm trên dữ liệu tự thu. [Lời trình bày](notebook/speaker_notes.md) dùng cho buổi báo cáo với giảng viên hướng dẫn. Tài liệu báo cáo nằm trong [reports](reports/); mã nguồn tham khảo và cách tải nằm trong [reference](reference/README.md).

## Cấu trúc

```text
Hand-Tracking/
├── configs/default.json        # Camera, chuỗi, LSTM, ngưỡng và đường dẫn
├── src/hand_tracking/
│   ├── __main__.py, cli.py     # Lệnh chạy chung
│   ├── config.py, labels.py    # Cấu hình và năm nhãn dùng chung
│   ├── camera.py              # Đọc frame và timestamp
│   ├── landmarks.py           # MediaPipe Hand Landmarker
│   ├── features.py            # 44 đặc trưng, lấy mẫu và bộ đệm
│   ├── collection.py          # Thu clip có nhãn
│   ├── dataset.py             # Xuất/đọc chuỗi [30,44]
│   ├── model.py               # LSTM một tầng, hidden size 64
│   ├── training.py            # Huấn luyện và lưu checkpoint
│   ├── evaluation.py          # Metric và confusion matrix
│   ├── control.py             # Xác nhận, chống lặp, gửi lệnh
│   └── app.py                 # Preview và nhận diện/điều khiển webcam
├── data/
│   ├── raw/{train,validation,test}/
│   ├── processed/{train,validation,test}/
│   ├── sessions/               # Tạo khi thu; metadata mỗi phiên
│   └── manifest.csv            # Tạo khi có clip đã lưu
├── assets/hand_landmarker/     # Model landmark đã tải trên máy này
├── models/                    # Checkpoint LSTM
├── outputs/                   # Log và kết quả đánh giá
├── notebook/                  # Nghiên cứu, thực nghiệm và lời trình bày
├── reference/                 # Bài báo và submodule mã nguồn tác giả
├── reports/                   # Báo cáo tiến độ và minh chứng
├── tests/                     # Cấu hình, I/O, đặc trưng, sampling, preview
├── docs/ROADMAP.md             # Thứ tự code tiếp
├── pyproject.toml             # Python package và nhóm phụ thuộc
└── requirements.txt           # Cài phụ thuộc ứng dụng khi cần
```

## Môi trường nền móng trên Windows

Chọn Python 3.11 cho dự án. Không dùng nhầm Python mặc định trên máy nếu đang là phiên bản khác.

Mở PowerShell tại thư mục Hand-Tracking:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m hand_tracking check
```

Khi clone từ GitHub, cần tạo lại môi trường và tải model landmark theo hướng dẫn bên dưới. Không cần activate môi trường để dùng các lệnh đầy đủ trên. Dữ liệu tự thu và checkpoint LSTM được lưu cục bộ.

CLI `check` in cấu hình, đường dẫn đã resolve, các thư viện hiện có và tài nguyên còn thiếu. Chạy được bằng Python chuẩn; không import MediaPipe/PyTorch, không mở camera và không gửi thao tác chuột/phím. `dependencies: null` hoặc `exists: false` nghĩa là chưa cài/chưa có tài nguyên tương ứng, không phải đã sẵn sàng chạy ứng dụng.

Đường dẫn bên trong JSON tính theo gốc dự án chứa `configs/`, không tính theo working directory. Khi đứng ở thư mục khác, truyền đường dẫn tuyệt đối của cấu hình trước tên lệnh:

```powershell
& 'D:\Learn\Hutech\DACN\Hand-Tracking\.venv\Scripts\python.exe' -m hand_tracking --config 'D:\Learn\Hutech\DACN\Hand-Tracking\configs\default.json' check
```

## Chạy xem trước camera

Mở PowerShell tại Hand-Tracking:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking preview
```

Đưa đúng một bàn tay vào camera và giữ trong khung khoảng hai giây. Cửa sổ hiển thị 21 điểm, trạng thái `one_hand`, 44 đặc trưng và bộ đệm tăng đến 30/30. Nhấn **Q**, **Esc** hoặc đóng cửa sổ để thoát. F8/F9 dùng trong chế độ `run`; chế độ `preview` thoát bằng Q/Esc hoặc đóng cửa sổ.

- Không thấy tay, phát hiện hai tay hoặc dữ liệu không hợp lệ: xóa bộ đệm, không ghép với chuỗi trước đó.
- Khoảng cách hai kết quả quá 100 ms: khởi tạo lại chuỗi. Ảnh camera đến nhanh không tự làm tăng số mẫu lên trên lưới 20 Hz.
- Tọa độ cục bộ chuẩn hóa theo kích thước lòng bàn tay; cả hai trục dùng cùng tỷ lệ ảnh. Hai giá trị cuối là vị trí cổ tay theo đơn vị cạnh ảnh dài nhất, để giữ hướng chuyển động.
- `handedness` của tracker phản ánh ảnh đầu vào; không dùng nhãn trái/phải đó để tự lật thêm ảnh hoặc đổi nhãn vuốt.
- Khi cảnh thay đổi đột ngột, tracker có thể cập nhật số tay chậm hơn một frame; lớp ứng dụng xóa chuỗi ngay khi nhận kết quả nhiều tay.

Đổi camera hoặc chạy thử có giới hạn:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking preview --camera-index 1
.\.venv\Scripts\python.exe -m hand_tracking preview --headless --max-frames 60
```

`--headless` bắt buộc có `--max-frames`; lệnh kết thúc bằng thống kê JSON, không lưu hình. FPS tính trên toàn vòng camera/tracking/đặc trưng; không tính mốc nội suy như frame camera mới. `sequences_ready` là số lần có cửa sổ đầy mới, không phải số cử chỉ đã nhận diện.

## Thu thử dữ liệu có nhãn

Đóng preview, sau đó chạy:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10
```

Mỗi nhãn thu mười clip, tổng 50 clip. **Space → đếm ngược hai giây → RECORDING → một lần vuốt → SAVED**. Đưa tay về vị trí chuẩn khi đang chờ, rồi Space để thu mẫu tiếp. BACKGROUND vẫn cần một tay hiện rõ, đang nghỉ hoặc di chuyển chậm.

Mất tay/hai tay/gap tracking sẽ báo RETRY, không lưu mẫu dở. Q/Esc/đóng cửa sổ dừng; chạy lại cùng lệnh tiếp tục phần còn thiếu, không ghi đè clip cũ. Chỉ chạy một cửa sổ thu tại một thời điểm.

```powershell
.\.venv\Scripts\python.exe -m hand_tracking dataset-check --split train
```

Video sạch nằm trong data/raw; đặc trưng [30,44] và timestamp ở data/processed; manifest và metadata session đi cùng dữ liệu. Cần tự xem lại đúng động tác/nhãn trước khi huấn luyện. [Hướng dẫn thu và chia phiên](docs/COLLECTION.md).

Thu sai một clip: thoát collect, dùng `dataset-remove --session pilot_01 --split train --label SWIPE_LEFT --last` để xem trước; thêm `--apply` để chuyển mẫu vào backup và cập nhật manifest. Bỏ `--last` nếu cần bỏ cả nhóm nhãn đó trong phiên. `dataset-restore --backup-id <removal_id> --apply` khôi phục khi bỏ nhầm. Chi tiết và cách thu bù trong hướng dẫn ở trên; không sửa danh sách năm nhãn.

## Cài lại thư viện vision và model

Snapshot đã kiểm tra trên Python 3.11/Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-vision.lock.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

Hoặc cài theo khoảng phiên bản khai báo trong pyproject.toml bằng `pip install -e '.[vision]'`. Khi thiết lập máy khác, tải model nếu chưa có:

```powershell
Invoke-WebRequest -Uri 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task' -OutFile 'assets/hand_landmarker/hand_landmarker.task'
```

Nguồn model và SHA-256 ở assets/hand_landmarker/README.md. `check` và `preview` không tự tải model khi chạy.

## Cài thư viện huấn luyện và điều khiển

```powershell
.\.venv\Scripts\python.exe -m pip install -c requirements-vision.lock.txt -r requirements.txt
```

Nhóm `app` khai báo thêm PyTorch, PyAutoGUI, pynput và scikit-learn. Tệp `requirements-vision.lock.txt` cố định nhóm vision đã kiểm tra; các thư viện còn lại dùng khoảng phiên bản khai báo trong dự án.

OpenCV dùng gói `opencv-contrib-python`, phù hợp với phụ thuộc MediaPipe; không cài thêm một gói OpenCV khác cùng namespace `cv2`. Xem [hướng dẫn gói OpenCV](https://pypi.org/project/opencv-python/).

Đường camera dùng MediaPipe Tasks Hand Landmarker ở VIDEO mode đồng bộ để kiểm soát timestamp và giải phóng tài nguyên rõ ràng. [Hướng dẫn MediaPipe](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python).

## Nhận diện và điều khiển webcam

Cần có model landmark và checkpoint LSTM phù hợp cấu hình. Từ gốc dự án:

```powershell
.\run.bat run
```

Hoặc mở `run.bat` và chọn **7**. F8 bật/tạm dừng, F9 thoát; Q/Esc/đóng cửa sổ cũng thoát. Khi bật điều khiển, ứng dụng yêu cầu confidence từ 80%, ít nhất ba dự đoán mới cùng nhãn và ổn định ít nhất 150 ms. Sau một lệnh, chỉ mở khóa khi hết cooldown 1 giây và có BACKGROUND đủ tin cậy ổn định 300 ms.

Ánh xạ trong code hiện tại: vuốt trái gửi mũi tên trái (slide trước), vuốt phải gửi mũi tên phải (slide tiếp theo), vuốt lên/xuống cuộn tương ứng. PyAutoGUI giữ fail-safe mặc định.

## Notebook và tài liệu nghiên cứu

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[app,notebook]"
.\.venv\Scripts\python.exe -m jupyterlab notebook
```

Chọn kernel thuộc môi trường `.venv` và chạy các ô từ trên xuống. Notebook dùng checkpoint riêng tại `models/notebook/gesture_lstm.pt` và kết quả tại `outputs/notebook/`. Các tệp này cùng dữ liệu tự thu cần được tạo hoặc cung cấp lại trên máy mới.

Để đọc code tham khảo, tải các submodule theo [hướng dẫn reference](reference/README.md). Bản thực nghiệm đồ án chưa tái lập benchmark LSTM gốc của IPN HandS.

## Các lệnh CLI

```powershell
.\.venv\Scripts\python.exe -m hand_tracking --help
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10
.\.venv\Scripts\python.exe -m hand_tracking dataset-check --split train
.\.venv\Scripts\python.exe -m hand_tracking extract
.\.venv\Scripts\python.exe -m hand_tracking train
.\.venv\Scripts\python.exe -m hand_tracking evaluate
.\.venv\Scripts\python.exe -m hand_tracking run
```

Các lệnh `check`, `preview`, `collect`, `dataset-check`, `dataset-remove`, `dataset-restore`, `train`, `evaluate` và `run` đã có chức năng. Riêng `extract` còn là lệnh giữ chỗ và trả exit code 2; collect đã lưu sẵn đặc trưng cho dữ liệu mới thu.

## Quy ước cốt lõi

- Nhãn: BACKGROUND = 0, SWIPE_LEFT = 1, SWIPE_RIGHT = 2, SWIPE_UP = 3, SWIPE_DOWN = 4.
- Chuỗi mặc định: 30 bước × 44 đặc trưng ở 20 Hz, xấp xỉ 1,5 giây.
- Giữ hai giá trị cổ tay toàn cục ngoài 42 tọa độ cục bộ để bảo toàn hướng chuyển động.
- Một LSTM, một tầng, 64 chiều trạng thái ẩn, năm đầu ra. Checkpoint tạo bởi lệnh train và không đưa vào Git.
- Điều khiển khởi động ở trạng thái tắt. F8 bật/tạm dừng và xóa chuỗi đang chờ; F9 thoát toàn cục khi chạy nhận diện có cửa sổ.
- Dữ liệu ba phiên riêng: train/validation/test. Chi tiết ở data/README.md.
- Dữ liệu thu gốc, đặc trưng, trọng số, log, .venv và video báo cáo đầy đủ không đưa vào Git. Các minh chứng ngắn được chọn trong reports có thể đi cùng báo cáo.

## Kiểm tra

Cần cài nhóm vision để chạy bộ test cho camera/đặc trưng. Test tự động dùng I/O giả ở biên camera/tracker, không tự bật webcam hoặc cần tải ảnh từ mạng.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q src
```

Đã kiểm tra ngày 30/10/2026: **26 test pass**, model thật chạy được trên ảnh trống và ảnh mẫu một/hai tay; webcam thật đọc 30 frame ở headless và 15 frame có cửa sổ. Lượt camera không có tay trong khung; chưa kiểm chứng cử chỉ động hoặc đo chất lượng trên tay người dùng. Chi tiết tại [ghi nhận kiểm tra](docs/VERIFICATION-2026-10-30.md).

Ngày 31/10/2026: chức năng thu/đọc/bỏ/khôi phục dữ liệu có **55 test pass** trên toàn dự án; thao tác ghi, chuyển và khôi phục được kiểm tra bằng video/NPZ thật trong thư mục tạm. Dữ liệu thu thật không bị thay đổi trong lần thêm lệnh xử lý mẫu sai.

Ngày 16/11/2026: chạy lại toàn bộ **60 test, đều đạt**. Kiểm tra thêm luồng ổn định/cooldown/nền của GestureGate và xác nhận test điều hướng phát hiện lỗi khi đảo phím trong bộ nhớ; source không bị thay đổi bởi phép kiểm tra này. Lượt kiểm tra không mở webcam hoặc gửi thao tác desktop.
