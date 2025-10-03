import pandas as pd
from tqdm import tqdm
from utils import gh_graphql
from schemas import REPOS_COLUMNS

# Busca os 200 repositórios mais estrelados e filtra os que têm >= 100 PRs (MERGED + CLOSED)
SEARCH_PAGE_SIZE = 50  # GraphQL máx. 100; usamos 50 para margem
ALVO_QTD = 200

SEARCH_QUERY = """
query($after: String) {
  search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: %d, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        nameWithOwner
        owner { login }
        url
        stargazerCount
        forkCount
        issues(states: OPEN) { totalCount }
        pullRequests(states: [MERGED, CLOSED]) { totalCount }
        isFork
        isArchived
      }
    }
  }
}""" % SEARCH_PAGE_SIZE

def main():
    repos = []
    after = None
    with tqdm(total=ALVO_QTD, desc="Buscando repositórios") as pbar:
        while len(repos) < ALVO_QTD:
            data = gh_graphql(SEARCH_QUERY, {"after": after})
            search = data["search"]
            for node in search["nodes"]:
                if node["isFork"] or node["isArchived"]:
                    continue
                pr_total = node["pullRequests"]["totalCount"]
                if pr_total >= 100:
                    repos.append({
                        "owner": node["owner"]["login"],
                        "name": node["name"],
                        "full_name": node["nameWithOwner"],
                        "url": node["url"],
                        "stars": node["stargazerCount"],
                        "forks": node["forkCount"],
                        "open_issues": node["issues"]["totalCount"],
                        "prs_total_closed_merged": pr_total
                    })
                    pbar.update(1)
                    if len(repos) >= ALVO_QTD:
                        break
            if not search["pageInfo"]["hasNextPage"]:
                break
            after = search["pageInfo"]["endCursor"]

    df = pd.DataFrame(repos, columns=REPOS_COLUMNS)
    df.sort_values(by="stars", ascending=False, inplace=True)
    out = "data/repositorios_selecionados.csv"
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"Salvo: {out} ({len(df)} repositórios)")

if __name__ == "__main__":
    main()
