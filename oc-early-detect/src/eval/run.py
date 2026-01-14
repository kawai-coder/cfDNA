"""Evaluation suite placeholder."""
from __future__ import annotations

from pathlib import Path

import yaml

REPORTS_DIR = Path("reports/tables")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def evaluate_models(config_path: str) -> None:
    """Write a stub evaluation table referencing the provided config."""
    config = yaml.safe_load(Path(config_path).read_text())
    report_path = REPORTS_DIR / "metrics_pending.csv"
    report_path.write_text("Evaluation pending; config summary:\n")
    report_path.write_text(
        report_path.read_text() + "keys," + ",".join(sorted(config.keys())) + "\n"
    )
