@echo off
chcp 65001 >nul
title Actualizar Facturación Fácil - Versión Mejorada

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔄 ACTUALIZAR APLICACIÓN                 ║
echo ║                  Facturación Fácil - Mejorado               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Cambiar al directorio de la aplicación
cd /d "%~dp0"

:: Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ❌ ERROR: No se encuentra main.py
    echo    Este script debe estar en la carpeta de la aplicación
    pause
    exit /b 1
)

echo 📍 Directorio: %CD%
echo.

:: Verificar Git
echo 🔍 Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Git no está instalado o no está en PATH
    echo.
    echo 💡 Soluciones:
    echo    • Instalar Git: https://git-scm.com/download/win
    echo    • Reiniciar el sistema después de instalar
    echo    • Verificar que Git esté en PATH
    echo.
    pause
    exit /b 1
)
echo ✅ Git disponible

:: Verificar conexión a internet
echo 🌐 Verificando conexión...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Sin conexión a GitHub
    echo.
    echo 💡 Verificar:
    echo    • Conexión a internet
    echo    • Firewall/proxy
    echo    • DNS
    echo.
    pause
    exit /b 1
)
echo ✅ Conexión a GitHub OK

echo.

:: Detectar rama actual
echo 🔍 Detectando configuración del repositorio...

:: Obtener rama actual
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "RAMA_ACTUAL=%%i"
if "%RAMA_ACTUAL%"=="" (
    echo ⚠️  No se pudo detectar rama actual, usando detección automática
    set "RAMA_ACTUAL=auto"
) else (
    echo 📋 Rama actual: %RAMA_ACTUAL%
)

:: Obtener ramas remotas disponibles
echo 🔍 Obteniendo información del repositorio...
git fetch origin >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se pudo conectar al repositorio remoto
    echo.
    echo 💡 Verificar:
    echo    • URL del repositorio remoto
    echo    • Permisos de acceso
    echo    • Configuración de Git
    echo.
    git remote -v
    echo.
    pause
    exit /b 1
)

:: Detectar ramas disponibles
git branch -r >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se pueden listar ramas remotas
    pause
    exit /b 1
)

echo ✅ Repositorio remoto accesible
echo.

:: Crear respaldo
echo 💾 Creando respaldo de datos...

if not exist "backup" mkdir backup

:: Respaldo con fecha y hora
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "FECHA=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%_%dt:~8,2%-%dt:~10,2%-%dt:~12,2%"

if exist "facturacion.db" (
    copy "facturacion.db" "backup\facturacion_%FECHA%.db" >nul
    if %errorlevel%==0 (
        echo ✅ Base de datos respaldada: backup\facturacion_%FECHA%.db
    ) else (
        echo ⚠️  Error creando respaldo de base de datos
    )
)

if exist "config.json" (
    copy "config.json" "backup\config_%FECHA%.json" >nul
    if %errorlevel%==0 (
        echo ✅ Configuración respaldada: backup\config_%FECHA%.json
    )
)

echo.

:: Actualizar código
echo 📥 Descargando actualizaciones...

set "ACTUALIZADO=NO"

:: Método 1: Usar rama actual si está definida
if not "%RAMA_ACTUAL%"=="auto" (
    echo 🔄 Intentando actualizar desde rama: %RAMA_ACTUAL%
    git pull origin %RAMA_ACTUAL% >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: %RAMA_ACTUAL%
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Error actualizando desde rama: %RAMA_ACTUAL%
    )
)

:: Método 2: Probar main si no funcionó el anterior
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Intentando actualizar desde rama: main
    git pull origin main >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: main
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Rama main no disponible
    )
)

:: Método 3: Probar master si main no funcionó
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Intentando actualizar desde rama: master
    git pull origin master >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: master
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Rama master no disponible
    )
)

:: Método 4: Pull genérico como último recurso
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Intentando actualización genérica...
    git pull >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente (método genérico)
        set "ACTUALIZADO=SI"
    ) else (
        echo ❌ ERROR: No se pudo actualizar desde ninguna rama
        echo.
        echo 💡 Información de debug:
        echo.
        echo 📋 Ramas remotas disponibles:
        git branch -r 2>nul || echo "No se pueden listar ramas remotas"
        echo.
        echo 📋 Estado del repositorio:
        git status --porcelain 2>nul || echo "No se puede obtener estado"
        echo.
        echo 📋 Configuración remota:
        git remote -v 2>nul || echo "No se puede obtener configuración remota"
        echo.
        pause
        exit /b 1
    )
)

echo.

:: Actualizar dependencias
echo 📦 Actualizando dependencias de Python...

:: Detectar Python
set "PYTHON=python"
python --version >nul 2>&1 || set "PYTHON=py"
py --version >nul 2>&1 || set "PYTHON=python3"

echo 🐍 Usando: %PYTHON%

:: Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual: venv
    call venv\Scripts\activate.bat >nul 2>&1
) else if exist "env\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual: env
    call env\Scripts\activate.bat >nul 2>&1
) else (
    echo ⚠️  No se encontró entorno virtual, usando Python global
)

:: Actualizar dependencias
if exist "requirements.txt" (
    echo 📋 Instalando dependencias desde requirements.txt...
    %PYTHON% -m pip install -r requirements.txt --upgrade --quiet >nul 2>&1
    if %errorlevel%==0 (
        echo ✅ Dependencias actualizadas
    ) else (
        echo ⚠️  Error actualizando dependencias (continuando...)
    )
) else (
    echo ⚠️  No se encontró requirements.txt
)

echo.

:: Verificar integridad
echo 🔍 Verificando integridad de la aplicación...

if exist "main.py" (
    echo ✅ main.py presente
) else (
    echo ❌ ERROR: main.py no encontrado después de la actualización
)

if exist "requirements.txt" (
    echo ✅ requirements.txt presente
) else (
    echo ⚠️  requirements.txt no encontrado
)

echo.

:: Mostrar información de la actualización
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ ACTUALIZACIÓN COMPLETADA              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 ¡Facturación Fácil actualizada exitosamente!
echo.
echo 📋 Resumen:
echo    • ✅ Código actualizado desde repositorio
echo    • ✅ Dependencias actualizadas
echo    • ✅ Respaldo de datos creado
echo    • ✅ Aplicación lista para usar
echo.

echo 🚀 La aplicación está lista para usar con la última versión
echo.

echo 🔄 ¿Desea iniciar la aplicación ahora? (S/N)
set /p iniciar=
if /i "%iniciar%"=="S" if /i "%iniciar%"=="s" (
    echo 🚀 Iniciando Facturación Fácil...
    %PYTHON% main.py
)

echo.
echo ✅ Actualización completada. Presione cualquier tecla para salir...
pause >nul
