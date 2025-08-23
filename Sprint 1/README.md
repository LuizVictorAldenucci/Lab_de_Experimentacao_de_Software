# GitHub Repo Popularity Analysis

## Passos

1. Configure seu token do GitHub:
```bash
export GITHUB_TOKEN=seu_token_aqui
```

2. Coletar os 1000 repositórios mais populares:
```bash
python fetch_github_repos.py --query "stars:>1" --out repos.csv --max 1000
```

3. Analisar resultados:
```bash
python analyze_repos.py --csv repos.csv --out report.md
```

O relatório final será salvo em `report.md`.
