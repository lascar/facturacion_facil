# Script d'installation PowerShell pour Windows 11
# Facturación Fácil - Version PyQt6 optimisée

param(
    [switch]$SkipPythonCheck,
    [switch]$DevTools,
    [switch]$CreateShortcut,
    [string]$PythonVersion = "3.12"
)

# Configuration des couleurs pour une meilleure lisibilité
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "White"

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "💡 $Message" -ForegroundColor Blue
}

function Test-WindowsVersion {
    Write-Header "VÉRIFICATION DE WINDOWS 11"
    
    $version = [System.Environment]::OSVersion.Version
    $build = $version.Build
    
    Write-Host "Version Windows: $($version.Major).$($version.Minor) Build $build"
    
    if ($build -ge 22000) {
        Write-Success "Windows 11 détecté - Optimisations disponibles"
        return $true
    } elseif ($build -ge 10240) {
        Write-Warning "Windows 10 détecté - Compatible mais non optimisé"
        return $true
    } else {
        Write-Error "Version Windows non supportée"
        return $false
    }
}

function Install-Python {
    param([string]$Version)
    
    Write-Header "INSTALLATION DE PYTHON $Version"
    
    # Vérifier si Python est déjà installé
    try {
        $currentVersion = python --version 2>$null
        if ($currentVersion) {
            Write-Success "Python déjà installé: $currentVersion"
            return $true
        }
    } catch {
        Write-Info "Python non détecté, installation nécessaire"
    }
    
    # Essayer d'installer avec winget
    Write-Info "Tentative d'installation avec winget..."
    try {
        winget install Python.Python.$Version --accept-source-agreements --accept-package-agreements
        Write-Success "Python $Version installé avec winget"
        return $true
    } catch {
        Write-Warning "Échec de l'installation avec winget"
    }
    
    # Instructions manuelles
    Write-Info "Installation manuelle requise:"
    Write-Host "1. Ouvrir Microsoft Store"
    Write-Host "2. Rechercher 'Python $Version'"
    Write-Host "3. Installer la version officielle"
    Write-Host "4. Redémarrer ce script"
    
    return $false
}

function Setup-VirtualEnvironment {
    Write-Header "CONFIGURATION DE L'ENVIRONNEMENT VIRTUEL"
    
    if (Test-Path "venv") {
        $response = Read-Host "Environnement virtuel existant. Recréer? (y/N)"
        if ($response -eq "y" -or $response -eq "Y") {
            Remove-Item -Recurse -Force "venv"
            Write-Info "Ancien environnement supprimé"
        } else {
            Write-Info "Utilisation de l'environnement existant"
            return $true
        }
    }
    
    Write-Info "Création de l'environnement virtuel..."
    python -m venv venv
    
    if (Test-Path "venv\Scripts\activate.ps1") {
        Write-Success "Environnement virtuel créé"
        return $true
    } else {
        Write-Error "Échec de la création de l'environnement virtuel"
        return $false
    }
}

function Install-Dependencies {
    Write-Header "INSTALLATION DES DÉPENDANCES"
    
    # Activer l'environnement virtuel
    & "venv\Scripts\Activate.ps1"
    
    # Mettre à jour pip
    Write-Info "Mise à jour de pip..."
    python -m pip install --upgrade pip
    
    # Installer les dépendances principales
    Write-Info "Installation des dépendances principales..."
    pip install -r requirements.txt
    
    if ($DevTools) {
        Write-Info "Installation des outils de développement..."
        pip install -r requirements-dev.txt
    }
    
    Write-Success "Dépendances installées"
}

function Test-Installation {
    Write-Header "TEST DE L'INSTALLATION"
    
    # Activer l'environnement virtuel
    & "venv\Scripts\Activate.ps1"
    
    # Exécuter le test de compatibilité
    python test_windows11_compatibility.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Tests de compatibilité réussis"
        return $true
    } else {
        Write-Error "Échec des tests de compatibilité"
        return $false
    }
}

function Create-DesktopShortcut {
    Write-Header "CRÉATION DU RACCOURCI"
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "Facturación Fácil.lnk"
    $currentPath = Get-Location
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-WindowStyle Hidden -Command `"cd '$currentPath'; & 'venv\Scripts\Activate.ps1'; python main.py`""
    $shortcut.WorkingDirectory = $currentPath
    $shortcut.Description = "Facturación Fácil - Sistema de Facturación"
    $shortcut.Save()
    
    Write-Success "Raccourci créé sur le bureau"
}

# Script principal
try {
    Write-Header "INSTALLATION FACTURACIÓN FÁCIL POUR WINDOWS 11"
    
    # Vérifier les privilèges administrateur si nécessaire
    if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Warning "Certaines fonctionnalités peuvent nécessiter des privilèges administrateur"
    }
    
    # Étapes d'installation
    $steps = @(
        @{ Name = "Vérification Windows"; Action = { Test-WindowsVersion } },
        @{ Name = "Installation Python"; Action = { if (-not $SkipPythonCheck) { Install-Python $PythonVersion } else { $true } } },
        @{ Name = "Environnement virtuel"; Action = { Setup-VirtualEnvironment } },
        @{ Name = "Installation dépendances"; Action = { Install-Dependencies } },
        @{ Name = "Test installation"; Action = { Test-Installation } }
    )
    
    $success = $true
    foreach ($step in $steps) {
        Write-Info "Étape: $($step.Name)..."
        $result = & $step.Action
        if (-not $result) {
            Write-Error "Échec de l'étape: $($step.Name)"
            $success = $false
            break
        }
    }
    
    if ($success) {
        if ($CreateShortcut) {
            Create-DesktopShortcut
        }
        
        Write-Header "🎉 INSTALLATION RÉUSSIE!"
        Write-Success "Facturación Fácil est prêt à être utilisé"
        Write-Info "Pour lancer l'application:"
        Write-Host "  1. Ouvrir PowerShell dans ce dossier"
        Write-Host "  2. Exécuter: & 'venv\Scripts\Activate.ps1'"
        Write-Host "  3. Exécuter: python main.py"
        
        $launch = Read-Host "Lancer l'application maintenant? (y/N)"
        if ($launch -eq "y" -or $launch -eq "Y") {
            & "venv\Scripts\Activate.ps1"
            python main.py
        }
    } else {
        Write-Error "L'installation a échoué. Consultez les messages d'erreur ci-dessus."
        exit 1
    }
    
} catch {
    Write-Error "Erreur inattendue: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    exit 1
}
