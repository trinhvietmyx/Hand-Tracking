"""Read existing experiment artifacts and write evidence only under reports/03_tien_do/2026-11-08_tuan-04/slide."""

from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent/'pyproject.toml').is_file() and (parent/'src/hand_tracking').is_dir())
SOURCES = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))

import numpy as np
import torch
from hand_tracking.config import load_config
from hand_tracking.dataset import load_split
from hand_tracking.model import load_gesture_model


def file_hash(path):
    digest = sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


original_files = []
for pattern in ['src/**/*.py', 'tests/**/*.py', 'configs/*.json', 'data/manifest.csv',
                'data/sessions/*.json', 'data/processed/**/*.npz', 'data/raw/**/*.avi',
                'models/**/*.pt', 'outputs/**/*.json', 'notebook/*.ipynb',
                'reports/01_tai_lieu_de_tai/*.md']:
    original_files.extend(ROOT.glob(pattern))
snapshot = {str(path.relative_to(ROOT)).replace('\\', '/'): file_hash(path)
            for path in sorted(set(original_files)) if path.is_file()}
(SOURCES / 'original_hashes.json').write_text(json.dumps(snapshot, indent=2), encoding='utf-8')

config = load_config(ROOT / 'configs/default.json')
model, epoch = load_gesture_model(config)
checkpoint = torch.load(config.checkpoint_path, map_location='cpu', weights_only=True)
datasets = {split: load_split(config, split) for split in ['train', 'validation', 'test']}
features, targets, rows = datasets['test']
with torch.inference_mode():
    predictions = model(torch.from_numpy(features)).argmax(dim=1).numpy()
matrix = np.zeros((5, 5), dtype=int)
np.add.at(matrix, (targets, predictions), 1)
existing = json.loads((ROOT / 'outputs/evaluation.json').read_text(encoding='utf-8'))
assert matrix.tolist() == existing['confusion_matrix']
assert len(rows) == 50 and int(matrix.trace()) == 40

notebook_path = ROOT / 'notebook/hand_tracking.ipynb'
notebook = json.loads(notebook_path.read_text(encoding='utf-8'))
training_stdout = '\n'.join(''.join(output.get('text', []))
                            for cell in notebook['cells'] for output in cell.get('outputs', [])
                            if output.get('output_type') == 'stream')
pattern = re.compile(r'Epoch (\d+)/(\d+) \| train_loss=([\d.]+) \| val_loss=([\d.]+) \| val_accuracy=([\d.]+)%')
history = [{'epoch': int(e), 'total_epochs': int(total), 'train_loss': float(train),
            'validation_loss': float(val), 'validation_accuracy': float(acc) / 100}
           for e, total, train, val, acc in pattern.findall(training_stdout)]
assert len(history) == 30 and [r['epoch'] for r in history] == list(range(1, 31))
best_record = min(history, key=lambda value: value['validation_loss'])
assert best_record['epoch'] == epoch == 23
assert abs(best_record['validation_loss'] - checkpoint['val_loss']) < 0.00005
with (SOURCES / 'training_history.csv').open('w', encoding='utf-8', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(history[0]))
    writer.writeheader()
    writer.writerows(history)
(SOURCES / 'notebook_training_stdout.txt').write_text(training_stdout, encoding='utf-8')

notebook_checkpoint_path = ROOT / 'models/notebook/gesture_lstm.pt'
notebook_checkpoint = torch.load(notebook_checkpoint_path, map_location='cpu', weights_only=True)
weights_identical = all(torch.equal(value, notebook_checkpoint['model_state_dict'][key])
                        for key, value in checkpoint['model_state_dict'].items())
assert weights_identical
notebook_report = json.loads((ROOT / 'outputs/notebook/evaluation.json').read_text(encoding='utf-8'))
assert notebook_report['confusion_matrix'] == matrix.tolist()

fingerprints = defaultdict(list)
split_info = {}
for split, (values, labels, source_rows) in datasets.items():
    for value, row in zip(values, source_rows, strict=True):
        fingerprints[sha256(value.tobytes()).hexdigest()].append({'split': split, 'clip_id': row['clip_id']})
    split_info[split] = {
        'count': len(labels), 'shape': list(values.shape),
        'class_counts': {name: int((labels == index).sum()) for index, name in enumerate(existing['class_names'])},
        'sessions': sorted({r['session_id'] for r in source_rows}),
        'first_created_at': min(r['created_at'] for r in source_rows),
        'last_created_at': max(r['created_at'] for r in source_rows),
    }
