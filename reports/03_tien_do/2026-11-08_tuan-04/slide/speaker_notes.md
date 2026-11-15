# Ghi chú thuyết trình — tuần 4, 08/11/2026

16 slide, không có phần kế hoạch tuần tiếp theo. Dùng phần lời nói để tập trình bày; nguồn cuối mục để tra cứu.
Sinh viên: Trịnh Viết Mỹ — 2380601382 — 23DTHA3. GVHD: PGS.TS. Võ Đình Bảy.
Các câu trong tài liệu là lời gợi ý; chỉ trình bày mức hiểu và công việc bạn có thể tự giải thích, kiểm chứng.

## Slide 1. Mở đầu

Em là Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3. Em xin báo cáo tiến độ tuần 4 của đề tài nhận diện cử chỉ tay động và điều khiển máy tính không chạm, dưới sự hướng dẫn của PGS.TS. Võ Đình Bảy.

Theo góp ý của thầy ở tuần 2, em trình bày công trình nghiên cứu có liên quan, giải thích phương pháp và đối chiếu với code hiện tại. Sau đó là dữ liệu, kết quả và giới hạn đã ghi nhận. Bài báo cáo tập trung vào phần đã làm và đã kiểm tra trong lần báo cáo này.

## Slide 2. Bài toán và phạm vi

Hệ thống dùng webcam RGB để nhận biết bốn hướng cử chỉ và một lớp nền. Trái/phải dùng chuyển slide; lên/xuống dùng cuộn trang; lớp nền giúp biểu diễn trạng thái không phát lệnh.

Phạm vi hiện tại là một bàn tay hợp lệ, chạy trên CPU. Ứng dụng đích phải có focus để nhận phím hoặc thao tác cuộn. Độ đúng khi phân loại clip và độ ổn định khi điều khiển liên tục là hai phép đánh giá khác nhau; báo cáo hiện đã có kết quả cho clip.

## Slide 3. Các công trình liên quan

Em đối chiếu ba hướng nghiên cứu. IPN HandS của Benitez-Garcia và cộng sự, Applied Sciences 2025, gần cách triển khai hiện tại vì dùng chuỗi điểm bàn tay và LSTM. SKETCH của Han và cộng sự, NeurIPS 2025, chuyển skeleton thành biểu diễn dạng ảnh rồi dùng backbone thị giác. ConvMixFormer của Garg, Ghosh và Pradhan, WACV 2025, nghiên cứu bộ trộn tích chập trong kiến trúc nhận diện cử chỉ động.

Các bài dùng dữ liệu và giao thức khác nhau, nên không dùng các tỷ lệ này để kết luận mô hình đồ án tốt hơn hoặc kém hơn. DR/FP của SKETCH cũng không phải accuracy. Phần tiếp theo đọc sâu IPN HandS để làm rõ bài toán, thí nghiệm và điều có thể học từ nghiên cứu.

Nguồn tra cứu (không cần đọc thành lời):
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition, Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. https://www.mdpi.com/2076-3417/15/11/6321
[2] S. H. Han et al., Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition, Advances in Neural Information Processing Systems, vol. 38, NeurIPS, 2025. https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html
[3] M. Garg, D. Ghosh, and P. M. Pradhan, ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition, Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pp. 6156–6166, 2025. https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html

## Slide 4. Đọc hiểu IPN HandS

Bài IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition được công bố trên Applied Sciences năm 2025, DOI 10.3390/app15116321. Trọng tâm là chất lượng gán nhãn điểm bàn tay và khoảng thời gian cử chỉ; LSTM được dùng làm mô hình cơ sở để kiểm tra tác động của chất lượng dữ liệu.

Tác giả dùng cùng 200 video, chia 50 người thành 37 người train và 13 người test. Ba mô hình được train riêng từ ba nguồn nhãn: MediaPipe Hands, MediaPipe Holistic và IPN HandS đã sửa nhãn. Chúng dùng cùng cấu trúc ba tầng LSTM, mỗi tầng 256 nút ẩn, dropout 0,3 và phân loại 14 cử chỉ. Các phép chạy được lặp ba lần.

