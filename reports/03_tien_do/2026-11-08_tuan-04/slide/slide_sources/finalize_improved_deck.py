"""Verify the improved candidate and publish it after all checks pass.

No training, no edits to experiment artifacts. The user-edited input is archived.
"""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import argparse
import json
import posixpath
import re
import shutil
from lxml import etree as E
from pypdf import PdfReader

S=Path(__file__).resolve().parent
O=S.parent
W=S/'qa/cai_thien_2026-11-08'
R=next(p for p in S.parents if (p/'pyproject.toml').is_file() and (p/'src/hand_tracking').is_dir())
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}

def verify(deck,pdf,notes):
    results={}
    with ZipFile(deck) as z:
        assert z.testzip() is None
        pres=E.fromstring(z.read('ppt/presentation.xml'))
        rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
        targets={r.get('Id'):r.get('Target') for r in rels}
        slides=[posixpath.normpath(posixpath.join('ppt',targets[n.get('{'+NS['r']+'}id')])) for n in pres.findall('./p:sldIdLst/p:sldId',NS)]
        assert len(slides)==16
        all_text=[];notes_seen=[];tables=0
        for i,name in enumerate(slides,1):
            root=E.fromstring(z.read(name))
            paragraphs=[''.join(t.text or '' for t in p.findall('.//a:t',NS)) for p in root.findall('.//a:p',NS)]
            text='\n'.join(paragraphs);all_text.append(text)
            assert f'{i:02d} / 16' in text,(i,'wrong footer')
            assert not re.search(r'kế hoạch|tuần 5|09–15/11|sản phẩm đầu ra|Bước tiếp:|Việc cần làm|Còn cần làm',text,re.I),(i,'unwanted planning section')
            tables+=len(root.findall('.//a:tbl',NS))
            rel_name=posixpath.join(posixpath.dirname(name),'_rels',posixpath.basename(name)+'.rels')
            rs=E.fromstring(z.read(rel_name))
            note_rel=[r for r in rs if r.get('Type','').endswith('/notesSlide')]
            assert len(note_rel)==1
            notes_seen.append(posixpath.normpath(posixpath.join(posixpath.dirname(name),note_rel[0].get('Target'))))
        assert len(set(notes_seen))==16
        for value in ['Trịnh Viết Mỹ','2380601382','23DTHA3','PGS.TS. Võ Đình Bảy']:
            assert value in all_text[0],value
        assert tables==6
        assert '10.3390/app15116321' in all_text[3]
        for value in ['87,5 ± 1,0','62,7 ± 2,0','89,2 ± 0,6','66,9 ± 0,7','91,2 ± 1,4','78,0 ± 1,2','15,3']:
            assert value in all_text[3],value
        for value in ['44 đặc trưng','30 mẫu','64 nút ẩn','chưa thử']:
            assert value in all_text[4],value
        for line in ['sequence, _ = self.lstm(features)','return self.classifier(sequence[:, -1, :])']:
            assert line in all_text[8] and line in (R/'src/hand_tracking/model.py').read_text(encoding='utf-8')
        assert '40/50' in all_text[10] and '0,7619' in all_text[10]
        assert '9/10' in all_text[11]
        charts=[n for n in z.namelist() if re.fullmatch(r'ppt/charts/chart\d+\.xml',n)]
        assert len(charts)==2
        videos=[n for n in z.namelist() if n.endswith('.mp4')]
        assert len(videos)==1
        assert sha256(z.read(videos[0])).hexdigest()==sha256((S/'assets/demo_test.mp4').read_bytes()).hexdigest()
        meta=json.loads((W/'revision_input.json').read_text(encoding='utf-8'))
        with ZipFile(R/meta['input_deck']) as original:
            protected=[n for n in original.namelist() if n.startswith(('ppt/media/','ppt/charts/','ppt/embeddings/'))]
            for name in protected:
                assert z.read(name)==original.read(name),name
        results['protected_media_chart_workbook_parts_unchanged']=len(protected)
        results.update({'slides':16,'notes_parts':16,'native_tables':tables,'native_charts':2,'embedded_videos':1,'weekly_plan_absent':True,'page_numbers_correct':True})
    reader=PdfReader(pdf)
    assert len(reader.pages)==16
    for i,page in enumerate(reader.pages,1):
        text=page.extract_text() or ''
        assert len(text)>50,i
    assert 'Trịnh Viết Mỹ' in reader.pages[0].extract_text()
    notes_text=Path(notes).read_text(encoding='utf-8')
    assert len(re.findall(r'^## Slide \d+\.',notes_text,re.M))==16
    results.update({'pdf_pages':16,'speaker_note_sections':16,'pdf_searchable_vietnamese':True})
    com=json.loads((W/'powerpoint_checks.json').read_text(encoding='utf-8-sig'))
    assert not [x for x in com['findings'] if 'overflow' in x['kind']]
    assert com['slides']==16 and com['rendered']==16
    assert any(x['kind']=='media' and x['slide']==13 and x['duration_ms']==10000 for x in com['findings'])
    results['powerpoint_overflow_findings']=0
    baseline=json.loads((S/'original_hashes.json').read_text(encoding='utf-8'))
    changed=[]
    for rel,expected in baseline.items():
        p=R/rel
        if rel.startswith('documents/Base/'):p=R/'reports/01_tai_lieu_de_tai'/Path(rel).name
        if not p.is_file() or sha256(p.read_bytes()).hexdigest()!=expected:changed.append(rel)
    assert not changed,changed
    results.update({'original_experiment_and_source_files_checked':len(baseline),'original_files_changed':changed,'status':'PASS','qa_status':'PASS'})
    return results

