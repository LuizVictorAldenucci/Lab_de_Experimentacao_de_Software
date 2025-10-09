# Relatório — Lab03S02
**Autora:** Gabrielle Lira Dantas Wanderley • **Curso:** Engenharia de Software (PUC Minas)

## Introdução & Hipóteses
- H1: PRs maiores → maior chance de *close*.
- H2: Muito tempo de análise → maior chance de *close*.
- H3: Descrições mais longas → maior chance de *merge*.
- H4: Interações muito altas → tendência a *close*; níveis moderados → *merge*.
- H5: PRs maiores → mais revisões.
- H6: Mais tempo de análise → mais revisões.
- H7: Descrições melhores → menos revisões.
- H8: Mais interações → mais revisões.

## Metodologia (S02)
Top-200 repositórios (estrelas), ≥100 PRs MERGED/CLOSED; coleta via GraphQL com filtros: MERGED/CLOSED, ≥1 review, ≥1h de análise. Métricas: tamanho (arquivos/linhas), tempo, descrição, interações, nº de revisões, status.

## Justificativa estatística
Usar **Spearman** (dados assimétricos, relação monotônica, robusto a *outliers*). Pearson como controle se normalidade/linearidade se mantiver.

## Próximos passos
Medianas gerais/por status, correlações para RQ01–RQ08, e (opcional) regressão logística para status.
