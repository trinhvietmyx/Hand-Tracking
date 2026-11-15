/* Three native, editable sections to insert into the user's current deck. */
const fs=require('fs'),path=require('path'),PptxGenJS=require('pptxgenjs');
const root=__dirname,work=path.join(root,'qa/cai_thien_2026-11-08');
const pptx=new PptxGenJS();pptx.layout='LAYOUT_WIDE';
pptx.author='Trịnh Viết Mỹ';pptx.lang='vi-VN';
pptx.theme={headFontFace:'Arial',bodyFontFace:'Arial',lang:'vi-VN'};
const C={ink:'1A2332',teal:'2D8B8B',pale:'EFF7F7',gray:'526270',white:'FFFFFF',red:'A23D32',grid:'DDE5E8'};
function tx(s,text,x,y,w,h,size=18,opts={}){
 s.addText(text,{x,y,w,h,fontFace:'Arial',fontSize:size,color:C.ink,margin:0,valign:'top',...opts});
}
function rect(s,x,y,w,h,color){s.addShape(pptx.ShapeType.rect,{x,y,w,h,fill:{color},line:{color,width:.6}});}
function arrow(s,x,y,w){s.addShape(pptx.ShapeType.line,{x,y,w,h:0,line:{color:C.teal,width:1.7,beginArrowType:'none',endArrowType:'triangle'}});}
function base(section,title,source,number){
 const s=pptx.addSlide();s.background={color:C.white};
 tx(s,section,.65,.38,12,.27,11,{bold:true,color:C.teal,charSpacing:1.5});
 tx(s,title,.65,.86,12,.63,31,{bold:true});
 tx(s,source,.65,6.98,11.25,.25,10.3,{color:C.gray});
 tx(s,`${String(number).padStart(2,'0')} / 16`,11.9,6.98,.78,.25,10.3,{align:'right',color:C.gray});
 return s;
}
function node(s,x,y,w,title,sub){
 rect(s,x,y,w,.83,C.pale);
 tx(s,title,x+.12,y+.12,w-.24,.29,17.5,{bold:true,align:'center'});
 tx(s,sub,x+.12,y+.49,w-.24,.26,12.7,{color:C.gray,align:'center'});
}
function table(s,headers,rows,y,widths,rowH=.4,size=15.2){
 const values=[headers.map(t=>({text:t,options:{fill:C.ink,color:C.white,bold:true}})),
  ...rows.map((r,i)=>r.map(t=>({text:t,options:{fill:i%2?C.white:C.pale}})))];
 s.addTable(values,{x:.65,y,w:12.03,colW:widths,rowH,fontFace:'Arial',fontSize:size,color:C.ink,
  margin:[.07,.11,.07,.11],border:{type:'solid',pt:.6,color:C.white},valign:'middle',autoPage:false});
}
{
 const s=base('02 / ĐỌC HIỂU NGHIÊN CỨU','IPN HandS: kiểm tra tác động của chất lượng gán nhãn',
  '[1] Applied Sciences 15(11), 6321, 2025; mục 5.1–5.3, Bảng 6, tr. 13–15. Số liệu của bài báo.',4);
 tx(s,'IPN HandS: Efficient Annotation Tool and Dataset\nfor Skeleton-Based Hand Gesture Recognition',.65,1.68,12.03,.8,21,{bold:true,color:C.teal});
 tx(s,'G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, H. Takahashi\nApplied Sciences, 2025  |  DOI: 10.3390/app15116321',.65,2.59,12.03,.48,13.5);
 node(s,.65,3.25,3.71,'200 video RGB','50 người; 14 lớp cử chỉ');
 node(s,4.81,3.25,3.71,'Ba nguồn gán nhãn','HandS / MP Hands / MP Holistic');
 node(s,8.97,3.25,3.71,'Cùng cấu trúc LSTM','3 tầng × 256; mỗi nguồn train riêng');
 arrow(s,4.42,3.66,.31);arrow(s,8.58,3.66,.31);
 tx(s,'Câu hỏi của bài: sửa chất lượng nhãn có giúp nhận diện tốt hơn với cùng kiến trúc?',.65,4.26,12.03,.35,18);
 table(s,['Nguồn gán nhãn','Accuracy (%)','Recall trung bình (%)'],[
  ['MediaPipe Hands','87,5 ± 1,0','62,7 ± 2,0'],
  ['MediaPipe Holistic','89,2 ± 0,6','66,9 ± 0,7'],
  ['IPN HandS đã sửa nhãn','91,2 ± 1,4','78,0 ± 1,2']
 ],4.75,[4.4,3.45,4.18],.38,15.2);
 tx(s,'Trong thí nghiệm này, HandS tăng recall 15,3 điểm phần trăm so với MP Hands; mean ± std qua 3 lần chạy.',.65,6.46,12.03,.4,15.2,{color:C.teal});
 s.addNotes('Trọng tâm của bài là chất lượng gán nhãn landmark và khoảng thời gian cử chỉ. Ba mô hình được huấn luyện riêng từ ba nguồn annotation nhưng dùng cùng cấu trúc và thiết lập. Chia 37/13 người train/test. Các số mean/std lấy từ Bảng 6; 15,3 là hiệu số 78,0 - 62,7, đơn vị điểm phần trăm. Không diễn giải đây là kết quả đồ án.');
}
{
 const s=base('03 / ĐỐI CHIẾU VỚI ĐỒ ÁN','44, 30, 64: ý nghĩa cấu hình và giới hạn kiểm chứng',
  'Nguồn: [1] mục 5.1–5.2; features.py, model.py, configs/default.json; checkpoint 28.485 tham số.',5);
 table(s,['Thành phần','IPN HandS [1]','Đồ án hiện tại'],[
  ['Đặc trưng','42 tọa độ xy của 21 điểm','42 tọa độ cục bộ + 2 vị trí cổ tay'],
  ['Chuỗi','Tối đa 64 frame; stride 32 khi dài','30 mẫu ở 20 Hz; đầu–cuối cách 1,45 s'],
  ['LSTM','3 tầng × 256; dropout 0,3','1 tầng × 64; 28.485 tham số'],
  ['Nhãn','14 cử chỉ; loại nền khi phân loại','5 nhãn: bốn hướng và BACKGROUND'],
  ['Chia tập','37 người train / 13 người test','Theo phiên: 150 train / 50 val / 50 test']
 ],1.78,[2.04,4.36,5.63],.48,15.2);
 const blocks=[
  ['44 đặc trưng','42 giá trị hình dạng + 2 vị trí cổ tay để giữ quỹ đạo trong ảnh.'],
  ['30 mẫu','Nhịp 20 Hz tạo cửa sổ gần 1,5 giây; đây là cấu hình lấy mẫu.'],
  ['64 nút ẩn','Cấu hình cơ sở hiện có; chưa thử đối chứng để kết luận tối ưu.']
 ];
 blocks.forEach((r,i)=>{const x=.65+i*4.16;tx(s,r[0],x,5.1,3.71,.37,21,{bold:true,color:C.teal});tx(s,r[1],x,5.68,3.71,.8,17);});
 tx(s,'Khác cấu hình và dữ liệu chưa phải bằng chứng cải tiến; chưa có kết quả tái lập thí nghiệm LSTM gốc.',.65,6.62,12.03,.27,14.3,{color:C.red});
 s.addNotes('44 được giải thích trực tiếp từ hàm extract_features. 30 ở 20 Hz có 29 khoảng thời gian, tổng 1,45 giây từ đầu tới cuối. 64 là hidden_size đã chọn trong cấu hình hiện có, tương ứng 28.485 tham số; không có thử nghiệm tìm cấu hình tốt nhất. Bài báo không padding/nội suy chuỗi ngắn và loại nền, trong khi đồ án có nội suy khe ngắn và lớp nền.');
}
{
 const s=base('05 / GIẢI THÍCH CODE','Hai dòng forward: từ chuỗi chuyển động tới năm điểm số',
  'Nguồn: src/hand_tracking/model.py: GestureLSTM.forward; model_execution_trace.json. B = số mẫu trong batch.',9);
 const xs=[.65,3.84,7.03,10.22];
 [['features','[B, 30, 44]'],['LSTM output','[B, 30, 64]'],['Bước cuối','[B, 64]'],['Linear → logits','[B, 5]']].forEach((r,i)=>{
  rect(s,xs[i],1.98,2.46,.98,i===1?C.teal:C.pale);
  tx(s,r[0],xs[i]+.1,2.12,2.26,.3,17.5,{bold:true,align:'center',color:i===1?C.white:C.ink});
  tx(s,r[1],xs[i]+.1,2.59,2.26,.27,15.3,{align:'center',color:i===1?C.white:C.gray});
  if(i<3)arrow(s,xs[i]+2.52,2.47,.58);
 });
 tx(s,'GestureLSTM.forward — đúng mã đang chạy',.65,3.47,7,.36,19,{bold:true});
 rect(s,.65,4.04,7.0,1.14,C.pale);
 tx(s,'sequence, _ = self.lstm(features)\nreturn self.classifier(sequence[:, -1, :])',.85,4.25,6.6,.7,16.2,{fontFace:'Courier New'});
 tx(s,'LSTM xử lý theo thứ tự thời gian; trạng thái ẩn mang thông tin từ các bước trước.',.65,5.56,7.0,.8,18);
 tx(s,'[:, -1, :] chọn gì?',8.16,3.47,4.52,.36,19,{bold:true,color:C.teal});
 tx(s,'Lấy trạng thái ở bước cuối của chuỗi cho từng mẫu trong batch.',8.16,4.03,4.52,.82,19);
 tx(s,'Linear tạo logits. Softmax và chọn nhãn nằm trong predict_gesture.',8.16,5.18,4.52,.82,18);
 tx(s,'Đã đối chiếu từng bước trên một clip lưu sẵn: kết quả trùng model(x). Đây là kiểm tra luồng thực thi.',.65,6.56,12.03,.31,15,{color:C.teal});
 s.addNotes('Đọc trực tiếp hai dòng forward và giải thích lần lượt features, sequence, chọn bước cuối, Linear. 64 là chiều trạng thái ẩn, không phải số điểm bàn tay. Softmax được tính sau forward trong predict_gesture. Một clip đã kiểm tra có input [1,30,44], sequence [1,30,64], last [1,64], logits [1,5], khớp model(x).');
}
fs.mkdirSync(work,{recursive:true});
pptx.writeFile({fileName:path.join(work,'improved_sections.pptx')});
