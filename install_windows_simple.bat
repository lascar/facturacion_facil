@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  Installation Facturacion Facil
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo 💡 Solutions:
    echo   1. Installer Python depuis Microsoft Store
    echo   2. Ou télécharger depuis python.org
    echo   3. Redémarrer ce script après installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Créer l'environnement virtuel
echo.
echo 📦 Création de l'environnement virtuel...
if exist venv (
    echo ⚠️  Environnement virtuel existant détecté
    set /p "recreate=Recréer l'environnement? (y/N): "
    if /i "!recreate!"=="y" (
        rmdir /s /q venv
        echo 🗑️  Ancien environnement supprimé
    )
)

if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Échec de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
)

REM Activer l'environnement virtuel
echo.
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Échec de l'activation de l'environnement virtuel
    pause
    exit /b 1
)

REM Mettre à jour pip
echo.
echo 📈 Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo.
echo 📚 Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Échec de l'installation des dépendances
    echo.
    echo 💡 Essayez ces solutions:
    echo   1. pip install PyQt6==6.6.1
    echo   2. pip install PySide6 (alternative)
    echo   3. Installer Visual C++ Redistributable
    echo.
    pause
    exit /b 1
)

REM Test de l'installation PyQt6
echo.
echo 🧪 Test de PyQt6...
python -c "from PyQt6 import QtCore; print('✅ PyQt6 fonctionne')" 2>nul
if errorlevel 1 (
    echo ❌ Problème avec PyQt6
    echo.
    echo 💡 Solutions pour le problème DLL:
    echo   1. Installer Visual C++ Redistributable 2015-2022
    echo   2. Réinstaller PyQt6: pip uninstall PyQt6 ^&^& pip install PyQt6==6.6.1
    echo   3. Utiliser PySide6: pip install PySide6
    echo.
    set /p "continue=Continuer malgré l'erreur? (y/N): "
    if not "!continue!"=="y" if not "!continue!"=="Y" (
        pause
        exit /b 1
    )
) else (
    echo ✅ PyQt6 fonctionne correctement
)

echo.
echo 🎉 Installation terminée!
echo.
echo 🚀 Pour lancer l'application:
echo   1. Ouvrir une invite de commande dans ce dossier
echo   2. Exécuter: venv\Scripts\activate.bat
echo   3. Exécuter: python main.py
echo.

set /p "launch=Lancer l'application maintenant? (y/N): "
if /i "!launch!"=="y" (
    echo.
    echo 🚀 Lancement de l'application...
    python main.py
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
