from pathlib import Path
import json

SOURCES = Path(__file__).resolve().parent
OUTPUT = SOURCES.parent
M = json.loads((SOURCES / 'verified_metrics.json').read_text(encoding='utf-8'))

references = [
    {'id': 1, 'short': 'IPN HandS', 'authors': 'G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and H. Takahashi',
     'title': 'IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition',
     'venue': 'Applied Sciences, vol. 15, no. 11, Art. 6321', 'year': 2025,
     'doi': '10.3390/app15116321', 'url': 'https://www.mdpi.com/2076-3417/15/11/6321',
     'local': 'reference/06_IPN_HandS_Applied_Sciences_2025/06_IPN_HandS_Applied_Sciences_2025.pdf',
     'evidence': 'Bảng 1, trang 4; mục 5.1–5.2, trang 13–14; Bảng 6, trang 15.'},
    {'id': 2, 'short': 'SKETCH', 'authors': 'S. H. Han et al.',
     'title': 'Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition',
     'venue': 'Advances in Neural Information Processing Systems, vol. 38, NeurIPS', 'year': 2025,
     'doi': '10.52202/085713-4682',
     'url': 'https://proceedings.neurips.cc/paper_files/paper/2025/hash/ccf308ecd36579d82532851419c283cd-Abstract-Conference.html',
     'local': 'reference/02_SKETCH_NeurIPS_2025/02_SKETCH_Doodle_to_Detect_NeurIPS_2025.pdf',
     'evidence': 'Bảng 1, trang 8; Bảng 2, trang 9; hạn chế tại mục 5.1, trang 10.'},
    {'id': 3, 'short': 'ConvMixFormer', 'authors': 'M. Garg, D. Ghosh, and P. M. Pradhan',
     'title': 'ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition',
     'venue': 'Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pp. 6156–6166',
     'year': 2025, 'doi': None,
     'url': 'https://openaccess.thecvf.com/content/WACV2025/html/Garg_ConvMixFormer-_A_Resource-Efficient_Convolution_Mixer_for_Transformer-Based_Dynamic_Hand_Gesture_WACV_2025_paper.html',
     'local': 'reference/04_ConvMixFormer_WACV_2025/04_ConvMixFormer_WACV_2025.pdf',
     'evidence': 'Bảng 1, trang PDF 5; mục 4.1–4.3, trang PDF 5–6; Bảng 6, trang PDF 8.'},
    {'id': 4, 'short': 'MediaPipe Hands', 'authors': 'F. Zhang et al.',
     'title': 'MediaPipe Hands: On-device Real-time Hand Tracking',
     'venue': 'arXiv:2006.10214', 'year': 2020, 'doi': '10.48550/arXiv.2006.10214',
     'url': 'https://arxiv.org/abs/2006.10214', 'local': None,
     'evidence': 'Tác giả, tiêu đề, năm và mô tả bộ phát hiện lòng bàn tay kết hợp mô hình landmark trên arXiv.'},
    {'id': 5, 'short': 'LSTM', 'authors': 'S. Hochreiter and J. Schmidhuber',
     'title': 'Long Short-Term Memory', 'venue': 'Neural Computation, vol. 9, no. 8, pp. 1735–1780',
     'year': 1997, 'doi': '10.1162/neco.1997.9.8.1735',
     'url': 'https://pubmed.ncbi.nlm.nih.gov/9377276/', 'local': None,
     'evidence': 'Thông tin thư mục và tóm tắt của công trình gốc.'},
    {'id': 6, 'short': 'PyTorch LSTM', 'authors': 'PyTorch Contributors',
     'title': 'torch.nn.LSTM', 'venue': 'Official PyTorch documentation, version 2.15',
     'year': 2026, 'doi': None, 'url': 'https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html',
     'local': None, 'evidence': 'Mô tả đầu vào, đầu ra và tham số LSTM. Môi trường hiện cài torch 2.15.0+cpu.'},
    {'id': 7, 'short': 'Hand Landmarker', 'authors': 'Google AI Edge',
     'title': 'Hand Landmarker', 'venue': 'Official MediaPipe documentation',
     'year': 2026, 'doi': None,
     'url': 'https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python',
     'local': None, 'evidence': '21 điểm bàn tay, các chế độ xử lý và đầu vào video có timestamp.'},
]

progress = [
    ['Nghiên cứu tài liệu', 'Đã có tài liệu và đối chiếu', '6 PDF trong reference; phân tích sâu [1]–[3]', 'Chưa tái lập benchmark công khai'],
    ['Thu thập dữ liệu', 'Đã có 250 clip', 'manifest, video và NPZ; 150/50/50 clip', 'Cần thống nhất lại quy cách động tác'],
    ['Tiền xử lý', 'Đã triển khai và kiểm tra', 'features.py, SequenceBuffer, dataset-check', 'Chưa đo ảnh hưởng của từng đặc trưng'],
    ['Xây dựng mô hình', 'Đã triển khai', 'GestureLSTM, 1 tầng, 64 nút ẩn, 5 lớp', 'Chưa có mô hình đối chứng'],
    ['Huấn luyện', 'Đã có log 30 epoch', 'notebook, checkpoint epoch 23', 'Chưa có thống kê nhiều seed'],
    ['Đánh giá clip', 'Đã đo trên 50 clip test', '40/50 đúng, Macro-F1 0,7619', 'Vuốt lên chỉ đúng 1/10'],
    ['Tích hợp hệ thống', 'Đã có mã nguồn', 'app.py, control.py, F8/F9 và bộ xác nhận', 'Chưa có đo lường thao tác trực tiếp'],
    ['Kiểm thử thực tế', 'Còn thiếu phép thử có ghi nhận', '60 test tự động qua; video phát lại clip', 'Chưa có dữ liệu thực nghiệm cho 40 lượt và 5 phút nền'],
]

