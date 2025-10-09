import argparse,pandas as pd
from scipy.stats import spearmanr,pearsonr
ap=argparse.ArgumentParser(); ap.add_argument('--csv',required=True); ap.add_argument('--method',choices=['spearman','pearson'],default='spearman'); args=ap.parse_args()
df=pd.read_csv(args.csv).copy(); df['status_bin']=(df['state']=='MERGED').astype(int)
pairs=[('changedFiles','status_bin'),('additions','status_bin'),('deletions','status_bin'),('tempo_analise_horas','status_bin'),('desc_len','status_bin'),('participants','status_bin'),('comments','status_bin'),('changedFiles','reviews'),('additions','reviews'),('deletions','reviews'),('tempo_analise_horas','reviews'),('desc_len','reviews'),('participants','reviews'),('comments','reviews')]
for a,b in pairs:
    x=df[a].astype(float); y=df[b].astype(float)
    if args.method=='spearman': c,p=spearmanr(x,y,nan_policy='omit')
    else: c,p=pearsonr(x,y)
    print(f"{args.method.upper()}({a}~{b})={c:.4f}, p={p:.4g}")
