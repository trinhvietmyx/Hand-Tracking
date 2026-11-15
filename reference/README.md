# Tài liệu tham khảo

Sáu thư mục tương ứng với các bài trong `notebook/hand_tracking.ipynb`. Mỗi thư mục có PDF và `Link_bai_bao.txt` ghi nguồn công bố, repo tác giả và commit đã đối chiếu.

Năm thư mục `Source/` là **Git submodule**, giữ mã nguồn ở commit đã dùng để đọc trong notebook. Các mô hình tham khảo không phải thành phần cần cài để chạy ứng dụng Hand-Tracking.

## Clone kèm mã nguồn tham khảo

```powershell
git clone --recurse-submodules https://github.com/trinhvietmyx/Hand-Tracking.git
```

Nếu đã clone project:

```powershell
git submodule update --init --recursive
```

Giữ các commit đã ghim khi đối chiếu bài báo. Lệnh update ở trên tải đúng commit được lưu trong project.

## Các repo tác giả

- **S2Gest:** [Chen-Ke-Fan/S2Gest](https://github.com/Chen-Ke-Fan/S2Gest).
- **SKETCH:** [capableofanything/SKETCH](https://github.com/capableofanything/SKETCH).
- **GESTRO:** [thohemp/gestro](https://github.com/thohemp/gestro).
- **ConvMixFormer:** [mallikagarg/ConvMixFormer](https://github.com/mallikagarg/ConvMixFormer).
- **IPN HandS:** [GibranBenitez/IPN-hand](https://github.com/GibranBenitez/IPN-hand).

Bài tổng quan Continuous Hand Gesture Recognition chưa có repo chính thức được xác minh trong bộ tài liệu hiện tại.

Notebook phân biệt nội dung bài báo, phần đọc tĩnh mã nguồn tham khảo và phần thực nghiệm của đồ án. Chưa tái lập benchmark LSTM gốc của IPN HandS. Việc tải submodule không tự cài thư viện hoặc chạy thí nghiệm của tác giả.

Bản quyền và giấy phép của từng mã nguồn thuộc repo tác giả; xem các tệp LICENSE và hướng dẫn đi kèm.
