@echo off
chcp 65001 >nul
title Creación de Iconos de Acceso - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎯 CREACIÓN DE ACCESOS DIRECTOS                          ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Obtener la ruta actual
set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"

echo 📁 Directorio de la aplicación: %APP_DIR%
echo.

REM Crear script VBS para crear accesos directos
echo 🔧 Preparando creador de accesos directos...

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set fso = CreateObject^("Scripting.FileSystemObject"^)
echo.
echo ' Acceso directo para lanzar la aplicación
echo Set oShellLink = WshShell.CreateShortcut^("%APP_DIR%\🚀 Lanzar App.lnk"^)
echo oShellLink.TargetPath = "%APP_DIR%\lancer_app.bat"
echo oShellLink.WorkingDirectory = "%APP_DIR%"
echo oShellLink.Description = "Lanzar Facturación Fácil"
echo oShellLink.IconLocation = "%APP_DIR%\assets\icon.ico"
echo oShellLink.Save
echo.
echo ' Acceso directo para actualizar la aplicación
echo Set oShellLink2 = WshShell.CreateShortcut^("%APP_DIR%\🔄 Actualizar App.lnk"^)
echo oShellLink2.TargetPath = "%APP_DIR%\ActualizarAppMejorado.bat"
echo oShellLink2.WorkingDirectory = "%APP_DIR%"
echo oShellLink2.Description = "Actualizar Facturación Fácil desde Git"
echo oShellLink2.IconLocation = "%APP_DIR%\assets\icon.ico"
echo oShellLink2.Save
echo.
echo ' Acceso directo para desinstalar
echo Set oShellLink3 = WshShell.CreateShortcut^("%APP_DIR%\🗑️ Desinstalar App.lnk"^)
echo oShellLink3.TargetPath = "%APP_DIR%\desinstalar_app.bat"
echo oShellLink3.WorkingDirectory = "%APP_DIR%"
echo oShellLink3.Description = "Desinstalar Facturación Fácil"
echo oShellLink3.IconLocation = "%APP_DIR%\assets\icon.ico"
echo oShellLink3.Save
echo.
echo ' Acceso directo para reinstalar
echo Set oShellLink4 = WshShell.CreateShortcut^("%APP_DIR%\🔧 Reinstalar App.lnk"^)
echo oShellLink4.TargetPath = "%APP_DIR%\instalar_app.bat"
echo oShellLink4.WorkingDirectory = "%APP_DIR%"
echo oShellLink4.Description = "Reinstalar Facturación Fácil"
echo oShellLink4.IconLocation = "%APP_DIR%\assets\icon.ico"
echo oShellLink4.Save
echo.
echo WScript.Echo "Accesos directos creados exitosamente"
) > crear_accesos.vbs

echo 🎯 Creando accesos directos...
cscript //nologo crear_accesos.vbs

REM Limpiar archivo temporal
del crear_accesos.vbs 2>nul

echo.
echo ✅ ACCESOS DIRECTOS CREADOS
echo.
echo 📋 Accesos disponibles en el directorio de la aplicación:
echo    🚀 Lanzar App.lnk        - Ejecutar la aplicación
echo    🔄 Actualizar App.lnk    - Actualizar desde Git
echo    🗑️ Desinstalar App.lnk   - Desinstalar completamente
echo    🔧 Reinstalar App.lnk    - Reinstalar la aplicación
echo.
echo 💡 Puede mover estos accesos directos a:
echo    • Escritorio
echo    • Barra de tareas
echo    • Menú Inicio
echo    • Cualquier carpeta
echo.
echo ✨ Los accesos directos funcionarán desde cualquier ubicación
echo.

REM Preguntar si crear en el escritorio
set /p desktop="¿Crear acceso directo en el escritorio? (S/N): "
if /i "%desktop%"=="S" (
    echo 🖥️ Creando acceso en el escritorio...
    
    (
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%USERPROFILE%\Desktop\Facturación Fácil.lnk"^)
    echo oShellLink.TargetPath = "%APP_DIR%\lancer_app.bat"
    echo oShellLink.WorkingDirectory = "%APP_DIR%"
    echo oShellLink.Description = "Facturación Fácil - Sistema de Facturación"
    echo oShellLink.IconLocation = "%APP_DIR%\assets\icon.ico"
    echo oShellLink.Save
    echo WScript.Echo "Acceso directo del escritorio creado"
    ) > crear_escritorio.vbs
    
    cscript //nologo crear_escritorio.vbs
    del crear_escritorio.vbs 2>nul
    
    echo ✅ Acceso directo creado en el escritorio
)

echo.
echo 🎉 ¡Configuración de accesos directos completada!
echo.
