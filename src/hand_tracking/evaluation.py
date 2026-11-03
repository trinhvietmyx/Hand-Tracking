"""Evaluate a trained gesture classifier on the held-out clips."""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import torch

from .config import ProjectConfig
from .dataset import load_split
from .labels import CLASS_NAMES
from .model import load_gesture_model


def evaluate_model(config: ProjectConfig) -> dict:
    model, epoch = load_gesture_model(config)
    features, targets, rows = load_split(config, "test")
    with torch.inference_mode():
        logits = model(torch.from_numpy(features))
        if not torch.isfinite(logits).all():
            raise ValueError("Model returned non-finite scores.")
        predictions = logits.argmax(dim=1).numpy()

    matrix = np.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=np.int64)
    np.add.at(matrix, (targets, predictions), 1)
    per_class = {}
    for index, name in enumerate(CLASS_NAMES):
        true_positives = int(matrix[index, index])
        actual = int(matrix[index, :].sum())
        predicted = int(matrix[:, index].sum())
        per_class[name] = {
            "support": actual,
            "precision": true_positives / predicted if predicted else 0.0,
            "recall": true_positives / actual if actual else 0.0,
            "f1": 2 * true_positives / (actual + predicted) if actual + predicted else 0.0,
        }

    correct = int(matrix.trace())
    report = {
        "split": "test",
        "sessions": sorted({row["session_id"] for row in rows}),
        "checkpoint_path": str(config.checkpoint_path),
        "checkpoint_epoch": epoch,
        "samples": len(targets),
        "correct": correct,
        "accuracy": correct / len(targets),
        "macro_f1": sum(metrics["f1"] for metrics in per_class.values()) / len(CLASS_NAMES),
        "class_names": list(CLASS_NAMES),
        "per_class": per_class,
        "confusion_matrix_axes": {"rows": "actual", "columns": "predicted"},
        "confusion_matrix": matrix.tolist(),
        "misclassified": [
            {
                "clip_id": row["clip_id"],
                "raw_path": row["raw_path"],
                "actual": CLASS_NAMES[actual],
                "predicted": CLASS_NAMES[predicted],
            }
            for row, actual, predicted in zip(rows, targets, predictions, strict=True)
            if actual != predicted
        ],
    }

    config.output_dir.mkdir(parents=True, exist_ok=True)
    destination = config.output_dir / "evaluation.json"
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=config.output_dir, suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(report, temporary, indent=2)
            temporary.write("\n")
        temporary_path.replace(destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return report
