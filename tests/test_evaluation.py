"""Exercise the evaluation command with a known set of clip predictions."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from importlib.util import find_spec
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from hand_tracking.cli import main
from hand_tracking.dataset import DatasetStore
from hand_tracking.features import FEATURE_VERSION
from hand_tracking.labels import CLASS_NAMES, Gesture

from test_dataset import CONFIG, example_clip, temporary_config


@unittest.skipUnless(find_spec("torch"), "Evaluation requires PyTorch")
class EvaluationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config_path = self.root / "configs" / "default.json"
        self.config_path.parent.mkdir()
        self.config_path.write_text(CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
        self.config = replace(
            temporary_config(self.root), checkpoint_path=self.root / "models" / "gesture_lstm.pt"
        )
        self.report_path = self.config.output_dir / "evaluation.json"

    def save_checkpoint(self, **overrides):
        import torch
        from hand_tracking.model import GestureLSTM

        settings = {"feature_dim": 44, "hidden_size": 64, "num_layers": 1, "num_classes": 5}
        model = GestureLSTM(**settings)
        with torch.no_grad():
            for parameter in model.parameters():
                parameter.zero_()
            model.classifier.bias[Gesture.SWIPE_LEFT] = 1.0
        checkpoint = {
            "model_settings": settings,
            "model_state_dict": model.state_dict(),
            "class_names": list(CLASS_NAMES),
            "feature_version": FEATURE_VERSION,
            "sequence_length": 30,
            "sample_rate_hz": 20,
            "mirror": True,
            "epoch": 23,
        }
        checkpoint.update(overrides)
        self.config.checkpoint_path.parent.mkdir()
        torch.save(checkpoint, self.config.checkpoint_path)

    def run_evaluate(self):
        output, errors = StringIO(), StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(["--config", str(self.config_path), "evaluate"])
        return exit_code, output.getvalue(), errors.getvalue()

    def test_evaluate_reports_held_out_metrics_with_actual_labels_as_rows(self):
        self.save_checkpoint()
        train = DatasetStore(self.config, "train_01", "train")
        train.save(example_clip(), Gesture.SWIPE_LEFT)
        test = DatasetStore(self.config, "test_01", "test")
        first = test.save(example_clip(), Gesture.BACKGROUND)
        second = test.save(example_clip(), Gesture.BACKGROUND)
        test.save(example_clip(), Gesture.SWIPE_LEFT)

        exit_code, output, errors = self.run_evaluate()

        self.assertEqual(exit_code, 0, errors)
        report = json.loads(output)
        self.assertEqual(report, json.loads(self.report_path.read_text(encoding="utf-8")))
        self.assertEqual(report["split"], "test")
        self.assertEqual(report["sessions"], ["test_01"])
        self.assertEqual(report["checkpoint_epoch"], 23)
        self.assertEqual(report["samples"], 3)
        self.assertEqual(report["correct"], 1)
        self.assertAlmostEqual(report["accuracy"], 1 / 3)
        self.assertAlmostEqual(report["macro_f1"], 0.1)
        self.assertEqual(report["class_names"], list(CLASS_NAMES))
        self.assertEqual(report["confusion_matrix"], [
            [0, 2, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        self.assertEqual(report["per_class"]["SWIPE_LEFT"], {
            "support": 1, "precision": 1 / 3, "recall": 1.0, "f1": 0.5,
        })
        self.assertEqual(report["per_class"]["SWIPE_UP"]["f1"], 0.0)
        self.assertEqual(
            {row["clip_id"] for row in report["misclassified"]},
            {first["clip_id"], second["clip_id"]},
        )

    def test_evaluate_rejects_a_checkpoint_with_reversed_label_order(self):
        self.save_checkpoint(class_names=list(reversed(CLASS_NAMES)))

        exit_code, _, errors = self.run_evaluate()

        self.assertEqual(exit_code, 2)
        self.assertIn("class_names", errors)
        self.assertFalse(self.report_path.exists())

    def test_evaluate_explains_a_missing_checkpoint(self):
        exit_code, _, errors = self.run_evaluate()

        self.assertEqual(exit_code, 2)
        self.assertIn("gesture_lstm.pt", errors)
        self.assertFalse(self.report_path.exists())
