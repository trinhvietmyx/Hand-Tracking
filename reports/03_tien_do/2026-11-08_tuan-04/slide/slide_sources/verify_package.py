"""Read-only verification of the current improved presentation."""
import json
from finalize_improved_deck import verify, O, S

if __name__ == '__main__':
    result = verify(O/'Bao_Cao_Tien_Do.pptx', O/'Bao_Cao_Tien_Do.pdf', O/'speaker_notes.md')
    (S/'qa/package_checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
