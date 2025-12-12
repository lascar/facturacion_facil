@echo off
chcp 65001 >nul
title Instalación Simple - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 INSTALACIÓN SIMPLE                                   ║
echo ║                   Evita problemas de Microsoft Store                        ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 Detectando Python (método seguro)...
echo.

REM Método más confiable: usar Python Launcher primero
set "PYTHON_CMD="

echo 📋 Método 1: Python Launcher (py.exe)
py --version >nul 2>&1
if not errorlevel 1 (
    echo    ✅ Python Launcher disponible:
    py --version
    set "PYTHON_CMD=py"
    goto :python_ok
) else (
    echo    ❌ Python Launcher no disponible
)

echo.
echo 📋 Método 2: Búsqueda directa en directorios
for %%d in (
    "%LOCALAPPDATA%\Programs\Python"
    "%PROGRAMFILES%"
    "%PROGRAMFILES(X86)%"
    "C:\"
) do (
    if exist "%%d" (
        for /d %%p in ("%%d\Python*") do (
            if exist "%%p\python.exe" (
                echo    • Probando: %%p\python.exe
                "%%p\python.exe" --version >nul 2>&1
                if not errorlevel 1 (
                    echo    ✅ Python funcional encontrado:
                    "%%p\python.exe" --version
                    set "PYTHON_CMD=%%p\python.exe"
                    goto :python_ok
                )
            )
        )
    )
)

echo.
echo ❌ Python no encontrado o no funcional
echo.
echo 💡 SOLUCIÓN RÁPIDA:
echo    1. Descargue Python desde: https://python.org/downloads/
echo    2. Durante la instalación, marque "Add Python to PATH"
echo    3. Ejecute este script nuevamente
echo.
echo 📥 ¿Abrir página de descarga? (s/n)
set /p open_download="Respuesta: "
if /i "%open_download%"=="s" (
    start https://python.org/downloads/
)
echo.
pause
exit /b 1

:python_ok
echo.
echo ✅ Python detectado correctamente
echo    Comando: %PYTHON_CMD%
echo.

echo 🔧 Creando entorno virtual...
if exist "venv" (
    echo    ℹ️  Entorno virtual ya existe
) else (
    echo    📦 Creando nuevo entorno virtual...
    "%PYTHON_CMD%" -m venv venv
    if errorlevel 1 (
        echo    ❌ Error al crear entorno virtual
        echo    💡 Intente ejecutar como administrador
        pause
        exit /b 1
    )
    echo    ✅ Entorno virtual creado
)

echo.
echo 📦 Instalando dependencias en el entorno virtual...
if exist "venv\Scripts\python.exe" (
    echo    🔄 Actualizando pip...
    venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
    
    echo    📋 Instalando desde requirements.txt...
    if exist "requirements.txt" (
        venv\Scripts\python.exe -m pip install -r requirements.txt
        if errorlevel 1 (
            echo    ⚠️  Error con requirements.txt, instalando dependencias básicas...
            venv\Scripts\python.exe -m pip install PyQt5 reportlab Pillow python-dateutil
        )
    ) else (
        echo    📦 Instalando dependencias básicas...
        venv\Scripts\python.exe -m pip install PyQt5 reportlab Pillow python-dateutil
    )
    
    if errorlevel 1 (
        echo    ❌ Error al instalar dependencias
        echo    💡 Verifique su conexión a internet
        pause
        exit /b 1
    )
    
    echo    ✅ Dependencias instaladas
) else (
    echo    ❌ Error: Python del entorno virtual no encontrado
    pause
    exit /b 1
)

echo.
echo 🧪 Verificando instalación...
venv\Scripts\python.exe -c "import PyQt5; print('✅ PyQt5 OK')" 2>nul
if errorlevel 1 (
    echo    ❌ PyQt5 no funciona correctamente
    echo    🔄 Intentando reinstalación...
    venv\Scripts\python.exe -m pip install --force-reinstall PyQt5
) else (
    echo    ✅ PyQt5 funciona correctamente
)

echo.
echo 🎯 Creando iconos de acceso...
if exist "crear_iconos_personalizados.bat" (
    call crear_iconos_personalizados.bat >nul 2>&1
    echo    ✅ Iconos creados
) else (
    echo    ⚠️  Script de iconos no encontrado
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎉 INSTALACIÓN COMPLETADA                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Facturación Fácil está listo para usar
echo.
echo 🚀 Para lanzar la aplicación:
echo    • Doble clic en: 🚀 Lanzar Facturación Fácil.lnk
echo    • O ejecute: lancer_app.bat
echo    • O ejecute: lancer_rapide.bat
echo.
echo 🔧 Para diagnóstico:
echo    • Ejecute: test_entorno_virtual.bat
echo    • Ejecute: diagnostico_completo.bat
echo.
echo 🎯 ¡Instalación exitosa!
pause
