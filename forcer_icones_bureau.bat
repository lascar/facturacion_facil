@echo off
chcp 65001 >nul
title FORCER Création Icônes Bureau - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔧 FORCER ICÔNES SUR BUREAU                  ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Vérifier qu'on est dans le bon dossier
if not exist "main.py" (
    echo ❌ ERREUR: Ce script doit être exécuté depuis le dossier de l'application
    pause
    exit /b 1
)

:: Chemins multiples pour le bureau
set "BUREAU1=%USERPROFILE%\Desktop"
set "BUREAU2=%USERPROFILE%\Escritorio"
set "BUREAU3=%PUBLIC%\Desktop"
set "BUREAU4=%HOMEDRIVE%%HOMEPATH%\Desktop"

echo 🔍 Détection du bureau utilisateur...
echo.

:: Trouver le bon chemin du bureau
set "BUREAU_FINAL="

if exist "%BUREAU1%" (
    set "BUREAU_FINAL=%BUREAU1%"
    echo ✅ Bureau trouvé: %BUREAU1%
) else if exist "%BUREAU2%" (
    set "BUREAU_FINAL=%BUREAU2%"
    echo ✅ Bureau trouvé: %BUREAU2%
) else if exist "%BUREAU3%" (
    set "BUREAU_FINAL=%BUREAU3%"
    echo ✅ Bureau trouvé: %BUREAU3%
) else if exist "%BUREAU4%" (
    set "BUREAU_FINAL=%BUREAU4%"
    echo ✅ Bureau trouvé: %BUREAU4%
) else (
    echo ❌ ERREUR: Impossible de trouver le bureau
    echo.
    echo 💡 Chemins testés:
    echo    - %BUREAU1%
    echo    - %BUREAU2%
    echo    - %BUREAU3%
    echo    - %BUREAU4%
    pause
    exit /b 1
)

set "DOSSIER_APP=%CD%"
echo 📁 Dossier application: %DOSSIER_APP%
echo.

echo 🔧 Création FORCÉE des scripts et icônes...
echo.

:: Créer le script de lancement SIMPLE
echo 📝 Création du script de lancement...
(
    echo @echo off
    echo title Facturación Fácil
    echo cd /d "%DOSSIER_APP%"
    echo.
    echo :: Détecter Python
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo.
    echo :: Environnement virtuel
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo.
    echo :: Lancer
    echo echo 🚀 Lancement de Facturación Fácil...
    echo %%PYTHON%% main.py
    echo if errorlevel 1 pause
) > "LANCER_APP.bat"

:: Créer le script de mise à jour SIMPLE
echo 📝 Création du script de mise à jour...
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Mise à Jour Facturación Fácil
    echo cd /d "%DOSSIER_APP%"
    echo.
    echo echo 🔄 MISE À JOUR FACTURACIÓN FÁCIL
    echo echo.
    echo echo 📡 Vérification des mises à jour...
    echo git fetch origin ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Erreur Git ou pas de connexion
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 💾 Sauvegarde...
    echo if not exist "backup" mkdir backup
    echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul
    echo.
    echo echo 📥 Téléchargement...
    echo git pull origin main
    echo.
    echo echo ✅ Mise à jour terminée!
    echo timeout /t 3 /nobreak ^>nul
) > "METTRE_A_JOUR.bat"

echo ✅ Scripts créés
echo.

:: MÉTHODE 1: Copier directement les fichiers .bat sur le bureau
echo 🖥️  MÉTHODE 1: Copie directe des fichiers .bat...

copy "LANCER_APP.bat" "%BUREAU_FINAL%\🚀 LANCER FACTURACION FACIL.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Fichier de lancement copié sur le bureau
) else (
    echo ❌ Échec copie fichier de lancement
)

copy "METTRE_A_JOUR.bat" "%BUREAU_FINAL%\🔄 METTRE A JOUR FACTURACION FACIL.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Fichier de mise à jour copié sur le bureau
) else (
    echo ❌ Échec copie fichier de mise à jour
)

echo.

:: MÉTHODE 2: Créer des raccourcis .lnk avec PowerShell
echo 🔗 MÉTHODE 2: Création de raccourcis .lnk...

:: Raccourci de lancement
powershell -ExecutionPolicy Bypass -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%BUREAU_FINAL%\LANCER Facturacion Facil.lnk'); $s.TargetPath = '%DOSSIER_APP%\LANCER_APP.bat'; $s.WorkingDirectory = '%DOSSIER_APP%'; $s.Description = 'Lancer Facturacion Facil'; $s.Save(); Write-Host 'OK' } catch { Write-Host 'ERREUR' }" 2>nul

if exist "%BUREAU_FINAL%\LANCER Facturacion Facil.lnk" (
    echo ✅ Raccourci de lancement créé
) else (
    echo ❌ Échec création raccourci de lancement
)

:: Raccourci de mise à jour
powershell -ExecutionPolicy Bypass -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%BUREAU_FINAL%\METTRE A JOUR Facturacion Facil.lnk'); $s.TargetPath = '%DOSSIER_APP%\METTRE_A_JOUR.bat'; $s.WorkingDirectory = '%DOSSIER_APP%'; $s.Description = 'Mettre a jour Facturacion Facil'; $s.Save(); Write-Host 'OK' } catch { Write-Host 'ERREUR' }" 2>nul

