@echo off
chcp 65001 >nul
title Diagnostic Environnement - Windows 11

echo ========================================
echo   🔍 DIAGNOSTIC ENVIRONNEMENT WINDOWS 11
echo ========================================
echo.

:: Informations système
echo 💻 Informations système:
echo   OS: %OS%
echo   Architecture: %PROCESSOR_ARCHITECTURE%
echo   Utilisateur: %USERNAME%
echo   Répertoire: %CD%
echo.

:: Vérification Python
echo 🐍 Diagnostic Python:
echo.

:: Test python
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'python' non disponible
    set PYTHON_AVAILABLE=0
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   ✅ python: %%i
    set PYTHON_AVAILABLE=1
    set PYTHON_CMD=python
)

:: Test py
py --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'py' non disponible
    set PY_AVAILABLE=0
) else (
    for /f "tokens=*" %%i in ('py --version 2^>^&1') do echo   ✅ py: %%i
    set PY_AVAILABLE=1
    if %PYTHON_AVAILABLE%==0 set PYTHON_CMD=py
)

:: Test python3
python3 --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'python3' non disponible
    set PYTHON3_AVAILABLE=0
) else (
    for /f "tokens=*" %%i in ('python3 --version 2^>^&1') do echo   ✅ python3: %%i
    set PYTHON3_AVAILABLE=1
    if %PYTHON_AVAILABLE%==0 if %PY_AVAILABLE%==0 set PYTHON_CMD=python3
)

echo.

:: Résumé Python
if %PYTHON_AVAILABLE%==0 if %PY_AVAILABLE%==0 if %PYTHON3_AVAILABLE%==0 (
    echo ❌ PROBLÈME: Aucune version de Python trouvée
    echo.
    echo 💡 Solutions:
    echo   1. Installer Python depuis https://python.org
    echo   2. Cocher "Add Python to PATH" pendant l'installation
    echo   3. Redémarrer l'ordinateur
    echo   4. Ou installer depuis Microsoft Store
    echo.
    goto :end_diagnostic
) else (
    echo ✅ Python disponible, commande recommandée: %PYTHON_CMD%
)

echo.

:: Vérification des environnements virtuels
echo 🔧 Diagnostic environnements virtuels:
echo.

set ENV_COUNT=0

if exist "env" (
    echo   📁 Dossier 'env' trouvé
    if exist "env\Scripts" (
        echo     📁 Sous-dossier 'Scripts' trouvé
        if exist "env\Scripts\activate.bat" (
            echo     ✅ env\Scripts\activate.bat existe
            set ENV_COUNT=1
            set ENV1_PATH=env
        ) else (
            echo     ❌ env\Scripts\activate.bat manquant
        )
        if exist "env\Scripts\python.exe" (
            echo     ✅ env\Scripts\python.exe existe
        ) else (
            echo     ❌ env\Scripts\python.exe manquant
        )
    ) else (
        echo     ❌ Sous-dossier 'Scripts' manquant
    )
) else (
    echo   ❌ Dossier 'env' non trouvé
)

if exist "venv" (
    echo   📁 Dossier 'venv' trouvé
    if exist "venv\Scripts\activate.bat" (
        echo     ✅ venv\Scripts\activate.bat existe
        set /a ENV_COUNT+=1
        set ENV2_PATH=venv
    )
)

if exist ".venv" (
    echo   📁 Dossier '.venv' trouvé
    if exist ".venv\Scripts\activate.bat" (
        echo     ✅ .venv\Scripts\activate.bat existe
        set /a ENV_COUNT+=1
        set ENV3_PATH=.venv
    )
)

echo.
echo   📊 Résumé: %ENV_COUNT% environnement(s) virtuel(s) trouvé(s)

if %ENV_COUNT%==0 (
    echo.
    echo ❌ PROBLÈME: Aucun environnement virtuel trouvé
    echo.
    echo 💡 Solutions:
    echo   1. Exécuter: %PYTHON_CMD% -m venv env
    echo   2. Ou utiliser fix_env_activate.bat
    echo   3. Ou réinstaller avec install.bat
    echo.
) else (
    echo.
    echo ✅ Environnement(s) disponible(s):
    if defined ENV1_PATH echo     • %ENV1_PATH%
    if defined ENV2_PATH echo     • %ENV2_PATH%
    if defined ENV3_PATH echo     • %ENV3_PATH%
)

