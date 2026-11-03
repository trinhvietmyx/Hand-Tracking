# Project Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng bộ khung gọn trong Hand-Tracking, sẵn sàng viết code theo đặc tả 1.1.

**Architecture:** Một Python package trong src/hand_tracking, cấu hình JSON và CLI chung. Các module camera, đặc trưng, dữ liệu, LSTM và điều khiển tách thành tệp nhỏ; chỉ cấu hình và CLI kiểm tra được triển khai ở bước nền móng.

**Tech Stack:** Python 3.11, setuptools, unittest; khai báo nhóm thư viện ứng dụng để cài ở bước triển khai camera/huấn luyện.

**Spec:** D:/Learn/Hutech/Do_an_chuyen_nganh/Documents/DAC_TA_NHAN_DIEN_CU_CHI_TAY_DONG_VA_DIEU_KHIEN_MAY_TINH_KHONG_CHAM.md — phiên bản 1.1.

## Global Constraints

- Bốn cử chỉ vuốt và một lớp nền; ID nền = 0, trái/phải/lên/xuống = 1/2/3/4.
- Đầu vào 30 bước × 44 đặc trưng, lấy mẫu 20 Hz; LSTM một tầng, hidden size 64.
- Dữ liệu chia theo phiên train/validation/test, kế hoạch 150/50/50 clip.
- Mặc định chưa bật điều khiển; F8 bật/tạm dừng, F9 dừng toàn cục khi triển khai runtime.
- Lần này chỉ dựng nền móng, không tự thu hình, tải mô hình, huấn luyện hoặc gửi lệnh máy tính.
- Không tạo commit/push hoặc triển khai các phần mở rộng ngoài yêu cầu.

## Review Focus

- Chạy từ thư mục khác: đường dẫn dữ liệu phải bám gốc dự án chứa configs, không bám working directory.
- Sai feature_dim/num_classes: từ chối cấu hình trước khi có thể nạp mô hình.
- control_enabled=true trong JSON: từ chối tự bật điều khiển khi khởi động.
- Cấu hình thiếu/sai kiểu: báo lỗi gọn và exit code khác 0.
- Lệnh chưa được triển khai: không báo thành công giả hoặc mở camera/gửi thao tác.

## Files and interfaces

- pyproject.toml, requirements.txt, .python-version, .gitignore: cài đặt và môi trường.
- configs/default.json: cấu hình duy nhất cho bản cơ bản.
- src/hand_tracking/config.py: load_config(path) -> ProjectConfig, resolve các đường dẫn theo gốc dự án.
- src/hand_tracking/labels.py: Gesture IntEnum và thứ tự nhãn dùng chung.
- src/hand_tracking/cli.py, __main__.py: main(argv=None) -> int; check và các lệnh dự kiến.
- camera.py, landmarks.py, features.py, collection.py, dataset.py, model.py, training.py, evaluation.py, control.py, app.py: vị trí và hợp đồng dự kiến, chưa có thuật toán.
- data/raw, data/processed: ba phiên train/validation/test; models, assets/hand_landmarker, outputs: tài nguyên sinh ra.
- README.md, data/README.md, docs/ROADMAP.md: cách chạy, dữ liệu và thứ tự code tiếp.
- tests/test_cli.py: kiểm tra hành vi thực qua CLI, không kiểm tra số lượng thư mục hoặc nội dung văn bản.

### Task 1: Configuration and CLI foundation

**Consumes:** đặc tả 1.1 và configs/default.json.

**Produces:** ProjectConfig; CLI check trả JSON cấu hình/đường dẫn và tình trạng tài nguyên; CLI scaffold trả exit code 2 cho chức năng chưa làm.

- [x] Tạo metadata, cấu hình, nhãn và test CLI; chưa viết bộ nạp cấu hình/CLI.
- [x] Chạy unittest và xác nhận test fail vì CLI chưa có.
- [x] Viết bộ nạp cấu hình và CLI tối thiểu để xử lý năm điều kiện Review Focus.
- [x] Chạy toàn bộ unittest, kiểm tra CLI help/check từ môi trường cài editable.

### Task 2: Source and data layout

**Consumes:** cấu hình và các nhãn từ Task 1.

**Produces:** các tệp module có mô tả công việc/interface dự kiến và thư mục dữ liệu có hướng dẫn.

- [x] Dựng các tệp module và thư mục cần cho bản cơ bản; không cài thuật toán giả.
- [x] Viết README/ROADMAP, phân biệt phần đã chạy được và phần chưa triển khai.
- [x] Kiểm tra packaging, cú pháp, lệnh báo chưa triển khai và toàn bộ test lần cuối.

## Verification — 29/10/2026

- Đã tạo .venv Python 3.11 và cài editable thành công; chưa cài nhóm app.
- Trước triển khai: test fail vì chưa có CLI; sau triển khai: toàn bộ 4 test pass.
- Đã kiểm tra compileall, console entry point --help và check từ thư mục Reference bằng đường dẫn cấu hình tuyệt đối.
- check báo đúng hai model chưa có và các phụ thuộc ứng dụng chưa cài. Không mở camera hoặc gửi lệnh hệ điều hành.

Không cần test tự động cho README hoặc tệp giữ chỗ. Việc dựng bộ khung đã được người dùng yêu cầu trực tiếp; thực hiện trong phiên này, không dừng ở bản kế hoạch.
