# Lab03S03 — Análise & Visualização (Code Review no GitHub)

Esta entrega inclui:
- `analysis/analyze.py`: roda as análises (medianas, correlações) e gera gráficos.
- `outputs/`: resultados de exemplo gerados a partir de um **dataset sintético**.
- `docs/Relatorio_Lab03S03.md`: **relatório final** com resultados e discussão.

## Como rodar

### 1) Ambiente
```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Dataset
- Para resultados oficiais, gere `data/prs_dataset.csv` a partir da **Lab03S02** e coloque-o em `data/`.
- Caso não exista, você pode usar o dataset sintético já incluído: `data/prs_dataset_sintetico.csv`.

### 3) Executar a análise
```bash
python analysis/analyze.py --csv data/prs_dataset.csv --csv-fallback data/prs_dataset_sintetico.csv --outdir outputs
```
- Resultados numéricos: `outputs/medianas_gerais.csv`, `outputs/medianas_por_status.csv`, `outputs/correlacoes_spearman.csv`
- Gráficos: `outputs/plots/*.png`
- Relatório: `docs/Relatorio_Lab03S03.md` (pode ser refeito conforme os novos resultados).

> Observação: As visualizações utilizam **matplotlib** e cada gráfico é gerado em arquivo **individual**.
