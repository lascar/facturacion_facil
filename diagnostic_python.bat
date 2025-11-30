@echo off
echo ========================================
echo   Diagnostic Python pour Windows 11
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

echo Test 1: Version de Python...
python --version
if errorlevel 1 (
    echo ❌ ECHEC: Python non trouve dans le PATH
    echo.
    echo SOLUTIONS:
    echo 1. Installer Python depuis https://python.org/downloads/windows/
    echo 2. Pendant l'installation, cocher "Add Python to PATH"
    echo 3. Redemarrer l'ordinateur
    echo 4. Relancer ce script
    echo.
    goto :error
) else (
    echo ✅ Python trouve
)
echo.

echo Test 2: Module venv disponible...
python -c "import venv; print('✅ Module venv OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: Module venv non disponible
    echo.
    echo SOLUTIONS:
    echo 1. Reinstaller Python avec l'option "pip" et "tcl/tk"
    echo 2. Ou utiliser: python -m ensurepip --upgrade
    echo 3. Ou installer Python depuis le Microsoft Store
    echo.
    goto :error
)
echo.

echo Test 3: Commande venv...
python -m venv --help >nul 2>&1
if errorlevel 1 (
    echo ❌ ECHEC: Commande venv non fonctionnelle
    echo.
    echo SOLUTIONS:
    echo 1. Verifier que Python est complet (pas une version allégée)
    echo 2. Reinstaller Python avec toutes les options
    echo 3. Essayer: py -m venv au lieu de python -m venv
    echo.
    goto :error
) else (
    echo ✅ Commande venv fonctionnelle
)
echo.

echo Test 4: Creation d'un environnement virtuel de test...
if exist "test_venv" (
    rmdir /s /q test_venv
)

python -m venv test_venv
if errorlevel 1 (
    echo ❌ ECHEC: Impossible de creer l'environnement virtuel
    echo.
    echo SOLUTIONS:
    echo 1. Executer en tant qu'administrateur
    echo 2. Verifier l'espace disque disponible
    echo 3. Desactiver l'antivirus temporairement
    echo 4. Essayer dans un autre dossier (ex: C:\temp)
    echo.
    goto :error
) else (
    echo ✅ Environnement virtuel de test cree
    rmdir /s /q test_venv
    echo ✅ Environnement virtuel de test supprime
)
echo.

echo Test 5: Alternative avec py...
py --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Commande 'py' non disponible (normal sur certains systemes)
) else (
    py --version
    echo ✅ Commande 'py' disponible comme alternative
)
echo.

echo Test 6: Modules Python essentiels...
python -c "import sys; print('✅ sys OK')" 2>nul
python -c "import os; print('✅ os OK')" 2>nul
python -c "import subprocess; print('✅ subprocess OK')" 2>nul
echo.

echo ========================================
echo        🎉 DIAGNOSTIC REUSSI!
echo ========================================
echo.
echo Python est correctement installe et configure.
echo Tu peux maintenant utiliser:
echo.
echo   install.bat     - Pour installer l'application
echo   start.bat       - Pour lancer l'application
echo.
goto :end

:error
echo.
echo ========================================
echo         ❌ PROBLEME DETECTE
echo ========================================
echo.
echo Recommandations:
echo.
echo 1. REINSTALLER PYTHON:
echo    - Aller sur https://python.org/downloads/windows/
echo    - Telecharger Python 3.8+ (version complete)
echo    - Pendant l'installation:
echo      ✅ Cocher "Add Python to PATH"
echo      ✅ Cocher "Install pip"
echo      ✅ Cocher "Install tcl/tk and IDLE"
echo      ✅ Choisir "Install for all users" si possible
echo.
echo 2. REDEMARRER l'ordinateur apres installation
echo.
echo 3. RELANCER ce script pour verifier
echo.

:end
echo Appuyez sur une touche pour continuer...
pause >nul
