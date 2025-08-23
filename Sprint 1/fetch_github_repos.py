import requests, csv, os, argparse

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def fetch_repos(query, out_file, max_repos=1000, sort="stars", order="desc"):
    repos = []
    per_page = 100
    for page in range(1, (max_repos // per_page) + 1):
        url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}&page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print("Erro:", r.json())
            break
        data = r.json().get("items", [])
        if not data: break
        for repo in data:
            repos.append({
                "name": repo["full_name"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "pushed_at": repo["pushed_at"],
                "stargazers_count": repo["stargazers_count"],
                "forks_count": repo["forks_count"],
                "open_issues_count": repo["open_issues_count"],
                "language": repo["language"],
                "license": repo["license"]["spdx_id"] if repo["license"] else None,
                "url": repo["html_url"]
            })
        print(f"Página {page} concluída, total {len(repos)} repositórios")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=repos[0].keys())
        writer.writeheader()
        writer.writerows(repos)
    print(f"Salvo em {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="stars:>1")
    parser.add_argument("--out", default="repos.csv")
    parser.add_argument("--max", type=int, default=1000)
    args = parser.parse_args()
    fetch_repos(args.query, args.out, args.max)
