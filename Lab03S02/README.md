# Lab03S02 — Dataset + Relatório (Hipóteses)
Inclui scripts de coleta (GraphQL), **dataset real** gerável com token e um **dataset sintético** (offline) para demonstração, além do **relatório inicial** (hipóteses).
Veja `docs/Relatorio_Lab03S02.md` e rode:
```
python src/select_repos.py
python src/collect_prs.py --max-prs-por-repo 1000
python analysis/summarize_medians.py --csv data/prs_dataset.csv
python analysis/corr_tests.py --csv data/prs_dataset.csv --method spearman
```
