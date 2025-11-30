@echo off
chcp 65001 >nul
title Detectar Escritorio - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔍 DETECTAR ESCRITORIO PERSONALIZADO         ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar directorio de la aplicación
if not exist "main.py" (
    echo ❌ ERROR: Ejecutar desde la carpeta de la aplicación
    pause
    exit /b 1
)

set "APP=%CD%"
echo 📁 Aplicación: %APP%
echo.

echo 🔍 Buscando el escritorio del usuario...
echo.

:: MÉTODO 1: Rutas estándar
echo 📋 Probando rutas estándar:
echo.

set "ESCRITORIO_ENCONTRADO=NO"
set "RUTA_ESCRITORIO="

:: Ruta estándar inglés
if exist "%USERPROFILE%\Desktop" (
    echo ✅ %USERPROFILE%\Desktop - EXISTE
    set "RUTA_ESCRITORIO=%USERPROFILE%\Desktop"
    set "ESCRITORIO_ENCONTRADO=SI"
) else (
    echo ❌ %USERPROFILE%\Desktop - NO EXISTE
)

:: Ruta estándar español
if exist "%USERPROFILE%\Escritorio" (
    echo ✅ %USERPROFILE%\Escritorio - EXISTE
    if "%ESCRITORIO_ENCONTRADO%"=="NO" (
        set "RUTA_ESCRITORIO=%USERPROFILE%\Escritorio"
        set "ESCRITORIO_ENCONTRADO=SI"
    )
) else (
    echo ❌ %USERPROFILE%\Escritorio - NO EXISTE
)

echo.

:: MÉTODO 2: Usar registro de Windows para encontrar el escritorio real
echo 🔍 Consultando registro de Windows...

for /f "tokens=3*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do (
    set "ESCRITORIO_REGISTRO=%%a %%b"
)

if defined ESCRITORIO_REGISTRO (
    echo ✅ Escritorio desde registro: %ESCRITORIO_REGISTRO%
    if exist "%ESCRITORIO_REGISTRO%" (
        echo ✅ Ruta del registro VÁLIDA
        set "RUTA_ESCRITORIO=%ESCRITORIO_REGISTRO%"
        set "ESCRITORIO_ENCONTRADO=SI"
    ) else (
        echo ❌ Ruta del registro NO VÁLIDA
    )
) else (
    echo ❌ No se pudo leer el registro
)

echo.

:: MÉTODO 3: Buscar manualmente en discos comunes
echo 🔍 Buscando manualmente en discos...

:: Buscar en D: (como en tu caso)
if exist "D:\disco principal\Escritorio" (
    echo ✅ D:\disco principal\Escritorio - ENCONTRADO
    set "RUTA_ESCRITORIO=D:\disco principal\Escritorio"
    set "ESCRITORIO_ENCONTRADO=SI"
)

if exist "D:\Escritorio" (
    echo ✅ D:\Escritorio - ENCONTRADO
    if "%ESCRITORIO_ENCONTRADO%"=="NO" (
        set "RUTA_ESCRITORIO=D:\Escritorio"
        set "ESCRITORIO_ENCONTRADO=SI"
    )
)

:: Buscar en C: con nombres alternativos
if exist "C:\Escritorio" (
    echo ✅ C:\Escritorio - ENCONTRADO
    if "%ESCRITORIO_ENCONTRADO%"=="NO" (
        set "RUTA_ESCRITORIO=C:\Escritorio"
        set "ESCRITORIO_ENCONTRADO=SI"
    )
)

if exist "C:\Desktop" (
    echo ✅ C:\Desktop - ENCONTRADO
    if "%ESCRITORIO_ENCONTRADO%"=="NO" (
        set "RUTA_ESCRITORIO=C:\Desktop"
        set "ESCRITORIO_ENCONTRADO=SI"
    )
)

echo.

:: MÉTODO 4: Permitir al usuario especificar manualmente
if "%ESCRITORIO_ENCONTRADO%"=="NO" (
    echo ❌ No se pudo detectar automáticamente el escritorio
    echo.
    echo 💡 Por favor, especifique la ruta manualmente:
    echo    Ejemplo: D:\disco principal\Escritorio
    echo.
    set /p "RUTA_MANUAL=Ruta del escritorio: "
    
    if exist "%RUTA_MANUAL%" (
        echo ✅ Ruta manual VÁLIDA: %RUTA_MANUAL%
        set "RUTA_ESCRITORIO=%RUTA_MANUAL%"
        set "ESCRITORIO_ENCONTRADO=SI"
    ) else (
        echo ❌ Ruta manual NO VÁLIDA: %RUTA_MANUAL%
        pause
        exit /b 1
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ ESCRITORIO DETECTADO                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎯 Escritorio encontrado: %RUTA_ESCRITORIO%
echo.

:: Crear scripts simples
echo 🔧 Creando scripts de la aplicación...

:: Script de inicio
(
    echo @echo off
    echo title Facturacion Facil
    echo cd /d "%APP%"
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo echo Iniciando Facturacion Facil...
    echo %%PYTHON%% main.py
    echo if errorlevel 1 pause
) > "IniciarApp.bat"

:: Script de actualización
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Actualizar Facturacion Facil
    echo cd /d "%APP%"
    echo echo Actualizando aplicacion...
    echo git fetch origin ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo Error: Git no disponible
    echo     pause
    echo     exit /b 1
    echo ^)
    echo if not exist "backup" mkdir backup
    echo if exist "facturacion.db" copy "facturacion.db" "backup\" ^>nul
    echo git pull origin main
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
    echo echo Actualizacion completada
    echo timeout /t 3 /nobreak ^>nul
) > "ActualizarApp.bat"

