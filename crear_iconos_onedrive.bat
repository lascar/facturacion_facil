@echo off
chcp 65001 >nul
title Crear Iconos OneDrive - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🖥️  CREAR ICONOS ONEDRIVE ESCRITORIO         ║
echo ║                  Facturación Fácil                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar directorio de la aplicación
if not exist "main.py" (
    echo ❌ ERROR: Ejecutar desde la carpeta de la aplicación
    pause
    exit /b 1
)

:: Rutas específicas para tu configuración
set "APP=%CD%"
set "ESCRITORIO=D:\mis documentos\onedrive\escritorio"

echo 📁 Aplicación: %APP%
echo 🖥️  Escritorio OneDrive: %ESCRITORIO%
echo.

:: Verificar que el escritorio OneDrive existe
if not exist "%ESCRITORIO%" (
    echo ❌ ERROR: No se encuentra el escritorio OneDrive
    echo    Ruta esperada: %ESCRITORIO%
    echo.
    echo 💡 Verificar:
    echo    • Que OneDrive esté sincronizado
    echo    • Que la ruta sea correcta
    echo    • Que tenga permisos de acceso
    echo.
    pause
    exit /b 1
)

echo ✅ Escritorio OneDrive encontrado
echo.

echo 🎯 Creando iconos en el escritorio OneDrive...
echo.

:: Crear scripts simples
echo 📝 Creando scripts de la aplicación...

:: Script de inicio (nombre simple)
(
    echo @echo off
    echo title Facturacion Facil
    echo cd /d "%APP%"
    echo.
    echo :: Detectar Python
    echo set PYTHON=python
    echo python --version ^>nul 2^>^&1 ^|^| set PYTHON=py
    echo py --version ^>nul 2^>^&1 ^|^| set PYTHON=python3
    echo.
    echo :: Activar entorno virtual
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo.
    echo :: Iniciar aplicación
    echo echo 🚀 Iniciando Facturacion Facil...
    echo %%PYTHON%% main.py
    echo.
    echo :: Pausa si hay error
    echo if errorlevel 1 ^(
    echo     echo.
    echo     echo ❌ Error al iniciar la aplicación
    echo     pause
    echo ^)
) > "IniciarApp.bat"

:: Script de actualización (nombre simple)
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
    echo echo 📡 Verificando actualizaciones en GitHub...
    echo git fetch origin ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ❌ Error: Git no disponible o sin conexión
    echo     echo.
    echo     echo 💡 Soluciones:
    echo     echo    • Verificar conexión a internet
    echo     echo    • Instalar Git: https://git-scm.com/download/win
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 💾 Creando respaldo de datos...
    echo if not exist "backup" mkdir backup
    echo if exist "facturacion.db" copy "facturacion.db" "backup\facturacion_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db" ^>nul
    echo if exist "config.json" copy "config.json" "backup\" ^>nul
    echo echo ✅ Respaldo creado
    echo.
    echo echo 📥 Descargando actualizaciones...
    echo git pull origin main
    echo if errorlevel 1 ^(
    echo     echo ❌ Error al descargar actualizaciones
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo 📦 Actualizando dependencias...
    echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat ^>nul 2^>^&1
    echo if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat ^>nul 2^>^&1
    echo pip install -r requirements.txt --upgrade --quiet ^>nul 2^>^&1
    echo.
    echo echo ╔══════════════════════════════════════════════════════════════╗
    echo echo ║                    ✅ ACTUALIZACIÓN COMPLETADA              ║
    echo echo ╚══════════════════════════════════════════════════════════════╝
    echo echo.
    echo echo 🎉 Aplicación actualizada exitosamente
    echo echo 🚀 Ya puede usar la nueva versión
    echo echo.
    echo timeout /t 5 /nobreak ^>nul
) > "ActualizarApp.bat"

echo ✅ Scripts creados
echo.

:: MÉTODO 1: Copiar archivos .bat directamente al escritorio OneDrive
echo 🖥️  Copiando archivos al escritorio OneDrive...

copy "IniciarApp.bat" "%ESCRITORIO%\IniciarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ IniciarApp.bat copiado al escritorio
) else (
    echo ❌ Error copiando IniciarApp.bat
    echo    Verificar permisos en: %ESCRITORIO%
)

copy "ActualizarApp.bat" "%ESCRITORIO%\ActualizarApp.bat" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ ActualizarApp.bat copiado al escritorio
) else (
    echo ❌ Error copiando ActualizarApp.bat
    echo    Verificar permisos en: %ESCRITORIO%
)

echo.

:: MÉTODO 2: Crear accesos directos .lnk con VBScript (compatible con OneDrive)
echo 🔗 Creando accesos directos en OneDrive...

:: Acceso directo para iniciar (VBScript es más compatible con rutas con espacios)
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO%\Facturacion.lnk"^)
    echo oShellLink.TargetPath = "%APP%\IniciarApp.bat"
    echo oShellLink.WorkingDirectory = "%APP%"
    echo oShellLink.Description = "Iniciar Facturacion Facil"
    echo oShellLink.Save
) > temp_facturacion.vbs

