#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de debug pour vérifier les données envoyées par l'interface de facture
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_debug_facture_interface():
    """Test de debug de l'interface de facture"""
    print("🔍 DEBUG INTERFACE FACTURE → STOCKS")
    print("="*50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        from database.database import db
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Vérifier les stocks initiaux
        products = db.get_all_products()
        print(f"\n📦 STOCKS INITIAUX:")
        for product in products:
            print(f"   • {product['nombre']} (ID: {product['id']}): {product.get('stock_actual', 0)} unités")
        
        # Créer l'éditeur de factures
        print("\n--- Test 1: Créer Éditeur de Factures ---")
        
        editor = FacturaEditorPyQt6Window()
        editor.show()
        
        print("✅ Éditeur de factures créé")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.0)
        
        # Simuler l'ajout d'un client
        print("\n--- Test 2: Ajouter Client ---")
        
        clients = db.get_all_clients()
        if clients:
            client = clients[0]
            editor.cliente_autocomplete.setText(client['nombre'])
            app.processEvents()
            time.sleep(0.2)
            editor.cliente_autocomplete.on_editing_finished()
            app.processEvents()
            time.sleep(0.2)
            print(f"✅ Client ajouté: {client['nombre']}")
        else:
            print("❌ Aucun client disponible")
            return False
        
        # Simuler l'ajout d'un produit
        print("\n--- Test 3: Ajouter Produit ---")
        
        if products:
            # Ajouter une ligne si nécessaire
            if editor.items_table.rowCount() == 0:
                editor.add_invoice_item()
                app.processEvents()
            
            # Sélectionner un produit dans la première ligne
            product_combo = editor.items_table.cellWidget(0, 0)
            cantidad_spin = editor.items_table.cellWidget(0, 2)
            precio_spin = editor.items_table.cellWidget(0, 3)
            
            if product_combo and cantidad_spin and precio_spin:
                # Chercher le produit dans le combo
                for i in range(product_combo.count()):
                    product_data = product_combo.itemData(i)
                    if product_data and product_data.get('id') == products[0]['id']:
                        product_combo.setCurrentIndex(i)
                        break
                
                # Définir quantité et prix
                cantidad_spin.setValue(3)  # Quantité de test
                precio_spin.setValue(20.0)  # Prix de test
                
                app.processEvents()
                time.sleep(0.5)
                
                print(f"✅ Produit ajouté: {products[0]['nombre']} x 3")
            else:
                print("❌ Widgets de ligne non trouvés")
                return False
        else:
            print("❌ Aucun produit disponible")
            return False
        
        # Test 4: Préparer les données de facture
        print("\n--- Test 4: Préparer Données de Facture ---")
        
        try:
            invoice_data = editor.prepare_invoice_data()
            
            if invoice_data:
                print("✅ Données de facture préparées:")
                print(f"   • Numéro: {invoice_data['numero']}")
                print(f"   • Client: {invoice_data['cliente']['nombre']}")
                print(f"   • Lignes: {len(invoice_data.get('lineas', []))}")
                
                # Analyser les lignes
                for i, ligne in enumerate(invoice_data.get('lineas', [])):
                    print(f"   • Ligne {i+1}:")
                    print(f"     - producto_id: {ligne.get('producto_id', 'MANQUANT')}")
                    print(f"     - cantidad: {ligne.get('cantidad', 'MANQUANT')}")
                    print(f"     - precio_unitario: {ligne.get('precio_unitario', 'MANQUANT')}")
                    print(f"     - total: {ligne.get('total', 'MANQUANT')}")
                
                # Vérifier si les données sont complètes pour les stocks
                lignes_valides = 0
                for ligne in invoice_data.get('lineas', []):
                    if ligne.get('producto_id') and ligne.get('cantidad', 0) > 0:
                        lignes_valides += 1
                
                print(f"   • Lignes valides pour stock: {lignes_valides}")
                
                if lignes_valides > 0:
                    print("✅ Données suffisantes pour mise à jour stock")
                    data_ok = True
                else:
                    print("❌ Données insuffisantes pour mise à jour stock")
                    data_ok = False
            else:
                print("❌ Aucune donnée de facture préparée")
                data_ok = False
                
        except Exception as e:
            print(f"❌ Erreur préparation données: {e}")
            data_ok = False
        
        # Test 5: Simuler la sauvegarde (sans vraiment sauvegarder)
        print("\n--- Test 5: Simulation Sauvegarde ---")
        
        if data_ok and invoice_data:
            print("🔄 Simulation de db.add_invoice()...")
            
            # Afficher ce qui serait envoyé à add_invoice
            print("📤 Données qui seraient envoyées:")
            print(f"   • invoice_data['lineas']: {len(invoice_data.get('lineas', []))} lignes")
            
            for i, ligne in enumerate(invoice_data.get('lineas', [])):
                print(f"   • Ligne {i+1} pour stock:")
                print(f"     - ID produit: {ligne.get('producto_id')}")
                print(f"     - Quantité: {ligne.get('cantidad')}")
                
                if ligne.get('producto_id') and ligne.get('cantidad', 0) > 0:
                    print(f"     ✅ Ligne valide pour diminuer stock")
                else:
                    print(f"     ❌ Ligne invalide pour stock")
            
            print("✅ Simulation terminée")
        
        # Fermer l'éditeur
        editor.close()
        print("\n✅ Éditeur fermé")
        
        return data_ok
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_debug_facture_interface()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU DEBUG")
        print("="*50)
        
        if success:
            print("🎉 DEBUG RÉUSSI !")
            print("\n✨ POINTS VALIDÉS :")
            print("   ✅ Interface de facture fonctionnelle")
            print("   ✅ Client ajouté correctement")
            print("   ✅ Produit ajouté avec quantité")
            print("   ✅ Données préparées correctement")
            print("   ✅ Lignes valides pour mise à jour stock")
            
            print("\n🔍 SI LES STOCKS NE DIMINUENT PAS :")
            print("   • Le problème n'est pas dans prepare_invoice_data()")
            print("   • Vérifier que save_invoice() appelle bien add_invoice()")
            print("   • Vérifier les logs lors de la sauvegarde")
            print("   • Tester avec une vraie sauvegarde")
            
            return 0
        else:
            print("❌ DEBUG ÉCHOUÉ")
            print("   Le problème est dans la préparation des données")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
