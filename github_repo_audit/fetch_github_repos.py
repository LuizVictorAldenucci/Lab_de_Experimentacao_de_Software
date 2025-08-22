#!/usr/bin/env python3
"""
Fetch up to N (default: 1000) repositories from GitHub Search API with pagination
and save them to a CSV.

Usage:
  python fetch_github_repos.py --query "stars:>10" --out repos.csv --max 1000 --sort stars --order desc

Auth:
  - Provide a token via the environment variable GITHUB_TOKEN for higher rate limits.
    Create a classic PAT with "public_repo" scope (for public repos) at https://github.com/settings/tokens
  - Alternatively, pass --token YOUR_TOKEN (env var recommended).

Notes:
  - GitHub Search caps results at 1000 items. We'll paginate 10 pages x 100 per page.
  - Be mindful of rate limits; this script auto-waits if needed.
"""

import os
import csv
import time
import math
import argparse
import requests
from datetime import datetime, timezone

API_URL = "https://api.github.com/search/repositories"

def github_headers(token: str | None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "repo-audit-script"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def wait_for_reset(reset_ts: str | int | None):
    if not reset_ts:
        return
    try:
        reset_ts = int(reset_ts)
        now = int(time.time())
        sleep_for = max(0, reset_ts - now) + 2
        if sleep_for > 0:
            print(f"[rate-limit] Sleeping {sleep_for}s until reset...")
            time.sleep(sleep_for)
    except Exception:
        pass

def search_page(query: str, page: int, per_page: int, sort: str | None, order: str, token: str | None):
    params = {
        "q": query,
        "page": page,
        "per_page": per_page,
        "order": order
    }
    if sort:
        params["sort"] = sort
    resp = requests.get(API_URL, headers=github_headers(token), params=params, timeout=60)
    # Rate limit handling
    remaining = resp.headers.get("X-RateLimit-Remaining")
    reset = resp.headers.get("X-RateLimit-Reset")
    if resp.status_code == 403 and remaining == "0":
        wait_for_reset(reset)
        resp = requests.get(API_URL, headers=github_headers(token), params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", [])
    total_count = data.get("total_count", 0)
    return items, total_count, remaining, reset

def flatten_repo(repo: dict) -> dict:
    owner = repo.get("owner") or {}
    license_info = repo.get("license") or {}
    topics = repo.get("topics") or []  # present with Accept: application/vnd.github+json

    return {
        "id": repo.get("id"),
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "owner_login": owner.get("login"),
        "owner_type": owner.get("type"),
        "html_url": repo.get("html_url"),
        "description": (repo.get("description") or "").replace("\n", " ").strip(),
        "homepage": repo.get("homepage"),
        "language": repo.get("language"),
        "topics": ";".join(topics),
        "license_key": license_info.get("key") if license_info else None,
        "license_name": license_info.get("name") if license_info else None,
        "default_branch": repo.get("default_branch"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "size_kb": repo.get("size"),
        "stargazers_count": repo.get("stargazers_count"),
        "forks_count": repo.get("forks_count"),
        "open_issues_count": repo.get("open_issues_count"),
        "watchers_count": repo.get("watchers_count"),
        "has_issues": repo.get("has_issues"),
        "has_wiki": repo.get("has_wiki"),
        "has_pages": repo.get("has_pages"),
        "is_template": repo.get("is_template"),
        "archived": repo.get("archived"),
        "disabled": repo.get("disabled"),
        "visibility": repo.get("visibility"),
        "allow_forking": repo.get("allow_forking"),
        "network_count": repo.get("network_count"),
        "subscribers_count": repo.get("subscribers_count"),
    }

def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub repositories to CSV (paginated).")
    parser.add_argument("--query", default="stars:>10", help="GitHub search query. E.g. 'language:TypeScript stars:>50 pushed:>2024-01-01'")
    parser.add_argument("--out", default="repos.csv", help="Output CSV path")
    parser.add_argument("--max", type=int, default=1000, help="Max repositories to fetch (<=1000 for GitHub Search)")
    parser.add_argument("--sort", default="stars", choices=[None, "stars", "forks", "help-wanted-issues", "updated"], help="Sort field")
    parser.add_argument("--order", default="desc", choices=["asc", "desc"], help="Sort order")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub token (env GITHUB_TOKEN recommended)")
    args = parser.parse_args()

    token = args.token
    max_items = min(1000, max(1, args.max))
    per_page = 100
    pages = math.ceil(max_items / per_page)

    print(f"[info] Query='{args.query}', sort='{args.sort}', order='{args.order}', target={max_items}")
    print(f"[info] Using token: {'YES' if token else 'NO'}")

    fieldnames = list(flatten_repo({}).keys())
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        fetched = 0
        for page in range(1, pages + 1):
            to_get = min(per_page, max_items - fetched)
            if to_get <= 0:
                break
            print(f"[fetch] page={page} per_page={per_page}")
            items, total_count, remaining, reset = search_page(args.query, page, per_page, args.sort, args.order, token)
            print(f"[fetch] received {len(items)} items (total_count reported by API: {total_count}) | rate remaining: {remaining}")
            if not items:
                break
            for repo in items:
                writer.writerow(flatten_repo(repo))
                fetched += 1
                if fetched >= max_items:
                    break
            # Be nice to API
            time.sleep(0.6)
            if fetched >= max_items:
                break

    print(f"[done] Wrote {fetched} repos to {args.out}")

if __name__ == "__main__":
    main()
