@echo off
REM Script d'installation automatisée pour Windows 11
REM Facturación Fácil - Version PyQt5

echo.
echo ========================================
echo  INSTALLATION FACTURACION FACIL
echo  Optimisé pour Windows 11
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo 💡 Options d'installation Python pour Windows 11:
    echo    1. Microsoft Store: Rechercher "Python 3.12"
    echo    2. Winget: winget install Python.Python.3.12
    echo    3. Site officiel: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Vérifier la version de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Version Python: %PYTHON_VERSION%

REM Mettre à jour pip
echo.
echo 📦 Mise à jour de pip...
python -m pip install --upgrade pip

REM Créer un environnement virtuel
echo.
echo 🔧 Création de l'environnement virtuel...
if exist venv (
    echo Environnement virtuel existant détecté
    choice /c YN /m "Voulez-vous le recréer"
    if !errorlevel!==1 (
        rmdir /s /q venv
        python -m venv venv
    )
) else (
    python -m venv venv
)

REM Activer l'environnement virtuel
echo.
echo 🚀 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo.
echo 📥 Installation des dépendances...
pip install -r requirements.txt

REM Installer les dépendances de développement (optionnel)
choice /c YN /m "Installer les outils de développement"
if %errorlevel%==1 (
    echo 🛠️ Installation des outils de développement...
    pip install -r requirements-dev.txt
)

REM Tester l'installation
echo.
echo 🧪 Test de compatibilité Windows 11...
python test_windows11_compatibility.py

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Des problèmes de compatibilité ont été détectés
    echo Consultez les messages ci-dessus pour plus de détails
    pause
    exit /b 1
)

REM Créer un raccourci sur le bureau (optionnel)
choice /c YN /m "Créer un raccourci sur le bureau"
if %errorlevel%==1 (
    echo 🔗 Création du raccourci...
    set DESKTOP=%USERPROFILE%\Desktop
    set CURRENT_DIR=%CD%
    
    echo @echo off > "%DESKTOP%\Facturacion Facil.bat"
    echo cd /d "%CURRENT_DIR%" >> "%DESKTOP%\Facturacion Facil.bat"
    echo call venv\Scripts\activate.bat >> "%DESKTOP%\Facturacion Facil.bat"
    echo python main.py >> "%DESKTOP%\Facturacion Facil.bat"
    
    echo ✅ Raccourci créé sur le bureau
)

echo.
echo ========================================
echo  🎉 INSTALLATION TERMINÉE AVEC SUCCÈS!
echo ========================================
echo.
echo 🚀 Pour lancer l'application:
echo    1. Ouvrir un terminal dans ce dossier
echo    2. Exécuter: venv\Scripts\activate.bat
echo    3. Exécuter: python main.py
echo.
echo 💡 Ou utiliser le raccourci sur le bureau (si créé)
echo.
echo 📚 Documentation complète: doc\manual_instalacion_windows.md
echo.

REM Proposer de lancer l'application
choice /c YN /m "Lancer l'application maintenant"
if %errorlevel%==1 (
    echo.
    echo 🚀 Lancement de Facturación Fácil...
    python main.py
)

echo.
echo Merci d'utiliser Facturación Fácil!
pause
