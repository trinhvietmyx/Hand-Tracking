# Ghi chú thuyết trình — chỉnh theo góp ý GVHD tuần 2

Báo cáo online 08/11/2026 từ 14:00. Sinh viên Trịnh Viết Mỹ — 2380601382 — 23DTHA3.
GVHD: PGS.TS. Võ Đình Bảy (giữ theo bìa PowerPoint hiện có của người dùng).

Ưu tiên trình bày: bài báo cụ thể → hiểu phương pháp → giải thích code → kết quả → việc cần làm trước khi mở rộng.

## Slide 1. Trang bìa

Em là Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3. Em xin báo cáo tiến độ tuần 4 của đồ án dưới sự hướng dẫn của PGS.TS. Võ Đình Bảy. Nội dung tập trung vào phương pháp đã triển khai, dữ liệu và kết quả thực tế, lỗi còn tồn tại và kế hoạch đến ngày 20/12. Trang bìa giữ hình minh họa 21 điểm bàn tay trong file hiện tại của người dùng. Tên đề tài được diễn đạt theo phạm vi chức năng trong mã nguồn; đối chiếu với tên đã đăng ký trên LMS nếu có khác biệt.

## Slide 2. Bài toán, mục tiêu và phạm vi

Bài toán là nhận diện bốn hướng cử chỉ và phân biệt trạng thái nền trước khi phát lệnh điều khiển. Trong mã nguồn, cử chỉ trái/phải tương ứng phím mũi tên; lên/xuống tương ứng cuộn trang. Phạm vi nguyên mẫu hiện tại dùng webcam RGB, một bàn tay hợp lệ, mô hình CPU. Bộ nhận diện có thể phát hiện tối đa hai bàn tay để loại trường hợp nhiều tay; ứng dụng chỉ chấp nhận đúng một bàn tay. Mục tiêu đánh giá gồm độ đúng trên clip và độ ổn định khi điều khiển liên tục. Độ đúng clip đã có; độ ổn định trực tiếp cần đo thêm. Chưa có dữ liệu thực nghiệm về người dùng chưa xuất hiện trong dữ liệu.

## Slide 3. Nghiên cứu liên quan

Ba công trình đã được đọc từ PDF gốc trong reference và đối chiếu thông tin xuất bản. IPN HandS là hướng gần nhất: bộ dữ liệu có 14 cử chỉ và 50 người; LSTM 3 tầng 256 nút ẩn trên 42 tọa độ xy. Kết quả được lấy đúng từ Bảng 6: accuracy 91,2 ± 1,4%, average recall 78,0 ± 1,2% qua ba lần chạy; không dùng con số diễn giải dễ gây nhầm trong abstract. Ưu điểm là chú trọng chất lượng và sửa landmark; cấu hình và dữ liệu lớn hơn đồ án nên không so sánh trực tiếp.

SKETCH biểu diễn chuyển động skeleton thành ảnh đồ thị rồi dùng ViT/Swin. Bảng 1, SHREC 2019, Swin-L + Augmentation có detection rate 0,93 và false positive 0,01. DR không phải accuracy. Tác giả nêu hạn chế các cửa sổ xử lý độc lập chưa tận dụng đầy đủ ngữ cảnh trước đó.

ConvMixFormer thay attention bằng bộ trộn tích chập và dùng gated feed-forward. RGB accuracy trong Bảng 1 là 76,04% trên NVGesture và 98,26% trên Briareo; mô hình 13,57 triệu tham số trong Bảng 6. Đây là bài toán và đầu vào khác với landmark + LSTM của đồ án. Điểm học hỏi là báo cáo chi phí tính toán cùng độ chính xác. Các DOI và URL đầy đủ có trong references.md và phần ghi chú này.

Tài liệu tham khảo:
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, “IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition,” Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. DOI: 10.3390/app15116321. https://www.mdpi.com/2076-3417/15/11/6321
Vị trí bằng chứng: Bảng 1, trang 4; mục 5.1–5.2, trang 13–14; Bảng 6, trang 15.

[2] S. H. Han et al., “Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition,” Advances in Neural Information Processing Systems, vol. 38, NeurIPS, 2025. DOI: 10.52202/085713-4682. https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html
Vị trí bằng chứng: Bảng 1, trang 8; Bảng 2, trang 9; hạn chế tại mục 5.1, trang 10.

