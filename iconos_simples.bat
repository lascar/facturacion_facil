@echo off
chcp 65001 >nul
title Iconos Simples - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🖥️  ICONOS SIMPLES                       ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar directorio
if not exist "main.py" (
    echo ❌ ERROR: Ejecutar desde la carpeta de la aplicación
    pause
    exit /b 1
)

:: Rutas simples
set "APP=%CD%"
set "DESK=%USERPROFILE%\Desktop"

:: Probar Escritorio si Desktop no existe
if not exist "%DESK%" set "DESK=%USERPROFILE%\Escritorio"

echo 📁 Aplicación: %APP%
echo 🖥️  Escritorio: %DESK%
echo.

if not exist "%DESK%" (
    echo ❌ ERROR: No se encuentra el escritorio
    pause
    exit /b 1
)

echo 🎯 Creando iconos simples en el escritorio...
echo.

:: Crear scripts simples
echo 📝 Creando scripts...

:: Script 1: Iniciar (nombre muy simple)
(
    echo @echo off
    echo title Facturacion Facil
    echo cd /d "%APP%"
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo echo Iniciando aplicacion...
    echo %%PYTHON%% main.py
    echo if errorlevel 1 pause
) > "Iniciar.bat"

:: Script 2: Actualizar (nombre muy simple)
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Actualizar App
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
) > "Actualizar.bat"

echo ✅ Scripts creados
echo.

:: MÉTODO 1: Copiar archivos .bat directamente (más simple)
echo 🖥️  Copiando archivos al escritorio...

copy "Iniciar.bat" "%DESK%\Iniciar.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Iniciar.bat copiado
) else (
    echo ❌ Error copiando Iniciar.bat
)

copy "Actualizar.bat" "%DESK%\Actualizar.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Actualizar.bat copiado
) else (
    echo ❌ Error copiando Actualizar.bat
)

echo.

:: MÉTODO 2: Crear accesos directos con nombres ultra-simples
echo 🔗 Creando accesos directos...

:: Crear acceso directo 1 (nombre ultra-simple)
echo Set WshShell = CreateObject("WScript.Shell") > temp1.vbs
echo Set oShellLink = WshShell.CreateShortcut("%DESK%\App.lnk") >> temp1.vbs
echo oShellLink.TargetPath = "%APP%\Iniciar.bat" >> temp1.vbs
echo oShellLink.WorkingDirectory = "%APP%" >> temp1.vbs
echo oShellLink.Description = "Iniciar App" >> temp1.vbs
echo oShellLink.Save >> temp1.vbs

cscript //nologo temp1.vbs >nul 2>&1
if exist "%DESK%\App.lnk" (
    echo ✅ App.lnk creado
) else (
    echo ❌ Error creando App.lnk
)

:: Crear acceso directo 2 (nombre ultra-simple)
echo Set WshShell = CreateObject("WScript.Shell") > temp2.vbs
echo Set oShellLink = WshShell.CreateShortcut("%DESK%\Update.lnk") >> temp2.vbs
echo oShellLink.TargetPath = "%APP%\Actualizar.bat" >> temp2.vbs
echo oShellLink.WorkingDirectory = "%APP%" >> temp2.vbs
echo oShellLink.Description = "Actualizar App" >> temp2.vbs
echo oShellLink.Save >> temp2.vbs

cscript //nologo temp2.vbs >nul 2>&1
if exist "%DESK%\Update.lnk" (
    echo ✅ Update.lnk creado
) else (
    echo ❌ Error creando Update.lnk
)

:: Limpiar
del temp1.vbs >nul 2>&1
del temp2.vbs >nul 2>&1

echo.

:: MÉTODO 3: Crear con PowerShell (nombres ASCII puros)
echo ⚡ Método PowerShell...

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\Start.lnk'); $s.TargetPath = '%APP%\Iniciar.bat'; $s.WorkingDirectory = '%APP%'; $s.Save()" >nul 2>&1

if exist "%DESK%\Start.lnk" (
    echo ✅ Start.lnk creado
) else (
    echo ❌ Error creando Start.lnk
)

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\Upgrade.lnk'); $s.TargetPath = '%APP%\Actualizar.bat'; $s.WorkingDirectory = '%APP%'; $s.Save()" >nul 2>&1

if exist "%DESK%\Upgrade.lnk" (
    echo ✅ Upgrade.lnk creado
) else (
    echo ❌ Error creando Upgrade.lnk
)

echo.

:: VERIFICACIÓN
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VERIFICACIÓN                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos en el escritorio:
echo.

set TOTAL=0

if exist "%DESK%\Iniciar.bat" (
    echo ✅ Iniciar.bat
    set /a TOTAL+=1
)

if exist "%DESK%\Actualizar.bat" (
    echo ✅ Actualizar.bat
    set /a TOTAL+=1
)

if exist "%DESK%\App.lnk" (
    echo ✅ App.lnk
    set /a TOTAL+=1
)

if exist "%DESK%\Update.lnk" (
    echo ✅ Update.lnk
    set /a TOTAL+=1
)

if exist "%DESK%\Start.lnk" (
    echo ✅ Start.lnk
    set /a TOTAL+=1
)

if exist "%DESK%\Upgrade.lnk" (
    echo ✅ Upgrade.lnk
    set /a TOTAL+=1
)

echo.

if %TOTAL% GTR 0 (
    echo 🎉 ¡ÉXITO! %TOTAL% archivo(s) creado(s) en el escritorio
    echo.
    echo 💡 PARA EL USUARIO:
    echo    • Mire en su escritorio
    echo    • Haga doble clic en cualquier archivo para usar la app
    echo    • Los archivos .bat y .lnk hacen lo mismo
    echo.
    echo 🎯 ¡MISIÓN CUMPLIDA!
    echo.
    echo 📋 ARCHIVOS DISPONIBLES:
    echo    • Iniciar.bat / App.lnk / Start.lnk = Iniciar aplicación
    echo    • Actualizar.bat / Update.lnk / Upgrade.lnk = Actualizar app
) else (
    echo ❌ ERROR: No se crearon archivos en el escritorio
    echo.
    echo 💡 SOLUCIONES:
    echo    • Ejecutar como administrador
    echo    • Verificar permisos del escritorio
    echo    • Desactivar antivirus temporalmente
)

echo.
echo 🖥️  ¿Abrir escritorio para ver los archivos? (S/N)
set /p ver=
if /i "%ver%"=="S" if /i "%ver%"=="s" (
    explorer "%DESK%"
)

echo.
echo 🧪 ¿Probar uno de los archivos creados? (S/N)
set /p probar=
if /i "%probar%"=="S" if /i "%probar%"=="s" (
    if exist "%DESK%\Iniciar.bat" (
        echo Probando Iniciar.bat...
        start "" "%DESK%\Iniciar.bat"
    ) else if exist "%DESK%\App.lnk" (
        echo Probando App.lnk...
        start "" "%DESK%\App.lnk"
    ) else if exist "%DESK%\Start.lnk" (
        echo Probando Start.lnk...
        start "" "%DESK%\Start.lnk"
    ) else (
        echo No hay archivos para probar
    )
)

echo.
pause
