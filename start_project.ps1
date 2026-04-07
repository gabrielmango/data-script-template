# ===============================
# Setup Projeto Python no Windows
# ===============================

# Versao do Python que voce quer usar
$PythonVersion = "3.12.0"
$EnvName = "venv"
$ReqFile = "requirements.txt"

Write-Host "================================="
Write-Host "Configurando Python com pyenv-win"
Write-Host "================================="

# Verifica se a versao do Python ja esta instalada
$installed = pyenv versions | Select-String $PythonVersion
if (-not $installed) {
    Write-Host "Instalando Python $PythonVersion via pyenv..."
    pyenv install $PythonVersion
} else {
    Write-Host "Python $PythonVersion ja instalado"
}

# Define a versao local do projeto
pyenv local $PythonVersion
Write-Host "Python ativo no projeto: $(python --version)"

Write-Host "=============================="
Write-Host "Criando ambiente virtual"
Write-Host "=============================="

if (-Not (Test-Path $EnvName)) {
    python -m venv $EnvName
    Write-Host "Ambiente virtual $EnvName criado com sucesso"
} else {
    Write-Host "Ambiente virtual $EnvName ja existe"
}

Write-Host "=============================="
Write-Host "Ativando ambiente virtual"
Write-Host "=============================="

# Ativa o ambiente no terminal atual
$activatePath = ".\$EnvName\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Ativando $EnvName..."
    & $activatePath
} else {
    Write-Host "Erro: arquivo de ativacao nao encontrado!"
    exit
}

Write-Host "=================================="
Write-Host "Instalando dependencias existentes"
Write-Host "=================================="

if (Test-Path $ReqFile) {
    Write-Host "$ReqFile encontrado! Instalando dependencias..."
    pip install -r $ReqFile
    Write-Host "Dependencias instaladas com sucesso!"
} else {
    Write-Host "$ReqFile nao encontrado!"
}

Write-Host "=============================="
Write-Host "Setup concluido!"
Write-Host "Para ativar o ambiente futuramente: .\$EnvName\Scripts\Activate.ps1"
