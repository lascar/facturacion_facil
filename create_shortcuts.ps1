# Script PowerShell pour créer des raccourcis avec icônes
# Facturación Fácil - Raccourcis Bureau

param(
    [switch]$Force = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎯 CRÉATION DES RACCOURCIS BUREAU" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si on est dans le bon répertoire
if (-not (Test-Path "main.py")) {
    Write-Host "❌ ERREUR: Fichier main.py non trouvé" -ForegroundColor Red
    Write-Host "Assurez-vous d'être dans le répertoire de l'application" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour fermer"
    exit 1
}

# Chemins
$AppDir = Get-Location
$Desktop = [Environment]::GetFolderPath("Desktop")
$StartMenu = [Environment]::GetFolderPath("StartMenu")

Write-Host "📁 Répertoire de l'application: $AppDir" -ForegroundColor Green
Write-Host "🖥️  Bureau: $Desktop" -ForegroundColor Green
Write-Host ""

# Fonction pour créer un raccourci
function Create-Shortcut {
    param(
        [string]$ShortcutPath,
        [string]$TargetPath,
        [string]$Description,
        [string]$IconPath = $null,
        [string]$Arguments = ""
    )
    
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $AppDir
    $Shortcut.Description = $Description
    $Shortcut.Arguments = $Arguments
    
    if ($IconPath -and (Test-Path $IconPath)) {
        $Shortcut.IconLocation = "$IconPath,0"
    }
    
    $Shortcut.Save()
    return $true
}

# Créer le script de lancement optimisé
Write-Host "🚀 Création du script de lancement..." -ForegroundColor Yellow

$LaunchScript = @"
@echo off
title Facturación Fácil
cd /d "$AppDir"

:: Démarrage silencieux - détection Python
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py
    ) else (
        set PYTHON_CMD=python3
    )
)

:: Activer l'environnement virtuel ou le créer
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat >nul 2>&1
) else if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat >nul 2>&1
) else (
    echo Initialisation de l'environnement...
    %PYTHON_CMD% -m venv venv >nul 2>&1
    call venv\Scripts\activate.bat >nul 2>&1
    pip install -r requirements.txt >nul 2>&1
)

:: Lancer l'application
%PYTHON_CMD% main.py

:: Pause seulement en cas d'erreur
if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du lancement
    echo Vérifiez les logs dans le dossier 'logs/'
    pause
)
"@

$LaunchScript | Out-File -FilePath "launch_app.bat" -Encoding ASCII

# Créer le script de mise à jour optimisé
Write-Host "🔄 Création du script de mise à jour..." -ForegroundColor Yellow

$UpdateScript = @"
@echo off
chcp 65001 >nul
title Mise à Jour - Facturación Fácil
cd /d "$AppDir"

echo ========================================
echo   🔄 MISE À JOUR FACTURACIÓN FÁCIL
echo ========================================
echo.

:: Vérifier Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git non installé
    echo.
    echo 💡 Installer Git depuis: https://git-scm.com/download/win
    echo Puis relancer cette mise à jour
    pause
    exit /b 1
)

echo 📡 Vérification des mises à jour disponibles...
git fetch origin >nul 2>&1

:: Comparer les versions
for /f %%i in ('git rev-list HEAD..origin/main --count') do set UPDATE_COUNT=%%i
if "%UPDATE_COUNT%"=="0" (
    echo ✅ Application déjà à jour!
    echo.
    timeout /t 3 /nobreak >nul
    exit /b 0
)

echo 🎯 %UPDATE_COUNT% mise(s) à jour disponible(s)
echo.
echo Voulez-vous continuer? (O/N)
set /p choice=
if /i not "%choice%"=="O" if /i not "%choice%"=="o" (
    echo Mise à jour annulée
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo.
echo 💾 Sauvegarde des données...
if not exist "backup" mkdir backup
if exist "facturacion.db" copy "facturacion.db" "backup\facturacion_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db" >nul
if exist "config.json" copy "config.json" "backup\config_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json" >nul
echo ✅ Sauvegarde terminée

echo.
echo 📥 Téléchargement des mises à jour...
git pull origin main
if errorlevel 1 (
    echo ❌ Erreur lors de la mise à jour
    pause
    exit /b 1
)

echo.
echo 📦 Mise à jour des dépendances...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
)
pip install -r requirements.txt --upgrade --quiet

