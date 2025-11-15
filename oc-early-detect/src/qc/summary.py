"""Quality control utilities placeholder."""
from __future__ import annotations

from pathlib import Path

QC_TABLE = Path("reports/tables/qc_summary.csv")


def run_qc() -> None:
    """Placeholder QC routine writing an empty summary table."""
    QC_TABLE.parent.mkdir(parents=True, exist_ok=True)
    QC_TABLE.write_text("sample_id,label,depth,notes\n")
