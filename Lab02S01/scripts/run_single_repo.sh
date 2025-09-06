#!/usr/bin/env bash
set -euo pipefail

# Uso:
#   bash scripts/run_single_repo.sh <owner/repo>         # remoto do GitHub
#   bash scripts/run_single_repo.sh examples/helloworld-java   # projeto local
#
# Requer: tools/ck.jar (use scripts/download_ck.sh)

CK_JAR="tools/ck.jar"
OUT_ROOT="data/ck_output"

if [[ ! -f "$CK_JAR" ]]; then
  echo "Erro: $CK_JAR não encontrado. Rode: bash scripts/download_ck.sh"
  exit 1
fi

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Uso: bash scripts/run_single_repo.sh <owner/repo | caminho_local>"
  exit 1
fi

workdir=""
outdir=""

if [[ -d "$TARGET" ]]; then
  workdir="$TARGET"
  safe=$(echo "$TARGET" | sed 's/[\/:]/_/g')
  outdir="$OUT_ROOT/${safe}"
else
  safe=$(echo "$TARGET" | sed 's/[\/:]/__/g')
  workdir="repos/${safe}"
  outdir="$OUT_ROOT/${safe}"
  mkdir -p repos
  if [[ -d "$workdir" ]]; then rm -rf "$workdir"; fi
  echo "Clonando https://github.com/$TARGET ..."
  git clone --depth=1 "https://github.com/$TARGET" "$workdir"
fi

mkdir -p "$outdir"
echo "Executando CK em $workdir ..."
# CK CLI: java -jar ck.jar <path> <useJars> <maxAtOnce> <variablesAndFields> <outputDir>
java -jar "$CK_JAR" "$workdir" true 0 false "$outdir"

echo "Concluído. Arquivos do CK em: $outdir"
