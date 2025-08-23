# Relatório – Primeira Versão (Hipóteses Informais)

**Data:** 2025-08-22T23:21:15.235816Z

## Objetivo
Coletar até **1000 repositórios** via **GitHub Search API**, salvar em **CSV**, e produzir uma **primeira versão** de relatório com **hipóteses informais** a serem validadas.

## Hipóteses Informais
1. **H1:** Repositórios com **mais tópicos** (campo `topics`) tendem a ter **mais estrelas**.
2. **H2:** **JavaScript/TypeScript** são frequentes entre os repositórios mais populares.
3. **H3:** Repositórios com **atividade recente** (push nos últimos 30 dias) tendem a ter **mais estrelas/forks**.
4. **H4:** Repositórios de **organizações** têm **mediana de estrelas** maior que de usuários.
5. **H5:** Repositórios com **licença definida** possuem **mais estrelas** em mediana.

## Como Reproduzir
1. Crie um **token** do GitHub e exporte como variável de ambiente `GITHUB_TOKEN`.
2. Rode a coleta (exemplo abaixo coleta por estrelas):
   ```bash
   python fetch_github_repos.py --query "stars:>10" --out repos.csv --max 1000 --sort stars --order desc
   ```
3. Gere o relatório com análises iniciais:
   ```bash
   python analyze_repos.py --csv repos.csv --out report.md
   ```

## Observações
- O GitHub limita a **busca** a **1000 resultados**. Ajuste o `--query` para focar no seu recorte (linguagem, período etc.).
- O CSV conterá campos úteis para análises posteriores (linguagem, licença, tópicos, timestamps, contagens, etc.).
