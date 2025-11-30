#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du système d'états de factures
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester les imports"""
    print("🔍 Test des imports...")
    
    try:
        from database.database import db
        print("✅ Import database.db réussi")
    except Exception as e:
        print(f"❌ Erreur import database: {e}")
        return False
    
    try:
        from utils.invoice_status_manager import invoice_status_manager
        print("✅ Import invoice_status_manager réussi")
    except Exception as e:
        print(f"❌ Erreur import invoice_status_manager: {e}")
        return False
    
    try:
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        print("✅ Import OrganizacionPyQt5Window réussi")
    except Exception as e:
        print(f"❌ Erreur import OrganizacionPyQt5Window: {e}")
        return False
    
    try:
        from ui.invoice_status_dialog_pyqt5 import InvoiceStatusDialogPyQt5
        print("✅ Import InvoiceStatusDialogPyQt5 réussi")
    except Exception as e:
        print(f"❌ Erreur import InvoiceStatusDialogPyQt5: {e}")
        return False
    
    return True

def test_database():
    """Tester la base de données"""
    print("\n🔍 Test de la base de données...")
    
    try:
        from database.database import db
        
        # Test de connexion
        conn = db.get_connection()
        if conn:
            print("✅ Connexion base de données réussie")
        else:
            print("❌ Échec connexion base de données")
            return False
        
        # Test des états
        statuses = db.get_all_invoice_statuses()
        print(f"✅ {len(statuses)} états trouvés dans la base")
        
        for status in statuses[:3]:  # Afficher les 3 premiers
            print(f"   - {status.get('nombre', 'N/A')}: {status.get('descripcion', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def test_status_manager():
    """Tester le gestionnaire d'états"""
    print("\n🔍 Test du gestionnaire d'états...")
    
    try:
        from utils.invoice_status_manager import invoice_status_manager
        
        # Test get_all_statuses
        statuses = invoice_status_manager.get_all_statuses()
        print(f"✅ {len(statuses)} états récupérés via le manager")
        
        # Test can_modify_invoice
        if statuses:
            first_status = statuses[0]
            can_modify = invoice_status_manager.can_modify_invoice(first_status['nombre'])
            print(f"✅ Test permissions pour '{first_status['nombre']}': {can_modify}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestionnaire d'états: {e}")
        return False

def test_ui_components():
    """Tester les composants UI (sans affichage)"""
    print("\n🔍 Test des composants UI...")
    
    try:
        # Test du dialogue d'états
        from ui.invoice_status_dialog_pyqt5 import InvoiceStatusDialogPyQt5
        
        # Créer une instance sans parent (test de structure)
        dialog = InvoiceStatusDialogPyQt5()
        
        # Vérifier les attributs essentiels
        required_attrs = ['name_edit', 'description_edit', 'allow_modification_cb', 'color_preview']
        for attr in required_attrs:
            if hasattr(dialog, attr):
                print(f"✅ Attribut {attr} présent")
            else:
                print(f"❌ Attribut {attr} manquant")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur composants UI: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST SIMPLE DU SYSTÈME D'ÉTATS DE FACTURES")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_status_manager,
        test_ui_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 SYSTÈME D'ÉTATS OPÉRATIONNEL !")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Test terminé avec succès: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
