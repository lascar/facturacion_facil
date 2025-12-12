@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo 🧪 SUITE DE TESTS PRODUCTOS FACTURA
echo ====================================
echo.

REM Changer vers le répertoire du script
cd /d "%~dp0"

REM Vérifier que nous sommes dans le bon répertoire
if not exist "main.py" (
    echo ❌ ERROR: No se encuentra main.py
    echo 💡 Asegúrese de ejecutar este script desde el directorio raíz de la aplicación
    pause
    exit /b 1
)

REM Fonction pour détecter Python
call :detect_python
if !PYTHON_FOUND! == 0 (
    echo ❌ ERROR: Python no encontrado
    echo 💡 Instale Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado: !PYTHON_CMD!
echo.

REM Vérifier l'environnement virtuel
if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado
    set "PYTHON_CMD=venv\Scripts\python.exe"
) else (
    echo ⚠️  Entorno virtual no encontrado, usando Python del sistema
)

REM Menu de sélection
echo 📋 OPCIONES DE TESTS:
echo.
echo 1. Tests unitarios de productos
echo 2. Tests de integración de productos  
echo 3. Todos los tests de productos
echo 4. Test rápido (verificar corrección)
echo 5. Test con cobertura
echo 6. Ejecutar aplicación para test manual
echo 7. Ver logs de la aplicación
echo 8. Limpiar archivos de test
echo 9. Salir
echo.

set /p "choice=Seleccione una opción (1-9): "

if "%choice%"=="1" goto unit_tests
if "%choice%"=="2" goto integration_tests
if "%choice%"=="3" goto all_tests
if "%choice%"=="4" goto quick_test
if "%choice%"=="5" goto coverage_test
if "%choice%"=="6" goto manual_test
if "%choice%"=="7" goto view_logs
if "%choice%"=="8" goto cleanup
if "%choice%"=="9" goto end
goto invalid_choice

:unit_tests
echo.
echo 🧪 Ejecutando tests unitarios de productos...
echo ============================================
!PYTHON_CMD! test\scripts\run_productos_factura_tests.py unit
goto end

:integration_tests
echo.
echo 🔗 Ejecutando tests de integración de productos...
echo =================================================
!PYTHON_CMD! test\scripts\run_productos_factura_tests.py integration
goto end

:all_tests
echo.
echo 🚀 Ejecutando todos los tests de productos...
echo ============================================
!PYTHON_CMD! test\scripts\run_productos_factura_tests.py all
goto end

:quick_test
echo.
echo ⚡ Test rápido - Verificando corrección...
echo ========================================
echo 📦 Verificando productos en base de datos...
!PYTHON_CMD! test_productos_factura.py
echo.
echo 🎯 Ejecutando test unitario básico...
!PYTHON_CMD! -m pytest test\unit\test_productos_factura.py::TestProductosFactura::test_precio_venta_vs_precio -v
goto end

:coverage_test
echo.
echo 📊 Ejecutando tests con cobertura...
echo ===================================
!PYTHON_CMD! -m pytest test\unit\test_productos_factura.py test\integration\test_productos_factura_integration.py --cov=ui.facturas_pyqt5 --cov=database.database --cov-report=term-missing --cov-report=html
echo.
echo 📈 Reporte de cobertura HTML generado en: htmlcov\index.html
goto end

:manual_test
echo.
echo 🎮 Iniciando aplicación para test manual...
echo ==========================================
echo 💡 Instrucciones:
echo    1. Vaya a Gestión de Facturas
echo    2. Haga clic en 'Crear Nueva Factura'
echo    3. Verifique que aparecen productos en el dropdown
echo    4. Seleccione un producto y agregue a la factura
echo    5. Cierre la aplicación cuando termine
echo.
pause
!PYTHON_CMD! main.py
goto end

:view_logs
echo.
echo 📄 Mostrando logs recientes...
echo =============================
if exist "logs\facturacion_facil.log" (
    echo Últimas 50 líneas del log:
    echo -------------------------
    powershell "Get-Content logs\facturacion_facil.log -Tail 50"
) else (
    echo ❌ No se encontraron logs
)
echo.
pause
goto end

:cleanup
echo.
echo 🧹 Limpiando archivos de test...
echo ===============================
if exist "test_productos_factura.py" del "test_productos_factura.py"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "test\__pycache__" rmdir /s /q "test\__pycache__"
if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
echo ✅ Limpieza completada
goto end

:invalid_choice
echo ❌ Opción inválida. Seleccione un número del 1 al 9.
pause
goto end

:detect_python
set PYTHON_FOUND=0
set PYTHON_CMD=

REM Intentar py launcher primero
py --version >nul 2>&1
if !errorlevel! == 0 (
    set PYTHON_CMD=py
    set PYTHON_FOUND=1
    goto :eof
)

REM Intentar python3
python3 --version >nul 2>&1
if !errorlevel! == 0 (
    set PYTHON_CMD=python3
    set PYTHON_FOUND=1
    goto :eof
)

REM Intentar python
python --version >nul 2>&1
if !errorlevel! == 0 (
    echo import sys; print("OK") | python >nul 2>&1
    if !errorlevel! == 0 (
        set PYTHON_CMD=python
        set PYTHON_FOUND=1
        goto :eof
    )
)

goto :eof

:end
echo.
echo 🎉 Script terminado
pause
