/** Editable research progress deck. Input facts are in verified_metrics.json. */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const root = __dirname;
const out = path.dirname(root);
const M = JSON.parse(fs.readFileSync(path.join(root, 'verified_metrics.json'), 'utf8'));
const C = JSON.parse(fs.readFileSync(path.join(root, 'report_content.json'), 'utf8'));
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = M.author.name;
pptx.subject = 'Báo cáo tiến độ đồ án chuyên ngành — tuần 4';
pptx.title = 'Nhận diện cử chỉ tay động và điều khiển máy tính không chạm';
pptx.company = 'HUTECH — Khoa Công nghệ Thông tin';
pptx.lang = 'vi-VN';
pptx.theme = { headFontFace: 'Arial', bodyFontFace: 'Arial', lang: 'vi-VN' };
const P = { ink:'1A2332', teal:'2D8B8B', mint:'A8DADC', pale:'EFF7F7', gray:'526270', grid:'DDE5E8', white:'FFFFFF', red:'A23D32', pink:'FCEDEA' };
const W=13.333333, H=7.5;
const notes=[], manifest=[];
const labelShort=['Nền','Trái','Phải','Lên','Xuống'];
function text(s,t,x,y,w,h,size=18,opts={}) {
  s.addText(t,{x,y,w,h,fontFace:'Arial',fontSize:size,color:P.ink,margin:0,breakLine:false,
    valign:'top',paraSpaceAfterPt:0,...opts});
}
function rect(s,x,y,w,h,fill=P.pale,line=fill) {
  s.addShape(pptx.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:{color:line,width:.6}});
}
function arrow(s,x1,y1,x2,y2,color=P.teal) {
  s.addShape(pptx.ShapeType.line,{x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1),
    flipH:x2<x1,flipV:y2<y1,line:{color,width:1.7,beginArrowType:'none',endArrowType:'triangle'}});
}
function line(s,x,y,w,color=P.grid){s.addShape(pptx.ShapeType.line,{x,y,w,h:0,line:{color,width:.7}});}
function image(s,name,x,y,w,h,contain=false) {
  const p=path.join(root,'assets',name);
  const b=fs.readFileSync(p);
  const naturalW=b.readUInt32BE(16)/96, naturalH=b.readUInt32BE(20)/96;
  s.addImage({path:p,x,y,w:naturalW,h:naturalH,sizing:{type:contain?'contain':'cover',w,h},altText:name});
}
function base(section,title,source='',dark=false) {
  const s=pptx.addSlide(); s.background={color:dark?P.ink:P.white};
  const n=pptx._slides.length;
  if(title){
    text(s,section.toUpperCase(),.65,.38,11.8,.27,11,{color:dark?P.mint:P.teal,bold:true,charSpacing:1.5});
    text(s,title,.65,.86,12,.63,31,{color:dark?P.white:P.ink,bold:true});
  }
  text(s,source,.65,6.98,11.3,.25,10.3,{color:dark?'B8CAD1':P.gray});
  text(s,String(n).padStart(2,'0')+' / 16',11.9,6.98,.78,.25,10.3,{color:dark?'B8CAD1':P.gray,align:'right'});
  return s;
}
function note(s,title,body,sources=[]) {
  const refText = sources.map(id=>{const r=C.references.find(x=>x.id===id);return `[${id}] ${r.authors}, “${r.title},” ${r.venue}, ${r.year}. ${r.doi?'DOI: '+r.doi+'. ':''}${r.url}\nVị trí bằng chứng: ${r.evidence}`;}).join('\n\n');
  const content=body+(refText?'\n\nTài liệu tham khảo:\n'+refText:'');
  s.addNotes(content);
  notes.push(`## Slide ${notes.length+1}. ${title}\n\n${content}\n`);
  manifest.push({slide:notes.length,title,references:sources,notes:content});
}
function node(s,x,y,w,title,sub,accent=false){
  rect(s,x,y,w,1.05,accent?P.teal:P.pale);
  text(s,title,x+.13,y+.13,w-.26,.32,18,{bold:true,color:accent?P.white:P.ink,align:'center'});
  text(s,sub,x+.12,y+.5,w-.24,.5,13.5,{color:accent?P.white:P.gray,align:'center'});
}
function table(s,headers,rows,{x=.65,y=1.75,w=12.03,colW,rowH=.6,fontSize=16}={}){
  const data=[headers.map(t=>({text:t,options:{bold:true,color:P.white,fill:P.ink}})),
    ...rows.map((r,i)=>r.map(t=>({text:String(t),options:{fill:i%2?P.white:P.pale}})))];
  s.addTable(data,{x,y,w,colW,rowH,autoPage:false,fontFace:'Arial',fontSize,color:P.ink,
    margin:[.09,.11,.07,.11],border:{type:'solid',pt:.6,color:P.white},valign:'middle',
    bold:false,paraSpaceAfterPt:0,verbose:false});
}
function stat(s,x,value,label,accent=P.teal){
  text(s,value,x,1.78,2.75,.7,39,{color:accent,bold:true});
  text(s,label,x,2.5,2.75,.5,16,{color:P.gray});
}
function chartOptions(x,y,w,h,title,extra={}){
  return {x,y,w,h,showTitle:true,title,titleFontFace:'Arial',titleFontSize:16,titleColor:P.ink,
    showLegend:true,legendPos:'b',legendFontFace:'Arial',legendFontSize:13,
    chartColors:[P.teal,'7A98AD','A8DADC'],showValue:true,dataLabelPosition:'outEnd',
    dataLabelColor:P.ink,dataLabelFormatCode:'0',dataLabelBkgrdColor:P.white,dataLabelFormatCodeSourceLinked:false,
    catAxisLabelFontFace:'Arial',catAxisLabelFontSize:14,catAxisLabelColor:P.ink,catAxisLineColor:P.grid,
    valAxisLabelFontFace:'Arial',valAxisLabelFontSize:12,valAxisLabelColor:P.gray,valAxisLineShow:false,
    valGridLine:{color:P.grid,size:.6},catGridLine:{style:'none'},
    chartArea:{fill:{color:P.white},border:{color:P.white,pt:0}},plotArea:{fill:{color:P.white},border:{color:P.white,pt:0}},
    showCatName:false,showSerName:false,showCatAxisTitle:false,showValAxisTitle:true,
    valAxisTitle:'Số clip',valAxisTitleFontFace:'Arial',valAxisTitleFontSize:12,
    ...extra};
}

