"""Apply three new sections to the user's 15-slide deck after add_slide.py registration.

Writes a candidate only. Original PowerPoint, media, charts and edited cover are preserved.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from hashlib import sha256
import json
import posixpath
import re
from lxml import etree as E

S=Path(__file__).resolve().parent
W=S/'qa/cai_thien_2026-11-08'
R=next(p for p in S.parents if (p/'pyproject.toml').is_file() and (p/'src/hand_tracking').is_dir())
meta=json.loads((W/'revision_input.json').read_text(encoding='utf-8'))
C=json.loads((S/'report_content.json').read_text(encoding='utf-8'))
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rel':'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct':'http://schemas.openxmlformats.org/package/2006/content-types'}

def read_zip(p):
    with ZipFile(p) as z:return {n:z.read(n) for n in z.namelist()}
def xml(data):return E.fromstring(data)
def encode(root):return E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
def notes_body(root):
    for shape in root.findall('.//p:sp',NS):
        ph=shape.find('.//p:ph',NS)
        if ph is not None and ph.get('type')=='body':return shape.find('p:txBody',NS)
    raise ValueError('Missing body notes placeholder')
def set_notes(root,body,page):
    target=notes_body(root)
    for p in list(target.findall('a:p',NS)):target.remove(p)
    for line in body.split('\n'):
        p=E.SubElement(target,'{'+NS['a']+'}p')
        if line:
            run=E.SubElement(p,'{'+NS['a']+'}r')
            rp=E.SubElement(run,'{'+NS['a']+'}rPr',lang='vi-VN',sz='1200')
            E.SubElement(rp,'{'+NS['a']+'}latin',typeface='Arial')
            E.SubElement(run,'{'+NS['a']+'}t').text=line
    for field in root.findall('.//a:fld',NS):
        if field.get('type')=='slidenum':
            for t in field.findall('a:t',NS):t.text=str(page)

original=read_zip(R/meta['input_deck'])
parts=read_zip(W/'structured_16.pptx')
sections=read_zip(W/'improved_sections.pptx')
# Structure was already registered with the skill's add_slide.py, before content edits.
pres=xml(parts['ppt/presentation.xml'])
rels=xml(parts['ppt/_rels/presentation.xml.rels'])
targets={r.get('Id'):r.get('Target') for r in rels}
order=[posixpath.normpath(posixpath.join('ppt',targets[s.get('{'+NS['r']+'}id')]))
       for s in pres.findall('./p:sldIdLst/p:sldId',NS)]
assert len(order)==16 and order[4]=='ppt/slides/slide16.xml',order
changed={'ppt/slides/slide4.xml':'ppt/slides/slide1.xml',
         'ppt/slides/slide16.xml':'ppt/slides/slide2.xml',
         'ppt/slides/slide8.xml':'ppt/slides/slide3.xml'}
for target,source in changed.items():
    root=xml(parts[target]);new=xml(sections[source])
    root.replace(root.find('p:cSld',NS),deepcopy(new.find('p:cSld',NS)))
    parts[target]=encode(root)

speeches=[
('Mở đầu', '''Em là Trịnh Viết Mỹ, MSSV 2380601382, lớp 23DTHA3. Em xin báo cáo tiến độ tuần 4 của đề tài nhận diện cử chỉ tay động và điều khiển máy tính không chạm, dưới sự hướng dẫn của PGS.TS. Võ Đình Bảy.

Theo góp ý của thầy ở tuần 2, em trình bày công trình nghiên cứu có liên quan, giải thích phương pháp và đối chiếu với code hiện tại. Sau đó là dữ liệu, kết quả và giới hạn đã ghi nhận. Bài báo cáo tập trung vào phần đã làm và đã kiểm tra trong lần báo cáo này.''',[]),
('Bài toán và phạm vi', '''Hệ thống dùng webcam RGB để nhận biết bốn hướng cử chỉ và một lớp nền. Trái/phải dùng chuyển slide; lên/xuống dùng cuộn trang; lớp nền giúp biểu diễn trạng thái không phát lệnh.

Phạm vi hiện tại là một bàn tay hợp lệ, chạy trên CPU. Ứng dụng đích phải có focus để nhận phím hoặc thao tác cuộn. Độ đúng khi phân loại clip và độ ổn định khi điều khiển liên tục là hai phép đánh giá khác nhau; báo cáo hiện đã có kết quả cho clip.''',[]),
('Các công trình liên quan', '''Em đối chiếu ba hướng nghiên cứu. IPN HandS của Benitez-Garcia và cộng sự, Applied Sciences 2025, gần cách triển khai hiện tại vì dùng chuỗi điểm bàn tay và LSTM. SKETCH của Han và cộng sự, NeurIPS 2025, chuyển skeleton thành biểu diễn dạng ảnh rồi dùng backbone thị giác. ConvMixFormer của Garg, Ghosh và Pradhan, WACV 2025, nghiên cứu bộ trộn tích chập trong kiến trúc nhận diện cử chỉ động.

Các bài dùng dữ liệu và giao thức khác nhau, nên không dùng các tỷ lệ này để kết luận mô hình đồ án tốt hơn hoặc kém hơn. DR/FP của SKETCH cũng không phải accuracy. Phần tiếp theo đọc sâu IPN HandS để làm rõ bài toán, thí nghiệm và điều có thể học từ nghiên cứu.''',[1,2,3]),
('Đọc hiểu IPN HandS', '''Bài IPN HandS: Efficient Annotation Tool and Dataset for Skeleton-Based Hand Gesture Recognition được công bố trên Applied Sciences năm 2025, DOI 10.3390/app15116321. Trọng tâm là chất lượng gán nhãn điểm bàn tay và khoảng thời gian cử chỉ; LSTM được dùng làm mô hình cơ sở để kiểm tra tác động của chất lượng dữ liệu.

Tác giả dùng cùng 200 video, chia 50 người thành 37 người train và 13 người test. Ba mô hình được train riêng từ ba nguồn nhãn: MediaPipe Hands, MediaPipe Holistic và IPN HandS đã sửa nhãn. Chúng dùng cùng cấu trúc ba tầng LSTM, mỗi tầng 256 nút ẩn, dropout 0,3 và phân loại 14 cử chỉ. Các phép chạy được lặp ba lần.

Bảng 6 cho thấy IPN HandS đạt accuracy 91,2 ± 1,4% và recall trung bình 78,0 ± 1,2%. So với MP Hands, recall tăng 15,3 điểm phần trăm. Đây là kết quả của bài báo. Vì dữ liệu bài có mất cân bằng lớp, chỉ nhìn accuracy có thể bỏ qua lớp ít mẫu; cần đọc cả recall trung bình. Bài học là phải kiểm tra chất lượng nhãn và giao thức, không chỉ đổi kiến trúc mạng.''',[1]),
('Ý nghĩa cấu hình của đồ án', '''Code hiện tại khác cấu hình và dữ liệu của bài. Mỗi bước có 44 đặc trưng: 42 tọa độ xy cục bộ của 21 điểm, nối hai tọa độ cổ tay trong ảnh. Chuẩn hóa cục bộ giữ hình dạng; vị trí cổ tay giữ thông tin quỹ đạo toàn cục. Chưa có phép thử bỏ/giữ hai giá trị này để kết luận tác động tới accuracy.

Chuỗi gồm 30 mẫu tại 20 Hz. Có 29 khoảng giữa mẫu đầu và mẫu cuối, nên khoảng đầu–cuối là 1,45 giây, thường mô tả là cửa sổ gần 1,5 giây. Đây là nhịp lấy mẫu cấu hình, không phải FPS toàn hệ thống đã đo.

Hidden size 64 và một tầng là cấu hình cơ sở đang có, tạo mô hình 28.485 tham số. Báo cáo chưa có đối chứng giữa các hidden size để nói 64 là tối ưu. Năm nhãn gồm bốn hướng và nền, khác phép thử 14 cử chỉ có chủ đích của bài. Khác cấu hình chưa phải bằng chứng cải tiến hoặc tái lập nghiên cứu.''',[1]),
('Luồng hệ thống', '''Ảnh webcam được đưa qua MediaPipe để lấy 21 điểm bàn tay. Chương trình chấp nhận đúng một tay hợp lệ, biến thành 44 đặc trưng và đưa vào bộ đệm theo thời gian. Khi đủ 30 mẫu, LSTM trả điểm số cho năm nhãn.

Dự đoán còn đi qua điều kiện xác nhận trước khi phát lệnh: ngưỡng 0,8, giữ ổn định ít nhất 150 ms và ít nhất ba dự đoán mới. Cooldown 1.000 ms cùng nền ổn định 300 ms giúp hạn chế lặp. F8 bật/tạm dừng; F9 dừng chương trình. Những cơ chế này đã có trong mã, chưa thay thế phép thử điều khiển trực tiếp.''',[4,7]),
('Tiền xử lý và chuỗi', '''Ba ảnh được lấy từ clip train SWIPE_LEFT tại 150, 750 và 1.250 ms. Đây là hình minh chứng từ dữ liệu đã thu.

extract_features đổi tọa độ về cùng đơn vị ảnh, trừ cổ tay và chia theo kích thước lòng bàn tay. Sau khi có 42 giá trị cục bộ, hàm nối hai tọa độ cổ tay thành vector 44 chiều. SequenceBuffer dùng timestamp để lấy mẫu đều mỗi 50 ms. Nội suy khe ngắn chỉ thực hiện khi đã biết cả hai đầu mút; mất tay hoặc khoảng hở trên 100 ms làm xóa chuỗi.

NPZ có kích thước đúng mới chứng minh hợp lệ về định dạng. Ý nghĩa nhãn và cách thực hiện cử chỉ vẫn cần xem lại video.''',[]),
('Dữ liệu thực tế', '''Đồ án có 250 clip hợp lệ, cân bằng giữa năm nhãn. Mỗi nhãn có 30 train, 10 validation và 10 test; tổng tương ứng 150, 50, 50. Train thuộc pilot_01 và train_02, validation thuộc val_01, test thuộc test_01.

Không thấy chuỗi đặc trưng trùng tuyệt đối xuyên tập. Điều này không chứng minh độc lập theo người dùng. Manifest chưa có subject_id và báo cáo chưa có đánh giá người chưa thấy; cách chia hiện tại là theo phiên thu.''',[]),
('Giải thích hai dòng forward', '''Khi mở model.py, em đi theo hai dòng forward. Dòng đầu gọi self.lstm(features). Đầu vào [B,30,44] trở thành chuỗi trạng thái [B,30,64]. B là số mẫu trong batch, 30 là số bước, 44 là đặc trưng mỗi bước, 64 là chiều trạng thái ẩn.

sequence[:, -1, :] lấy trạng thái ở thời điểm cuối cho mỗi mẫu, được [B,64]. Trạng thái này mang thông tin đã tích lũy qua các bước trước; không phải lấy nhãn cuối hoặc chỉ lấy 44 giá trị của frame cuối. classifier là Linear 64→5, trả logits. Softmax và chọn nhãn được tính trong predict_gesture sau forward.

Đã kiểm tra tách từng bước trên một clip test lưu sẵn: [1,30,44] → [1,30,64] → [1,64] → [1,5], trùng kết quả model(x). Đây là phép kiểm tra luồng thực thi của code đồ án; chưa phải chạy lại thí nghiệm LSTM gốc của tác giả.''',[5,6]),
('Đường cong huấn luyện', '''Biểu đồ lấy đúng 30 dòng stdout đã lưu trong notebook; loss được làm tròn bốn chữ số theo log. Train loss giảm từ 1,5541 tới 0,1293; validation loss từ 1,4313 tới 0,1720 ở epoch cuối.

Checkpoint được chọn bằng validation loss thấp nhất ở epoch 23, loss đầy đủ khoảng 0,108522 và validation accuracy 94%. Không chọn checkpoint theo test. Cấu hình train là CrossEntropyLoss, Adam learning rate 0,001, batch 16, seed 42, chạy CPU. Đây mới là một lần chạy có log, chưa có thống kê nhiều seed hoặc kết luận cấu hình tối ưu.''',[]),
('Chỉ số đánh giá', '''Chạy lại checkpoint trên 50 clip test cho đúng 40 clip, accuracy 80%; Macro-Precision và Macro-Recall đều 0,8; Macro-F1 khoảng 0,7619. Các giá trị khớp kết quả đã lưu.

Macro-F1 lấy trung bình F1 từng lớp, không phải tính F1 trực tiếp từ hai số macro precision/recall. Nền, trái và phải đúng 10/10 trong tập test nhỏ này. Vuốt lên recall chỉ 0,1, vì vậy 80% tổng thể chưa có nghĩa mọi hướng đều dùng tốt. Mỗi lớp chỉ có 10 mẫu test; một clip làm thay đổi recall lớp 10 điểm phần trăm.''',[]),
('Phân tích lỗi lên và xuống', '''Hàng là nhãn thật, cột là nhãn dự đoán. Chín trong mười clip vuốt lên bị nhận thành xuống. Ở lớp xuống có chín clip đúng và một clip bị nhận thành lên. Toàn bộ mười lỗi test tập trung ở cặp này.

Ảnh minh họa trích từ một clip UP bị đoán DOWN; dự đoán sai này có mức tin cậy khoảng 0,965. Vì thế chỉ tăng ngưỡng chưa chắc sửa lỗi. Qua một số mẫu có khác biệt tư thế ngón tay giữa nhãn; đây là dấu hiệu cần xem quy cách dữ liệu, chưa chứng minh nguyên nhân duy nhất hoặc mô hình chỉ học tư thế.''',[]),
('Demo và giới hạn kiểm thử', '''Video dài 10 giây, phát lại năm clip test với nhãn thật và dự đoán từ toàn chuỗi. Có giữ một clip UP bị nhận sai để minh họa giới hạn. Đây là phát lại dữ liệu đã lưu, không phải bản ghi webcam đang điều khiển ứng dụng khác.

Bộ 60 test tự động đã qua, kiểm tra logic và dùng mô phỏng tại biên phần cứng. Chưa có dữ liệu thực nghiệm cho 40 lượt trực tiếp, 5 phút nền, FPS toàn luồng hoặc độ trễ tới lệnh. Không dùng nhịp lấy mẫu 20 Hz để thay cho phép đo FPS.''',[]),
('Trạng thái đã kiểm tra', '''Bảng này tách từng hạng mục theo minh chứng. Hiện có dữ liệu, tiền xử lý, mô hình, log train, checkpoint, kết quả test, mã tích hợp và test tự động. Đây là phần đã có thể mở tệp hoặc chạy kiểm tra lại.

Có mã phát lệnh không đồng nghĩa đã đo đầy đủ điều khiển trực tiếp. Không đổi thành phần trăm hoàn thành khi chưa thống nhất tiêu chí và trọng số. Những mục còn thiếu trong bảng là giới hạn bằng chứng của lần báo cáo này.''',[]),
('Giới hạn và cách diễn giải', '''Hai kết quả đã quan sát là nhầm lên/xuống và chênh 14 điểm phần trăm giữa validation 94% với test 80%. Từ một lần train và một bộ test nhỏ, chưa đủ kết luận nguyên nhân duy nhất là overfitting.

Giả thuyết liên quan tư thế, cách thu hoặc sai lệch giữa các phiên cần được phân biệt với kết quả đã đo. Độ tổng quát sang người khác, FPS/latency và độ ổn định khi phát lệnh hiện chưa có dữ liệu thực nghiệm. Việc phân tích lỗi và điều kiện thử giúp đặt đúng phạm vi kết luận, không che các trường hợp nhận sai.''',[]),
('Kết luận', '''Báo cáo đã chỉ rõ nghiên cứu IPN HandS và bài học về chất lượng gán nhãn, đối chiếu các khác biệt với cấu hình hiện tại, đồng thời giải thích trực tiếp hai dòng forward của LSTM trong code.

Kết quả hiện có gồm 250 clip, log 30 epoch, checkpoint và đánh giá 50 clip đạt accuracy 80%, Macro-F1 khoảng 0,7619. Luồng thực thi đã được đối chiếu ở một clip và code tích hợp đã có. Giới hạn chính là lỗi lên/xuống và phần đo điều khiển trực tiếp còn thiếu. Chưa có minh chứng tái lập thí nghiệm LSTM gốc hoặc chứng minh cấu hình tối ưu. Em xin kết thúc phần báo cáo tiến độ.''',[1]),
]
assert len(speeches)==16
contents=xml(parts['[Content_Types].xml'])
existing_note_numbers=[int(re.search(r'notesSlide(\d+)\.xml$',n).group(1)) for n in parts if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
next_note=max(existing_note_numbers,default=0)+1
manifest=[]
status_replacements={
    13:{
        'Bước tiếp: ghi CSV từng lượt, log sự kiện và điều kiện chạy.':
        'Video dùng clip lưu sẵn; chưa đo độ trễ tới lệnh.'
    },
    14:{
        'Các phần đã triển khai và phần còn phải đo':'Tiến độ hiện tại được đối chiếu bằng minh chứng',
        'Còn cần làm':'Giới hạn hiện tại',
        'Chốt quy cách cử chỉ':'Quy cách động tác chưa thống nhất',
        'Đo ảnh hưởng đặc trưng':'Chưa đo ảnh hưởng đặc trưng',
        'Thêm mô hình đối chứng':'Chưa có mô hình đối chứng',
        'Sửa nhầm lên / xuống':'Còn nhầm lên / xuống',
        'Đo điều khiển trực tiếp':'Chưa đo điều khiển trực tiếp'
    },
    15:{
        'Sửa lỗi có bằng chứng, rồi đo lại bằng giao thức rõ ràng':'Ba giới hạn khi đọc kết quả hiện tại',
        'Việc cần làm':'Phần chưa xác nhận',
        'Cách kiểm chứng':'Diễn giải kết quả',
        'Đối chiếu video với quy cách; chốt cách vuốt; thu bù train/validation khi cần.':
        'Nguyên nhân lỗi lên/xuống chưa được xác định từ bằng chứng hiện có.',
        'So sánh recall lên/xuống; kiểm tra mẫu lỗi. Không dùng test để chọn checkpoint.':
        'Lỗi tập trung ở hướng dọc. Chưa thể kết luận chỉ do tư thế, dữ liệu hay mô hình.',
        'Giữ phiên test cuối riêng; ghi mã phiên, cấu hình, seed.':
        'Chưa có thống kê nhiều seed; số mẫu mỗi lớp còn ít.',
        'Đánh giá sau khi khóa mô hình; báo số mẫu và độ biến động nếu chạy nhiều seed.':
        'Chênh 14 điểm phần trăm chưa đủ kết luận nguyên nhân duy nhất là overfitting.',
        'Đo 40 lượt; 5 phút nền; ghi FPS và timestamp từng phần.':
        'Chưa có số đo FPS toàn luồng, độ trễ tới lệnh hoặc thử nghiệm nền liên tục.',
        'Báo đúng/sai/bỏ sót/lặp, FPS và độ trễ trong cùng điều kiện.':
        'Kết quả clip chưa phản ánh đầy đủ độ ổn định khi điều khiển máy tính.',
        'Khả năng tổng quát hóa sang người khác: Chưa có dữ liệu thực nghiệm. Nguyên nhân lỗi lên/xuống vẫn là giả thuyết cần kiểm tra.':
        'Khả năng tổng quát hóa sang người khác: chưa có dữ liệu thực nghiệm. Nguyên nhân lỗi lên/xuống chưa có kết luận.'
    }
}
for page,(slide_name,(title,spoken,ref_ids)) in enumerate(zip(order,speeches),1):
    root=xml(parts[slide_name])
    for text in root.findall('.//a:t',NS):
        text.text=status_replacements.get(page,{}).get(text.text,text.text)
        if text.text and re.fullmatch(r'\d{2}\s*/\s*\d+',text.text.strip()):text.text=f'{page:02d} / 16'
        if page==16 and text.text:
            text.text=text.text.replace('10 / KẾT LUẬN','09 / KẾT LUẬN')
            text.text=text.text.replace('Hiểu bài báo và code trước khi mở rộng','Kết luận: kết quả hiện có và giới hạn kiểm thử')
            text.text=text.text.replace('Việc ưu tiên ngay sau buổi báo cáo','Kết quả và giới hạn hiện tại')
            text.text=text.text.replace('Đọc sâu IPN HandS → giải thích code → kiểm chứng lỗi lên/xuống.',
                'Đã đo trên clip lưu sẵn; chưa có số liệu về điều khiển trực tiếp.')
    parts[slide_name]=encode(root)
    rel_name=posixpath.join(posixpath.dirname(slide_name),'_rels',posixpath.basename(slide_name)+'.rels')
    relationships=xml(parts[rel_name])
    note_rel=next((r for r in relationships if r.get('Type','').endswith('/notesSlide')),None)
    if note_rel is None:
        note_name=f'ppt/notesSlides/notesSlide{next_note}.xml';next_note+=1
        note_root=xml(sections['ppt/notesSlides/notesSlide1.xml'])
        note_relationships=xml(sections['ppt/notesSlides/_rels/notesSlide1.xml.rels'])
        for r in note_relationships:
            if r.get('Type','').endswith('/slide'):r.set('Target','../slides/'+posixpath.basename(slide_name))
        parts[posixpath.join('ppt/notesSlides/_rels',posixpath.basename(note_name)+'.rels')]=encode(note_relationships)
        rid=max([int(r.get('Id')[3:]) for r in relationships if re.fullmatch(r'rId\d+',r.get('Id',''))],default=0)+1
        E.SubElement(relationships,'{'+NS['rel']+'}Relationship',Id=f'rId{rid}',
                     Type=NS['r']+'/notesSlide',Target='../notesSlides/'+posixpath.basename(note_name))
        E.SubElement(contents,'{'+NS['ct']+'}Override',PartName='/'+note_name,
                     ContentType='application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
    else:
        note_name=posixpath.normpath(posixpath.join(posixpath.dirname(slide_name),note_rel.get('Target')))
        note_root=xml(parts[note_name])
    sources=[]
    for ref_id in ref_ids:
        r=next(x for x in C['references'] if x['id']==ref_id)
        sources.append(f"[{ref_id}] {r['authors']}, {r['title']}, {r['venue']}, {r['year']}. {r['url']}")
    notes=spoken+('\n\nNguồn tra cứu (không cần đọc thành lời):\n'+'\n'.join(sources) if sources else '')
    set_notes(note_root,notes,page)
    parts[note_name]=encode(note_root);parts[rel_name]=encode(relationships)
    manifest.append({'slide':page,'part':slide_name,'title':title,'spoken_notes':spoken,'notes':notes,'references':ref_ids})
parts['[Content_Types].xml']=encode(contents)
if 'docProps/app.xml' in parts:
    root=xml(parts['docProps/app.xml'])
    for node in root.iter():
        if E.QName(node).localname=='Slides':node.text='16'
    parts['docProps/app.xml']=encode(root)

# Preserve all binary content: user-added cover image, video, original chart/workbook data.
protected=[n for n in original if n.startswith(('ppt/media/','ppt/charts/','ppt/embeddings/'))]
for n in protected:assert parts[n]==original[n],n
def canonical_tree(data):
    root=xml(data)
    for t in root.findall('.//a:t',NS):
        if t.text and re.fullmatch(r'\d{2}\s*/\s*\d+',t.text.strip()):t.text='PAGE'
    return E.tostring(root.find('p:cSld',NS),method='c14n',exclusive=True)
preserved=[]
for n in order:
    if n in original and n not in changed and n not in {f'ppt/slides/slide{i}.xml' for i in [12,13,14,15]}:
        assert canonical_tree(parts[n])==canonical_tree(original[n]),n
        preserved.append(n)
assert len(preserved)==9
candidate=W/'Bao_Cao_Tien_Do_candidate.pptx'
with ZipFile(candidate,'w',compression=ZIP_DEFLATED) as z:
    for n,data in parts.items():z.writestr(n,data)
with ZipFile(candidate) as z:assert z.testzip() is None
(W/'slides_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
notes_md=['# Ghi chú thuyết trình — tuần 4, 08/11/2026','',
          '16 slide, không có phần kế hoạch tuần tiếp theo. Dùng phần lời nói để tập trình bày; nguồn cuối mục để tra cứu.',
          'Sinh viên: Trịnh Viết Mỹ — 2380601382 — 23DTHA3. GVHD: PGS.TS. Võ Đình Bảy.',
          'Các câu trong tài liệu là lời gợi ý; chỉ trình bày mức hiểu và công việc bạn có thể tự giải thích, kiểm chứng.','']
for m in manifest:notes_md += [f"## Slide {m['slide']}. {m['title']}",'',m['notes'],'']
notes_md += ['## Câu hỏi cần tập trả lời','',
 '**Đóng góp chính của IPN HandS là gì?** Công cụ/dữ liệu landmark và biên thời gian được sửa nhãn; LSTM là mô hình cơ sở để đo tác động của chất lượng gán nhãn.', '',
 '**Vì sao 44 đặc trưng?** 21 điểm xy tạo 42 giá trị cục bộ; nối hai tọa độ cổ tay. Chưa có đối chứng bỏ/giữ để kết luận mức tăng accuracy.', '',
 '**Vì sao 30 mẫu, 64 nút ẩn?** 30 mẫu ở 20 Hz tạo cửa sổ gần 1,5 giây. 64 là cấu hình cơ sở đang có, tổng 28.485 tham số; chưa có thí nghiệm chọn tối ưu.', '',
 '**MediaPipe có nhận diện năm cử chỉ không?** Trong project, MediaPipe tìm điểm bàn tay; LSTM phân loại chuỗi thành năm nhãn.', '',
 '**Lấy trạng thái cuối có bỏ hết các frame trước không?** Trạng thái cuối LSTM đã được cập nhật theo chuỗi; nó khác việc chỉ lấy vector đặc trưng của frame cuối.', '',
 '**80% test có nghĩa hệ thống ổn định không?** Chỉ phản ánh 40/50 clip đúng. Lớp lên recall 0,1; chưa đo đủ điều khiển liên tục.', '',
 '**Validation 94%, test 80% là do overfitting?** Có chênh lệch nhưng một lần chạy và ít mẫu chưa xác định được nguyên nhân duy nhất.', '',
 '**Đã chạy code tác giả chưa?** Chưa có minh chứng tái lập thí nghiệm LSTM gốc. Phép trace là của code đồ án trên clip tự thu.', '',
 '**Video có phải demo điều khiển trực tiếp?** Là phát lại clip test đã lưu với dự đoán toàn chuỗi. Chưa có số liệu thử trực tiếp trong báo cáo này.','']
(W/'speaker_notes.md').write_text('\n'.join(notes_md),encoding='utf-8')
report={'candidate':str(candidate),'slides':len(order),'added_slide':'paper-to-code comparison, no weekly plan',
        'original_content_slides_preserved_except_numbering':preserved,'protected_parts_unchanged':len(protected),
        'updated_original_sections':['slide4.xml','slide8.xml','slide12.xml','slide13.xml','slide14.xml','slide15.xml'],'original_sha256':meta['original_deck_sha256']}
(W/'preservation_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
