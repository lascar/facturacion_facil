@echo off
chcp 65001 >nul
title Création des Raccourcis Bureau - Facturación Fácil

echo ========================================
echo   🎯 CRÉATION DES RACCOURCIS BUREAU
echo ========================================
echo.

:: Vérifier si on est dans le bon répertoire
if not exist "main.py" (
    echo ❌ ERREUR: Fichier main.py non trouvé
    echo Assurez-vous d'être dans le répertoire de l'application
    pause
    exit /b 1
)

:: Obtenir le chemin complet du répertoire actuel
set "APP_DIR=%CD%"
set "DESKTOP=%USERPROFILE%\Desktop"

echo 📁 Répertoire de l'application: %APP_DIR%
echo 🖥️  Bureau: %DESKTOP%
echo.

:: Créer le script de lancement optimisé
echo 🚀 Création du script de lancement...
(
    echo @echo off
    echo title Facturación Fácil
    echo cd /d "%APP_DIR%"
    echo.
    echo :: Démarrage silencieux
    echo set PYTHON_CMD=
    echo python --version ^>nul 2^>^&1
    echo if not errorlevel 1 ^(
    echo     set PYTHON_CMD=python
    echo ^) else ^(
    echo     py --version ^>nul 2^>^&1
    echo     if not errorlevel 1 ^(
    echo         set PYTHON_CMD=py
    echo     ^) else ^(
    echo         set PYTHON_CMD=python3
    echo     ^)
    echo ^)
    echo.
    echo :: Activer l'environnement virtuel
    echo if exist "venv\Scripts\activate.bat" ^(
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else if exist "env\Scripts\activate.bat" ^(
    echo     call env\Scripts\activate.bat ^>nul 2^>^&1
    echo ^) else ^(
    echo     echo Création de l'environnement virtuel...
    echo     %%PYTHON_CMD%% -m venv venv ^>nul 2^>^&1
    echo     call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo     pip install -r requirements.txt ^>nul 2^>^&1
    echo ^)
    echo.
    echo :: Lancer l'application
    echo %%PYTHON_CMD%% main.py
    echo.
    echo :: Pause seulement en cas d'erreur
    echo if errorlevel 1 ^(
    echo     echo.
    echo     echo ❌ Erreur lors du lancement
    echo     pause
    echo ^)
) > "launch_app.bat"

:: Créer le script de mise à jour optimisé
echo 🔄 Création du script de mise à jour...
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Mise à Jour - Facturación Fácil
    echo cd /d "%APP_DIR%"
    echo.
    echo echo ========================================
    echo echo   🔄 MISE À JOUR FACTURACIÓN FÁCIL
    echo echo ========================================
    echo echo.
    echo.
    echo :: Vérifier Git
    echo git --version ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Git non installé
    echo     echo.
    echo     echo 💡 Installer Git depuis: https://git-scm.com/download/win
    echo     echo Puis relancer cette mise à jour
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 📡 Vérification des mises à jour disponibles...
    echo git fetch origin ^>nul 2^>^&1
    echo.
    echo :: Comparer les versions
    echo for /f %%%%i in ^('git rev-list HEAD..origin/main --count'^) do set UPDATE_COUNT=%%%%i
    echo if "%%UPDATE_COUNT%%"=="0" ^(
    echo     echo ✅ Application déjà à jour!
    echo     echo.
    echo     timeout /t 3 /nobreak ^>nul
    echo     exit /b 0
    echo ^)
    echo.
    echo echo 🎯 %%UPDATE_COUNT%% mise^(s^) à jour disponible^(s^)
    echo echo.
    echo echo Voulez-vous continuer? ^(O/N^)
    echo set /p choice=
    echo if /i not "%%choice%%"=="O" if /i not "%%choice%%"=="o" ^(
    echo     echo Mise à jour annulée
    echo     timeout /t 2 /nobreak ^>nul
    echo     exit /b 0
    echo ^)
    echo.
    echo echo 💾 Sauvegarde des données...
    echo if not exist "backup" mkdir backup
    echo if exist "facturacion.db" copy "facturacion.db" "backup\facturacion_%%date:~-4,4%%%%date:~-10,2%%%%date:~-7,2%%.db" ^>nul
    echo if exist "config.json" copy "config.json" "backup\config_%%date:~-4,4%%%%date:~-10,2%%%%date:~-7,2%%.json" ^>nul
    echo echo ✅ Sauvegarde terminée
    echo.
    echo echo 📥 Téléchargement des mises à jour...
    echo git pull origin main
    echo if errorlevel 1 ^(
    echo     echo ❌ Erreur lors de la mise à jour
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 📦 Mise à jour des dépendances...
    echo if exist "venv\Scripts\activate.bat" ^(
    echo     call venv\Scripts\activate.bat
    echo ^) else if exist "env\Scripts\activate.bat" ^(
    echo     call env\Scripts\activate.bat
    echo ^)
    echo pip install -r requirements.txt --upgrade --quiet
    echo.
    echo echo ========================================
    echo echo   ✅ MISE À JOUR TERMINÉE!
    echo echo ========================================
    echo echo.
    echo echo L'application a été mise à jour avec succès
    echo echo Vous pouvez maintenant la relancer
    echo echo.
    echo timeout /t 5 /nobreak ^>nul
) > "update_app.bat"

echo ✅ Scripts créés avec succès
echo.

:: Créer les raccourcis avec PowerShell
echo 🔗 Création des raccourcis sur le bureau...

:: Raccourci pour lancer l'application
powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🚀 Facturación Fácil.lnk');
$Shortcut.TargetPath = '%APP_DIR%\launch_app.bat';
$Shortcut.WorkingDirectory = '%APP_DIR%';
$Shortcut.Description = 'Lancer Facturación Fácil';
$Shortcut.IconLocation = '%APP_DIR%\assets\icon.ico,0';
$Shortcut.Save()
"

if errorlevel 1 (
    echo ⚠️  Impossible de créer le raccourci avec icône, création simple...
    powershell -Command "
    $WshShell = New-Object -comObject WScript.Shell;
    $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Facturación Fácil.lnk');
    $Shortcut.TargetPath = '%APP_DIR%\launch_app.bat';
    $Shortcut.WorkingDirectory = '%APP_DIR%';
    $Shortcut.Description = 'Lancer Facturación Fácil';
    $Shortcut.Save()
    "
)

:: Raccourci pour la mise à jour
powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🔄 Mise à Jour Facturación Fácil.lnk');
$Shortcut.TargetPath = '%APP_DIR%\update_app.bat';
$Shortcut.WorkingDirectory = '%APP_DIR%';
$Shortcut.Description = 'Mettre à jour Facturación Fácil depuis GitHub';
$Shortcut.Save()
"

echo.
echo ========================================
echo   🎉 RACCOURCIS CRÉÉS AVEC SUCCÈS!
echo ========================================
echo.
echo 📋 Raccourcis créés sur le bureau:
echo.
echo   🚀 Facturación Fácil
echo      → Lance l'application directement
echo      → Gère automatiquement l'environnement virtuel
echo      → Installe les dépendances si nécessaire
echo.
echo   🔄 Mise à Jour Facturación Fácil  
echo      → Met à jour depuis GitHub
echo      → Sauvegarde automatique des données
echo      → Mise à jour des dépendances
echo.
echo 💡 Utilisation:
echo   • Double-clic sur l'icône pour lancer
echo   • Double-clic sur l'icône de mise à jour pour mettre à jour
echo   • Aucune connaissance technique requise!
echo.
echo 🎯 L'utilisateur final n'a plus qu'à cliquer sur les icônes!
echo.

pause
