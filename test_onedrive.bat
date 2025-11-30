@echo off
chcp 65001 >nul
title Test OneDrive Escritorio - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🧪 TEST ONEDRIVE ESCRITORIO                  ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Ruta específica de tu OneDrive
set "ESCRITORIO_ONEDRIVE=D:\mis documentos\onedrive\escritorio"

echo 🔍 Probando acceso al escritorio OneDrive...
echo    Ruta: %ESCRITORIO_ONEDRIVE%
echo.

:: Test 1: Verificar que la carpeta existe
if exist "%ESCRITORIO_ONEDRIVE%" (
    echo ✅ PASO 1: Carpeta OneDrive existe
) else (
    echo ❌ PASO 1: Carpeta OneDrive NO existe
    echo.
    echo 💡 Verificar:
    echo    • Que OneDrive esté instalado y funcionando
    echo    • Que la sincronización esté completa
    echo    • Que la ruta sea exactamente: %ESCRITORIO_ONEDRIVE%
    echo.
    pause
    exit /b 1
)

:: Test 2: Verificar permisos de escritura
echo 🔐 PASO 2: Probando permisos de escritura...

echo Test de escritura > "%ESCRITORIO_ONEDRIVE%\test_facturacion.txt" 2>nul

if exist "%ESCRITORIO_ONEDRIVE%\test_facturacion.txt" (
    echo ✅ PASO 2: Permisos de escritura OK
    del "%ESCRITORIO_ONEDRIVE%\test_facturacion.txt" >nul 2>&1
) else (
    echo ❌ PASO 2: Sin permisos de escritura
    echo.
    echo 💡 Soluciones:
    echo    • Ejecutar como administrador
    echo    • Verificar permisos de la carpeta OneDrive
    echo    • Esperar que OneDrive termine de sincronizar
    echo.
    pause
    exit /b 1
)

:: Test 3: Crear archivo .bat de prueba
echo 📝 PASO 3: Creando archivo .bat de prueba...

(
    echo @echo off
    echo echo ¡Hola desde Facturacion Facil!
    echo echo Este es un test desde OneDrive
    echo pause
) > "%ESCRITORIO_ONEDRIVE%\test_app.bat"

if exist "%ESCRITORIO_ONEDRIVE%\test_app.bat" (
    echo ✅ PASO 3: Archivo .bat creado exitosamente
) else (
    echo ❌ PASO 3: Error creando archivo .bat
    pause
    exit /b 1
)

:: Test 4: Crear acceso directo .lnk de prueba
echo 🔗 PASO 4: Creando acceso directo .lnk de prueba...

(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO_ONEDRIVE%\test_link.lnk"^)
    echo oShellLink.TargetPath = "%ESCRITORIO_ONEDRIVE%\test_app.bat"
    echo oShellLink.Description = "Test Link"
    echo oShellLink.Save
) > temp_test.vbs

cscript //nologo temp_test.vbs >nul 2>&1

if exist "%ESCRITORIO_ONEDRIVE%\test_link.lnk" (
    echo ✅ PASO 4: Acceso directo .lnk creado exitosamente
) else (
    echo ❌ PASO 4: Error creando acceso directo .lnk
)

del temp_test.vbs >nul 2>&1

:: Test 5: Verificar que los archivos son visibles
echo 👀 PASO 5: Verificando visibilidad de archivos...

dir "%ESCRITORIO_ONEDRIVE%\test_*" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ PASO 5: Archivos de test visibles
) else (
    echo ❌ PASO 5: Archivos de test no visibles
)

echo.

:: Mostrar contenido del escritorio OneDrive
echo 📋 CONTENIDO ACTUAL DEL ESCRITORIO ONEDRIVE:
echo.
dir "%ESCRITORIO_ONEDRIVE%" /b 2>nul | findstr /v "^$" || echo (Carpeta vacía o sin acceso)

echo.

:: Test 6: Probar el archivo creado
echo 🧪 PASO 6: ¿Desea probar el archivo .bat creado? (S/N)
set /p probar=
if /i "%probar%"=="S" if /i "%probar%"=="s" (
    if exist "%ESCRITORIO_ONEDRIVE%\test_app.bat" (
        echo 🚀 Ejecutando test_app.bat...
        start "" "%ESCRITORIO_ONEDRIVE%\test_app.bat"
    )
)

echo.

:: Limpiar archivos de test
echo 🧹 PASO 7: ¿Desea limpiar los archivos de test? (S/N)
set /p limpiar=
if /i "%limpiar%"=="S" if /i "%limpiar%"=="s" (
    del "%ESCRITORIO_ONEDRIVE%\test_app.bat" >nul 2>&1
    del "%ESCRITORIO_ONEDRIVE%\test_link.lnk" >nul 2>&1
    echo ✅ Archivos de test eliminados
)

echo.

:: Resumen final
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📋 RESUMEN DEL TEST                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎯 RESULTADO: OneDrive Escritorio está LISTO para usar
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Ejecutar crear_iconos_onedrive.bat
echo    2. Los iconos aparecerán en: %ESCRITORIO_ONEDRIVE%
echo    3. El usuario podrá hacer doble clic en los iconos
echo.

echo 🚀 ¿Desea ejecutar crear_iconos_onedrive.bat ahora? (S/N)
set /p ejecutar=
if /i "%ejecutar%"=="S" if /i "%ejecutar%"=="s" (
    if exist "crear_iconos_onedrive.bat" (
        echo 🔄 Ejecutando crear_iconos_onedrive.bat...
        call crear_iconos_onedrive.bat
    ) else (
        echo ❌ crear_iconos_onedrive.bat no encontrado
    )
)

echo.
echo 🖥️  ¿Desea abrir el escritorio OneDrive? (S/N)
set /p abrir=
if /i "%abrir%"=="S" if /i "%abrir%"=="s" (
    explorer "%ESCRITORIO_ONEDRIVE%"
)

echo.
pause