plan = [
    {'week': 5, 'dates': '09–15/11', 'goal': 'Đọc sâu bài báo, giải thích code và xử lý lỗi lên/xuống',
     'work': 'Đọc mục 5.1–5.3 của IPN HandS; đối chiếu features/model/training; chạy trace một clip; chốt cử chỉ với GVHD và phân tích lỗi trước khi thu bù.',
     'output': 'Phiếu đọc bài báo, sơ đồ luồng code, trace một clip, quy cách cử chỉ và phân tích lỗi lên/xuống.',
     'acceptance': 'Chỉ được bài gốc và các hàm tương ứng; giải thích 44/30/64/5; phân biệt code đồ án với code tác giả; mọi sửa dữ liệu/mô hình chọn bằng validation.',
     'risk': 'Cách làm cử chỉ thay đổi khiến dữ liệu cũ không còn phù hợp.',
     'backup': 'Chốt năm nhãn và một điều kiện quay trước, thu lại nhóm mẫu bị ảnh hưởng.'},
    {'week': 6, 'dates': '16–22/11', 'goal': 'Đo nhận diện và điều khiển trực tiếp',
     'work': 'Thử 10 lượt mỗi hướng; 5 phút tay nghỉ; đo FPS và thời gian từ cử chỉ tới lệnh.',
     'output': 'CSV 40 lượt, log 5 phút nền, cấu hình ngưỡng và cách đo thời gian.',
     'acceptance': 'Ghi đúng/sai/bỏ sót/lặp cho đủ 40 lượt; đủ 5 phút; F8/F9 hoạt động khi ứng dụng đích có focus.',
     'risk': 'Nhận nhầm hoặc phát nhiều lệnh cho một động tác.',
     'backup': 'Điều chỉnh bằng dữ liệu phát triển, tăng thời gian nghỉ và giữ bộ thử cuối sau khi khóa cấu hình.'},
    {'week': 7, 'dates': '23–29/11', 'goal': 'Sửa lỗi điều khiển và thử tình huống lỗi',
     'work': 'Thử mất tay, hai tay, bật lại, camera lỗi; sửa theo lỗi quan sát được.',
     'output': 'Checklist có kết quả và phiên bản chạy demo.',
     'acceptance': 'Mỗi lần vuốt tạo tối đa một lệnh; mất tay không phát lệnh; dừng toàn cục hoạt động.',
     'risk': 'Tốc độ xử lý thấp hoặc chuỗi bị ngắt nhiều.',
     'backup': 'Đo từng phần, điều chỉnh nhịp lấy mẫu đồng nhất giữa train và runtime rồi thử lại.'},
    {'week': 8, 'dates': '30/11–06/12', 'goal': 'Đánh giá cuối và khóa cấu hình',
     'work': 'Chốt mô hình/ngưỡng; đánh giá trên tập giữ lại; tổng hợp metric và lỗi.',
     'output': 'Checkpoint cuối, confusion matrix, bảng thao tác trực tiếp và video demo.',
     'acceptance': 'Có tệp kết quả, mã phiên và điều kiện thử đủ để kiểm tra lại.',
     'risk': 'Test đã được xem nhiều lần trong quá trình phát triển.',
     'backup': 'Thu một phiên test mới sau khi chốt quy cách và cấu hình, báo rõ giao thức mới.'},
    {'week': 9, 'dates': '07–13/12', 'goal': 'Hoàn thiện bản báo cáo và nhận góp ý',
     'work': 'Viết phương pháp/kết quả/hạn chế; hoàn thiện slide; gửi GVHD và hẹn ký phiếu.',
     'output': 'Báo cáo đầy đủ, slide, video và nhật ký các tuần.',
     'acceptance': 'Số liệu khớp tệp gốc; trích dẫn có nguồn; GVHD nhận được bản xem trước.',
     'risk': 'Thiếu số liệu hoặc chậm nhận phản hồi.',
     'backup': 'Gửi bản đủ nội dung sớm, đánh dấu rõ mục còn chờ góp ý.'},
    {'week': 10, 'dates': '14–20/12', 'goal': 'Sửa góp ý và chuẩn bị nộp',
     'work': 'Sửa báo cáo, chạy demo trên máy bảo vệ, lấy chữ ký GVHD, scan phiếu và sao lưu.',
     'output': 'Bộ hồ sơ sẵn sàng nộp LMS từ 21–27/12.',
     'acceptance': 'Mở được mọi tệp; bản scan rõ chữ ký; demo chạy được; kiểm tra yêu cầu LMS.',
     'risk': 'Lỗi môi trường sát hạn hoặc thiếu chữ ký.',
     'backup': 'Giữ môi trường đã chạy và video dự phòng, hẹn GVHD trước tuần cuối.'},
]

