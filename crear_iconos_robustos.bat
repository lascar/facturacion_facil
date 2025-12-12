@echo off
chcp 65001 >nul
title Iconos Ultra-Robustos - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                🛡️ ICONOS ULTRA-ROBUSTOS                                    ║
echo ║           Funcionan desde CUALQUIER ubicación                               ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Obtener la ruta ABSOLUTA de la aplicación
set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"

echo 📁 Directorio de la aplicación: %APP_DIR%
echo.

echo 🔍 Verificando estructura de la aplicación...
if not exist "%APP_DIR%\main.py" (
    echo ❌ main.py no encontrado en %APP_DIR%
    echo 💡 Asegúrese de ejecutar este script desde el directorio de la aplicación
    pause
    exit /b 1
)

if not exist "%APP_DIR%\lancer_app.bat" (
    echo ❌ lancer_app.bat no encontrado
    pause
    exit /b 1
)

echo ✅ Estructura de la aplicación verificada
echo.

echo 🛡️ Creando iconos ultra-robustos...
echo.

REM Crear script VBS para iconos robustos
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set fso = CreateObject^("Scripting.FileSystemObject"^)
echo.
echo ' Función para crear acceso directo robusto
echo Function CreateRobustShortcut^(linkPath, targetPath, workingDir, description, iconPath^)
echo     Set oShellLink = WshShell.CreateShortcut^(linkPath^)
echo     
echo     ' Usar rutas ABSOLUTAS para máxima compatibilidad
echo     oShellLink.TargetPath = targetPath
echo     oShellLink.WorkingDirectory = workingDir
echo     oShellLink.Description = description
echo     
echo     ' Configurar icono si existe
echo     If fso.FileExists^(iconPath^) Then
echo         oShellLink.IconLocation = iconPath
echo     Else
echo         ' Usar icono del sistema si no existe el personalizado
echo         oShellLink.IconLocation = "shell32.dll,137"
echo     End If
echo     
echo     ' Configurar argumentos adicionales para robustez
echo     oShellLink.Arguments = ""
echo     oShellLink.WindowStyle = 1
echo     
echo     oShellLink.Save
echo     
echo     ' Verificar que se creó correctamente
echo     If fso.FileExists^(linkPath^) Then
echo         WScript.Echo "✅ Creado: " ^& fso.GetFileName^(linkPath^)
echo     Else
echo         WScript.Echo "❌ Error: " ^& fso.GetFileName^(linkPath^)
echo     End If
echo End Function
echo.
echo ' Crear iconos principales con rutas absolutas
echo Call CreateRobustShortcut^("%APP_DIR%\🚀 Lanzar Facturación Fácil.lnk", "%APP_DIR%\lancer_app.bat", "%APP_DIR%", "Ejecutar Facturación Fácil con entorno virtual", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateRobustShortcut^("%APP_DIR%\⚡ Lanzamiento Rápido.lnk", "%APP_DIR%\lancer_rapide.bat", "%APP_DIR%", "Lanzamiento rápido de Facturación Fácil", "%APP_DIR%\assets\icon.ico"^)
echo Call CreateRobustShortcut^("%APP_DIR%\🔄 Actualizar desde Git.lnk", "%APP_DIR%\actualizar_git_mejorado.bat", "%APP_DIR%", "Actualizar aplicación desde repositorio Git", "shell32.dll,238"^)
echo Call CreateRobustShortcut^("%APP_DIR%\🗑️ Desinstalar Aplicación.lnk", "%APP_DIR%\desinstalar_app.bat", "%APP_DIR%", "Desinstalar completamente la aplicación", "shell32.dll,131"^)
echo Call CreateRobustShortcut^("%APP_DIR%\🔧 Reinstalar Aplicación.lnk", "%APP_DIR%\instalar_app.bat", "%APP_DIR%", "Reinstalar la aplicación", "shell32.dll,162"^)
echo Call CreateRobustShortcut^("%APP_DIR%\🧪 Test Entorno Virtual.lnk", "%APP_DIR%\test_entorno_virtual.bat", "%APP_DIR%", "Verificar entorno virtual", "shell32.dll,23"^)
echo Call CreateRobustShortcut^("%APP_DIR%\🔍 Diagnóstico Completo.lnk", "%APP_DIR%\diagnostico_completo.bat", "%APP_DIR%", "Diagnóstico completo del sistema", "shell32.dll,78"^)
echo Call CreateRobustShortcut^("%APP_DIR%\📊 Abrir Base de Datos.lnk", "%APP_DIR%\base_de_datos", "%APP_DIR%", "Abrir carpeta de base de datos", "shell32.dll,4"^)
echo Call CreateRobustShortcut^("%APP_DIR%\📄 Ver PDFs Generados.lnk", "%APP_DIR%\pdfs", "%APP_DIR%", "Ver facturas PDF generadas", "shell32.dll,71"^)
echo Call CreateRobustShortcut^("%APP_DIR%\📝 Logs de la Aplicación.lnk", "%APP_DIR%\logs", "%APP_DIR%", "Ver logs de la aplicación", "shell32.dll,1"^)
echo.
echo WScript.Echo ""
echo WScript.Echo "🎯 Iconos ultra-robustos creados exitosamente"
echo WScript.Echo "🛡️ Funcionan desde CUALQUIER ubicación"
) > crear_iconos_robustos.vbs

