"""Create a portable archive without following the runtime dependency junction."""
from pathlib import Path
from hashlib import sha256
import json
import os
import zipfile

source = Path(__file__).resolve().parent
output = source.parent
checks = json.loads((source/'qa/package_checks.json').read_text(encoding='utf-8'))
assert checks['qa_status']=='PASS'
names = ['Bao_Cao_Tien_Do.pptx','Bao_Cao_Tien_Do.pdf','Bao_Cao_Tien_Do.md',
         'speaker_notes.md','references.md','qa_report.md','Huong_dan_doc_bai_bao_va_code.md']
manifest = {'report_date':'2026-11-08','verified_evidence_date':'2026-11-07',
            'files':{name:{'bytes':(output/name).stat().st_size,
                           'sha256':sha256((output/name).read_bytes()).hexdigest()}
                     for name in names},'checks':checks}
(output/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive = output.parent/'goi_xuat_lai/Bao_Cao_Theo_Gop_Y_GVHD_2026-11-08.zip'
archive.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for current,dirs,files in os.walk(output,followlinks=False):
        dirs[:] = [d for d in dirs if d not in {'node_modules','__pycache__','.git'}]
        for name in sorted(files):
            p=Path(current)/name
            z.write(p,Path('progress')/p.relative_to(output))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any('node_modules' in name for name in z.namelist())
    for name in names:
        assert 'progress/'+name in z.namelist()
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,
                  'main_files':manifest['files']},ensure_ascii=False,indent=2))
