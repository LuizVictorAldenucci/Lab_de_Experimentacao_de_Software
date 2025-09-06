#!/usr/bin/env bash
set -euo pipefail

mkdir -p tools
cd tools

# Versão estável conhecida do CK
CK_VERSION="0.7.1"
CK_URL="https://repo1.maven.org/maven2/com/github/mauricioaniche/ck/${CK_VERSION}/ck-${CK_VERSION}.jar"

echo "Baixando CK ${CK_VERSION} de ${CK_URL} ..."
curl -L -o ck.jar "$CK_URL"

echo "OK! ck.jar salvo em tools/ck.jar"
