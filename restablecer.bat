@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================================================
:: SCRIPT DE RESTAURACIÓN DE BACKUPS - Facturación Fácil
:: ============================================================================

color 0B
title 🔄 Restaurar Base de Datos - Facturación Fácil

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║        🔄 RESTAURAR BASE DE DATOS - FACTURACIÓN FÁCIL             ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:: Verificar si existe el directorio de backups
if not exist "base_de_datos\backups" (
    echo ❌ ERROR: No se encontró el directorio de backups
    echo.
    echo 💡 Creando directorio de backups...
    mkdir base_de_datos\backups
    echo ✅ Directorio creado
    echo.
    echo ⚠️  No hay backups disponibles todavía
    echo.
    pause
    exit /b 1
)

:: Contar backups disponibles
set count=0
for %%f in (base_de_datos\backups\*.db) do set /a count+=1

if %count%==0 (
    echo ⚠️  No hay backups disponibles en el directorio 'base_de_datos\backups'
    echo.
    echo 💡 Los backups se crean automáticamente cuando usas la aplicación
    echo    o puedes crearlos manualmente con crear_backup.bat
    echo.
    pause
    exit /b 1
)

:: Listar backups disponibles
echo 📋 Backups disponibles (%count% encontrados):
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

set index=0
for /f "tokens=*" %%f in ('dir /b /o-d base_de_datos\backups\*.db') do (
    set /a index+=1
    set "backup[!index!]=%%f"

    :: Obtener tamaño del archivo
    for %%a in ("base_de_datos\backups\%%f") do set size=%%~za
    set /a sizekb=!size!/1024
    
    :: Obtener fecha de modificación
    for %%a in ("backups\%%f") do set fecha=%%~ta
    
    echo [!index!] %%f
    echo     📅 Fecha: !fecha!
    echo     💾 Tamaño: !sizekb! KB
    echo.
)

echo ════════════════════════════════════════════════════════════════════
echo.
echo [0] ❌ Cancelar y salir
echo.

:: Solicitar selección
set /p choice="👉 Selecciona el número del backup a restaurar (0-%index%): "

:: Validar entrada
if "%choice%"=="0" (
    echo.
    echo ℹ️  Operación cancelada
    echo.
    pause
    exit /b 0
)

if %choice% LSS 1 (
    echo.
    echo ❌ ERROR: Selección inválida
    pause
    exit /b 1
)

if %choice% GTR %index% (
    echo.
    echo ❌ ERROR: Selección inválida
    pause
    exit /b 1
)

:: Obtener el archivo seleccionado
set "selected=!backup[%choice%]!"

echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo 📦 Backup seleccionado: !selected!
echo.
echo ⚠️  ADVERTENCIA: Esta operación reemplazará la base de datos actual
echo.
set /p confirm="¿Estás seguro de continuar? (S/N): "

if /i not "%confirm%"=="S" (
    echo.
    echo ℹ️  Operación cancelada
    echo.
    pause
    exit /b 0
)

:: Crear backup de seguridad de la base actual antes de restaurar
echo.
echo 💾 Creando backup de seguridad de la base actual...

if exist "base_de_datos\facturacion.db" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c%%b%%a
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
    set mytime=!mytime::=!

    copy "base_de_datos\facturacion.db" "base_de_datos\backups\antes_restaurar_!mydate!_!mytime!.db" >nul
    
    if errorlevel 1 (
        echo ❌ ERROR: No se pudo crear el backup de seguridad
        pause
        exit /b 1
    )
    
    echo ✅ Backup de seguridad creado: antes_restaurar_!mydate!_!mytime!.db
)

:: Restaurar el backup seleccionado
echo.
echo 🔄 Restaurando backup...

copy "base_de_datos\backups\!selected!" "base_de_datos\facturacion.db" /Y >nul

if errorlevel 1 (
    echo ❌ ERROR: No se pudo restaurar el backup
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ RESTAURACIÓN EXITOSA                         ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📦 Backup restaurado: !selected!
echo 💾 Base de datos actualizada: base_de_datos\facturacion.db
echo.
echo 💡 Puedes iniciar la aplicación ahora con start.bat
echo.
pause