[3] M. Garg, D. Ghosh, and P. M. Pradhan, “ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition,” Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pp. 6156–6166, 2025. https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html
Vị trí bằng chứng: Bảng 1, trang PDF 5; mục 4.1–4.3, trang PDF 5–6; Bảng 6, trang PDF 8.

## Slide 4. Đọc sâu IPN HandS và đối chiếu code

Theo góp ý của GVHD ở tuần 2, phần này trả lời cụ thể bài nào làm trước và mình hiểu được gì. IPN HandS công bố trên Applied Sciences năm 2025, DOI 10.3390/app15116321, bốn tác giả được ghi trên slide. Bài nghiên cứu tác động của chất lượng gán nhãn landmark và biên thời gian lên nhận diện cử chỉ; LSTM là mô hình cơ sở để so sánh ba nguồn annotation. Cần hiểu công cụ/dữ liệu đã sửa nhãn và cách đánh giá cùng với mạng LSTM.

Mục 5.1: mỗi bước gồm 42 tọa độ xy của 21 điểm; ba tầng LSTM 256, dropout 0,3; trạng thái cuối qua lớp phân loại 14 cử chỉ. Mục 5.2: 50 người, 37 train/13 test; tối đa 64 frame, stride 32 cho chuỗi dài; không padding/nội suy chuỗi ngắn. Đo phân loại 14 lớp có chủ đích, bỏ đoạn nền. Huấn luyện 30 epoch, batch 64, Adam 0,001, lặp ba lần. Bảng 6: accuracy 91,2 ± 1,4%, average recall 78,0 ± 1,2%. Bài có mất cân bằng lớp; bộ 250 clip của đồ án hiện cân bằng.

Đồ án dùng 44 đặc trưng, chuỗi 30 mẫu tại 20 Hz, LSTM một tầng 64 và năm nhãn gồm nền. Cấu hình và giao thức khác nhau; chưa đủ để nói đã tái lập bài báo hoặc cải tiến tốt hơn.

Đã kiểm tra nguồn tác giả: https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md mô tả dữ liệu HandS; model.py ở nhánh được xem thuộc benchmark CNN của IPN Hand trước đó. Chưa xác minh được đường chạy LSTM tương ứng bài 2025 và chưa chạy thí nghiệm gốc. Không trình bày chạy code đồ án thành chạy code tác giả.

Khoảng trống của nguyên mẫu vẫn là lỗi lên/xuống, đo điều khiển trực tiếp, FPS và độ trễ. Trước khi mở rộng, cần nắm phương pháp và giải thích luồng code hiện có.

Tài liệu tham khảo:
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, “IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition,” Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. DOI: 10.3390/app15116321. https://www.mdpi.com/2076-3417/15/11/6321
Vị trí bằng chứng: Bảng 1, trang 4; mục 5.1–5.2, trang 13–14; Bảng 6, trang 15.

## Slide 5. Kiến trúc tổng thể

Webcam cung cấp ảnh RGB kích thước cấu hình 640×480 và lật gương đúng một lần. MediaPipe Hand Landmarker chạy VIDEO, trả 21 điểm mỗi bàn tay; cấu hình num_hands=2 nhằm nhận biết trường hợp có nhiều tay, nhưng hệ thống chỉ chấp nhận đúng một tay. features.py chuẩn hóa tọa độ theo cổ tay và kích thước lòng bàn tay, rồi nối vị trí cổ tay thành 44 đặc trưng. Bộ đệm tạo chuỗi 30 mẫu ở nhịp 20 Hz. LSTM trả logits của năm nhãn. Bộ điều khiển dùng ngưỡng 0,8, thời gian ổn định tối thiểu 150 ms và tối thiểu ba dự đoán mới; cooldown 1.000 ms, xác nhận nền 300 ms. F8 bật hoặc tạm dừng, F9 dừng toàn cục. Các điều kiện này đã có trong mã nguồn và test tự động; chưa thể xem là kết quả thử thành công trong môi trường thực tế.

Tài liệu tham khảo:
[4] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020. DOI: 10.48550/arXiv.2006.10214. https://arxiv.org/abs/2006.10214
Vị trí bằng chứng: Tác giả, tiêu đề, năm và mô tả bộ phát hiện lòng bàn tay kết hợp mô hình landmark trên arXiv.

