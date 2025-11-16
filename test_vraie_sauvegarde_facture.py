#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'une vraie sauvegarde de facture via l'interface
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_vraie_sauvegarde_facture():
    """Test d'une vraie sauvegarde de facture"""
    print("💾 TEST VRAIE SAUVEGARDE FACTURE → STOCKS")
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
        product_test = products[0]  # Produit 001
        stock_initial = product_test.get('stock_actual', 0)
        
        print(f"\n📦 STOCK INITIAL:")
        print(f"   • {product_test['nombre']} (ID: {product_test['id']}): {stock_initial} unités")
        
        # Créer l'éditeur de factures
        print("\n--- Test 1: Créer et Remplir Facture ---")
        
        editor = FacturaEditorPyQt6Window()
        editor.show()
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.0)
        
        # Ajouter un client
        clients = db.get_all_clients()
        client = clients[0]
        editor.cliente_autocomplete.setText(client['nombre'])
        app.processEvents()
        time.sleep(0.2)
        editor.cliente_autocomplete.on_editing_finished()
        app.processEvents()
        time.sleep(0.2)
        
        print(f"✅ Client ajouté: {client['nombre']}")
        
        # Ajouter un produit
        if editor.items_table.rowCount() == 0:
            editor.add_invoice_item()
            app.processEvents()
        
        # Sélectionner le produit dans la première ligne
        product_combo = editor.items_table.cellWidget(0, 0)
        cantidad_spin = editor.items_table.cellWidget(0, 2)
        precio_spin = editor.items_table.cellWidget(0, 3)
        
        # Chercher le produit dans le combo
        for i in range(product_combo.count()):
            product_data = product_combo.itemData(i)
            if product_data and product_data.get('id') == product_test['id']:
                product_combo.setCurrentIndex(i)
                break
        
        # Définir quantité et prix
        test_quantity = 2  # Quantité de test
        cantidad_spin.setValue(test_quantity)
        precio_spin.setValue(25.0)
        
        app.processEvents()
        time.sleep(0.5)
        
        print(f"✅ Produit ajouté: {product_test['nombre']} x {test_quantity}")
        
        # Test 2: Sauvegarder la facture
        print("\n--- Test 2: Sauvegarde Réelle ---")
        
        print("🔄 Appel de save_invoice()...")
        
        try:
            # Appeler directement save_invoice
            editor.save_invoice()
            
            # Traiter les événements pour laisser le temps à la sauvegarde
            app.processEvents()
            time.sleep(1.0)
            
            print("✅ save_invoice() exécuté sans erreur")
            
        except Exception as e:
            print(f"❌ Erreur lors de save_invoice(): {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 3: Vérifier les stocks après sauvegarde
        print("\n--- Test 3: Vérification Stocks Après Sauvegarde ---")
        
        # Attendre un peu pour que la transaction soit commitée
        time.sleep(0.5)
        
        # Récupérer les stocks mis à jour
        products_after = db.get_all_products()
        product_after = next(p for p in products_after if p['id'] == product_test['id'])
        stock_after = product_after.get('stock_actual', 0)
        
        print(f"📦 STOCK APRÈS SAUVEGARDE:")
        print(f"   • {product_test['nombre']} (ID: {product_test['id']}): {stock_after} unités")
        print(f"   • Différence: {stock_after - stock_initial} (attendu: -{test_quantity})")
        
        # Vérifier si le stock a diminué
        expected_stock = max(0, stock_initial - test_quantity)
        
        if stock_after == expected_stock:
            print("🎉 STOCK DIMINUÉ CORRECTEMENT !")
            stock_success = True
        else:
            print("❌ PROBLÈME: Stock non diminué")
            stock_success = False
        
        # Test 4: Vérifier dans les logs
        print("\n--- Test 4: Vérification Logs ---")
        
        # Lire les dernières lignes du log
        try:
            with open('logs/facturacion_facil.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Chercher les lignes récentes liées aux stocks
            recent_stock_logs = []
            for line in lines[-20:]:  # 20 dernières lignes
                if 'stock' in line.lower() or 'movimiento' in line.lower():
                    recent_stock_logs.append(line.strip())
            
            if recent_stock_logs:
                print("📋 Logs récents liés aux stocks:")
                for log in recent_stock_logs:
                    print(f"   {log}")
            else:
                print("⚠️ Aucun log récent lié aux stocks trouvé")
                
        except Exception as e:
            print(f"⚠️ Impossible de lire les logs: {e}")
        
        # Fermer l'éditeur
        editor.close()
        print("\n✅ Éditeur fermé")
        
        return stock_success
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_vraie_sauvegarde_facture()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST VRAIE SAUVEGARDE")
        print("="*50)
        
        if success:
            print("🎉 TEST VRAIE SAUVEGARDE RÉUSSI !")
            print("\n✨ VALIDATION COMPLÈTE :")
            print("   ✅ Facture créée via interface")
            print("   ✅ Client et produit ajoutés")
            print("   ✅ Sauvegarde exécutée sans erreur")
            print("   ✅ Stock diminué automatiquement")
            print("   ✅ Relation stocks-factures opérationnelle")
            
            print("\n🎯 PROBLÈME RÉSOLU !")
            print("   La relation stocks-factures fonctionne correctement")
            print("   Les stocks diminuent automatiquement lors des ventes")
            
            return 0
        else:
            print("❌ TEST VRAIE SAUVEGARDE ÉCHOUÉ")
            print("\n🔍 PROBLÈME IDENTIFIÉ :")
            print("   • La sauvegarde ne diminue pas les stocks")
            print("   • Vérifier les logs pour plus de détails")
            print("   • Le problème est dans save_invoice() ou add_invoice()")
            
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
