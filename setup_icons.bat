@echo off
chcp 65001 >nul
title Configuration des Icônes - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎯 FACTURACIÓN FÁCIL                     ║
echo ║                Configuration des Icônes Bureau              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Vérifier si on est dans le bon répertoire
if not exist "main.py" (
    echo ❌ ERREUR: Vous devez exécuter ce script depuis le dossier de l'application
    echo.
    echo 💡 Instructions:
    echo    1. Ouvrez le dossier de l'application
    echo    2. Double-cliquez sur setup_icons.bat
    echo.
    pause
    exit /b 1
)

echo 🔍 Vérification de l'environnement...
echo.

:: Obtenir le chemin complet
set "APP_DIR=%CD%"
set "DESKTOP=%USERPROFILE%\Desktop"

echo ✅ Application trouvée dans: %APP_DIR%
echo ✅ Bureau utilisateur: %DESKTOP%
echo.

echo 🎨 Que voulez-vous créer?
echo.
echo   1. 🚀 Icône de lancement uniquement
echo   2. 🔄 Icône de mise à jour uniquement  
echo   3. 🎯 Les deux icônes (recommandé)
echo   4. ❌ Annuler
echo.
set /p choice="Votre choix (1-4): "

if "%choice%"=="4" (
    echo Opération annulée
    timeout /t 2 /nobreak >nul
    exit /b 0
)

if "%choice%"=="1" set CREATE_LAUNCH=1
if "%choice%"=="2" set CREATE_UPDATE=1
if "%choice%"=="3" (
    set CREATE_LAUNCH=1
    set CREATE_UPDATE=1
)

if not defined CREATE_LAUNCH if not defined CREATE_UPDATE (
    echo ❌ Choix invalide
    pause
    exit /b 1
)

echo.
echo 🔧 Création des scripts...

