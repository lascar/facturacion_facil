@echo off
echo ========================================
echo   Installation Facturacion Facil
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

REM Verifier si Python est installe
echo Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo.
    echo SOLUTION:
    echo 1. Telecharger Python depuis https://python.org/downloads/windows/
    echo 2. Pendant l'installation, cocher "Add Python to PATH"
    echo 3. Relancer ce script apres installation
    echo.
    pause
    exit /b 1
)

python --version
echo Python OK!
echo.

REM Creer l'environnement virtuel
echo Creation de l'environnement virtuel...
if exist "venv" (
    echo Environnement virtuel existe deja, suppression...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)
echo Environnement virtuel cree!
echo.

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre a jour pip
echo Mise a jour de pip...
python -m pip install --upgrade pip

REM Installer les dependances
echo Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERREUR: Impossible d'installer les dependances
    echo.
    echo SOLUTIONS POSSIBLES:
    echo 1. Verifier la connexion internet
    echo 2. Executer en tant qu'administrateur
    echo 3. Desactiver temporairement l'antivirus
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo     INSTALLATION TERMINEE!
echo ========================================
echo.
echo Pour lancer l'application:
echo 1. Double-clic sur start.bat
echo 2. Ou executer: python main.py
echo.
echo Test de l'installation...
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import reportlab; print('ReportLab OK')"
python -c "import PIL; print('Pillow OK')"
echo.
echo Toutes les dependances sont installees!
echo.

REM Proposer de lancer l'application
set /p launch="Voulez-vous lancer l'application maintenant? (o/n): "
if /i "%launch%"=="o" (
    echo.
    echo Lancement de l'application...
    python main.py
)

echo.
echo Installation terminee avec succes!
pause
