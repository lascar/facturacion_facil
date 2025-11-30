@echo off
echo ========================================
echo   Installation Alternative (avec py)
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

REM Essayer d'abord avec 'py' (launcher Python Windows)
echo Tentative avec le launcher Python Windows (py)...
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Launcher Python trouve
    set PYTHON_CMD=py
    goto :install
)

REM Sinon essayer avec 'python'
echo Tentative avec python...
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python trouve
    set PYTHON_CMD=python
    goto :install
)

REM Aucune commande Python trouvée
echo ❌ ERREUR: Aucune installation Python trouvee
echo.
echo SOLUTION:
echo 1. Installer Python depuis https://python.org/downloads/windows/
echo 2. Cocher "Add Python to PATH" pendant l'installation
echo 3. Redemarrer l'ordinateur
echo 4. Relancer ce script
echo.
pause
exit /b 1

:install
echo.
echo Utilisation de: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Creer l'environnement virtuel
echo Creation de l'environnement virtuel...
if exist "venv" (
    echo Suppression de l'ancien environnement...
    rmdir /s /q venv
)

%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo ❌ ERREUR: Impossible de creer l'environnement virtuel
    echo.
    echo SOLUTIONS:
    echo 1. Executer en tant qu'administrateur
    echo 2. Verifier l'espace disque
    echo 3. Desactiver l'antivirus temporairement
    echo 4. Essayer diagnostic_python.bat pour plus d'infos
    echo.
    pause
    exit /b 1
)
echo ✅ Environnement virtuel cree
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
    echo ❌ ERREUR: Installation des dependances echouee
    echo.
    echo SOLUTIONS:
    echo 1. Verifier la connexion internet
    echo 2. Essayer: pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
    echo 3. Desactiver temporairement l'antivirus
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo     ✅ INSTALLATION REUSSIE!
echo ========================================
echo.
echo Test des dependances...
python -c "import PyQt5; print('✅ PyQt5 OK')" 2>nul
python -c "import reportlab; print('✅ ReportLab OK')" 2>nul
python -c "import PIL; print('✅ Pillow OK')" 2>nul
echo.
echo Pour lancer l'application:
echo   start.bat
echo   ou: start_alternative.bat
echo.

set /p launch="Lancer l'application maintenant? (o/n): "
if /i "%launch%"=="o" (
    echo Lancement...
    python main.py
)

pause
