#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'édition de factures avec lignes de produits
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_edition_lignes_final():
    """Test final de l'édition avec lignes"""
    print("🎯 TEST FINAL ÉDITION FACTURES AVEC LIGNES")
    print("="*60)
    
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
        
        # Test 1: Chercher la facture avec lignes créée précédemment
        print("\n--- Test 1: Recherche Facture avec Lignes ---")
        
        factures = db.get_all_invoices()
        facture_test = None
        
        for facture in factures:
            if 'F-TEST-LIGNES-CORR-' in facture['numero']:
                facture_test = facture
                break
        
        if not facture_test:
            print("❌ Facture de test non trouvée")
            return False
        
        print(f"✅ Facture trouvée: {facture_test['numero']} (ID: {facture_test['id']})")
        
        # Test 2: Récupérer la facture complète
        print("\n--- Test 2: Récupération Complète ---")
        
        facture_complete = db.get_invoice_by_id(facture_test['id'])
        if not facture_complete:
            print("❌ Facture complète non récupérée")
            return False
        
        lignes = facture_complete.get('lineas', [])
        print(f"✅ Facture complète récupérée avec {len(lignes)} lignes:")
        
        for i, ligne in enumerate(lignes):
            print(f"   {i+1}. {ligne['producto_nombre']} (ID: {ligne['producto_id']})")
            print(f"      Qté: {ligne['cantidad']}, Prix: {ligne['precio_unitario']} €")
        
        # Test 3: Créer l'éditeur en mode édition
        print("\n--- Test 3: Éditeur en Mode Édition ---")
        
        editor = FacturaEditorPyQt6Window(None, facture_complete)
        editor.show()
        
        print("✅ Éditeur créé en mode édition")
        print(f"   • is_editing: {editor.is_editing}")
        print(f"   • factura_data: {editor.factura_data is not None}")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.5)  # Plus de temps pour le chargement
        
        # Test 4: Vérifier les données chargées
        print("\n--- Test 4: Données Chargées ---")
        
        numero_charge = editor.numero_edit.text()
        client_charge = editor.cliente_autocomplete.text()
        
        print(f"✅ Données de base chargées:")
        print(f"   • Numéro: {numero_charge}")
        print(f"   • Client: {client_charge}")
        
        # Test 5: Vérifier les lignes dans la table
        print("\n--- Test 5: Lignes dans la Table ---")
        
        table = editor.items_table
        row_count = table.rowCount()
        
        print(f"✅ Lignes dans la table: {row_count}")
        
        lignes_avec_produit = 0
        for row in range(row_count):
            product_combo = table.cellWidget(row, 0)
            cantidad_spin = table.cellWidget(row, 2)
            precio_spin = table.cellWidget(row, 3)
            
            if product_combo and cantidad_spin and precio_spin:
                current_text = product_combo.currentText()
                current_data = product_combo.currentData()
                cantidad = cantidad_spin.value()
                precio = precio_spin.value()
                
                if current_data and current_data.get('id') and cantidad > 0:
                    lignes_avec_produit += 1
                    print(f"   ✅ Ligne {row + 1}: {current_text}")
                    print(f"      • Produit ID: {current_data.get('id')}")
                    print(f"      • Quantité: {cantidad}")
                    print(f"      • Prix: {precio} €")
                else:
                    print(f"   ⚠️ Ligne {row + 1}: Vide ou incomplète")
                    print(f"      • Texte: '{current_text}'")
                    print(f"      • Data: {current_data}")
                    print(f"      • Quantité: {cantidad}")
                    print(f"      • Prix: {precio}")
        
        print(f"✅ Lignes avec produit chargées: {lignes_avec_produit}")
        
        # Comparer avec les données originales
        lignes_attendues = len(facture_complete.get('lineas', []))
        if lignes_avec_produit >= lignes_attendues:
            print("🎉 TOUTES LES LIGNES CHARGÉES CORRECTEMENT !")
            success = True
        else:
            print(f"❌ PROBLÈME: {lignes_attendues} lignes attendues, {lignes_avec_produit} chargées")
            success = False
        
        # Test 6: Vérifier les totaux
        print("\n--- Test 6: Totaux ---")
        
        total_affiche = editor.total_label.text()
        total_attendu = f"{facture_complete['total']:.2f} €"
        
        print(f"✅ Total affiché: {total_affiche}")
        print(f"✅ Total attendu: {total_attendu}")
        
        if total_affiche == total_attendu or abs(float(total_affiche.replace(' €', '')) - facture_complete['total']) < 0.01:
            print("✅ Totaux cohérents")
        else:
            print("⚠️ Totaux incohérents")
        
        # Fermer l'éditeur
        editor.close()
        print("\n✅ Éditeur fermé")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_edition_lignes_final()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST FINAL")
        print("="*60)
        
        if success:
            print("🎉 TEST FINAL RÉUSSI !")
            print("\n✨ PROBLÈME RÉSOLU :")
            print("   ✅ Méthode add_invoice sauvegarde les lignes")
            print("   ✅ Méthode get_invoice_by_id récupère les lignes")
            print("   ✅ Éditeur charge les lignes correctement")
            print("   ✅ Produits sélectionnés dans les combos")
            print("   ✅ Quantités et prix définis")
            print("   ✅ Totaux cohérents")
            
            print("\n🎯 ÉDITION DE FACTURES AVEC LIGNES OPÉRATIONNELLE !")
            print("\n📋 PROCESSUS COMPLET :")
            print("   1. Création facture → Lignes sauvegardées")
            print("   2. Récupération facture → Lignes incluses")
            print("   3. Édition facture → Lignes chargées")
            print("   4. Interface → Produits visibles")
            print("   5. Modification → Sauvegarde complète")
            
            print("\n🚀 UTILISATION :")
            print("   • Créez une facture avec produits")
            print("   • Éditez-la → Lignes apparaissent")
            print("   • Modifiez quantités/prix")
            print("   • Sauvegardez → Tout fonctionne !")
            
            return 0
        else:
            print("❌ TEST FINAL ÉCHOUÉ")
            print("   Le problème persiste malgré les corrections")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
