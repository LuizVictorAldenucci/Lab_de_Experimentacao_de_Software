# CK (Chidamber & Kemerer) + Extras

Este diretório armazenará o `ck.jar`. Para baixar, rode:

```bash
bash scripts/download_ck.sh
# ou no Windows:
powershell -ExecutionPolicy Bypass -File scripts/download_ck.ps1
```

Execução do CK (exemplo):

```bash
java -jar tools/ck.jar <caminho-do-projeto-java> true 0 false data/ck_output/<nome>
```

Onde os argumentos são:
- `true`: considerar dependências externas (useJars)
- `0`: processar sem limite de projetos simultâneos (maxAtOnce)
- `false`: não incluir variáveis e campos (variablesAndFields)
- `data/ck_output/<nome>`: diretório de saída onde serão gerados `class.csv`, `method.csv`, `variable.csv`, etc.
