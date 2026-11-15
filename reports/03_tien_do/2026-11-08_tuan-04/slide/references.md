# Tài liệu tham khảo

Ngày đối chiếu 07/11/2026. Đánh số thống nhất với báo cáo và slide.

## [1] IPN HandS

G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi, “IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition,” *Applied Sciences, vol. 15, no. 11, Art. 6321*, 2025.

[Nguồn gốc](https://www.mdpi.com/2076-3417/15/11/6321). DOI [10.3390/app15116321](https://doi.org/10.3390/app15116321).

Minh chứng dùng trong báo cáo. Bảng 1, trang 4; mục 5.1–5.2, trang 13–14; Bảng 6, trang 15.

Bản PDF được cung cấp trong project tại `reference/06_IPN_HandS_Applied_Sciences_2025/06_IPN_HandS_Applied_Sciences_2025.pdf`.

## [2] SKETCH

S. H. Han et al., “Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition,” *Advances in Neural Information Processing Systems, vol. 38, NeurIPS*, 2025.

[Nguồn gốc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html). DOI [10.52202/085713-4682](https://doi.org/10.52202/085713-4682).

Minh chứng dùng trong báo cáo. Bảng 1, trang 8; Bảng 2, trang 9; hạn chế tại mục 5.1, trang 10.

Bản PDF được cung cấp trong project tại `reference/02_SKETCH_NeurIPS_2025/02_SKETCH_Doodle_to_Detect_NeurIPS_2025.pdf`.

## [3] ConvMixFormer

M. Garg, D. Ghosh, and P. M. Pradhan, “ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition,” *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pp. 6156–6166*, 2025.

[Nguồn gốc](https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html).

Minh chứng dùng trong báo cáo. Bảng 1, trang PDF 5; mục 4.1–4.3, trang PDF 5–6; Bảng 6, trang PDF 8.

Bản PDF được cung cấp trong project tại `reference/04_ConvMixFormer_WACV_2025/04_ConvMixFormer_WACV_2025.pdf`.

## [4] MediaPipe Hands

F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” *arXiv:2006.10214*, 2020.

[Nguồn gốc](https://arxiv.org/abs/2006.10214). DOI [10.48550/arXiv.2006.10214](https://doi.org/10.48550/arXiv.2006.10214).

Minh chứng dùng trong báo cáo. Tác giả, tiêu đề, năm và mô tả bộ phát hiện lòng bàn tay kết hợp mô hình landmark trên arXiv.

## [5] LSTM

S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” *Neural Computation, vol. 9, no. 8, pp. 1735–1780*, 1997.

[Nguồn gốc](https://pubmed.ncbi.nlm.nih.gov/9377276/). DOI [10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735).

Minh chứng dùng trong báo cáo. Thông tin thư mục và tóm tắt của công trình gốc.

## [6] PyTorch LSTM

PyTorch Contributors, “torch.nn.LSTM,” *Official PyTorch documentation, version 2.15*, 2026.

[Nguồn gốc](https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html).

Minh chứng dùng trong báo cáo. Mô tả đầu vào, đầu ra và tham số LSTM. Môi trường hiện cài torch 2.15.0+cpu.

## [7] Hand Landmarker

Google AI Edge, “Hand Landmarker,” *Official MediaPipe documentation*, 2026.

[Nguồn gốc](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python).

Minh chứng dùng trong báo cáo. 21 điểm bàn tay, các chế độ xử lý và đầu vào video có timestamp.

## Đối chiếu số liệu từ các bài đã cung cấp

| Nguồn | Dữ liệu và giao thức | Kết quả sử dụng | Vị trí |
|---|---|---|---|
| [1] IPN HandS | 50 người, 14 lớp, 5.177 mẫu; chia 37/13 người train/test | Accuracy 91,2 ± 1,4%; average recall 78,0 ± 1,2%; ba lần chạy | Bảng 1 và 6 |
| [2] SKETCH | SHREC’19; cấu hình Swin-L có tăng cường dữ liệu | Detection rate 0,93; false positive 0,01 | Bảng 1, trang 8 |
| [3] ConvMixFormer | RGB đơn phương thức; NVGesture và Briareo | Accuracy tương ứng 76,04% và 98,26%; mô hình 13,57 triệu tham số | Bảng 1 và 6 |

Các kết quả trên dùng dữ liệu và giao thức riêng. Chúng phục vụ phân tích phương pháp. Báo cáo chỉ đo mô hình đồ án trên bộ 50 clip test tự thu.

Ba PDF chính được người dùng cung cấp. Đã xem ảnh render của các bảng kết quả. Trang NeurIPS xác nhận thông tin công bố và DOI. Chỉ mục CVF xác nhận tiêu đề, tác giả và trang hội nghị. Truy cập trực tiếp CVF/MDPI có lúc trả 403/429, được ghi trong qa_report.md.

## Phạm vi tài liệu khác trong thư mục reference

Đã trích xuất văn bản của S2Gest, GESTRO và bài tổng quan Continuous Hand Gesture Recognition để khảo sát. Ba công trình [1]–[3] là nhóm được dùng phân tích sâu trong báo cáo này vì có liên hệ trực tiếp với landmark, chất lượng dữ liệu và nhận diện chuỗi.

## Nguồn nội bộ

- `data/manifest.csv`, `data/sessions/`, video AVI và NPZ đi kèm.
- `notebook/hand_tracking.ipynb`, output huấn luyện 30 epoch và đánh giá đã lưu.
- `models/gesture_lstm.pt`, `models/notebook/gesture_lstm.pt`.
- `outputs/evaluation.json`, `outputs/notebook/evaluation.json`.
- `src/hand_tracking/` và bộ test hiện có.
- Đặc tả 1.1 trong `reports/01_tai_lieu_de_tai/` và thông báo lịch học kỳ do người dùng cung cấp.

## Mã nguồn và dữ liệu tác giả được kiểm tra thêm

[README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) mô tả dữ liệu công bố; [model.py](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) được xem thuộc benchmark CNN của IPN Hand. Chưa xác minh đường chạy LSTM tương ứng thí nghiệm 2025; chưa có kết quả tái lập mã tác giả.
