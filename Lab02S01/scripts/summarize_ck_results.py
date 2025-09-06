#!/usr/bin/env python3
"""
Lê as saídas do CK (class.csv) e gera um CSV por repositório com
métricas de tendência central (mediana, média, desvio-padrão) para CBO, DIT, LCOM, LOC.
Também faz merge (se fornecido) com dados de processo (stars, releases_count, age_years, etc.).

Uso:
  python scripts/summarize_ck_results.py --ck-root data/ck_output --repos-csv data/java_repos_top1000.csv --out data/summaries/summary_per_repo.csv
"""
import argparse
import os
import pandas as pd
import numpy as np
from glob import glob

def safe_stats(series):
    return {
        "median": float(np.median(series)) if len(series) else np.nan,
        "mean": float(np.mean(series)) if len(series) else np.nan,
        "std": float(np.std(series, ddof=1)) if len(series) > 1 else np.nan,
    }

def summarize_repo(repo_dir):
    class_csv = os.path.join(repo_dir, "class.csv")
    if not os.path.isfile(class_csv):
        return None
    df = pd.read_csv(class_csv)
    # Campos usuais do CK: 'cbo', 'dit', 'lcom', 'loc' podem variar de versão, aqui assumimos esses nomes padrão.
    needed = [c for c in ["cbo", "dit", "lcom", "loc"] if c in df.columns]
    if len(needed) < 4:
        # tentar compatibilidade: alguns dumps trazem 'lcom*'; se não achar, aborta
        return None

    stats = {}
    for col in ["cbo", "dit", "lcom", "loc"]:
        s = safe_stats(df[col].dropna())
        for k, v in s.items():
            stats[f"{col}_{k}"] = v

    # LOC total do repo (soma de classes)
    stats["loc_total"] = float(df["loc"].sum())
    return stats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ck-root", required=True, help="diretório raiz contendo saídas do CK por repositório")
    ap.add_argument("--repos-csv", default=None, help="CSV com metadados (gerado por fetch_top_repos.py)")
    ap.add_argument("--out", required=True, help="arquivo CSV de saída")
    args = ap.parse_args()

    rows = []
    for repo_path in sorted(glob(os.path.join(args.ck_root, "*"))):
        if not os.path.isdir(repo_path):
            continue
        repo_key = os.path.basename(repo_path)
        s = summarize_repo(repo_path)
        if s is None:
            continue
        s["repo_key"] = repo_key
        rows.append(s)

    summary_df = pd.DataFrame(rows)
    if args.repos_csv and os.path.isfile(args.repos_csv):
        meta = pd.read_csv(args.repos_csv)
        # Normalizar chave de junção: "owner__repo" vs "owner/repo"
        meta["repo_key"] = meta["full_name"].str.replace("/", "__", regex=False)
        merged = summary_df.merge(meta, on="repo_key", how="left")
    else:
        merged = summary_df

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    merged.to_csv(args.out, index=False, encoding="utf-8")
    print(f"OK! Sumarização escrita em: {args.out}  ({len(merged)} repositórios resumidos)")

if __name__ == "__main__":
    main()
