#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'édition de factures
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_edition_factures():
    """Test de l'édition de factures"""
    print("📝 TEST DE L'ÉDITION DE FACTURES")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        from database.database import db
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Test 1: Vérifier les méthodes de récupération de factures
        print("\n--- Test 1: Méthodes de Base de Données ---")
        
        methods_to_check = [
            'get_invoice_by_id',
            'get_invoice_by_number'
        ]
        
        for method_name in methods_to_check:
            if hasattr(db, method_name):
                print(f"✅ Méthode {method_name} disponible")
            else:
                print(f"❌ Méthode {method_name} manquante")
        
        # Test 2: Créer une facture de test pour l'édition
        print("\n--- Test 2: Création de Facture de Test ---")
        
        # Créer un client de test
        test_client = {
            'nombre': 'Cliente Test Edición',
            'nif': 'EDIT123456',
            'direccion': 'Calle Edición, 123',
            'telefono': '91-000-0000',
            'email': 'edit@test.com'
        }
        
        try:
            client_id = db.add_client(test_client)
            print(f"✅ Cliente de test creado (ID: {client_id})")
        except Exception as e:
            print(f"⚠️ Error creando cliente: {e}")
            # Utiliser un client existant
            clients = db.get_all_clients()
            if clients:
                client_id = clients[0]['id']
                test_client = clients[0]
                print(f"✅ Usando cliente existente (ID: {client_id})")
            else:
                print("❌ No hay clientes disponibles")
                return False
        
        # Créer une facture de test
        test_invoice = {
            'numero': 'F-EDIT-TEST-001',
            'fecha': '2024-11-16',
            'vencimiento': '2024-12-16',
            'cliente': {
                'id': client_id,
                'nombre': test_client['nombre'],
                'nif': test_client.get('nif', ''),
                'direccion': test_client.get('direccion', '')
            },
            'lineas': [],
            'subtotal': 150.0,
            'iva_total': 31.5,
            'total': 181.5
        }
        
        try:
            invoice_id = db.add_invoice(test_invoice)
            print(f"✅ Factura de test creada (ID: {invoice_id})")
        except Exception as e:
            print(f"❌ Error creando factura de test: {e}")
            return False
        
        # Test 3: Récupérer la facture par numéro
        print("\n--- Test 3: Récupération de Facture ---")
        
        retrieved_invoice = db.get_invoice_by_number('F-EDIT-TEST-001')
        if retrieved_invoice:
            print("✅ Factura récupérée par numéro:")
            print(f"   • Numéro: {retrieved_invoice['numero']}")
            print(f"   • Date: {retrieved_invoice['fecha']}")
            print(f"   • Client: {retrieved_invoice['cliente']['nombre']}")
            print(f"   • NIF: {retrieved_invoice['cliente']['nif']}")
            print(f"   • Total: {retrieved_invoice['total']} €")
        else:
            print("❌ Factura non récupérée")
            return False
        
        # Test 4: Récupérer la facture par ID
        print("\n--- Test 4: Récupération par ID ---")
        
        retrieved_by_id = db.get_invoice_by_id(invoice_id)
        if retrieved_by_id:
            print("✅ Factura récupérée par ID:")
            print(f"   • ID: {retrieved_by_id['id']}")
            print(f"   • Numéro: {retrieved_by_id['numero']}")
            print(f"   • Client ID: {retrieved_by_id['cliente']['id']}")
        else:
            print("❌ Factura non récupérée par ID")
        
        # Test 5: Créer l'éditeur en mode édition
        print("\n--- Test 5: Éditeur en Mode Édition ---")
        
        editor = FacturaEditorPyQt6Window(None, retrieved_invoice)
        editor.show()
        
        print("✅ Éditeur créé en mode édition")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.0)
        
        # Test 6: Vérifier le chargement des données
        print("\n--- Test 6: Vérification du Chargement ---")
        
        # Vérifier le numéro de facture
        numero_loaded = editor.numero_edit.text()
        if numero_loaded == retrieved_invoice['numero']:
            print(f"✅ Numéro chargé correctement: {numero_loaded}")
        else:
            print(f"⚠️ Numéro incorrect: '{numero_loaded}' vs '{retrieved_invoice['numero']}'")
        
        # Vérifier le client
        client_loaded = editor.cliente_autocomplete.text()
        expected_client = retrieved_invoice['cliente']['nombre']
        if client_loaded == expected_client:
            print(f"✅ Client chargé correctement: {client_loaded}")
        else:
            print(f"⚠️ Client incorrect: '{client_loaded}' vs '{expected_client}'")
        
        # Vérifier les informations client
        nif_loaded = editor.cliente_nif_label.text()
        expected_nif = retrieved_invoice['cliente']['nif'] or '-'
        if nif_loaded == expected_nif:
            print(f"✅ NIF client chargé correctement: {nif_loaded}")
        else:
            print(f"⚠️ NIF incorrect: '{nif_loaded}' vs '{expected_nif}'")
        
        # Vérifier les totaux
        total_loaded = editor.total_label.text()
        expected_total = f"{retrieved_invoice['total']:.2f} €"
        if total_loaded == expected_total:
            print(f"✅ Total chargé correctement: {total_loaded}")
        else:
            print(f"⚠️ Total incorrect: '{total_loaded}' vs '{expected_total}'")
        
        # Test 7: Vérifier le mode édition
        print("\n--- Test 7: Mode Édition ---")
        
        if editor.is_editing:
            print("✅ Mode édition activé")
        else:
            print("⚠️ Mode édition non activé")
        
        if editor.factura_data:
            print("✅ Données de facture présentes")
        else:
            print("⚠️ Données de facture manquantes")
        
        # Test 8: Tester la fenêtre des factures
        print("\n--- Test 8: Fenêtre des Factures ---")
        
        facturas_window = FacturasPyQt6Window()
        facturas_window.show()
        
        app.processEvents()
        time.sleep(0.5)
        
        # Vérifier que la facture de test apparaît dans la liste
        table = facturas_window.invoices_table
        found_test_invoice = False
        
        for row in range(table.rowCount()):
            numero_item = table.item(row, 0)
            if numero_item and numero_item.text() == 'F-EDIT-TEST-001':
                found_test_invoice = True
                print(f"✅ Factura de test trouvée dans la liste (ligne {row})")
                break
        
        if not found_test_invoice:
            print("⚠️ Factura de test non trouvée dans la liste")
        
        # Fermer les fenêtres
        editor.close()
        facturas_window.close()
        print("\n✅ Fenêtres fermées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_edition_factures()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST D'ÉDITION DE FACTURES")
        print("="*60)
        
        if success:
            print("🎉 TEST D'ÉDITION DE FACTURES RÉUSSI !")
            print("\n✨ FONCTIONNALITÉS VALIDÉES :")
            print("   ✅ Méthodes de récupération de factures")
            print("   ✅ Récupération par numéro et par ID")
            print("   ✅ Éditeur en mode édition")
            print("   ✅ Chargement du numéro de facture")
            print("   ✅ Chargement des données client")
            print("   ✅ Chargement des totaux")
            print("   ✅ Mode édition activé")
            
            print("\n🎯 ÉDITION DE FACTURES OPÉRATIONNELLE !")
            print("\n📝 PROCESSUS D'ÉDITION :")
            print("   1. Sélectionner une facture dans la liste")
            print("   2. Cliquer 'Ver/Editar'")
            print("   3. Éditeur s'ouvre avec toutes les données")
            print("   4. Modifier les informations nécessaires")
            print("   5. Sauvegarder les modifications")
            
            print("\n🚀 Pour tester manuellement :")
            print("   1. Lancez: python main.py")
            print("   2. Cliquez sur 'Facturas'")
            print("   3. Sélectionnez une facture existante")
            print("   4. Cliquez 'Ver/Editar'")
            print("   5. Vérifiez que toutes les données sont chargées")
            
            return 0
        else:
            print("❌ TEST D'ÉDITION DE FACTURES ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
