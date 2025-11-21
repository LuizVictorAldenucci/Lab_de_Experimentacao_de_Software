# Artigo TIS6 — Atualizado com os resultados do experimento

## 1. Introdução
Este artigo apresenta a caracterização do dataset e os resultados das RQs que
comparam Java (threads) e Kotlin (coroutines) em tarefas concorrentes (CPU-bound e I/O-bound).

## 2. Metodologia / Descrição da base
Foram utilizados dois conjuntos de dados no projeto:

1. **Caracterização dos repositórios** (arquivo: Lab04S01/dataset_characterization.csv) — contém 200 repositórios sintéticos com colunas como language, stars, commits, contributors, size_kb, created_at.

2. **Resultados do experimento controlado** (arquivo: Lab04S02_full/experiment_results.csv) — contém execuções para combinações de linguagem, tarefa, número de threads/coroutines e repetições.

## 3. Caracterização do Dataset
A caracterização apresenta a distribuição por linguagem (ver Lab04S01/chart_language_distribution.png) e um resumo por linguagem (Lab04S01/summary_by_language.csv).

## 4. Resultados (RQ1 a RQ4)
### RQ1 — Desempenho (Tempo)
Foram geradas curvas Tempo médio vs Número de threads/coroutines para cada tarefa:
- Lab04S02_full/rq1_time_vs_threads_matrix_mul.png
- Lab04S02_full/rq1_time_vs_threads_io_bound.png
Arquivos agregados: Lab04S02_full/rq1_time_aggregated.csv

### RQ2 — Consumo de recursos (CPU & Memória)
Gráficos:
- Lab04S02_full/rq2_cpu_matrix_mul.png
- Lab04S02_full/rq2_cpu_io_bound.png
- Lab04S02_full/rq2_mem_matrix_mul.png
- Lab04S02_full/rq2_mem_io_bound.png
Arquivo agregado: Lab04S02_full/rq2_cpu_mem_aggregated.csv

### RQ3 — Impacto do paralelismo (Speedup)
Gráficos:
- Lab04S02_full/rq3_speedup_matrix_mul.png
- Lab04S02_full/rq3_speedup_io_bound.png
Arquivo agregado: Lab04S02_full/rq3_speedup.csv

### RQ4 — Estabilidade / Variabilidade
Boxplots de variabilidade do tempo:
- Lab04S02_full/rq4_time_variability_matrix_mul.png
- Lab04S02_full/rq4_time_variability_io_bound.png

## 5. Discussão
(Preencha com interpretação dos resultados. Exemplos: Kotlin tende a apresentar menor tempo médio e menor uso de memória para as configurações testadas; Java pode apresentar maior consumo de memória, etc.)

## 6. Conclusão
Resumo final e recomendações.

## 7. Anexos
Inclui arquivos CSV com dados brutos e agregados para reprodução das análises.