echo.
echo ========================================
echo   ✅ MISE À JOUR TERMINÉE!
echo ========================================
echo.
echo L'application a été mise à jour avec succès
echo Vous pouvez maintenant la relancer
echo.
timeout /t 5 /nobreak >nul
"@

$UpdateScript | Out-File -FilePath "update_app.bat" -Encoding ASCII

Write-Host "✅ Scripts créés avec succès" -ForegroundColor Green
Write-Host ""

# Créer les raccourcis sur le bureau
Write-Host "🔗 Création des raccourcis sur le bureau..." -ForegroundColor Yellow

# Raccourci de lancement
$LaunchShortcut = "$Desktop\🚀 Facturación Fácil.lnk"
$IconPath = "$AppDir\assets\icon.ico"

if (Test-Path $IconPath) {
    Write-Host "   📱 Avec icône personnalisée" -ForegroundColor Cyan
} else {
    Write-Host "   📱 Avec icône par défaut" -ForegroundColor Cyan
    $IconPath = $null
}

try {
    Create-Shortcut -ShortcutPath $LaunchShortcut -TargetPath "$AppDir\launch_app.bat" -Description "Lancer Facturación Fácil" -IconPath $IconPath
    Write-Host "   ✅ Raccourci de lancement créé" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Erreur lors de la création du raccourci de lancement" -ForegroundColor Red
}

# Raccourci de mise à jour
$UpdateShortcut = "$Desktop\🔄 Mise à Jour Facturación Fácil.lnk"

try {
    Create-Shortcut -ShortcutPath $UpdateShortcut -TargetPath "$AppDir\update_app.bat" -Description "Mettre à jour Facturación Fácil depuis GitHub"
    Write-Host "   ✅ Raccourci de mise à jour créé" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Erreur lors de la création du raccourci de mise à jour" -ForegroundColor Red
}

# Optionnel : Créer aussi dans le menu Démarrer
$CreateStartMenu = Read-Host "Créer aussi les raccourcis dans le menu Démarrer? (O/N)"
if ($CreateStartMenu -eq "O" -or $CreateStartMenu -eq "o") {
    $StartMenuFolder = "$StartMenu\Programs\Facturación Fácil"
    
    if (-not (Test-Path $StartMenuFolder)) {
        New-Item -ItemType Directory -Path $StartMenuFolder -Force | Out-Null
    }
    
    try {
        Create-Shortcut -ShortcutPath "$StartMenuFolder\Facturación Fácil.lnk" -TargetPath "$AppDir\launch_app.bat" -Description "Lancer Facturación Fácil" -IconPath $IconPath
        Create-Shortcut -ShortcutPath "$StartMenuFolder\Mise à Jour.lnk" -TargetPath "$AppDir\update_app.bat" -Description "Mettre à jour Facturación Fácil"
        Write-Host "   ✅ Raccourcis du menu Démarrer créés" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Erreur lors de la création des raccourcis du menu Démarrer" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎉 RACCOURCIS CRÉÉS AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Raccourcis créés sur le bureau:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   🚀 Facturación Fácil" -ForegroundColor Green
Write-Host "      → Lance l'application directement" -ForegroundColor Gray
Write-Host "      → Gère automatiquement l'environnement virtuel" -ForegroundColor Gray
Write-Host "      → Installe les dépendances si nécessaire" -ForegroundColor Gray
Write-Host ""
Write-Host "   🔄 Mise à Jour Facturación Fácil" -ForegroundColor Green
Write-Host "      → Met à jour depuis GitHub" -ForegroundColor Gray
Write-Host "      → Sauvegarde automatique des données" -ForegroundColor Gray
Write-Host "      → Mise à jour des dépendances" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Utilisation:" -ForegroundColor Yellow
Write-Host "   • Double-clic sur l'icône pour lancer" -ForegroundColor White
Write-Host "   • Double-clic sur l'icône de mise à jour pour mettre à jour" -ForegroundColor White
Write-Host "   • Aucune connaissance technique requise!" -ForegroundColor White
Write-Host ""
Write-Host "🎯 L'utilisateur final n'a plus qu'à cliquer sur les icônes!" -ForegroundColor Cyan
Write-Host ""

Read-Host "Appuyez sur Entrée pour fermer"
