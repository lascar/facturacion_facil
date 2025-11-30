# Script PowerShell pour lancer Facturacion Facil sur Windows 11
# Execution: .\start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Facturacion Facil - Demarrage" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Changer vers le repertoire du script
Set-Location $PSScriptRoot

# Verifier si Python est installe
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python detecte: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Python n'est pas installe ou pas dans le PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer Python depuis https://python.org" -ForegroundColor Yellow
    Write-Host "N'oubliez pas de cocher 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Appuyez sur Entree pour continuer"
    exit 1
}

# Verifier si l'environnement virtuel existe
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Creation de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Impossible de creer l'environnement virtuel" -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour continuer"
        exit 1
    }
}

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Verifier si les dependances sont installees
try {
    python -c "import PyQt5" 2>$null
    Write-Host "Dependances deja installees" -ForegroundColor Green
} catch {
    Write-Host "Installation des dependances..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Impossible d'installer les dependances" -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour continuer"
        exit 1
    }
}

# Lancer l'application
Write-Host ""
Write-Host "Lancement de Facturacion Facil..." -ForegroundColor Green
Write-Host ""

try {
    python main.py
} catch {
    Write-Host ""
    Write-Host "ERREUR: L'application s'est fermee avec une erreur" -ForegroundColor Red
    Write-Host "Verifiez les logs dans le dossier 'logs/'" -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Appuyez sur Entree pour continuer"