[5] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997. DOI: 10.1162/neco.1997.9.8.1735. https://pubmed.ncbi.nlm.nih.gov/9377276/
Vị trí bằng chứng: Thông tin thư mục và tóm tắt của công trình gốc.

[6] PyTorch Contributors, “torch.nn.LSTM,” Official PyTorch documentation, version 2.15, 2026. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html
Vị trí bằng chứng: Mô tả đầu vào, đầu ra và tham số LSTM. Môi trường hiện cài torch 2.15.0+cpu.

[7] Google AI Edge, “Hand Landmarker,” Official MediaPipe documentation, 2026. https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python
Vị trí bằng chứng: 21 điểm bàn tay, các chế độ xử lý và đầu vào video có timestamp.

## Slide 6. Pipeline thu thập và tiền xử lý

Ba ảnh là các khung tại 150, 750 và 1.250 ms của một clip train nhãn SWIPE_LEFT, được trích từ video thật, không tạo ảnh giả. Với ảnh W×H, trước hết q = p×[W,H]/max(W,H). Lấy cổ tay q0 làm gốc và scale bằng trung vị khoảng cách từ q0 tới các mốc 5,9,13,17. Đặc trưng cục bộ là (q−q0)/scale, gồm 42 giá trị xy; nối thêm q0 gồm hai giá trị để giữ chuyển động tuyệt đối của cổ tay. SequenceBuffer lấy mẫu theo timestamp mỗi 50 ms và chỉ nội suy khi đã biết cả hai đầu mút. Mất tay, nhiều tay hoặc khoảng trống lớn hơn 100 ms sẽ xóa chuỗi. Từ mẫu đầu tới mẫu cuối là 29/20=1,45 giây, xấp xỉ cửa sổ 1,5 giây. Cấu hình 20 Hz không phải kết quả đo FPS. Video gốc, NPZ, manifest và thông tin phiên cho phép kiểm tra lại nhãn.

## Slide 7. Dữ liệu và phân chia

Tất cả 250 clip có tệp tương ứng và chuỗi đúng kích thước. Mỗi lớp có 50 clip: 30 train, 10 validation và 10 test. Tổng train150, validation50, test50, tỷ lệ 60/20/20. Train thuộc pilot_01 và train_02; validation là val_01; test là test_01. Kiểm tra băm nội dung feature không thấy chuỗi giống tuyệt đối xuyên tập; kết quả này không chứng minh các mẫu độc lập theo người dùng. Manifest không có subject_id để chứng minh giao thức giữ người riêng. Các phiên thu riêng giúp kiểm soát nguồn mẫu, nhưng không được gọi là thử trên người chưa thấy. Phân bố hiện tại cân bằng, vì vậy không nêu mất cân bằng lớp như một lỗi đã xảy ra.

## Slide 8. Đọc code và giải thích một lượt suy luận

Đọc theo đường đi dữ liệu. features.py:extract_features nhận 21 điểm xy, đổi về cùng đơn vị, trừ cổ tay và chia kích thước lòng bàn tay. 42 giá trị cục bộ nối hai tọa độ cổ tay thành 44. SequenceBuffer.push nhận vector và timestamp; lấy mẫu 20 Hz thành 30 bước, xóa chuỗi khi mất tay hoặc khoảng hở quá 100 ms.

Trong model.py, GestureLSTM.forward gọi sequence,_=self.lstm(features). Đầu vào [B,30,44] tạo sequence [B,30,64]. Dòng sequence[:, -1, :] lấy trạng thái ở thời điểm cuối cho mỗi mẫu, được [B,64]; đây không phải nhãn cuối hoặc frame cuối của video gốc. Linear 64→5 tạo logits cho năm nhãn. predict_gesture thêm chiều batch, chạy model, softmax rồi lấy nhãn/mức tin cậy cao nhất. MediaPipe tìm điểm bàn tay; LSTM trong đồ án phân loại cử chỉ.

Đã chạy riêng một clip test đã lưu: input [1,30,44] → LSTM output [1,30,64] → last state [1,64] → logits [1,5]. Nhãn thật/dự đoán đều BACKGROUND; confidence khoảng 0,99244. Đường gọi từng bước và model(x) cho cùng kết quả. Đây là minh chứng luồng thực thi của một clip trong code đồ án, không phải số liệu tái lập IPN HandS. Chạy lại bằng trace_current_model.py; kết quả model_execution_trace.json.

