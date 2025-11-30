@echo off
chcp 65001 >nul
title Diagnostic Mise à Jour - Facturación Fácil

echo ========================================
echo   🔍 DIAGNOSTIC MISE À JOUR
echo ========================================
echo.

:: Vérifier l'environnement
echo 🔧 Vérification de l'environnement...
echo.

:: Vérifier Python
echo 🐍 Python:
python --version 2>nul
if errorlevel 1 (
    echo   ❌ Python non trouvé ou non installé
    set python_ok=0
) else (
    echo   ✅ Python installé
    set python_ok=1
)

:: Vérifier Git
echo.
echo 📦 Git:
git --version 2>nul
if errorlevel 1 (
    echo   ❌ Git non trouvé ou non installé
    set git_ok=0
) else (
    echo   ✅ Git installé
    set git_ok=1
)

:: Vérifier l'environnement virtuel
echo.
echo 🔧 Environnement virtuel:
if exist "env\Scripts\activate.bat" (
    echo   ✅ Environnement virtuel trouvé
    set venv_ok=1
) else (
    echo   ❌ Environnement virtuel non trouvé
    set venv_ok=0
)

:: Vérifier les fichiers principaux
echo.
echo 📁 Fichiers de l'application:
if exist "main.py" (
    echo   ✅ main.py trouvé
    set main_ok=1
) else (
    echo   ❌ main.py non trouvé
    set main_ok=0
)

if exist "requirements.txt" (
    echo   ✅ requirements.txt trouvé
    set req_ok=1
) else (
    echo   ❌ requirements.txt non trouvé
    set req_ok=0
)

if exist "facturacion.db" (
    echo   ✅ Base de données trouvée
    set db_ok=1
) else (
    echo   ⚠️  Base de données non trouvée (sera créée au premier lancement)
    set db_ok=1
)

:: Vérifier l'état Git
echo.
echo 📋 État Git:
if %git_ok%==1 (
    git status --porcelain >nul 2>&1
    if errorlevel 1 (
        echo   ❌ Pas un dépôt Git ou problème Git
        set git_status_ok=0
    ) else (
        git status --porcelain > temp_status.txt
        for /f %%i in ('type temp_status.txt ^| find /c /v ""') do set modified_files=%%i
        del temp_status.txt
        
        if %modified_files%==0 (
            echo   ✅ Aucune modification locale
        ) else (
            echo   ⚠️  %modified_files% fichier(s) modifié(s) localement
        )
        
        :: Vérifier les mises à jour disponibles
        git fetch origin >nul 2>&1
        git log HEAD..origin/main --oneline >nul 2>&1
        if errorlevel 1 (
            echo   ✅ Application à jour
        ) else (
            for /f %%i in ('git log HEAD..origin/main --oneline ^| find /c /v ""') do set updates=%%i
            echo   📥 %updates% mise(s) à jour disponible(s)
        )
        set git_status_ok=1
    )
) else (
    echo   ❌ Git non disponible
    set git_status_ok=0
)

:: Vérifier les dépendances
echo.
echo 📦 Dépendances Python:
if %venv_ok%==1 if %python_ok%==1 (
    call env\Scripts\activate.bat
    pip check >nul 2>&1
    if errorlevel 1 (
        echo   ⚠️  Problèmes de dépendances détectés
        set deps_ok=0
    ) else (
        echo   ✅ Dépendances OK
        set deps_ok=1
    )
) else (
    echo   ❌ Impossible de vérifier (Python ou venv manquant)
    set deps_ok=0
)

:: Test de l'application
echo.
echo 🧪 Test de l'application:
if %python_ok%==1 if %main_ok%==1 (
    python -c "import main; print('✅ Application peut être importée')" 2>nul
    if errorlevel 1 (
        echo   ❌ Erreur lors de l'import de l'application
        set app_ok=0
    ) else (
        echo   ✅ Application testée avec succès
        set app_ok=1
    )
) else (
    echo   ❌ Impossible de tester (Python ou main.py manquant)
    set app_ok=0
)

:: Résumé du diagnostic
echo.
echo ========================================
echo   📊 RÉSUMÉ DU DIAGNOSTIC
echo ========================================
echo.

set total_score=0
set max_score=7

if %python_ok%==1 set /a total_score+=1
if %git_ok%==1 set /a total_score+=1
if %venv_ok%==1 set /a total_score+=1
if %main_ok%==1 set /a total_score+=1
if %req_ok%==1 set /a total_score+=1
if %git_status_ok%==1 set /a total_score+=1
if %app_ok%==1 set /a total_score+=1

echo Score: %total_score%/%max_score%
echo.

if %total_score%==%max_score% (
    echo 🎉 EXCELLENT: Tout est prêt pour la mise à jour!
    echo.
    echo Actions recommandées:
    echo   • Exécuter update.bat pour mettre à jour
    echo   • Ou utiliser git pull manuellement
) else if %total_score% GEQ 5 (
    echo ✅ BON: Mise à jour possible avec quelques précautions
    echo.
    echo Actions recommandées:
    if %git_ok%==0 echo   • Installer Git
    if %venv_ok%==0 echo   • Exécuter install.bat pour créer l'environnement virtuel
    if %deps_ok%==0 echo   • Mettre à jour les dépendances: pip install -r requirements.txt
    echo   • Puis exécuter update.bat
) else (
    echo ⚠️  ATTENTION: Problèmes détectés
    echo.
    echo Actions requises:
    if %python_ok%==0 echo   • Installer Python
    if %git_ok%==0 echo   • Installer Git
    if %main_ok%==0 echo   • Vérifier que vous êtes dans le bon répertoire
    if %venv_ok%==0 echo   • Exécuter install.bat
    echo   • Résoudre les problèmes avant de mettre à jour
)

echo.
echo ========================================
echo   🛠️  ACTIONS DISPONIBLES
echo ========================================
echo.
echo 1. Exécuter install.bat (installation/réparation)
echo 2. Exécuter update.bat (mise à jour)
echo 3. Exécuter backup.bat (sauvegarde)
echo 4. Ouvrir le guide de mise à jour
echo 5. Quitter
echo.

set /p action=Choisissez une action (1-5): 

if "%action%"=="1" (
    echo 🔧 Lancement de install.bat...
    call install.bat
) else if "%action%"=="2" (
    echo 🔄 Lancement de update.bat...
    call update.bat
) else if "%action%"=="3" (
    echo 💾 Lancement de backup.bat...
    call backup.bat
) else if "%action%"=="4" (
    echo 📖 Ouverture du guide...
    start "" notepad GUIDE_UPDATE_WINDOWS11.md
) else (
    echo Au revoir!
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
