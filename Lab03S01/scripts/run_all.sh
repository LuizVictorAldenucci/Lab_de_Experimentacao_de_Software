#!/usr/bin/env bash
set -euo pipefail

python src/select_repos.py
python src/collect_prs.py --max-prs-por-repo 1000