Bảng 6 cho thấy IPN HandS đạt accuracy 91,2 ± 1,4% và recall trung bình 78,0 ± 1,2%. So với MP Hands, recall tăng 15,3 điểm phần trăm. Đây là kết quả của bài báo. Vì dữ liệu bài có mất cân bằng lớp, chỉ nhìn accuracy có thể bỏ qua lớp ít mẫu; cần đọc cả recall trung bình. Bài học là phải kiểm tra chất lượng nhãn và giao thức, không chỉ đổi kiến trúc mạng.

Nguồn tra cứu (không cần đọc thành lời):
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition, Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. https://www.mdpi.com/2076-3417/15/11/6321

## Slide 5. Ý nghĩa cấu hình của đồ án

Code hiện tại khác cấu hình và dữ liệu của bài. Mỗi bước có 44 đặc trưng: 42 tọa độ xy cục bộ của 21 điểm, nối hai tọa độ cổ tay trong ảnh. Chuẩn hóa cục bộ giữ hình dạng; vị trí cổ tay giữ thông tin quỹ đạo toàn cục. Chưa có phép thử bỏ/giữ hai giá trị này để kết luận tác động tới accuracy.

Chuỗi gồm 30 mẫu tại 20 Hz. Có 29 khoảng giữa mẫu đầu và mẫu cuối, nên khoảng đầu–cuối là 1,45 giây, thường mô tả là cửa sổ gần 1,5 giây. Đây là nhịp lấy mẫu cấu hình, không phải FPS toàn hệ thống đã đo.

Hidden size 64 và một tầng là cấu hình cơ sở đang có, tạo mô hình 28.485 tham số. Báo cáo chưa có đối chứng giữa các hidden size để nói 64 là tối ưu. Năm nhãn gồm bốn hướng và nền, khác phép thử 14 cử chỉ có chủ đích của bài. Khác cấu hình chưa phải bằng chứng cải tiến hoặc tái lập nghiên cứu.

Nguồn tra cứu (không cần đọc thành lời):
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition, Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. https://www.mdpi.com/2076-3417/15/11/6321

## Slide 6. Luồng hệ thống

Ảnh webcam được đưa qua MediaPipe để lấy 21 điểm bàn tay. Chương trình chấp nhận đúng một tay hợp lệ, biến thành 44 đặc trưng và đưa vào bộ đệm theo thời gian. Khi đủ 30 mẫu, LSTM trả điểm số cho năm nhãn.

Dự đoán còn đi qua điều kiện xác nhận trước khi phát lệnh: ngưỡng 0,8, giữ ổn định ít nhất 150 ms và ít nhất ba dự đoán mới. Cooldown 1.000 ms cùng nền ổn định 300 ms giúp hạn chế lặp. F8 bật/tạm dừng; F9 dừng chương trình. Những cơ chế này đã có trong mã, chưa thay thế phép thử điều khiển trực tiếp.

Nguồn tra cứu (không cần đọc thành lời):
[4] F. Zhang et al., MediaPipe Hands: On-device Real-time Hand Tracking, arXiv:2006.10214, 2020. https://arxiv.org/abs/2006.10214
[7] Google AI Edge, Hand Landmarker, Official MediaPipe documentation, 2026. https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python

## Slide 7. Tiền xử lý và chuỗi

Ba ảnh được lấy từ clip train SWIPE_LEFT tại 150, 750 và 1.250 ms. Đây là hình minh chứng từ dữ liệu đã thu.

extract_features đổi tọa độ về cùng đơn vị ảnh, trừ cổ tay và chia theo kích thước lòng bàn tay. Sau khi có 42 giá trị cục bộ, hàm nối hai tọa độ cổ tay thành vector 44 chiều. SequenceBuffer dùng timestamp để lấy mẫu đều mỗi 50 ms. Nội suy khe ngắn chỉ thực hiện khi đã biết cả hai đầu mút; mất tay hoặc khoảng hở trên 100 ms làm xóa chuỗi.

NPZ có kích thước đúng mới chứng minh hợp lệ về định dạng. Ý nghĩa nhãn và cách thực hiện cử chỉ vẫn cần xem lại video.

## Slide 8. Dữ liệu thực tế

Đồ án có 250 clip hợp lệ, cân bằng giữa năm nhãn. Mỗi nhãn có 30 train, 10 validation và 10 test; tổng tương ứng 150, 50, 50. Train thuộc pilot_01 và train_02, validation thuộc val_01, test thuộc test_01.

Không thấy chuỗi đặc trưng trùng tuyệt đối xuyên tập. Điều này không chứng minh độc lập theo người dùng. Manifest chưa có subject_id và báo cáo chưa có đánh giá người chưa thấy; cách chia hiện tại là theo phiên thu.

