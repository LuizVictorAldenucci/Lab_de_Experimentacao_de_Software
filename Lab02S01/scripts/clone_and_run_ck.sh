#!/usr/bin/env bash
set -euo pipefail

# Executa CK em lote a partir de um CSV gerado por fetch_top_repos.py
# Uso:
#   bash scripts/clone_and_run_ck.sh --input data/java_repos_top1000.csv --limit 50

CK_JAR="tools/ck.jar"
INPUT="data/java_repos_top1000.csv"
LIMIT=0  # 0 = sem limite
OUT_ROOT="data/ck_output"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2;;
    --limit) LIMIT="$2"; shift 2;;
    *) echo "Parâmetro desconhecido: $1"; exit 1;;
  esac
done

if [[ ! -f "$CK_JAR" ]]; then
  echo "Erro: $CK_JAR não encontrado. Rode: bash scripts/download_ck.sh"
  exit 1
fi
if [[ ! -f "$INPUT" ]]; then
  echo "Erro: CSV de entrada não encontrado em $INPUT"
  exit 1
fi

mkdir -p repos "$OUT_ROOT"

# pular cabeçalho; ler campo "full_name" (coluna 2)
count=0
tail -n +2 "$INPUT" | cut -d',' -f2 | while read -r full_name; do
  [[ -z "$full_name" ]] && continue
  ((count++))
  if [[ "$LIMIT" -gt 0 && "$count" -gt "$LIMIT" ]]; then
    echo "Limite alcançado ($LIMIT). Saindo."
    break
  fi

  safe=$(echo "$full_name" | sed 's/[\/:]/__/g')
  repo_dir="repos/${safe}"
  out_dir="$OUT_ROOT/${safe}"
  if [[ -d "$repo_dir" ]]; then rm -rf "$repo_dir"; fi
  echo "[$count] Clonando $full_name ..."
  git clone --depth=1 "https://github.com/${full_name}" "$repo_dir" || { echo "Falhou clonar $full_name"; continue; }

  mkdir -p "$out_dir"
  echo "[$count] Rodando CK em $full_name ..."
  java -jar "$CK_JAR" "$repo_dir" true 0 false "$out_dir" || { echo "Falhou CK em $full_name"; continue; }
done

echo "Processamento em lote concluído."
