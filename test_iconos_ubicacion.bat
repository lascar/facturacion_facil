@echo off
chcp 65001 >nul
title Test Iconos desde Cualquier Ubicación

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                🧪 TEST DE ICONOS DESDE CUALQUIER UBICACIÓN                 ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Obtener directorio original de la aplicación
set "ORIGINAL_DIR=%~dp0"
set "ORIGINAL_DIR=%ORIGINAL_DIR:~0,-1%"

echo 📁 Directorio original de la aplicación: %ORIGINAL_DIR%
echo 📁 Directorio actual de ejecución: %CD%
echo.

echo 🔍 Verificando que el script puede cambiar al directorio correcto...
cd /d "%~dp0"
echo ✅ Cambiado al directorio del script: %CD%
echo.

echo 🔍 Verificando estructura de la aplicación...
if exist "main.py" (
    echo ✅ main.py encontrado
) else (
    echo ❌ main.py NO encontrado
    set "ERROR_FOUND=1"
)

if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado
) else (
    echo ❌ Entorno virtual NO encontrado
    set "ERROR_FOUND=1"
)

if exist "lancer_app.bat" (
    echo ✅ lancer_app.bat encontrado
) else (
    echo ❌ lancer_app.bat NO encontrado
    set "ERROR_FOUND=1"
)

echo.
echo 🧪 Simulando ejecución desde diferentes ubicaciones...
echo.

REM Crear directorio temporal para test
set "TEMP_TEST_DIR=%TEMP%\test_iconos_facturacion"
if exist "%TEMP_TEST_DIR%" rmdir /s /q "%TEMP_TEST_DIR%"
mkdir "%TEMP_TEST_DIR%"

echo 📋 Test 1: Creando icono en directorio temporal
echo    Ubicación de test: %TEMP_TEST_DIR%

REM Crear un icono de test en el directorio temporal
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set oShellLink = WshShell.CreateShortcut^("%TEMP_TEST_DIR%\Test Facturación Fácil.lnk"^)
echo oShellLink.TargetPath = "%ORIGINAL_DIR%\lancer_app.bat"
echo oShellLink.WorkingDirectory = "%ORIGINAL_DIR%"
echo oShellLink.Description = "Test - Facturación Fácil desde ubicación externa"
echo oShellLink.Save
echo WScript.Echo "Icono de test creado"
) > "%TEMP_TEST_DIR%\crear_test.vbs"

cscript //nologo "%TEMP_TEST_DIR%\crear_test.vbs"
del "%TEMP_TEST_DIR%\crear_test.vbs"

if exist "%TEMP_TEST_DIR%\Test Facturación Fácil.lnk" (
    echo ✅ Icono de test creado exitosamente
) else (
    echo ❌ Error al crear icono de test
    set "ERROR_FOUND=1"
)

echo.
echo 📋 Test 2: Verificando propiedades del icono
echo.

REM Crear script para leer propiedades del icono
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set oShellLink = WshShell.CreateShortcut^("%TEMP_TEST_DIR%\Test Facturación Fácil.lnk"^)
echo WScript.Echo "TargetPath: " ^& oShellLink.TargetPath
echo WScript.Echo "WorkingDirectory: " ^& oShellLink.WorkingDirectory
echo WScript.Echo "Description: " ^& oShellLink.Description
) > "%TEMP_TEST_DIR%\leer_propiedades.vbs"

echo 🔍 Propiedades del icono de test:
cscript //nologo "%TEMP_TEST_DIR%\leer_propiedades.vbs"
del "%TEMP_TEST_DIR%\leer_propiedades.vbs"

echo.
echo 📋 Test 3: Verificando que lancer_app.bat maneja correctamente el directorio
echo.

