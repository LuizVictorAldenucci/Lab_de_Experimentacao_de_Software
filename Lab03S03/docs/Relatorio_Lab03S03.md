# Relatório Final — Lab03S03
**Autora:** Gabrielle Lira Dantas Wanderley  
**Curso:** Engenharia de Software (PUC Minas)

## Metodologia
Dataset com PRs MERGED/CLOSED, ≥1 review e ≥1h de análise; métricas de tamanho, tempo, descrição, interações, nº de revisões e status. Análise por medianas e correlações de Spearman.

## Medianas gerais

|                     |   mediana |
|:--------------------|----------:|
| changedFiles        |   10      |
| additions           |  143.5    |
| deletions           |   90      |
| desc_len            |  827.5    |
| participants        |    3      |
| comments            |    6.5    |
| reviews             |    2      |
| tempo_analise_horas |    6.9805 |

## Medianas por status

| state   |   changedFiles |   additions |   deletions |   desc_len |   participants |   comments |   reviews |   tempo_analise_horas |
|:--------|---------------:|------------:|------------:|-----------:|---------------:|-----------:|----------:|----------------------:|
| CLOSED  |              9 |       111.5 |       111   |        965 |            2.5 |          7 |         2 |                6.2565 |
| MERGED  |             10 |       156.5 |        82.5 |        783 |            3   |          6 |         2 |                7.2445 |

## Correlações (Spearman)

| x                   | y          |   spearman_rho |   p_value |
|:--------------------|:-----------|---------------:|----------:|
| changedFiles        | status_bin |     0.0907883  |  0.25356  |
| additions           | status_bin |     0.0805793  |  0.311101 |
| deletions           | status_bin |    -0.104958   |  0.186545 |
| tempo_analise_horas | status_bin |     0.0277346  |  0.727739 |
| desc_len            | status_bin |    -0.110209   |  0.165336 |
| participants        | status_bin |     0.0335096  |  0.674002 |
| comments            | status_bin |    -0.0620312  |  0.435839 |
| changedFiles        | reviews    |    -0.0443248  |  0.577837 |
| additions           | reviews    |    -0.0364206  |  0.647507 |
| deletions           | reviews    |    -0.0986627  |  0.214517 |
| tempo_analise_horas | reviews    |     0.0480741  |  0.546059 |
| desc_len            | reviews    |     0.00735472 |  0.926458 |
| participants        | reviews    |    -0.0287823  |  0.717882 |
| comments            | reviews    |     0.0457612  |  0.565561 |

## Discussão por RQ
### RQ01
Correlação positiva fraca (rho=0.091, p=0.254) — não significativa.

### RQ02
Correlação positiva fraca (rho=0.028, p=0.728) — não significativa.

### RQ03
Correlação negativa fraca (rho=-0.110, p=0.165) — não significativa.

### RQ04
Correlação negativa fraca (rho=-0.062, p=0.436) — não significativa.

### RQ05
Correlação negativa fraca (rho=-0.044, p=0.578) — não significativa.

### RQ06
Correlação positiva fraca (rho=0.048, p=0.546) — não significativa.

### RQ07
Correlação positiva fraca (rho=0.007, p=0.926) — não significativa.

### RQ08
Correlação positiva fraca (rho=0.046, p=0.566) — não significativa.

## Gráficos gerados
- outputs/plots/box_additions_por_status.png
- outputs/plots/box_changedFiles_por_status.png
- outputs/plots/box_tempo_analise_horas_por_status.png
- outputs/plots/hist_additions.png
- outputs/plots/hist_changedFiles.png
- outputs/plots/hist_deletions.png
- outputs/plots/hist_tempo_analise_horas.png
- outputs/plots/scatter_reviews_vs_additions.png
- outputs/plots/scatter_reviews_vs_changedFiles.png
