import pandas as pd, argparse
from datetime import datetime

def analyze(csv_file, out_file):
    df = pd.read_csv(csv_file)
    now = datetime.utcnow()

    results = {}

    # RQ01 - Idade
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['age_years'] = (now - df['created_at']).dt.days / 365
    results['RQ01_median_age'] = df['age_years'].median()

    # RQ02, RQ03 precisam de dados extras (PRs e releases) -> placeholder
    results['RQ02_total_prs'] = "Necessário coletar via pulls API"
    results['RQ03_total_releases'] = "Necessário coletar via releases API"

    # RQ04 - Última atualização
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df['last_update_days'] = (now - df['updated_at']).dt.days
    results['RQ04_median_last_update'] = df['last_update_days'].median()

    # RQ05 - Linguagem
    lang_counts = df['language'].value_counts().to_dict()
    results['RQ05_languages'] = lang_counts

    # RQ06 - Issues
    results['RQ06_open_issues_median'] = df['open_issues_count'].median()

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# Relatório de Análise")
        for k,v in results.items():
            f.write(f"**{k}:** {v}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="repos.csv")
    parser.add_argument("--out", default="report.md")
    args = parser.parse_args()
    analyze(args.csv, args.out)
