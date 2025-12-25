@echo off
REM Script de migration pour Windows
REM Importe les produits depuis 'Productos tienda.xls' vers la table 'products_shop'

echo.
echo ========================================================================
echo MIGRATION DE PRODUCTOS TIENDA
echo ========================================================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

REM Vérifier que xlrd est installé
python -c "import xlrd" >nul 2>&1
if errorlevel 1 (
    echo Installation du module xlrd...
    python -m pip install xlrd
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer xlrd
        pause
        exit /b 1
    )
)

REM Exécuter le script de migration
echo Execution de la migration...
echo.
python migracion_productos_shop.py

if errorlevel 1 (
    echo.
    echo ERREUR: La migration a echoue
    pause
    exit /b 1
) else (
    echo.
    echo Migration terminee avec succes!
    pause
    exit /b 0
)