cross_split_duplicates = [items for items in fingerprints.values() if len({r['split'] for r in items}) > 1]

test_environment = os.environ.copy()
test_environment['PYTHONPATH'] = str(ROOT / 'src')
test_run = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'],
                          cwd=ROOT, env=test_environment, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=180)
test_text = test_run.stdout + test_run.stderr
(SOURCES / 'unit_tests.txt').write_text(test_text, encoding='utf-8')
if test_run.returncode:
    raise RuntimeError(test_text)
test_match = re.search(r'Ran (\d+) tests in ([\d.]+)s', test_text)
assert test_match

versions = {}
for package in ['numpy', 'torch', 'mediapipe', 'opencv-contrib-python', 'pyautogui', 'pynput', 'matplotlib', 'scikit-learn']:
    try:
        versions[package] = metadata.version(package)
    except metadata.PackageNotFoundError:
        versions[package] = None

all_metrics = existing['per_class'].values()
summary = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'author': {'name': 'Trịnh Viết Mỹ', 'student_id': '2380601382', 'class': '23DTHA3',
               'supervisor': 'ThS. TS. Võ Đình Bảy'},
    'report_date': '2026-11-08', 'evidence_date': '2026-11-07',
    'project_root': str(ROOT), 'dataset': split_info,
    'cross_split_identical_feature_sequences': cross_split_duplicates,
    'checkpoint': {'path': str(config.checkpoint_path.relative_to(ROOT)), 'epoch': epoch,
                   'validation_loss': checkpoint['val_loss'], 'validation_accuracy': checkpoint['val_accuracy'],
                   'parameters': sum(parameter.numel() for parameter in model.parameters()),
                   'notebook_weights_identical': weights_identical},
    'test': {'samples': len(rows), 'correct': int(matrix.trace()), 'accuracy': float(matrix.trace()/len(rows)),
             'macro_precision': sum(m['precision'] for m in all_metrics)/5,
             'macro_recall': sum(m['recall'] for m in existing['per_class'].values())/5,
             'macro_f1': existing['macro_f1'], 'per_class': existing['per_class'],
             'confusion_matrix': matrix.tolist(), 'reproduced_existing_result': True},
    'training_history': history,
    'logged_training_seconds': float(re.search(r'Thời gian huấn luyện: ([\d.]+) giây', training_stdout).group(1)),
    'configuration': json.loads((ROOT / 'configs/default.json').read_text(encoding='utf-8')),
    'versions': versions, 'python': sys.version.split()[0],
    'tests': {'passed': int(test_match.group(1)), 'seconds': float(test_match.group(2)), 'returncode': 0},
    'missing_experiments': ['steady-state inference latency', 'end-to-end webcam FPS with hand tracking and LSTM',
                            '40 live gesture trials', 'five-minute idle false-command test',
                            'unseen-person evaluation'],
    'training_log_provenance': {'file': 'notebook/hand_tracking.ipynb', 'output': 'stored stdout',
                                 'epochs': 30, 'rounded_loss_decimals': 4},
}
(SOURCES / 'verified_metrics.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

previous_assets = ROOT / 'reports/99_luu_tru/ban_9_slide/nguon_tao_slide/assets'
for source in previous_assets.glob('*.png'):
    shutil.copy2(source, SOURCES / 'assets' / source.name)
shutil.copy2(ROOT / 'reports/03_tien_do/2026-11-08_tuan-04/minh_chung/03-phat-lai-5-clip-test.mp4',
             SOURCES / 'assets/demo_test.mp4')
print(json.dumps({'dataset_counts': {key: value['count'] for key, value in split_info.items()},
                  'test_accuracy': summary['test']['accuracy'], 'parameters': summary['checkpoint']['parameters'],
                  'training_epochs': len(history), 'notebook_weights_identical': weights_identical,
                  'unit_tests': summary['tests'], 'versions': versions,
                  'cross_split_identical_features': len(cross_split_duplicates)}, ensure_ascii=False, indent=2))
