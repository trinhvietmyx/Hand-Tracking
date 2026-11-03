from pickle import UnpicklingError

import torch
from torch import nn

from .config import ProjectConfig
from .features import FEATURE_VERSION
from .labels import CLASS_NAMES, Gesture


class GestureLSTM(nn.Module):
    def __init__(self, feature_dim, hidden_size, num_layers, num_classes):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=feature_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, features):
        sequence, _ = self.lstm(features)
        return self.classifier(sequence[:, -1, :])


def load_gesture_model(config: ProjectConfig) -> tuple[GestureLSTM, int]:
    try:
        checkpoint = torch.load(config.checkpoint_path, map_location="cpu", weights_only=True)
    except (UnpicklingError, EOFError) as error:
        raise ValueError(f"Cannot read checkpoint {config.checkpoint_path}: {error}") from error
    if not isinstance(checkpoint, dict):
        raise ValueError("Checkpoint must contain a dictionary of weights and metadata.")

    model_settings = {
        "feature_dim": config.feature_dim,
        "hidden_size": config.hidden_size,
        "num_layers": config.num_layers,
        "num_classes": config.num_classes,
    }
    expected = {
        "model_settings": model_settings,
        "class_names": list(CLASS_NAMES),
        "feature_version": FEATURE_VERSION,
        "sequence_length": config.sequence_length,
        "sample_rate_hz": config.sample_rate_hz,
        "mirror": config.mirror,
    }
    for name, value in expected.items():
        if checkpoint.get(name) != value:
            raise ValueError(f"Checkpoint {name} does not match the current configuration.")

    state = checkpoint.get("model_state_dict")
    epoch = checkpoint.get("epoch")
    if not isinstance(state, dict) or type(epoch) is not int or epoch < 1:
        raise ValueError("Checkpoint must contain model weights and a positive epoch.")

    model = GestureLSTM(**model_settings)
    model.load_state_dict(state)
    model.eval()
    return model, epoch


@torch.inference_mode()
def predict_gesture(model, sequence) -> tuple[Gesture, float]:
    features = torch.from_numpy(sequence).unsqueeze(0)
    logits = model(features)
    probabilities = logits.softmax(dim=1)
    confidence, label_id = probabilities.max(dim=1)
    return Gesture(label_id.item()), confidence.item()
