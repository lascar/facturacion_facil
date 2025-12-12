@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 Facturacion Facil - Lancement
echo ========================================
echo.

REM Changer vers le répertoire du script (CRITIQUE pour fonctionner depuis n'importe où)
echo 📁 Directorio actual: %CD%
echo 📁 Directorio del script: %~dp0
cd /d "%~dp0"
echo 📁 Cambiado a: %CD%
echo.

REM Vérifier si l'environnement virtuel existe d'abord
echo 🔍 Vérification de l'environnement virtuel...
if not exist "venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel non trouvé
    echo 📥 Exécutez d'abord: instalar_app.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Environnement virtuel trouvé
venv\Scripts\python.exe --version

REM Utiliser directement Python du venv (pas besoin d'activation)
echo 🔧 Utilisation de l'environnement virtuel...

REM Vérifier si PyQt5 est installé dans le venv
echo.
echo 🔍 Vérification de PyQt5 dans l'environnement virtuel...
venv\Scripts\python.exe -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt5 non trouvé dans l'environnement virtuel
    echo 📥 Exécutez d'abord: instalar_app.bat
    echo.
    pause
    exit /b 1
) else (
    echo ✅ PyQt5 détecté dans l'environnement virtuel
)

REM Test rapide de PyQt5 dans le venv
echo.
echo 🧪 Test de PyQt5...
venv\Scripts\python.exe -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 fonctionne!')" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 ne fonctionne pas correctement
    echo 📥 Exécutez: instalar_app.bat pour réinstaller
    pause
    exit /b 1
)

REM Vérifier la base de données
echo.
echo 🔍 Vérification de la base de données...
if exist "facturacion.db" (
    echo ✅ Base de données trouvée
) else (
    echo ⚠️  Base de données non trouvée - sera créée au premier lancement
)

REM Créer le dossier logs s'il n'existe pas
if not exist "logs" (
    mkdir logs
    echo ✅ Dossier logs créé
)

REM Lancer l'application
echo.
echo ========================================
echo 🚀 Lancement de Facturacion Facil...
echo ========================================
echo.
echo 💡 Fonctionnalités disponibles:
echo    • Gestion des clients avec autocomplétion
echo    • Édition de clients avec boutons Guardar/Deshacer
echo    • Gestion des factures et produits
echo    • Génération de PDF
echo    • Système de stock
echo.
echo 🔧 En cas de problème, consultez les logs dans le dossier 'logs/'
echo.

venv\Scripts\python.exe main.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ L'application s'est fermée avec une erreur
    echo ========================================
    echo.
    echo 🔍 Vérifiez les logs dans le dossier 'logs/' pour plus de détails
    echo.
    echo 💡 Solutions courantes:
    echo    • Redémarrez le script
    echo    • Vérifiez votre connexion internet
    echo    • Contactez le support technique
    echo.
) else (
    echo.
    echo ========================================
    echo ✅ Application fermée normalement
    echo ========================================
    echo.
)

echo 👋 Appuyez sur une touche pour fermer...
pause >nul