## Slide 9. Giải thích hai dòng forward

Khi mở model.py, em đi theo hai dòng forward. Dòng đầu gọi self.lstm(features). Đầu vào [B,30,44] trở thành chuỗi trạng thái [B,30,64]. B là số mẫu trong batch, 30 là số bước, 44 là đặc trưng mỗi bước, 64 là chiều trạng thái ẩn.

sequence[:, -1, :] lấy trạng thái ở thời điểm cuối cho mỗi mẫu, được [B,64]. Trạng thái này mang thông tin đã tích lũy qua các bước trước; không phải lấy nhãn cuối hoặc chỉ lấy 44 giá trị của frame cuối. classifier là Linear 64→5, trả logits. Softmax và chọn nhãn được tính trong predict_gesture sau forward.

Đã kiểm tra tách từng bước trên một clip test lưu sẵn: [1,30,44] → [1,30,64] → [1,64] → [1,5], trùng kết quả model(x). Đây là phép kiểm tra luồng thực thi của code đồ án; chưa phải chạy lại thí nghiệm LSTM gốc của tác giả.

Nguồn tra cứu (không cần đọc thành lời):
[5] S. Hochreiter and J. Schmidhuber, Long Short-Term Memory, Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997. https://pubmed.ncbi.nlm.nih.gov/9377276/
[6] PyTorch Contributors, torch.nn.LSTM, Official PyTorch documentation, version 2.15, 2026. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html

## Slide 10. Đường cong huấn luyện

Biểu đồ lấy đúng 30 dòng stdout đã lưu trong notebook; loss được làm tròn bốn chữ số theo log. Train loss giảm từ 1,5541 tới 0,1293; validation loss từ 1,4313 tới 0,1720 ở epoch cuối.

Checkpoint được chọn bằng validation loss thấp nhất ở epoch 23, loss đầy đủ khoảng 0,108522 và validation accuracy 94%. Không chọn checkpoint theo test. Cấu hình train là CrossEntropyLoss, Adam learning rate 0,001, batch 16, seed 42, chạy CPU. Đây mới là một lần chạy có log, chưa có thống kê nhiều seed hoặc kết luận cấu hình tối ưu.

## Slide 11. Chỉ số đánh giá

Chạy lại checkpoint trên 50 clip test cho đúng 40 clip, accuracy 80%; Macro-Precision và Macro-Recall đều 0,8; Macro-F1 khoảng 0,7619. Các giá trị khớp kết quả đã lưu.

Macro-F1 lấy trung bình F1 từng lớp, không phải tính F1 trực tiếp từ hai số macro precision/recall. Nền, trái và phải đúng 10/10 trong tập test nhỏ này. Vuốt lên recall chỉ 0,1, vì vậy 80% tổng thể chưa có nghĩa mọi hướng đều dùng tốt. Mỗi lớp chỉ có 10 mẫu test; một clip làm thay đổi recall lớp 10 điểm phần trăm.

## Slide 12. Phân tích lỗi lên và xuống

Hàng là nhãn thật, cột là nhãn dự đoán. Chín trong mười clip vuốt lên bị nhận thành xuống. Ở lớp xuống có chín clip đúng và một clip bị nhận thành lên. Toàn bộ mười lỗi test tập trung ở cặp này.

Ảnh minh họa trích từ một clip UP bị đoán DOWN; dự đoán sai này có mức tin cậy khoảng 0,965. Vì thế chỉ tăng ngưỡng chưa chắc sửa lỗi. Qua một số mẫu có khác biệt tư thế ngón tay giữa nhãn; đây là dấu hiệu cần xem quy cách dữ liệu, chưa chứng minh nguyên nhân duy nhất hoặc mô hình chỉ học tư thế.

## Slide 13. Demo và giới hạn kiểm thử

Video dài 10 giây, phát lại năm clip test với nhãn thật và dự đoán từ toàn chuỗi. Có giữ một clip UP bị nhận sai để minh họa giới hạn. Đây là phát lại dữ liệu đã lưu, không phải bản ghi webcam đang điều khiển ứng dụng khác.

Bộ 60 test tự động đã qua, kiểm tra logic và dùng mô phỏng tại biên phần cứng. Chưa có dữ liệu thực nghiệm cho 40 lượt trực tiếp, 5 phút nền, FPS toàn luồng hoặc độ trễ tới lệnh. Không dùng nhịp lấy mẫu 20 Hz để thay cho phép đo FPS.

