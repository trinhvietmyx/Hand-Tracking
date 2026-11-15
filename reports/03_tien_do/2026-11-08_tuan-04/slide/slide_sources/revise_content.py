"""Revise generated sources to address the supervisor's week-2 feedback."""
from pathlib import Path

S=Path(__file__).resolve().parent
p=S/'build_deck.cjs'
t=p.read_text(encoding='utf-8')
block4=r'''// 04 — Read one primary paper closely, then compare it with the current implementation.
{
 const s=base('02 / Bài báo đọc sâu','IPN HandS: bài báo nào, học được gì, khác code ở đâu?','Nguồn: [1], mục 5.1–5.3, tr. 13–15; features.py, model.py và cấu hình đồ án.');
 text(s,'IPN HandS: Efficient Annotation Tool and Dataset\nfor Skeleton-Based Hand Gesture Recognition',.65,1.7,12.03,.85,22,{bold:true,color:P.teal});
 text(s,'G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, H. Takahashi\nApplied Sciences 15(11), 6321, 2025  |  DOI: 10.3390/app15116321',.65,2.71,12.03,.58,14.3);
 table(s,['Thành phần','Bài báo [1]','Code đồ án hiện tại'],[
  ['Đầu vào mỗi bước','21 điểm xy → 42 giá trị','42 giá trị chuẩn hóa + 2 vị trí cổ tay'],
  ['Mô hình','3 tầng LSTM × 256; dropout 0,3','1 tầng LSTM × 64; Linear → 5 nhãn'],
  ['Nhãn đánh giá','14 cử chỉ; bỏ nền khi phân loại','4 hướng cử chỉ + BACKGROUND'],
  ['Dữ liệu / cách chia','50 người; 37 train / 13 test','250 clip; chia 150/50/50 theo phiên']
 ],{y:3.46,colW:[2.15,4.65,5.23],rowH:.49,fontSize:15.2});
 text(s,'Học được: chất lượng landmark ảnh hưởng kết quả; cần đọc recall từng lớp và cách chia tập.',.65,6.13,12.03,.38,16.5);
 text(s,'Chưa có minh chứng đã chạy lại thí nghiệm LSTM của bài báo trên dữ liệu gốc.',.65,6.62,12.03,.28,14.5,{color:P.red});
 note(s,'Đọc sâu IPN HandS và đối chiếu code','Theo góp ý của GVHD ở tuần 2, phần này trả lời cụ thể bài nào làm trước và mình hiểu được gì. IPN HandS công bố trên Applied Sciences năm 2025, DOI 10.3390/app15116321, bốn tác giả được ghi trên slide. Bài nghiên cứu tác động của chất lượng gán nhãn landmark và biên thời gian lên nhận diện cử chỉ; LSTM là mô hình cơ sở để so sánh ba nguồn annotation. Cần hiểu công cụ/dữ liệu đã sửa nhãn và cách đánh giá cùng với mạng LSTM.\n\nMục 5.1: mỗi bước gồm 42 tọa độ xy của 21 điểm; ba tầng LSTM 256, dropout 0,3; trạng thái cuối qua lớp phân loại 14 cử chỉ. Mục 5.2: 50 người, 37 train/13 test; tối đa 64 frame, stride 32 cho chuỗi dài; không padding/nội suy chuỗi ngắn. Đo phân loại 14 lớp có chủ đích, bỏ đoạn nền. Huấn luyện 30 epoch, batch 64, Adam 0,001, lặp ba lần. Bảng 6: accuracy 91,2 ± 1,4%, average recall 78,0 ± 1,2%. Bài có mất cân bằng lớp; bộ 250 clip của đồ án hiện cân bằng.\n\nĐồ án dùng 44 đặc trưng, chuỗi 30 mẫu tại 20 Hz, LSTM một tầng 64 và năm nhãn gồm nền. Cấu hình và giao thức khác nhau; chưa đủ để nói đã tái lập bài báo hoặc cải tiến tốt hơn.\n\nĐã kiểm tra nguồn tác giả: https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md mô tả dữ liệu HandS; model.py ở nhánh được xem thuộc benchmark CNN của IPN Hand trước đó. Chưa xác minh được đường chạy LSTM tương ứng bài 2025 và chưa chạy thí nghiệm gốc. Không trình bày chạy code đồ án thành chạy code tác giả.\n\nKhoảng trống của nguyên mẫu vẫn là lỗi lên/xuống, đo điều khiển trực tiếp, FPS và độ trễ. Trước khi mở rộng, cần nắm phương pháp và giải thích luồng code hiện có.',[1]);
}
'''
block8=r'''// 08 — Explain actual functions and tensor shapes before discussing extensions.
{
 const s=base('05 / Hiểu code đang chạy','Từ chuỗi 30 × 44 tới năm nhãn: đọc hàm nào?','Nguồn: features.py, model.py, training.py; trace một clip trong model_execution_trace.json; [5], [6].');
 const xs=[.65,3.84,7.03,10.22];
 [['Chuỗi đầu vào','[B, 30, 44]'],['LSTM','64 nút ẩn; 1 tầng'],['Trạng thái cuối','[B, 64]'],['Linear → logits','[B, 5]']].forEach((r,i)=>node(s,xs[i],2.12,2.46,r[0],r[1],i===1));
 for(let i=0;i<3;i++)arrow(s,xs[i]+2.52,2.64,xs[i+1]-.08,2.64);
 table(s,['Tệp / hàm cần đọc','Đầu vào → đầu ra','Nhiệm vụ'],[
 ['features.py: extract_features','21 × 2 → 44 giá trị','Chuẩn hóa; giữ thêm vị trí cổ tay'],
 ['features.py: SequenceBuffer','Vector + thời gian → 30 × 44','Lấy mẫu 20 Hz; xóa khi mất tay'],
 ['model.py: forward','[B,30,44] → [B,5]','LSTM → lấy bước cuối → Linear'],
 ['model.py: predict_gesture','Chuỗi → nhãn + mức tin cậy','Softmax; chọn nhãn điểm cao nhất']
 ],{y:3.83,colW:[3.35,3.35,5.33],rowH:.49,fontSize:15});
 text(s,'Train: Adam 0,001 • batch 16 • seed 42 • 30 epoch • CPU • chọn checkpoint theo validation loss.',.65,6.48,12.03,.33,14.5,{color:P.teal});
 note(s,'Đọc code và giải thích một lượt suy luận','Đọc theo đường đi dữ liệu. features.py:extract_features nhận 21 điểm xy, đổi về cùng đơn vị, trừ cổ tay và chia kích thước lòng bàn tay. 42 giá trị cục bộ nối hai tọa độ cổ tay thành 44. SequenceBuffer.push nhận vector và timestamp; lấy mẫu 20 Hz thành 30 bước, xóa chuỗi khi mất tay hoặc khoảng hở quá 100 ms.\n\nTrong model.py, GestureLSTM.forward gọi sequence,_=self.lstm(features). Đầu vào [B,30,44] tạo sequence [B,30,64]. Dòng sequence[:, -1, :] lấy trạng thái ở thời điểm cuối cho mỗi mẫu, được [B,64]; đây không phải nhãn cuối hoặc frame cuối của video gốc. Linear 64→5 tạo logits cho năm nhãn. predict_gesture thêm chiều batch, chạy model, softmax rồi lấy nhãn/mức tin cậy cao nhất. MediaPipe tìm điểm bàn tay; LSTM trong đồ án phân loại cử chỉ.\n\nĐã chạy riêng một clip test đã lưu: input [1,30,44] → LSTM output [1,30,64] → last state [1,64] → logits [1,5]. Nhãn thật/dự đoán đều BACKGROUND; confidence khoảng 0,99244. Đường gọi từng bước và model(x) cho cùng kết quả. Đây là minh chứng luồng thực thi của một clip trong code đồ án, không phải số liệu tái lập IPN HandS. Chạy lại bằng trace_current_model.py; kết quả model_execution_trace.json.\n\nĐọc tiếp training.py:train_model theo thứ tự load_split, DataLoader, forward, CrossEntropyLoss, backward, Adam.step, validation, lưu checkpoint khi val_loss giảm. Cấu hình: 44 chiều, hidden 64, một tầng, năm nhãn, 28.485 tham số; batch 16, Adam 0,001, seed 42, 30 epoch, CPU. Checkpoint epoch 23 được chọn bằng validation loss. Chưa có thí nghiệm chứng minh cấu hình tối ưu. Môi trường Python 3.11.0, torch 2.15.0+cpu, MediaPipe 0.10.35, OpenCV 4.14.0.94.',[5,6]);
}
'''
for num,nxt,new in [('04','05',block4),('08','09',block8)]:
 a=t.index('// '+num+' —');b=t.index('// '+nxt+' —',a);t=t[:a]+new+t[b:]
