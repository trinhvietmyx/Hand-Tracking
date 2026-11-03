"""Hardware-free configuration checks and honest entry points for future work."""

import argparse
from collections import Counter
from dataclasses import replace
from importlib import metadata
import json
from pathlib import Path
import sys

from . import __version__
from .config import ConfigError, load_config
from .labels import CLASS_NAMES, Gesture


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hand-tracking",
        description="Foundation for four dynamic gestures and touchless slide/page control.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--config", type=Path, default=Path("configs/default.json"),
        help="Configuration in <project>/configs/ (default: configs/default.json).",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Check configuration and resource paths; no hardware access.")
    preview = commands.add_parser("preview", help="Preview one hand, 44 features and the time buffer; no OS control.")
    run = commands.add_parser("run", help="Recognize gestures from the webcam.")
    for camera_command in (preview, run):
        camera_command.add_argument("--headless", action="store_true")
        camera_command.add_argument("--max-frames", type=int)
        camera_command.add_argument("--camera-index", type=int)
    collect = commands.add_parser("collect", help="Record labelled clips with SPACE/countdown and resume a session.")
    collect.add_argument("--session", required=True, help="Session ID, for example pilot_01 (letters/digits/_/-).")
    collect.add_argument("--split", choices=("train", "validation", "test"), default="train")
    collect.add_argument("--count", type=int, default=10, help="Target clips per label in this session, including existing clips.")
    collect.add_argument("--label", choices=CLASS_NAMES, help="Record only this label; default: all five labels.")
    collect.add_argument("--countdown", type=float, default=2, help="Seconds between SPACE and recording (default: 2).")
    collect.add_argument("--camera-index", type=int, help="Override camera index for this run.")
    collect.add_argument("--max-frames", type=int, help="Optional limit for a short camera/setup check.")
    dataset_check = commands.add_parser("dataset-check", help="Validate saved NPZ/video references and report split counts.")
    dataset_check.add_argument("--split", choices=("train", "validation", "test"), default="train")
    remove = commands.add_parser("dataset-remove", help="Preview removal of one session/label; --apply moves files to backup.")
    remove.add_argument("--session", required=True)
    remove.add_argument("--split", choices=("train", "validation", "test"), default="train")
    remove.add_argument("--label", choices=CLASS_NAMES, required=True)
    remove.add_argument("--last", action="store_true", help="Select only the latest matching clip instead of all matching clips.")
    remove.add_argument("--apply", action="store_true", help="Apply removal; default is a read-only preview.")
    restore = commands.add_parser("dataset-restore", help="Preview restoration from a removal backup; --apply restores files.")
    restore.add_argument("--backup-id", required=True, help="removal_id printed by dataset-remove --apply.")
    restore.add_argument("--apply", action="store_true", help="Apply restoration; default is a read-only preview.")
    train = commands.add_parser("train", help="Train the gesture LSTM.")
    train.add_argument("--epochs", type=int, default=30)
    commands.add_parser("evaluate", help="Evaluate the trained model on held-out test clips.")
    pending = {
        "extract": "features.py and dataset.py",
    }
    for command, module in pending.items():
        commands.add_parser(command, help=f"Planned entry point; implement {module} first.")
    arguments = parser.parse_args(argv)
    try:
        config = load_config(arguments.config)
    except ConfigError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2

    if arguments.command == "train":
        if arguments.epochs < 1:
            parser.error("--epochs must be positive")

        from .training import train_model

        train_model(config, epochs=arguments.epochs)
        return 0

    if arguments.command == "evaluate":
        try:
            from .evaluation import evaluate_model

            summary = evaluate_model(config)
        except ImportError as error:
            print(f"Missing evaluation dependency: {error}. Install PyTorch in the project environment.", file=sys.stderr)
            return 2
        except (OSError, RuntimeError, ValueError) as error:
            print(f"Evaluation error: {error}", file=sys.stderr)
            return 2
        print(json.dumps(summary, indent=2))
        return 0

    if arguments.command in ("preview", "run"):
        if arguments.headless and arguments.max_frames is None:
            parser.error("preview --headless requires --max-frames N")
        if arguments.max_frames is not None and arguments.max_frames < 1:
            parser.error("--max-frames must be positive")
        if arguments.camera_index is not None:
            if arguments.camera_index < 0:
                parser.error("--camera-index must be non-negative")
            config = replace(config, camera_index=arguments.camera_index)
        try:
            from .app import run_preview

            summary = run_preview(
                config,
                headless=arguments.headless,
                max_frames=arguments.max_frames,
                predict=arguments.command == "run",
            )
        except ImportError as error:
            print(
                f"Missing vision dependency: {error}. "
                "Install with: python -m pip install -e '.[vision]'",
                file=sys.stderr,
            )
            return 2
        except (OSError, RuntimeError, ValueError) as error:
            print(f"Preview error: {error}", file=sys.stderr)
            return 2
        except KeyboardInterrupt:
            print("Preview stopped.", file=sys.stderr)
            return 130
        print(json.dumps(summary, indent=2))
        return 0

    if arguments.command in ("collect", "dataset-check", "dataset-remove", "dataset-restore"):
        try:
            if arguments.command == "collect":
                if arguments.camera_index is not None:
                    if arguments.camera_index < 0:
                        parser.error("--camera-index must be non-negative")
                    config = replace(config, camera_index=arguments.camera_index)
                from .collection import collect_clips

                labels = None if arguments.label is None else [Gesture[arguments.label]]
                summary = collect_clips(config, arguments.session, arguments.split, arguments.count,
                                        labels=labels, countdown_seconds=arguments.countdown,
                                        max_frames=arguments.max_frames)
            elif arguments.command == "dataset-remove":
                from .dataset_cleanup import remove_recordings

                summary = remove_recordings(config, arguments.session, arguments.split,
                                            Gesture[arguments.label], last=arguments.last, apply=arguments.apply)
            elif arguments.command == "dataset-restore":
                from .dataset_cleanup import restore_recordings

                summary = restore_recordings(config, arguments.backup_id, apply=arguments.apply)
            else:
                from .dataset import load_split

                X, y, rows = load_split(config, arguments.split)
                counts = Counter(y.tolist())
                summary = {"status": "valid", "split": arguments.split, "samples": len(y),
                           "input_shape": list(X.shape), "counts": {name: counts[index] for index, name in enumerate(CLASS_NAMES)},
                           "sessions": sorted({row["session_id"] for row in rows})}
        except ImportError as error:
            print(f"Missing vision dependency: {error}. Install with: python -m pip install -e '.[vision]'", file=sys.stderr)
            return 2
        except (OSError, RuntimeError, ValueError) as error:
            print(f"Dataset/collection error: {error}", file=sys.stderr)
            return 2
        except KeyboardInterrupt:
            print("Collection stopped; completed clips remain saved.", file=sys.stderr)
            return 130
        print(json.dumps(summary, indent=2))
        return 0

    if arguments.command != "check":
        print(
            f"'{arguments.command}' is not implemented in this foundation. "
            f"Implement src/hand_tracking/{pending[arguments.command]}; see docs/ROADMAP.md.",
            file=sys.stderr,
        )
        return 2

    paths = {
        name: str(getattr(config, name))
        for name in ("raw_dir", "processed_dir", "output_dir", "checkpoint_path", "landmarker_path")
    }
    dependencies = {}
    for package in ("numpy", "opencv-contrib-python", "mediapipe", "torch", "pyautogui", "pynput", "scikit-learn"):
        try:
            dependencies[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            dependencies[package] = None
    report = {
        "status": "foundation_ready",
        "application_implemented": False,
        "preview_implemented": True,
        "collection_implemented": True,
        "project_root": str(config.project_root),
        "input_shape": [config.sequence_length, config.feature_dim],
        "sample_rate_hz": config.sample_rate_hz,
        "class_names": CLASS_NAMES,
        "control_enabled": config.control_enabled,
        "paths": paths,
        "resources": {
            "checkpoint": {"path": paths["checkpoint_path"], "exists": config.checkpoint_path.is_file()},
            "hand_landmarker": {"path": paths["landmarker_path"], "exists": config.landmarker_path.is_file()},
        },
        "dependencies": dependencies,
    }
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0
