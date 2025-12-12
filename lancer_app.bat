@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 Facturacion Facil - Lancement
echo ========================================
echo.

REM Changer vers le répertoire du script
cd /d "%~dp0"

REM Vérifier si Python est installé
echo 🔍 Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
    echo.
    echo 💡 Veuillez installer Python depuis https://python.org
    echo    N'oubliez pas de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python détecté

REM Vérifier si l'environnement virtuel existe
echo.
echo 🔍 Vérification de l'environnement virtuel...
if not exist "venv\Scripts\activate.bat" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERREUR: Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel trouvé
)

REM Activer l'environnement virtuel
echo.
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

echo ✅ Environnement virtuel activé

REM Vérifier si PyQt5 est installé
echo.
echo 🔍 Vérification de PyQt5...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo 📚 Installation des dépendances...
    echo    - Mise à jour de pip...
    python -m pip install --upgrade pip
    echo    - Installation de PyQt5 et autres dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERREUR: Impossible d'installer les dépendances
        echo.
        echo 💡 Vérifiez votre connexion internet et réessayez
        pause
        exit /b 1
    )
    echo ✅ Dépendances installées
) else (
    echo ✅ PyQt5 détecté
)

REM Test rapide de PyQt5
echo.
echo 🧪 Test de PyQt5...
python -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 fonctionne!')" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 ne fonctionne pas correctement
    echo 💡 Réinstallez les dépendances avec: pip install --force-reinstall PyQt5
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

python main.py

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