Đọc tiếp training.py:train_model theo thứ tự load_split, DataLoader, forward, CrossEntropyLoss, backward, Adam.step, validation, lưu checkpoint khi val_loss giảm. Cấu hình: 44 chiều, hidden 64, một tầng, năm nhãn, 28.485 tham số; batch 16, Adam 0,001, seed 42, 30 epoch, CPU. Checkpoint epoch 23 được chọn bằng validation loss. Chưa có thí nghiệm chứng minh cấu hình tối ưu. Môi trường Python 3.11.0, torch 2.15.0+cpu, MediaPipe 0.10.35, OpenCV 4.14.0.94.

Tài liệu tham khảo:
[5] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997. DOI: 10.1162/neco.1997.9.8.1735. https://pubmed.ncbi.nlm.nih.gov/9377276/
Vị trí bằng chứng: Thông tin thư mục và tóm tắt của công trình gốc.

[6] PyTorch Contributors, “torch.nn.LSTM,” Official PyTorch documentation, version 2.15, 2026. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html
Vị trí bằng chứng: Mô tả đầu vào, đầu ra và tham số LSTM. Môi trường hiện cài torch 2.15.0+cpu.

## Slide 9. Đường cong huấn luyện

Đồ thị lấy toàn bộ 30 epoch từ stdout lưu trong notebook, không tạo dữ liệu giả và không nối từ hai lần chạy khác nhau. Train loss từ1,5541 xuống0,1293; validation loss từ1,4313 xuống0,1720 ở epoch30. Checkpoint tốt nhất là epoch23 với validation loss đầy đủ0,1085219458 và accuracy0,94. Các giá trị trên đường cong có độ chính xác bốn chữ số thập phân theo log. Validation có dao động; chỉ từ một lần chạy và độ chênh validation/test không đủ kết luận nguyên nhân duy nhất là overfitting. Notebook ghi5,0giây cho một lần huấn luyện; đây không phải latency suy luận hoặc benchmark nhiều lần. Bước sau là cố định giao thức rồi so sánh nhiều seed nếu còn thời gian.

## Slide 10. Kết quả đánh giá

Tôi đã nạp checkpoint hiện tại và chạy lại 50 chuỗi test trong bộ nhớ; accuracy, confusion matrix và các chỉ số khớp tệp outputs/evaluation.json. Accuracy40/50=80%. Macro-Precision và Macro-Recall đều0,8; Macro-F1 là0,7619047619. Macro-F1 là trung bình F1 từng lớp, không phải F1 tính trực tiếp từ macroP và macroR. BACKGROUND,LEFT,RIGHT đều đúng10/10 trong bộ nhỏ hiện tại; không suy rộng thành hoàn hảo trong sử dụng thực tế. UP cóP0,5,R0,1,F1≈0,1667; DOWN cóP0,5,R0,9,F1≈0,6429. Mỗi lớp support10 nên một clip tương ứng10 điểm phần trăm recall của lớp. Kết quả phản ánh thử trên clip đã lưu, chưa phản ánh đầy đủ điều khiển liên tục.

## Slide 11. Confusion matrix và mẫu lỗi

Ma trận có hàng là nhãn thật, cột là nhãn dự đoán, đơn vị là clip. Ba lớp đầu mỗi lớp10/10 đúng. Trong10clip UP chỉ1đúng,9bị nhận DOWN. Trong10clip DOWN có9đúng,1bị nhận UP. Ảnh bên phải trích từ test/SWIPE_UP/test_01_3bd55bb323444226a3d8c37cdf1a2f92.avi; dự đoán toàn chuỗi là DOWN với độ tin cậy khoảng0,965. Dự đoán sai có độ tin cậy cao cho thấy chỉ tăng ngưỡng không nhất thiết sửa được lỗi này. Quan sát một số video cho thấy tư thế ngón tay khác nhau theo nhãn trong khi mô tả cử chỉ yêu cầu vuốt lòng bàn tay mở. Đây là dấu hiệu cần đối chiếu quy cách và phân tích thêm, chưa chứng minh nguyên nhân mô hình học tư thế thay vì chuyển động.

## Slide 12. Demo và giới hạn kiểm thử

