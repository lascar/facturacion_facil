@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================================================
:: LIMPIAR BACKUPS ANTIGUOS - Facturación Fácil
:: ============================================================================

color 0C
title 🧹 Limpiar Backups Antiguos

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║           🧹 LIMPIAR BACKUPS ANTIGUOS                             ║
echo ║              FACTURACIÓN FÁCIL                                     ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:: Verificar si existe el directorio de backups
if not exist "base_de_datos\backups" (
    echo ❌ ERROR: No se encontró el directorio de backups
    echo.
    pause
    exit /b 1
)

:: Contar backups totales
set total=0
for %%f in (base_de_datos\backups\*.db) do set /a total+=1

echo 📊 Backups actuales: %total%
echo.

if %total% LEQ 10 (
    echo ✅ Tienes %total% backups. No es necesario limpiar.
    echo.
    echo 💡 Se recomienda limpiar cuando tienes más de 10 backups
    echo.
    pause
    exit /b 0
)

echo ⚠️  ADVERTENCIA: Tienes %total% backups
echo.
echo 💡 Opciones de limpieza:
echo.
echo    [1] Mantener los últimos 10 backups (eliminar %total% menos 10)
echo    [2] Mantener los últimos 20 backups
echo    [3] Mantener los últimos 30 backups
echo    [4] Eliminar backups con nombre específico
echo    [0] Cancelar
echo.

set /p choice="👉 Selecciona una opción (0-4): "

if "%choice%"=="0" (
    echo.
    echo ℹ️  Operación cancelada
    echo.
    pause
    exit /b 0
)

if "%choice%"=="1" set keep=10
if "%choice%"=="2" set keep=20
if "%choice%"=="3" set keep=30

if "%choice%"=="4" (
    echo.
    echo 🔍 Patrones comunes:
    echo    • backup_add_talla_column_*
    echo    • backup_productos_without_stock_migration_*
    echo    • backup_test_*
    echo.
    set /p pattern="👉 Introduce el patrón a eliminar (ej: backup_test_*): "
    
    echo.
    echo ⚠️  Se eliminarán todos los archivos que coincidan con: !pattern!
    echo.
    set /p confirm="¿Estás seguro? (S/N): "
    
    if /i not "!confirm!"=="S" (
        echo.
        echo ℹ️  Operación cancelada
        echo.
        pause
        exit /b 0
    )
    
    echo.
    echo 🧹 Eliminando backups con patrón: !pattern!
    
    set deleted=0
    for %%f in (base_de_datos\backups\!pattern!.db) do (
        del "%%f" 2>nul
        if not errorlevel 1 (
            set /a deleted+=1
            echo    ✅ Eliminado: %%~nxf
        )
    )
    
    echo.
    echo ✅ Eliminados: !deleted! backups
    
    :: Contar backups restantes
    set remaining=0
    for %%f in (base_de_datos\backups\*.db) do set /a remaining+=1
    echo 📊 Backups restantes: !remaining!
    echo.
    pause
    exit /b 0
)

:: Validar opción
if not defined keep (
    echo.
    echo ❌ ERROR: Opción inválida
    pause
    exit /b 1
)

echo.
echo ⚠️  Se mantendrán los últimos %keep% backups
echo    Se eliminarán aproximadamente %total% menos %keep% backups
echo.
set /p confirm="¿Estás seguro de continuar? (S/N): "

if /i not "%confirm%"=="S" (
    echo.
    echo ℹ️  Operación cancelada
    echo.
    pause
    exit /b 0
)

echo.
echo 🧹 Limpiando backups antiguos...
echo.

:: Crear lista temporal de backups ordenados por fecha (más recientes primero)
set "temp_list=%TEMP%\backup_list.txt"
dir /b /o-d base_de_datos\backups\*.db > "%temp_list%"

:: Contar y eliminar
set index=0
set deleted=0

for /f "tokens=*" %%f in (%temp_list%) do (
    set /a index+=1
    
    if !index! GTR %keep% (
        del "base_de_datos\backups\%%f" 2>nul
        if not errorlevel 1 (
            set /a deleted+=1
            echo    ✅ Eliminado: %%f
        )
    )
)

:: Limpiar archivo temporal
del "%temp_list%" 2>nul

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ LIMPIEZA COMPLETADA                          ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📊 Backups eliminados: %deleted%
echo 📊 Backups conservados: %keep%
echo.
pause

