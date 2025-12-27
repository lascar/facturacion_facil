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

echo 🔍 DEBUG: Información del sistema
echo    SCRIPT_DIR: %SCRIPT_DIR%
echo    TEMP: %TEMP%
echo.

:: Verificar que existe restablecer.bat
if exist "%SCRIPT_DIR%\restablecer.bat" (
    echo ✅ DEBUG: restablecer.bat encontrado
) else (
    echo ❌ DEBUG: restablecer.bat NO encontrado en %SCRIPT_DIR%
    pause
    exit /b 1
)

echo.
echo 📝 DEBUG: Creando script VBS temporal...

:: Crear el script VBS temporal
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%SCRIPT_DIR%\Restaurar Backups.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%\restablecer.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Restaurar base de datos desde backups" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,109" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

if exist "%TEMP%\CreateShortcut.vbs" (
    echo ✅ DEBUG: Script VBS creado en %TEMP%\CreateShortcut.vbs
    echo.
    echo 📄 DEBUG: Contenido del script VBS:
    type "%TEMP%\CreateShortcut.vbs"
    echo.
) else (
    echo ❌ DEBUG: No se pudo crear el script VBS
    pause
    exit /b 1
)

echo.
echo 🚀 DEBUG: Ejecutando script VBS...
echo.

:: Ejecutar el script VBS
cscript //nologo "%TEMP%\CreateShortcut.vbs"

set VBS_ERROR=%ERRORLEVEL%
echo.
echo 📊 DEBUG: Código de salida de cscript: %VBS_ERROR%
echo.

:: Limpiar
del "%TEMP%\CreateShortcut.vbs"

echo 🔍 DEBUG: Verificando si se creó el acceso directo...
echo    Buscando: %SCRIPT_DIR%\Restaurar Backups.lnk
echo.

if exist "%SCRIPT_DIR%\Restaurar Backups.lnk" (
    echo ✅ Acceso directo creado exitosamente:
    echo.
    echo    📁 Ubicación: %SCRIPT_DIR%
    echo    📄 Nombre: Restaurar Backups.lnk
    echo.

    :: Mostrar propiedades del archivo
    dir "%SCRIPT_DIR%\Restaurar Backups.lnk"
    echo.

    echo 💡 Puedes copiar este acceso directo a:
    echo    • Escritorio
    echo    • Cualquier otra carpeta
    echo    • Barra de tareas (arrastrando el archivo)
    echo.
) else (
    echo ❌ ERROR: No se pudo crear el acceso directo
    echo.
    echo 🔍 DEBUG: Listando archivos .lnk en el directorio:
    dir /b "%SCRIPT_DIR%\*.lnk" 2>nul
    if errorlevel 1 (
        echo    (No hay archivos .lnk en el directorio)
    )
    echo.
    echo 💡 Posibles causas:
    echo    1. Permisos insuficientes en el directorio
    echo    2. Nombre de archivo con caracteres especiales
    echo    3. Error en la ejecución del script VBS
    echo    4. Antivirus bloqueando la creación
    echo.
)

pause

