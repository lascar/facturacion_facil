@echo off
chcp 65001 >nul
title Création Icônes Bureau - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🖥️  ICÔNES BUREAU                        ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Vérifier qu'on est dans le bon dossier
if not exist "main.py" (
    echo ❌ ERREUR: Ce script doit être exécuté depuis le dossier de l'application
    echo.
    echo 💡 Instructions:
    echo    1. Ouvrez le dossier contenant main.py
    echo    2. Double-cliquez sur ce fichier
    echo.
    pause
    exit /b 1
)

:: Chemins
set "DOSSIER_APP=%CD%"
set "BUREAU=%USERPROFILE%\Desktop"

echo 📁 Dossier application: %DOSSIER_APP%
echo 🖥️  Bureau utilisateur: %BUREAU%
echo.

echo 🎯 Ce script va créer 2 icônes sur votre bureau:
echo.
echo    🚀 Facturación Fácil
echo       → Pour lancer l'application
echo.
echo    🔄 Mise à Jour
echo       → Pour mettre à jour depuis GitHub
echo.

set /p continuer="Continuer? (O/N): "
if /i not "%continuer%"=="O" if /i not "%continuer%"=="o" (
    echo Opération annulée
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo.
echo 🔧 Création des scripts de lancement...

:: Script de lancement simple
(
    echo @echo off
    echo title Facturación Fácil
    echo cd /d "%DOSSIER_APP%"
    echo.
    echo :: Trouver Python
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo.
    echo :: Activer environnement virtuel
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo.
    echo :: Lancer l'application
    echo %%PYTHON%% main.py
    echo.
    echo :: En cas d'erreur
    echo if errorlevel 1 pause
) > "Lancer_App.bat"

:: Script de mise à jour simple
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Mise à Jour - Facturación Fácil
    echo cd /d "%DOSSIER_APP%"
    echo.
    echo echo 🔄 MISE À JOUR
    echo echo.
    echo echo 📡 Recherche de nouvelles versions...
    echo git fetch origin ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Git non installé ou erreur réseau
    echo     echo 💡 Installer Git: https://git-scm.com/download/win
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 💾 Sauvegarde...
    echo if not exist "backup" mkdir backup ^>nul 2^>^&1
    echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul 2^>^&1
    echo.
    echo echo 📥 Téléchargement...
    echo git pull origin main
    echo.
    echo echo 📦 Mise à jour des composants...
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
    echo.
    echo echo ✅ Mise à jour terminée!
    echo timeout /t 3 /nobreak ^>nul
) > "Mettre_a_Jour.bat"

echo ✅ Scripts créés
echo.

:: Créer les raccourcis avec une méthode native Windows
echo 🖥️  Création des icônes sur le bureau...

:: Méthode 1: Copier les fichiers .bat directement sur le bureau
echo    🚀 Création de l'icône de lancement...
copy "Lancer_App.bat" "%BUREAU%\🚀 Lancer Facturacion Facil.bat" >nul 2>&1
if %errorlevel%==0 (
    echo       ✅ Icône de lancement créée sur le bureau
) else (
    echo       ❌ Erreur création icône lancement
)

echo    🔄 Création de l'icône de mise à jour...
copy "Mettre_a_Jour.bat" "%BUREAU%\🔄 Mettre a Jour Facturacion Facil.bat" >nul 2>&1
if %errorlevel%==0 (
    echo       ✅ Icône de mise à jour créée sur le bureau
) else (
    echo       ❌ Erreur création icône mise à jour
)

:: Méthode alternative: Créer des raccourcis .lnk avec PowerShell simple
echo.
echo    🔗 Création des raccourcis .lnk...

:: Raccourci de lancement
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%BUREAU%\Facturacion Facil.lnk'); $Shortcut.TargetPath = '%DOSSIER_APP%\Lancer_App.bat'; $Shortcut.WorkingDirectory = '%DOSSIER_APP%'; $Shortcut.Description = 'Lancer Facturacion Facil'; $Shortcut.Save()" >nul 2>&1

if exist "%BUREAU%\Facturacion Facil.lnk" (
    echo       ✅ Raccourci de lancement créé
) else (
    echo       ⚠️  Raccourci de lancement non créé (utiliser les fichiers .bat)
)

:: Raccourci de mise à jour
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%BUREAU%\Mise a Jour Facturacion Facil.lnk'); $Shortcut.TargetPath = '%DOSSIER_APP%\Mettre_a_Jour.bat'; $Shortcut.WorkingDirectory = '%DOSSIER_APP%'; $Shortcut.Description = 'Mettre a jour Facturacion Facil'; $Shortcut.Save()" >nul 2>&1

if exist "%BUREAU%\Mise a Jour Facturacion Facil.lnk" (
    echo       ✅ Raccourci de mise à jour créé
) else (
    echo       ⚠️  Raccourci de mise à jour non créé (utiliser les fichiers .bat)
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 ICÔNES CRÉÉES!                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🖥️  Regardez sur votre bureau, vous devriez voir:
echo.
echo     🚀 Lancer Facturacion Facil (.bat ou .lnk)
echo        → Double-clic pour lancer l'application
echo.
echo     🔄 Mettre a Jour Facturacion Facil (.bat ou .lnk)
echo        → Double-clic pour mettre à jour depuis GitHub
echo.
echo 💡 UTILISATION:
echo    • Les icônes sont maintenant sur votre BUREAU
echo    • Double-clic sur une icône = action automatique
echo    • Les fichiers .bat fonctionnent toujours même si les .lnk échouent
echo.
echo 🎯 Mission accomplie! L'utilisateur peut maintenant utiliser
echo    l'application en cliquant sur les icônes du bureau!
echo.

:: Vérifier ce qui a été créé
echo 📋 Vérification des fichiers créés sur le bureau:
echo.
if exist "%BUREAU%\🚀 Lancer Facturacion Facil.bat" echo ✅ 🚀 Lancer Facturacion Facil.bat
if exist "%BUREAU%\🔄 Mettre a Jour Facturacion Facil.bat" echo ✅ 🔄 Mettre a Jour Facturacion Facil.bat
if exist "%BUREAU%\Facturacion Facil.lnk" echo ✅ Facturacion Facil.lnk
if exist "%BUREAU%\Mise a Jour Facturacion Facil.lnk" echo ✅ Mise a Jour Facturacion Facil.lnk

echo.
echo 🎮 PRÊT À UTILISER!
echo    Double-cliquez sur n'importe laquelle de ces icônes pour commencer.
echo.

pause
