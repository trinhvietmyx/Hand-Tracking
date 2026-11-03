# Thu thử 50 clip có nhãn

Đóng cửa sổ `preview` trước khi mở bộ thu; chỉ chạy một cửa sổ thu tại một thời điểm. Giữ cấu hình camera, chiều gương và nhịp lấy mẫu thống nhất trong cả phiên.

## Bắt đầu

Tại thư mục Hand-Tracking, chạy:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10
```

Đây là mục tiêu **10 clip hợp lệ mỗi nhãn trong phiên pilot_01**, tổng 50 clip. Thứ tự mặc định: BACKGROUND, SWIPE_LEFT, SWIPE_RIGHT, SWIPE_UP, SWIPE_DOWN. Chương trình chuyển sang nhãn kế tiếp sau khi đủ số lượng.

Mỗi lần thu:

1. Đưa đúng một bàn tay vào khung; kiểm tra trạng thái `one_hand`.
2. Đọc nhãn và hướng dẫn ở cửa sổ; đặt tay ở vị trí chuẩn.
3. Nhấn **Space**. Có hai giây `GET READY`, chưa ghi clip ở giai đoạn này.
4. Khi xuất hiện **RECORDING**, thực hiện đúng một lần vuốt, khoảng 0,5–1 giây, giữ tay còn trong khung đến khi báo **SAVED**. Tránh đưa tay nhanh trở lại trong cùng clip.
5. Đưa tay về vị trí chuẩn ở giai đoạn chờ; nhấn Space để thu mẫu kế tiếp.

Đối với **BACKGROUND**, vẫn giữ một tay nhìn thấy rõ: đứng yên hoặc chuyển động chậm, không thực hiện bốn động tác vuốt. Trường hợp không có tay được xử lý là tracking mất, không phải clip nền hợp lệ.

Các hướng trái/phải/lên/xuống theo hình xem trước. Với SWIPE_LEFT, di chuyển bàn tay trên hình từ phải sang trái; SWIPE_RIGHT làm ngược lại.

Mỗi lượt cần chuỗi liên tục đủ 30 mẫu ở 20 Hz, xấp xỉ 1,5 giây. Mất tay, hai tay, hình dạng không chuẩn hóa được hoặc khe hở tracking trên 100 ms sẽ báo **RETRY** và không lưu lượt đó. Nhấn Space để thu lại cùng nhãn. Bộ thu kiểm tra tính hợp lệ của tracking, chưa thể biết bạn đã thực hiện đúng động tác của nhãn hay chưa.

**Q**, **Esc** hoặc đóng cửa sổ: dừng và bỏ lượt còn dở. Những mẫu đã báo SAVED vẫn được giữ. Không gửi thao tác điều khiển máy tính trong quá trình thu.

## Dừng và thu tiếp

Chạy lại đúng lệnh đầu để tiếp tục. `--count 10` là tổng mục tiêu/nhãn trong phiên, không phải thêm mười clip mỗi lần chạy. Ví dụ đã có bảy clip SWIPE_LEFT thì chỉ thu thêm ba clip cho nhãn đó.

Nếu thu ở buổi khác, dùng session mới thay vì tái sử dụng tên cũ. Tên phiên dùng chữ không dấu, số, dấu gạch dưới hoặc gạch ngang. Không dùng một tên phiên cho cả train và validation/test. Chương trình từ chối nếu split, chiều gương hoặc hợp đồng đặc trưng của phiên thay đổi.

Chỉ thu một nhãn, hoặc dùng camera khác:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10 --label SWIPE_LEFT
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10 --camera-index 1
```

`--countdown` đổi số giây chuẩn bị; mặc định hai giây. Nên giữ mặc định khi mới tập thu.

## Sau khi thu

```powershell
.\.venv\Scripts\python.exe -m hand_tracking dataset-check --split train
```

Lệnh kiểm tra manifest và NPZ, đối chiếu nhãn/phiên/split/thông số, xác nhận video gốc còn tồn tại và báo số clip theo lớp. Sau pilot đầy đủ, nếu chưa có dữ liệu khác trong train, kết quả mong đợi là `samples: 50`, `input_shape: [50,30,44]` và mười clip ở mỗi nhãn.

