# Hình ảnh dùng trong README

Các asset ở đây được tạo riêng cho README và dùng đường dẫn tương đối trong repository. Chúng không phụ thuộc vào thư mục `reference/`, `reports/`, dịch vụ lưu ảnh hoặc badge từ bên ngoài.

## Banner và badges

- `banner.png`: minh họa khái niệm được tạo bằng công cụ **imagegen** tích hợp, không phải ảnh chụp ứng dụng hoặc mô hình giải phẫu để đo đạc. Banner không biểu diễn độ chính xác, FPS hoặc kết quả thực nghiệm.
- `badges/*.svg`: đồ họa vector tĩnh cho các công nghệ có trong `pyproject.toml`. Python 3.11–3.12 là khoảng phiên bản khai báo; môi trường kiểm tra là Python 3.11/Windows.
- Badge **60 passed** ghi nhận lượt kiểm thử cục bộ ngày 16/11/2026. Repository chưa có workflow CI, nên badge này không phải trạng thái CI.

## GIF và ảnh giao diện

- `landmark-demo.gif`: phát lại landmark xy từ một clip test của mỗi nhãn. Confidence và nhãn dự đoán được tính lại bằng `predict_gesture()` trên toàn bộ chuỗi đặc trưng của clip, dùng checkpoint notebook ở epoch 23.
- `landmark-demo-still.png`: một khung hình của bản phát lại để xem khi không dùng ảnh động.
- `app-preview.png`: đầu ra của hàm `draw_preview()` thật trong `app.py`, dùng landmark đã lưu trên nền trống. Đây là render tĩnh để minh họa giao diện; `FPS: 0.0` không phải benchmark camera. Không mở webcam hoặc gửi thao tác desktop khi dựng ảnh.

GIF giữ chuyển động và hướng của dữ liệu, với phép phóng to đồng nhất để dễ nhìn. Nhãn dự đoán đứng yên trong mỗi clip vì được tính từ toàn bộ chuỗi. Có ví dụ vuốt lên bị nhầm thành vuốt xuống; không gán nhãn thành công cho mẫu đó. Nhịp GIF dùng 100 ms/khung và có giữ khung cuối để người xem đọc được nhãn, không dùng thời lượng GIF để đo độ trễ nhận diện.

Chỉ tọa độ landmark và kết quả dự đoán được dùng để dựng bản phát lại. Không sao chép video webcam, khuôn mặt, cảnh phòng riêng hoặc danh sách clip gốc vào thư mục này.

## Sơ đồ và số liệu

- `pipeline.svg`: sơ đồ code hiện tại, từ webcam đến landmark, bộ đệm, LSTM, GestureGate và thao tác máy tính.
- `confusion-matrix.png`: biểu đồ Matplotlib từ `outputs/notebook/evaluation.json` cục bộ, với hàng là nhãn thật và cột là dự đoán.
- `evaluation-summary.json`: bản rút gọn chỉ có số liệu tổng hợp và giao thức đánh giá. Không chứa đường dẫn máy, clip ID hoặc thông tin người thu.
- `test-results.png`: định dạng lại phần tóm tắt stdout/stderr thật của lệnh `python -m unittest discover -s tests -v`, chạy ngày 16/11/2026. Không phải ảnh chụp terminal hệ điều hành.
- `asset-manifest.json`: tên file, kích thước, SHA-256 và dự đoán các clip minh họa để đối chiếu.

Nguồn code: [features.py](../../src/hand_tracking/features.py), [model.py](../../src/hand_tracking/model.py), [app.py](../../src/hand_tracking/app.py) và [control.py](../../src/hand_tracking/control.py).

Các kết quả 80% accuracy, Macro-F1 0.7619 và epoch 23 thuộc thực nghiệm notebook trên dữ liệu tự thu, chia theo phiên. Chúng không phải kết quả benchmark của bài IPN HandS và không đánh giá trực tiếp việc điều khiển webcam liên tục. Nếu chạy lại mô hình hoặc đổi dữ liệu, cần cập nhật hình và số liệu tương ứng.

## Prompt tạo banner

Công cụ: **imagegen tích hợp**, nền không trong suốt. Ảnh gốc được sao chép nguyên vẹn vào `banner.png`.

<details>
<summary>Prompt đã dùng</summary>

```text
Create a polished editorial banner for the actual open-source student project named HAND-TRACKING. Very wide landscape 3:1 aspect ratio, intended as a GitHub README header. Light icy blue background (#edf3ff), rich cobalt blue (#2749c9), dark navy typography, tiny warm amber accents. Left 55%: striking legible custom geometric sans-serif typography with the exact title 'HAND-TRACKING' and underneath only the exact subtitle 'Dynamic gestures. Touchless control.' Right 45%: a tasteful technical illustration of ONE anatomically plausible open hand with FIVE fingers, represented as fine cobalt wire lines and distinct landmark nodes, with a few quiet horizontal motion trails to suggest a swipe. A subtle sampling grid and small timing ticks can appear behind the hand. Composition should feel like an intentional computer vision research identity with generous clean negative space, not a generic AI dashboard. Keep the hand and all text comfortably inside the canvas. This is a conceptual illustration, not an application screenshot. Do not depict a person, face, real room, computer UI, software window, metric, accuracy score, badge, certification, third party logo or simulated demo. No decorative cards, no neon green, no purple gradients, no photographic background, no watermark. Only the title and subtitle specified above may be written.
```

</details>

GitHub hỗ trợ [PNG, GIF và SVG](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files). Các file SVG ở đây chỉ dùng đồ họa và chữ; không có script, font bên ngoài hoặc tài nguyên nhúng từ dịch vụ khác.
