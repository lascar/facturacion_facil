@echo off
chcp 65001 >nul

REM Script de lancement rapide pour Facturacion Facil
REM Utilise l'environnement virtuel existant
REM FONCTIONNE DEPUIS N'IMPORTE QUELLE UBICACIÓN

REM Changer vers le répertoire du script (CRITIQUE)
cd /d "%~dp0"

echo 🚀 Lancement rapide de Facturacion Facil...
echo 📁 Directorio: %CD%

REM Vérifier l'environnement virtuel
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé
    echo 💡 Utilisez 'lancer_app.bat' pour l'installation complète
    pause
    exit /b 1
)

REM Lancer directement avec Python du venv (plus rapide)
venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo ❌ Erreur - Consultez les logs dans 'logs/'
    pause
)
