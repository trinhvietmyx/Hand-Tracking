# Remove Mistaken Recordings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Người dùng bỏ mẫu thu sai theo nhãn/phiên, có tùy chọn mẫu cuối và khôi phục, không sửa taxonomy.

**Architecture:** dataset_cleanup.py lọc manifest, kiểm tra đường dẫn rồi chuyển từng tệp sang vùng backup và cập nhật manifest nguyên tử. CLI mặc định chỉ xem trước; --apply mới thay đổi dữ liệu. Restore ghép lại đúng các hàng bị bỏ, giữ các mẫu mới thu sau đó.

**Tech Stack:** Python chuẩn, CSV/Path, unittest; dùng lại hợp đồng manifest hiện có.

**Spec:** Câu hỏi người dùng về xóa nhãn thu lỗi và docs/COLLECTION.md. Chỉ tạo công cụ; chưa được chỉ định nhãn/phiên nào cần xóa thực tế.

## Global Constraints

- Không xóa tên lớp trong labels.py.
- Phải chọn session, split, label; --last chỉ chọn hàng cuối trong nhóm đó.
- Mặc định dry-run; không sửa dữ liệu thật trong phiên lập trình này.
- Chỉ di chuyển từng video/NPZ đã xác minh thuộc đúng thư mục cấu hình; không xóa thư mục đệ quy.
- Giữ session metadata để collect tiếp tục bù đủ số lượng.

## Review Focus

- Chỉ bỏ đúng session/label, giữ nhãn khác và phiên khác.
- Dry-run không tạo backup hoặc sửa manifest.
- Đường dẫn sai/thiếu tệp phải bị chặn trước khi di chuyển.
- Manifest commit lỗi phải trả các tệp về chỗ cũ.
- Restore giữ mẫu thu mới và từ chối ghi đè/collision.

## Tasks

1. [x] Test trước remove/dry-run/last/rollback/path scope và restore sau khi có mẫu mới.
2. [x] Xác nhận test fail; triển khai remove_recordings và restore_recordings trong dataset_cleanup.py.
3. [x] Nối dataset-remove/dataset-restore CLI, chạy cả bộ test và cập nhật hướng dẫn thu.

## Verification

Toàn bộ 55 test pass, compileall thành công. Các kiểm tra apply/restore chỉ chạy trong thư mục tạm. CLI dry-run trên dữ liệu thật chọn một SWIPE_LEFT trong pilot_01; applied=false, SHA-256 manifest không đổi và tổng số mẫu vẫn 11. Không thay đổi mẫu thu của người dùng.

Không thực hiện thao tác xóa hoặc chuyển dữ liệu thật của người dùng. Không commit/push.
