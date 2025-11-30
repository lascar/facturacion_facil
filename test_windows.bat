@echo off
echo ========================================
echo   Test Installation Windows 11
echo ========================================
echo.

REM Changer vers le repertoire du script
cd /d "%~dp0"

echo Test 1: Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ECHEC: Python non trouve
    echo Solution: Installer Python depuis python.org
    goto :error
) else (
    python --version
    echo ✅ Python OK
)
echo.

echo Test 2: Verification de l'environnement virtuel...
if not exist "venv\Scripts\python.exe" (
    echo ❌ ECHEC: Environnement virtuel non trouve
    echo Solution: Executer install.bat
    goto :error
) else (
    echo ✅ Environnement virtuel OK
)
echo.

echo Test 3: Activation de l'environnement...
call venv\Scripts\activate.bat
echo ✅ Environnement active
echo.

echo Test 4: Test des dependances...
python -c "import PyQt5; print('✅ PyQt5 OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: PyQt5 non installe
    goto :error
)

python -c "import reportlab; print('✅ ReportLab OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: ReportLab non installe
    goto :error
)

python -c "import PIL; print('✅ Pillow OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: Pillow non installe
    goto :error
)
echo.

echo Test 5: Test des modules de l'application...
python -c "from ui.base_pyqt5_window import BasePyQt5Window; print('✅ Interface de base OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: Module interface non trouve
    goto :error
)

python -c "from ui.scroll_mixin_pyqt5 import ScrollableMixin; print('✅ Scroll mixin OK')" 2>nul
if errorlevel 1 (
    echo ❌ ECHEC: Module scroll non trouve
    goto :error
)
echo.

echo Test 6: Test de lancement rapide (5 secondes)...
timeout /t 2 /nobreak >nul
python -c "
import sys
from PyQt5.QtWidgets import QApplication
from ui.base_pyqt5_window import BasePyQt5Window

app = QApplication(sys.argv)
window = BasePyQt5Window(title='Test Windows', enable_scroll=True)
window.show()
print('✅ Fenetre de test creee')

# Test du scroll
window.enable_window_scroll()
layout = window.get_content_layout()
print('✅ Scroll active')

window.close()
app.quit()
print('✅ Test interface OK')
" 2>nul

if errorlevel 1 (
    echo ❌ ECHEC: Erreur lors du test interface
    goto :error
)
echo.

echo ========================================
echo        🎉 TOUS LES TESTS PASSES!
echo ========================================
echo.
echo Installation Windows 11 validee:
echo ✅ Python installe et configure
echo ✅ Environnement virtuel fonctionnel
echo ✅ Toutes les dependances installees
echo ✅ Modules de l'application charges
echo ✅ Interface PyQt5 fonctionnelle
echo ✅ Scroll avec molette active
echo.
echo Tu peux maintenant utiliser:
echo - start.bat pour lancer l'application
echo - Scroll avec la molette dans Productos/Organizacion/Facturas
echo.
goto :end

:error
echo.
echo ========================================
echo           ❌ ECHEC DU TEST
echo ========================================
echo.
echo Solutions:
echo 1. Executer install.bat pour installer/reparer
echo 2. Verifier que Python est dans le PATH
echo 3. Executer en tant qu'administrateur
echo 4. Consulter INSTALLATION_WINDOWS11.md
echo.

:end
pause
