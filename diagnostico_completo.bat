@echo off
chcp 65001 >nul
title Diagnóstico Completo - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA                     ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📋 Información del sistema:
echo    • Fecha: %date%
echo    • Hora: %time%
echo    • Directorio: %CD%
echo    • Usuario: %USERNAME%
echo.

echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    1. VERIFICACIÓN DE PYTHON                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Python del sistema
echo 🔍 Python del sistema:
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ Python NO disponible en PATH del sistema
) else (
    echo    ✅ Python disponible:
    python --version
    echo    📁 Ubicación:
    where python 2>nul
)

REM Python del venv
echo.
echo 🔍 Python del entorno virtual:
if exist "venv\Scripts\python.exe" (
    echo    ✅ Python del venv existe
    echo    📁 Ubicación: %CD%\venv\Scripts\python.exe
    echo    🔢 Versión:
    venv\Scripts\python.exe --version 2>nul
    if errorlevel 1 (
        echo    ❌ Python del venv no funciona
    )
) else (
    echo    ❌ Python del venv NO EXISTE
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    2. VERIFICACIÓN DEL ENTORNO VIRTUAL                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if exist "venv" (
    echo ✅ Directorio venv/ existe
    
    echo 📁 Contenido de venv/:
    dir venv /b 2>nul
    
    echo.
    echo 📁 Contenido de venv\Scripts\:
    if exist "venv\Scripts" (
        dir venv\Scripts\*.exe /b 2>nul | findstr /i "python pip"
    ) else (
        echo    ❌ Directorio Scripts no existe
    )
) else (
    echo ❌ Directorio venv/ NO EXISTE
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    3. VERIFICACIÓN DE DEPENDENCIAS                         ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if exist "venv\Scripts\python.exe" (
    echo 🔍 Paquetes instalados en el venv:
    venv\Scripts\pip.exe list 2>nul | findstr /i "pyqt5 reportlab pillow dateutil"
    
    echo.
    echo 🧪 Test de importación:
    
    echo    📦 PyQt5:
    venv\Scripts\python.exe -c "import PyQt5; print('       ✅ OK')" 2>nul || echo        ❌ FALLA
    
    echo    📦 PyQt5.QtWidgets:
    venv\Scripts\python.exe -c "from PyQt5.QtWidgets import QApplication; print('       ✅ OK')" 2>nul || echo        ❌ FALLA
    
    echo    📦 reportlab:
    venv\Scripts\python.exe -c "import reportlab; print('       ✅ OK')" 2>nul || echo        ❌ FALLA
    
    echo    📦 Pillow:
    venv\Scripts\python.exe -c "import PIL; print('       ✅ OK')" 2>nul || echo        ❌ FALLA
    
    echo    📦 python-dateutil:
    venv\Scripts\python.exe -c "import dateutil; print('       ✅ OK')" 2>nul || echo        ❌ FALLA
) else (
    echo ❌ No se puede verificar dependencias - Python del venv no disponible
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    4. VERIFICACIÓN DE ARCHIVOS                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 📁 Archivos principales:
if exist "main.py" (echo    ✅ main.py) else (echo    ❌ main.py)
if exist "requirements.txt" (echo    ✅ requirements.txt) else (echo    ❌ requirements.txt)
if exist "lancer_app.bat" (echo    ✅ lancer_app.bat) else (echo    ❌ lancer_app.bat)
if exist "lancer_rapide.bat" (echo    ✅ lancer_rapide.bat) else (echo    ❌ lancer_rapide.bat)
if exist "instalar_app.bat" (echo    ✅ instalar_app.bat) else (echo    ❌ instalar_app.bat)

echo.
echo 📁 Directorios importantes:
if exist "ui" (echo    ✅ ui/) else (echo    ❌ ui/)
if exist "database" (echo    ✅ database/) else (echo    ❌ database/)
if exist "common" (echo    ✅ common/) else (echo    ❌ common/)
if exist "utils" (echo    ✅ utils/) else (echo    ❌ utils/)
if exist "config" (echo    ✅ config/) else (echo    ❌ config/)
if exist "assets" (echo    ✅ assets/) else (echo    ❌ assets/)

echo.
echo 📁 Directorios de datos:
if exist "logs" (echo    ✅ logs/) else (echo    ⚠️  logs/ (se creará automáticamente))
if exist "pdfs" (echo    ✅ pdfs/) else (echo    ⚠️  pdfs/ (se creará automáticamente))
if exist "base_de_datos" (echo    ✅ base_de_datos/) else (echo    ⚠️  base_de_datos/ (se creará automáticamente))

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    5. VERIFICACIÓN DE ICONOS                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🎯 Iconos de acceso directo:
if exist "🚀 Lanzar Facturación Fácil.lnk" (echo    ✅ 🚀 Lanzar Facturación Fácil.lnk) else (echo    ❌ 🚀 Lanzar Facturación Fácil.lnk)
if exist "🔄 Actualizar desde Git.lnk" (echo    ✅ 🔄 Actualizar desde Git.lnk) else (echo    ❌ 🔄 Actualizar desde Git.lnk)
if exist "🗑️ Desinstalar Aplicación.lnk" (echo    ✅ 🗑️ Desinstalar Aplicación.lnk) else (echo    ❌ 🗑️ Desinstalar Aplicación.lnk)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📋 RESUMEN Y RECOMENDACIONES                            ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Determinar estado general
set "SYSTEM_OK=1"

if not exist "venv\Scripts\python.exe" set "SYSTEM_OK=0"
if not exist "main.py" set "SYSTEM_OK=0"

venv\Scripts\python.exe -c "import PyQt5" >nul 2>&1
if errorlevel 1 set "SYSTEM_OK=0"

if "%SYSTEM_OK%"=="1" (
    echo ✅ SISTEMA COMPLETAMENTE FUNCIONAL
    echo.
    echo 🎯 Todo está listo para usar:
    echo    • Entorno virtual: Configurado
    echo    • Dependencias: Instaladas
    echo    • Aplicación: Lista
    echo.
    echo 🚀 Para usar la aplicación:
    echo    lancer_app.bat      - Lanzamiento con verificaciones
    echo    lancer_rapide.bat   - Lanzamiento rápido
) else (
    echo ❌ SISTEMA REQUIERE CONFIGURACIÓN
    echo.
    echo 🔧 Acciones recomendadas:
    echo    1. Ejecutar: instalar_app.bat
    echo    2. Ejecutar: crear_iconos_personalizados.bat
    echo    3. Ejecutar: test_entorno_virtual.bat
)

echo.
echo 🎯 Diagnóstico completado
pause
