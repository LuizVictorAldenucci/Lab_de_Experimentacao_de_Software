#!/usr/bin/env python3
"""
Analyze the CSV exported by fetch_github_repos.py and produce a Markdown report.
Generates basic summary tables and saves them alongside the input.
"""

import argparse
import pandas as pd
import textwrap
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import os

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    # ensure datetimes
    for col in ["created_at", "updated_at", "pushed_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
    return df

def save_plot(fig, out_path: str):
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Analyze GitHub repos CSV and write report.md")
    parser.add_argument("--csv", default="repos.csv", help="Path to CSV")
    parser.add_argument("--out", default="report.md", help="Output Markdown path")
    args = parser.parse_args()

    df = load_csv(args.csv)
    n = len(df)

    now = datetime.now(timezone.utc)

    # Basic summaries
    by_lang = df.groupby("language", dropna=False)["stargazers_count"].agg(["count","median","mean"]).sort_values("count", ascending=False).head(20)
    by_owner_type = df.groupby("owner_type")["stargazers_count"].agg(["count","median","mean"]).sort_values("median", ascending=False)
    df["has_license"] = df["license_key"].notna()
    license_stats = df.groupby("has_license")["stargazers_count"].agg(["count","median","mean"])

    # Activity
    df["days_since_push"] = (now - df["pushed_at"]).dt.days
    recent = df[df["days_since_push"] <= 30]
    activity_stats = {
        "recent_push_share": len(recent) / n if n > 0 else 0.0,
        "median_days_since_push": float(df["days_since_push"].median()) if n > 0 else None
    }

    # Topics
    df["topic_count"] = df["topics"].fillna("").apply(lambda s: 0 if not isinstance(s, str) else (0 if s.strip()=="" else len(s.split(";"))))
    topic_corr = df[["topic_count","stargazers_count"]].dropna().corr().iloc[0,1] if n > 1 else None

    # Save charts (one per figure, default colors)
    charts_dir = os.path.join(os.path.dirname(args.out), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    fig = plt.figure()
    (df["language"].value_counts().head(10)).plot(kind="bar")
    plt.title("Top 10 Languages by Repo Count")
    plt.xlabel("Language")
    plt.ylabel("Count")
    save_plot(fig, os.path.join(charts_dir, "top_languages.png"))

    fig = plt.figure()
    df["stargazers_count"].plot(kind="hist", bins=40)
    plt.title("Stars Distribution")
    plt.xlabel("Stars")
    plt.ylabel("Frequency")
    save_plot(fig, os.path.join(charts_dir, "stars_hist.png"))

    # Assemble report
    md = f"""# GitHub Repositories – First Report

**Generated:** {now.isoformat()}
**Input CSV:** {os.path.abspath(args.csv)}
**Rows:** {n}

## Informal Hypotheses (to be validated)
- **H1:** Repositórios com **mais tópicos** tendem a ter **mais estrelas**.
- **H2:** **JavaScript/TypeScript** aparecem entre as linguagens mais comuns nos repositórios populares.
- **H3:** Repositórios com **atividade recente** (push nos últimos 30 dias) apresentam **mais forks/estrelas**.
- **H4:** Repositórios de **organizações** (owner_type=Organization) possuem **mediana de estrelas** maior que os de usuários individuais.
- **H5:** Ter uma **licença definida** se associa a **maior adoção** (mais estrelas).

## Metodologia (resumo)
- Coleta via **GitHub Search API**, até 1000 resultados (limite da API), ordenados por parâmetro configurável (padrão: `stars desc`).
- Campos extraídos incluem: metadados do repositório, contagens (stars, forks, issues), timestamps (created/updated/pushed), linguagem, licença e **tópicos**.
- Análises exploratórias com `pandas` e gráficos com `matplotlib`.

## Resumo Rápido
- Proporção com push nos últimos 30 dias: **{activity_stats['recent_push_share']:.1%}**
- Mediana de dias desde o último push: **{activity_stats['median_days_since_push']}**
- Correlação (Pearson) entre **#tópicos** e **estrelas**: **{topic_corr}**

## Top Linguagens (por contagem de repositórios)
{by_lang.to_markdown()}

## Stars por Tipo de Dono (User vs Organization)
{by_owner_type.to_markdown()}

## Stars vs Licença Definida
{license_stats.to_markdown()}

## Gráficos
- charts/top_languages.png
- charts/stars_hist.png

---

> Esta é uma **primeira versão** do relatório. Recomenda-se filtrar o universo de consulta (ex.: por linguagem, período de atualização, ou tamanho mínimo de estrelas) e refinar as hipóteses com testes estatísticos adicionais.
"""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"[done] Wrote report to {args.out} and charts to {charts_dir}")

if __name__ == "__main__":
    main()
