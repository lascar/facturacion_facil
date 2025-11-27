#!/usr/bin/env python3
"""
Test PySide2 avec variables d'environnement
"""

import os
import sys

# Définir les variables d'environnement avant l'import
os.environ['QT_QPA_PLATFORM'] = 'xcb'
os.environ['QT_X11_NO_MITSHM'] = '1'
os.environ['QT_LOGGING_RULES'] = 'qt5ct.debug=false'

print("🔧 Variables d'environnement Qt définies")
print(f"QT_QPA_PLATFORM: {os.environ.get('QT_QPA_PLATFORM')}")
print(f"QT_X11_NO_MITSHM: {os.environ.get('QT_X11_NO_MITSHM')}")

try:
    print("🧪 Test import PySide2.QtCore...")
    from PySide2 import QtCore
    print("✅ QtCore OK")
    
    print("🧪 Test import PySide2.QtGui...")
    from PySide2 import QtGui
    print("✅ QtGui OK")
    
    print("🧪 Test import PySide2.QtWidgets...")
    from PySide2 import QtWidgets
    print("✅ QtWidgets OK")
    
    print("🧪 Test création QApplication...")
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    print("✅ QApplication OK")
    
    print("🎉 PySide2 fonctionne avec les variables d'environnement!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\n💡 Solutions alternatives:")
    print("1. pip install PyQt5")
    print("2. sudo apt install libxcb-*")
    print("3. Utiliser une interface web avec Flask")
