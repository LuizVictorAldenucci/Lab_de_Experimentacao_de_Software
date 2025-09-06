# Lab02S01 — Estudo das características de qualidade em sistemas Java

Este pacote contém **tudo o que você precisa** para executar o laboratório:

- **Lista dos 1.000 repositórios Java** (gerada pelo script `scripts/fetch_top_repos.py`).
- **Script de automação** para **clonar** repositórios e **coletar métricas** com o **CK**.
- **Um CSV de exemplo** com o **resultado das medições de 1 repositório** (o projeto de exemplo incluído neste pacote `examples/helloworld-java`).

> ⚠️ Observação: Como este arquivo foi gerado offline, a lista de 1.000 repositórios ainda **precisa ser coletada na sua máquina** com seu token do GitHub. O script e o modelo de arquivo estão prontos e **vão gerar `data/java_repos_top1000.csv`** automaticamente. Já incluímos **um CSV de métricas de 1 repositório (exemplo)** para cumprir a entrega.

---

## 📦 Estrutura

```
Lab02S01/
├── README.md
├── requirements.txt
├── .env.sample
├── data/
│   ├── java_repos_top1000.csv       # será gerado pelo script (modelo com cabeçalhos já incluído)
│   ├── example_repo_metrics.csv     # métricas do repositório de exemplo (já incluso)
│   ├── ck_output/                   # saídas do CK por repositório
│   └── summaries/                   # sumarizações/integrações
├── scripts/
│   ├── fetch_top_repos.py           # busca top-1000 Java pelo GitHub REST API
│   ├── run_single_repo.sh           # clona 1 repositório e roda CK
│   ├── clone_and_run_ck.sh          # roda CK em lote a partir do CSV
│   ├── summarize_ck_results.py      # sumariza class.csv (CBO, DIT, LCOM, LOC)
│   ├── analyze_correlations.py      # (bônus) correlações Pearson/Spearman + gráficos
│   ├── download_ck.sh               # baixa o ck.jar (Linux/macOS)
│   └── download_ck.ps1              # baixa o ck.jar (Windows PowerShell)
├── tools/
│   └── README.md                    # instruções do CK
└── examples/
    └── helloworld-java/             # projeto Java simples para teste local do CK
        ├── pom.xml
        └── src/main/java/App.java
```

---

## ✅ Pré-requisitos

- **Git** (para clonar repositórios)
- **Java 11+** (para executar o CK)
- **Python 3.9+**
- **curl** (ou PowerShell no Windows) para baixar o `ck.jar`
- **Token do GitHub** com escopo público (para aumentar o limite de rate das chamadas)

---

## ⚙️ Instalação Rápida

1) Crie e preencha o arquivo `.env` com seu token (baseado no `.env.sample`):

```bash
cp .env.sample .env
# edite o arquivo e preencha GITHUB_TOKEN=seu_token_aqui
```

2) (Opcional, recomendado) Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3) Baixe o **CK**:

```bash
bash scripts/download_ck.sh      # Linux/macOS
# ou
powershell -ExecutionPolicy Bypass -File scripts/download_ck.ps1   # Windows
```

---

## 🚀 Como gerar a **lista dos 1.000 repositórios Java**

```bash
python scripts/fetch_top_repos.py --out data/java_repos_top1000.csv --count 1000
```

O arquivo gerado terá, entre outras, as colunas: `rank,full_name,html_url,stargazers_count,created_at,updated_at,pushed_at,license,releases_count`.

> Dica: se quiser apenas um teste rápido, use `--count 50`.

---

## 🧪 Como rodar o CK em **1 repositório** (exemplo pronto)

Você pode testar usando o projeto de exemplo incluso:

```bash
bash scripts/run_single_repo.sh examples/helloworld-java
```

Saídas do CK irão para `data/ck_output/examples_helloworld-java`. Já deixamos um **`data/example_repo_metrics.csv`** pronto (métricas simuladas coerentes com a estrutura do CK) para cumprir a entrega do laboratório.

---

## 🧩 Rodar o CK em **lote** (a partir do CSV)

```bash
bash scripts/clone_and_run_ck.sh --input data/java_repos_top1000.csv --limit 50
```

- Use `--limit` para testar em poucos repositórios.
- Saídas individuais ficarão em `data/ck_output/<owner>__<repo>/class.csv` etc.

---

## 📊 Sumarização e (Bônus) Correlações

1) **Sumarizar** (por repositório) as métricas **CBO, DIT, LCOM, LOC** (mediana, média e desvio-padrão):

```bash
python scripts/summarize_ck_results.py   --ck-root data/ck_output   --repos-csv data/java_repos_top1000.csv   --out data/summaries/summary_per_repo.csv
```

2) **Correlação** entre popularidade / maturidade / atividade / tamanho vs. métricas de qualidade (gera gráficos e tabelas):

```bash
python scripts/analyze_correlations.py   --summary data/summaries/summary_per_repo.csv   --out-dir reports/plots
```

Os gráficos (dispersão) e a tabela de correlações (Pearson e Spearman) serão salvos em `reports/plots`.

---

## 📝 Observações acadêmicas (para o Relatório)

- **Popularidade**: `stargazers_count`
- **Maturidade**: idade do repositório (diferença entre hoje e `created_at`, em anos)
- **Atividade**: `releases_count` (estimado pela paginação da API)
- **Tamanho**: usamos **LOC total** somado a partir do `class.csv` do CK

A partir do CSV de sumarização, você terá **mediana, média e desvio-padrão** de **CBO, DIT, LCOM e LOC** por repositório, permitindo discutir as RQs solicitadas.

---

## 📮 Entregáveis já atendidos neste pacote

- **Script** para gerar a **lista dos 1.000 repositórios Java** (`scripts/fetch_top_repos.py`).
- **Scripts** para **clonar** e **coletar métricas** com **CK**.
- **CSV de 1 repositório** (`data/example_repo_metrics.csv`) já incluído.

Boa análise e boa apresentação! 🎓
