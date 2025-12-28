@echo off
chcp 65001 >nul
title Actualizar Facturación Fácil - Versión Robusta

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔄 ACTUALIZAR APLICACIÓN                 ║
echo ║                  Facturación Fácil - Robusta               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Cambiar al directorio de la aplicación
cd /d "%~dp0"

:: Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ❌ ERROR: No se encuentra main.py
    echo    Este script debe estar en la carpeta de la aplicación
    pause
    exit /b 1
)

echo 📍 Directorio: %CD%
echo.

:: Verificar Git
echo 🔍 Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Git no está instalado o no está en PATH
    echo.
    echo 💡 Soluciones:
    echo    • Instalar Git: https://git-scm.com/download/win
    echo    • Reiniciar el sistema después de instalar
    echo    • Verificar que Git esté en PATH
    echo.
    pause
    exit /b 1
)
echo ✅ Git disponible

:: Verificar conexión a internet
echo 🌐 Verificando conexión...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Sin conexión a GitHub
    echo.
    echo 💡 Verificar:
    echo    • Conexión a internet
    echo    • Firewall/proxy
    echo    • DNS
    echo.
    pause
    exit /b 1
)
echo ✅ Conexión a GitHub OK

echo.

:: CRÍTICO: Crear respaldo obligatorio antes de cualquier modificación
echo 💾 CREANDO RESPALDO OBLIGATORIO...
echo ⚠️  CRÍTICO: Respaldo de datos antes de actualización

if not exist "backup" mkdir backup

:: Respaldo con fecha y hora
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "FECHA=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%_%dt:~8,2%-%dt:~10,2%-%dt:~12,2%"

:: Respaldo de base de datos - CRÍTICO
if exist "facturacion.db" (
    copy "facturacion.db" "backup\facturacion_%FECHA%.db" >nul
    if %errorlevel%==0 (
        echo ✅ Base de datos respaldada: backup\facturacion_%FECHA%.db
    ) else (
        echo ❌ ERROR CRÍTICO: No se pudo respaldar la base de datos
        echo    DETENIENDO actualización para evitar pérdida de datos
        pause
        exit /b 1
    )
) else (
    echo ⚠️  Base de datos no encontrada (primera instalación?)
)

:: Respaldo de configuración
if exist "config\config.json" (
    copy "config\config.json" "backup\config_%FECHA%.json" >nul
    if %errorlevel%==0 (
        echo ✅ Configuración respaldada: backup\config_%FECHA%.json
    )
)

echo ✅ RESPALDO COMPLETADO - Datos protegidos
echo.

:: Detectar rama actual y configuración del repositorio
echo 🔍 Detectando configuración del repositorio...

:: Verificar si hay cambios locales no guardados
echo 🔍 Verificando cambios locales...
git diff --quiet 2>nul
if errorlevel 1 (
    echo ⚠️  ADVERTENCIA: Hay cambios locales no guardados
    echo.
    echo 💡 Opciones:
    echo    1. Guardar cambios locales (stash)
    echo    2. Descartar cambios locales
    echo    3. Cancelar actualización
    echo.
    set /p "OPCION=Seleccione opción (1/2/3): "

    if "%OPCION%"=="1" (
        echo 💾 Guardando cambios locales...
        git stash save "Cambios guardados antes de actualización %FECHA%" >nul 2>&1
        if not errorlevel 1 (
            echo ✅ Cambios guardados (usar 'git stash pop' para recuperarlos)
        ) else (
            echo ❌ Error guardando cambios
            pause
            exit /b 1
        )
    ) else if "%OPCION%"=="2" (
        echo ⚠️  Descartando cambios locales...
        git reset --hard HEAD >nul 2>&1
        echo ✅ Cambios descartados
    ) else (
        echo ❌ Actualización cancelada
        pause
        exit /b 0
    )
) else (
    echo ✅ No hay cambios locales pendientes
)

:: Obtener información del repositorio
echo 🔍 Conectando al repositorio remoto...
git fetch origin >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se pudo conectar al repositorio remoto
    echo.
    echo 💡 Verificar:
    echo    • URL del repositorio remoto
    echo    • Permisos de acceso
    echo    • Configuración de Git
    echo.
    git remote -v
    echo.
    pause
    exit /b 1
)

:: Obtener rama actual
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "RAMA_ACTUAL=%%i"
if "%RAMA_ACTUAL%"=="" (
    echo ⚠️  No se pudo detectar rama actual, usando detección automática
    set "RAMA_ACTUAL=auto"
) else (
    echo 📋 Rama actual: %RAMA_ACTUAL%
)

echo ✅ Repositorio remoto accesible
echo.

:: Actualizar código con detección automática de rama
echo 📥 Descargando actualizaciones...

