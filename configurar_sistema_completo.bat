@echo off
chcp 65001 >nul
title Configuración Completa del Sistema - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 CONFIGURACIÓN COMPLETA DEL SISTEMA                    ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🎯 Este script configurará completamente su sistema con:
echo.
echo    ✅ Instalación automática de Python (si es necesario)
echo    ✅ Configuración del entorno virtual
echo    ✅ Instalación de todas las dependencias
echo    ✅ Creación de iconos de acceso directo
echo    ✅ Configuración de Git (si es necesario)
echo    ✅ Scripts de mantenimiento
echo.

set /p continue="¿Desea continuar con la configuración completa? (S/N): "
if /i not "%continue%"=="S" (
    echo ❌ Configuración cancelada
    pause
    exit /b 0
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    PASO 1: INSTALACIÓN DE LA APLICACIÓN                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Ejecutando instalación completa...
call instalar_app.bat
if errorlevel 1 (
    echo ❌ Error en la instalación
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    PASO 2: CREACIÓN DE ICONOS PERSONALIZADOS               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🎨 Creando iconos personalizados...
call crear_iconos_personalizados.bat

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    PASO 3: CONFIGURACIÓN DE GIT                            ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando configuración de Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Git no está instalado
    set /p install_git="¿Desea instalar Git para actualizaciones automáticas? (S/N): "
    if /i "%install_git%"=="S" (
        echo 📥 Instalando Git...
        call :install_git_simple
    )
) else (
    echo ✅ Git ya está instalado
    git --version
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    PASO 4: VERIFICACIÓN FINAL                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🧪 Verificando que todo funciona correctamente...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no funciona
) else (
    echo ✅ Python: OK
)

REM Verificar entorno virtual
if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual: OK
) else (
    echo ❌ Entorno virtual: Error
)

REM Verificar PyQt5
call venv\Scripts\activate.bat >nul 2>&1
python -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5: OK')" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5: Error
) else (
    echo ✅ PyQt5: OK
)

REM Verificar iconos
if exist "🚀 Lanzar Facturación Fácil.lnk" (
    echo ✅ Iconos: Creados
) else (
    echo ❌ Iconos: No encontrados
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎉 CONFIGURACIÓN COMPLETADA                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo ✅ SISTEMA COMPLETAMENTE CONFIGURADO
echo.
echo 📋 Componentes instalados:
echo    • Python + entorno virtual
echo    • PyQt5 + dependencias
echo    • Iconos de acceso directo
echo    • Scripts de mantenimiento
if exist "git.exe" echo    • Git para actualizaciones
echo.
echo 🚀 ICONOS DISPONIBLES:
echo    🚀 Lanzar Facturación Fácil.lnk    - Ejecutar aplicación
echo    🔄 Actualizar desde Git.lnk        - Actualizar código
echo    🗑️ Desinstalar Aplicación.lnk      - Desinstalar
echo    🔧 Reinstalar Aplicación.lnk       - Reinstalar
echo    📊 Abrir Base de Datos.lnk         - Ver base de datos
echo    📄 Ver PDFs Generados.lnk          - Ver facturas PDF
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Haga doble clic en "🚀 Lanzar Facturación Fácil.lnk"
echo    2. Configure su organización en la aplicación
echo    3. ¡Comience a crear facturas!
echo.
echo 🔄 MANTENIMIENTO:
echo    • Use "🔄 Actualizar desde Git.lnk" para actualizaciones
echo    • Use "🗑️ Desinstalar Aplicación.lnk" para desinstalar
echo.

pause
goto :eof

:install_git_simple
echo 📥 Descargando Git...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git_installer.exe'}"
if exist "git_installer.exe" (
    echo 🔧 Instalando Git...
    git_installer.exe /VERYSILENT /NORESTART
    del git_installer.exe
    echo ✅ Git instalado
) else (
    echo ❌ Error al descargar Git
)
goto :eof
