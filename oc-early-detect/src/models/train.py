"""Training orchestration for baseline and transformer models."""
from __future__ import annotations

from pathlib import Path

import yaml

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def train_models(config_path: str) -> None:
    """Placeholder training routine that records config usage."""
    config = yaml.safe_load(Path(config_path).read_text())
    summary_path = MODEL_DIR / "TRAINING_PENDING.txt"
    summary_path.write_text(
        "Training not yet implemented. Config entries:\n" + yaml.dump(config)
    )
