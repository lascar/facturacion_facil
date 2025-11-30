@echo off
chcp 65001 >nul
title Correction Environnement Virtuel - Facturación Fácil

echo ========================================
echo   🔧 CORRECTION ENVIRONNEMENT VIRTUEL
echo ========================================
echo.

:: Vérifier si on est dans le bon répertoire
if not exist "main.py" (
    echo ❌ ERREUR: Fichier main.py non trouvé
    echo Assurez-vous d'être dans le répertoire de l'application
    echo.
    pause
    exit /b 1
)

echo 🔍 Diagnostic de l'environnement virtuel...
echo.

:: Vérifier Python
echo 📋 Vérification de Python:
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'python' non trouvé, essai avec 'py'...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo   ❌ Python non installé ou pas dans le PATH
        echo.
        echo 💡 Solutions:
        echo   1. Installer Python depuis https://python.org
        echo   2. Cocher "Add Python to PATH" pendant l'installation
        echo   3. Redémarrer l'ordinateur après installation
        echo.
        pause
        exit /b 1
    ) else (
        py --version
        echo   ✅ Python trouvé avec 'py'
        set PYTHON_CMD=py
    )
) else (
    python --version
    echo   ✅ Python trouvé avec 'python'
    set PYTHON_CMD=python
)

echo.

:: Chercher les environnements virtuels existants
echo 🔍 Recherche d'environnements virtuels existants:
set ENV_FOUND=0

if exist "env\Scripts\activate.bat" (
    echo   ✅ Trouvé: env\Scripts\activate.bat
    set ENV_PATH=env
    set ENV_FOUND=1
)

if exist "venv\Scripts\activate.bat" (
    echo   ✅ Trouvé: venv\Scripts\activate.bat
    set ENV_PATH=venv
    set ENV_FOUND=1
)

if exist ".venv\Scripts\activate.bat" (
    echo   ✅ Trouvé: .venv\Scripts\activate.bat
    set ENV_PATH=.venv
    set ENV_FOUND=1
)

if exist "Scripts\activate.bat" (
    echo   ✅ Trouvé: Scripts\activate.bat (environnement dans le répertoire courant)
    set ENV_PATH=.
    set ENV_FOUND=1
)

if %ENV_FOUND%==0 (
    echo   ⚠️  Aucun environnement virtuel trouvé
    echo.
    echo 🔧 Création d'un nouvel environnement virtuel...
    
    %PYTHON_CMD% -m venv env
    if errorlevel 1 (
        echo   ❌ Échec de la création de l'environnement virtuel
        echo.
        echo 💡 Essai avec une méthode alternative...
        %PYTHON_CMD% -m virtualenv env
        if errorlevel 1 (
            echo   ❌ Échec avec virtualenv aussi
            echo.
            echo 🛠️  Solutions à essayer:
            echo   1. Installer virtualenv: %PYTHON_CMD% -m pip install virtualenv
            echo   2. Vérifier les permissions (exécuter en tant qu'administrateur)
            echo   3. Désactiver temporairement l'antivirus
            echo.
            pause
            exit /b 1
        )
    )
    
    echo   ✅ Environnement virtuel créé: env
    set ENV_PATH=env
    set ENV_FOUND=1
)

echo.

:: Tester l'activation
echo 🧪 Test d'activation de l'environnement virtuel:
echo   Environnement: %ENV_PATH%
echo.

if "%ENV_PATH%"=="." (
    call Scripts\activate.bat
) else (
    call %ENV_PATH%\Scripts\activate.bat
)

if errorlevel 1 (
    echo   ❌ Échec de l'activation
    echo.
    echo 🔧 Tentative de réparation...
    
    :: Supprimer et recréer l'environnement
    if exist "%ENV_PATH%" (
        echo   🗑️  Suppression de l'environnement corrompu...
        rmdir /S /Q "%ENV_PATH%" >nul 2>&1
    )
    
    echo   🔧 Création d'un nouvel environnement...
    %PYTHON_CMD% -m venv env
    if errorlevel 1 (
        echo   ❌ Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    
    set ENV_PATH=env
    call env\Scripts\activate.bat
    if errorlevel 1 (
        echo   ❌ L'activation échoue encore
        echo.
        echo 🚨 Problème persistant détecté
        echo.
        echo 💡 Solutions avancées:
        echo   1. Vérifier les permissions du répertoire
        echo   2. Exécuter en tant qu'administrateur
        echo   3. Vérifier l'antivirus (peut bloquer les scripts)
        echo   4. Essayer dans un autre répertoire
        echo.
        pause
        exit /b 1
    )
)

echo   ✅ Activation réussie!
echo.

:: Vérifier pip dans l'environnement virtuel
echo 📦 Vérification de pip:
pip --version >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  pip non trouvé, installation...
    %PYTHON_CMD% -m ensurepip --upgrade
    if errorlevel 1 (
        echo   ❌ Impossible d'installer pip
    ) else (
        echo   ✅ pip installé
    )
) else (
    pip --version
    echo   ✅ pip disponible
)

echo.

:: Installer les dépendances
echo 📋 Installation des dépendances:
if exist "requirements.txt" (
    echo   📦 Installation depuis requirements.txt...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo   ⚠️  Problème lors de l'installation des dépendances
        echo   Essai sans --quiet pour voir les erreurs...
        pip install -r requirements.txt
    ) else (
        echo   ✅ Dépendances installées
    )
) else (
    echo   ⚠️  Fichier requirements.txt non trouvé
    echo   Installation des dépendances de base...
    pip install PyQt5 reportlab pillow
    if errorlevel 1 (
        echo   ❌ Échec de l'installation des dépendances de base
    ) else (
        echo   ✅ Dépendances de base installées
    )
)