// 01 — Cover, using a real project frame rather than an invented illustration.
{
 const s=base('','','Rà soát project: 07/11/2026 • Báo cáo online: 08/11/2026, từ 14:00',true);
 image(s,'landmarks.png',8.14,0,5.2,H);
 rect(s,0,0,7.88,6.78,P.ink);
 text(s,'HUTECH  /  ĐỒ ÁN CHUYÊN NGÀNH',.65,.56,6.7,.3,12,{color:P.mint,bold:true,charSpacing:1});
 text(s,'BÁO CÁO TIẾN ĐỘ',.65,1.14,6.7,.58,30,{color:P.white,bold:true});
 text(s,'Nhận diện cử chỉ\ntay động và điều khiển\nmáy tính không chạm',.65,2.04,7.05,2.1,35,{color:P.white,bold:true,breakLine:false});
 text(s,'MediaPipe Hand Landmarker + LSTM',.65,4.43,6.8,.43,19,{color:P.mint});
 text(s,'Trịnh Viết Mỹ  •  2380601382  •  23DTHA3',.65,5.37,7,.34,17,{color:P.white});
 text(s,'GVHD: PGS.TS. Võ Đình Bảy',.65,5.87,7,.34,17,{color:P.white});
 text(s,'Tuần 4  /  02–08/11/2026',.65,6.35,7,.28,13,{color:P.mint});
 note(s,'Trang bìa','Em là Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3. Em xin báo cáo tiến độ tuần 4 của đồ án dưới sự hướng dẫn của PGS.TS. Võ Đình Bảy. Nội dung tập trung vào phương pháp đã triển khai, dữ liệu và kết quả thực tế, lỗi còn tồn tại và kế hoạch đến ngày 20/12. Ảnh trên trang bìa lấy từ clip kiểm tra của chính project. Tên đề tài được diễn đạt theo phạm vi chức năng trong mã nguồn; đối chiếu với tên đã đăng ký trên LMS nếu có khác biệt.');
}
// 02 — Problem and scope.
{
 const s=base('01 / Bài toán','Một webcam, bốn hướng cử chỉ, năm nhãn','Nguồn: README, configs/default.json, src/hand_tracking/app.py và control.py; ảnh clip test.');
 image(s,'cover.png',8.18,1.78,4.5,3.375);
 text(s,'Mục tiêu của nguyên mẫu',.65,1.8,7,.35,21,{bold:true});
 text(s,'Dùng chuyển động bàn tay để chuyển slide và cuộn trang trên máy tính.',.65,2.37,6.8,.86,23);
 const rows=[['Trái / phải','Trang trước / trang tiếp theo'],['Lên / xuống','Cuộn trang'],['Nền','Không phát lệnh']];
 rows.forEach((r,i)=>{const y=3.63+i*.66;line(s,.65,y-.12,6.7);text(s,r[0],.65,y,2.15,.4,18,{bold:true,color:P.teal});text(s,r[1],3.02,y,4.15,.4,18);});
 text(s,'Phạm vi hiện tại',8.18,5.49,4.5,.35,19,{bold:true});
 text(s,'Một bàn tay hợp lệ • RGB 640 × 480\nChạy CPU • Ứng dụng đích cần có focus',8.18,6.0,4.5,.68,16,{color:P.gray});
 note(s,'Bài toán, mục tiêu và phạm vi','Bài toán là nhận diện bốn hướng cử chỉ và phân biệt trạng thái nền trước khi phát lệnh điều khiển. Trong mã nguồn, cử chỉ trái/phải tương ứng phím mũi tên; lên/xuống tương ứng cuộn trang. Phạm vi nguyên mẫu hiện tại dùng webcam RGB, một bàn tay hợp lệ, mô hình CPU. Bộ nhận diện có thể phát hiện tối đa hai bàn tay để loại trường hợp nhiều tay; ứng dụng chỉ chấp nhận đúng một bàn tay. Mục tiêu đánh giá gồm độ đúng trên clip và độ ổn định khi điều khiển liên tục. Độ đúng clip đã có; độ ổn định trực tiếp cần đo thêm. Chưa có dữ liệu thực nghiệm về người dùng chưa xuất hiện trong dữ liệu.');
}
// 03 — Genuine related work, metrics retain their original definitions.
{
 const s=base('02 / Nghiên cứu liên quan','Ba hướng tiếp cận làm cơ sở lựa chọn','Nguồn: [1] Bảng 6, tr. 15; [2] Bảng 1, tr. 8; [3] Bảng 1, tr. PDF 5.');
 table(s,['Công trình','Phương pháp / dữ liệu','Kết quả công bố','Giới hạn và liên hệ'],[
 ['[1] IPN HandS\nBenitez-Garcia và cs.\nApplied Sciences, 2025','Landmark 2D + LSTM\n14 cử chỉ; 50 người;\n5.177 mẫu cử chỉ','Accuracy 91,2 ± 1,4%\nRecall 78,0 ± 1,2%\n3 lần chạy','Cần kiểm soát chất lượng landmark.\nGần với cách biểu diễn đang dùng.'],
 ['[2] SKETCH\nHan và cs.\nNeurIPS, 2025','Chuỗi skeleton → ảnh đồ thị\nViT / Swin\nSHREC 2019 / 2022','SHREC 2019: DR 0,93;\nFP 0,01\nSwin-L + augmentation','Cửa sổ xử lý độc lập còn hạn chế ngữ cảnh.\nGợi ý đánh giá chuỗi liên tục.'],
 ['[3] ConvMixFormer\nGarg, Ghosh, Pradhan\nWACV, 2025','Conv token mixer\nNVGesture / Briareo\nĐánh giá nhiều loại đầu vào','RGB accuracy:\nNVGesture 76,04%\nBriareo 98,26%','Chi phí tính toán cần đo theo phần cứng.\nGợi ý báo cáo cả độ đúng và tốc độ.']
 ],{colW:[2.43,3.23,2.67,3.7],rowH:[.65,1.23,1.23,1.23],fontSize:15.2});
 text(s,'Khác bộ dữ liệu và giao thức: các chỉ số này không dùng để xếp hạng trực tiếp với kết quả 80% của đồ án.',.65,6.34,12,.44,15,{color:P.red});
 note(s,'Nghiên cứu liên quan','Ba công trình đã được đọc từ PDF gốc trong reference và đối chiếu thông tin xuất bản. IPN HandS là hướng gần nhất: bộ dữ liệu có 14 cử chỉ và 50 người; LSTM 3 tầng 256 nút ẩn trên 42 tọa độ xy. Kết quả được lấy đúng từ Bảng 6: accuracy 91,2 ± 1,4%, average recall 78,0 ± 1,2% qua ba lần chạy; không dùng con số diễn giải dễ gây nhầm trong abstract. Ưu điểm là chú trọng chất lượng và sửa landmark; cấu hình và dữ liệu lớn hơn đồ án nên không so sánh trực tiếp.\n\nSKETCH biểu diễn chuyển động skeleton thành ảnh đồ thị rồi dùng ViT/Swin. Bảng 1, SHREC 2019, Swin-L + Augmentation có detection rate 0,93 và false positive 0,01. DR không phải accuracy. Tác giả nêu hạn chế các cửa sổ xử lý độc lập chưa tận dụng đầy đủ ngữ cảnh trước đó.\n\nConvMixFormer thay attention bằng bộ trộn tích chập và dùng gated feed-forward. RGB accuracy trong Bảng 1 là 76,04% trên NVGesture và 98,26% trên Briareo; mô hình 13,57 triệu tham số trong Bảng 6. Đây là bài toán và đầu vào khác với landmark + LSTM của đồ án. Điểm học hỏi là báo cáo chi phí tính toán cùng độ chính xác. Các DOI và URL đầy đủ có trong references.md và phần ghi chú này.',[1,2,3]);
}
// 04 — Read one primary paper closely, then compare it with the current implementation.
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
// 05 — Native editable architecture.
{
 const s=base('03 / Phương pháp','Luồng xử lý từ webcam đến lệnh điều khiển','Nguồn: camera.py, landmarks.py, features.py, model.py, app.py, control.py; cấu hình hiện tại.');
 const xs=[.65,3.84,7.03,10.22], nw=2.46, yt=2.02,yb=4.2;
 node(s,xs[0],yt,nw,'Webcam RGB','640 × 480; ảnh lật gương');
 node(s,xs[1],yt,nw,'MediaPipe','21 điểm; đúng 1 bàn tay');
 node(s,xs[2],yt,nw,'Đặc trưng','42 tọa độ + 2 cổ tay');
 node(s,xs[3],yt,nw,'Bộ đệm chuỗi','30 × 44; lấy mẫu 20 Hz');
 for(let i=0;i<3;i++)arrow(s,xs[i]+nw+.06,yt+.52,xs[i+1]-.08,yt+.52);
 arrow(s,xs[3]+nw/2,yt+1.11,xs[3]+nw/2,yb-.08);
 node(s,xs[3],yb,nw,'LSTM → 5 nhãn','1 tầng; hidden size = 64',true);
 node(s,xs[2],yb,nw,'Xác nhận lệnh','p ≥ 0,8; ≥ 150 ms; ≥ 3 lần');
 node(s,xs[1],yb,nw,'Gửi lệnh','Phím trái/phải; cuộn trang');
 arrow(s,xs[3]-.08,yb+.52,xs[2]+nw+.06,yb+.52);
 arrow(s,xs[2]-.08,yb+.52,xs[1]+nw+.06,yb+.52);
 text(s,'F8: bật / tạm dừng\nF9: dừng',.65,4.28,2.5,.95,18,{color:P.teal,bold:true});
 text(s,'Chống lặp: nghỉ 1.000 ms và xác nhận nền 300 ms. Điều khiển mặc định tắt khi khởi động.',.65,6.12,12,.58,18);
 note(s,'Kiến trúc tổng thể','Webcam cung cấp ảnh RGB kích thước cấu hình 640×480 và lật gương đúng một lần. MediaPipe Hand Landmarker chạy VIDEO, trả 21 điểm mỗi bàn tay; cấu hình num_hands=2 nhằm nhận biết trường hợp có nhiều tay, nhưng hệ thống chỉ chấp nhận đúng một tay. features.py chuẩn hóa tọa độ theo cổ tay và kích thước lòng bàn tay, rồi nối vị trí cổ tay thành 44 đặc trưng. Bộ đệm tạo chuỗi 30 mẫu ở nhịp 20 Hz. LSTM trả logits của năm nhãn. Bộ điều khiển dùng ngưỡng 0,8, thời gian ổn định tối thiểu 150 ms và tối thiểu ba dự đoán mới; cooldown 1.000 ms, xác nhận nền 300 ms. F8 bật hoặc tạm dừng, F9 dừng toàn cục. Các điều kiện này đã có trong mã nguồn và test tự động; chưa thể xem là kết quả thử thành công trong môi trường thực tế.',[4,5,6,7]);
}
// 06 — Actual frames and preprocessing.
{
 const s=base('03 / Dữ liệu và tiền xử lý','Giữ hình dạng bàn tay và vị trí cổ tay theo thời gian','Nguồn: ba khung hình từ clip train SWIPE_LEFT; features.py và collection.py.');
 [150,750,1250].forEach((t,i)=>{image(s,`train-left-${i+1}.png`,.65+i*3.0,1.78,2.7,2.025);text(s,`${t} ms`,.65+i*3.0,3.95,2.7,.3,15,{align:'center',color:P.gray});});
 text(s,'Một chuỗi\n30 × 44',10.03,2.05,2.65,1.05,27,{bold:true,color:P.teal});
 text(s,'Ảnh minh họa lấy trực tiếp\ntừ video đã thu.',10.03,3.26,2.65,.66,16,{color:P.gray});
 const p=[['01','Chuẩn hóa 21 điểm xy','Trừ cổ tay; chia theo kích thước lòng bàn tay.'],['02','Nối vị trí cổ tay','42 giá trị cục bộ + 2 giá trị vị trí = 44.'],['03','Lưu chuỗi và thông tin','Video gốc + NPZ + nhãn, tập và mã phiên.']];
 p.forEach((r,i)=>{const x=.65+i*4.12;text(s,r[0],x,4.63,.5,.4,24,{bold:true,color:P.teal});text(s,r[1],x+.65,4.65,3.28,.42,18,{bold:true});text(s,r[2],x,5.3,3.75,.75,17);});
 text(s,'Lấy mẫu 20 Hz là cấu hình; FPS thực tế chưa được đo. Mất tay hoặc khoảng trống > 100 ms sẽ xóa chuỗi.',.65,6.38,12,.38,15,{color:P.gray});
 note(s,'Pipeline thu thập và tiền xử lý','Ba ảnh là các khung tại 150, 750 và 1.250 ms của một clip train nhãn SWIPE_LEFT, được trích từ video thật, không tạo ảnh giả. Với ảnh W×H, trước hết q = p×[W,H]/max(W,H). Lấy cổ tay q0 làm gốc và scale bằng trung vị khoảng cách từ q0 tới các mốc 5,9,13,17. Đặc trưng cục bộ là (q−q0)/scale, gồm 42 giá trị xy; nối thêm q0 gồm hai giá trị để giữ chuyển động tuyệt đối của cổ tay. SequenceBuffer lấy mẫu theo timestamp mỗi 50 ms và chỉ nội suy khi đã biết cả hai đầu mút. Mất tay, nhiều tay hoặc khoảng trống lớn hơn 100 ms sẽ xóa chuỗi. Từ mẫu đầu tới mẫu cuối là 29/20=1,45 giây, xấp xỉ cửa sổ 1,5 giây. Cấu hình 20 Hz không phải kết quả đo FPS. Video gốc, NPZ, manifest và thông tin phiên cho phép kiểm tra lại nhãn.');
}
// 07 — Editable dataset chart with exact class counts.
{
 const s=base('04 / Dataset','250 clip cân bằng giữa năm nhãn','Nguồn: data/manifest.csv và NPZ; load_split, dataset-check; verified_metrics.json.');
 s.addChart(pptx.ChartType.bar,[{name:'Train',labels:labelShort,values:[30,30,30,30,30]},{name:'Validation',labels:labelShort,values:[10,10,10,10,10]},{name:'Test',labels:labelShort,values:[10,10,10,10,10]}],
   chartOptions(.65,1.69,8.03,4.81,'Số clip theo nhãn và tập dữ liệu',{barDir:'col',barGrouping:'clustered',barGapWidthPct:90,valAxisMinVal:0,valAxisMaxVal:35,valAxisMajorUnit:10,showCatAxisTitle:true,catAxisTitle:'Nhãn cử chỉ',catAxisTitleFontSize:12}));
 text(s,'150 / 50 / 50',9.14,1.95,3.54,.61,32,{color:P.teal,bold:true});
 text(s,'Train / Validation / Test\nTỷ lệ 60% / 20% / 20%',9.14,2.72,3.54,.82,18);
 line(s,9.14,3.84,3.54);
 text(s,'Chia theo phiên thu',9.14,4.1,3.54,.38,20,{bold:true});
 text(s,'Train: pilot_01, train_02\nValidation: val_01\nTest: test_01',9.14,4.7,3.54,1.1,17,{color:P.gray});
 text(s,'Không có chuỗi đặc trưng trùng tuyệt đối giữa các tập. Chưa có đánh giá trên người chưa xuất hiện trong dữ liệu.',.65,6.49,12.03,.38,14.5,{color:P.gray});
 note(s,'Dữ liệu và phân chia','Tất cả 250 clip có tệp tương ứng và chuỗi đúng kích thước. Mỗi lớp có 50 clip: 30 train, 10 validation và 10 test. Tổng train150, validation50, test50, tỷ lệ 60/20/20. Train thuộc pilot_01 và train_02; validation là val_01; test là test_01. Kiểm tra băm nội dung feature không thấy chuỗi giống tuyệt đối xuyên tập; kết quả này không chứng minh các mẫu độc lập theo người dùng. Manifest không có subject_id để chứng minh giao thức giữ người riêng. Các phiên thu riêng giúp kiểm soát nguồn mẫu, nhưng không được gọi là thử trên người chưa thấy. Phân bố hiện tại cân bằng, vì vậy không nêu mất cân bằng lớp như một lỗi đã xảy ra.');
}
// 08 — Explain actual functions and tensor shapes before discussing extensions.
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
// 09 — Native training chart from the stored notebook log.
{
 const s=base('05 / Huấn luyện','Loss giảm; checkpoint được chọn ở epoch 23','Nguồn: stdout đã lưu trong notebook, trích thành slide_sources/training_history.csv; 30 epoch.');
 const h=M.training_history;
 s.addChart(pptx.ChartType.line,[{name:'Training loss',labels:h.map(x=>String(x.epoch)),values:h.map(x=>x.train_loss)},{name:'Validation loss',labels:h.map(x=>String(x.epoch)),values:h.map(x=>x.validation_loss)}],
   chartOptions(.65,1.71,8.22,4.95,'Loss theo epoch',{showValue:false,lineSize:2.5,lineDataSymbol:'none',showCatAxisTitle:true,catAxisTitle:'Epoch',catAxisTitleFontSize:12,catAxisLabelFontSize:10,catAxisLabelFrequency:'5',valAxisTitle:'Cross-entropy loss',valAxisMinVal:0,valAxisMaxVal:1.6,valAxisMajorUnit:.4,valAxisLabelFormatCode:'0.0'}));
 text(s,'Epoch 23',9.3,1.98,3.38,.52,28,{bold:true,color:P.teal});
 text(s,'Validation loss thấp nhất\n0,1085',9.3,2.8,3.38,1.03,22);
 text(s,'Validation accuracy\n94% tại checkpoint',9.3,4.17,3.38,.94,21);
 text(s,'Một lần chạy đã có log.\nChưa có thống kê nhiều seed.',9.3,5.57,3.38,.85,17,{color:P.gray});
 note(s,'Đường cong huấn luyện','Đồ thị lấy toàn bộ 30 epoch từ stdout lưu trong notebook, không tạo dữ liệu giả và không nối từ hai lần chạy khác nhau. Train loss từ1,5541 xuống0,1293; validation loss từ1,4313 xuống0,1720 ở epoch30. Checkpoint tốt nhất là epoch23 với validation loss đầy đủ0,1085219458 và accuracy0,94. Các giá trị trên đường cong có độ chính xác bốn chữ số thập phân theo log. Validation có dao động; chỉ từ một lần chạy và độ chênh validation/test không đủ kết luận nguyên nhân duy nhất là overfitting. Notebook ghi5,0giây cho một lần huấn luyện; đây không phải latency suy luận hoặc benchmark nhiều lần. Bước sau là cố định giao thức rồi so sánh nhiều seed nếu còn thời gian.');
}
// 10 — Native table and macro metrics.
{
 const s=base('06 / Đánh giá trên clip','40/50 clip đúng; Macro-F1 đạt 0,7619','Nguồn: tái đánh giá checkpoint hiện có; khớp outputs/evaluation.json. P/R/F1 trong bảng làm tròn 3 chữ số.');
 stat(s,.65,'80%','Accuracy — 40/50 clip');stat(s,3.82,'0,800','Macro-Precision');stat(s,6.99,'0,800','Macro-Recall');stat(s,10.16,'0,7619','Macro-F1');
 const keys=Object.keys(M.test.per_class);
 const f=n=>n.toFixed(3).replace('.',',');
 table(s,['Nhãn','Precision','Recall','F1-score','Số clip'],keys.map((k,i)=>{const v=M.test.per_class[k];return[labelShort[i],f(v.precision),f(v.recall),f(v.f1),v.support];}),
 {y:3.23,colW:[3.63,2.1,2.1,2.1,2.1],rowH:.48,fontSize:17});
 text(s,'Điểm yếu tập trung ở hai hướng dọc: vuốt lên chỉ đúng 1/10; cần xem từng lỗi trước khi thu bù hoặc sửa mô hình.',.65,6.4,12.03,.46,17,{color:P.red});
 note(s,'Kết quả đánh giá','Tôi đã nạp checkpoint hiện tại và chạy lại 50 chuỗi test trong bộ nhớ; accuracy, confusion matrix và các chỉ số khớp tệp outputs/evaluation.json. Accuracy40/50=80%. Macro-Precision và Macro-Recall đều0,8; Macro-F1 là0,7619047619. Macro-F1 là trung bình F1 từng lớp, không phải F1 tính trực tiếp từ macroP và macroR. BACKGROUND,LEFT,RIGHT đều đúng10/10 trong bộ nhỏ hiện tại; không suy rộng thành hoàn hảo trong sử dụng thực tế. UP cóP0,5,R0,1,F1≈0,1667; DOWN cóP0,5,R0,9,F1≈0,6429. Mỗi lớp support10 nên một clip tương ứng10 điểm phần trăm recall của lớp. Kết quả phản ánh thử trên clip đã lưu, chưa phản ánh đầy đủ điều khiển liên tục.');
}
// 11 — Fully editable confusion matrix.
{
 const s=base('06 / Phân tích lỗi','9/10 clip vuốt lên bị nhận thành vuốt xuống','Nguồn: confusion matrix tái lập từ models/gesture_lstm.pt; ảnh clip test UP bị dự đoán DOWN.');
 const x=1.82,y=2.36,cw=1.0,ch=.66;
 text(s,'Nhãn dự đoán',x,y-.67,5,.32,17,{bold:true,align:'center'});
 text(s,'Thực tế',.65,1.91,1.0,.31,15,{bold:true});
 labelShort.forEach((l,i)=>{text(s,l,x+i*cw,y-.34,cw,.28,14.5,{align:'center'});text(s,l,.65,y+i*ch+.17,1.0,.28,15);});
 M.test.confusion_matrix.forEach((r,i)=>r.forEach((v,j)=>{
   const color=v===0?'F2F5F6':i===j?(v>=8?P.teal:'C7E4E1'):v===9?P.red:'F5C8C1';
   rect(s,x+j*cw,y+i*ch,cw-.025,ch-.025,color);
   text(s,String(v),x+j*cw,y+i*ch+.16,cw-.025,.36,21,{align:'center',bold:v>0,color:v>=9?P.white:P.ink});
 }));
 text(s,'Đơn vị: số clip • Mỗi hàng có 10 clip',.65,6.03,6.7,.3,14,{color:P.gray});
 image(s,'up-2.png',7.77,1.94,4.9,3.675);
 text(s,'Nhãn thật: LÊN → Dự đoán: XUỐNG',7.77,5.81,4.9,.37,18,{bold:true,color:P.red});
 text(s,'Lỗi còn lại: 1 clip XUỐNG → LÊN.\nƯu tiên xem lại quy cách động tác và mẫu lỗi.',7.77,6.3,4.9,.54,15);
 note(s,'Confusion matrix và mẫu lỗi','Ma trận có hàng là nhãn thật, cột là nhãn dự đoán, đơn vị là clip. Ba lớp đầu mỗi lớp10/10 đúng. Trong10clip UP chỉ1đúng,9bị nhận DOWN. Trong10clip DOWN có9đúng,1bị nhận UP. Ảnh bên phải trích từ test/SWIPE_UP/test_01_3bd55bb323444226a3d8c37cdf1a2f92.avi; dự đoán toàn chuỗi là DOWN với độ tin cậy khoảng0,965. Dự đoán sai có độ tin cậy cao cho thấy chỉ tăng ngưỡng không nhất thiết sửa được lỗi này. Quan sát một số video cho thấy tư thế ngón tay khác nhau theo nhãn trong khi mô tả cử chỉ yêu cầu vuốt lòng bàn tay mở. Đây là dấu hiệu cần đối chiếu quy cách và phân tích thêm, chưa chứng minh nguyên nhân mô hình học tư thế thay vì chuyển động.');
}
// 12 — Embedded evidence video, explicitly offline playback.
{
 const s=base('06 / Demo và kiểm thử','Phát lại năm clip test với dự đoán của mô hình','Nguồn: video 10 giây dựng từ clip test thật; slide_sources/assets/demo_test.mp4; unit_tests.txt.');
 const poster='data:image/png;base64,'+fs.readFileSync(path.join(root,'assets','video-poster.png')).toString('base64');
 s.addMedia({type:'video',path:path.join(root,'assets','demo_test.mp4'),cover:poster,x:.65,y:1.72,w:5.07,h:4.68975});
 text(s,'Bấm video khi trình chiếu PowerPoint',.65,6.54,5.07,.27,13,{color:P.gray,align:'center'});
 text(s,'60 test tự động đã qua',6.31,1.8,6.37,.48,25,{bold:true,color:P.teal});
 text(s,'Kiểm tra logic bằng dữ liệu và mô phỏng; video có cả trường hợp UP bị nhận sai.',6.31,2.51,6.1,.9,20);
 text(s,'Chưa có dữ liệu thực nghiệm',6.31,3.79,6.1,.39,21,{bold:true,color:P.red});
 text(s,'40 lượt thao tác trực tiếp\n5 phút nền để đếm lệnh ngoài ý muốn\nFPS toàn hệ thống và độ trễ đến lệnh',6.31,4.4,6.1,1.36,19,{paraSpaceAfterPt:10});
 text(s,'Bước tiếp: ghi CSV từng lượt, log sự kiện và điều kiện chạy.',6.31,6.19,6.1,.59,17,{color:P.gray});
 note(s,'Demo và giới hạn kiểm thử','Bấm video trong chế độ Slide Show. Video dài10giây, phát lại5clip test đã lưu và dự đoán từ checkpoint, có một clip UP nhận sai DOWN để thể hiện giới hạn hiện tại. Đây không phải bản ghi webcam đang điều khiển ứng dụng khác. Bản PDF chỉ hiển thị ảnh bìa của video; fileMP4 được cung cấp trong slide_sources/assets. Bộ60test tự động đã chạy qua trong15,998giây; test sử dụng dữ liệu/mô phỏng cho các ranh giới phần cứng và điều khiển, chưa thay thế phép thử trực tiếp. Chưa có dữ liệu thực nghiệm cho40lượt cử chỉ,5phút nền, latency suy luận ổn định và FPS toàn hệ thống. Cần10lượt mỗi hướng, ghi đúng/sai/bỏ sót/lặp và timestamp từ động tác tới lệnh. Đo idle5phút để đếm lệnh không mong muốn; báo cáo điều kiện ánh sáng, khoảng cách, phần cứng và cấu hình.');
}
// 13 — Evidence-based implementation status.
{
 const s=base('07 / Tiến độ thực tế','Các phần đã triển khai và phần còn phải đo','Nguồn: mã nguồn, manifest, notebook, checkpoint, evaluation.json và bộ 60 test; rà soát 07/11/2026.');
 table(s,['Hạng mục','Trạng thái thực tế','Minh chứng','Còn cần làm'],[
 ['Tài liệu','Đã đối chiếu','6 PDF; phân tích sâu [1]–[3]','Chưa tái lập benchmark'],
 ['Thu dữ liệu','250 clip hợp lệ','Video + NPZ + manifest','Chốt quy cách cử chỉ'],
 ['Tiền xử lý','Đã triển khai / kiểm tra','44 đặc trưng; chuỗi 30 mẫu','Đo ảnh hưởng đặc trưng'],
 ['Mô hình','Đã có mã và checkpoint','LSTM 64 → 5; 28.485 tham số','Thêm mô hình đối chứng'],
 ['Huấn luyện','Có log 30 epoch','Notebook; chọn epoch 23','Chưa thống kê nhiều seed'],
 ['Đánh giá clip','Đã đo 50 clip test','40/50 đúng; Macro-F1 0,7619','Sửa nhầm lên / xuống'],
 ['Tích hợp','Đã có mã nguồn','app.py; control.py; F8 / F9','Đo điều khiển trực tiếp'],
 ['Kiểm thử','60 test đã qua','unit_tests.txt; video clip test','40 lượt + 5 phút nền chưa đo']
 ],{colW:[1.77,2.8,4.16,3.3],rowH:.51,fontSize:14.2});
 text(s,'Không quy đổi thành % hoàn thành khi chưa có bộ tiêu chí và trọng số được thống nhất.',.65,6.58,12,.3,14,{color:P.gray});
 note(s,'Bảng tiến độ','Bảng tiến độ ghi theo hiện trạng kiểm chứng được ngày07/11. Dữ liệu và mô hình đã vượt giai đoạn chỉ cài webcam: đã có250clip, train, checkpoint, kết quả test và ứng dụng điều khiển. Tuy nhiên cần phân biệt có mã nguồn với kết quả đo trực tiếp. Mô tả cũ trong một số README/ROADMAP còn ghi train/run/control chưa hoàn thành; báo cáo này dựa trên mã và artifact thực tế. Không đưa phần trăm hoàn thành vì chưa có tiêu chí và trọng số thống nhất.\n\nBảng chi tiết:\n'+C.progress.map(r=>r.join(' | ')).join('\n'));
}
// 14 — Evidence, hypotheses and next verification.
{
 const s=base('08 / Khó khăn và hạn chế','Sửa lỗi có bằng chứng, rồi đo lại bằng giao thức rõ ràng','Nguồn: confusion matrix, mẫu video, manifest và danh mục phép thử còn thiếu.');
 table(s,['Bằng chứng hiện tại','Việc cần làm','Cách kiểm chứng'],[
 ['Lên đúng 1/10; 9 clip thành xuống.\nTư thế ngón tay khác nhau trong một số mẫu.','Đối chiếu video với quy cách; chốt cách vuốt; thu bù train/validation khi cần.','So sánh recall lên/xuống; kiểm tra mẫu lỗi. Không dùng test để chọn checkpoint.'],
 ['Validation 94%; test 80%.\nMới có một lần chạy và ít mẫu.','Giữ phiên test cuối riêng; ghi mã phiên, cấu hình, seed.','Đánh giá sau khi khóa mô hình; báo số mẫu và độ biến động nếu chạy nhiều seed.'],
 ['Chưa đo thời gian thực và lệnh ngoài ý muốn.','Đo 40 lượt; 5 phút nền; ghi FPS và timestamp từng phần.','Báo đúng/sai/bỏ sót/lặp, FPS và độ trễ trong cùng điều kiện.']
 ],{colW:[4.02,4.01,4.0],rowH:[.6,1.25,1.25,1.25],fontSize:16.5});
 text(s,'Khả năng tổng quát hóa sang người khác: Chưa có dữ liệu thực nghiệm. Nguyên nhân lỗi lên/xuống vẫn là giả thuyết cần kiểm tra.',.65,6.3,12.03,.59,16,{color:P.red});
 note(s,'Khó khăn và biện pháp','Vấn đề đã đo được là lỗi lên/xuống và chênh14điểm phần trăm giữa validation94% và test80%. Quan sát tư thế ngón tay khác nhau chỉ là dấu hiệu dữ liệu cần xem xét, chưa chứng minh nguyên nhân. Cần chốt định nghĩa cử chỉ với GVHD, kiểm tra nhãn và cách thu rồi bổ sung dữ liệu đúng quy cách. Do đã xem nhiều lần tập test hiện tại, tập này chỉ nên xem là bộ chẩn đoán phát triển; trước đánh giá cuối nên thu một phiên giữ riêng sau khi khóa cấu hình.\n\nChưa có dữ liệu thực nghiệm về độ trễ, FPS, điều khiển40lượt,5phút tay nghỉ và người chưa thấy. Không khẳng định CPU yếu, overfitting hoặc hệ thống thời gian thực ổn định khi chưa đo. Phương án đo là ghi thời gian từng khối, số frame xử lý trên thời gian tường, thời gian từ cử chỉ tới lệnh, số đúng/sai/bỏ sót/lặp và false command trên5phút. Nếu nhầm nhiều, ưu tiên sửa quy cách/dữ liệu trước khi tăng độ phức tạp mô hình.');
}
// 15 — Remaining weeks, concrete actions and acceptance outputs.
{
 const s=base('09 / Kế hoạch','Sáu tuần còn lại: hoàn thiện phần lõi trước ngày 20/12','Lịch học phần do sinh viên cung cấp: thực hiện 12/10–20/12; nộp LMS 21–27/12/2026.');
 table(s,['Tuần / thời gian','Công việc chính','Đầu ra và điều kiện hoàn thành'],[
 ['5 • 09–15/11','Đọc sâu bài [1]; đối chiếu code','Phiếu đọc báo + sơ đồ code + quy cách cử chỉ; phân tích lỗi dọc'],
 ['6 • 16–22/11','Thử 40 lượt; 5 phút nền; đo tốc độ','CSV đủ 40 lượt; log đủ 5 phút; có cách đo FPS / độ trễ'],
 ['7 • 23–29/11','Sửa lệnh lặp; thử mất tay, hai tay, F8/F9','Checklist có kết quả; mất tay không lệnh; mỗi vuốt tối đa một lệnh'],
 ['8 • 30/11–06/12','Khóa mô hình; đánh giá phiên giữ lại','Checkpoint cuối + metric + confusion matrix + video demo'],
 ['9 • 07–13/12','Viết báo cáo; gửi GVHD; hẹn ký phiếu','Bản đầy đủ; số liệu khớp tệp gốc; nhật ký đủ các tuần'],
 ['10 • 14–20/12','Sửa góp ý; thử máy demo; lấy chữ ký','Hồ sơ mở được; scan rõ chữ ký; sao lưu; sẵn sàng nộp LMS']
 ],{colW:[2.05,4.05,5.93],rowH:.62,fontSize:15.2});
 text(s,'Hằng tuần: ghi đúng kết quả vào nhật ký, báo GVHD và nộp LMS. Đợt nộp cuối: 21–27/12; kiểm tra giờ đóng trên LMS.',.65,6.48,12.03,.4,14.5,{color:P.teal,bold:true});
 note(s,'Kế hoạch sáu tuần còn lại','Buổi báo cáo hiện tại ở cuối tuần4, nên phần còn lại là tuần5–10. Không lặp lại kế hoạch bảy tuần dành cho thời điểm cuối tuần3. Kế hoạch ưu tiên giải quyết lỗi lớp dọc, đo sử dụng trực tiếp, sửa ổn định rồi mới khóa đánh giá và hoàn thiện hồ sơ. Các mốc sau là kế hoạch, không phải kết quả đã đạt.\n\n'+C.plan.map(p=>`Tuần ${p.week} (${p.dates}/2026)\nMục tiêu: ${p.goal}\nCông việc: ${p.work}\nĐầu ra: ${p.output}\nNghiệm thu: ${p.acceptance}\nRủi ro: ${p.risk}\nDự phòng: ${p.backup}`).join('\n\n')+'\n\nHọc phần kết thúc giai đoạn thực hiện20/12. Nộp báo cáo LMS21–27/12, kèm scan phiếu tiến độ có chữ ký GVHD; cần gặp GVHD ký bảng điểm. Chưa biết giờ đóng LMS và lịch bảo vệ cá nhân. Khung chấm/bảo vệ28/12/2026–10/01/2027.');
}
// 16 — Clear conclusion and actual bibliography.
{
 const s=base('10 / Kết luận','Hiểu bài báo và code trước khi mở rộng','Các nguồn đầy đủ, DOI, liên kết gốc và vị trí bảng: references.md • Ghi chú: speaker_notes.md',true);
 const stats=[['250','clip hợp lệ'],['30','epoch có log'],['80%','accuracy trên 50 clip test']];
 stats.forEach((r,i)=>{const x=.65+i*4.12;text(s,r[0],x,1.89,3.7,.84,48,{color:P.mint,bold:true});text(s,r[1],x,2.86,3.7,.45,18,{color:P.white});});
 text(s,'Việc ưu tiên ngay sau buổi báo cáo',.65,3.77,12,.42,23,{bold:true,color:P.white});
 text(s,'Đọc sâu IPN HandS → giải thích code → kiểm chứng lỗi lên/xuống.',.65,4.41,12,.76,24,{color:P.white});
 line(s,.65,5.62,12,'506575');
 text(s,'Tài liệu chính',.65,5.89,2.1,.4,16,{bold:true,color:P.mint});
 text(s,'[1] Benitez-Garcia và cs., IPN HandS, Applied Sciences, 2025.\n[2] Han và cs., Doodle to Detect (SKETCH), NeurIPS, 2025.\n[3] Garg, Ghosh, Pradhan, ConvMixFormer, WACV, 2025.',3.03,5.83,9.65,.96,14,{color:P.white});
 note(s,'Kết luận và tài liệu tham khảo','Theo góp ý tuần 2, thứ tự ưu tiên là đọc hiểu bài báo, giải thích được code và phép thử hiện có, rồi mới mở rộng. Chưa có minh chứng tái lập mã LSTM của bài báo. Kết quả đạt được là một pipeline có mã nguồn từ webcam tới bộ phát lệnh,250clip hợp lệ, mô hình LSTM có checkpoint, log30epoch và đánh giá trên50clip cho accuracy80%, Macro-F1≈0,7619. Bộ60test tự động đã qua. Phần chưa đáp ứng đủ mục tiêu là phân biệt lên/xuống và bằng chứng đo điều khiển trực tiếp. Vì vậy, ưu tiên tiếp theo là thống nhất quy cách động tác, sửa lỗi dữ liệu/mô hình theo validation rồi đo40lượt,5phút nền và tốc độ. Em xin ý kiến GVHD về quy cách cử chỉ và tiêu chí nghiệm thu của nguyên mẫu. Các nghiên cứu là cơ sở lựa chọn và đánh giá, chưa dùng để khẳng định kiến trúc có tính mới.',[1,2,3,4,5,6,7]);
}