:: Script de lancement (toujours créé pour les raccourcis)
(
    echo @echo off
    echo title Facturación Fácil
    echo cd /d "%APP_DIR%"
    echo.
    echo :: Détection automatique de Python
    echo set PYTHON_CMD=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON_CMD=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON_CMD=python3
    echo.
    echo :: Gestion de l'environnement virtuel
    echo if exist "venv\Scripts\activate.bat" ^(
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else if exist "env\Scripts\activate.bat" ^(
    echo     call env\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else ^(
    echo     echo 🔧 Initialisation...
    echo     %%PYTHON_CMD%% -m venv venv ^>nul 2^>^&1
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo     pip install -r requirements.txt ^>nul 2^>^&1
    echo ^)
    echo.
    echo :: Lancement de l'application
    echo %%PYTHON_CMD%% main.py
    echo.
    echo :: Gestion des erreurs
    echo if errorlevel 1 ^(
    echo     echo.
    echo     echo ❌ Erreur lors du lancement
    echo     echo 📋 Vérifiez les logs dans le dossier 'logs/'
    echo     pause
    echo ^)
) > "🚀_Lancer_App.bat"

:: Script de mise à jour (si demandé)
if defined CREATE_UPDATE (
    (
        echo @echo off
        echo chcp 65001 ^>nul
        echo title Mise à Jour - Facturación Fácil
        echo cd /d "%APP_DIR%"
        echo.
        echo echo ╔══════════════════════════════════════════════════════════════╗
        echo echo ║                    🔄 MISE À JOUR                           ║
        echo echo ║                  Facturación Fácil                          ║
        echo echo ╚══════════════════════════════════════════════════════════════╝
        echo echo.
        echo.
        echo :: Vérifier Git
        echo git --version ^>nul 2^>^&1
        echo if errorlevel 1 ^(
        echo     echo ❌ Git non installé
        echo     echo.
        echo     echo 💡 Télécharger Git: https://git-scm.com/download/win
        echo     echo    Puis relancer cette mise à jour
        echo     pause
        echo     exit /b 1
        echo ^)
        echo.
        echo echo 📡 Recherche de mises à jour...
        echo git fetch origin ^>nul 2^>^&1
        echo.
        echo for /f %%%%i in ^('git rev-list HEAD..origin/main --count'^) do set UPDATES=%%%%i
        echo if "%%UPDATES%%"=="0" ^(
        echo     echo ✅ Votre application est déjà à jour!
        echo     timeout /t 3 /nobreak ^>nul
        echo     exit /b 0
        echo ^)
        echo.
        echo echo 🎯 %%UPDATES%% mise^(s^) à jour trouvée^(s^)
        echo echo.
        echo echo 💾 Sauvegarde automatique en cours...
        echo if not exist "backup" mkdir backup ^>nul 2^>^&1
        echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul 2^>^&1
        echo if exist "config.json" copy "config.json" "backup\" ^>nul 2^>^&1
        echo echo ✅ Données sauvegardées
        echo.
        echo echo 📥 Téléchargement des mises à jour...
        echo git pull origin main
        echo if errorlevel 1 ^(
        echo     echo ❌ Erreur lors du téléchargement
        echo     pause
        echo     exit /b 1
        echo ^)
        echo.
        echo echo 📦 Mise à jour des composants...
        echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
        echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
        echo pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
        echo.
        echo echo ╔══════════════════════════════════════════════════════════════╗
        echo echo ║                    ✅ MISE À JOUR TERMINÉE                  ║
        echo echo ╚══════════════════════════════════════════════════════════════╝
        echo echo.
        echo echo 🎉 Votre application a été mise à jour avec succès!
        echo echo 🚀 Vous pouvez maintenant la relancer
        echo echo.
        echo timeout /t 5 /nobreak ^>nul
    ) > "🔄_Mettre_à_Jour.bat"
)

echo ✅ Scripts créés
echo.

:: Créer les raccourcis sur le bureau
echo 🔗 Création des raccourcis sur le bureau...

if defined CREATE_LAUNCH (
    powershell -Command "
    try {
        $WshShell = New-Object -comObject WScript.Shell;
        $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🚀 Facturación Fácil.lnk');
        $Shortcut.TargetPath = '%APP_DIR%\🚀_Lancer_App.bat';
        $Shortcut.WorkingDirectory = '%APP_DIR%';
        $Shortcut.Description = 'Lancer Facturación Fácil';
        if (Test-Path '%APP_DIR%\assets\icon.ico') {
            $Shortcut.IconLocation = '%APP_DIR%\assets\icon.ico,0';
        }
        $Shortcut.Save();
        Write-Host '   ✅ Icône de lancement créée' -ForegroundColor Green;
    } catch {
        Write-Host '   ❌ Erreur création icône lancement' -ForegroundColor Red;
    }"
)

if defined CREATE_UPDATE (
    powershell -Command "
    try {
        $WshShell = New-Object -comObject WScript.Shell;
        $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🔄 Mise à Jour Facturación Fácil.lnk');
        $Shortcut.TargetPath = '%APP_DIR%\🔄_Mettre_à_Jour.bat';
        $Shortcut.WorkingDirectory = '%APP_DIR%';
        $Shortcut.Description = 'Mettre à jour Facturación Fácil depuis GitHub';
        $Shortcut.Save();
        Write-Host '   ✅ Icône de mise à jour créée' -ForegroundColor Green;
    } catch {
        Write-Host '   ❌ Erreur création icône mise à jour' -ForegroundColor Red;
    }"
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 CONFIGURATION TERMINÉE                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

if defined CREATE_LAUNCH (
    echo 🚀 Icône "Facturación Fácil" créée sur le bureau
    echo    → Double-clic pour lancer l'application
)

if defined CREATE_UPDATE (
    echo 🔄 Icône "Mise à Jour Facturación Fácil" créée sur le bureau  
    echo    → Double-clic pour mettre à jour depuis GitHub
)

echo.
echo 💡 UTILISATION POUR L'UTILISATEUR FINAL:
echo    • Double-clic sur l'icône = lancement automatique
echo    • Aucune connaissance technique requise
echo    • Gestion automatique de l'environnement Python
echo.
echo 🎯 Mission accomplie! L'utilisateur peut maintenant utiliser
echo    l'application en cliquant simplement sur les icônes!
echo.

pause
