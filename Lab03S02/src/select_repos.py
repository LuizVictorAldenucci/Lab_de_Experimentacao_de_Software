import pandas as pd
from utils import gh_graphql
from schemas import REPOS_COLUMNS
PAGE=50; TARGET=200
Q=f"""query($after:String){{
  search(query:"stars:>1 sort:stars-desc",type:REPOSITORY,first:{PAGE},after:$after){{
    pageInfo{{hasNextPage endCursor}}
    nodes{{... on Repository{{name nameWithOwner owner{{login}} url stargazerCount forkCount issues(states:OPEN){{totalCount}} pullRequests(states:[MERGED,CLOSED]){{totalCount}} isFork isArchived}}}}
  }}
}}"""
def main():
    repos=[]; after=None
    while len(repos)<TARGET:
        data=gh_graphql(Q,{"after":after}); s=data["search"]
        for n in s["nodes"]:
            if n["isFork"] or n["isArchived"]: continue
            prt=n["pullRequests"]["totalCount"]
            if prt>=100:
                repos.append({"owner":n["owner"]["login"],"name":n["name"],"full_name":n["nameWithOwner"],"url":n["url"],"stars":n["stargazerCount"],"forks":n["forkCount"],"open_issues":n["issues"]["totalCount"],"prs_total_closed_merged":prt})
                if len(repos)>=TARGET: break
        if not s["pageInfo"]["hasNextPage"]: break
        after=s["pageInfo"]["endCursor"]
    df=pd.DataFrame(repos,columns=REPOS_COLUMNS).sort_values("stars",ascending=False)
    df.to_csv("data/repositorios_selecionados.csv",index=False,encoding="utf-8")
    print(f"Salvo data/repositorios_selecionados.csv ({len(df)})")
if __name__=="__main__": main()
