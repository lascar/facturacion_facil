@echo off
chcp 65001 >nul
title Diagnóstico Git - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🔍 DIAGNÓSTICO GIT - FACTURACIÓN FÁCIL         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📍 Directorio actual:
echo    %CD%
echo.

:: Verificar Git
echo ═══════════════════════════════════════════════════════════════
echo 1. VERIFICACIÓN DE GIT
echo ═══════════════════════════════════════════════════════════════
echo.

git --version 2>nul
if errorlevel 1 (
    echo ❌ Git NO está instalado o no está en PATH
    echo.
    echo 💡 Instalar desde: https://git-scm.com/download/win
    goto :END
) else (
    echo ✅ Git está instalado
)
echo.

:: Información del repositorio
echo ═══════════════════════════════════════════════════════════════
echo 2. INFORMACIÓN DEL REPOSITORIO
echo ═══════════════════════════════════════════════════════════════
echo.

echo 📋 Rama actual:
git branch --show-current 2>nul || echo "   ❌ No se pudo detectar"
echo.

echo 📋 Todas las ramas locales:
git branch 2>nul || echo "   ❌ No se pudo listar"
echo.

echo 📋 Ramas remotas:
git branch -r 2>nul || echo "   ❌ No se pudo listar"
echo.

echo 📋 Configuración remota:
git remote -v 2>nul || echo "   ❌ No se pudo obtener"
echo.

:: Estado del repositorio
echo ═══════════════════════════════════════════════════════════════
echo 3. ESTADO DEL REPOSITORIO
echo ═══════════════════════════════════════════════════════════════
echo.

echo 📋 Estado de archivos:
git status --short 2>nul
if errorlevel 1 (
    echo    ❌ No se pudo obtener estado
) else (
    if "%errorlevel%"=="0" (
        echo    ✅ No hay cambios pendientes
    )
)
echo.

echo 📋 Últimos 5 commits:
git log --oneline -5 2>nul || echo "   ❌ No se pudo obtener historial"
echo.

:: Verificar conexión
echo ═══════════════════════════════════════════════════════════════
echo 4. VERIFICACIÓN DE CONEXIÓN
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🌐 Probando conexión a GitHub...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo ❌ Sin conexión a GitHub
) else (
    echo ✅ Conexión a GitHub OK
)
echo.

echo 🔄 Probando fetch desde remoto...
git fetch origin --dry-run 2>nul
if errorlevel 1 (
    echo ❌ No se puede conectar al repositorio remoto
) else (
    echo ✅ Conexión al repositorio remoto OK
)
echo.

:: Verificar actualizaciones disponibles
echo ═══════════════════════════════════════════════════════════════
echo 5. ACTUALIZACIONES DISPONIBLES
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🔍 Obteniendo información del remoto...
git fetch origin >nul 2>&1

for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "RAMA=%%i"
if "%RAMA%"=="" set "RAMA=master"

echo 📋 Comparando rama local '%RAMA%' con remoto...
git rev-list HEAD..origin/%RAMA% --count 2>nul >temp_count.txt
set /p COMMITS_PENDIENTES=<temp_count.txt
del temp_count.txt 2>nul

if "%COMMITS_PENDIENTES%"=="0" (
    echo ✅ Repositorio local está actualizado
) else if "%COMMITS_PENDIENTES%"=="" (
    echo ⚠️  No se pudo comparar (rama remota no encontrada?)
) else (
    echo ⚠️  Hay %COMMITS_PENDIENTES% commits pendientes de actualizar
)
echo.

:: Verificar archivos críticos
echo ═══════════════════════════════════════════════════════════════
echo 6. VERIFICACIÓN DE ARCHIVOS CRÍTICOS
echo ═══════════════════════════════════════════════════════════════
echo.

if exist "main.py" (echo ✅ main.py) else (echo ❌ main.py NO ENCONTRADO)
if exist "requirements.txt" (echo ✅ requirements.txt) else (echo ⚠️  requirements.txt no encontrado)
if exist "facturacion.db" (echo ✅ facturacion.db) else (echo ⚠️  facturacion.db no encontrado)
if exist "database\database.py" (echo ✅ database\database.py) else (echo ❌ database\database.py NO ENCONTRADO)
if exist "ui\main_window.py" (echo ✅ ui\main_window.py) else (echo ❌ ui\main_window.py NO ENCONTRADO)
echo.

:: Resumen
echo ═══════════════════════════════════════════════════════════════
echo 7. RESUMEN Y RECOMENDACIONES
echo ═══════════════════════════════════════════════════════════════
echo.

echo 💡 Si hay problemas con actualizar.bat:
echo.
echo    1. Verificar que Git esté instalado y en PATH
echo    2. Verificar conexión a internet
echo    3. Verificar que no haya cambios locales sin guardar
echo    4. Intentar: git pull origin master
echo    5. Si persiste, contactar soporte técnico
echo.

:END
echo ═══════════════════════════════════════════════════════════════
echo.
echo Presione cualquier tecla para salir...
pause >nul

