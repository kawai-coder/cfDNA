"""Feature engineering pipeline placeholder."""
from __future__ import annotations

from pathlib import Path

import yaml

CONF_PATH = Path("conf/datasets.yaml")
OUTPUT_FRAGMENT = Path("data/interim/fragment_features.parquet")
OUTPUT_METHYL = Path("data/interim/methyl_features.parquet")


def build_features(force: bool = False) -> None:
    """Generate fragmentomic and methylation features according to config."""
    OUTPUT_FRAGMENT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_METHYL.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FRAGMENT.exists() and not force:
        return

    datasets = yaml.safe_load(CONF_PATH.read_text())
    _write_placeholder(OUTPUT_FRAGMENT, "fragment", datasets)
    _write_placeholder(OUTPUT_METHYL, "methyl", datasets)


def _write_placeholder(path: Path, feature_type: str, datasets: dict) -> None:
    placeholder = (
        "This is a placeholder for {ft} features. Replace with actual computation.\n"
    ).format(ft=feature_type)
    path.write_text(placeholder)
