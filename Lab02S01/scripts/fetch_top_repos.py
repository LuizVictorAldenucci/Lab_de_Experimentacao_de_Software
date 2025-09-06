#!/usr/bin/env python3
"""
Busca os top-N repositórios em Java no GitHub (por estrelas) e salva em CSV.

Uso:
  python scripts/fetch_top_repos.py --out data/java_repos_top1000.csv --count 1000

Requer variável de ambiente GITHUB_TOKEN definida em .env
"""
import os
import csv
import time
import argparse
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

SEARCH_URL = "https://api.github.com/search/repositories"
RELEASES_URL_TMPL = "https://api.github.com/repos/{full_name}/releases?per_page=1"

def get_releases_count(full_name: str) -> int:
    url = RELEASES_URL_TMPL.format(full_name=full_name)
    r = requests.get(url, headers=HEADERS, timeout=30)
    # Se a API retornar a paginação no header "Link", inferimos a última página
    link = r.headers.get("Link", "")
    if "rel=\"last\"" in link:
        # ...page=N>; rel="last"
        try:
            last = [seg for seg in link.split(",") if 'rel="last"' in seg][0]
            # extrair page=N
            import re
            m = re.search(r"[?&]page=(\d+)", last)
            if m:
                return int(m.group(1))
        except Exception:
            pass
    # Senão, contamos o retorno atual (0 ou 1)
    if r.status_code == 200:
        return len(r.json())
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="caminho do CSV de saída")
    ap.add_argument("--count", type=int, default=1000, help="quantidade total desejada (<=1000)")
    args = ap.parse_args()

    total = min(args.count, 1000)
    per_page = 100
    pages = (total + per_page - 1) // per_page

    fields = [
        "rank","full_name","name","html_url","description",
        "stargazers_count","forks_count","open_issues_count","watchers_count",
        "language","license","created_at","updated_at","pushed_at","size_kb"
    ]
    extra_fields = ["releases_count","age_years"]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields + extra_fields)
        rank = 1
        for page in tqdm(range(1, pages+1), desc="Paginando GitHub"):
            params = {
                "q": "language:Java",
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
                "page": page,
            }
            r = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=60)
            if r.status_code != 200:
                raise SystemExit(f"Erro na API do GitHub: {r.status_code} {r.text}")

            items = r.json().get("items", [])
            for it in items:
                if rank > total:
                    break
                full_name = it["full_name"]
                # license pode ser None
                license_name = it["license"]["spdx_id"] if it.get("license") else ""
                created_at = it["created_at"]
                created_dt = datetime.fromisoformat(created_at.replace("Z","+00:00"))
                age_years = (datetime.now(timezone.utc) - created_dt).days / 365.25

                # releases_count (chamada extra leve)
                rel_count = get_releases_count(full_name)

                row = [
                    rank,
                    full_name,
                    it["name"],
                    it["html_url"],
                    (it.get("description") or "").replace("\n"," ").strip(),
                    it["stargazers_count"],
                    it["forks_count"],
                    it["open_issues_count"],
                    it["watchers_count"],
                    it.get("language") or "",
                    license_name,
                    it["created_at"],
                    it["updated_at"],
                    it["pushed_at"],
                    it["size"],  # KB
                ] + [rel_count, f"{age_years:.3f}"]
                w.writerow(row)
                rank += 1

            # Para evitar rate-limit agressivo
            time.sleep(1)

    print(f"OK! CSV escrito em: {args.out}")

if __name__ == "__main__":
    main()
