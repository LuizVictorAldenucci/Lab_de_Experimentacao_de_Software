import argparse,pandas as pd
ap=argparse.ArgumentParser(); ap.add_argument('--csv',required=True); args=ap.parse_args()
df=pd.read_csv(args.csv)
cols=['changedFiles','additions','deletions','desc_len','participants','comments','reviews','tempo_analise_horas']
print('Medianas gerais:'); print(df[cols].median(numeric_only=True).to_string())
print('\nMedianas por estado:'); print(df.groupby('state')[cols].median(numeric_only=True).to_string())