if exist "%BUREAU_FINAL%\METTRE A JOUR Facturacion Facil.lnk" (
    echo ✅ Raccourci de mise à jour créé
) else (
    echo ❌ Échec création raccourci de mise à jour
)

echo.

:: MÉTHODE 3: Créer avec VBScript
echo 📜 MÉTHODE 3: Création avec VBScript...

:: Script VBScript pour le lancement
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%BUREAU_FINAL%\Facturacion Facil LANCER.lnk"^)
    echo oShellLink.TargetPath = "%DOSSIER_APP%\LANCER_APP.bat"
    echo oShellLink.WorkingDirectory = "%DOSSIER_APP%"
    echo oShellLink.Description = "Lancer Facturacion Facil"
    echo oShellLink.Save
) > temp_lancer.vbs

cscript //nologo temp_lancer.vbs >nul 2>&1
if exist "%BUREAU_FINAL%\Facturacion Facil LANCER.lnk" (
    echo ✅ Raccourci VBScript de lancement créé
) else (
    echo ❌ Échec raccourci VBScript de lancement
)

:: Script VBScript pour la mise à jour
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%BUREAU_FINAL%\Facturacion Facil MISE A JOUR.lnk"^)
    echo oShellLink.TargetPath = "%DOSSIER_APP%\METTRE_A_JOUR.bat"
    echo oShellLink.WorkingDirectory = "%DOSSIER_APP%"
    echo oShellLink.Description = "Mettre a jour Facturacion Facil"
    echo oShellLink.Save
) > temp_update.vbs

cscript //nologo temp_update.vbs >nul 2>&1
if exist "%BUREAU_FINAL%\Facturacion Facil MISE A JOUR.lnk" (
    echo ✅ Raccourci VBScript de mise à jour créé
) else (
    echo ❌ Échec raccourci VBScript de mise à jour
)

:: Nettoyer les fichiers temporaires
del temp_lancer.vbs >nul 2>&1
del temp_update.vbs >nul 2>&1

echo.

:: VÉRIFICATION FINALE
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VÉRIFICATION FINALE                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Fichiers créés sur le bureau (%BUREAU_FINAL%):
echo.

set TOTAL_ICONES=0

:: Vérifier tous les fichiers possibles
if exist "%BUREAU_FINAL%\🚀 LANCER FACTURACION FACIL.bat" (
    echo ✅ 🚀 LANCER FACTURACION FACIL.bat
    set /a TOTAL_ICONES+=1
)

if exist "%BUREAU_FINAL%\🔄 METTRE A JOUR FACTURACION FACIL.bat" (
    echo ✅ 🔄 METTRE A JOUR FACTURACION FACIL.bat
    set /a TOTAL_ICONES+=1
)

if exist "%BUREAU_FINAL%\LANCER Facturacion Facil.lnk" (
    echo ✅ LANCER Facturacion Facil.lnk
    set /a TOTAL_ICONES+=1
)

if exist "%BUREAU_FINAL%\METTRE A JOUR Facturacion Facil.lnk" (
    echo ✅ METTRE A JOUR Facturacion Facil.lnk
    set /a TOTAL_ICONES+=1
)

if exist "%BUREAU_FINAL%\Facturacion Facil LANCER.lnk" (
    echo ✅ Facturacion Facil LANCER.lnk
    set /a TOTAL_ICONES+=1
)

if exist "%BUREAU_FINAL%\Facturacion Facil MISE A JOUR.lnk" (
    echo ✅ Facturacion Facil MISE A JOUR.lnk
    set /a TOTAL_ICONES+=1
)

echo.

if %TOTAL_ICONES% GTR 0 (
    echo 🎉 SUCCÈS! %TOTAL_ICONES% icône(s) créée(s) sur le bureau!
    echo.
    echo 💡 INSTRUCTIONS POUR L'UTILISATEUR:
    echo    1. Regardez sur votre bureau (escritorio)
    echo    2. Vous devriez voir des fichiers pour Facturacion Facil
    echo    3. Double-cliquez sur n'importe lequel pour utiliser l'app
    echo.
    echo 🎯 MISSION ACCOMPLIE!
) else (
    echo ❌ ÉCHEC: Aucune icône créée sur le bureau
    echo.
    echo 🚨 DIAGNOSTIC:
    echo    • Bureau détecté: %BUREAU_FINAL%
    echo    • Permissions: Vérifiez les droits d'écriture
    echo    • Antivirus: Peut bloquer la création de fichiers
    echo    • UAC: Essayez d'exécuter en tant qu'administrateur
)

echo.
echo 🖥️  Voulez-vous ouvrir le bureau pour voir les icônes? (O/N)
set /p ouvrir=
if /i "%ouvrir%"=="O" if /i "%ouvrir%"=="o" (
    explorer "%BUREAU_FINAL%"
)

echo.
pause