def publish():
    results=verify(W/'Bao_Cao_Tien_Do_candidate.pptx',W/'Bao_Cao_Tien_Do.pdf',W/'speaker_notes.md')
    meta=json.loads((W/'revision_input.json').read_text(encoding='utf-8'))
    # Prevent overwriting any concurrent user edits made after the input was archived.
    allowed={meta['original_deck_sha256']}
    previous=W/'published_manifest.json'
    if previous.is_file():allowed.add(json.loads(previous.read_text(encoding='utf-8'))['pptx_sha256'])
    assert sha256((O/'Bao_Cao_Tien_Do.pptx').read_bytes()).hexdigest() in allowed,'Current PowerPoint has new edits; merge them before publishing.'
    assert not list(O.glob('~$*.pptx')),'Close and save the open PowerPoint before publishing.'
    report=(O/'Bao_Cao_Tien_Do.md').read_text(encoding='utf-8')
    report=re.sub(r'\n## 7\. Kế hoạch phát triển tiếp theo\n.*?\n## 8\. Kết luận', '\n## 7. Kết luận',report,flags=re.S)
    report=report.replace('Biểu đồ trong slide 9','Biểu đồ trong slide 10')
    assert '### Tuần 5' not in report
    (W/'Bao_Cao_Tien_Do.md').write_text(report,encoding='utf-8')
    qa=f'''# Kiểm tra bản thuyết trình cải thiện — 08/11/2026

Đã giữ yêu cầu không có phần kế hoạch tuần tiếp theo hoặc bảng đầu ra theo tuần. Bản hiện tại gồm **16 slide, 16 trang PDF và 16 mục ghi chú**.

## Nội dung thay đổi

- Đọc sâu IPN HandS: bổ sung tác giả, Applied Sciences 2025, DOI, sơ đồ ba nguồn annotation và Bảng 6. Các số mean/std thuộc bài báo, không phải thực nghiệm đồ án. Hiệu recall 78,0 − 62,7 = 15,3 điểm phần trăm được diễn giải rõ.
- Thêm một slide đối chiếu paper/code và ý nghĩa 44 đặc trưng, 30 mẫu ở 20 Hz, hidden size 64. Ghi rõ 64 là cấu hình cơ sở hiện có, chưa có đối chứng để kết luận tối ưu.
- Minh họa hai dòng forward đúng mã nguồn, tensor [B,30,44] → [B,30,64] → [B,64] → [B,5], vị trí softmax trong predict_gesture.
- Kết luận chỉ nêu kết quả và giới hạn đã ghi nhận. Các dòng bước tiếp/việc cần làm được đổi thành giới hạn hiện tại. Sửa toàn bộ số trang; bỏ mục kế hoạch theo tuần khỏi báo cáo viết đi kèm.
- Viết lại ghi chú đủ 16 slide và phần luyện trả lời câu hỏi; nguồn được đặt riêng để tra cứu.

## Giữ nguyên nội dung người dùng và thực nghiệm

Bản trước được sao lưu tại `{meta['backup_folder']}`. Bìa và bố cục các chỉnh sửa trực tiếp của người dùng được giữ. Nội dung chín slide cũ chỉ đổi số trang; ba slide được cải thiện nội dung nghiên cứu/code/kết luận, ba slide đổi lời hướng dẫn tiếp theo thành giới hạn hiện tại, và thêm một slide đối chiếu cấu hình. Toàn bộ 14 part ảnh/video/chart/workbook của bản vào giữ nguyên bytes. Có log `slide_sources/qa/cai_thien_2026-11-08/preservation_checks.json`.

Đối chiếu **{results['original_experiment_and_source_files_checked']} tệp** nguồn/thực nghiệm/đặc tả trong snapshot, có ánh xạ ba tài liệu đã chuyển sang `reports/01_tai_lieu_de_tai/`: không có thay đổi. Không huấn luyện hoặc sửa số liệu; giữ 250 clip, 40/50 test đúng, Macro-F1 0,7619, lỗi lên/xuống và phần chưa đo.

## Kiểm tra kỹ thuật

PowerPoint mở được, render đủ 16 slide 1.600 × 900. Kiểm tra BoundHeight/BoundWidth của textbox và ô bảng không phát hiện tràn. Có 6 bảng native, 2 biểu đồ với workbook và video 10 giây ở slide 13. Đã xem từng slide; đã render PDF và kiểm tra các trang mới.

Validator của skill Anthropic pptx được chạy với `--original` là bản trước, báo PASSED về XML, relationships, IDs, content types, chart và không có lỗi XSD mới. Bản PDF có 16 trang, trích xuất được chữ Việt. Poppler cảnh báo font phụ Symbol/ArialUnicode; hình kiểm tra vẫn hiện đúng các ký hiệu/chữ Việt được xem.

Ghi chú trong PPTX và Markdown đều có đủ 16 mục, không lẫn ghi chú kế hoạch đã bỏ. Kiểm tra thứ tự và chân trang 01/16 đến 16/16. Các log và PNG hiện tại nằm trong `slide_sources/qa/cai_thien_2026-11-08/`.

## Phạm vi bằng chứng

Video là phát lại clip đã lưu. Chưa có dữ liệu thực nghiệm cho FPS/latency toàn hệ thống, 40 lượt trực tiếp, 5 phút nền hoặc người chưa thấy. Chưa tái lập LSTM gốc của IPN HandS. Kiểm tra media gồm bytes và thời lượng PowerPoint nhận; chưa chạy thử phát bằng buổi Slide Show qua giao diện. Tài liệu không tự chứng minh sinh viên đã hiểu code; phần câu hỏi hỗ trợ tập giải thích.
'''
    (W/'qa_report.md').write_text(qa,encoding='utf-8')
    for src,dest in [('Bao_Cao_Tien_Do_candidate.pptx','Bao_Cao_Tien_Do.pptx'),('Bao_Cao_Tien_Do.pdf','Bao_Cao_Tien_Do.pdf'),
                     ('speaker_notes.md','speaker_notes.md'),('Bao_Cao_Tien_Do.md','Bao_Cao_Tien_Do.md'),('qa_report.md','qa_report.md')]:
        shutil.copy2(W/src,O/dest)
    shutil.copy2(W/'slides_manifest.json',S/'slides_manifest.json')
    (W/'package_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    (S/'qa/package_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(W/'powerpoint_checks.json',S/'qa/powerpoint_checks.json')
    files=['Bao_Cao_Tien_Do.pptx','Bao_Cao_Tien_Do.pdf','Bao_Cao_Tien_Do.md','speaker_notes.md','references.md','qa_report.md','Huong_dan_doc_bai_bao_va_code.md']
    manifest={'report_date':'2026-11-08','verified_evidence_date':'2026-11-07','revision':'Cải thiện bài báo và code; không có kế hoạch theo tuần',
              'files':{name:{'bytes':(O/name).stat().st_size,'sha256':sha256((O/name).read_bytes()).hexdigest()} for name in files},'checks':results}
    (O/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (W/'published_manifest.json').write_text(json.dumps({'pptx_sha256':manifest['files']['Bao_Cao_Tien_Do.pptx']['sha256'],'backup':meta['backup_folder']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'published':str(O/'Bao_Cao_Tien_Do.pptx'),'checks':results,'backup':meta['backup_folder']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--publish',action='store_true');args=parser.parse_args()
    if args.publish:publish()
    else:print(json.dumps(verify(O/'Bao_Cao_Tien_Do.pptx',O/'Bao_Cao_Tien_Do.pdf',O/'speaker_notes.md'),ensure_ascii=False,indent=2))
