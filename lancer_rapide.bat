@echo off
chcp 65001 >nul

REM Script de lancement rapide pour Facturacion Facil
REM Utilise l'environnement virtuel existant

cd /d "%~dp0"

echo 🚀 Lancement rapide de Facturacion Facil...

REM Vérifier l'environnement virtuel
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé
    echo 💡 Utilisez 'lancer_app.bat' pour l'installation complète
    pause
    exit /b 1
)

REM Activer et lancer
call venv\Scripts\activate.bat
python main.py

if errorlevel 1 (
    echo ❌ Erreur - Consultez les logs dans 'logs/'
    pause
)
