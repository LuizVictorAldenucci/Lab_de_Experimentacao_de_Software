$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path tools | Out-Null
Set-Location tools

$CK_VERSION = "0.7.1"
$CK_URL = "https://repo1.maven.org/maven2/com/github/mauricioaniche/ck/$CK_VERSION/ck-$CK_VERSION.jar"

Write-Host "Baixando CK $CK_VERSION de $CK_URL ..."
Invoke-WebRequest -Uri $CK_URL -OutFile "ck.jar"

Write-Host "OK! ck.jar salvo em tools/ck.jar"
