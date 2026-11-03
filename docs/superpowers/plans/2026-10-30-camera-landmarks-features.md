# Camera, Landmarks and Features Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chạy xem trước webcam, trích đúng một bàn tay, tạo 44 đặc trưng và bộ đệm [30,44] trước khi thu dữ liệu.

**Architecture:** camera.py quản lý tài nguyên OpenCV; landmarks.py bọc MediaPipe Tasks ở VIDEO mode đồng bộ; features.py dùng chung cho runtime và dữ liệu sau này. app.py ghép thành lệnh preview, không nạp LSTM hoặc gửi thao tác hệ điều hành.

**Tech Stack:** Python 3.11, NumPy, OpenCV contrib, MediaPipe Hand Landmarker, unittest.

**Spec:** D:/Learn/Hutech/Do_an_chuyen_nganh/Documents/DAC_TA_NHAN_DIEN_CU_CHI_TAY_DONG_VA_DIEU_KHIEN_MAY_TINH_KHONG_CHAM.md — 1.1, bước kế tiếp của docs/ROADMAP.md.

## Global Constraints

- Một người, đúng một tay; dùng num_hands=2 để phát hiện trường hợp hai tay và từ chối.
- Tọa độ x/y, 42 giá trị cục bộ + hai giá trị cổ tay toàn cục; sửa tỷ lệ ảnh trước khi chuẩn hóa lòng bàn tay.
- Chuỗi 30 mẫu tại 20 Hz; chỉ nội suy giữa dữ liệu hợp lệ đã nhận, khe hở tối đa 100 ms.
- Không thấy tay/hai tay/đặc trưng lỗi thì xóa bộ đệm; không tạo dữ liệu giả.
- Xem trước không điều khiển máy tính và không ghi hình/dữ liệu người dùng.
- Dùng nhóm phụ thuộc vision; chưa cài Torch và nhóm điều khiển.

## Review Focus

- Mất hướng vuốt do trừ cổ tay: kiểm tra hình dạng không đổi khi dịch tay nhưng hai giá trị cổ tay thay đổi đúng.
- Dữ liệu đến không đều: kiểm tra lưới 50 ms, không nhân đôi khi camera chạy nhanh, reset khi có gap >100 ms.
- Hai tay/mất tay: parse thành trạng thái không hợp lệ và xóa toàn chuỗi.
- Camera đọc lỗi/đóng cửa sổ: luôn giải phóng camera và landmarker.
- Model thiếu hoặc thư viện thiếu: CLI báo cách chuẩn bị tài nguyên, check/help không mở camera.

## Interfaces

- camera.py: CameraError; CameraFrame(timestamp_ms, image); Camera(config), read(), close(), context manager.
- landmarks.py: HandObservation(landmarks_xy, hand_count, handedness, reason), observation_from_result(result); HandTracker(model_path), detect(frame,timestamp_ms), close(), context manager.
- features.py: extract_features(landmarks_xy, frame_size=(width,height)); SequenceBuffer(length=30,sample_rate_hz=20,max_gap_ms=100), push(timestamp_ms,features_or_none), reset(), size.
- app.py: run_preview(config, headless=False, max_frames=None) -> dict tóm tắt, không lưu frame.
- cli.py: preview [--headless --max-frames N] [--camera-index N]. Các lệnh run/train/collect còn chờ bước sau.

### Task 1: Features and time buffer

- [x] Viết test trước cho tỷ lệ ảnh, vị trí cổ tay, input lỗi, nội suy, dữ liệu đến nhanh và reset.
- [x] Chạy test xác nhận thiếu triển khai.
- [x] Viết extract_features và SequenceBuffer; chạy test nhóm này.

### Task 2: Camera and hand adapter

- [x] Viết test trước cho release khi lỗi, chiều gương, timestamp tăng, không tay/hai tay/21 điểm hợp lệ.
- [x] Chạy test xác nhận thiếu triển khai.
- [x] Viết Camera và HandTracker; kiểm tra model thật trên ảnh trống, không dùng ảnh người dùng lưu xuống đĩa.

### Task 3: Preview and docs

- [x] Test vòng preview với biên I/O giả và thuật toán thật, bao gồm reset bộ đệm khi mất tay và cleanup khi lỗi.
- [x] Triển khai preview/CLI và test toàn bộ dự án.
- [x] Cài nhóm vision, lấy model chính thức, kiểm tra có giới hạn bằng webcam nếu phần cứng truy cập được.
- [x] Cập nhật README/ROADMAP, ghi rõ phần đã xác minh và giới hạn thử nghiệm.

## Verification

26 test pass; compileall, CLI help/check và pip check thành công. Webcam thật chạy headless 30 frame và cửa sổ 15 frame, không có tay trong hai lượt đó. Model thật nhận một/hai tay trên mẫu chính thức, tạo được 44 đặc trưng và ghép [30,44] từ đặc trưng tĩnh. Đã ghi nhận độ chậm một frame khi tracker đổi cảnh đột ngột; không coi đây là đánh giá cử chỉ động. Chi tiết ở docs/VERIFICATION-2026-10-30.md.

Người dùng đã yêu cầu thực hiện bước kế tiếp; triển khai trực tiếp trong phiên này. Không tạo commit/push hoặc mở rộng sang huấn luyện/điều khiển.
