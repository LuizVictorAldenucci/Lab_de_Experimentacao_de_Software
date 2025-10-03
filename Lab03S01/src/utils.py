import os
import time
from typing import Dict, Any, Optional
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com/graphql")

class GitHubAPIError(Exception):
    pass

def _headers() -> Dict[str, str]:
    if not GITHUB_TOKEN:
        raise GitHubAPIError("GITHUB_TOKEN não configurado. Defina a variável de ambiente ou o .env.")
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30),
       retry=retry_if_exception_type(GitHubAPIError))
def gh_graphql(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resp = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables or {}}, headers=_headers(), timeout=60)
    if resp.status_code == 200:
        data = resp.json()
        if "errors" in data:
            # Pode ser rate limit, backoff gentil
            msg = str(data["errors"])
            if "rate limit" in msg.lower():
                time.sleep(5)
            raise GitHubAPIError(msg)
        return data["data"]
    elif resp.status_code in (429, 502, 503):
        time.sleep(5)
        raise GitHubAPIError(f"HTTP {resp.status_code} — reintentando")
    else:
        raise GitHubAPIError(f"HTTP {resp.status_code}: {resp.text}")
