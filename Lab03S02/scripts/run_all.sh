#!/usr/bin/env bash
set -euo pipefail
python src/select_repos.py
python src/collect_prs.py --max-prs-por-repo 1000
python analysis/summarize_medians.py --csv data/prs_dataset.csv
python analysis/corr_tests.py --csv data/prs_dataset.csv --method spearman
