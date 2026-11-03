# Dữ liệu

Kế hoạch theo đặc tả 1.1: 250 clip, gồm bốn cử chỉ và nền. Bộ thu đã có; dữ liệu thật do người sử dụng thực hiện qua lệnh collect. Thử nghiệm tự động không đưa mẫu tổng hợp vào thư mục dữ liệu dự án.

## Chia phiên

- train: 30 clip/nhãn × 5 nhãn = 150 clip.
- validation: 10 clip/nhãn × 5 nhãn = 50 clip.
- test: 10 clip/nhãn × 5 nhãn = 50 clip.

Thu ba phiên riêng, không cắt một video rồi chia các cửa sổ chồng lấp sang nhiều tập.

## Tên và nhãn

Giữ thống nhất với src/hand_tracking/labels.py:

- 0: BACKGROUND.
- 1: SWIPE_LEFT.
- 2: SWIPE_RIGHT.
- 3: SWIPE_UP.
- 4: SWIPE_DOWN.

Lệnh collect tạo thư mục khi cần: `raw/train/SWIPE_LEFT/<session>_<clip_id>.avi`; NPZ cùng tên ở `processed/train/SWIPE_LEFT/`.

NPZ gồm `features` float32 [30,44], `label`, `session_id`, `split`, `source_clip`, `frame_timestamps_ms`, `sample_timestamps_ms`, `landmarks_xy` [N,21,2], kích thước frame và hợp đồng tiền xử lý. Các mốc thời gian tính tương đối từ frame đầu, đơn vị ms. Lưới đặc trưng dùng cửa sổ đầy mới nhất khi hoàn thành lượt, nên mốc đầu của lưới có thể sau frame đầu vài chục ms; các mốc đã được lưu rõ.

Video AVI dùng MJPG, FPS danh nghĩa đo từ các frame của lượt ghi; timestamp trong NPZ mới là căn cứ khi cần thời gian chính xác. Không coi header FPS là bằng chứng mọi frame webcam cách đều nhau.

`manifest.csv` gồm `clip_id,session_id,split,label_id,label,raw_path,processed_path,created_at`. Tệp `sessions/<session>.json` chặn nhầm split hoặc thay hợp đồng tiền xử lý khi thu tiếp. Chỉ chạy một bộ thu tại một thời điểm.

Giữ cấu hình lấy mẫu và chiều gương cùng bộ dữ liệu. Nếu đổi đặc trưng/nhịp lấy mẫu thì trích lại dữ liệu và huấn luyện lại.

Video, NPZ, manifest và metadata phiên đã được .gitignore loại khỏi Git. Khi chia sẻ dữ liệu phải đi cùng toàn bộ nhóm tệp này, giữ nguyên đường dẫn tương đối.

Xem [hướng dẫn thu 50 clip](D:/Learn/Hutech/Do_an_chuyen_nganh/Hand-Tracking/docs/COLLECTION.md). Kiểm tra bằng `python -m hand_tracking dataset-check --split train`; hiện chưa huấn luyện LSTM.
