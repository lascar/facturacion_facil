@echo off
chcp 65001 >nul
title Crear Package de Distribución - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    📦 CREAR PACKAGE DE DISTRIBUCIÓN                        ║
echo ║                         Facturación Fácil                                   ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🎯 Este script creará un package completo para distribución
echo    que incluye todos los scripts de instalación y la aplicación.
echo.

set /p create_package="¿Crear package de distribución? (S/N): "
if /i not "%create_package%"=="S" (
    echo ❌ Operación cancelada
    pause
    exit /b 0
)

echo.
echo 📦 Creando package de distribución...

REM Crear directorio de distribución
set "DIST_DIR=Facturacion_Facil_Distribucion_%date:~-4,4%%date:~-10,2%%date:~-7,2%"
set "DIST_DIR=%DIST_DIR: =0%"

if exist "%DIST_DIR%" (
    echo 🗑️ Eliminando package anterior...
    rmdir /s /q "%DIST_DIR%"
)

echo 📁 Creando directorio: %DIST_DIR%
mkdir "%DIST_DIR%"

echo 📋 Copiando archivos esenciales...

REM Copiar scripts de instalación
copy "configurar_sistema_completo.bat" "%DIST_DIR%\" >nul
copy "instalar_app.bat" "%DIST_DIR%\" >nul
copy "desinstalar_app.bat" "%DIST_DIR%\" >nul
copy "crear_iconos_acceso.bat" "%DIST_DIR%\" >nul
copy "crear_iconos_personalizados.bat" "%DIST_DIR%\" >nul
copy "actualizar_git_mejorado.bat" "%DIST_DIR%\" >nul
copy "test_sistema_instalacion.bat" "%DIST_DIR%\" >nul

REM Copiar scripts existentes importantes
copy "lancer_app.bat" "%DIST_DIR%\" >nul 2>&1
copy "lancer_rapide.bat" "%DIST_DIR%\" >nul 2>&1
copy "ActualizarAppMejorado.bat" "%DIST_DIR%\" >nul 2>&1

REM Copiar archivos de la aplicación
copy "main.py" "%DIST_DIR%\" >nul
copy "requirements.txt" "%DIST_DIR%\" >nul
copy "main.spec" "%DIST_DIR%\" >nul 2>&1

REM Copiar documentación
copy "SISTEMA_INSTALACION_COMPLETO.md" "%DIST_DIR%\" >nul
copy "README.md" "%DIST_DIR%\" >nul 2>&1
copy "NETTOYAGE_PYQT6_COMPLETE.md" "%DIST_DIR%\" >nul 2>&1

REM Copiar directorios importantes
echo 📁 Copiando directorios...
xcopy "ui" "%DIST_DIR%\ui\" /E /I /Q >nul 2>&1
xcopy "database" "%DIST_DIR%\database\" /E /I /Q >nul 2>&1
xcopy "common" "%DIST_DIR%\common\" /E /I /Q >nul 2>&1
xcopy "utils" "%DIST_DIR%\utils\" /E /I /Q >nul 2>&1
xcopy "config" "%DIST_DIR%\config\" /E /I /Q >nul 2>&1
xcopy "assets" "%DIST_DIR%\assets\" /E /I /Q >nul 2>&1
xcopy "data" "%DIST_DIR%\data\" /E /I /Q >nul 2>&1

REM Crear directorios vacíos necesarios
mkdir "%DIST_DIR%\logs" 2>nul
mkdir "%DIST_DIR%\pdfs" 2>nul
mkdir "%DIST_DIR%\base_de_datos" 2>nul
mkdir "%DIST_DIR%\facturas" 2>nul

REM Crear archivo README para el package
(
echo # 🚀 Facturación Fácil - Package de Distribución
echo.
echo ## 📋 Instalación Rápida
echo.
echo **Para instalar completamente la aplicación:**
echo ```
echo configurar_sistema_completo.bat
echo ```
echo.
echo **Para instalar paso a paso:**
echo ```
echo 1. instalar_app.bat
echo 2. crear_iconos_personalizados.bat
echo ```
echo.
echo ## 🧪 Verificación
echo.
echo **Para verificar que todo esté correcto:**
echo ```
echo test_sistema_instalacion.bat
echo ```
echo.
echo ## 📖 Documentación Completa
echo.
echo Ver: `SISTEMA_INSTALACION_COMPLETO.md`
echo.
echo ## 🎯 Contenido del Package
echo.
echo - ✅ Aplicación completa Facturación Fácil
echo - ✅ Scripts de instalación automática
echo - ✅ Scripts de creación de iconos
echo - ✅ Scripts de mantenimiento
echo - ✅ Documentación completa
echo - ✅ Estructura de directorios lista
echo.
echo **¡Todo listo para usar!** 🚀
) > "%DIST_DIR%\README_INSTALACION.md"

REM Crear script de inicio rápido
(
echo @echo off
echo chcp 65001 ^>nul
echo title Inicio Rápido - Facturación Fácil
echo.
echo echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo echo ║                    🚀 INICIO RÁPIDO                                        ║
echo echo ║                         Facturación Fácil                                   ║
echo echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo echo.
echo echo 🎯 Seleccione una opción:
echo echo.
echo echo    1. Configuración completa automática ^(recomendado^)
echo echo    2. Instalación paso a paso
echo echo    3. Solo crear iconos
echo echo    4. Verificar sistema
echo echo    5. Salir
echo echo.
echo set /p option="Seleccione opción (1-5): "
echo.
echo if "%%option%%"=="1" call configurar_sistema_completo.bat
echo if "%%option%%"=="2" call instalar_app.bat
echo if "%%option%%"=="3" call crear_iconos_personalizados.bat
echo if "%%option%%"=="4" call test_sistema_instalacion.bat
echo if "%%option%%"=="5" exit /b 0
echo.
echo pause
) > "%DIST_DIR%\INICIO_RAPIDO.bat"

echo.
echo ✅ PACKAGE DE DISTRIBUCIÓN CREADO
echo.
echo 📁 Ubicación: %DIST_DIR%\
echo.
echo 📋 Contenido del package:
echo    • Scripts de instalación completa
echo    • Aplicación Facturación Fácil
echo    • Scripts de creación de iconos
echo    • Scripts de mantenimiento
echo    • Documentación completa
echo    • Estructura de directorios
echo.
echo 🚀 Para distribuir:
echo    1. Comprima la carpeta %DIST_DIR%
echo    2. Distribuya el archivo ZIP
echo    3. El usuario solo necesita ejecutar INICIO_RAPIDO.bat
echo.
echo 💡 El package está listo para distribución profesional
echo.

REM Preguntar si crear ZIP
set /p create_zip="¿Crear archivo ZIP para distribución? (S/N): "
if /i "%create_zip%"=="S" (
    echo 📦 Creando archivo ZIP...
    powershell -Command "& {Compress-Archive -Path '%DIST_DIR%' -DestinationPath '%DIST_DIR%.zip' -Force}"
    if exist "%DIST_DIR%.zip" (
        echo ✅ Archivo ZIP creado: %DIST_DIR%.zip
        echo 📤 Listo para distribución
    ) else (
        echo ❌ Error al crear ZIP
    )
)

echo.
echo 🎉 ¡Package de distribución completado!
echo.

pause
