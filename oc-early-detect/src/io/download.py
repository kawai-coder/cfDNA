"""Dataset downloaders and registry."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict

import yaml

CONFIG_PATH = Path("conf/datasets.yaml")
DATA_ROOT = Path("data/raw")


def _ensure_directories() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def download_dataset(dataset: str) -> None:
    """Dispatch download tasks based on the dataset key."""
    _ensure_directories()
    config = yaml.safe_load(CONFIG_PATH.read_text())
    registry: Dict[str, Callable[[dict], None]] = {
        "gse71378": _download_placeholder,
        "finaledb": _download_placeholder,
    }
    if dataset == "all":
        for name, params in config.items():
            _invoke_downloader(name, params, registry)
    else:
        params = config.get(dataset)
        if params is None:
            raise KeyError(f"Dataset '{dataset}' not found in {CONFIG_PATH}")
        _invoke_downloader(dataset, params, registry)


def _invoke_downloader(name: str, params: dict, registry: Dict[str, Callable[[dict], None]]) -> None:
    downloader = registry.get(name, _download_placeholder)
    downloader({"name": name, **(params or {})})


def _download_placeholder(config: dict) -> None:
    """Placeholder downloader until implementation."""
    target = DATA_ROOT / config["name"]
    target.mkdir(parents=True, exist_ok=True)
    (target / "README.txt").write_text(
        "Placeholder for dataset download. Populate with real fetch logic.\n"
    )
