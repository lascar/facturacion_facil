@echo off
chcp 65001 >nul
title Test del Sistema de Instalación - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🧪 TEST DEL SISTEMA DE INSTALACIÓN                      ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando que todos los scripts estén presentes...
echo.

set "SCRIPTS_OK=1"

REM Verificar scripts principales
if exist "configurar_sistema_completo.bat" (
    echo ✅ configurar_sistema_completo.bat
) else (
    echo ❌ configurar_sistema_completo.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "instalar_app.bat" (
    echo ✅ instalar_app.bat
) else (
    echo ❌ instalar_app.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "desinstalar_app.bat" (
    echo ✅ desinstalar_app.bat
) else (
    echo ❌ desinstalar_app.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "crear_iconos_acceso.bat" (
    echo ✅ crear_iconos_acceso.bat
) else (
    echo ❌ crear_iconos_acceso.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "crear_iconos_personalizados.bat" (
    echo ✅ crear_iconos_personalizados.bat
) else (
    echo ❌ crear_iconos_personalizados.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "actualizar_git_mejorado.bat" (
    echo ✅ actualizar_git_mejorado.bat
) else (
    echo ❌ actualizar_git_mejorado.bat - FALTANTE
    set "SCRIPTS_OK=0"
)

REM Verificar scripts existentes
if exist "lancer_app.bat" (
    echo ✅ lancer_app.bat (existente)
) else (
    echo ⚠️  lancer_app.bat - No encontrado
)

if exist "ActualizarAppMejorado.bat" (
    echo ✅ ActualizarAppMejorado.bat (existente)
) else (
    echo ⚠️  ActualizarAppMejorado.bat - No encontrado
)

echo.
echo 🔍 Verificando estructura de directorios...

if exist "assets" (
    echo ✅ Directorio assets/
    if exist "assets\icon.ico" (
        echo ✅ assets\icon.ico
    ) else (
        echo ⚠️  assets\icon.ico - No encontrado (se creará automáticamente)
    )
) else (
    echo ⚠️  Directorio assets/ - No encontrado (se creará automáticamente)
)

if exist "requirements.txt" (
    echo ✅ requirements.txt
) else (
    echo ❌ requirements.txt - FALTANTE
    set "SCRIPTS_OK=0"
)

if exist "main.py" (
    echo ✅ main.py
) else (
    echo ❌ main.py - FALTANTE
    set "SCRIPTS_OK=0"
)

echo.
echo 🔍 Verificando herramientas del sistema...

REM Verificar PowerShell
powershell -Command "Write-Host 'PowerShell OK'" >nul 2>&1
if errorlevel 1 (
    echo ❌ PowerShell - No disponible
    set "SCRIPTS_OK=0"
) else (
    echo ✅ PowerShell - Disponible
)

REM Verificar VBScript
echo WScript.Echo "VBScript OK" > test_vbs.vbs
cscript //nologo test_vbs.vbs >nul 2>&1
if errorlevel 1 (
    echo ❌ VBScript - No disponible
    set "SCRIPTS_OK=0"
) else (
    echo ✅ VBScript - Disponible
)
del test_vbs.vbs 2>nul

echo.
echo 🧪 Resultado del test:

if "%SCRIPTS_OK%"=="1" (
    echo ✅ TODOS LOS COMPONENTES ESTÁN LISTOS
    echo.
    echo 🚀 El sistema de instalación está completo y listo para usar
    echo.
    echo 📋 Para comenzar, ejecute:
    echo    configurar_sistema_completo.bat
    echo.
    echo 💡 O siga estos pasos:
    echo    1. instalar_app.bat
    echo    2. crear_iconos_personalizados.bat
    echo    3. actualizar_git_mejorado.bat (opcional)
) else (
    echo ❌ FALTAN COMPONENTES CRÍTICOS
    echo.
    echo ⚠️  El sistema no está completo. Verifique los archivos faltantes arriba.
    echo.
    echo 🔧 Asegúrese de que todos los scripts estén en el directorio correcto.
)

echo.
echo 📋 Archivos de documentación:
if exist "SISTEMA_INSTALACION_COMPLETO.md" (
    echo ✅ SISTEMA_INSTALACION_COMPLETO.md - Documentación completa
) else (
    echo ⚠️  SISTEMA_INSTALACION_COMPLETO.md - No encontrado
)

echo.
echo 🎯 Test completado
echo.

pause
