# Ovarian Cancer cfDNA Early Detection

This repository scaffolds a full pipeline for developing cfDNA-based early detection models for ovarian cancer. It is organized to support reproducible data acquisition, feature engineering, modeling (baselines and transformer-style models), and reporting for paper-ready deliverables.

## Repository layout

```
oc-early-detect/
  data/
    raw/           # .fastq/.bam or processed matrices
    interim/       # per-sample feature dumps
    processed/     # model-ready tables
  conf/
    datasets.yaml  # dataset paths, filters, labels
    modeling.yaml  # model & training params
  src/
    io/            # downloaders, parsers
    qc/            # read-level, sample-level QC
    features/      # fragmentomics & methylation featurizers
    models/        # baselines, transformer
    eval/          # metrics, calibration, CI, plots
    cli/           # entrypoints (e.g., cli_train.py)
  notebooks/
    00_explore.ipynb
    01_baselines.ipynb
    02_transformer.ipynb
  reports/
    figures/
    tables/
  Makefile
  environment.yml
  README.md
```

## Getting started

1. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate oc-early-detect
   ```
2. Inspect dataset configuration in `conf/datasets.yaml` and update with local paths or download settings.
3. Pull raw data and metadata:
   ```bash
   make data
   ```
4. Derive features, train models, and run evaluations:
   ```bash
   make features
   make train
   make eval
   ```

## Issue backlog & definitions of done

### Issue 1 — Environment & reproducibility
- **Goal:** Provide a replicable environment and Makefile entrypoints.
- **DoD:** `conda env create -f environment.yml` works; `make --help` lists the canonical commands.

### Issue 2 — Data acquisition module
- **Goal:** Implement downloaders for FinaleDB and GEO/SRA (GSE71378).
- **DoD:** `python -m src.io.download --dataset gse71378` populates `data/raw/...`.

### Issue 3 — QC & metadata normalization
- **Goal:** Compute WGS/5-hmC quality metrics and harmonize sample metadata.
- **DoD:** `reports/tables/qc_summary.csv` populated with per-sample QC and outlier flags.

### Issue 4 — Fragmentomics featurizer (WGS)
- **Goal:** Implement fragment length histograms, 5′ motif frequencies, and coverage metrics.
- **DoD:** `data/interim/fragment_features.parquet` has `[n_samples, n_features]` with tests.

### Issue 5 — Methylation featurizer
- **Goal:** Generate windowed methylation/5-hmC features and DMR summaries.
- **DoD:** `data/interim/methyl_features.parquet` created with logged feature schema.

### Issue 6 — Data splits (study-aware)
- **Goal:** Build grouped splits and confirm no site leakage.
- **DoD:** `reports/tables/splits.csv` lists splits; leakage checks documented.

### Issue 7 — Baseline models
- **Goal:** Fit logistic regression and gradient-boosted trees with calibration.
- **DoD:** Saved models in `models/baselines/*.pkl`; ROC curves generated.

### Issue 8 — Thresholding for high specificity
- **Goal:** Lock ≥99% specificity threshold on validation and evaluate on test/external.
- **DoD:** `reports/tables/metrics.csv` with metrics and bootstrap CIs.

### Issue 9 — Calibration & PPV reporting
- **Goal:** Produce calibration diagnostics and PPV estimates for target prevalences.
- **DoD:** Reliability plots and `reports/tables/ppv_table.csv` available.

### Issue 10 — Leakage & confounding audits
- **Goal:** Detect study/batch confounders and quantify sensitivity to depth/read length.
- **DoD:** `reports/tables/confound_audit.csv` plus narrative summary.

### Issue 11 — Transformer/LLM-style model (Evo-like track)
- **Goal:** Implement fragment/methylation token encoders and optional self-supervision.
- **DoD:** Saved checkpoints in `models/transformer/*.pt`; scripts benchmarked for resources.

### Issue 12 — External validation run
- **Goal:** Freeze preprocessing, threshold, and evaluate on independent dataset.
- **DoD:** `reports/tables/external_metrics.csv` and ROC/PR plots.

### Issue 13 — Paper-ready artifacts
- **Goal:** Assemble final tables/figures (datasets, metrics, pipeline, ROC, calibration).
- **DoD:** `reports/` contains publication-ready figures (SVG/PNG) and tables (CSV).

## Notebooks

Use the numbered notebooks for exploration, baseline modeling, and transformer experimentation. They should follow the order `00_explore` → `01_baselines` → `02_transformer`.

## Contributing

1. Create feature branches for each issue.
2. Ensure `make format`/`make test` (to be added) succeed before opening pull requests.
3. Document major findings in `reports/` and keep notebooks under version control using tools like `jupytext` if desired.