fs.writeFileSync(path.join(out,'speaker_notes.md'),
 '# Ghi chú thuyết trình — báo cáo tiến độ tuần 4\n\n'+
 '**Sinh viên:** Trịnh Viết Mỹ — 2380601382 — 23DTHA3.  \n**GVHD:** PGS.TS. Võ Đình Bảy.  \n**Buổi báo cáo:** 08/11/2026 từ 14:00, online.\n\n'+
 'Gợi ý trình bày khoảng 12–15 phút, điều chỉnh theo thời lượng GVHD cho phép. Các phần “kế hoạch” là việc dự kiến. Video là phát lại clip đã lưu.\n\n'+notes.join('\n')+
 '\n## Câu hỏi dễ gặp\n\n**Vì sao accuracy 80% mà Macro-F1 thấp hơn?** Hai lớp lên/xuống có precision và recall lệch nhau; Macro-F1 lấy trung bình F1 của từng lớp.\n\n**Có chạy thời gian thực ổn định không?** Đã có mã chạy webcam và điều khiển; Chưa có dữ liệu thực nghiệm về FPS và độ trễ toàn hệ thống.\n\n**Tại sao không đổi ngay sang Transformer?** Cần xử lý quy cách dữ liệu và giao thức đánh giá trước; chưa có thử nghiệm đối chứng chứng minh mô hình phức tạp hơn giải quyết lỗi.\n\n**Có chứng minh dùng tốt với người khác không?** Chưa có dữ liệu thực nghiệm. Chia phiên chưa đủ chứng minh chia theo người.\n\n**Số liệu có được tạo thêm để đẹp biểu đồ không?** Không. Đường loss lấy 30 dòng stdout notebook; metric và confusion matrix được tái lập từ checkpoint; chi tiết trong verified_metrics.json và qa_report.md.\n', 'utf8');
fs.writeFileSync(path.join(root,'slides_manifest.json'),JSON.stringify(manifest,null,2),'utf8');
fs.writeFileSync(path.join(root,'design_tokens.json'),JSON.stringify({theme:C.theme,palette:P,layout:'LAYOUT_WIDE',width:W,height:H,font:'Arial',titlePt:31,bodyPt:'17–24',tablePt:'14.2–17',sourcePt:10.3},null,2),'utf8');
pptx.writeFile({fileName:path.join(out,'Bao_Cao_Tien_Do.pptx')});