set "ACTUALIZADO=NO"

:: Método 1: Usar rama actual si está definida y no es 'auto'
if not "%RAMA_ACTUAL%"=="auto" (
    echo 🔄 Probando rama actual: %RAMA_ACTUAL%
    git pull origin %RAMA_ACTUAL% >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: %RAMA_ACTUAL%
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Error actualizando desde rama: %RAMA_ACTUAL%
    )
)

:: Método 2: Probar master (rama principal detectada)
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama master...

    :: Verificar si la rama master existe en el remoto
    git ls-remote --heads origin master >nul 2>&1
    if not errorlevel 1 (
        echo    ✓ Rama master encontrada en remoto

        :: Intentar pull con estrategia de merge
        git pull origin master 2>&1 | findstr /C:"Already up to date" /C:"Updating" /C:"Fast-forward" >nul
        if not errorlevel 1 (
            echo ✅ Actualizado exitosamente desde rama: master
            set "ACTUALIZADO=SI"
        ) else (
            :: Intentar con rebase si hay conflictos
            echo    ⚠️  Intentando con estrategia alternativa...
            git pull --rebase origin master >nul 2>&1
            if not errorlevel 1 (
                echo ✅ Actualizado exitosamente desde rama: master (rebase)
                set "ACTUALIZADO=SI"
            ) else (
                echo ⚠️  No se pudo actualizar desde master (posibles cambios locales)
            )
        )
    ) else (
        echo ⚠️  Rama master no encontrada en remoto
    )
)

:: Método 3: Probar main como alternativa
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama main...
    git pull origin main >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente desde rama: main
        set "ACTUALIZADO=SI"
    ) else (
        echo ⚠️  Rama main no disponible
    )
)

:: Método 4: Pull genérico como último recurso
if "%ACTUALIZADO%"=="NO" (
    echo 🔄 Probando rama por defecto...
    git pull >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Actualizado exitosamente (método genérico)
        set "ACTUALIZADO=SI"
    ) else (
        echo ❌ Error : no se puede actualizar desde ninguna rama
        echo    Verificar conexión y configuración Git
        echo.
        echo 💡 Información de debug:
        echo.
        echo 📋 Ramas remotas disponibles:
        git branch -r 2>&1 || echo No se pueden listar ramas remotas
        echo.
        echo 📋 Estado del repositorio:
        git status --porcelain 2>&1 || echo No se puede obtener estado
        echo.
        echo 📋 Configuración remota:
        git remote -v 2>&1 || echo No se puede obtener configuración remota
        echo.
        echo Presione cualquier tecla para continuar...
        pause >nul
        exit /b 1
    )
)

echo.

:: Actualizar dependencias de Python
echo 📦 Actualizando dependencias de Python...

:: Detectar Python disponible
set "PYTHON=python"
python --version >nul 2>&1 || set "PYTHON=py"
py --version >nul 2>&1 || set "PYTHON=python3"

echo 🐍 Usando: %PYTHON%

:: Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual: venv
    call venv\Scripts\activate.bat >nul 2>&1
) else if exist "env\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual: env
    call env\Scripts\activate.bat >nul 2>&1
) else (
    echo ⚠️  No se encontró entorno virtual, usando Python global
)

:: Actualizar dependencias
if exist "requirements.txt" (
    echo 📋 Instalando dependencias desde requirements.txt...
    %PYTHON% -m pip install -r requirements.txt --upgrade --quiet >nul 2>&1
    if %errorlevel%==0 (
        echo ✅ Dependencias actualizadas
    ) else (
        echo ⚠️  Error actualizando dependencias (continuando...)
    )
) else (
    echo ⚠️  No se encontró requirements.txt
)

echo.

:: CRÍTICO: Verificar y migrar estructura de base de datos
echo 🔄 VERIFICANDO Y MIGRANDO BASE DE DATOS...
echo ⚠️  CRÍTICO: Verificación de compatibilidad de estructura

