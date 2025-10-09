import os,time,requests
from tenacity import retry,stop_after_attempt,wait_exponential,retry_if_exception_type
from dotenv import load_dotenv; load_dotenv()
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN",""); API=os.getenv("GITHUB_API_URL","https://api.github.com/graphql")
class GitHubAPIError(Exception): pass
def _headers():
    if not GITHUB_TOKEN: raise GitHubAPIError("GITHUB_TOKEN não configurado.")
    return {"Authorization":f"Bearer {GITHUB_TOKEN}","Accept":"application/vnd.github+json"}
@retry(stop=stop_after_attempt(5),wait=wait_exponential(1,2,30),retry=retry_if_exception_type(GitHubAPIError))
def gh_graphql(query, variables=None):
    r=requests.post(API,json={"query":query,"variables":variables or {}},headers=_headers(),timeout=60)
    if r.status_code==200:
        j=r.json()
        if "errors" in j: 
            msg=str(j["errors"]); 
            if "rate limit" in msg.lower(): time.sleep(5)
            raise GitHubAPIError(msg)
        return j["data"]
    elif r.status_code in (429,502,503):
        time.sleep(5); raise GitHubAPIError(f"HTTP {r.status_code}")
    else: raise GitHubAPIError(f"HTTP {r.status_code}: {r.text}")