Bấm video trong chế độ Slide Show. Video dài10giây, phát lại5clip test đã lưu và dự đoán từ checkpoint, có một clip UP nhận sai DOWN để thể hiện giới hạn hiện tại. Đây không phải bản ghi webcam đang điều khiển ứng dụng khác. Bản PDF chỉ hiển thị ảnh bìa của video; fileMP4 được cung cấp trong slide_sources/assets. Bộ60test tự động đã chạy qua trong15,998giây; test sử dụng dữ liệu/mô phỏng cho các ranh giới phần cứng và điều khiển, chưa thay thế phép thử trực tiếp. Chưa có dữ liệu thực nghiệm cho40lượt cử chỉ,5phút nền, latency suy luận ổn định và FPS toàn hệ thống. Cần10lượt mỗi hướng, ghi đúng/sai/bỏ sót/lặp và timestamp từ động tác tới lệnh. Đo idle5phút để đếm lệnh không mong muốn; báo cáo điều kiện ánh sáng, khoảng cách, phần cứng và cấu hình.

## Slide 13. Bảng tiến độ

Bảng tiến độ ghi theo hiện trạng kiểm chứng được ngày07/11. Dữ liệu và mô hình đã vượt giai đoạn chỉ cài webcam: đã có250clip, train, checkpoint, kết quả test và ứng dụng điều khiển. Tuy nhiên cần phân biệt có mã nguồn với kết quả đo trực tiếp. Mô tả cũ trong một số README/ROADMAP còn ghi train/run/control chưa hoàn thành; báo cáo này dựa trên mã và artifact thực tế. Không đưa phần trăm hoàn thành vì chưa có tiêu chí và trọng số thống nhất.

Bảng chi tiết:
Nghiên cứu tài liệu | Đã có tài liệu và đối chiếu | 6 PDF trong reference; phân tích sâu [1]–[3] | Chưa tái lập benchmark công khai
Thu thập dữ liệu | Đã có 250 clip | manifest, video và NPZ; 150/50/50 clip | Cần thống nhất lại quy cách động tác
Tiền xử lý | Đã triển khai và kiểm tra | features.py, SequenceBuffer, dataset-check | Chưa đo ảnh hưởng của từng đặc trưng
Xây dựng mô hình | Đã triển khai | GestureLSTM, 1 tầng, 64 nút ẩn, 5 lớp | Chưa có mô hình đối chứng
Huấn luyện | Đã có log 30 epoch | notebook, checkpoint epoch 23 | Chưa có thống kê nhiều seed
Đánh giá clip | Đã đo trên 50 clip test | 40/50 đúng, Macro-F1 0,7619 | Vuốt lên chỉ đúng 1/10
Tích hợp hệ thống | Đã có mã nguồn | app.py, control.py, F8/F9 và bộ xác nhận | Chưa có đo lường thao tác trực tiếp
Kiểm thử thực tế | Còn thiếu phép thử có ghi nhận | 60 test tự động qua; video phát lại clip | Chưa có dữ liệu thực nghiệm cho 40 lượt và 5 phút nền

## Slide 14. Khó khăn và biện pháp

Vấn đề đã đo được là lỗi lên/xuống và chênh14điểm phần trăm giữa validation94% và test80%. Quan sát tư thế ngón tay khác nhau chỉ là dấu hiệu dữ liệu cần xem xét, chưa chứng minh nguyên nhân. Cần chốt định nghĩa cử chỉ với GVHD, kiểm tra nhãn và cách thu rồi bổ sung dữ liệu đúng quy cách. Do đã xem nhiều lần tập test hiện tại, tập này chỉ nên xem là bộ chẩn đoán phát triển; trước đánh giá cuối nên thu một phiên giữ riêng sau khi khóa cấu hình.

Chưa có dữ liệu thực nghiệm về độ trễ, FPS, điều khiển40lượt,5phút tay nghỉ và người chưa thấy. Không khẳng định CPU yếu, overfitting hoặc hệ thống thời gian thực ổn định khi chưa đo. Phương án đo là ghi thời gian từng khối, số frame xử lý trên thời gian tường, thời gian từ cử chỉ tới lệnh, số đúng/sai/bỏ sót/lặp và false command trên5phút. Nếu nhầm nhiều, ưu tiên sửa quy cách/dữ liệu trước khi tăng độ phức tạp mô hình.

## Slide 15. Kế hoạch sáu tuần còn lại

