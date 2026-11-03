# Mô hình trích landmark

Vị trí: `hand_landmarker.task`, theo configs/default.json. Đã tải và kiểm tra trên máy ngày 30/10/2026.

- [Nguồn model chính thức, float16 phiên bản 1](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task).
- Kích thước: 7.819.105 byte.
- SHA-256: `fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1`.
- Adapter dùng MediaPipe 0.10.35, VIDEO mode đồng bộ, tối đa hai tay để phát hiện trường hợp nhiều tay.

Tải lại theo hướng dẫn trong README gốc nếu chuyển máy; binary được .gitignore loại khỏi Git. [Tài liệu Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python).

Đây là mô hình trích landmark có sẵn. Mô hình LSTM nhận diện cử chỉ do đồ án huấn luyện được lưu riêng trong models/.
