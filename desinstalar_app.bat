@echo off
chcp 65001 >nul
title Desinstalación Completa - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🗑️  DESINSTALACIÓN COMPLETA                              ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  ADVERTENCIA: Esta operación eliminará TODOS los componentes de la aplicación
echo.
echo 📋 Se eliminarán:
echo    • Entorno virtual Python (venv)
echo    • Todas las dependencias instaladas
echo    • Cache de Python (__pycache__)
echo    • Logs de la aplicación
echo    • Archivos temporales
echo.
echo ⚠️  NO se eliminarán:
echo    • Base de datos (facturacion.db)
echo    • PDFs generados
echo    • Configuración (config.json)
echo    • Logos personalizados
echo.

set /p confirm="¿Está seguro de continuar? (S/N): "
if /i not "%confirm%"=="S" (
    echo ❌ Operación cancelada por el usuario
    pause
    exit /b 0
)

echo.
echo 🔄 Iniciando desinstalación...
echo.

REM Desactivar entorno virtual si está activo
if defined VIRTUAL_ENV (
    echo 📤 Desactivando entorno virtual...
    call deactivate 2>nul
)

REM Eliminar entorno virtual
if exist "venv" (
    echo 🗑️  Eliminando entorno virtual...
    rmdir /s /q "venv" 2>nul
    if exist "venv" (
        echo ⚠️  No se pudo eliminar completamente el entorno virtual
        echo    Puede que algunos archivos estén en uso
    ) else (
        echo ✅ Entorno virtual eliminado
    )
) else (
    echo ℹ️  No se encontró entorno virtual
)

REM Eliminar cache de Python
echo 🧹 Limpiando cache de Python...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d" 2>nul
    )
)

REM Eliminar archivos .pyc
echo 🧹 Eliminando archivos .pyc...
del /s /q "*.pyc" 2>nul

REM Eliminar logs (opcional)
set /p clean_logs="¿Eliminar logs de la aplicación? (S/N): "
if /i "%clean_logs%"=="S" (
    if exist "logs" (
        echo 🗑️  Eliminando logs...
        rmdir /s /q "logs" 2>nul
        echo ✅ Logs eliminados
    )
)

REM Eliminar archivos temporales
echo 🧹 Limpiando archivos temporales...
del /q "*.tmp" 2>nul
del /q "*.log" 2>nul
del /q "*.bak" 2>nul

echo.
echo ✅ DESINSTALACIÓN COMPLETADA
echo.
echo 📋 Resumen:
echo    • Entorno virtual: Eliminado
echo    • Cache Python: Limpiado
echo    • Archivos temporales: Eliminados
if /i "%clean_logs%"=="S" (
    echo    • Logs: Eliminados
) else (
    echo    • Logs: Conservados
)
echo.
echo 💾 Datos conservados:
echo    • Base de datos: facturacion.db
echo    • PDFs: carpeta pdfs/
echo    • Configuración: config/config.json
echo    • Logos: data/logos/
echo.
echo 🔄 Para reinstalar la aplicación, ejecute: instalar_app.bat
echo.

pause