echo.

:: Test de l'application
echo 🧪 Test de l'application:
python -c "import main; print('✅ Application peut être importée')" 2>nul
if errorlevel 1 (
    echo   ⚠️  Problème lors du test d'import
    echo   Vérification des modules manquants...
    python -c "import PyQt5; print('PyQt5: OK')" 2>nul || echo "   ❌ PyQt5 manquant"
    python -c "import reportlab; print('reportlab: OK')" 2>nul || echo "   ❌ reportlab manquant"
    python -c "import PIL; print('PIL: OK')" 2>nul || echo "   ❌ PIL manquant"
) else (
    echo   ✅ Application testée avec succès
)

echo.

:: Créer un script d'activation personnalisé
echo 🔧 Création d'un script d'activation personnalisé...
(
    echo @echo off
    echo :: Script d'activation personnalisé pour Facturación Fácil
    echo call %ENV_PATH%\Scripts\activate.bat
    echo if errorlevel 1 ^(
    echo     echo ❌ Erreur d'activation de l'environnement virtuel
    echo     echo Exécutez fix_env_activate.bat pour réparer
    echo     pause
    echo     exit /b 1
    echo ^)
    echo echo ✅ Environnement virtuel activé: %ENV_PATH%
) > activate_env.bat

echo   ✅ Script créé: activate_env.bat
echo.

:: Mettre à jour les scripts existants
echo 🔄 Mise à jour des scripts existants...

:: Corriger install.bat
if exist "install.bat" (
    echo   🔧 Correction de install.bat...
    powershell -Command "(Get-Content install.bat) -replace 'python -m env env', '%PYTHON_CMD% -m venv env' | Set-Content install.bat.new"
    if exist "install.bat.new" (
        move "install.bat" "install.bat.backup" >nul 2>&1
        move "install.bat.new" "install.bat" >nul 2>&1
        echo   ✅ install.bat corrigé
    )
)

:: Corriger update.bat
if exist "update.bat" (
    echo   🔧 Correction de update.bat...
    powershell -Command "(Get-Content update.bat) -replace 'env\\Scripts\\activate.bat', '%ENV_PATH%\\Scripts\\activate.bat' | Set-Content update.bat.new"
    if exist "update.bat.new" (
        move "update.bat" "update.bat.backup" >nul 2>&1
        move "update.bat.new" "update.bat" >nul 2>&1
        echo   ✅ update.bat corrigé
    )
)

echo.
echo ========================================
echo   🎉 CORRECTION TERMINÉE AVEC SUCCÈS!
echo ========================================
echo.
echo Environnement virtuel configuré: %ENV_PATH%
echo.
echo 🎯 Pour utiliser l'application:
echo   1. Double-clic sur activate_env.bat (pour activer l'environnement)
echo   2. Puis: python main.py
echo   3. Ou utilisez directement start.bat
echo.
echo 🔧 Scripts corrigés:
if exist "install.bat.backup" echo   • install.bat (sauvegarde: install.bat.backup)
if exist "update.bat.backup" echo   • update.bat (sauvegarde: update.bat.backup)
echo   • Nouveau: activate_env.bat
echo.

echo Voulez-vous tester l'application maintenant? (O/N)
set /p choice=
if /i "%choice%"=="O" if /i "%choice%"=="o" (
    echo 🚀 Lancement de l'application...
    python main.py
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
