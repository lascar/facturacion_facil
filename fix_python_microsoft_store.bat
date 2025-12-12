@echo off
chcp 65001 >nul
title Corrección Python Microsoft Store

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                🔧 CORRECCIÓN PYTHON MICROSOFT STORE                        ║
echo ║                                                                              ║
echo ║  Este script resuelve el problema donde 'python' abre Microsoft Store      ║
echo ║  en lugar de ejecutar Python en Windows 10/11                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Diagnosticando el problema...
echo.

REM Verificar si el problema existe
echo 📋 Test 1: Verificando comando 'python'
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ El comando 'python' no funciona (probablemente abre Microsoft Store)
    set "PROBLEM_DETECTED=1"
) else (
    echo    ✅ El comando 'python' funciona correctamente
    python --version
    echo.
    echo 🎉 No hay problema detectado. Su Python funciona correctamente.
    pause
    exit /b 0
)

echo.
echo 📋 Test 2: Verificando Python Launcher
py --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ Python Launcher (py) no disponible
) else (
    echo    ✅ Python Launcher (py) disponible:
    py --version
    set "PY_AVAILABLE=1"
)

echo.
echo 📋 Test 3: Buscando instalaciones de Python
set "PYTHON_INSTALLATIONS=0"
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%PROGRAMFILES%\Python*\python.exe"
    "%PROGRAMFILES(X86)%\Python*\python.exe"
) do (
    if exist "%%p" (
        set /a PYTHON_INSTALLATIONS+=1
        echo    ✅ Encontrado: %%p
        "%%p" --version 2>nul
    )
)

if %PYTHON_INSTALLATIONS%==0 (
    echo    ❌ No se encontraron instalaciones de Python
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🛠️ SOLUCIONES DISPONIBLES                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if defined PY_AVAILABLE (
    echo ✅ SOLUCIÓN RECOMENDADA: Usar Python Launcher
    echo.
    echo    El Python Launcher (py) está disponible y es la forma más confiable
    echo    de ejecutar Python en Windows. Los scripts han sido actualizados
    echo    para usar 'py' en lugar de 'python'.
    echo.
    echo    📋 Comandos equivalentes:
    echo       En lugar de: python script.py
    echo       Use:         py script.py
    echo.
    echo       En lugar de: python -m pip install package
    echo       Use:         py -m pip install package
    echo.
    goto :end_solutions
)

if %PYTHON_INSTALLATIONS% gtr 0 (
    echo ✅ SOLUCIÓN ALTERNATIVA: Usar ruta completa
    echo.
    echo    Se encontraron instalaciones de Python. Los scripts han sido
    echo    actualizados para usar la ruta completa en lugar del comando 'python'.
    echo.
    goto :end_solutions
)

echo ❌ PROBLEMA: Python no está instalado correctamente
echo.
echo 💡 SOLUCIONES:
echo.
echo    1. INSTALAR PYTHON CORRECTAMENTE:
echo       • Vaya a https://python.org/downloads/
echo       • Descargue Python 3.8 o superior
echo       • Durante la instalación, MARQUE "Add Python to PATH"
echo       • Reinicie la terminal después de la instalación
echo.
echo    2. DESACTIVAR ALIAS DE MICROSOFT STORE:
echo       • Abra Configuración de Windows
echo       • Vaya a Aplicaciones ^> Alias de ejecución de aplicaciones
echo       • Desactive los alias para python.exe y python3.exe
echo.
echo    3. USAR PYTHON LAUNCHER:
echo       • Instale Python desde python.org (incluye Python Launcher)
echo       • Use 'py' en lugar de 'python' en comandos

:end_solutions
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🔧 APLICAR CORRECCIÓN AUTOMÁTICA                        ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if defined PY_AVAILABLE (
    echo ✅ Los scripts de instalación ya están configurados para usar 'py'
    echo.
    echo 🚀 Puede proceder con la instalación usando:
    echo    instalar_app.bat
    echo.
) else (
    echo ⚠️  Se requiere acción manual:
    echo.
    echo    1. Instale Python desde https://python.org/downloads/
    echo    2. Marque "Add Python to PATH" durante la instalación
    echo    3. Ejecute este script nuevamente para verificar
    echo.
    echo 📥 ¿Desea abrir la página de descarga de Python? (s/n)
    set /p open_page="Respuesta: "
    if /i "%open_page%"=="s" (
        start https://python.org/downloads/
        echo 📥 Página de descarga abierta
    )
)

echo.
echo 🎯 Diagnóstico completado
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Si Python Launcher está disponible: ejecute instalar_app.bat
echo    2. Si no: instale Python desde python.org y ejecute este script nuevamente
echo.
pause
