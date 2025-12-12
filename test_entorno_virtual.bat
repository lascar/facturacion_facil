@echo off
chcp 65001 >nul
title Test Entorno Virtual - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🧪 TEST DEL ENTORNO VIRTUAL                             ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 Verificando estructura del entorno virtual...
echo.

REM Verificar directorio venv
if exist "venv" (
    echo ✅ Directorio venv/ existe
) else (
    echo ❌ Directorio venv/ NO EXISTE
    echo 📥 Ejecute: instalar_app.bat
    goto :end_test
)

REM Verificar Python en venv
if exist "venv\Scripts\python.exe" (
    echo ✅ Python en venv existe
    echo    Ubicación: %CD%\venv\Scripts\python.exe
    
    REM Mostrar versión de Python del venv
    echo    Versión: 
    venv\Scripts\python.exe --version 2>nul
    if errorlevel 1 (
        echo ❌ Python del venv no funciona
    )
) else (
    echo ❌ Python en venv NO EXISTE
    goto :end_test
)

REM Verificar pip en venv
if exist "venv\Scripts\pip.exe" (
    echo ✅ pip en venv existe
    echo    Versión: 
    venv\Scripts\pip.exe --version 2>nul
) else (
    echo ❌ pip en venv NO EXISTE
)

REM Verificar script de activación
if exist "venv\Scripts\activate.bat" (
    echo ✅ Script de activación existe
) else (
    echo ❌ Script de activación NO EXISTE
)

echo.
echo 🔍 Verificando dependencias en el entorno virtual...
echo.

REM Verificar PyQt5
echo 📦 PyQt5:
venv\Scripts\python.exe -c "import PyQt5; print('   ✅ PyQt5 importado correctamente')" 2>nul
if errorlevel 1 (
    echo    ❌ PyQt5 NO ESTÁ INSTALADO en el venv
    set "DEPS_ERROR=1"
) else (
    venv\Scripts\python.exe -c "from PyQt5.QtWidgets import QApplication; print('   ✅ PyQt5.QtWidgets funciona')" 2>nul
    if errorlevel 1 (
        echo    ⚠️  PyQt5 instalado pero QtWidgets no funciona
        set "DEPS_ERROR=1"
    )
)

REM Verificar reportlab
echo 📦 reportlab:
venv\Scripts\python.exe -c "import reportlab; print('   ✅ reportlab importado correctamente')" 2>nul
if errorlevel 1 (
    echo    ❌ reportlab NO ESTÁ INSTALADO en el venv
    set "DEPS_ERROR=1"
)

REM Verificar Pillow
echo 📦 Pillow:
venv\Scripts\python.exe -c "import PIL; print('   ✅ Pillow importado correctamente')" 2>nul
if errorlevel 1 (
    echo    ❌ Pillow NO ESTÁ INSTALADO en el venv
    set "DEPS_ERROR=1"
)

REM Verificar python-dateutil
echo 📦 python-dateutil:
venv\Scripts\python.exe -c "import dateutil; print('   ✅ python-dateutil importado correctamente')" 2>nul
if errorlevel 1 (
    echo    ❌ python-dateutil NO ESTÁ INSTALADO en el venv
    set "DEPS_ERROR=1"
)

echo.
echo 🔍 Verificando archivos de la aplicación...
echo.

if exist "main.py" (
    echo ✅ main.py existe
) else (
    echo ❌ main.py NO EXISTE
    set "APP_ERROR=1"
)

if exist "requirements.txt" (
    echo ✅ requirements.txt existe
    echo    Contenido:
    type requirements.txt | findstr /v "^#" | findstr /v "^$"
) else (
    echo ❌ requirements.txt NO EXISTE
    set "APP_ERROR=1"
)

echo.
echo 🧪 Test de lanzamiento simulado...
echo.

REM Test de importación de la aplicación
echo 📋 Verificando que la aplicación puede importar sus módulos...
venv\Scripts\python.exe -c "
import sys
sys.path.insert(0, '.')
try:
    import main
    print('✅ main.py se puede importar')
except ImportError as e:
    print(f'❌ Error al importar main.py: {e}')
except Exception as e:
    print(f'⚠️  main.py importado pero con advertencias: {e}')
" 2>nul

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📋 RESUMEN DEL TEST                                      ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if not defined DEPS_ERROR if not defined APP_ERROR (
    echo ✅ ENTORNO VIRTUAL COMPLETAMENTE FUNCIONAL
    echo.
    echo 🎯 Todo está listo para usar:
    echo    • Entorno virtual: Configurado correctamente
    echo    • Dependencias: Todas instaladas
    echo    • Aplicación: Lista para ejecutar
    echo.
    echo 🚀 Para lanzar la aplicación:
    echo    • lancer_app.bat (con verificaciones)
    echo    • lancer_rapide.bat (lanzamiento rápido)
    echo    • Doble clic en "🚀 Lanzar App.lnk"
) else (
    echo ❌ PROBLEMAS DETECTADOS
    echo.
    if defined DEPS_ERROR (
        echo 🔧 Dependencias faltantes o corruptas
        echo    Solución: Ejecute instalar_app.bat
    )
    if defined APP_ERROR (
        echo 🔧 Archivos de aplicación faltantes
        echo    Solución: Verifique que está en el directorio correcto
    )
    echo.
    echo 💡 Ejecute instalar_app.bat para resolver los problemas
)

:end_test
echo.
echo 🎯 Test completado
pause
