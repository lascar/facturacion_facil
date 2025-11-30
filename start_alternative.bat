@echo off
echo ========================================
echo   Lancement Alternative (avec py)
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

REM Detecter la commande Python disponible
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo Utilisation du launcher Python Windows (py)
    goto :check_venv
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo Utilisation de python
    goto :check_venv
)

echo ❌ ERREUR: Python non trouve
echo.
echo SOLUTIONS:
echo 1. Executer diagnostic_python.bat pour diagnostiquer
echo 2. Installer Python depuis python.org
echo 3. Cocher "Add Python to PATH" pendant l'installation
echo.
pause
exit /b 1

:check_venv
REM Verifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouve
    echo.
    echo SOLUTIONS:
    echo 1. Executer install.bat ou install_alternative.bat
    echo 2. Ou creer manuellement: %PYTHON_CMD% -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Verifier les dependances
echo Verification des dependances...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt5 non installe
    echo Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERREUR: Installation echouee
        echo Essayez install_alternative.bat
        pause
        exit /b 1
    )
)

REM Lancer l'application
echo.
echo ✅ Lancement de Facturacion Facil...
echo.
python main.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo ❌ L'application s'est fermee avec une erreur
    echo.
    echo DIAGNOSTIC:
    echo 1. Verifier les logs dans logs/
    echo 2. Executer diagnostic_python.bat
    echo 3. Reinstaller avec install_alternative.bat
    echo.
)

pause
