@echo off
chcp 65001 >nul
setlocal

:: ============================================================================
:: CREAR TODOS LOS ACCESOS DIRECTOS - Facturación Fácil
:: ============================================================================

color 0E
title 🔗 Crear Todos los Accesos Directos

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║         🔗 CREAR TODOS LOS ACCESOS DIRECTOS                       ║
echo ║              FACTURACIÓN FÁCIL                                     ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:: Obtener la ruta actual
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo 📁 Directorio: %SCRIPT_DIR%
echo.
echo 🔨 Creando accesos directos...
echo.

:: Crear script VBS temporal
set "VBS_FILE=%TEMP%\CreateShortcuts.vbs"

:: ============================================================================
:: 1. Acceso directo para INICIAR la aplicación
:: ============================================================================
echo [1/5] 🚀 Iniciar Aplicación...

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%SCRIPT_DIR%\Iniciar Facturacion.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%SCRIPT_DIR%\start.bat" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "Iniciar Facturación Fácil" >> "%VBS_FILE%"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,1" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"

if exist "%SCRIPT_DIR%\Iniciar Facturacion.lnk" (
    echo    ✅ Creado: Iniciar Facturacion.lnk
) else (
    echo    ❌ Error al crear el acceso directo
)

:: ============================================================================
:: 2. Acceso directo para CREAR BACKUP
:: ============================================================================
echo [2/5] 💾 Crear Backup...

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%SCRIPT_DIR%\Crear Backup.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%SCRIPT_DIR%\crear_backup.bat" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "Crear backup de la base de datos" >> "%VBS_FILE%"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,98" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"

if exist "%SCRIPT_DIR%\Crear Backup.lnk" (
    echo    ✅ Creado: Crear Backup.lnk
) else (
    echo    ❌ Error al crear el acceso directo
)

:: ============================================================================
:: 3. Acceso directo para RESTAURAR BACKUP
:: ============================================================================
echo [3/5] 🔄 Restaurar Backup...

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%SCRIPT_DIR%\Restaurar Backup.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%SCRIPT_DIR%\restablecer.bat" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "Restaurar base de datos desde backups" >> "%VBS_FILE%"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,109" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"

if exist "%SCRIPT_DIR%\Restaurar Backup.lnk" (
    echo    ✅ Creado: Restaurar Backup.lnk
) else (
    echo    ❌ Error al crear el acceso directo
)

:: ============================================================================
:: 4. Acceso directo para CARPETA DE BACKUPS
:: ============================================================================
echo [4/5] 📁 Carpeta de Backups...

:: Crear carpeta de backups si no existe
if not exist "%SCRIPT_DIR%\base_de_datos\backups" mkdir "%SCRIPT_DIR%\base_de_datos\backups"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%SCRIPT_DIR%\Ver Backups.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%SCRIPT_DIR%\base_de_datos\backups" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%\base_de_datos\backups" >> "%VBS_FILE%"
echo oLink.Description = "Abrir carpeta de backups" >> "%VBS_FILE%"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,3" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"

if exist "%SCRIPT_DIR%\Ver Backups.lnk" (
    echo    ✅ Creado: Ver Backups.lnk
) else (
    echo    ❌ Error al crear el acceso directo
)

:: ============================================================================
:: 5. Acceso directo para LIMPIAR BACKUPS
:: ============================================================================
echo [5/5] 🧹 Limpiar Backups...

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%SCRIPT_DIR%\Limpiar Backups.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%SCRIPT_DIR%\limpiar_backups.bat" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "Limpiar backups antiguos" >> "%VBS_FILE%"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,54" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"

if exist "%SCRIPT_DIR%\Limpiar Backups.lnk" (
    echo    ✅ Creado: Limpiar Backups.lnk
) else (
    echo    ❌ Error al crear el acceso directo
)

:: Limpiar archivo temporal
del "%VBS_FILE%" 2>nul

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                  ✅ ACCESOS DIRECTOS CREADOS                       ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📂 Los siguientes accesos directos están disponibles:
echo.
echo    • Iniciar Facturacion.lnk    - Iniciar la aplicación
echo    • Crear Backup.lnk            - Crear backup manual
echo    • Restaurar Backup.lnk        - Restaurar desde backup
echo    • Ver Backups.lnk             - Abrir carpeta de backups
echo    • Limpiar Backups.lnk         - Limpiar backups antiguos
echo.
echo 💡 Puedes copiar estos accesos directos a:
echo    • Escritorio
echo    • Cualquier carpeta
echo    • Barra de tareas (arrastrando)
echo.
pause

