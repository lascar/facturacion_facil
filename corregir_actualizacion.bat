@echo off
chcp 65001 >nul
title Corregir Script de Actualización - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔧 CORREGIR SCRIPT ACTUALIZACIÓN             ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎯 Este script corrige el problema de "fatal: couldn't find remote ref main"
echo.

:: Verificar directorio
if not exist "main.py" (
    echo ❌ ERROR: Ejecutar desde la carpeta de la aplicación
    pause
    exit /b 1
)

set "APP=%CD%"
set "ESCRITORIO=D:\mis documentos\onedrive\escritorio"

echo 📁 Aplicación: %APP%
echo 🖥️  Escritorio OneDrive: %ESCRITORIO%
echo.

:: Verificar que OneDrive existe
if not exist "%ESCRITORIO%" (
    echo ❌ ERROR: Escritorio OneDrive no encontrado
    echo    Ruta: %ESCRITORIO%
    pause
    exit /b 1
)

echo ✅ Escritorio OneDrive encontrado
echo.

echo 🔧 Creando script de actualización corregido...

:: Crear script de actualización mejorado
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Actualizar Facturacion Facil
    echo cd /d "%APP%"
    echo.
    echo echo ╔══════════════════════════════════════════════════════════════╗
    echo echo ║                    🔄 ACTUALIZAR APP                        ║
    echo echo ╚══════════════════════════════════════════════════════════════╝
    echo echo.
    echo.
    echo echo 📡 Verificando Git y conexión...
    echo git --version ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Git no instalado
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 🌐 Verificando conexión a GitHub...
    echo ping -n 1 github.com ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Sin conexión a GitHub
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 💾 Creando respaldo...
    echo if not exist "backup" mkdir backup
    echo for /f "tokens=2 delims==" %%%%a in ^('wmic OS Get localdatetime /value'^) do set "dt=%%%%a"
    echo set "FECHA=%%dt:~0,4%%-%%dt:~4,2%%-%%dt:~6,2%%_%%dt:~8,2%%-%%dt:~10,2%%-%%dt:~12,2%%"
    echo if exist "facturacion.db" copy "facturacion.db" "backup\facturacion_%%FECHA%%.db" ^>nul
    echo echo ✅ Respaldo creado
    echo.
    echo echo 📥 Descargando actualizaciones...
    echo echo    Detectando rama del repositorio...
    echo git fetch origin ^>nul 2^>^&1
    echo.
    echo set "ACTUALIZADO=NO"
    echo.
    echo echo    Probando rama main...
    echo git pull origin main ^>nul 2^>^&1
    echo if not errorlevel 1 ^(
    echo     echo ✅ Actualizado desde rama main
    echo     set "ACTUALIZADO=SI"
    echo ^) else ^(
    echo     echo    main no disponible, probando master...
    echo     git pull origin master ^>nul 2^>^&1
    echo     if not errorlevel 1 ^(
    echo         echo ✅ Actualizado desde rama master
    echo         set "ACTUALIZADO=SI"
    echo     ^) else ^(
    echo         echo    master no disponible, probando pull genérico...
    echo         git pull ^>nul 2^>^&1
    echo         if not errorlevel 1 ^(
    echo             echo ✅ Actualizado ^(método genérico^)
    echo             set "ACTUALIZADO=SI"
    echo         ^) else ^(
    echo             echo ❌ Error: No se pudo actualizar
    echo             echo.
    echo             echo 💡 Información de debug:
    echo             git branch -r 2^>nul
    echo             echo.
    echo             pause
    echo             exit /b 1
    echo         ^)
    echo     ^)
    echo ^)
    echo.
    echo echo 📦 Actualizando dependencias...
    echo set "PYTHON=python"
    echo python --version ^>nul 2^>^&1 ^|^| set "PYTHON=py"
    echo py --version ^>nul 2^>^&1 ^|^| set "PYTHON=python3"
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "requirements.txt" %%PYTHON%% -m pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
    echo.
    echo echo ╔══════════════════════════════════════════════════════════════╗
    echo echo ║                    ✅ ACTUALIZACIÓN COMPLETADA              ║
    echo echo ╚══════════════════════════════════════════════════════════════╝
    echo echo.
    echo echo 🎉 Aplicación actualizada exitosamente
    echo echo 🚀 Ya puede usar la nueva versión
    echo echo.
    echo timeout /t 5 /nobreak ^>nul
) > "ActualizarAppCorregido.bat"