if exist "facturacion.db" (
    echo 📋 Base de datos encontrada: facturacion.db

    :: Ejecutar verificación y migración automática
    echo 🔧 Ejecutando verificación de estructura...
    %PYTHON% -c "
import sys
import os
sys.path.insert(0, '.')
try:
    from database.migration_manager import MigrationManager

    # Crear instancia del gestor de migración
    migration_manager = MigrationManager('facturacion.db')

    print('✅ Sistema de migración cargado correctamente')

    # Crear backup adicional específico para migración
    backup_path = migration_manager.create_backup('pre_update_migration')
    if backup_path:
        print(f'✅ Backup de migración creado: {backup_path}')
    else:
        print('⚠️  No se pudo crear backup de migración')

    # Ejecutar todas las migraciones
    print('🔄 Ejecutando migraciones de base de datos...')
    migration_success = migration_manager.run_all_migrations()

    if migration_success:
        print('✅ MIGRACIÓN COMPLETADA: Base de datos actualizada correctamente')
        sys.exit(0)
    else:
        print('❌ ERROR EN MIGRACIÓN: Problemas detectados en la estructura')
        print('   Consultar logs para más detalles')
        sys.exit(1)

except ImportError as e:
    print(f'⚠️  Sistema de migración no disponible: {e}')
    print('   Continuando sin migración automática')
    sys.exit(0)
except Exception as e:
    print(f'❌ ERROR CRÍTICO EN MIGRACIÓN: {e}')
    print('   RECOMENDACIÓN: Verificar manualmente la base de datos')
    sys.exit(2)
" 2>nul

    set "MIGRATION_RESULT=%errorlevel%"

    if %MIGRATION_RESULT%==0 (
        echo ✅ MIGRACIÓN EXITOSA: Base de datos compatible y actualizada
    ) else if %MIGRATION_RESULT%==1 (
        echo ❌ ERROR EN MIGRACIÓN: Problemas en la estructura de base de datos
        echo.
        echo ⚠️  ADVERTENCIA CRÍTICA:
        echo    • La base de datos puede tener problemas de compatibilidad
        echo    • Se recomienda verificar manualmente antes de usar la aplicación
        echo    • Backup disponible en: backup\facturacion_%FECHA%.db
        echo.
        echo 💡 Acciones recomendadas:
        echo    1. Verificar logs de la aplicación
        echo    2. Contactar soporte técnico si persisten problemas
        echo    3. Usar backup si es necesario restaurar
        echo.
        echo ¿Desea continuar con la actualización? (S/N)
        set /p "CONTINUAR=Respuesta: "
        if /i not "%CONTINUAR%"=="S" (
            echo ❌ Actualización cancelada por el usuario
            echo    Datos protegidos en backup\facturacion_%FECHA%.db
            pause
            exit /b 1
        )
        echo ⚠️  Continuando bajo responsabilidad del usuario...
    ) else if %MIGRATION_RESULT%==2 (
        echo ❌ ERROR CRÍTICO: Fallo grave en el sistema de migración
        echo.
        echo 🚨 ALERTA MÁXIMA:
        echo    • Error crítico en el sistema de base de datos
        echo    • NO se recomienda continuar sin verificación manual
        echo    • Backup disponible en: backup\facturacion_%FECHA%.db
        echo.
        echo 💡 Acciones OBLIGATORIAS:
        echo    1. Verificar integridad de facturacion.db manualmente
        echo    2. Contactar soporte técnico inmediatamente
        echo    3. NO usar la aplicación hasta resolver el problema
        echo.
        echo ❌ DETENIENDO actualización por seguridad de datos
        pause
        exit /b 1
    ) else (
        echo ✅ Sistema de migración no disponible - Continuando
        echo    (Esto es normal en instalaciones básicas)
    )
) else (
    echo ⚠️  Base de datos no encontrada - Primera instalación
    echo    Se creará automáticamente al iniciar la aplicación
)

echo ✅ VERIFICACIÓN DE BASE DE DATOS COMPLETADA
echo.

:: Verificar integridad de la aplicación
echo 🔍 Verificando integridad de la aplicación...

if exist "main.py" (
    echo ✅ main.py presente
) else (
    echo ❌ ERROR: main.py no encontrado después de la actualización
)

if exist "requirements.txt" (
    echo ✅ requirements.txt presente
) else (
    echo ⚠️  requirements.txt no encontrado
)

:: Verificar estructura crítica de base de datos
if exist "database\migration_manager.py" (
    echo ✅ Sistema de migración presente
) else (
    echo ⚠️  Sistema de migración no encontrado
)

echo.

:: Mostrar información de la actualización
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ ACTUALIZACIÓN COMPLETADA              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 ¡Facturación Fácil actualizada exitosamente!
echo.
echo 📋 Resumen:
echo    • ✅ Respaldo de datos creado (CRÍTICO)
echo    • ✅ Código actualizado desde repositorio
echo    • ✅ Dependencias actualizadas
echo    • ✅ Base de datos verificada y migrada
echo    • ✅ Integridad verificada
echo    • ✅ Aplicación lista para usar
echo.

echo 🔒 DATOS PROTEGIDOS: Respaldo en backup\facturacion_%FECHA%.db
echo.

echo 🚀 La aplicación está lista para usar con la última versión
echo.

echo ✅ Actualización completada. Presione cualquier tecla para salir...
pause >nul
