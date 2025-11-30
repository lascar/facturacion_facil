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

:: Script de lancement simple et robuste
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
    echo if exist "venv\Scripts\activate.bat" ^(
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else if exist "env\Scripts\activate.bat" ^(
    echo     call env\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else ^(
    echo     echo 🔧 Préparation de l'environnement...
    echo     %%PYTHON%% -m venv venv ^>nul 2^>^&1
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo     pip install -r requirements.txt ^>nul 2^>^&1
    echo ^)
    echo.
    echo :: Lancer l'application
    echo %%PYTHON%% main.py
    echo.
    echo :: En cas d'erreur
    echo if errorlevel 1 ^(
    echo     echo.
    echo     echo ❌ Erreur de lancement
    echo     echo 📋 Consultez les logs dans le dossier 'logs/'
    echo     pause
    echo ^)
) > "Lancer_Application.bat"

:: Script de mise à jour simple et robuste
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Mise à Jour - Facturación Fácil
    echo cd /d "%DOSSIER_APP%"
    echo.
    echo echo ╔══════════════════════════════════════════════════════════════╗
    echo echo ║                    🔄 MISE À JOUR                           ║
    echo echo ╚══════════════════════════════════════════════════════════════╝
    echo echo.
    echo.
    echo :: Vérifier Git
    echo git --version ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Git non installé
    echo     echo.
    echo     echo 💡 Télécharger: https://git-scm.com/download/win
    echo     echo    Puis relancer cette mise à jour
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 📡 Recherche de nouvelles versions...
    echo git fetch origin ^>nul 2^>^&1
    echo.
    echo for /f %%%%i in ^('git rev-list HEAD..origin/main --count'^) do set NOUVELLES=%%%%i
    echo if "%%NOUVELLES%%"=="0" ^(
    echo     echo ✅ Vous avez déjà la dernière version!
    echo     timeout /t 3 /nobreak ^>nul
    echo     exit /b 0
    echo ^)
    echo.
    echo echo 🎯 %%NOUVELLES%% nouvelle^(s^) version^(s^) disponible^(s^)
    echo echo.
    echo echo 💾 Sauvegarde de vos données...
    echo if not exist "backup" mkdir backup ^>nul 2^>^&1
    echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul 2^>^&1
    echo if exist "config.json" copy "config.json" "backup\" ^>nul 2^>^&1
    echo echo ✅ Données sauvegardées
    echo.
    echo echo 📥 Téléchargement de la mise à jour...
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
    echo echo 🎉 Application mise à jour avec succès!
    echo echo 🚀 Vous pouvez maintenant la relancer
    echo echo.
    echo timeout /t 5 /nobreak ^>nul
) > "Mettre_a_Jour.bat"

echo ✅ Scripts créés
echo.

:: Créer les icônes sur le bureau
echo 🖥️  Création des icônes sur le bureau...

:: Icône de lancement
echo    🚀 Création de l'icône de lancement...
powershell -Command "
try {
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('%BUREAU%\🚀 Facturación Fácil.lnk')
    $Shortcut.TargetPath = '%DOSSIER_APP%\Lancer_Application.bat'
    $Shortcut.WorkingDirectory = '%DOSSIER_APP%'
    $Shortcut.Description = 'Lancer Facturación Fácil'
    if (Test-Path '%DOSSIER_APP%\assets\icon.ico') {
        $Shortcut.IconLocation = '%DOSSIER_APP%\assets\icon.ico,0'
    }
    $Shortcut.Save()
    Write-Host '       ✅ Icône de lancement créée sur le bureau' -ForegroundColor Green
} catch {
    Write-Host '       ❌ Erreur création icône lancement' -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}"

:: Icône de mise à jour
echo    🔄 Création de l'icône de mise à jour...
powershell -Command "
try {
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('%BUREAU%\🔄 Mise à Jour Facturación Fácil.lnk')
    $Shortcut.TargetPath = '%DOSSIER_APP%\Mettre_a_Jour.bat'
    $Shortcut.WorkingDirectory = '%DOSSIER_APP%'
    $Shortcut.Description = 'Mettre à jour Facturación Fácil depuis GitHub'
    $Shortcut.Save()
    Write-Host '       ✅ Icône de mise à jour créée sur le bureau' -ForegroundColor Green
} catch {
    Write-Host '       ❌ Erreur création icône mise à jour' -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 ICÔNES CRÉÉES!                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🖥️  Regardez sur votre bureau, vous devriez voir:
echo.
echo     🚀 Facturación Fácil
echo        → Double-clic pour lancer l'application
echo.
echo     🔄 Mise à Jour Facturación Fácil
echo        → Double-clic pour mettre à jour depuis GitHub
echo.
echo 💡 UTILISATION:
echo    • Les icônes sont maintenant sur votre BUREAU
echo    • Double-clic sur une icône = action automatique
echo    • Aucune connaissance technique nécessaire
echo.
echo 🎯 Mission accomplie! L'utilisateur peut maintenant utiliser
echo    l'application en cliquant sur les icônes du bureau!
echo.

pause
