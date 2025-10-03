# Lab03S01 — Code Review no GitHub (Seleção de Repositórios + Script de Coleta)

Este pacote entrega **apenas a etapa Lab03S01**:
1) **Seleção dos repositórios** (top 200 do GitHub por estrelas, com pelo menos 100 PRs fechados/mesclados).
2) **Script de coleta** dos PRs e das métricas definidas no enunciado, pronto para gerar o dataset na próxima etapa.

> **Importante:** você precisará de um **GitHub Personal Access Token** com permissão pública de leitura (`read:public_repo`).  
> Salve-o em uma variável de ambiente `GITHUB_TOKEN` (ou use um `.env`).

## Estrutura

```
Lab03S01-CodeReview-GitHub/
├─ src/
│  ├─ select_repos.py        # Busca e filtra os 200 repositórios-alvo
│  ├─ collect_prs.py         # Coleta PRs e métricas (pronto para Lab03S02)
│  ├─ utils.py               # Funções auxiliares (GraphQL, paginação, rate limit)
│  └─ schemas.py             # Colunas/validações básicas do CSV
├─ data/
│  ├─ repositorios_selecionados.csv  # Gerado pelo select_repos.py
│  └─ (datasets serão salvos aqui)
├─ scripts/
│  └─ run_all.sh             # Exemplo de execução
├─ requirements.txt
├─ .env.example
└─ README.md
```

## Como usar

### 1) Instalar dependências
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2) Configurar o token
Crie um arquivo `.env` a partir do `.env.example` **ou** exporte a variável:
```bash
cp .env.example .env
# edite o valor do token no arquivo
# ou use:
export GITHUB_TOKEN="SEU_TOKEN_AQUI"
```

### 3) Selecionar repositórios (gera `data/repositorios_selecionados.csv`)
```bash
python src/select_repos.py
```

### 4) (Opcional nesta etapa) Coletar PRs e métricas — pronto para a Lab03S02
```bash
python src/collect_prs.py --max-prs-por-repo 1000
```
O script respeita os filtros do enunciado:
- Estados: `MERGED` ou `CLOSED`;
- Pelo menos **1 revisão** (`reviews.totalCount >= 1`);
- Intervalo entre criação e fechamento/merge de **≥ 1 hora**.

### Métricas coletadas
- **Tamanho:** `changedFiles`, `additions`, `deletions`  
- **Tempo de Análise:** `tempo_analise_horas` (diferença entre `createdAt` e `mergedAt/closedAt`)  
- **Descrição:** `desc_len` (nº de caracteres do `bodyText`)  
- **Interações:** `participants.totalCount`, `comments.totalCount`  
- **Status do PR:** `state` (`MERGED` ou `CLOSED`)  
- **Nº de revisões:** `reviews.totalCount`

### Observações técnicas
- Uso da **API GraphQL do GitHub** (v4) para eficiência e contadores (`totalCount`).  
- Tratamento básico de **rate limit** (backoff exponencial e reexecução).  
- Paginação robusta (cursor-based).  
- Saídas em **CSV** para fácil ingestão nas etapas seguintes.

Boa pesquisa! :)
