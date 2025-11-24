"""Dataset downloaders and registry.

This module implements small-footprint downloaders for public datasets
referenced in :mod:`conf/datasets.yaml`. The goal is to make metadata and
manifests available locally while deferring large FASTQ/BAM transfers to
specialized tools (e.g., `prefetch`, `fasterq-dump`, or cloud sync).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Dict

import requests
import yaml

CONFIG_PATH = Path("conf/datasets.yaml")
DATA_ROOT = Path("data/raw")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _ensure_directories() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def download_dataset(dataset: str) -> None:
    """Dispatch download tasks based on the dataset key.

    Parameters
    ----------
    dataset:
        Dataset key defined in ``conf/datasets.yaml``. Use ``"all"`` to
        materialize every configured dataset.
    """

    _ensure_directories()
    config = yaml.safe_load(CONFIG_PATH.read_text())
    registry: Dict[str, Callable[[dict], None]] = {
        "gse71378": _download_gse71378,
        "finaledb": _download_finaledb,
    }

    if dataset == "all":
        for name, params in config.items():
            _invoke_downloader(name, params, registry)
    else:
        params = config.get(dataset)
        if params is None:
            raise KeyError(f"Dataset '{dataset}' not found in {CONFIG_PATH}")
        _invoke_downloader(dataset, params, registry)


def _invoke_downloader(
    name: str, params: dict, registry: Dict[str, Callable[[dict], None]]
) -> None:
    downloader = registry.get(name, _download_placeholder)
    logger.info("Downloading dataset: %s", name)
    downloader({"name": name, **(params or {})})


def _download_gse71378(config: dict) -> None:
    """Fetch GEO metadata and run table for the cfDNA 5-hmC study GSE71378.

    The downloader retrieves:
    * GEO series matrix (sample-level metadata)
    * SRA runinfo table for the study
    These artifacts are small (~MB-scale) and provide the manifests needed for
    subsequent FASTQ retrieval using SRA Toolkit or cloud mirrors.
    """

    accession = config.get("accession", "GSE71378")
    target = DATA_ROOT / config["name"]
    target.mkdir(parents=True, exist_ok=True)

    matrix_url = _geo_series_matrix_url(accession)
    runinfo_url = _sra_runinfo_url(accession)

    downloads = {
        target / f"{accession}_series_matrix.txt.gz": matrix_url,
        target / f"{accession}_runinfo.csv": runinfo_url,
    }

    for dest, url in downloads.items():
        _download_file(url, dest)

    (target / "README.txt").write_text(
        "GSE71378 metadata downloaded. Use SRA Toolkit (`prefetch`,\n"
        "`fasterq-dump`) or cloud mirrors to fetch FASTQ files listed in\n"
        "the runinfo table.\n"
    )


def _download_finaledb(config: dict) -> None:
    """Download FinaleDB release metadata manifests.

    FinaleDB publishes fragmentomics features and metadata. This downloader
    grabs the public sample manifest for the specified release so that users
    can mirror only the needed samples or feature matrices.
    """

    release = config.get("release", "v1.0")
    target = DATA_ROOT / config["name"]
    target.mkdir(parents=True, exist_ok=True)

    manifest_url = (
        "https://finaledb.s3.us-east-1.amazonaws.com/releases/"
        f"{release}/metadata/finaledb_{release}_sample_metadata.tsv"
    )

    dest = target / f"finaledb_{release}_sample_metadata.tsv"
    _download_file(manifest_url, dest)

    (target / "README.txt").write_text(
        "FinaleDB sample metadata downloaded. Use the manifest to locate\n"
        "feature matrices or alignments for the desired cohort.\n"
    )


def _download_placeholder(config: dict) -> None:
    """Fallback downloader until an explicit implementation is provided."""

    target = DATA_ROOT / config["name"]
    target.mkdir(parents=True, exist_ok=True)
    (target / "README.txt").write_text(
        "Placeholder for dataset download. Populate with real fetch logic.\n"
    )


def _download_file(url: str, dest: Path, chunk_size: int = 1_048_576) -> None:
    """Stream a remote file to ``dest`` if it does not already exist."""

    if dest.exists():
        logger.info("File exists, skipping: %s", dest)
        return

    logger.info("Fetching %s -> %s", url, dest)
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                fh.write(chunk)


def _geo_series_matrix_url(accession: str) -> str:
    """Construct the GEO FTP URL for the series matrix."""

    prefix = accession[:-3] + "nnn"
    return (
        "https://ftp.ncbi.nlm.nih.gov/geo/series/"
        f"{prefix}/{accession}/matrix/{accession}_series_matrix.txt.gz"
    )


def _sra_runinfo_url(accession: str) -> str:
    """Construct the NCBI SRA runinfo URL for a GEO accession."""

    return (
        "https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?"
        f"save=efetch&db=sra&rettype=runinfo&term={accession}"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download configured datasets")
    parser.add_argument(
        "--dataset",
        default="all",
        help="Dataset key (or 'all') as defined in conf/datasets.yaml",
    )
    args = parser.parse_args()
    download_dataset(args.dataset)
