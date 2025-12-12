@echo off
chcp 65001 >nul
title Iconos Personalizados - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎨 ICONOS PERSONALIZADOS                                 ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Obtener la ruta actual
set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"

echo 📁 Directorio de la aplicación: %APP_DIR%
echo.

REM Verificar si existe el icono principal
if not exist "assets\icon.ico" (
    echo ⚠️  Icono principal no encontrado
    echo 🎨 Creando icono por defecto...
    
    if not exist "assets" mkdir assets
    
    REM Crear un icono básico usando PowerShell
    powershell -Command "& {
        Add-Type -AssemblyName System.Drawing
        $bitmap = New-Object System.Drawing.Bitmap(64, 64)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.Clear([System.Drawing.Color]::Blue)
        $font = New-Object System.Drawing.Font('Arial', 20, [System.Drawing.FontStyle]::Bold)
        $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
        $graphics.DrawString('FF', $font, $brush, 10, 20)
        $graphics.Dispose()
        $bitmap.Save('%APP_DIR%\assets\icon.png', [System.Drawing.Imaging.ImageFormat]::Png)
        $bitmap.Dispose()
    }"
    
    echo ✅ Icono básico creado
)

echo 🎯 Creando iconos personalizados con emojis...

REM Crear script VBS para iconos personalizados
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set fso = CreateObject^("Scripting.FileSystemObject"^)
echo.
echo ' Función para crear acceso directo
echo Function CreateShortcut^(linkPath, targetPath, workingDir, description, iconPath^)
echo     Set oShellLink = WshShell.CreateShortcut^(linkPath^)
echo     oShellLink.TargetPath = targetPath
echo     oShellLink.WorkingDirectory = workingDir
echo     oShellLink.Description = description
echo     If iconPath ^<^> "" Then
echo         oShellLink.IconLocation = iconPath
echo     End If
echo     oShellLink.Save
echo End Function
echo.
echo ' Crear iconos con nombres descriptivos
echo Call CreateShortcut^("%APP_DIR%\🚀 Lanzar Facturación Fácil.lnk", "%APP_DIR%\lancer_app.bat", "%APP_DIR%", "Ejecutar Facturación Fácil", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateShortcut^("%APP_DIR%\🔄 Actualizar desde Git.lnk", "%APP_DIR%\ActualizarAppMejorado.bat", "%APP_DIR%", "Actualizar aplicación desde repositorio Git", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateShortcut^("%APP_DIR%\🗑️ Desinstalar Aplicación.lnk", "%APP_DIR%\desinstalar_app.bat", "%APP_DIR%", "Desinstalar completamente la aplicación", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateShortcut^("%APP_DIR%\🔧 Reinstalar Aplicación.lnk", "%APP_DIR%\instalar_app.bat", "%APP_DIR%", "Reinstalar la aplicación", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateShortcut^("%APP_DIR%\📊 Abrir Base de Datos.lnk", "%APP_DIR%\base_de_datos", "%APP_DIR%", "Abrir carpeta de base de datos", "shell32.dll,4"^)
echo Call CreateShortcut^("%APP_DIR%\📄 Ver PDFs Generados.lnk", "%APP_DIR%\pdfs", "%APP_DIR%", "Ver facturas PDF generadas", "shell32.dll,71"^)
echo Call CreateShortcut^("%APP_DIR%\⚙️ Configuración.lnk", "%APP_DIR%\config", "%APP_DIR%", "Abrir carpeta de configuración", "shell32.dll,316"^)
echo Call CreateShortcut^("%APP_DIR%\📝 Logs de la Aplicación.lnk", "%APP_DIR%\logs", "%APP_DIR%", "Ver logs de la aplicación", "shell32.dll,1"^)
echo.
echo WScript.Echo "Iconos personalizados creados exitosamente"
) > crear_iconos_personalizados.vbs

echo 🎨 Generando iconos personalizados...
cscript //nologo crear_iconos_personalizados.vbs

REM Limpiar archivo temporal
del crear_iconos_personalizados.vbs 2>nul

echo.
echo ✅ ICONOS PERSONALIZADOS CREADOS
echo.
echo 📋 Iconos disponibles:
echo    🚀 Lanzar Facturación Fácil.lnk    - Ejecutar aplicación
echo    🔄 Actualizar desde Git.lnk        - Actualizar código
echo    🗑️ Desinstalar Aplicación.lnk      - Desinstalar
echo    🔧 Reinstalar Aplicación.lnk       - Reinstalar
echo    📊 Abrir Base de Datos.lnk         - Ver base de datos
echo    📄 Ver PDFs Generados.lnk          - Ver facturas PDF
echo    ⚙️ Configuración.lnk               - Configuración
echo    📝 Logs de la Aplicación.lnk       - Ver logs
echo.
echo 💡 Características:
echo    • Nombres descriptivos con emojis
echo    • Iconos del sistema apropiados
echo    • Movibles a cualquier ubicación
echo    • Funcionan desde cualquier carpeta
echo.

REM Crear también versiones para el escritorio
set /p create_desktop="¿Crear iconos principales en el escritorio? (S/N): "
if /i "%create_desktop%"=="S" (
    echo 🖥️ Creando iconos en el escritorio...
    
    (
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo.
    echo ' Icono principal en escritorio
    echo Set oShellLink = WshShell.CreateShortcut^("%USERPROFILE%\Desktop\Facturación Fácil.lnk"^)
    echo oShellLink.TargetPath = "%APP_DIR%\lancer_app.bat"
    echo oShellLink.WorkingDirectory = "%APP_DIR%"
    echo oShellLink.Description = "Facturación Fácil - Sistema de Facturación"
    echo oShellLink.IconLocation = "%APP_DIR%\assets\icon.ico"
    echo oShellLink.Save
    echo.
    echo ' Icono de actualización en escritorio
    echo Set oShellLink2 = WshShell.CreateShortcut^("%USERPROFILE%\Desktop\Actualizar Facturación Fácil.lnk"^)
    echo oShellLink2.TargetPath = "%APP_DIR%\ActualizarAppMejorado.bat"
    echo oShellLink2.WorkingDirectory = "%APP_DIR%"
    echo oShellLink2.Description = "Actualizar Facturación Fácil desde Git"
    echo oShellLink2.IconLocation = "%APP_DIR%\assets\icon.ico"
    echo oShellLink2.Save
    echo.
    echo WScript.Echo "Iconos del escritorio creados"
    ) > crear_escritorio_personalizados.vbs
    
    cscript //nologo crear_escritorio_personalizados.vbs
    del crear_escritorio_personalizados.vbs 2>nul
    
    echo ✅ Iconos creados en el escritorio
)

echo.
echo 🎉 ¡Iconos personalizados listos!
echo.
echo 💡 Consejos:
echo    • Puede mover los iconos a cualquier carpeta
echo    • Los iconos funcionan desde cualquier ubicación
echo    • Para cambiar iconos, edite este script
echo.

pause
