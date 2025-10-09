import argparse,math
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from utils import gh_graphql
from schemas import PRS_COLUMNS
Q="""query($owner:String!,$name:String!,$after:String){{
  repository(owner:$owner,name:$name){{
    nameWithOwner
    pullRequests(states:[MERGED,CLOSED],first:50,after:$after,orderBy:{{field:UPDATED_AT,direction:DESC}}){{
      pageInfo{{hasNextPage endCursor}}
      nodes{{number url state createdAt closedAt mergedAt changedFiles additions deletions bodyText
        participants{{totalCount}} comments{{totalCount}} reviews:reviews{{totalCount}} }}
    }}
  }}
}}"""
def horas(a,b):
    if not a or not b: return math.nan
    da=datetime.fromisoformat(a.replace("Z","+00:00")); db=datetime.fromisoformat(b.replace("Z","+00:00"))
    return (db-da).total_seconds()/3600.0
def coleta(owner,name,maxn):
    out=[]; after=None; got=0
    while True:
        d=gh_graphql(Q,{"owner":owner,"name":name,"after":after}); repo=d["repository"]; 
        if repo is None: break
        prc=repo["pullRequests"]
        for pr in prc["nodes"]:
            if (pr["reviews"]["totalCount"] or 0)<1: continue
            fim=pr["mergedAt"] or pr["closedAt"]; if fim is None: continue
            h=horas(pr["createdAt"],fim); if math.isnan(h) or h<1.0: continue
            out.append({"repo_full_name":repo["nameWithOwner"],"number":pr["number"],"url":pr["url"],"state":pr["state"],"createdAt":pr["createdAt"],"closedAt":pr["closedAt"],"mergedAt":pr["mergedAt"],"changedFiles":pr["changedFiles"],"additions":pr["additions"],"deletions":pr["deletions"],"desc_len":len(pr["bodyText"] or ""), "participants":pr["participants"]["totalCount"],"comments":pr["comments"]["totalCount"],"reviews":pr["reviews"]["totalCount"],"tempo_analise_horas":round(h,3)})
            got+=1
            if maxn and got>=maxn: break
        if maxn and got>=maxn: break
        if not prc["pageInfo"]["hasNextPage"]: break
        after=prc["pageInfo"]["endCursor"]
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repos-csv",default="data/repositorios_selecionados.csv")
    ap.add_argument("--max-prs-por-repo",type=int,default=0)
    ap.add_argument("--saida",default="data/prs_dataset.csv")
    args=ap.parse_args()
    repos=pd.read_csv(args.repos_csv)
    todos=[]
    for _,r in tqdm(repos.iterrows(),total=len(repos),desc="Coletando PRs"):
        todos.extend(coleta(r["owner"],r["name"],args.max_prs_por_repo))
    pd.DataFrame(todos,columns=PRS_COLUMNS).to_csv(args.saida,index=False,encoding="utf-8")
    print(f"Salvo {args.saida} ({len(todos)} PRs)")
if __name__=="__main__": main()
