@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  Setup Facturacion Facil avec PySide6
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 💡 Installez Python depuis Microsoft Store ou python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo.
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Échec de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel existant trouvé
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

echo ✅ Environnement virtuel activé

REM Mettre à jour pip
echo.
echo 📈 Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer PySide6
echo.
echo 📚 Installation de PySide6...
pip install PySide6
if errorlevel 1 (
    echo ❌ Échec de l'installation de PySide6
    pause
    exit /b 1
)

REM Installer les autres dépendances
echo.
echo 📚 Installation des autres dépendances...
pip install -r requirements.txt

REM Tester PySide6
echo.
echo 🧪 Test de PySide6...
python -c "from PySide6 import QtCore; print('✅ PySide6 fonctionne!')" 2>nul
if errorlevel 1 (
    echo ❌ PySide6 ne fonctionne pas correctement
    echo 💡 Vérifiez l'installation
    pause
    exit /b 1
)

echo ✅ PySide6 fonctionne correctement

REM Lancer l'application
echo.
echo 🚀 Lancement de l'application...
echo.
python main.py

echo.
echo 👋 Application fermée
pause
