@echo off
chcp 65001 >nul
title Ubicación de Iconos - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📍 UBICACIÓN DE ICONOS                                  ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📁 Directorio actual: %CD%
echo.

echo 🔍 Verificando iconos existentes...
echo.

REM Verificar iconos en el directorio de la aplicación
echo 📋 ICONOS EN EL DIRECTORIO DE LA APLICACIÓN:
echo    Ubicación: %CD%
echo.

set "ICONOS_ENCONTRADOS=0"

if exist "🚀 Lanzar Facturación Fácil.lnk" (
    echo    ✅ 🚀 Lanzar Facturación Fácil.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 🚀 Lanzar Facturación Fácil.lnk
)

if exist "🔄 Actualizar desde Git.lnk" (
    echo    ✅ 🔄 Actualizar desde Git.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 🔄 Actualizar desde Git.lnk
)

if exist "🗑️ Desinstalar Aplicación.lnk" (
    echo    ✅ 🗑️ Desinstalar Aplicación.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 🗑️ Desinstalar Aplicación.lnk
)

if exist "🔧 Reinstalar Aplicación.lnk" (
    echo    ✅ 🔧 Reinstalar Aplicación.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 🔧 Reinstalar Aplicación.lnk
)

if exist "📊 Abrir Base de Datos.lnk" (
    echo    ✅ 📊 Abrir Base de Datos.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 📊 Abrir Base de Datos.lnk
)

if exist "📄 Ver PDFs Generados.lnk" (
    echo    ✅ 📄 Ver PDFs Generados.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 📄 Ver PDFs Generados.lnk
)

if exist "⚙️ Configuración.lnk" (
    echo    ✅ ⚙️ Configuración.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ ⚙️ Configuración.lnk
)

if exist "📝 Logs de la Aplicación.lnk" (
    echo    ✅ 📝 Logs de la Aplicación.lnk
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 📝 Logs de la Aplicación.lnk
)

REM Verificar iconos básicos
if exist "🚀 Lanzar App.lnk" (
    echo    ✅ 🚀 Lanzar App.lnk (versión básica)
    set /a ICONOS_ENCONTRADOS+=1
) else (
    echo    ❌ 🚀 Lanzar App.lnk (versión básica)
)

echo.
echo 📋 ICONOS EN EL ESCRITORIO:
echo    Ubicación: %USERPROFILE%\Desktop
echo.

if exist "%USERPROFILE%\Desktop\Facturación Fácil.lnk" (
    echo    ✅ Facturación Fácil.lnk
) else (
    echo    ❌ Facturación Fácil.lnk
)

if exist "%USERPROFILE%\Desktop\Actualizar Facturación Fácil.lnk" (
    echo    ✅ Actualizar Facturación Fácil.lnk
) else (
    echo    ❌ Actualizar Facturación Fácil.lnk
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📊 RESUMEN                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if %ICONOS_ENCONTRADOS% gtr 0 (
    echo ✅ Se encontraron %ICONOS_ENCONTRADOS% iconos
    echo.
    echo 📍 UBICACIONES DONDE ESTÁN LOS ICONOS:
    echo.
    echo    1. 📁 DIRECTORIO DE LA APLICACIÓN:
    echo       %CD%
    echo       • Aquí están todos los iconos principales
    echo       • Puede moverlos a cualquier ubicación
    echo       • Funcionan desde cualquier carpeta
    echo.
    echo    2. 🖥️ ESCRITORIO (si se crearon):
    echo       %USERPROFILE%\Desktop
    echo       • Iconos principales para acceso rápido
    echo.
    echo 💡 CÓMO USAR LOS ICONOS:
    echo    • Doble clic para ejecutar
    echo    • Arrastrar al escritorio para copiar
    echo    • Arrastrar a la barra de tareas para anclar
    echo    • Mover a cualquier carpeta
) else (
    echo ❌ No se encontraron iconos
    echo.
    echo 🔧 SOLUCIÓN: Crear los iconos
    echo.
    echo    Opciones disponibles:
    echo    1. crear_iconos_personalizados.bat  (iconos completos con emojis)
    echo    2. crear_iconos_acceso.bat          (iconos básicos)
    echo    3. instalar_app.bat                 (instalación completa con iconos)
    echo.
    echo 🚀 RECOMENDADO: Ejecutar crear_iconos_personalizados.bat
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🎯 ACCIONES DISPONIBLES                                 ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 1. Crear iconos personalizados (recomendado)
echo 2. Crear iconos básicos
echo 3. Mostrar esta información nuevamente
echo 4. Salir
echo.

set /p accion="Seleccione una opción (1-4): "

if "%accion%"=="1" (
    echo.
    echo 🎨 Ejecutando crear_iconos_personalizados.bat...
    call crear_iconos_personalizados.bat
) else if "%accion%"=="2" (
    echo.
    echo 🔧 Ejecutando crear_iconos_acceso.bat...
    call crear_iconos_acceso.bat
) else if "%accion%"=="3" (
    echo.
    echo 🔄 Actualizando información...
    goto :inicio
) else (
    echo.
    echo 👋 Saliendo...
)

echo.
echo 🎯 Proceso completado
pause
