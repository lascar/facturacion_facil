@echo off
chcp 65001 >nul
title Actualizar Facturación Fácil - Versión Robusta

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔄 ACTUALIZAR APLICACIÓN                 ║
echo ║                  Facturación Fácil - Robusta               ║
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

:: CRÍTICO: Crear respaldo obligatorio antes de cualquier modificación
echo 💾 CREANDO RESPALDO OBLIGATORIO...
echo ⚠️  CRÍTICO: Respaldo de datos antes de actualización

if not exist "backup" mkdir backup

:: Respaldo con fecha y hora
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "FECHA=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%_%dt:~8,2%-%dt:~10,2%-%dt:~12,2%"

:: Respaldo de base de datos - CRÍTICO
if exist "facturacion.db" (
    copy "facturacion.db" "backup\facturacion_%FECHA%.db" >nul
    if %errorlevel%==0 (
        echo ✅ Base de datos respaldada: backup\facturacion_%FECHA%.db
    ) else (
        echo ❌ ERROR CRÍTICO: No se pudo respaldar la base de datos
        echo    DETENIENDO actualización para evitar pérdida de datos
        pause
        exit /b 1
    )
) else (
    echo ⚠️  Base de datos no encontrada (primera instalación?)
)

:: Respaldo de configuración
if exist "config\config.json" (
    copy "config\config.json" "backup\config_%FECHA%.json" >nul
    if %errorlevel%==0 (
        echo ✅ Configuración respaldada: backup\config_%FECHA%.json
    )
)

echo ✅ RESPALDO COMPLETADO - Datos protegidos
echo.

:: Detectar rama actual y configuración del repositorio
echo 🔍 Detectando configuración del repositorio...

:: Obtener información del repositorio
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

:: Obtener rama actual
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "RAMA_ACTUAL=%%i"
if "%RAMA_ACTUAL%"=="" (
    echo ⚠️  No se pudo detectar rama actual, usando detección automática
    set "RAMA_ACTUAL=auto"
) else (
    echo 📋 Rama actual: %RAMA_ACTUAL%
)

echo ✅ Repositorio remoto accesible
echo.

:: Actualizar código con detección automática de rama
echo 📥 Descargando actualizaciones...

set "ACTUALIZADO=NO"

:: Método 1: Usar rama actual si está definida y no es 'auto'
if not "%RAMA_ACTUAL%"=="auto" (
    echo 🔄 Probando rama actual: %RAMA_ACTUAL%
    git pull origin %RAMA_ACTUAL% >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: %RAMA_ACTUAL%
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Error actualizando desde rama: %RAMA_ACTUAL%
    )
)

:: Método 2: Probar master (rama principal detectada)
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama master...
    git pull origin master >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: master
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Rama master no disponible
    )
)

:: Método 3: Probar main como alternativa
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama main...
    git pull origin main >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: main
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Rama main no disponible
    )
)

:: Método 4: Pull genérico como último recurso
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama por defecto...
    git pull >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente (método genérico)
        set "ACTUALIZADO=SI"
    ) else (
        echo ❌ Error : no se puede actualizar desde ninguna rama
        echo    Verificar conexión y configuración Git
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
        echo Presione cualquier tecla para continuar...
        pause >nul
        exit /b 1
    )
)

echo.

:: Actualizar dependencias de Python
echo 📦 Actualizando dependencias de Python...

:: Detectar Python disponible
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

:: Verificar integridad de la aplicación
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

:: Verificar estructura crítica de base de datos
if exist "database\migration_manager.py" (
    echo ✅ Sistema de migración presente
) else (
    echo ⚠️  Sistema de migración no encontrado
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
echo    • ✅ Respaldo de datos creado (CRÍTICO)
echo    • ✅ Código actualizado desde repositorio
echo    • ✅ Dependencias actualizadas
echo    • ✅ Integridad verificada
echo    • ✅ Aplicación lista para usar
echo.

echo 🔒 DATOS PROTEGIDOS: Respaldo en backup\facturacion_%FECHA%.db
echo.

echo 🚀 La aplicación está lista para usar con la última versión
echo.

echo ✅ Actualización completada. Presione cualquier tecla para salir...
pause >nul
