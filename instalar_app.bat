@echo off
chcp 65001 >nul
title Instalación Completa - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 INSTALACIÓN AUTOMÁTICA COMPLETA                       ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando requisitos del sistema...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo.
    echo 🔍 Buscando Python en ubicaciones comunes...

    REM Buscar Python en ubicaciones típicas
    set "PYTHON_FOUND="
    for %%p in (
        "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
        "%PROGRAMFILES%\Python*\python.exe"
        "%PROGRAMFILES(X86)%\Python*\python.exe"
        "C:\Python*\python.exe"
    ) do (
        if exist "%%p" (
            set "PYTHON_FOUND=%%p"
            goto :python_found
        )
    )

    :python_not_found
    echo ❌ Python no encontrado en el sistema
    echo.
    echo 📥 Opciones de instalación:
    echo    1. Instalación automática (recomendado)
    echo    2. Instalación manual
    echo.
    set /p install_option="Seleccione opción (1/2): "

    if "%install_option%"=="1" (
        echo 🚀 Iniciando instalación automática de Python...
        call :install_python_auto
    ) else (
        echo 📥 Abriendo página de descarga de Python...
        start https://www.python.org/downloads/
        echo.
        echo ⚠️  Por favor:
        echo    1. Descargue Python 3.8 o superior
        echo    2. Durante la instalación, marque "Add Python to PATH"
        echo    3. Ejecute este script nuevamente después de la instalación
        echo.
        pause
        exit /b 1
    )

    :python_found
    echo ✅ Python encontrado en: %PYTHON_FOUND%
    set "PYTHON_CMD=%PYTHON_FOUND%"
) else (
    set "PYTHON_CMD=python"
)

echo ✅ Python detectado:
%PYTHON_CMD% --version

REM Verificar pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está disponible
    echo 📥 Instalando pip...
    python -m ensurepip --upgrade
)

echo ✅ pip disponible:
pip --version

echo.
echo 🔧 Configurando entorno virtual...

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error al crear el entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ℹ️  Entorno virtual ya existe
)

REM Activar entorno virtual
echo 🔌 Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar el entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado

echo.
echo 📦 Instalando dependencias...

REM Actualizar pip
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias desde requirements.txt
if exist "requirements.txt" (
    echo 📋 Instalando desde requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        echo 🔄 Intentando instalación individual...
        
        echo 📦 Instalando PyQt5...
        pip install PyQt5
        
        echo 📦 Instalando reportlab...
        pip install reportlab
        
        echo 📦 Instalando Pillow...
        pip install Pillow
        
        echo 📦 Instalando python-dateutil...
        pip install python-dateutil
    )
) else (
    echo 📦 Instalando dependencias básicas...
    pip install PyQt5 reportlab Pillow python-dateutil
)

echo.
echo 🧪 Verificando instalación...

REM Verificar que PyQt5 funciona
python -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 OK')" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 no funciona correctamente
    echo 🔄 Reinstalando PyQt5...
    pip uninstall -y PyQt5
    pip install PyQt5
)

echo.
echo 🎯 Creando accesos directos...
call crear_iconos_acceso.bat

echo.
echo ✅ INSTALACIÓN COMPLETADA
echo.
echo 📋 Resumen:
echo    • Python: Verificado
echo    • Entorno virtual: Configurado
echo    • Dependencias: Instaladas
echo    • Accesos directos: Creados
echo.
echo 🚀 Para ejecutar la aplicación:
echo    • Doble clic en "🚀 Lanzar App.lnk"
echo    • O ejecute: lancer_app.bat
echo.

pause
goto :eof

:install_python_auto
echo 📥 Descargando Python 3.11 (versión estable recomendada)...
echo.

REM Crear directorio temporal
if not exist "temp_install" mkdir temp_install
cd temp_install

REM Descargar Python usando PowerShell
echo 🌐 Descargando instalador de Python...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist "python_installer.exe" (
    echo ❌ Error al descargar Python
    echo 🔄 Intentando descarga alternativa...
    powershell -Command "& {(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe', 'python_installer.exe')}"
)

if exist "python_installer.exe" (
    echo ✅ Descarga completada
    echo 🔧 Instalando Python...
    echo    (Esto puede tomar unos minutos)

    REM Instalar Python silenciosamente con PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo ✅ Instalación de Python completada
    echo 🔄 Actualizando variables de entorno...

    REM Actualizar PATH en la sesión actual
    call refreshenv 2>nul

    REM Limpiar archivos temporales
    cd ..
    rmdir /s /q temp_install 2>nul

    echo ✅ Python instalado correctamente
    echo 🔄 Reiniciando verificación...

    REM Verificar instalación
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Python instalado pero no disponible en PATH
        echo    Reinicie el script o la terminal
        pause
        exit /b 1
    )
) else (
    echo ❌ No se pudo descargar Python
    echo 📥 Abriendo página de descarga manual...
    start https://www.python.org/downloads/
    cd ..
    rmdir /s /q temp_install 2>nul
    pause
    exit /b 1
)

cd ..
rmdir /s /q temp_install 2>nul
goto :eof
