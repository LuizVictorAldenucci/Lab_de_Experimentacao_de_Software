# Lab04S02 — Visualizações (RQ1 a RQ4)

## Contexto
Este pacote contém visualizações e dados sintéticos que simulam experimentos comparando Java (threads) e Kotlin (coroutines) em duas tarefas: multiplicação de matrizes (CPU-bound) e operações I/O (I/O-bound).
Foram realizadas 10 repetições por configuração.

## RQ1 — Desempenho (Tempo)
Arquivos: rq1_time_vs_threads_matrix_mul.png, rq1_time_vs_threads_io_bound.png
Arquivo agregado: rq1_time_aggregated.csv
Descrição: mostra o tempo médio por número de threads/coroutines para cada linguagem e tarefa.

## RQ2 — Consumo de recursos (CPU & Memória)
Arquivos: rq2_cpu_matrix_mul.png, rq2_cpu_io_bound.png, rq2_mem_matrix_mul.png, rq2_mem_io_bound.png
Arquivo agregado: rq2_cpu_mem_aggregated.csv
Descrição: compara CPU e memória média por linguagem e tarefa.

## RQ3 — Impacto do paralelismo (Speedup)
Arquivos: rq3_speedup_matrix_mul.png, rq3_speedup_io_bound.png
Arquivo agregado: rq3_speedup.csv
Descrição: curvas de speedup calculadas em relação ao tempo de execução com 1 thread.

## RQ4 — Estabilidade / Variabilidade
Arquivos: rq4_time_variability_matrix_mul.png, rq4_time_variability_io_bound.png
Descrição: boxplots mostrando variação do tempo entre execuções.

## Conteúdo do pacote
- experiment_results.csv (dados brutos de cada execução)
- vários PNGs com as visualizações descritas
- arquivos CSV agregados com estatísticas (rq1_time_aggregated.csv, rq2_cpu_mem_aggregated.csv, rq3_speedup.csv)
- este relatório (Lab04S02_report.md)

**Observação:** Estes dados são sintéticos e servem como modelo. Ao fornecer os resultados reais do experimento (CSV de medições), posso reprocessar e gerar visualizações idênticas com dados verdadeiros.