Mở một số video AVI trong `data/raw/train/<LABEL>/` để xem đúng hướng và có một động tác/clip. `dataset-check` không thẩm định ý nghĩa cử chỉ hoặc thay việc xem lại nhãn. Mẫu làm sai có thể bỏ bằng lệnh dataset-remove dưới đây, thay vì tự xóa riêng video hoặc NPZ.

Video được lưu ở dạng sạch, chưa vẽ landmark/chữ. NPZ chứa sẵn đặc trưng nên chưa cần chạy một lệnh extract riêng cho những clip này.

## Thu sai: bỏ mẫu và thu lại

Thoát cửa sổ collect trước khi sửa dữ liệu. Giữ nguyên năm nhãn trong labels.py; chỉ bỏ các clip đã thu sai.

Ví dụ muốn bỏ mẫu SWIPE_LEFT vừa thu cuối cùng trong pilot_01:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking dataset-remove --session pilot_01 --split train --label SWIPE_LEFT --last
```

Lệnh trên chỉ xem trước: `matched` là số mẫu được chọn, `applied: false` nghĩa là dữ liệu còn nguyên. Thêm `--apply` để thực hiện:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking dataset-remove --session pilot_01 --split train --label SWIPE_LEFT --last --apply
```

Nếu muốn bỏ **toàn bộ mẫu của nhãn SWIPE_LEFT trong phiên pilot_01**, dùng cùng lệnh nhưng bỏ `--last`. Thay SWIPE_LEFT bằng BACKGROUND, SWIPE_RIGHT, SWIPE_UP hoặc SWIPE_DOWN tùy nhãn cần thu lại. Các nhãn và phiên khác được giữ nguyên.

Sau đó thu lại đúng nhãn:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking collect --session pilot_01 --split train --count 10 --label SWIPE_LEFT
```

Collector đếm lại số mẫu đang còn và bù đến mười mẫu. Session metadata vẫn được giữ để đảm bảo hợp đồng tiền xử lý không đổi.

Các tệp bị bỏ được chuyển vào `data/removed/<removal_id>/`, cùng `removed.csv` và bản manifest trước thay đổi. Chúng không được dùng khi load tập dữ liệu. Lệnh xóa trả `removal_id` và `backup_dir`; không xóa vĩnh viễn video/NPZ.

Nếu bỏ nhầm, khôi phục bằng lệnh sau; thay MA_BACKUP bằng removal_id đã nhận:

```powershell
.\.venv\Scripts\python.exe -m hand_tracking dataset-restore --backup-id MA_BACKUP --apply
```

Bỏ `--apply` để chỉ xem trước. Restore ghép lại những clip đã bỏ, giữ các mẫu mới thu sau đó; nếu tệp hoặc clip_id gốc đã tồn tại thì từ chối ghi đè. Không chép đè manifest_before.csv lên manifest hiện tại vì sẽ làm mất chỉ mục các mẫu mới.

## Tổ chức tệp

- `data/raw/<split>/<LABEL>/<session>_<clip_id>.avi`: các frame gốc đã áp dụng chiều gương theo cấu hình.
- `data/processed/<split>/<LABEL>/<session>_<clip_id>.npz`: đặc trưng, nhãn, tọa độ landmark và timestamp.
- `data/manifest.csv`: chỉ mục những clip đã lưu thành công.
- `data/sessions/<session>.json`: split và hợp đồng tiền xử lý của phiên.

Không ghi đè clip cũ. Video/NPZ được chuẩn bị trước, kiểm tra đọc được rồi mới cập nhật manifest. Lỗi ghi thông thường làm hủy các tệp mới của lượt đó. Dùng Q/Esc để thoát bình thường; nếu tiến trình bị tắt đột ngột khi đang ghi, kiểm tra lại dữ liệu trước khi huấn luyện.

## Tiến tới bộ 250 clip

Nếu 50 clip pilot có chất lượng tốt và được dùng cho train:

- Train: pilot_01 đã có 10 clip/nhãn; thu thêm một phiên train_02 với `--count 20` để đủ 30 clip/nhãn, tổng 150 clip.
- Validation: một phiên validation_01 riêng, `--split validation --count 10`, tổng 50 clip.
- Test: một phiên test_01 riêng, `--split test --count 10`, tổng 50 clip.

Đánh giá chất lượng pilot trước khi thu hàng loạt. Giữ test cho đánh giá cuối; không dùng nó để chọn mô hình hoặc ngưỡng.
