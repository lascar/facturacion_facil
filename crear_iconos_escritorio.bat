@echo off
chcp 65001 >nul
title Crear Iconos Escritorio - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🖥️  CREAR ICONOS ESCRITORIO              ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ❌ ERROR: Este script debe ejecutarse desde la carpeta de la aplicación
    echo.
    echo 💡 Instrucciones:
    echo    1. Abra la carpeta que contiene main.py
    echo    2. Haga doble clic en este archivo
    echo.
    pause
    exit /b 1
)

:: Rutas
set "CARPETA_APP=%CD%"
set "ESCRITORIO=%USERPROFILE%\Desktop"

:: Si Desktop no existe, probar Escritorio
if not exist "%ESCRITORIO%" (
    set "ESCRITORIO=%USERPROFILE%\Escritorio"
)

echo 📁 Carpeta aplicación: %CARPETA_APP%
echo 🖥️  Escritorio usuario: %ESCRITORIO%
echo.

if not exist "%ESCRITORIO%" (
    echo ❌ ERROR: No se puede encontrar el escritorio
    echo.
    echo 💡 Rutas probadas:
    echo    - %USERPROFILE%\Desktop
    echo    - %USERPROFILE%\Escritorio
    echo.
    pause
    exit /b 1
)

echo 🎯 Este script creará 2 iconos en su escritorio:
echo.
echo    🚀 FacturacionFacil
echo       → Para iniciar la aplicación
echo.
echo    🔄 ActualizarApp
echo       → Para actualizar desde GitHub
echo.

set /p continuar="¿Continuar? (S/N): "
if /i not "%continuar%"=="S" if /i not "%continuar%"=="s" (
    echo Operación cancelada
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo.
echo 🔧 Creando scripts de lanzamiento...

:: Script de lanzamiento SIMPLE (sin caracteres especiales)
(
    echo @echo off
    echo title Facturacion Facil
    echo cd /d "%CARPETA_APP%"
    echo.
    echo :: Detectar Python
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo.
    echo :: Entorno virtual
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo.
    echo :: Lanzar aplicación
    echo echo 🚀 Iniciando Facturacion Facil...
    echo %%PYTHON%% main.py
    echo if errorlevel 1 pause
) > "IniciarApp.bat"

:: Script de actualización SIMPLE (sin caracteres especiales)
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Actualizar Facturacion Facil
    echo cd /d "%CARPETA_APP%"
    echo.
    echo echo 🔄 ACTUALIZAR FACTURACION FACIL
    echo echo.
    echo echo 📡 Buscando actualizaciones...
    echo git fetch origin ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Error Git o sin conexión
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 💾 Respaldo...
    echo if not exist "backup" mkdir backup
    echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul
    echo.
    echo echo 📥 Descargando...
    echo git pull origin main
    echo.
    echo echo 📦 Actualizando componentes...
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
    echo.
    echo echo ✅ Actualización completada!
    echo timeout /t 3 /nobreak ^>nul
) > "ActualizarApp.bat"

echo ✅ Scripts creados
echo.

:: MÉTODO 1: Copiar archivos .bat directamente al escritorio
echo 🖥️  MÉTODO 1: Copiando archivos .bat al escritorio...

copy "IniciarApp.bat" "%ESCRITORIO%\FacturacionFacil.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Archivo de inicio copiado al escritorio
) else (
    echo ❌ Error copiando archivo de inicio
)

copy "ActualizarApp.bat" "%ESCRITORIO%\ActualizarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Archivo de actualización copiado al escritorio
) else (
    echo ❌ Error copiando archivo de actualización
)

echo.

:: MÉTODO 2: Crear accesos directos .lnk con nombres simples
echo 🔗 MÉTODO 2: Creando accesos directos .lnk...

:: Acceso directo de lanzamiento (nombre simple, sin espacios ni caracteres especiales)
powershell -ExecutionPolicy Bypass -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%ESCRITORIO%\FacturacionFacil.lnk'); $s.TargetPath = '%CARPETA_APP%\IniciarApp.bat'; $s.WorkingDirectory = '%CARPETA_APP%'; $s.Description = 'Iniciar Facturacion Facil'; $s.Save(); Write-Host 'OK' } catch { Write-Host 'ERROR: ' + $_.Exception.Message }" 2>nul

if exist "%ESCRITORIO%\FacturacionFacil.lnk" (
    echo ✅ Acceso directo de inicio creado
) else (
    echo ❌ Error creando acceso directo de inicio
)

:: Acceso directo de actualización (nombre simple, sin espacios ni caracteres especiales)
powershell -ExecutionPolicy Bypass -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%ESCRITORIO%\ActualizarApp.lnk'); $s.TargetPath = '%CARPETA_APP%\ActualizarApp.bat'; $s.WorkingDirectory = '%CARPETA_APP%'; $s.Description = 'Actualizar Facturacion Facil'; $s.Save(); Write-Host 'OK' } catch { Write-Host 'ERROR: ' + $_.Exception.Message }" 2>nul

