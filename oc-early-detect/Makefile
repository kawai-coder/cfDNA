.PHONY: help data features train eval clean

help:
@echo "Available commands:"
@echo "  make data     # download raw datasets"
@echo "  make features # generate fragmentomic/methyl features"
@echo "  make train    # fit models"
@echo "  make eval     # run evaluation and reporting"

ENV?=environment.yml
CONDA_ENV?=oc-early-detect

conda:
conda env create -f $(ENV)

data:
python -m src.cli.cli_data make

features:
python -m src.cli.cli_features make

train:
python -m src.cli.cli_train fit

eval:
python -m src.cli.cli_eval run

clean:
rm -rf data/interim/* data/processed/* reports/figures/* reports/tables/*
