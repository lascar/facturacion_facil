#!/usr/bin/env python3
"""
Test console pour vérifier que l'application fonctionne sans interface graphique
"""

import sys
import os

# Ajouter le répertoire au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester tous les imports"""
    print("🧪 Test des imports...")
    
    try:
        from database.database import db
        print("✅ Database OK")
    except Exception as e:
        print(f"❌ Database: {e}")
        return False
    
    try:
        from utils.logger import get_logger
        print("✅ Logger OK")
    except Exception as e:
        print(f"❌ Logger: {e}")
        return False
    
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        print("✅ PySide2 OK")
    except Exception as e:
        print(f"❌ PySide2: {e}")
        return False
    
    return True

def test_database():
    """Tester la base de données"""
    print("\n📊 Test de la base de données...")
    
    try:
        from database.database import db
        
        # Initialiser la base de données
        db.init_database()
        print("✅ Base de données initialisée")
        
        # Tester quelques opérations
        productos = db.get_all_productos()
        print(f"✅ Produits trouvés: {len(productos)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def test_gui_minimal():
    """Test minimal de l'interface graphique"""
    print("\n🖥️ Test minimal de l'interface...")
    
    try:
        import sys
        from PySide2.QtWidgets import QApplication
        
        # Créer l'application sans fenêtre
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        
        print("✅ QApplication créée")
        
        # Test de création de widget simple
        from PySide2.QtWidgets import QLabel
        label = QLabel("Test")
        print("✅ Widget créé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur interface: {e}")
        return False

def main():
    """Test principal"""
    print("🔍 DIAGNOSTIC FACTURACIÓN FÁCIL")
    print("="*40)
    
    # Test des imports
    if not test_imports():
        print("\n❌ Échec des imports")
        return 1
    
    # Test de la base de données
    if not test_database():
        print("\n❌ Échec base de données")
        return 1
    
    # Test GUI minimal
    if not test_gui_minimal():
        print("\n❌ Échec interface graphique")
        print("\n💡 Solutions possibles:")
        print("   export QT_QPA_PLATFORM=xcb")
        print("   export QT_X11_NO_MITSHM=1")
        print("   sudo apt install libxcb-xinerama0")
        return 1
    
    print("\n🎉 Tous les tests réussis!")
    print("💡 L'application devrait fonctionner")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