echo ✅ Scripts creados
echo.

:: Copiar al escritorio detectado
echo 🖥️  Copiando archivos al escritorio...

copy "IniciarApp.bat" "%RUTA_ESCRITORIO%\IniciarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ IniciarApp.bat copiado al escritorio
) else (
    echo ❌ Error copiando IniciarApp.bat
)

copy "ActualizarApp.bat" "%RUTA_ESCRITORIO%\ActualizarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ ActualizarApp.bat copiado al escritorio
) else (
    echo ❌ Error copiando ActualizarApp.bat
)

echo.

:: Crear accesos directos con VBScript (más compatible con rutas con espacios)
echo 🔗 Creando accesos directos...

:: Acceso directo de inicio
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%RUTA_ESCRITORIO%\Iniciar.lnk"^)
    echo oShellLink.TargetPath = "%APP%\IniciarApp.bat"
    echo oShellLink.WorkingDirectory = "%APP%"
    echo oShellLink.Description = "Iniciar Facturacion Facil"
    echo oShellLink.Save
) > temp_inicio.vbs

cscript //nologo temp_inicio.vbs >nul 2>&1
if exist "%RUTA_ESCRITORIO%\Iniciar.lnk" (
    echo ✅ Iniciar.lnk creado
) else (
    echo ❌ Error creando Iniciar.lnk
)

:: Acceso directo de actualización
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%RUTA_ESCRITORIO%\Actualizar.lnk"^)
    echo oShellLink.TargetPath = "%APP%\ActualizarApp.bat"
    echo oShellLink.WorkingDirectory = "%APP%"
    echo oShellLink.Description = "Actualizar Facturacion Facil"
    echo oShellLink.Save
) > temp_actualizar.vbs

cscript //nologo temp_actualizar.vbs >nul 2>&1
if exist "%RUTA_ESCRITORIO%\Actualizar.lnk" (
    echo ✅ Actualizar.lnk creado
) else (
    echo ❌ Error creando Actualizar.lnk
)

:: Limpiar archivos temporales
del temp_inicio.vbs >nul 2>&1
del temp_actualizar.vbs >nul 2>&1

echo.

:: Verificación final
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VERIFICACIÓN FINAL                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos en el escritorio (%RUTA_ESCRITORIO%):
echo.

set TOTAL=0

if exist "%RUTA_ESCRITORIO%\IniciarApp.bat" (
    echo ✅ IniciarApp.bat
    set /a TOTAL+=1
)

if exist "%RUTA_ESCRITORIO%\ActualizarApp.bat" (
    echo ✅ ActualizarApp.bat
    set /a TOTAL+=1
)

if exist "%RUTA_ESCRITORIO%\Iniciar.lnk" (
    echo ✅ Iniciar.lnk
    set /a TOTAL+=1
)

if exist "%RUTA_ESCRITORIO%\Actualizar.lnk" (
    echo ✅ Actualizar.lnk
    set /a TOTAL+=1
)

echo.

if %TOTAL% GTR 0 (
    echo 🎉 ¡ÉXITO! %TOTAL% archivo(s) creado(s) en el escritorio
    echo.
    echo 💡 PARA EL USUARIO:
    echo    • Mire en su escritorio: %RUTA_ESCRITORIO%
    echo    • Haga doble clic en IniciarApp.bat o Iniciar.lnk para usar la app
    echo    • Haga doble clic en ActualizarApp.bat o Actualizar.lnk para actualizar
    echo.
    echo 🎯 ¡MISIÓN CUMPLIDA!
) else (
    echo ❌ ERROR: No se crearon archivos en el escritorio
    echo.
    echo 💡 Verificar permisos de escritura en: %RUTA_ESCRITORIO%
)

echo.
echo 🖥️  ¿Abrir el escritorio para ver los archivos? (S/N)
set /p abrir=
if /i "%abrir%"=="S" if /i "%abrir%"=="s" (
    explorer "%RUTA_ESCRITORIO%"
)

echo.
pause
