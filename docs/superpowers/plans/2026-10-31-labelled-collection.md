# Labelled Collection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thu thử 10 clip mỗi nhãn bằng cửa sổ có đếm ngược, lưu video/đặc trưng và kiểm tra dữ liệu trước huấn luyện.

**Architecture:** collection.py quản lý một lượt ghi và vòng tương tác; dataset.py quản lý session, ghi video/NPZ/manifest và đọc kiểm tra dữ liệu. Dùng lại Camera, HandTracker, extract_features và SequenceBuffer; app.py chia sẻ phần vẽ/phím cửa sổ.

**Tech Stack:** Python 3.11, NumPy, OpenCV MJPG/AVI, MediaPipe, CSV/JSON, unittest. Không thêm phụ thuộc.

**Spec:** D:/Learn/Hutech/Do_an_chuyen_nganh/Documents/DAC_TA_NHAN_DIEN_CU_CHI_TAY_DONG_VA_DIEU_KHIEN_MAY_TINH_KHONG_CHAM.md — bản 1.1 và phần thu thử 50 clip đã được người dùng đồng ý.

## Global Constraints

- Năm nhãn; 30 × 44 float32, 20 Hz mặc định; dùng cùng tiền xử lý với preview.
- Chỉ ghi sau SPACE và đếm ngược; Q/Esc/đóng cửa sổ hủy lượt dở, giữ các clip hoàn thành.
- Mất tay, nhiều tay, dữ liệu lỗi hoặc gap >100 ms làm loại toàn lượt; không lưu clip dở/không tự gán nhãn.
- Session không được dùng lại ở split khác hoặc với hợp đồng đặc trưng/chiều gương khác.
- Lưu video sạch trước overlay, timestamp thật, landmark, đặc trưng, nhãn và thông tin phiên; không ghi đè clip trước.
- Kiểm thử bằng dữ liệu tổng hợp trong thư mục tạm; không tạo dữ liệu huấn luyện giả trong dự án.

## Review Focus

- Mất tay ở giữa clip: không ghép hai đoạn tracking thành một mẫu.
- Tốc độ camera không đều: NPZ giữ timestamp thật và mốc lưới mẫu, video chỉ có FPS danh nghĩa đo từ lượt thu.
- Chạy lại lệnh: đếm clip đã có trong session, chỉ thu phần còn thiếu tới --count.
- Nhầm split/session hoặc đổi mirror: từ chối trước khi ghi.
- Writer lỗi hoặc thoát giữa lượt: không tạo manifest trỏ đến file hỏng và không đụng dữ liệu cũ.

## Interfaces and files

- collection.py: ClipRejected, ClipAttempt(config).push(frame, observation) -> RecordedClip | None; collect_clips(config,session_id,split,count,labels=None,countdown_seconds=2,max_frames=None) -> dict.
- dataset.py: DatasetError; RecordedClip(features,frames,frame_timestamps_ms,landmarks_xy,sample_timestamps_ms); DatasetStore(config,session_id,split).counts(), save(clip,label); load_split(config,split) -> (X,y,records).
- features.py: FEATURE_VERSION cho hợp đồng 44 chiều hiện tại.
- app.py: dùng chung draw_preview và poll_key; preview giữ nguyên hành vi.
- cli.py: collect --session NAME --split train --count 10 [--label NAME]; dataset-check --split train.
- tests/test_collection.py, tests/test_dataset.py, tests/test_cli.py: thuật toán thật, tệp tạm và I/O camera/tracker được thay ở biên.
- README.md, data/README.md, docs/COLLECTION.md, docs/ROADMAP.md, .gitignore: cách thu và bảo vệ dữ liệu sinh ra.

### Task 1: A complete clip and dataset storage

- [x] Viết test cho clip đủ thời gian, mất tay/gap, lưu đọc NPZ/video thật, session conflict, resume và file lỗi.
- [x] Xác nhận test fail trước triển khai.
- [x] Triển khai ClipAttempt, DatasetStore và load_split tối thiểu; chạy test.

### Task 2: Interactive collection and CLI

- [x] Test SPACE/countdown, không ghi khi chưa bấm, hủy/retry và resume bằng biên I/O giả.
- [x] Xác nhận test fail; triển khai collect_clips và các lệnh CLI.
- [x] Chạy toàn bộ test và smoke test codec/NPZ thật trong thư mục tạm.

### Task 3: User instructions

- [x] Hướng dẫn thu 50 mẫu pilot, xem lại video, kiểm tra số lượng và chia các phiên sau.
- [x] Cập nhật trạng thái, kiểm tra CLI/help/compileall; ghi rõ chưa thu cử chỉ thật thay người dùng.

## Verification — 31/10/2026

- Toàn bộ 46 test pass, gồm hồi quy preview và lỗi NPZ bị hỏng; tệp nguồn được đóng cả khi NumPy báo lỗi ZIP.
- Smoke test thật với codec MJPG, NPZ và CLI dataset-check: năm mẫu tổng hợp trong thư mục tạm, mỗi nhãn một mẫu, đọc được [5,30,44]. Không đưa các mẫu này vào dữ liệu dự án.
- Cửa sổ collect dùng webcam/model thật chạy có giới hạn tám frame trong một session ở thư mục tạm: không nhấn Space, saved_this_run=0; thoát và giải phóng tài nguyên.
- CLI help và compileall thành công. data/ của dự án vẫn chỉ có tài liệu và tệp giữ chỗ; người dùng sẽ tự thực hiện các cử chỉ để thu pilot.

Thực hiện trực tiếp trong phiên theo yêu cầu. Không commit/push hoặc huấn luyện mô hình ở bước này.