echo 🎨 Generando iconos ultra-robustos...
cscript //nologo crear_iconos_robustos.vbs

REM Limpiar archivo temporal
del crear_iconos_robustos.vbs 2>nul

echo.
echo 🧪 Verificando que los iconos funcionan correctamente...
echo.

REM Verificar cada icono creado
set "ICONOS_CREADOS=0"
for %%i in (
    "🚀 Lanzar Facturación Fácil.lnk"
    "⚡ Lanzamiento Rápido.lnk"
    "🔄 Actualizar desde Git.lnk"
    "🗑️ Desinstalar Aplicación.lnk"
    "🔧 Reinstalar Aplicación.lnk"
    "🧪 Test Entorno Virtual.lnk"
    "🔍 Diagnóstico Completo.lnk"
    "📊 Abrir Base de Datos.lnk"
    "📄 Ver PDFs Generados.lnk"
    "📝 Logs de la Aplicación.lnk"
) do (
    if exist "%%i" (
        set /a ICONOS_CREADOS+=1
        echo ✅ %%i
        
        REM Verificar propiedades del icono
        (
        echo Set WshShell = CreateObject^("WScript.Shell"^)
        echo Set oShellLink = WshShell.CreateShortcut^("%%i"^)
        echo If oShellLink.WorkingDirectory = "%APP_DIR%" Then
        echo     WScript.Echo "   ✅ WorkingDirectory: CORRECTO"
        echo Else
        echo     WScript.Echo "   ❌ WorkingDirectory: " ^& oShellLink.WorkingDirectory
        echo End If
        echo If InStr^(oShellLink.TargetPath, "%APP_DIR%"^) ^> 0 Then
        echo     WScript.Echo "   ✅ TargetPath: CORRECTO"
        echo Else
        echo     WScript.Echo "   ❌ TargetPath: " ^& oShellLink.TargetPath
        echo End If
        ) > temp_verify.vbs
        
        cscript //nologo temp_verify.vbs
        del temp_verify.vbs
    ) else (
        echo ❌ %%i (no se pudo crear)
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎯 RESULTADO FINAL                                      ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo ✅ Iconos creados: %ICONOS_CREADOS%/10
echo.
echo 🛡️ CARACTERÍSTICAS ULTRA-ROBUSTAS:
echo    • Rutas ABSOLUTAS: Funcionan desde cualquier ubicación
echo    • WorkingDirectory configurado: El entorno virtual se encuentra siempre
echo    • Verificación automática: Cada icono se verifica al crearse
echo    • Iconos del sistema: Si no hay iconos personalizados, usa iconos Windows
echo    • Scripts mejorados: lancer_app.bat y lancer_rapide.bat usan cd /d "%%~dp0"
echo.
echo 🎯 UBICACIONES DONDE FUNCIONAN:
echo    • ✅ Escritorio
echo    • ✅ Barra de tareas (anclados)
echo    • ✅ Menú Inicio
echo    • ✅ Cualquier carpeta
echo    • ✅ Accesos directos copiados/movidos
echo    • ✅ Unidades de red (si accesibles)
echo.

REM Crear también en el escritorio si el usuario quiere
set /p create_desktop="¿Crear iconos principales en el escritorio? (S/N): "
if /i "%create_desktop%"=="S" (
    echo.
    echo 🖥️ Creando iconos en el escritorio...
    
    (
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set fso = CreateObject^("Scripting.FileSystemObject"^)
    echo.
    echo ' Icono principal en escritorio
    echo Set oShellLink = WshShell.CreateShortcut^("%USERPROFILE%\Desktop\Facturación Fácil.lnk"^)
    echo oShellLink.TargetPath = "%APP_DIR%\lancer_app.bat"
    echo oShellLink.WorkingDirectory = "%APP_DIR%"
    echo oShellLink.Description = "Facturación Fácil - Sistema de Facturación con Entorno Virtual"
    echo If fso.FileExists^("%APP_DIR%\assets\icon.ico"^) Then
    echo     oShellLink.IconLocation = "%APP_DIR%\assets\icon.ico"
    echo Else
    echo     oShellLink.IconLocation = "shell32.dll,137"
    echo End If
    echo oShellLink.Save
    echo WScript.Echo "✅ Icono principal creado en escritorio"
    ) > crear_escritorio_robusto.vbs
    
    cscript //nologo crear_escritorio_robusto.vbs
    del crear_escritorio_robusto.vbs
)

echo.
echo 🎉 ¡ICONOS ULTRA-ROBUSTOS COMPLETADOS!
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Pruebe mover un icono al escritorio
echo    2. Ejecute desde el escritorio para verificar
echo    3. Use test_iconos_ubicacion.bat para test completo
echo.
pause
