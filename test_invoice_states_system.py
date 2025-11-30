#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système d'états de factures PyQt5
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from database.database import db
from utils.invoice_status_manager import invoice_status_manager

def test_database_connection():
    """Tester la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")
    try:
        conn = db.get_connection()
        if conn:
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print("❌ Échec de connexion à la base de données")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_invoice_status_manager():
    """Tester le gestionnaire d'états de factures"""
    print("\n🔍 Test du gestionnaire d'états de factures...")
    try:
        # Obtenir tous les états
        statuses = invoice_status_manager.get_all_statuses()
        print(f"✅ {len(statuses)} états trouvés:")
        
        for status in statuses:
            print(f"   - {status['nombre']}: {status['descripcion']} "
                  f"(Modifiable: {status['permite_modificacion']}, "
                  f"Couleur: {status['color']})")
        
        # Tester les permissions
        if statuses:
            first_status = statuses[0]
            can_modify = invoice_status_manager.can_modify_invoice(first_status['nombre'])
            print(f"✅ Test de permissions pour '{first_status['nombre']}': {can_modify}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur du gestionnaire d'états: {e}")
        return False

def test_organization_window():
    """Tester la fenêtre d'organisation avec états"""
    print("\n🔍 Test de la fenêtre d'organisation...")
    try:
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        window = OrganizacionPyQt5Window()
        
        # Vérifier que les composants d'états existent
        if hasattr(window, 'statuses_table'):
            print("✅ Table des états créée")
        else:
            print("❌ Table des états manquante")
            return False
            
        if hasattr(window, 'add_status_btn'):
            print("✅ Boutons d'états créés")
        else:
            print("❌ Boutons d'états manquants")
            return False
        
        # Tester le chargement des états
        window.load_invoice_statuses()
        row_count = window.statuses_table.rowCount()
        print(f"✅ {row_count} états chargés dans la table")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fenêtre d'organisation: {e}")
        return False

def test_invoice_status_dialog():
    """Tester le dialogue d'édition d'états"""
    print("\n🔍 Test du dialogue d'édition d'états...")
    try:
        from ui.invoice_status_dialog_pyqt5 import InvoiceStatusDialogPyQt5
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test création nouveau état
        dialog = InvoiceStatusDialogPyQt5()
        
        # Vérifier les composants
        if hasattr(dialog, 'name_edit') and hasattr(dialog, 'description_edit'):
            print("✅ Champs de saisie créés")
        else:
            print("❌ Champs de saisie manquants")
            return False
            
        if hasattr(dialog, 'allow_modification_cb') and hasattr(dialog, 'color_preview'):
            print("✅ Contrôles de configuration créés")
        else:
            print("❌ Contrôles de configuration manquants")
            return False
        
        # Test édition état existant
        test_status = {
            'id': 1,
            'nombre': 'Test Estado',
            'descripcion': 'Estado de prueba',
            'permite_modificacion': True,
            'color': '#ff0000',
            'orden': 1
        }
        
        edit_dialog = InvoiceStatusDialogPyQt5(None, test_status)
        if edit_dialog.name_edit.text() == 'Test Estado':
            print("✅ Chargement des données d'édition réussi")
        else:
            print("❌ Échec du chargement des données d'édition")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dialogue d'états: {e}")
        return False

def test_invoice_editor_integration():
    """Tester l'intégration dans l'éditeur de factures"""
    print("\n🔍 Test de l'intégration dans l'éditeur de factures...")
    try:
        # Créer une facture de test
        test_factura = {
            'id': 1,
            'numero': 'TEST-001',
            'fecha': '2024-01-01',
            'cliente': {'id': 1, 'nombre': 'Cliente Test'},
            'estado': 'Borrador',
            'lineas': []
        }
        
        from ui.facturas_pyqt5 import EditarFacturaDialog
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        dialog = EditarFacturaDialog(test_factura)
        
        # Vérifier que le combo d'état existe
        if hasattr(dialog, 'estado_combo'):
            print("✅ Combo d'état créé dans l'éditeur")
        else:
            print("❌ Combo d'état manquant dans l'éditeur")
            return False
        
        # Vérifier que la méthode de permissions existe
        if hasattr(dialog, 'update_permissions'):
            print("✅ Méthode de gestion des permissions créée")
        else:
            print("❌ Méthode de gestion des permissions manquante")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration éditeur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 DÉBUT DES TESTS DU SYSTÈME D'ÉTATS DE FACTURES")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_invoice_status_manager,
        test_organization_window,
        test_invoice_status_dialog,
        test_invoice_editor_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS ! Le système d'états est opérationnel.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
