@echo off
chcp 65001 >nul
title Test de Détection Python

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🔍 TEST DE DÉTECTION PYTHON                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Méthode 1: Commande 'python'
python --version 2>nul
if errorlevel 1 (
    echo    ❌ 'python' ne fonctionne pas (peut ouvrir Microsoft Store)
) else (
    echo    ✅ 'python' fonctionne
)

echo.
echo 🔍 Méthode 2: Commande 'python.exe' avec where
where python.exe >nul 2>&1
if errorlevel 1 (
    echo    ❌ 'python.exe' non trouvé avec where
) else (
    echo    ✅ 'python.exe' trouvé avec where:
    for /f "tokens=*" %%i in ('where python.exe 2^>nul') do (
        echo       %%i
        "%%i" --version 2>nul
        if errorlevel 1 (
            echo       ❌ Ce python.exe ne fonctionne pas
        ) else (
            echo       ✅ Ce python.exe fonctionne
        )
    )
)

echo.
echo 🔍 Méthode 3: Python Launcher 'py'
py --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ 'py' (Python Launcher) non disponible
) else (
    echo    ✅ 'py' (Python Launcher) disponible:
    py --version
)

echo.
echo 🔍 Méthode 4: Recherche dans les emplacements standards
set "FOUND_PYTHON="
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%PROGRAMFILES%\Python*\python.exe"
    "%PROGRAMFILES(X86)%\Python*\python.exe"
    "C:\Python*\python.exe"
) do (
    if exist "%%p" (
        echo    ✅ Trouvé: %%p
        "%%p" --version 2>nul
        if not errorlevel 1 (
            echo       ✅ Fonctionne
            set "FOUND_PYTHON=%%p"
        ) else (
            echo       ❌ Ne fonctionne pas
        )
    )
)

if not defined FOUND_PYTHON (
    echo    ❌ Aucun Python trouvé dans les emplacements standards
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📋 RÉSUMÉ                                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Déterminer la meilleure méthode
set "BEST_PYTHON="

REM Essayer py en premier (plus fiable)
py --version >nul 2>&1
if not errorlevel 1 (
    set "BEST_PYTHON=py"
    echo ✅ RECOMMANDÉ: Utiliser 'py' (Python Launcher)
    py --version
    goto :end_test
)

REM Essayer where python.exe
where python.exe >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('where python.exe 2^>nul') do (
        "%%i" --version >nul 2>&1
        if not errorlevel 1 (
            set "BEST_PYTHON=%%i"
            echo ✅ RECOMMANDÉ: Utiliser '%%i'
            "%%i" --version
            goto :end_test
        )
    )
)

REM Essayer les emplacements standards
if defined FOUND_PYTHON (
    set "BEST_PYTHON=%FOUND_PYTHON%"
    echo ✅ RECOMMANDÉ: Utiliser '%FOUND_PYTHON%'
    "%FOUND_PYTHON%" --version
    goto :end_test
)

echo ❌ AUCUN PYTHON FONCTIONNEL TROUVÉ
echo.
echo 💡 Solutions:
echo    1. Installer Python depuis https://python.org
echo    2. Cocher "Add Python to PATH" pendant l'installation
echo    3. Redémarrer la terminal après installation

:end_test
echo.
echo 🎯 Test terminé
pause
