"""Load the local project configuration without importing camera or ML libraries."""

from dataclasses import dataclass, fields
import json
import math
from pathlib import Path

from .labels import Gesture


class ConfigError(ValueError):
    """Configuration cannot be used by the current project contract."""


@dataclass(frozen=True)
class ProjectConfig:
    project_root: Path
    camera_index: int
    frame_width: int
    frame_height: int
    mirror: bool
    sequence_length: int
    sample_rate_hz: int
    feature_dim: int
    hidden_size: int
    num_layers: int
    num_classes: int
    confidence_threshold: float
    stable_ms: int
    min_predictions: int
    cooldown_ms: int
    background_ms: int
    control_enabled: bool
    toggle_key: str
    stop_key: str
    scroll_steps: int
    raw_dir: Path
    processed_dir: Path
    output_dir: Path
    checkpoint_path: Path
    landmarker_path: Path


def load_config(path: str | Path) -> ProjectConfig:
    """Resolve paths from the project containing configs/<name>.json, not from cwd."""
    config_path = Path(path).expanduser().resolve()
    try:
        values = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        raise ConfigError(f"Cannot read configuration {config_path}: {error}") from error
    if not isinstance(values, dict):
        raise ConfigError("Configuration must be a JSON object.")

    expected = {field.name for field in fields(ProjectConfig)} - {"project_root"}
    missing = expected - values.keys()
    unknown = values.keys() - expected
    if missing:
        raise ConfigError(f"Missing settings: {', '.join(sorted(missing))}")
    if unknown:
        raise ConfigError(f"Unknown settings: {', '.join(sorted(unknown))}")

    positive_ints = (
        "frame_width", "frame_height", "sequence_length", "sample_rate_hz",
        "feature_dim", "hidden_size", "num_layers", "num_classes", "stable_ms",
        "min_predictions", "cooldown_ms", "background_ms", "scroll_steps",
    )
    for name in positive_ints:
        if type(values[name]) is not int or values[name] <= 0:
            raise ConfigError(f"{name} must be a positive integer.")
    if type(values["camera_index"]) is not int or values["camera_index"] < 0:
        raise ConfigError("camera_index must be a non-negative integer.")
    if type(values["mirror"]) is not bool:
        raise ConfigError("mirror must be true or false.")
    if values["control_enabled"] is not False:
        raise ConfigError("control_enabled must be false; enable control explicitly at runtime.")
    if values["feature_dim"] != 44:
        raise ConfigError("feature_dim must be 44 for the current feature contract.")
    if values["num_classes"] != len(Gesture):
        raise ConfigError("num_classes must be 5 for the current label contract.")

    threshold = values["confidence_threshold"]
    if (type(threshold) not in (int, float) or not math.isfinite(threshold)
            or not 0 < threshold <= 1):
        raise ConfigError("confidence_threshold must be finite and in (0, 1].")

    function_keys = {f"f{number}" for number in range(1, 13)}
    for name in ("toggle_key", "stop_key"):
        if not isinstance(values[name], str) or values[name] not in function_keys:
            raise ConfigError(f"{name} must be a lowercase function key f1 through f12.")
    if values["toggle_key"] == values["stop_key"]:
        raise ConfigError("toggle_key and stop_key must be different.")

    project_root = config_path.parent.parent
    for name in ("raw_dir", "processed_dir", "output_dir", "checkpoint_path", "landmarker_path"):
        value = values[name]
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"{name} must be a non-empty path string.")
        values[name] = (project_root / Path(value).expanduser()).resolve()
    return ProjectConfig(project_root=project_root, **values)
