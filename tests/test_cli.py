"""Check real CLI boundaries: paths, incompatible config and pending commands."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.config_path = self.root / "configs" / "default.json"
        self.config_path.parent.mkdir(parents=True)
        self.values = json.loads(
            (PROJECT_ROOT / "configs" / "default.json").read_text(encoding="utf-8")
        )
        self.cwd = Path(self.temp.name) / "another-directory"
        self.cwd.mkdir()

    def call_cli(self, command="check", values=None, extra_args=()):
        self.config_path.write_text(
            json.dumps(self.values if values is None else values), encoding="utf-8"
        )
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "hand_tracking", "--config", str(self.config_path), command, *extra_args],
            cwd=self.cwd,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

    def test_check_resolves_data_paths_against_project_instead_of_cwd(self):
        result = self.call_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(Path(report["paths"]["raw_dir"]), self.root / "data" / "raw")
        self.assertFalse(report["control_enabled"])
        self.assertFalse(report["resources"]["checkpoint"]["exists"])

    def test_rejects_incompatible_model_and_invalid_numeric_settings(self):
        invalid_values = (
            ("feature_dim", 42),
            ("num_classes", 4),
            ("sample_rate_hz", 0),
            ("sequence_length", True),
            ("confidence_threshold", 1.5),
            ("confidence_threshold", float("nan")),
            ("control_enabled", True),
        )
        for name, value in invalid_values:
            with self.subTest(setting=name, value=value):
                values = dict(self.values, **{name: value})
                result = self.call_cli(values=values)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(name, result.stderr)

    def test_rejects_missing_and_misspelled_settings(self):
        for values in (
            {key: value for key, value in self.values.items() if key != "sequence_length"},
            dict(self.values, sequence_lenght=30),
        ):
            result = self.call_cli(values=values)
            self.assertEqual(result.returncode, 2, result.stderr)

    def test_unimplemented_commands_return_error_instead_of_fake_success(self):
        for command in ("extract",):
            with self.subTest(command=command):
                result = self.call_cli(command)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("ROADMAP", result.stderr)

    def test_train_requires_positive_epochs(self):
        result = self.call_cli("train", extra_args=("--epochs", "0"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("--epochs must be positive", result.stderr)

    def test_headless_preview_requires_a_frame_limit(self):
        result = self.call_cli("preview", extra_args=("--headless",))
        self.assertEqual(result.returncode, 2)
        self.assertIn("--max-frames", result.stderr)

    def test_preview_reports_missing_landmarker_model(self):
        result = self.call_cli("preview", extra_args=("--headless", "--max-frames", "1"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("hand_landmarker.task", result.stderr)

    def test_collect_requires_an_explicit_session(self):
        result = self.call_cli("collect")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--session", result.stderr)

    def test_dataset_check_reports_empty_split_without_creating_data(self):
        result = self.call_cli("dataset-check", extra_args=("--split", "train"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("No clips", result.stderr)
        self.assertFalse((self.root / "data").exists())

    def test_collect_rejects_session_traversal_before_camera_access(self):
        result = self.call_cli("collect", extra_args=("--session", "../outside", "--max-frames", "1"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("session_id", result.stderr)
        self.assertFalse((self.root / "data").exists())

    def test_remove_defaults_to_preview_without_creating_data(self):
        result = self.call_cli("dataset-remove", extra_args=("--session", "pilot_01", "--label", "SWIPE_LEFT"))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["applied"])
        self.assertEqual(report["matched"], 0)
        self.assertFalse((self.root / "data").exists())

    def test_restore_refuses_backup_path_traversal(self):
        result = self.call_cli("dataset-restore", extra_args=("--backup-id", "../other"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("backup ID", result.stderr)


if __name__ == "__main__":
    unittest.main()