Buổi báo cáo hiện tại ở cuối tuần4, nên phần còn lại là tuần5–10. Không lặp lại kế hoạch bảy tuần dành cho thời điểm cuối tuần3. Kế hoạch ưu tiên giải quyết lỗi lớp dọc, đo sử dụng trực tiếp, sửa ổn định rồi mới khóa đánh giá và hoàn thiện hồ sơ. Các mốc sau là kế hoạch, không phải kết quả đã đạt.

Tuần 5 (09–15/11/2026)
Mục tiêu: Đọc sâu bài báo, giải thích code và xử lý lỗi lên/xuống
Công việc: Đọc mục 5.1–5.3 của IPN HandS; đối chiếu features/model/training; chạy trace một clip; chốt cử chỉ với GVHD và phân tích lỗi trước khi thu bù.
Đầu ra: Phiếu đọc bài báo, sơ đồ luồng code, trace một clip, quy cách cử chỉ và phân tích lỗi lên/xuống.
Nghiệm thu: Chỉ được bài gốc và các hàm tương ứng; giải thích 44/30/64/5; phân biệt code đồ án với code tác giả; mọi sửa dữ liệu/mô hình chọn bằng validation.
Rủi ro: Cách làm cử chỉ thay đổi khiến dữ liệu cũ không còn phù hợp.
Dự phòng: Chốt năm nhãn và một điều kiện quay trước, thu lại nhóm mẫu bị ảnh hưởng.

Tuần 6 (16–22/11/2026)
Mục tiêu: Đo nhận diện và điều khiển trực tiếp
Công việc: Thử 10 lượt mỗi hướng; 5 phút tay nghỉ; đo FPS và thời gian từ cử chỉ tới lệnh.
Đầu ra: CSV 40 lượt, log 5 phút nền, cấu hình ngưỡng và cách đo thời gian.
Nghiệm thu: Ghi đúng/sai/bỏ sót/lặp cho đủ 40 lượt; đủ 5 phút; F8/F9 hoạt động khi ứng dụng đích có focus.
Rủi ro: Nhận nhầm hoặc phát nhiều lệnh cho một động tác.
Dự phòng: Điều chỉnh bằng dữ liệu phát triển, tăng thời gian nghỉ và giữ bộ thử cuối sau khi khóa cấu hình.

Tuần 7 (23–29/11/2026)
Mục tiêu: Sửa lỗi điều khiển và thử tình huống lỗi
Công việc: Thử mất tay, hai tay, bật lại, camera lỗi; sửa theo lỗi quan sát được.
Đầu ra: Checklist có kết quả và phiên bản chạy demo.
Nghiệm thu: Mỗi lần vuốt tạo tối đa một lệnh; mất tay không phát lệnh; dừng toàn cục hoạt động.
Rủi ro: Tốc độ xử lý thấp hoặc chuỗi bị ngắt nhiều.
Dự phòng: Đo từng phần, điều chỉnh nhịp lấy mẫu đồng nhất giữa train và runtime rồi thử lại.

Tuần 8 (30/11–06/12/2026)
Mục tiêu: Đánh giá cuối và khóa cấu hình
Công việc: Chốt mô hình/ngưỡng; đánh giá trên tập giữ lại; tổng hợp metric và lỗi.
Đầu ra: Checkpoint cuối, confusion matrix, bảng thao tác trực tiếp và video demo.
Nghiệm thu: Có tệp kết quả, mã phiên và điều kiện thử đủ để kiểm tra lại.
Rủi ro: Test đã được xem nhiều lần trong quá trình phát triển.
Dự phòng: Thu một phiên test mới sau khi chốt quy cách và cấu hình, báo rõ giao thức mới.

Tuần 9 (07–13/12/2026)
Mục tiêu: Hoàn thiện bản báo cáo và nhận góp ý
Công việc: Viết phương pháp/kết quả/hạn chế; hoàn thiện slide; gửi GVHD và hẹn ký phiếu.
Đầu ra: Báo cáo đầy đủ, slide, video và nhật ký các tuần.
Nghiệm thu: Số liệu khớp tệp gốc; trích dẫn có nguồn; GVHD nhận được bản xem trước.
Rủi ro: Thiếu số liệu hoặc chậm nhận phản hồi.
Dự phòng: Gửi bản đủ nội dung sớm, đánh dấu rõ mục còn chờ góp ý.

