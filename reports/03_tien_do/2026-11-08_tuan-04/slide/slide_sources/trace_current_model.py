"""Read one stored clip and explain model tensor shapes; never train or save weights."""
from pathlib import Path
import json
import sys

import torch

S = Path(__file__).resolve().parent
ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent/'pyproject.toml').is_file() and (parent/'src/hand_tracking').is_dir())
sys.path.insert(0,str(ROOT/'src'))
from hand_tracking.config import load_config
from hand_tracking.dataset import load_split
from hand_tracking.model import load_gesture_model
from hand_tracking.labels import CLASS_NAMES

config=load_config(ROOT/'configs/default.json')
model,epoch=load_gesture_model(config)
features,targets,rows=load_split(config,'test')
x=torch.from_numpy(features[:1])
with torch.inference_mode():
    sequence,(hidden,cell)=model.lstm(x)
    last=sequence[:,-1,:]
    logits=model.classifier(last)
    assert torch.allclose(logits,model(x))
    probs=logits.softmax(dim=1)
    confidence,pred=probs.max(dim=1)
report={
 'kind':'One stored test clip; no retraining or live camera',
 'raw_clip':rows[0]['raw_path'],'checkpoint_epoch':epoch,
 'input_shape':list(x.shape),'lstm_output_shape':list(sequence.shape),
 'hidden_shape':list(hidden.shape),'cell_shape':list(cell.shape),
 'last_timestep_shape':list(last.shape),'logits_shape':list(logits.shape),
 'true_label':CLASS_NAMES[int(targets[0])],
 'predicted_label':CLASS_NAMES[int(pred[0])],
 'confidence':float(confidence[0]),
 'forward_matches_explicit_steps':True,
 'code_locations':['features.py:extract_features','features.py:SequenceBuffer.push',
  'model.py:GestureLSTM.forward','model.py:predict_gesture','training.py:train_model'],
 'limitations':'This trace proves the execution path for one stored sequence; it is not a reproduction of IPN HandS code.'}
(S/'model_execution_trace.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
