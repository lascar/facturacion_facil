@echo off
chcp 65001 >nul
title Actualización Git - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🔄 ACTUALIZACIÓN DESDE GIT                              ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado
    echo.
    echo 📥 Opciones:
    echo    1. Instalar Git automáticamente
    echo    2. Descargar Git manualmente
    echo    3. Cancelar
    echo.
    set /p git_option="Seleccione opción (1/2/3): "
    
    if "%git_option%"=="1" (
        echo 🚀 Instalando Git...
        call :install_git
    ) else if "%git_option%"=="2" (
        echo 📥 Abriendo página de descarga de Git...
        start https://git-scm.com/download/win
        echo.
        echo ⚠️  Instale Git y ejecute este script nuevamente
        pause
        exit /b 1
    ) else (
        echo ❌ Operación cancelada
        pause
        exit /b 0
    )
)

echo ✅ Git disponible:
git --version

echo.
echo 🔍 Verificando estado del repositorio...

REM Verificar si estamos en un repositorio Git
if not exist ".git" (
    echo ❌ Este directorio no es un repositorio Git
    echo.
    echo 🔄 ¿Desea inicializar como repositorio Git?
    set /p init_git="(S/N): "
    if /i "%init_git%"=="S" (
        echo 🚀 Inicializando repositorio Git...
        git init
        echo ✅ Repositorio inicializado
    ) else (
        echo ❌ No se puede actualizar sin repositorio Git
        pause
        exit /b 1
    )
)

echo 📡 Verificando conexión con el repositorio remoto...

REM Verificar si hay un remoto configurado
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ⚠️  No hay repositorio remoto configurado
    echo.
    echo 🔗 ¿Desea configurar un repositorio remoto?
    set /p setup_remote="(S/N): "
    if /i "%setup_remote%"=="S" (
        set /p remote_url="Ingrese la URL del repositorio: "
        git remote add origin !remote_url!
        echo ✅ Repositorio remoto configurado
    ) else (
        echo ❌ No se puede actualizar sin repositorio remoto
        pause
        exit /b 1
    )
)

echo 💾 Creando respaldo de seguridad...

REM Crear backup antes de actualizar
set "BACKUP_DIR=backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "BACKUP_DIR=%BACKUP_DIR: =0%"

if not exist "backups" mkdir backups
echo 📦 Creando backup en: backups\%BACKUP_DIR%

REM Copiar archivos importantes
xcopy "config" "backups\%BACKUP_DIR%\config\" /E /I /Q >nul 2>&1
xcopy "base_de_datos" "backups\%BACKUP_DIR%\base_de_datos\" /E /I /Q >nul 2>&1
xcopy "data" "backups\%BACKUP_DIR%\data\" /E /I /Q >nul 2>&1

echo ✅ Backup creado

echo.
echo 🔄 Actualizando desde Git...

REM Verificar cambios locales
git status --porcelain >nul 2>&1
if not errorlevel 1 (
    for /f %%i in ('git status --porcelain') do (
        echo ⚠️  Hay cambios locales no guardados
        echo.
        echo 💾 Opciones:
        echo    1. Guardar cambios locales (stash)
        echo    2. Descartar cambios locales
        echo    3. Cancelar actualización
        echo.
        set /p changes_option="Seleccione opción (1/2/3): "
        
        if "!changes_option!"=="1" (
            echo 💾 Guardando cambios locales...
            git stash push -m "Backup antes de actualización %date% %time%"
            echo ✅ Cambios guardados
        ) else if "!changes_option!"=="2" (
            echo 🗑️ Descartando cambios locales...
            git reset --hard HEAD
            git clean -fd
            echo ✅ Cambios descartados
        ) else (
            echo ❌ Actualización cancelada
            pause
            exit /b 0
        )
        goto :continue_update
    )
)

:continue_update
echo 📥 Descargando actualizaciones...
git fetch origin

echo 🔄 Aplicando actualizaciones...
git pull origin main
if errorlevel 1 (
    echo ❌ Error al actualizar desde Git
    echo 🔄 Intentando con rama master...
    git pull origin master
    if errorlevel 1 (
        echo ❌ Error al actualizar. Verificando ramas disponibles...
        git branch -r
        echo.
        echo ⚠️  Especifique la rama manualmente o contacte al administrador
        pause
        exit /b 1
    )
)

echo ✅ Código actualizado desde Git

echo.
echo 🔧 Actualizando dependencias...

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔌 Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Actualizar dependencias
if exist "requirements.txt" (
    echo 📦 Actualizando dependencias...
    pip install -r requirements.txt --upgrade
    echo ✅ Dependencias actualizadas
)

echo.
echo ✅ ACTUALIZACIÓN COMPLETADA
echo.
echo 📋 Resumen:
echo    • Backup: Creado en backups\%BACKUP_DIR%
echo    • Código: Actualizado desde Git
echo    • Dependencias: Actualizadas
echo.
echo 🚀 La aplicación está lista para usar
echo.

pause
goto :eof

:install_git
echo 📥 Descargando Git para Windows...
if not exist "temp_install" mkdir temp_install
cd temp_install

powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git_installer.exe'}"

if exist "git_installer.exe" (
    echo ✅ Descarga completada
    echo 🔧 Instalando Git...
    git_installer.exe /VERYSILENT /NORESTART
    echo ✅ Git instalado
) else (
    echo ❌ Error al descargar Git
    start https://git-scm.com/download/win
)

cd ..
rmdir /s /q temp_install 2>nul
goto :eof
