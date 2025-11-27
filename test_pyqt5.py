#!/usr/bin/env python3
"""
Test minimal PyQt5
"""

import sys
import os

print("🧪 Test PyQt5...")

try:
    print("📦 Import QtCore...")
    from PyQt5 import QtCore
    print("✅ QtCore OK")
    
    print("📦 Import QtGui...")
    from PyQt5 import QtGui
    print("✅ QtGui OK")
    
    print("📦 Import QtWidgets...")
    from PyQt5 import QtWidgets
    print("✅ QtWidgets OK")
    
    print("🖥️ Création QApplication...")
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    print("✅ QApplication OK")
    
    print("🏷️ Création QLabel...")
    label = QtWidgets.QLabel("Test PyQt5")
    print("✅ QLabel OK")
    
    print("🎉 PyQt5 fonctionne parfaitement!")
    
except Exception as e:
    print(f"❌ Erreur PyQt5: {e}")
    print("\n💡 Solutions:")
    print("sudo apt install python3-pyqt5")
    print("ou")
    print("pip install --upgrade PyQt5")
