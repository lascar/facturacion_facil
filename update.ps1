# PowerShell Script pour Mise à Jour - Facturación Fácil
# Exécution: PowerShell -ExecutionPolicy Bypass -File update.ps1

param(
    [switch]$Force,
    [switch]$NoBackup,
    [switch]$Quiet
)

# Configuration
$AppName = "Facturación Fácil"
$MainFile = "main.py"
$DbFile = "facturacion.db"
$BackupDir = "backups"

# Couleurs pour l'affichage
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success { Write-ColorOutput Green $args }
function Write-Warning { Write-ColorOutput Yellow $args }
function Write-Error { Write-ColorOutput Red $args }
function Write-Info { Write-ColorOutput Cyan $args }

# Fonction pour afficher le titre
function Show-Title {
    if (-not $Quiet) {
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "   🔄 MISE À JOUR - $AppName" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
    }
}

# Fonction pour vérifier les prérequis
function Test-Prerequisites {
    Write-Info "🔍 Vérification des prérequis..."
    
    # Vérifier Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Python: $pythonVersion"
        } else {
            throw "Python non trouvé"
        }
    } catch {
        Write-Error "❌ Python n'est pas installé ou pas dans le PATH"
        return $false
    }
    
    # Vérifier Git
    try {
        $gitVersion = git --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Git: $gitVersion"
        } else {
            throw "Git non trouvé"
        }
    } catch {
        Write-Error "❌ Git n'est pas installé ou pas dans le PATH"
        return $false
    }
    
    # Vérifier le fichier principal
    if (-not (Test-Path $MainFile)) {
        Write-Error "❌ Fichier $MainFile non trouvé"
        Write-Error "Assurez-vous d'être dans le répertoire de l'application"
        return $false
    }
    
    Write-Success "✅ Tous les prérequis sont satisfaits"
    return $true
}

# Fonction pour créer une sauvegarde
function New-Backup {
    if ($NoBackup) {
        Write-Warning "⚠️ Sauvegarde ignorée (paramètre -NoBackup)"
        return $true
    }
    
    Write-Info "💾 Création de la sauvegarde..."
    
    # Créer le répertoire de sauvegarde
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir | Out-Null
    }
    
    # Générer un nom de sauvegarde avec timestamp
    $timestamp = Get-Date -Format "yyyyMMdd_HHmm"
    $backupName = "backup_$timestamp"
    
    try {
        # Sauvegarder la base de données
        if (Test-Path $DbFile) {
            Copy-Item $DbFile "$BackupDir\${backupName}_$DbFile"
            Write-Success "✅ Base de données sauvegardée"
        }
        
        # Sauvegarder la configuration
        if (Test-Path "config") {
            Copy-Item "config" "$BackupDir\${backupName}_config" -Recurse
            Write-Success "✅ Configuration sauvegardée"
        }
        
        return $true
    } catch {
        Write-Error "❌ Erreur lors de la sauvegarde: $_"
        return $false
    }
}

# Fonction pour vérifier les mises à jour disponibles
function Test-UpdatesAvailable {
    Write-Info "🌐 Vérification des mises à jour disponibles..."
    
    try {
        # Récupérer les informations du dépôt distant
        git fetch origin 2>$null
        
        # Comparer avec la branche locale
        $updates = git log HEAD..origin/main --oneline 2>$null
        
        if ($updates) {
            Write-Info "📥 Mises à jour disponibles:"
            $updates | ForEach-Object { Write-Host "  • $_" -ForegroundColor Yellow }
            return $true
        } else {
            Write-Success "✅ Application déjà à jour"
            return $false
        }
    } catch {
        Write-Error "❌ Impossible de vérifier les mises à jour: $_"
        return $false
    }
}

# Fonction pour appliquer les mises à jour
function Update-Application {
    Write-Info "🔄 Application des mises à jour..."
    
    try {
        # Appliquer les mises à jour Git
        git pull origin main
        if ($LASTEXITCODE -ne 0) {
            throw "Échec de git pull"
        }
        Write-Success "✅ Code mis à jour"
        
        # Vérifier l'environnement virtuel
        if (-not (Test-Path "env\Scripts\activate.bat")) {
            Write-Warning "⚠️ Environnement virtuel non trouvé, création..."
            python -m venv env
            if ($LASTEXITCODE -ne 0) {
                throw "Impossible de créer l'environnement virtuel"
            }
        }
        
        # Mettre à jour les dépendances
        Write-Info "📦 Mise à jour des dépendances..."
        & "env\Scripts\python.exe" -m pip install -r requirements.txt --upgrade --quiet
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "⚠️ Problème lors de la mise à jour des dépendances"
        } else {
            Write-Success "✅ Dépendances mises à jour"
        }
        
        return $true
    } catch {
        Write-Error "❌ Erreur lors de la mise à jour: $_"
        return $false
    }
}

# Fonction pour tester l'application
function Test-Application {
    Write-Info "🧪 Test de l'application..."
    
    try {
        $testResult = python -c "import main; print('OK')" 2>$null
        if ($LASTEXITCODE -eq 0 -and $testResult -eq "OK") {
            Write-Success "✅ Application testée avec succès"
            return $true
        } else {
            throw "Test d'import échoué"
        }
    } catch {
        Write-Error "❌ Problème détecté lors du test: $_"
        return $false
    }
}

# Fonction principale
function Main {
    Show-Title
    
    # Vérifier les prérequis
    if (-not (Test-Prerequisites)) {
        Write-Error "Prérequis non satisfaits. Arrêt de la mise à jour."
        exit 1
    }
    
    # Vérifier s'il y a des mises à jour
    if (-not $Force) {
        $hasUpdates = Test-UpdatesAvailable
        if (-not $hasUpdates) {
            if (-not $Quiet) {
                Write-Host "Appuyez sur une touche pour fermer..."
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
            exit 0
        }
        
        # Demander confirmation
        if (-not $Quiet) {
            $response = Read-Host "Voulez-vous appliquer ces mises à jour? (O/N)"
            if ($response -notmatch "^[Oo]$") {
                Write-Host "Mise à jour annulée"
                exit 0
            }
        }
    }
    
    # Créer une sauvegarde
    if (-not (New-Backup)) {
        Write-Error "Échec de la sauvegarde. Arrêt de la mise à jour."
        exit 1
    }
    
    # Appliquer les mises à jour
    if (-not (Update-Application)) {
        Write-Error "Échec de la mise à jour."
        exit 1
    }
    
    # Tester l'application
    if (-not (Test-Application)) {
        Write-Warning "⚠️ Problème détecté après mise à jour"
        Write-Warning "Vous pouvez restaurer la sauvegarde avec restore.bat"
    }
    
    # Succès
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    if (-not $Quiet) {
        $response = Read-Host "Voulez-vous lancer l'application maintenant? (O/N)"
        if ($response -match "^[Oo]$") {
            Write-Info "🚀 Lancement de l'application..."
            Start-Process python -ArgumentList "main.py"
        }
        
        Write-Host ""
        Write-Host "Appuyez sur une touche pour fermer..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

# Exécuter le script principal
try {
    Main
} catch {
    Write-Error "❌ Erreur inattendue: $_"
    if (-not $Quiet) {
        Write-Host "Appuyez sur une touche pour fermer..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    exit 1
}
