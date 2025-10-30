# Lab04S01 — Caracterização do Dataset

## 1. Introdução
Este pacote contém uma caracterização exemplo de um dataset de repositórios (GitHub-like). Ele demonstra as visualizações e tabelas esperadas para a entrega Lab04S01.

## 2. Dataset
O arquivo `dataset_characterization.csv` contém as seguintes colunas:
- repo_id, language, stars, forks, open_issues, commits, contributors, size_kb, created_at, last_push

Substitua este arquivo pelo dataset real (por exemplo, os repositórios coletados no Laboratório 01). Mantenha os nomes das colunas ou ajuste as consultas no Power BI / Tableau.

## 3. Visualizações incluídas (caracterização)
1. **Distribuição por linguagem** (`chart_language_distribution.png`) — mostra a quantidade de repositórios por linguagem (útil para entender se há balanceamento entre grupos).
2. **Distribuição de stars por linguagem** (`chart_stars_by_language.png`) — boxplot que evidencia tendências e outliers nas métricas de *stars* por linguagem.
3. **Repositórios criados por ano** (`chart_repos_by_year.png`) — série temporal do início dos repositórios no conjunto.

Também foi gerado um resumo tabular em `summary_by_language.csv` com métricas agregadas por linguagem (média de stars, média de commits, mediana de colaboradores, média de tamanho).

## 4. Como usar este pacote para o Lab04S01
- Abra o `dataset_characterization.csv` no Power BI / Tableau / Google Data Studio.
- Crie uma aba/página chamada "Caracterização do dataset".
- Importe a tabela e:
  - Crie um gráfico de barras com `language` (eixo X) e contagem de `repo_id` (eixo Y).
  - Crie boxplots ou gráficos de violino para `stars` por `language`.
  - Crie uma série temporal usando `created_at` (agrupando por ano) para visualizar tendência de criação de repositórios.
- Se você particionar o dataset (por exemplo, por linguagem ou por período), gere as mesmas visualizações para cada subgrupo e inclua uma tabela comparativa.

## 5. Entrega (o que incluir)
- PDF ou imagem exportada da página "Caracterização do dataset" do seu dashboard.
- Arquivos de apoio (o CSV original usado e os resumos).
- Um slide curto (1–2 slides) demonstrando os principais achados da caracterização.

## 6. Observações finais
Este pacote é um modelo. Ao substituir pelo seu dataset real, confirme:
- Consistência de tipos (datas como yyyy-mm-dd).
- Valores faltantes e limpeza necessária.
- Definição clara de subgrupos usados nas futuras RQs.

Boa sorte!