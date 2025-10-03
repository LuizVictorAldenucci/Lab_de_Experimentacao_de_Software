import argparse
from datetime import datetime, timezone
import math
import pandas as pd
from tqdm import tqdm
from utils import gh_graphql
from schemas import PRS_COLUMNS

PR_QUERY = """
query($owner:String!, $name:String!, $after:String) {
  repository(owner:$owner, name:$name) {
    nameWithOwner
    pullRequests(states:[MERGED, CLOSED], first: 50, after:$after, orderBy:{field:UPDATED_AT, direction:DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        url
        state
        createdAt
        closedAt
        mergedAt
        changedFiles
        additions
        deletions
        bodyText
        participants { totalCount }
        comments { totalCount }
        reviews: reviews { totalCount }
      }
    }
  }
}
"""

def horas_entre(a: str, b: str) -> float:
    if not a or not b:
        return math.nan
    da = datetime.fromisoformat(a.replace("Z", "+00:00"))
    db = datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (db - da).total_seconds() / 3600.0

def coleta_prs(owner: str, name: str, max_prs: int):
    prs = []
    after = None
    coletados = 0
    while True:
        data = gh_graphql(PR_QUERY, {"owner": owner, "name": name, "after": after})
        repo = data["repository"]
        if repo is None:
            break
        prconn = repo["pullRequests"]
        for pr in prconn["nodes"]:
            # Filtros da atividade de code review
            if (pr["reviews"]["totalCount"] or 0) < 1:
                continue
            fim = pr["mergedAt"] or pr["closedAt"]
            if fim is None:
                continue
            horas = horas_entre(pr["createdAt"], fim)
            if math.isnan(horas) or horas < 1.0:
                continue

            desc_len = len(pr["bodyText"] or "")
            prs.append({
                "repo_full_name": repo["nameWithOwner"],
                "number": pr["number"],
                "url": pr["url"],
                "state": pr["state"],
                "createdAt": pr["createdAt"],
                "closedAt": pr["closedAt"],
                "mergedAt": pr["mergedAt"],
                "changedFiles": pr["changedFiles"],
                "additions": pr["additions"],
                "deletions": pr["deletions"],
                "desc_len": desc_len,
                "participants": pr["participants"]["totalCount"],
                "comments": pr["comments"]["totalCount"],
                "reviews": pr["reviews"]["totalCount"],
                "tempo_analise_horas": round(horas, 3)
            })
            coletados += 1
            if max_prs and coletados >= max_prs:
                break

        if max_prs and coletados >= max_prs:
            break
        if not prconn["pageInfo"]["hasNextPage"]:
            break
        after = prconn["pageInfo"]["endCursor"]
    return prs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos-csv", default="data/repositorios_selecionados.csv", help="CSV com owner,name (gerado pelo select_repos.py)")
    ap.add_argument("--max-prs-por-repo", type=int, default=0, help="0 = sem limite")
    ap.add_argument("--saida", default="data/prs_dataset.csv", help="Caminho do CSV de saída")
    args = ap.parse_args()

    repos = pd.read_csv(args.repos_csv)
    todos = []
    for _, row in tqdm(repos.iterrows(), total=len(repos), desc="Coletando PRs"):
        owner = row["owner"]
        name = row["name"]
        prs = coleta_prs(owner, name, args.max_prs_por_repo)
        todos.extend(prs)

    df = pd.DataFrame(todos, columns=PRS_COLUMNS)
    df.to_csv(args.saida, index=False, encoding="utf-8")
    print(f"Salvo: {args.saida} ({len(df)} PRs)")

if __name__ == "__main__":
    main()