content = {'references': references, 'progress': progress, 'plan': plan,
           'theme': {'name': 'Ocean Depths', 'primary': '1A2332', 'accent': '2D8B8B',
                     'secondary': 'A8DADC', 'light': 'F1FAEE', 'content_background': 'FFFFFF',
                     'font': 'Arial', 'font_reason': 'Font Office hỗ trợ tiếng Việt, đã kiểm tra trực tiếp bằng PowerPoint.'}}
(SOURCES / 'report_content.json').write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')

ref_lines = ['# Tài liệu tham khảo', '', 'Ngày đối chiếu 07/11/2026. Đánh số thống nhất với báo cáo và slide.', '']
for r in references:
    ref_lines += [f"## [{r['id']}] {r['short']}", '',
        f"{r['authors']}, “{r['title']},” *{r['venue']}*, {r['year']}.", '',
        f"[Nguồn gốc]({r['url']})" + (f". DOI [{r['doi']}](https://doi.org/{r['doi']})." if r['doi'] else '.'), '',
        f"Minh chứng dùng trong báo cáo. {r['evidence']}", '']
    if r['local']:
        ref_lines += [f"Bản PDF được cung cấp trong project tại `{r['local']}`.", '']
ref_lines += ['## Đối chiếu số liệu từ các bài đã cung cấp', '',
    '| Nguồn | Dữ liệu và giao thức | Kết quả sử dụng | Vị trí |',
    '|---|---|---|---|',
    '| [1] IPN HandS | 50 người, 14 lớp, 5.177 mẫu; chia 37/13 người train/test | Accuracy 91,2 ± 1,4%; average recall 78,0 ± 1,2%; ba lần chạy | Bảng 1 và 6 |',
    '| [2] SKETCH | SHREC’19; cấu hình Swin-L có tăng cường dữ liệu | Detection rate 0,93; false positive 0,01 | Bảng 1, trang 8 |',
    '| [3] ConvMixFormer | RGB đơn phương thức; NVGesture và Briareo | Accuracy tương ứng 76,04% và 98,26%; mô hình 13,57 triệu tham số | Bảng 1 và 6 |', '',
    'Các kết quả trên dùng dữ liệu và giao thức riêng. Chúng phục vụ phân tích phương pháp. Báo cáo chỉ đo mô hình đồ án trên bộ 50 clip test tự thu.', '',
    'Ba PDF chính được người dùng cung cấp. Đã xem ảnh render của các bảng kết quả. Trang NeurIPS xác nhận thông tin công bố và DOI. Chỉ mục CVF xác nhận tiêu đề, tác giả và trang hội nghị. Truy cập trực tiếp CVF/MDPI có lúc trả 403/429, được ghi trong qa_report.md.', '',
    '## Phạm vi tài liệu khác trong thư mục reference', '',
    'Đã trích xuất văn bản của S2Gest, GESTRO và bài tổng quan Continuous Hand Gesture Recognition để khảo sát. Ba công trình [1]–[3] là nhóm được dùng phân tích sâu trong báo cáo này vì có liên hệ trực tiếp với landmark, chất lượng dữ liệu và nhận diện chuỗi.', '',
    '## Nguồn nội bộ', '',
    '- `data/manifest.csv`, `data/sessions/`, video AVI và NPZ đi kèm.',
    '- `notebook/hand_tracking.ipynb`, output huấn luyện 30 epoch và đánh giá đã lưu.',
    '- `models/gesture_lstm.pt`, `models/notebook/gesture_lstm.pt`.',
    '- `outputs/evaluation.json`, `outputs/notebook/evaluation.json`.',
    '- `src/hand_tracking/` và bộ test hiện có.',
    '- Đặc tả 1.1 trong `reports/01_tai_lieu_de_tai/` và thông báo lịch học kỳ do người dùng cung cấp.', '']
ref_lines += ['## Mã nguồn và dữ liệu tác giả được kiểm tra thêm', '', '[README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) mô tả dữ liệu công bố; [model.py](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) được xem thuộc benchmark CNN của IPN Hand. Chưa xác minh đường chạy LSTM tương ứng thí nghiệm 2025; chưa có kết quả tái lập mã tác giả.', '']
(OUTPUT / 'references.md').write_text('\n'.join(ref_lines), encoding='utf-8')

metric_rows = '\n'.join(f"| {name} | {values['support']} | {values['precision']:.3f} | {values['recall']:.3f} | {values['f1']:.3f} |"
                         for name, values in M['test']['per_class'].items())
progress_rows = '\n'.join('| ' + ' | '.join(row) + ' |' for row in progress)
version_rows = '\n'.join(f"| {package} | {version or 'Chưa cài trong môi trường hiện tại'} |" for package, version in M['versions'].items())
plan_text = '\n\n'.join(f"### Tuần {item['week']} ({item['dates']}/2026)\n\n"
    f"**Mục tiêu**. {item['goal']}.\n\n**Công việc**. {item['work']}\n\n"
    f"**Sản phẩm đầu ra**. {item['output']}\n\n**Tiêu chí nghiệm thu**. {item['acceptance']}\n\n"
    f"**Rủi ro và dự phòng**. {item['risk']} {item['backup']}" for item in plan)

