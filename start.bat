@echo off
echo ========================================
echo    Facturacion Facil - Demarrage
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo.
    echo Veuillez installer Python depuis https://python.org
    echo N'oubliez pas de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Verifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Verifier si les dependances sont installees
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo Installation des dependances...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dependances
        pause
        exit /b 1
    )
)

REM Lancer l'application
echo.
echo Lancement de Facturacion Facil...
echo.
python main.py

REM Pause pour voir les erreurs eventuelles
if errorlevel 1 (
    echo.
    echo ERREUR: L'application s'est fermee avec une erreur
    echo Verifiez les logs dans le dossier 'logs/'
    echo.
)

pause