echo.

:: Test d'activation si environnement trouvé
if %ENV_COUNT% GTR 0 (
    echo 🧪 Test d'activation:
    echo.
    
    if defined ENV1_PATH (
        echo   Test de %ENV1_PATH%\Scripts\activate.bat...
        call %ENV1_PATH%\Scripts\activate.bat >nul 2>&1
        if errorlevel 1 (
            echo     ❌ Échec d'activation
        ) else (
            echo     ✅ Activation réussie
            call deactivate >nul 2>&1
        )
    )
)

echo.

:: Vérification des fichiers de l'application
echo 📁 Diagnostic fichiers application:
echo.

if exist "main.py" (
    echo   ✅ main.py trouvé
) else (
    echo   ❌ main.py manquant
)

if exist "requirements.txt" (
    echo   ✅ requirements.txt trouvé
    echo     Contenu:
    for /f "tokens=*" %%i in (requirements.txt) do echo       %%i
) else (
    echo   ❌ requirements.txt manquant
)

if exist "install.bat" (
    echo   ✅ install.bat trouvé
) else (
    echo   ❌ install.bat manquant
)

if exist "start.bat" (
    echo   ✅ start.bat trouvé
) else (
    echo   ❌ start.bat manquant
)

echo.

:: Diagnostic des erreurs courantes
echo 🚨 Diagnostic erreurs courantes:
echo.

:: Vérifier les permissions
echo   🔒 Permissions:
icacls . >nul 2>&1
if errorlevel 1 (
    echo     ⚠️  Impossible de vérifier les permissions
) else (
    echo     ✅ Permissions OK
)

:: Vérifier l'antivirus (approximatif)
echo   🛡️  Antivirus:
tasklist /FI "IMAGENAME eq MsMpEng.exe" >nul 2>&1
if not errorlevel 1 (
    echo     ⚠️  Windows Defender actif (peut bloquer les scripts)
) else (
    echo     ℹ️  Windows Defender non détecté en cours
)

:: Vérifier l'espace disque
echo   💾 Espace disque:
for /f "tokens=3" %%i in ('dir /-c ^| find "bytes free"') do (
    echo     ℹ️  Espace libre: %%i bytes
)

echo.

:end_diagnostic
echo ========================================
echo   📋 RÉSUMÉ ET RECOMMANDATIONS
echo ========================================
echo.

if %PYTHON_AVAILABLE%==0 if %PY_AVAILABLE%==0 if %PYTHON3_AVAILABLE%==0 (
    echo 🚨 CRITIQUE: Python non installé
    echo.
    echo 🎯 Actions requises:
    echo   1. Installer Python depuis https://python.org
    echo   2. Cocher "Add Python to PATH"
    echo   3. Redémarrer l'ordinateur
    echo   4. Relancer ce diagnostic
    echo.
) else if %ENV_COUNT%==0 (
    echo ⚠️  ATTENTION: Environnement virtuel manquant
    echo.
    echo 🎯 Actions recommandées:
    echo   1. Exécuter fix_env_activate.bat
    echo   2. Ou créer manuellement: %PYTHON_CMD% -m venv env
    echo   3. Puis installer les dépendances
    echo.
) else (
    echo ✅ ÉTAT: Configuration de base OK
    echo.
    echo 🎯 Actions suggérées:
    echo   1. Tester l'activation: env\Scripts\activate.bat
    echo   2. Si problème: exécuter fix_env_activate.bat
    echo   3. Lancer l'application: start.bat
    echo.
)

echo 🛠️  Scripts utiles:
echo   • fix_env_activate.bat - Répare l'environnement virtuel
echo   • install.bat - Installation complète
echo   • diagnostic_update.bat - Diagnostic mise à jour
echo.

echo Appuyez sur une touche pour fermer...
pause >nul