report = f'''# Báo cáo tiến độ nghiên cứu

## Nhận diện cử chỉ tay động và điều khiển máy tính không chạm

**Sinh viên**. Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3.  
**GVHD**. PGS.TS. Võ Đình Bảy.  
**Buổi báo cáo**. 08/11/2026, từ 14 giờ, online.  
**Phạm vi số liệu**. Rà soát ngày 07/11/2026, đến tuần 4 của kế hoạch 12/10–20/12/2026.  
**Repository**. `{M['project_root']}`.

## 1. Tổng quan đề tài

### 1.1. Bài toán và lý do lựa chọn

Đề tài xây dựng một nguyên mẫu dùng webcam RGB để nhận diện chuỗi chuyển động bàn tay và phát lệnh chuyển slide hoặc cuộn trang. Người dùng ngồi trước máy, đưa một bàn tay vào khung hình và thực hiện một trong bốn hướng cử chỉ. Chương trình cần phân biệt cử chỉ với trạng thái nền, xác nhận trước khi gửi lệnh và có cách bật/tạm dừng rõ ràng.

Nhận diện một chuỗi chuyển động đòi hỏi kết hợp thông tin tư thế và sự thay đổi theo thời gian. MediaPipe cung cấp điểm bàn tay từ ảnh [4], [7]. LSTM xử lý chuỗi đặc trưng để dự đoán nhãn [5], [6]. Bài toán đồ án còn bao gồm việc biến dự đoán thành một lệnh có thể dùng trong ứng dụng.

### 1.2. Mục tiêu và phạm vi

Mục tiêu tổng quát là tạo một nguyên mẫu nhận diện và điều khiển có thể trình diễn, kiểm tra lại số liệu và giải thích cách xử lý. Các mục tiêu cụ thể gồm thu dữ liệu có nhãn, xây dựng chuỗi đặc trưng, huấn luyện LSTM, đánh giá phân loại clip và thử nghiệm phát lệnh trực tiếp.

Phạm vi theo đặc tả 1.1 gồm một người và một bàn tay, webcam Windows, bốn hướng cử chỉ cùng lớp nền. Bản cơ bản dùng chuyển slide và cuộn trang, phím F8 để bật/tạm dừng, F9 để dừng toàn cục. Điều kiện mục tiêu là đủ sáng, bàn tay thấy rõ và cử chỉ thực hiện từng lần có thời gian nghỉ.

Giá trị ở quy mô đồ án nằm ở bộ dữ liệu tự thu, quy trình xử lý đồng nhất, mô hình nhỏ và phép thử điều khiển có ghi nhận. Kết luận về kiến trúc mới hoặc khả năng tổng quát cần nghiên cứu đối chứng và dữ liệu bổ sung.

## 2. Nghiên cứu liên quan

### 2.1. IPN HandS [1]

Gibran Benitez-Garcia, Jesus Olivares-Mercado, Gabriel Sanchez-Perez và Hiroki Takahashi công bố *IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition* trên Applied Sciences năm 2025, DOI 10.3390/app15116321. Công trình nghiên cứu chất lượng gán nhãn skeleton trong video cử chỉ RGB liên tục. Bảng 1 ghi 50 người, 14 lớp và 5.177 mẫu cử chỉ. Giao thức đánh giá chia người độc lập, 37 người train và 13 người test.

Mô hình dùng 42 tọa độ x/y của 21 điểm, ba tầng LSTM với 256 nút ẩn mỗi tầng và lớp phân loại 14 nhãn. Bảng 6 báo accuracy 91,2 ± 1,4% và average recall 78,0 ± 1,2% qua ba lần chạy. Các số này phải được đọc cùng giao thức và đơn vị phần trăm của bảng. Báo cáo dùng Bảng 6 làm nguồn định lượng.

Ưu điểm là kết hợp kiểm tra landmark, sửa bằng tay và đánh giá theo người chưa xuất hiện trong train. Hạn chế đối với việc áp dụng trực tiếp vào đồ án là quy mô, số lớp và mô hình lớn hơn, cùng yêu cầu kiểm tra nhãn. Tác động quan trọng đối với đề tài hiện tại là cần xem video và kiểm tra ý nghĩa cử chỉ, bên cạnh kiểm tra shape của NPZ.

### 2.2. SKETCH [2]

Sang Hoon Han và cộng sự công bố *Doodle to Detect: A Goofy but Powerful Approach to Skeleton-based Hand Gesture Recognition* tại NeurIPS 2025, DOI 10.52202/085713-4682. SKETCH chuyển skeleton có thời gian và tọa độ x/y/z thành biểu diễn đồ thị dạng ảnh, sử dụng Dynamic Range Embedding và backbone thị giác. Công trình đánh giá trên SHREC’19 và SHREC’22.

Bảng 1, cấu hình Swin-L có augmentation, ghi detection rate 0,93 và false positive 0,01 trên SHREC’19. Đây là DR/FP của giao thức phát hiện cử chỉ. Trong mục 5.1, tác giả nêu quyết định theo từng cửa sổ độc lập còn bỏ qua ngữ cảnh giữa các cửa sổ. Cơ chế tổng hợp dự đoán cũng đặt ra đánh đổi giữa giảm nhiễu và độ trễ.

Ưu điểm liên quan đến đồ án là cách kiểm tra thông tin chuyển động và vai trò của chuẩn hóa. Hạn chế khi chuyển trực tiếp sang nguyên mẫu là cần biểu diễn và backbone khác LSTM hiện tại. Đồ án có thể học cách đánh giá lỗi và chất lượng biểu diễn từ nghiên cứu này, trong khi việc tái lập phương pháp cần một thí nghiệm riêng.

### 2.3. ConvMixFormer [3]

Mallika Garg, Debashis Ghosh và Pyari Mohan Pradhan công bố *ConvMixFormer- A Resource-Efficient Convolution Mixer for Transformer-Based Dynamic Hand Gesture Recognition* tại WACV 2025, trang 6156–6166. Phương pháp thay bộ trộn self-attention bằng convolution và dùng cơ chế gating. Nghiên cứu sử dụng NVGesture và Briareo, với cả đầu vào đơn phương thức và kết hợp cảm biến.

Bảng 1 cho RGB đơn phương thức báo accuracy 76,04% trên NVGesture và 98,26% trên Briareo. Bảng 6 ghi 13,57 triệu tham số, so với 24,30 triệu của Transformer được dùng làm đối chiếu trong bài. Các kết quả thể hiện đánh đổi độ chính xác và quy mô mô hình trong chính giao thức của nghiên cứu.

Ưu điểm là phân tích chi phí tham số cùng kết quả nhiều loại đầu vào. Hạn chế đối với đồ án là đầu vào ảnh và bộ dữ liệu khác, cùng chi phí mô hình lớn hơn LSTM nhỏ hiện tại. Bài học áp dụng là cần ghi cả hiệu năng đo trên máy và chất lượng phân loại trước khi chọn mở rộng kiến trúc.

### 2.4. So sánh và hướng tiếp cận

| Công trình | Phương pháp và dữ liệu | Kết quả gốc được dùng | Liên quan và giới hạn |
|---|---|---|---|
| IPN HandS [1] | Landmark 2D, LSTM 3 tầng; 50 người, 14 lớp | Accuracy 91,2 ± 1,4%; average recall 78,0 ± 1,2% | Kiểm tra chất lượng nhãn; giao thức chia theo người |
| SKETCH [2] | Skeleton thành ảnh, DRE, ViT/Swin; SHREC’19/22 | SHREC’19 DR 0,93; FP 0,01 | Biểu diễn chuyển động và chuẩn hóa; còn giới hạn cửa sổ độc lập |
| ConvMixFormer [3] | Convolution token mixer và gating; NVGesture, Briareo | RGB accuracy 76,04% và 98,26%; 13,57M tham số | Đánh đổi chi phí và độ chính xác; đầu vào khác đồ án |

Các chỉ số trên thuộc các tập dữ liệu và bài toán đánh giá khác nhau. Kết quả 80% của đồ án được diễn giải trong phạm vi 50 clip tự thu. Chưa có thí nghiệm chạy các phương pháp [1]–[3] trên cùng dữ liệu của đồ án.

Hướng tiếp cận hiện tại kế thừa landmark và mô hình chuỗi, tập trung vào năm nhãn và việc phát lệnh trên máy đang dùng. Những nội dung còn cần chứng minh gồm khả năng phân biệt lên/xuống, độ ổn định của phát lệnh, độ trễ và khả năng hoạt động với người hoặc điều kiện mới. Đây là khoảng trống thực nghiệm của nguyên mẫu cần hoàn thiện.

### 2.5. Trọng tâm theo góp ý GVHD ở tuần 2

GVHD yêu cầu chỉ rõ nghiên cứu trước, đọc hiểu bài báo, hiểu code chạy như thế nào rồi mới mở rộng. Phần đọc sâu chọn IPN HandS [1] vì có mô hình cơ sở landmark + LSTM gần cách triển khai hiện tại. SKETCH [2] và ConvMixFormer [3] dùng để đối chiếu các hướng khác. Việc chọn này không khẳng định code đồ án bắt nguồn trực tiếp từ code tác giả.

Cần đọc Abstract/Introduction để xác định bài toán và đóng góp; mục 5.1–5.2, trang 13–14 để hiểu đầu vào, LSTM, phân chia và huấn luyện; Bảng 6 trang 15 để hiểu kết quả; phần hạn chế để biết phạm vi kết luận. Đầu ra của việc đọc là bản giải thích bằng lời của sinh viên, có chỉ đúng đoạn/bảng làm căn cứ.

Nguồn tác giả tại [README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) có mô tả dữ liệu. [model.py trong repo](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) đang được xem là bộ chọn mô hình CNN thuộc benchmark IPN Hand trước đó. Chưa xác minh được đường chạy LSTM của thí nghiệm 2025 và chưa tái lập kết quả gốc. Cần kiểm tra đúng phiên bản mã và dữ liệu trước khi nói đã chạy code bài báo.

## 3. Phương pháp nghiên cứu và cấu hình đã triển khai

### 3.1. Kiến trúc và trách nhiệm từng phần

| Thành phần | Đầu vào | Xử lý | Đầu ra |
|---|---|---|---|
| Camera | Webcam RGB | Đọc ảnh, hình gương một lần, timestamp tăng | Ảnh và thời gian |
| Hand Landmarker | Ảnh | Tìm 21 điểm, chấp nhận đúng một tay | Tọa độ x/y hoặc trạng thái mất tay |
| Đặc trưng | 21 điểm x/y | Cùng đơn vị ảnh, trừ cổ tay, chuẩn hóa lòng bàn tay | Vector 44 chiều |
| Bộ đệm | Vector và timestamp | Lấy mẫu 20 Hz, giữ 30 mẫu | Chuỗi 30 × 44 |
| LSTM và Linear | Chuỗi | LSTM 1 tầng, 64 nút ẩn, lớp phân loại | 5 logits và xác suất |
| Xác nhận lệnh | Nhãn, xác suất, trạng thái bật/tắt | Ngưỡng, giữ ổn định, chờ nền và cooldown | Một lệnh hoặc chờ |
| Điều khiển | Nhãn đã xác nhận | Gửi phím trái/phải hoặc cuộn | Thao tác ở ứng dụng có focus |

### 3.2. Thu thập và chuẩn hóa

Công cụ `collect` cho chọn nhãn, đếm ngược và lưu một động tác trong mỗi clip. Mỗi mẫu có AVI sạch, NPZ đặc trưng, mã phiên và dòng manifest. Mất tay, hai tay hoặc khoảng gián đoạn quá 100 ms làm lượt thu cần thực hiện lại. Kiểm tra dữ liệu xác nhận kiểu dữ liệu, kích thước, nhãn, phiên, video tham chiếu và tính hợp lệ số học. Ý nghĩa của động tác được kiểm tra bằng việc xem lại video.

Với ảnh rộng W, cao H, tọa độ ban đầu p được đổi thành q = p × [W, H] / max(W, H). Gọi w là điểm cổ tay và s là trung vị khoảng cách từ cổ tay tới các điểm 5, 9, 13, 17. Vector hình dạng là (q − w)/s, trải phẳng thành 42 giá trị. Nối thêm hai tọa độ cổ tay tạo vector 44 chiều. Hai giá trị cuối giữ quỹ đạo toàn cục trong ảnh.

Bộ đệm lấy mẫu cách 50 ms và nội suy khe hở ngắn khi đã có hai đầu mút hợp lệ. Chuỗi bị xóa khi mất dữ liệu hoặc khoảng hở quá 100 ms. 30 bước có khoảng từ mẫu đầu tới mẫu cuối là 1,45 giây, thường được mô tả gần 1,5 giây. Nhịp lấy mẫu 20 Hz là cấu hình dữ liệu, cần đo riêng FPS xử lý thực tế.

### 3.3. Huấn luyện và đánh giá

Đầu vào theo batch là [B, 30, 44]. LSTM trả chuỗi trạng thái ẩn, chương trình lấy trạng thái cuối, qua Linear 64 → 5. Mô hình có {M['checkpoint']['parameters']:,} tham số. CrossEntropyLoss nhận logits khi huấn luyện. Softmax dùng lúc suy luận để chọn nhãn và mức tin cậy.

Cấu hình mã nguồn gồm Adam, learning rate 0,001, batch size 16 và seed 42. Log đã lưu trong notebook có đủ 30 epoch. Checkpoint được chọn theo validation loss thấp nhất ở epoch 23, với loss {M['checkpoint']['validation_loss']:.6f} và validation accuracy 94%. Hai checkpoint ứng dụng và notebook có trọng số trùng khớp khi kiểm tra từng tensor.

Mô hình dùng train để cập nhật trọng số, validation để chọn checkpoint, test để đo kết quả. Các chỉ số hiện được tính trong `evaluation.py` bằng NumPy. Ngưỡng phát lệnh khởi đầu 0,80, cần ít nhất ba dự đoán mới và ổn định 150 ms. Sau một lệnh, chương trình chờ ít nhất 1.000 ms và nền ổn định 300 ms trước lần tiếp.

### 3.4. Môi trường hiện tại

Python {M['python']}, Windows, PyTorch bản CPU. Đây là phiên bản đọc từ môi trường đang dùng trong lần rà soát.

| Thư viện | Phiên bản đã cài |
|---|---|
{version_rows}

### 3.5. Đối chiếu nghiên cứu với luồng code hiện có

Bài [1] dùng 42 tọa độ xy, LSTM ba tầng 256 nút ẩn, dropout 0,3 và 14 lớp có chủ đích; đồ án dùng 42 giá trị cục bộ nối hai tọa độ cổ tay, LSTM một tầng 64 và năm lớp gồm nền. Bài dùng cửa sổ dài tối đa 64 frame, stride 32 cho chuỗi dài và không padding/nội suy chuỗi ngắn; đồ án tạo chuỗi cố định 30 mẫu ở 20 Hz. Bài chia theo 37/13 người; đồ án hiện chia theo phiên thu. Các khác biệt này cần được giải thích và đánh giá riêng, chưa phải bằng chứng cải tiến.

Thứ tự đọc mã: `features.py:extract_features` → `SequenceBuffer.push` → `model.py:GestureLSTM.forward` → `predict_gesture` → `training.py:train_model` → `evaluation.py:evaluate_model` → luồng webcam trong `app.py` và xác nhận lệnh trong `control.py`.

Đã chạy tách các bước suy luận của một clip test: [1,30,44] → [1,30,64] → [1,64] → [1,5]. Kết quả trùng `model(x)`, nhãn BACKGROUND đúng với clip được chọn; đây là kiểm tra luồng thực thi, không thay đổi chỉ số của bộ test hoặc chứng minh tái lập nghiên cứu. Chi tiết tại `slide_sources/model_execution_trace.json`; cách tự học tại `Huong_dan_doc_bai_bao_va_code.md`.

## 4. Tiến độ triển khai thực tế

| Hạng mục | Trạng thái | Minh chứng | Vấn đề tồn tại |
|---|---|---|---|
{progress_rows}

Tuần 1 (12–18/10) nghiên cứu tài liệu. Tuần 2 (19–25/10) tìm hiểu MediaPipe và LSTM. Tuần 3 (26/10–01/11) thiết lập webcam và công cụ thu. Tuần 4 (02–08/11) đã có bộ 250 clip, mô hình và đánh giá clip. Trạng thái được đối chiếu với mã nguồn và artifact hiện tại. Một số đoạn README/ROADMAP vẫn ghi trạng thái cũ và cần đồng bộ khi cập nhật tài liệu dự án.

## 5. Dữ liệu và kết quả thực nghiệm

### 5.1. Quy mô và cách chia tập

| Nhóm | Số clip | Tỷ lệ | Mỗi nhãn | Phiên |
|---|---:|---:|---:|---|
| Train | 150 | 60% | 30 | pilot_01, train_02 |
| Validation | 50 | 20% | 10 | val_01 |
| Test | 50 | 20% | 10 | test_01 |
| Tổng | 250 | 100% | 50 | 4 phiên |

Cả năm lớp có số mẫu cân bằng. Kiểm tra không thấy chuỗi đặc trưng trùng tuyệt đối giữa các nhóm. Phân chia theo phiên giúp tách các lần thu. Manifest chưa ghi mã người tham gia, nên chưa có cơ sở xác nhận đánh giá theo người chưa xuất hiện trong train.

### 5.2. Đường cong huấn luyện

Biểu đồ trong slide 9 dùng 30 dòng output đã lưu ở notebook, được trích nguyên giá trị vào `slide_sources/training_history.csv`. Loss trong log được làm tròn bốn chữ số thập phân. Train loss đầu/cuối là 1,5541/0,1293. Validation loss đầu/cuối là 1,4313/0,1720. Validation loss thấp nhất là 0,1085 ở epoch 23. Giá trị cuối cùng không phải tiêu chí chọn mô hình trong mã.

Validation accuracy ở checkpoint là 94%, cao hơn test accuracy 80% là 14 điểm phần trăm. Đường validation dao động sau khi loss train giảm. Đây là bằng chứng cần kiểm tra thêm độ ổn định giữa các phiên và các lần chạy. Một lần chạy và một bộ test nhỏ chưa đủ để kết luận nguyên nhân của chênh lệch.

Notebook ghi thời gian huấn luyện 5,0 giây. Đây là thời gian được lưu của lần chạy notebook, chưa phải phép đo nhiều lần hoặc thời gian suy luận webcam.

### 5.3. Chỉ số phân loại trên test

Chạy lại checkpoint hiện tại trên đủ 50 clip test khớp với `outputs/evaluation.json` và báo cáo notebook. Accuracy 0,8000, macro precision 0,8000, macro recall 0,8000 và Macro-F1 0,7619. Precision, recall và F1 nằm trên thang 0–1.

| Nhãn | Số mẫu | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
{metric_rows}

Macro-F1 lấy trung bình F1 của từng lớp. Vì lỗi tập trung ở lớp vuốt lên, cần xem từng lớp và ma trận nhầm lẫn cùng accuracy.

### 5.4. Ma trận nhầm lẫn và ý nghĩa

Hàng là nhãn thật, cột là nhãn dự đoán. Mỗi ô là số clip.

| Thật / Dự đoán | Nền | Trái | Phải | Lên | Xuống |
|---|---:|---:|---:|---:|---:|
| Nền | 10 | 0 | 0 | 0 | 0 |
| Trái | 0 | 10 | 0 | 0 | 0 |
| Phải | 0 | 0 | 10 | 0 | 0 |
| Lên | 0 | 0 | 0 | 1 | 9 |
| Xuống | 0 | 0 | 0 | 1 | 9 |

Trong 10 lỗi, có chín clip lên bị nhận thành xuống và một clip xuống bị nhận thành lên. Nền, trái và phải đạt 10/10 trong phiên test hiện có. Một video 10 giây đã được tạo bằng cách phát lại năm clip test, có hiển thị nhãn thật và dự đoán. Riêng lớp lên sử dụng một clip sai để minh họa vấn đề.

### 5.5. Tích hợp, kiểm thử và phần chưa đo

Lệnh `run` đã nối dự đoán với hiển thị và cơ chế phát lệnh. Mã nguồn có F8/F9 toàn cục, khởi đầu điều khiển tắt, xác nhận cử chỉ và chống lặp. Bộ test hiện có chạy qua {M['tests']['passed']} trường hợp trong lần rà soát. Các test tự động sử dụng dữ liệu hoặc đối tượng giả tại biên camera/điều khiển và kiểm tra thuật toán thực ở phần tương ứng.

| Phép đo | Trạng thái | Cách bổ sung |
|---|---|---|
| Latency suy luận ổn định | Chưa có dữ liệu thực nghiệm | Warm-up, đo nhiều lần với timestamp và ghi cấu hình máy |
| FPS toàn luồng có tay và LSTM | Chưa có dữ liệu thực nghiệm | Đo sau warm-up trên webcam thật, chỉ đếm kết quả mới |
| 40 lượt thao tác trực tiếp | Chưa có dữ liệu thực nghiệm | Mỗi hướng 10 lượt, ghi đúng/sai/bỏ sót/lặp |
| 5 phút nền và chuyển động thường | Chưa có dữ liệu thực nghiệm | Ghi nguyên số lệnh phát nhầm trong 5 phút |
| Người chưa xuất hiện trong train | Chưa có dữ liệu thực nghiệm | Thu người mới, giữ riêng phiên đánh giá |

## 6. Khó khăn, hạn chế và cách kiểm chứng

| Vấn đề | Bằng chứng và mức chắc chắn | Hướng xử lý | Kiểm chứng |
|---|---|---|---|
| Lên/xuống bị nhầm | Đã quan sát 10 lỗi trong test | Xem video sai, kiểm tra quy ước và thu bù train/validation | So sánh recall từng lớp trên phiên đánh giá được khóa |
| Tư thế giữa nhãn khác nhau | Quan sát các clip mẫu, còn cần GVHD xác nhận quy cách | Thống nhất mô tả cử chỉ và cách đưa tay về nghỉ | Xem mẫu trước khi thu hàng loạt, lưu tiêu chí nhận mẫu |
| Khái quát hóa còn giới hạn | Bộ tự thu nhỏ, tách phiên, chưa có mã người | Bổ sung metadata và người/điều kiện mới theo phạm vi được duyệt | Tập người mới hoặc phiên mới độc lập |
| Validation và test chênh 14 điểm phần trăm | Đã quan sát ở checkpoint hiện tại | Giữ giao thức và ghi nhiều lần chạy nếu thời gian cho phép | Báo mean/std và kết quả từng phiên khi đã đo |
| Độ ổn định điều khiển còn thiếu đo lường | Có mã nguồn, thiếu bảng thử trực tiếp | Thực hiện 40 lượt, 5 phút nền và kiểm tra F8/F9 | Báo đúng/sai/bỏ sót/lặp và log thời gian |

Các khả năng mô hình học tư thế thay vì hướng chuyển động, sai lệch giữa các phiên hoặc overfitting là giả thuyết cần thí nghiệm. Dữ liệu hiện có xác nhận lỗi phân loại, chưa xác định nguyên nhân duy nhất. Chưa có bằng chứng bộ dữ liệu mất cân bằng số lượng vì mỗi lớp đều có 50 clip.

## 7. Kế hoạch phát triển tiếp theo

Kế hoạch cập nhật bắt đầu từ tuần 5 vì đã có kết quả huấn luyện và đánh giá trong tuần 4. Thời hạn kết thúc thực hiện là 20/12/2026. Đợt nộp LMS 21–27/12 cần file scan phiếu tiến độ có chữ ký GVHD.

{plan_text}

## 8. Kết luận

Đồ án đã có bộ dữ liệu 250 clip, cách xử lý chuỗi 30 × 44, LSTM 28.485 tham số, log huấn luyện và checkpoint. Kết quả kiểm tra lại trên 50 clip đạt accuracy 80% và Macro-F1 0,7619. Mã nguồn đã nối nhận diện với hiển thị, phím điều khiển và xác nhận lệnh.

Kết quả hiện tại chứng minh chương trình có thể học và đánh giá năm nhãn trên bộ clip đã thu. Lỗi lên/xuống và phần kiểm thử điều khiển trực tiếp còn cần xử lý. Công việc ưu tiên là thống nhất quy cách cử chỉ, củng cố dữ liệu và ghi nhận các phép thử ứng dụng trước khi chốt kết quả cuối.

Danh mục tài liệu tham khảo theo số [1]–[7] nằm trong `references.md`. Dữ liệu dùng dựng biểu đồ, nguồn tạo slide và ghi chú thuyết trình đi cùng thư mục `slide_sources/` và `speaker_notes.md`.
'''
(OUTPUT / 'Bao_Cao_Tien_Do.md').write_text(report, encoding='utf-8')
print(json.dumps({'report': str(OUTPUT / 'Bao_Cao_Tien_Do.md'), 'references': len(references),
                  'progress_items': len(progress), 'planned_weeks': len(plan)}, ensure_ascii=False))
