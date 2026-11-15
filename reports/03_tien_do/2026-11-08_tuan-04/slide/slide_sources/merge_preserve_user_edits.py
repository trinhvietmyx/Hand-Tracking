"""Use the current user-edited deck as base; replace only four content slides."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from io import BytesIO
from hashlib import sha256
from lxml import etree as ET
import json

S=Path(__file__).resolve().parent
O=S.parent
original=S/'qa/input_current_user_deck.pptx'
target=O/'Bao_Cao_Tien_Do.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
selected=[4,8,15,16]
with ZipFile(original) as z:
    base={n:z.read(n) for n in z.namelist()}
with ZipFile(BytesIO(target.read_bytes())) as z:
    candidate={n:z.read(n) for n in z.namelist()}
before={n:sha256(base[n]).hexdigest() for n in base if n.startswith('ppt/slides/slide') and n.endswith('.xml')}
for i in selected:
    for name in [f'ppt/slides/slide{i}.xml',f'ppt/slides/_rels/slide{i}.xml.rels',
                 f'ppt/notesSlides/notesSlide{i}.xml',f'ppt/notesSlides/_rels/notesSlide{i}.xml.rels']:
        assert name in base and name in candidate,name
        base[name]=candidate[name]
# Align notes with the supervisor title already edited by the user on the cover.
for name in list(base):
    if name.startswith('ppt/notesSlides/notesSlide') and name.endswith('.xml'):
        root=ET.fromstring(base[name]);changed=False
        for node in root.findall('.//a:t',ns):
            if node.text and 'ThS. TS. Võ Đình Bảy' in node.text:
                node.text=node.text.replace('ThS. TS. Võ Đình Bảy','PGS.TS. Võ Đình Bảy');changed=True
            if node.text and 'Ảnh trên trang bìa lấy từ clip kiểm tra của chính project.' in node.text:
                node.text=node.text.replace('Ảnh trên trang bìa lấy từ clip kiểm tra của chính project.',
                    'Trang bìa giữ hình minh họa 21 điểm bàn tay trong file hiện tại của người dùng.');changed=True
        if changed:base[name]=ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
preserved=[]
for i in range(1,17):
    n=f'ppt/slides/slide{i}.xml'
    if i not in selected:
        assert sha256(base[n]).hexdigest()==before[n]
        preserved.append(i)
with ZipFile(target,'w',compression=ZIP_DEFLATED) as z:
    for name,data in base.items():z.writestr(name,data)
with ZipFile(target) as z:assert z.testzip() is None

manifest=json.loads((S/'slides_manifest.json').read_text(encoding='utf-8'))
notes=['# Ghi chú thuyết trình — chỉnh theo góp ý GVHD tuần 2','',
       'Báo cáo online 08/11/2026 từ 14:00. Sinh viên Trịnh Viết Mỹ — 2380601382 — 23DTHA3.',
       'GVHD: PGS.TS. Võ Đình Bảy (giữ theo bìa PowerPoint hiện có của người dùng).','',
       'Ưu tiên trình bày: bài báo cụ thể → hiểu phương pháp → giải thích code → kết quả → việc cần làm trước khi mở rộng.','']
for item in manifest:
    i=item['slide'];root=ET.fromstring(base[f'ppt/notesSlides/notesSlide{i}.xml'])
    blocks=[]
    for shape in root.findall('.//p:sp',ns):
        ph=shape.find('.//p:ph',ns)
        if ph is not None and ph.get('type')=='body':
            for p in shape.findall('.//a:p',ns):
                line=''.join(n.text or '' for n in p.findall('.//a:t',ns))
                if line:blocks.append(line)
    body='\n'.join(blocks)
    assert body, i
    item['notes']=body
    notes += [f"## Slide {i}. {item['title']}",'',body,'']
(O/'speaker_notes.md').write_text('\n'.join(notes),encoding='utf-8')
(S/'slides_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report={'base_file':str(original),'base_sha256':sha256(original.read_bytes()).hexdigest(),
 'replaced_content_slides':selected,'other_slide_xml_preserved_exactly':preserved,
 'notes_title_aligned_with_existing_cover':True,
 'original_user_file_modified':False}
(S/'qa/user_edits_preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
