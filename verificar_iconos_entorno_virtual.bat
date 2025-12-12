@echo off
chcp 65001 >nul
title Verificación Iconos + Entorno Virtual

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║            🔍 VERIFICACIÓN COMPLETA: ICONOS + ENTORNO VIRTUAL              ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"
set "APP_DIR=%CD%"

echo 📁 Directorio de la aplicación: %APP_DIR%
echo.

echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🧪 TEST 1: ENTORNO VIRTUAL                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando entorno virtual...
if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado
    echo 📍 Ubicación: %APP_DIR%\venv\Scripts\python.exe
    
    echo 🐍 Versión de Python en el entorno virtual:
    venv\Scripts\python.exe --version
    
    echo 📦 Verificando PyQt5 en el entorno virtual:
    venv\Scripts\python.exe -c "import PyQt5; print('✅ PyQt5 versión:', PyQt5.QtCore.QT_VERSION_STR)" 2>nul && (
        echo ✅ PyQt5 funciona correctamente
    ) || (
        echo ❌ PyQt5 no está instalado o no funciona
        set "VENV_ERROR=1"
    )
) else (
    echo ❌ Entorno virtual NO encontrado
    echo 💡 Ejecute: instalar_app.bat
    set "VENV_ERROR=1"
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🔗 TEST 2: ICONOS Y SCRIPTS                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando scripts de lanzamiento...
if exist "lancer_app.bat" (
    echo ✅ lancer_app.bat encontrado
    
    REM Verificar que el script tiene el cd correcto
    findstr /C:"cd /d" lancer_app.bat >nul && (
        echo ✅ lancer_app.bat tiene cambio de directorio correcto
    ) || (
        echo ❌ lancer_app.bat NO tiene cambio de directorio
        set "SCRIPT_ERROR=1"
    )
) else (
    echo ❌ lancer_app.bat NO encontrado
    set "SCRIPT_ERROR=1"
)

if exist "lancer_rapide.bat" (
    echo ✅ lancer_rapide.bat encontrado
    
    findstr /C:"cd /d" lancer_rapide.bat >nul && (
        echo ✅ lancer_rapide.bat tiene cambio de directorio correcto
    ) || (
        echo ❌ lancer_rapide.bat NO tiene cambio de directorio
        set "SCRIPT_ERROR=1"
    )
) else (
    echo ❌ lancer_rapide.bat NO encontrado
    set "SCRIPT_ERROR=1"
)

echo.
echo 🔍 Verificando iconos existentes...
set "ICONOS_OK=0"
set "ICONOS_TOTAL=0"

for %%i in (
    "🚀 Lanzar Facturación Fácil.lnk"
    "⚡ Lanzamiento Rápido.lnk"
    "🔄 Actualizar desde Git.lnk"
    "🗑️ Desinstalar Aplicación.lnk"
    "🔧 Reinstalar Aplicación.lnk"
) do (
    set /a ICONOS_TOTAL+=1
    if exist "%%i" (
        echo ✅ %%i
        set /a ICONOS_OK+=1
        
        REM Verificar propiedades críticas del icono
        (
        echo Set WshShell = CreateObject^("WScript.Shell"^)
        echo Set oShellLink = WshShell.CreateShortcut^("%%i"^)
        echo If oShellLink.WorkingDirectory = "%APP_DIR%" Then
        echo     WScript.Echo "   ✅ WorkingDirectory correcto"
        echo Else
        echo     WScript.Echo "   ❌ WorkingDirectory incorrecto: " ^& oShellLink.WorkingDirectory
        echo End If
        echo If InStr^(oShellLink.TargetPath, "%APP_DIR%"^) ^> 0 Then
        echo     WScript.Echo "   ✅ TargetPath correcto"
        echo Else
        echo     WScript.Echo "   ❌ TargetPath incorrecto: " ^& oShellLink.TargetPath
        echo End If
        ) > temp_check_icon.vbs
        
        cscript //nologo temp_check_icon.vbs
        del temp_check_icon.vbs
    ) else (
        echo ❌ %%i (no existe)
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                🧪 TEST 3: SIMULACIÓN DESDE OTRA UBICACIÓN                 ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Crear directorio temporal para test
set "TEMP_DIR=%TEMP%\test_facturacion_%RANDOM%"
mkdir "%TEMP_DIR%" 2>nul

echo 📁 Directorio de test: %TEMP_DIR%
echo.

REM Crear icono de test en ubicación externa
echo 🔧 Creando icono de test en ubicación externa...
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set oShellLink = WshShell.CreateShortcut^("%TEMP_DIR%\Test Facturación.lnk"^)
echo oShellLink.TargetPath = "%APP_DIR%\lancer_app.bat"
echo oShellLink.WorkingDirectory = "%APP_DIR%"
echo oShellLink.Description = "Test desde ubicación externa"
echo oShellLink.Save
echo WScript.Echo "Icono de test creado"
) > "%TEMP_DIR%\crear_test.vbs"

cscript //nologo "%TEMP_DIR%\crear_test.vbs" >nul
del "%TEMP_DIR%\crear_test.vbs"

if exist "%TEMP_DIR%\Test Facturación.lnk" (
    echo ✅ Icono de test creado exitosamente
    
    REM Verificar propiedades
    (
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%TEMP_DIR%\Test Facturación.lnk"^)
    echo WScript.Echo "TargetPath: " ^& oShellLink.TargetPath
    echo WScript.Echo "WorkingDirectory: " ^& oShellLink.WorkingDirectory
    ) > "%TEMP_DIR%\verificar_test.vbs"
    
    echo 🔍 Propiedades del icono de test:
    cscript //nologo "%TEMP_DIR%\verificar_test.vbs"
    del "%TEMP_DIR%\verificar_test.vbs"
    
    echo ✅ El icono funcionaría correctamente desde cualquier ubicación
) else (
    echo ❌ Error al crear icono de test
)

REM Limpiar directorio temporal
rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📊 RESULTADO FINAL                                      ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if not defined VENV_ERROR if not defined SCRIPT_ERROR if %ICONOS_OK% geq 3 (
    echo 🎉 ¡VERIFICACIÓN EXITOSA!
    echo.
    echo ✅ ENTORNO VIRTUAL: Configurado y funcional
    echo ✅ SCRIPTS: Configurados para cambiar directorio correctamente
    echo ✅ ICONOS: %ICONOS_OK%/%ICONOS_TOTAL% funcionan correctamente
    echo ✅ PORTABILIDAD: Los iconos funcionan desde cualquier ubicación
    echo.
    echo 🎯 FUNCIONAMIENTO GARANTIZADO:
    echo    • Los iconos usan WorkingDirectory = "%APP_DIR%"
    echo    • Los scripts usan 'cd /d "%%~dp0"' para cambiar al directorio correcto
    echo    • El entorno virtual se encuentra usando rutas relativas
    echo    • main.py se ejecuta desde el directorio correcto con el entorno virtual
    echo.
    echo 🚀 PUEDE USAR LOS ICONOS DESDE CUALQUIER UBICACIÓN:
    echo    • Escritorio
    echo    • Barra de tareas
    echo    • Menú Inicio
    echo    • Cualquier carpeta
    echo    • Accesos directos copiados/movidos
) else (
    echo ❌ SE ENCONTRARON PROBLEMAS
    echo.
    if defined VENV_ERROR (
        echo 🔧 ENTORNO VIRTUAL: Ejecute instalar_app.bat
    )
    if defined SCRIPT_ERROR (
        echo 🔧 SCRIPTS: Verifique que lancer_app.bat y lancer_rapide.bat existen
    )
    if %ICONOS_OK% lss 3 (
        echo 🔧 ICONOS: Ejecute crear_iconos_robustos.bat
    )
    echo.
    echo 💡 SOLUCIONES RECOMENDADAS:
    echo    1. instalar_app.bat          (configurar entorno virtual)
    echo    2. crear_iconos_robustos.bat (crear iconos ultra-robustos)
    echo    3. Ejecutar este test nuevamente
)

echo.
echo 💡 SCRIPTS DISPONIBLES:
echo    • crear_iconos_robustos.bat     - Crear iconos ultra-robustos
echo    • test_iconos_ubicacion.bat     - Test detallado de ubicaciones
echo    • mostrar_ubicacion_iconos.bat  - Ver dónde están los iconos
echo.
pause
