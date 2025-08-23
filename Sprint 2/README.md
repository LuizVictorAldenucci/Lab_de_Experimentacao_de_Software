# GitHub Repo Audit – 1000 repos (CSV + Report)

## Passo a passo

1. **Python 3.10+** e dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. **Token do GitHub** (recomendado para maior limite de rate):
   - Crie um token em https://github.com/settings/tokens
   - Exporte no shell:
     ```bash
     export GITHUB_TOKEN=seu_token_aqui
     ```

3. **Coleta (até 1000 repositórios)**:
   ```bash
   python fetch_github_repos.py --query "stars:>10" --out repos.csv --max 1000 --sort stars --order desc
   ```a
   

4. **Análise + relatório inicial**:
   ```bash
   python analyze_repos.py --csv repos.csv --out report.md
   ```

Arquivos gerados:
- `repos.csv` – dados brutos dos repositórios.
- `report.md` – relatório com hipóteses informais e estatísticas iniciais.
- `charts/` – gráficos PNG.

> Dica: personalize a query (ex.: `language:Python pushed:>2024-08-01 stars:>50`) para focar no seu universo.
