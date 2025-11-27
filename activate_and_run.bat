@echo off
chcp 65001 >nul
echo.
echo 🐍 Activation de l'environnement virtuel...

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé
    echo 💡 Créez-le avec: python -m venv venv
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

echo ✅ Environnement virtuel activé
echo 🐍 Python: %VIRTUAL_ENV%\Scripts\python.exe

REM Vérifier PySide6
echo.
echo 🧪 Test de PySide6...
python -c "from PySide6 import QtCore; print('✅ PySide6 fonctionne!')" 2>nul
if errorlevel 1 (
    echo ❌ PySide6 ne fonctionne pas
    echo 💡 Installez-le avec: pip install PySide6
    pause
    exit /b 1
)

REM Lancer l'application
echo.
echo 🚀 Lancement de l'application...
python main.py

echo.
echo 👋 Application fermée
pause
