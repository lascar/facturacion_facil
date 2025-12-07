#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'application réelle
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_app_real():
    """Test simple de l'application réelle"""
    print("🧪 TEST APPLICATION RÉELLE")
    print("=" * 30)
    
    # Setup
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    try:
        print("📱 Lancement application...")
        
        # Créer l'application
        main_window = MainWindowPyQt5()
        main_window.show()
        app.processEvents()
        time.sleep(1)
        
        print("✅ Application lancée")
        print("📋 Ouverture Facturas...")
        
        # Ouvrir facturas
        main_window.open_facturas()
        app.processEvents()
        time.sleep(1)
        
        print("✅ Facturas ouvert")
        print("\n🎯 INSTRUCTIONS UTILISATEUR:")
        print("1. Clique sur 'Nueva Factura'")
        print("2. Vérifie que le dialog s'ouvre AU PREMIER PLAN")
        print("3. Vérifie que le dialog ne se ferme PAS automatiquement")
        print("4. Ferme le dialog manuellement")
        print("5. Ferme l'application")
        print("\nAppuie sur Ctrl+C pour arrêter le test")
        
        # Laisser l'application tourner pour test manuel
        app.exec_()
        
        return True
        
    except KeyboardInterrupt:
        print("\n✅ Test arrêté par l'utilisateur")
        return True
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    success = test_app_real()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