echo    🚀 Creando acceso directo de inicio...
cscript //nologo temp_facturacion.vbs >nul 2>&1
if exist "%ESCRITORIO%\Facturacion.lnk" (
    echo ✅ Facturacion.lnk creado en OneDrive
) else (
    echo ❌ Error creando Facturacion.lnk
)

:: Acceso directo para actualizar
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%ESCRITORIO%\Actualizar.lnk"^)
    echo oShellLink.TargetPath = "%APP%\ActualizarApp.bat"
    echo oShellLink.WorkingDirectory = "%APP%"
    echo oShellLink.Description = "Actualizar Facturacion Facil"
    echo oShellLink.Save
) > temp_actualizar.vbs

echo    🔄 Creando acceso directo de actualización...
cscript //nologo temp_actualizar.vbs >nul 2>&1
if exist "%ESCRITORIO%\Actualizar.lnk" (
    echo ✅ Actualizar.lnk creado en OneDrive
) else (
    echo ❌ Error creando Actualizar.lnk
)

:: Limpiar archivos temporales
del temp_facturacion.vbs >nul 2>&1
del temp_actualizar.vbs >nul 2>&1

echo.

:: MÉTODO 3: Crear versiones adicionales con nombres alternativos
echo 📋 Creando versiones adicionales...

:: Copiar con nombres alternativos por si acaso
copy "IniciarApp.bat" "%ESCRITORIO%\Iniciar.bat" >nul 2>&1
if %errorlevel%==0 echo ✅ Iniciar.bat creado

copy "ActualizarApp.bat" "%ESCRITORIO%\Update.bat" >nul 2>&1
if %errorlevel%==0 echo ✅ Update.bat creado

echo.

:: Verificación final
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 VERIFICACIÓN FINAL                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos creados en OneDrive Escritorio:
echo    Ruta: %ESCRITORIO%
echo.

set TOTAL=0

if exist "%ESCRITORIO%\IniciarApp.bat" (
    echo ✅ IniciarApp.bat
    set /a TOTAL+=1
)

if exist "%ESCRITORIO%\ActualizarApp.bat" (
    echo ✅ ActualizarApp.bat
    set /a TOTAL+=1
)

if exist "%ESCRITORIO%\Facturacion.lnk" (
    echo ✅ Facturacion.lnk
    set /a TOTAL+=1
)

if exist "%ESCRITORIO%\Actualizar.lnk" (
    echo ✅ Actualizar.lnk
    set /a TOTAL+=1
)

if exist "%ESCRITORIO%\Iniciar.bat" (
    echo ✅ Iniciar.bat
    set /a TOTAL+=1
)

if exist "%ESCRITORIO%\Update.bat" (
    echo ✅ Update.bat
    set /a TOTAL+=1
)

echo.

if %TOTAL% GTR 0 (
    echo 🎉 ¡ÉXITO! %TOTAL% archivo(s) creado(s) en el escritorio OneDrive
    echo.
    echo 💡 INSTRUCCIONES PARA EL USUARIO:
    echo.
    echo    1. 🖥️  Abra su escritorio (OneDrive sincronizado)
    echo    2. 👀 Busque los archivos de Facturación Fácil
    echo    3. 🖱️  Haga doble clic para usar:
    echo.
    echo       🚀 INICIAR LA APLICACIÓN:
    echo          • IniciarApp.bat
    echo          • Facturacion.lnk  
    echo          • Iniciar.bat
    echo.
    echo       🔄 ACTUALIZAR LA APLICACIÓN:
    echo          • ActualizarApp.bat
    echo          • Actualizar.lnk
    echo          • Update.bat
    echo.
    echo 🎯 ¡MISIÓN CUMPLIDA!
    echo    Los iconos están ahora en su escritorio OneDrive
) else (
    echo ❌ ERROR: No se crearon archivos en el escritorio OneDrive
    echo.
    echo 🚨 POSIBLES CAUSAS:
    echo    • OneDrive no sincronizado completamente
    echo    • Permisos insuficientes en la carpeta OneDrive
    echo    • Antivirus bloqueando la creación de archivos
    echo.
    echo 💡 SOLUCIONES:
    echo    • Esperar que OneDrive termine de sincronizar
    echo    • Ejecutar como administrador
    echo    • Verificar configuración de OneDrive
)

echo.
echo 🖥️  ¿Desea abrir el escritorio OneDrive para ver los archivos? (S/N)
set /p abrir=
if /i "%abrir%"=="S" if /i "%abrir%"=="s" (
    echo 🚀 Abriendo escritorio OneDrive...
    explorer "%ESCRITORIO%"
)

echo.
echo 🧪 ¿Desea probar uno de los archivos creados? (S/N)
set /p probar=
if /i "%probar%"=="S" if /i "%probar%"=="s" (
    if exist "%ESCRITORIO%\IniciarApp.bat" (
        echo 🚀 Probando IniciarApp.bat...
        start "" "%ESCRITORIO%\IniciarApp.bat"
    ) else if exist "%ESCRITORIO%\Facturacion.lnk" (
        echo 🚀 Probando Facturacion.lnk...
        start "" "%ESCRITORIO%\Facturacion.lnk"
    ) else (
        echo ❌ No hay archivos para probar
    )
)

echo.
pause