if exist "%ESCRITORIO%\ActualizarApp.lnk" (
    echo ✅ Acceso directo de actualización creado
) else (
    echo ❌ Error creando acceso directo de actualización
)

echo.

:: MÉTODO 3: Crear con VBScript como respaldo
echo 📜 MÉTODO 3: Creando con VBScript (respaldo)...

:: Script VBScript para lanzamiento
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO%\IniciarFacturacion.lnk"^)
    echo oShellLink.TargetPath = "%CARPETA_APP%\IniciarApp.bat"
    echo oShellLink.WorkingDirectory = "%CARPETA_APP%"
    echo oShellLink.Description = "Iniciar Facturacion Facil"
    echo oShellLink.Save
) > temp_iniciar.vbs

cscript //nologo temp_iniciar.vbs >nul 2>&1
if exist "%ESCRITORIO%\IniciarFacturacion.lnk" (
    echo ✅ Acceso directo VBScript de inicio creado
) else (
    echo ❌ Error acceso directo VBScript de inicio
)

:: Script VBScript para actualización
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO%\ActualizarFacturacion.lnk"^)
    echo oShellLink.TargetPath = "%CARPETA_APP%\ActualizarApp.bat"
    echo oShellLink.WorkingDirectory = "%CARPETA_APP%"
    echo oShellLink.Description = "Actualizar Facturacion Facil"
    echo oShellLink.Save
) > temp_actualizar.vbs

cscript //nologo temp_actualizar.vbs >nul 2>&1
if exist "%ESCRITORIO%\ActualizarFacturacion.lnk" (
    echo ✅ Acceso directo VBScript de actualización creado
) else (
    echo ❌ Error acceso directo VBScript de actualización
)

:: Limpiar archivos temporales
del temp_iniciar.vbs >nul 2>&1
del temp_actualizar.vbs >nul 2>&1

echo.

:: VERIFICACIÓN FINAL
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VERIFICACIÓN FINAL                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos creados en el escritorio (%ESCRITORIO%):
echo.

set TOTAL_ICONOS=0

:: Verificar todos los archivos posibles
if exist "%ESCRITORIO%\FacturacionFacil.bat" (
    echo ✅ FacturacionFacil.bat
    set /a TOTAL_ICONOS+=1
)

if exist "%ESCRITORIO%\ActualizarApp.bat" (
    echo ✅ ActualizarApp.bat
    set /a TOTAL_ICONOS+=1
)

if exist "%ESCRITORIO%\FacturacionFacil.lnk" (
    echo ✅ FacturacionFacil.lnk
    set /a TOTAL_ICONOS+=1
)

if exist "%ESCRITORIO%\ActualizarApp.lnk" (
    echo ✅ ActualizarApp.lnk
    set /a TOTAL_ICONOS+=1
)

if exist "%ESCRITORIO%\IniciarFacturacion.lnk" (
    echo ✅ IniciarFacturacion.lnk
    set /a TOTAL_ICONOS+=1
)

if exist "%ESCRITORIO%\ActualizarFacturacion.lnk" (
    echo ✅ ActualizarFacturacion.lnk
    set /a TOTAL_ICONOS+=1
)

echo.

if %TOTAL_ICONOS% GTR 0 (
    echo 🎉 ¡ÉXITO! %TOTAL_ICONOS% icono(s) creado(s) en el escritorio!
    echo.
    echo 💡 INSTRUCCIONES PARA EL USUARIO:
    echo    1. Mire en su escritorio (Desktop/Escritorio)
    echo    2. Debería ver archivos para Facturacion Facil
    echo    3. Haga doble clic en cualquiera para usar la aplicación
    echo.
    echo 🎯 ¡MISIÓN CUMPLIDA!
) else (
    echo ❌ ERROR: No se crearon iconos en el escritorio
    echo.
    echo 🚨 POSIBLES CAUSAS:
    echo    • Permisos insuficientes
    echo    • Antivirus bloqueando la creación
    echo    • Ejecutar como administrador
)

echo.
echo 🖥️  ¿Desea abrir el escritorio para ver los iconos? (S/N)
set /p abrir=
if /i "%abrir%"=="S" if /i "%abrir%"=="s" (
    explorer "%ESCRITORIO%"
)

echo.
echo 🔄 ¿Desea actualizar el escritorio (F5)? (S/N)
set /p actualizar=
if /i "%actualizar%"=="S" if /i "%actualizar%"=="s" (
    echo Actualizando escritorio...
    powershell -Command "[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.SendKeys]::SendWait('{F5}')"
)

echo.
pause