t=t.replace("['5 • 09–15/11','Chốt cử chỉ; sửa nhầm lên/xuống','Quy cách + danh mục dữ liệu + checkpoint chọn bằng validation']", "['5 • 09–15/11','Đọc sâu bài [1]; đối chiếu code','Phiếu đọc báo + sơ đồ code + quy cách cử chỉ; phân tích lỗi dọc']")
t=t.replace("'Đã có mô hình chạy được; ưu tiên sửa hai hướng dọc'", "'Hiểu bài báo và code trước khi mở rộng'")
t=t.replace("'Chốt cách vuốt với GVHD → sửa lỗi lên/xuống → thử trực tiếp và ghi số liệu.'", "'Đọc sâu IPN HandS → giải thích code → kiểm chứng lỗi lên/xuống.'")
t=t.replace("'Kết luận và tài liệu tham khảo','", "'Kết luận và tài liệu tham khảo','Theo góp ý tuần 2, thứ tự ưu tiên là đọc hiểu bài báo, giải thích được code và phép thử hiện có, rồi mới mở rộng. Chưa có minh chứng tái lập mã LSTM của bài báo. ")
p.write_text(t,encoding='utf-8')

p=S/'write_report.py';t=p.read_text(encoding='utf-8')
t=t.replace("'goal': 'Chốt cử chỉ và xử lý lỗi lên/xuống'", "'goal': 'Đọc sâu bài báo, giải thích code và xử lý lỗi lên/xuống'")
t=t.replace("'work': 'Đối chiếu video với GVHD; thu bù ở train/validation nếu cần; giữ nhóm test cuối riêng.'", "'work': 'Đọc mục 5.1–5.3 của IPN HandS; đối chiếu features/model/training; chạy trace một clip; chốt cử chỉ với GVHD và phân tích lỗi trước khi thu bù.'")
t=t.replace("'output': 'Quy cách cử chỉ, danh mục dữ liệu và checkpoint có mã phiên.'", "'output': 'Phiếu đọc bài báo, sơ đồ luồng code, trace một clip, quy cách cử chỉ và phân tích lỗi lên/xuống.'")
t=t.replace("'acceptance': 'Mẫu đúng quy cách; chia tập rõ ràng; chọn checkpoint bằng validation.'", "'acceptance': 'Chỉ được bài gốc và các hàm tương ứng; giải thích 44/30/64/5; phân biệt code đồ án với code tác giả; mọi sửa dữ liệu/mô hình chọn bằng validation.'")
new_section='''### 2.5. Trọng tâm theo góp ý GVHD ở tuần 2

GVHD yêu cầu chỉ rõ nghiên cứu trước, đọc hiểu bài báo, hiểu code chạy như thế nào rồi mới mở rộng. Phần đọc sâu chọn IPN HandS [1] vì có mô hình cơ sở landmark + LSTM gần cách triển khai hiện tại. SKETCH [2] và ConvMixFormer [3] dùng để đối chiếu các hướng khác. Việc chọn này không khẳng định code đồ án bắt nguồn trực tiếp từ code tác giả.

Cần đọc Abstract/Introduction để xác định bài toán và đóng góp; mục 5.1–5.2, trang 13–14 để hiểu đầu vào, LSTM, phân chia và huấn luyện; Bảng 6 trang 15 để hiểu kết quả; phần hạn chế để biết phạm vi kết luận. Đầu ra của việc đọc là bản giải thích bằng lời của sinh viên, có chỉ đúng đoạn/bảng làm căn cứ.

Nguồn tác giả tại [README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) có mô tả dữ liệu. [model.py trong repo](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) đang được xem là bộ chọn mô hình CNN thuộc benchmark IPN Hand trước đó. Chưa xác minh được đường chạy LSTM của thí nghiệm 2025 và chưa tái lập kết quả gốc. Cần kiểm tra đúng phiên bản mã và dữ liệu trước khi nói đã chạy code bài báo.

'''
t=t.replace('## 3. Phương pháp nghiên cứu và cấu hình đã triển khai',new_section+'## 3. Phương pháp nghiên cứu và cấu hình đã triển khai')
new_code='''### 3.5. Đối chiếu nghiên cứu với luồng code hiện có

Bài [1] dùng 42 tọa độ xy, LSTM ba tầng 256 nút ẩn, dropout 0,3 và 14 lớp có chủ đích; đồ án dùng 42 giá trị cục bộ nối hai tọa độ cổ tay, LSTM một tầng 64 và năm lớp gồm nền. Bài dùng cửa sổ dài tối đa 64 frame, stride 32 cho chuỗi dài và không padding/nội suy chuỗi ngắn; đồ án tạo chuỗi cố định 30 mẫu ở 20 Hz. Bài chia theo 37/13 người; đồ án hiện chia theo phiên thu. Các khác biệt này cần được giải thích và đánh giá riêng, chưa phải bằng chứng cải tiến.

Thứ tự đọc mã: `features.py:extract_features` → `SequenceBuffer.push` → `model.py:GestureLSTM.forward` → `predict_gesture` → `training.py:train_model` → `evaluation.py:evaluate_model` → luồng webcam trong `app.py` và xác nhận lệnh trong `control.py`.

Đã chạy tách các bước suy luận của một clip test: [1,30,44] → [1,30,64] → [1,64] → [1,5]. Kết quả trùng `model(x)`, nhãn BACKGROUND đúng với clip được chọn; đây là kiểm tra luồng thực thi, không thay đổi chỉ số của bộ test hoặc chứng minh tái lập nghiên cứu. Chi tiết tại `slide_sources/model_execution_trace.json`; cách tự học tại `Huong_dan_doc_bai_bao_va_code.md`.

'''
t=t.replace('## 4. Tiến độ triển khai thực tế',new_code+'## 4. Tiến độ triển khai thực tế')
t=t.replace("(OUTPUT / 'references.md').write_text('\\n'.join(ref_lines), encoding='utf-8')", "ref_lines += ['## Mã nguồn và dữ liệu tác giả được kiểm tra thêm', '', '[README HandS](https://github.com/GibranBenitez/IPN-hand/blob/master/README_HandS.md) mô tả dữ liệu công bố; [model.py](https://github.com/GibranBenitez/IPN-hand/blob/master/model.py) được xem thuộc benchmark CNN của IPN Hand. Chưa xác minh đường chạy LSTM tương ứng thí nghiệm 2025; chưa có kết quả tái lập mã tác giả.', '']\n(OUTPUT / 'references.md').write_text('\\n'.join(ref_lines), encoding='utf-8')")
p.write_text(t,encoding='utf-8')
print('Updated slides 4/8/15/16, report and week-5 study priorities.')
