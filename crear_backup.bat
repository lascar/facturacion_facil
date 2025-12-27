@echo off
chcp 65001 >nul
setlocal

:: ============================================================================
:: CREAR BACKUP MANUAL - Facturación Fácil
:: ============================================================================

color 0A
title 💾 Crear Backup - Facturación Fácil

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║              💾 CREAR BACKUP - FACTURACIÓN FÁCIL                  ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:: Verificar si existe la base de datos
if not exist "base_de_datos\facturacion.db" (
    echo ❌ ERROR: No se encontró la base de datos
    echo.
    echo 📁 Ruta esperada: base_de_datos\facturacion.db
    echo.
    pause
    exit /b 1
)

:: Crear directorio de backups si no existe
if not exist "base_de_datos\backups" (
    echo 📁 Creando directorio de backups...
    mkdir base_de_datos\backups
    echo ✅ Directorio creado
    echo.
)

:: Obtener fecha y hora actual
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c%%b%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
set mytime=%mytime::=%
set mytime=%mytime: =0%

:: Nombre del backup
set "backup_name=backup_%mydate%_%mytime%.db"

echo 💾 Creando backup...
echo.
echo 📅 Fecha: %date%
echo 🕐 Hora: %time:~0,8%
echo 📄 Nombre: %backup_name%
echo.

:: Copiar la base de datos
copy "base_de_datos\facturacion.db" "base_de_datos\backups\%backup_name%" >nul

if errorlevel 1 (
    echo ❌ ERROR: No se pudo crear el backup
    echo.
    pause
    exit /b 1
)

:: Obtener tamaño del backup
for %%a in ("base_de_datos\backups\%backup_name%") do set size=%%~za
set /a sizekb=%size%/1024

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                      ✅ BACKUP CREADO EXITOSAMENTE                 ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📦 Archivo: base_de_datos\backups\%backup_name%
echo 💾 Tamaño: %sizekb% KB
echo.

:: Listar todos los backups
echo 📋 Backups disponibles:
echo.
dir /b /o-d base_de_datos\backups\*.db
echo.

:: Contar backups
set count=0
for %%f in (base_de_datos\backups\*.db) do set /a count+=1

echo 📊 Total de backups: %count%
echo.

:: Sugerencia de limpieza si hay muchos backups
if %count% GTR 10 (
    echo 💡 SUGERENCIA: Tienes %count% backups. Considera eliminar los más antiguos
    echo    para ahorrar espacio en disco.
    echo.
)

echo 💡 Para restaurar un backup, ejecuta: restablecer.bat
echo.
pause