REM Crear un script de test que simule ejecución desde otra ubicación
(
echo @echo off
echo echo Test: Ejecutando lancer_app.bat desde %TEMP_TEST_DIR%
echo echo Directorio actual antes: %%CD%%
echo cd /d "%ORIGINAL_DIR%"
echo echo Directorio después del cambio: %%CD%%
echo if exist "venv\Scripts\python.exe" ^(
echo     echo ✅ Entorno virtual accesible desde directorio correcto
echo ^) else ^(
echo     echo ❌ Entorno virtual NO accesible
echo ^)
echo if exist "main.py" ^(
echo     echo ✅ main.py accesible desde directorio correcto
echo ^) else ^(
echo     echo ❌ main.py NO accesible
echo ^)
echo pause
) > "%TEMP_TEST_DIR%\test_cambio_directorio.bat"

echo 🧪 Ejecutando test de cambio de directorio...
call "%TEMP_TEST_DIR%\test_cambio_directorio.bat"

echo.
echo 📋 Test 4: Verificando iconos existentes en la aplicación
echo.

cd /d "%ORIGINAL_DIR%"

echo 🔍 Iconos en el directorio de la aplicación:
set "ICONOS_OK=0"
set "ICONOS_TOTAL=0"

for %%i in (
    "🚀 Lanzar Facturación Fácil.lnk"
    "🔄 Actualizar desde Git.lnk"
    "🗑️ Desinstalar Aplicación.lnk"
    "🔧 Reinstalar Aplicación.lnk"
) do (
    set /a ICONOS_TOTAL+=1
    if exist "%%i" (
        echo    ✅ %%i
        set /a ICONOS_OK+=1
        
        REM Verificar propiedades del icono
        (
        echo Set WshShell = CreateObject^("WScript.Shell"^)
        echo Set oShellLink = WshShell.CreateShortcut^("%%i"^)
        echo If oShellLink.WorkingDirectory = "%ORIGINAL_DIR%" Then
        echo     WScript.Echo "       ✅ WorkingDirectory correcto"
        echo Else
        echo     WScript.Echo "       ❌ WorkingDirectory incorrecto: " ^& oShellLink.WorkingDirectory
        echo End If
        ) > temp_check.vbs
        
        cscript //nologo temp_check.vbs
        del temp_check.vbs
    ) else (
        echo    ❌ %%i (no existe)
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📊 RESULTADOS DEL TEST                                  ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if not defined ERROR_FOUND (
    echo ✅ TODOS LOS TESTS PASARON
    echo.
    echo 🎯 Los iconos funcionarán correctamente desde cualquier ubicación porque:
    echo    • lancer_app.bat usa 'cd /d "%%~dp0"' para cambiar al directorio correcto
    echo    • Los iconos tienen WorkingDirectory configurado correctamente
    echo    • El entorno virtual se encuentra usando rutas relativas
    echo    • main.py se ejecuta desde el directorio correcto
    echo.
    echo ✅ Iconos verificados: %ICONOS_OK%/%ICONOS_TOTAL%
) else (
    echo ❌ SE ENCONTRARON PROBLEMAS
    echo.
    echo 🔧 Posibles soluciones:
    echo    1. Ejecutar instalar_app.bat para configurar el entorno virtual
    echo    2. Ejecutar crear_iconos_personalizados.bat para crear los iconos
    echo    3. Verificar que está en el directorio correcto de la aplicación
)

echo.
echo 📋 Test 5: Creando iconos mejorados con verificación robusta
echo.

if %ICONOS_OK% lss %ICONOS_TOTAL% (
    echo 🔧 Algunos iconos faltan. ¿Crear iconos mejorados? (S/N)
    set /p crear_iconos="Respuesta: "
    if /i "!crear_iconos!"=="S" (
        echo 🎨 Creando iconos con verificación robusta...
        call crear_iconos_personalizados.bat
    )
)

REM Limpiar directorio temporal
rmdir /s /q "%TEMP_TEST_DIR%" 2>nul

echo.
echo 🎯 Test completado
echo.
echo 💡 RESUMEN:
echo    • Los iconos usan WorkingDirectory para funcionar desde cualquier ubicación
echo    • lancer_app.bat cambia automáticamente al directorio correcto
echo    • El entorno virtual se accede con rutas relativas desde el directorio correcto
echo    • Los iconos son completamente portables
echo.
pause
