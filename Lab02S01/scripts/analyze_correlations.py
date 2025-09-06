#!/usr/bin/env python3
"""
Gera tabela de correlação (Pearson/Spearman) entre métricas de processo e de qualidade,
além de gráficos de dispersão.

Uso:
  python scripts/analyze_correlations.py --summary data/summaries/summary_per_repo.csv --out-dir reports/plots
"""
import argparse
import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

PROCESS_COLS = ["stargazers_count", "releases_count", "age_years", "loc_total"]
QUALITY_COLS = [
    "cbo_median","cbo_mean","cbo_std",
    "dit_median","dit_mean","dit_std",
    "lcom_median","lcom_mean","lcom_std",
]

def safe_float(s):
    try:
        return float(s)
    except Exception:
        return np.nan

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, help="CSV produzido por summarize_ck_results.py (com merge de meta se possível)")
    ap.add_argument("--out-dir", required=True, help="diretório para salvar gráficos e tabelas")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    df = pd.read_csv(args.summary)
    # Garantir tipos
    for c in ["stargazers_count","releases_count","age_years","loc_total"]:
        if c in df.columns:
            df[c] = df[c].apply(safe_float)

    # Tabela de correlações
    records = []
    for p in PROCESS_COLS:
        if p not in df.columns: 
            continue
        for q in QUALITY_COLS:
            if q not in df.columns: 
                continue
            sub = df[[p, q]].dropna()
            if len(sub) < 5:
                pear = (np.nan, np.nan)
                spear = (np.nan, np.nan)
            else:
                pear = pearsonr(sub[p], sub[q])
                spear = spearmanr(sub[p], sub[q])
            records.append({
                "x_metric": p,
                "y_metric": q,
                "pearson_r": pear[0],
                "pearson_pvalue": pear[1],
                "spearman_rho": spear[0],
                "spearman_pvalue": spear[1],
                "n": len(sub)
            })
    corr_df = pd.DataFrame(records)
    corr_csv = os.path.join(args.out_dir, "correlations.csv")
    corr_df.to_csv(corr_csv, index=False)
    print(f"Correlação salva em: {corr_csv}")

    # Gráficos de dispersão (sem customizações de cor/estilo)
    for p in PROCESS_COLS:
        if p not in df.columns: 
            continue
        for q in ["cbo_mean","dit_mean","lcom_mean"]:
            if q not in df.columns:
                continue
            sub = df[[p, q]].dropna()
            if len(sub) < 5:
                continue
            plt.figure()
            plt.scatter(sub[p], sub[q])
            plt.xlabel(p)
            plt.ylabel(q)
            plt.title(f"Scatter: {p} vs {q}")
            out_png = os.path.join(args.out_dir, f"scatter_{p}_vs_{q}.png")
            plt.savefig(out_png, bbox_inches="tight")
            plt.close()
            print(f"Salvo gráfico: {out_png}")

if __name__ == "__main__":
    main()