## Slide 14. Trạng thái đã kiểm tra

Bảng này tách từng hạng mục theo minh chứng. Hiện có dữ liệu, tiền xử lý, mô hình, log train, checkpoint, kết quả test, mã tích hợp và test tự động. Đây là phần đã có thể mở tệp hoặc chạy kiểm tra lại.

Có mã phát lệnh không đồng nghĩa đã đo đầy đủ điều khiển trực tiếp. Không đổi thành phần trăm hoàn thành khi chưa thống nhất tiêu chí và trọng số. Những mục còn thiếu trong bảng là giới hạn bằng chứng của lần báo cáo này.

## Slide 15. Giới hạn và cách diễn giải

Hai kết quả đã quan sát là nhầm lên/xuống và chênh 14 điểm phần trăm giữa validation 94% với test 80%. Từ một lần train và một bộ test nhỏ, chưa đủ kết luận nguyên nhân duy nhất là overfitting.

Giả thuyết liên quan tư thế, cách thu hoặc sai lệch giữa các phiên cần được phân biệt với kết quả đã đo. Độ tổng quát sang người khác, FPS/latency và độ ổn định khi phát lệnh hiện chưa có dữ liệu thực nghiệm. Việc phân tích lỗi và điều kiện thử giúp đặt đúng phạm vi kết luận, không che các trường hợp nhận sai.

## Slide 16. Kết luận

Báo cáo đã chỉ rõ nghiên cứu IPN HandS và bài học về chất lượng gán nhãn, đối chiếu các khác biệt với cấu hình hiện tại, đồng thời giải thích trực tiếp hai dòng forward của LSTM trong code.

Kết quả hiện có gồm 250 clip, log 30 epoch, checkpoint và đánh giá 50 clip đạt accuracy 80%, Macro-F1 khoảng 0,7619. Luồng thực thi đã được đối chiếu ở một clip và code tích hợp đã có. Giới hạn chính là lỗi lên/xuống và phần đo điều khiển trực tiếp còn thiếu. Chưa có minh chứng tái lập thí nghiệm LSTM gốc hoặc chứng minh cấu hình tối ưu. Em xin kết thúc phần báo cáo tiến độ.

Nguồn tra cứu (không cần đọc thành lời):
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition, Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. https://www.mdpi.com/2076-3417/15/11/6321

## Câu hỏi cần tập trả lời

**Đóng góp chính của IPN HandS là gì?** Công cụ/dữ liệu landmark và biên thời gian được sửa nhãn; LSTM là mô hình cơ sở để đo tác động của chất lượng gán nhãn.

**Vì sao 44 đặc trưng?** 21 điểm xy tạo 42 giá trị cục bộ; nối hai tọa độ cổ tay. Chưa có đối chứng bỏ/giữ để kết luận mức tăng accuracy.

**Vì sao 30 mẫu, 64 nút ẩn?** 30 mẫu ở 20 Hz tạo cửa sổ gần 1,5 giây. 64 là cấu hình cơ sở đang có, tổng 28.485 tham số; chưa có thí nghiệm chọn tối ưu.

**MediaPipe có nhận diện năm cử chỉ không?** Trong project, MediaPipe tìm điểm bàn tay; LSTM phân loại chuỗi thành năm nhãn.

**Lấy trạng thái cuối có bỏ hết các frame trước không?** Trạng thái cuối LSTM đã được cập nhật theo chuỗi; nó khác việc chỉ lấy vector đặc trưng của frame cuối.

**80% test có nghĩa hệ thống ổn định không?** Chỉ phản ánh 40/50 clip đúng. Lớp lên recall 0,1; chưa đo đủ điều khiển liên tục.

**Validation 94%, test 80% là do overfitting?** Có chênh lệch nhưng một lần chạy và ít mẫu chưa xác định được nguyên nhân duy nhất.

**Đã chạy code tác giả chưa?** Chưa có minh chứng tái lập thí nghiệm LSTM gốc. Phép trace là của code đồ án trên clip tự thu.

**Video có phải demo điều khiển trực tiếp?** Là phát lại clip test đã lưu với dự đoán toàn chuỗi. Chưa có số liệu thử trực tiếp trong báo cáo này.
