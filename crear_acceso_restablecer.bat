@echo off
chcp 65001 >nul
setlocal

:: ============================================================================
:: CREAR ACCESO DIRECTO PARA RESTABLECER.BAT
:: ============================================================================

color 0E
title 🔗 Crear Acceso Directo - Restaurar Backups

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║           🔗 CREAR ACCESO DIRECTO - RESTAURAR BACKUPS             ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:: Obtener la ruta actual
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Crear el script VBS temporal
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%SCRIPT_DIR%\🔄 Restaurar Backups.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%\restablecer.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Restaurar base de datos desde backups" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,109" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

:: Ejecutar el script VBS
cscript //nologo "%TEMP%\CreateShortcut.vbs"

:: Limpiar
del "%TEMP%\CreateShortcut.vbs"

if exist "%SCRIPT_DIR%\🔄 Restaurar Backups.lnk" (
    echo ✅ Acceso directo creado exitosamente:
    echo.
    echo    📁 Ubicación: %SCRIPT_DIR%
    echo    📄 Nombre: 🔄 Restaurar Backups.lnk
    echo.
    echo 💡 Puedes copiar este acceso directo a:
    echo    • Escritorio
    echo    • Cualquier otra carpeta
    echo    • Barra de tareas (arrastrando el archivo)
    echo.
) else (
    echo ❌ ERROR: No se pudo crear el acceso directo
    echo.
)

pause