Tuần 10 (14–20/12/2026)
Mục tiêu: Sửa góp ý và chuẩn bị nộp
Công việc: Sửa báo cáo, chạy demo trên máy bảo vệ, lấy chữ ký GVHD, scan phiếu và sao lưu.
Đầu ra: Bộ hồ sơ sẵn sàng nộp LMS từ 21–27/12.
Nghiệm thu: Mở được mọi tệp; bản scan rõ chữ ký; demo chạy được; kiểm tra yêu cầu LMS.
Rủi ro: Lỗi môi trường sát hạn hoặc thiếu chữ ký.
Dự phòng: Giữ môi trường đã chạy và video dự phòng, hẹn GVHD trước tuần cuối.

Học phần kết thúc giai đoạn thực hiện20/12. Nộp báo cáo LMS21–27/12, kèm scan phiếu tiến độ có chữ ký GVHD; cần gặp GVHD ký bảng điểm. Chưa biết giờ đóng LMS và lịch bảo vệ cá nhân. Khung chấm/bảo vệ28/12/2026–10/01/2027.

## Slide 16. Kết luận và tài liệu tham khảo

Theo góp ý tuần 2, thứ tự ưu tiên là đọc hiểu bài báo, giải thích được code và phép thử hiện có, rồi mới mở rộng. Chưa có minh chứng tái lập mã LSTM của bài báo. Kết quả đạt được là một pipeline có mã nguồn từ webcam tới bộ phát lệnh,250clip hợp lệ, mô hình LSTM có checkpoint, log30epoch và đánh giá trên50clip cho accuracy80%, Macro-F1≈0,7619. Bộ60test tự động đã qua. Phần chưa đáp ứng đủ mục tiêu là phân biệt lên/xuống và bằng chứng đo điều khiển trực tiếp. Vì vậy, ưu tiên tiếp theo là thống nhất quy cách động tác, sửa lỗi dữ liệu/mô hình theo validation rồi đo40lượt,5phút nền và tốc độ. Em xin ý kiến GVHD về quy cách cử chỉ và tiêu chí nghiệm thu của nguyên mẫu. Các nghiên cứu là cơ sở lựa chọn và đánh giá, chưa dùng để khẳng định kiến trúc có tính mới.

Tài liệu tham khảo:
[1] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, “IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition,” Applied Sciences, vol. 15, no. 11, Art. 6321, 2025. DOI: 10.3390/app15116321. https://www.mdpi.com/2076-3417/15/11/6321
Vị trí bằng chứng: Bảng 1, trang 4; mục 5.1–5.2, trang 13–14; Bảng 6, trang 15.

[2] S. H. Han et al., “Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition,” Advances in Neural Information Processing Systems, vol. 38, NeurIPS, 2025. DOI: 10.52202/085713-4682. https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html
Vị trí bằng chứng: Bảng 1, trang 8; Bảng 2, trang 9; hạn chế tại mục 5.1, trang 10.

[3] M. Garg, D. Ghosh, and P. M. Pradhan, “ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition,” Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pp. 6156–6166, 2025. https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html
Vị trí bằng chứng: Bảng 1, trang PDF 5; mục 4.1–4.3, trang PDF 5–6; Bảng 6, trang PDF 8.

[4] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020. DOI: 10.48550/arXiv.2006.10214. https://arxiv.org/abs/2006.10214
Vị trí bằng chứng: Tác giả, tiêu đề, năm và mô tả bộ phát hiện lòng bàn tay kết hợp mô hình landmark trên arXiv.

[5] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997. DOI: 10.1162/neco.1997.9.8.1735. https://pubmed.ncbi.nlm.nih.gov/9377276/
Vị trí bằng chứng: Thông tin thư mục và tóm tắt của công trình gốc.

[6] PyTorch Contributors, “torch.nn.LSTM,” Official PyTorch documentation, version 2.15, 2026. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html
Vị trí bằng chứng: Mô tả đầu vào, đầu ra và tham số LSTM. Môi trường hiện cài torch 2.15.0+cpu.

[7] Google AI Edge, “Hand Landmarker,” Official MediaPipe documentation, 2026. https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python
Vị trí bằng chứng: 21 điểm bàn tay, các chế độ xử lý và đầu vào video có timestamp.