echo ✅ Script corregido creado: ActualizarAppCorregido.bat
echo.

:: Reemplazar archivos en OneDrive
echo 🖥️  Actualizando archivos en OneDrive...

:: Reemplazar el archivo de actualización
copy "ActualizarAppCorregido.bat" "%ESCRITORIO%\ActualizarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ ActualizarApp.bat actualizado en OneDrive
) else (
    echo ❌ Error actualizando ActualizarApp.bat en OneDrive
)

:: Crear versiones adicionales
copy "ActualizarAppCorregido.bat" "%ESCRITORIO%\Update.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Update.bat actualizado en OneDrive
)

:: Actualizar accesos directos si existen
if exist "%ESCRITORIO%\Actualizar.lnk" (
    echo 🔗 Actualizando acceso directo Actualizar.lnk...
    (
        echo Set WshShell = CreateObject^("WScript.Shell"^)
        echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO%\Actualizar.lnk"^)
        echo oShellLink.TargetPath = "%APP%\ActualizarAppCorregido.bat"
        echo oShellLink.WorkingDirectory = "%APP%"
        echo oShellLink.Description = "Actualizar Facturacion Facil ^(Corregido^)"
        echo oShellLink.Save
    ) > temp_actualizar_fix.vbs
    
    cscript //nologo temp_actualizar_fix.vbs >nul 2>&1
    if %errorlevel%==0 (
        echo ✅ Acceso directo Actualizar.lnk actualizado
    )
    del temp_actualizar_fix.vbs >nul 2>&1
)

echo.

:: Verificación
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VERIFICACIÓN                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos corregidos:
echo.

if exist "ActualizarAppCorregido.bat" (
    echo ✅ ActualizarAppCorregido.bat (en carpeta app)
)

if exist "%ESCRITORIO%\ActualizarApp.bat" (
    echo ✅ ActualizarApp.bat (en OneDrive)
)

if exist "%ESCRITORIO%\Update.bat" (
    echo ✅ Update.bat (en OneDrive)
)

if exist "%ESCRITORIO%\Actualizar.lnk" (
    echo ✅ Actualizar.lnk (en OneDrive)
)

echo.

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ CORRECCIÓN COMPLETADA                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 ¡Problema de actualización corregido!
echo.
echo 💡 CAMBIOS REALIZADOS:
echo    • ✅ Script detecta automáticamente la rama correcta
echo    • ✅ Prueba main, master y pull genérico
echo    • ✅ Mejor manejo de errores
echo    • ✅ Información de debug si falla
echo    • ✅ Archivos en OneDrive actualizados
echo.

echo 🎯 PRÓXIMOS PASOS:
echo    1. Ir al escritorio OneDrive
echo    2. Probar ActualizarApp.bat o Actualizar.lnk
echo    3. Debería funcionar sin errores
echo.

echo 🧪 ¿Desea probar el script corregido ahora? (S/N)
set /p probar=
if /i "%probar%"=="S" if /i "%probar%"=="s" (
    echo 🚀 Probando ActualizarAppCorregido.bat...
    call ActualizarAppCorregido.bat
)

echo.
echo 🖥️  ¿Desea abrir OneDrive para ver los archivos actualizados? (S/N)
set /p abrir=
if /i "%abrir%"=="S" if /i "%abrir%"=="s" (
    explorer "%ESCRITORIO%"
)

echo.
pause
