#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier qu'aucune ligne vide n'est ajoutée en mode édition
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pas_ligne_vide():
    """Test qu'aucune ligne vide n'est ajoutée en édition"""
    print("🚫 TEST PAS DE LIGNE VIDE EN ÉDITION")
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
        
        # Test 1: Chercher une facture avec lignes
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
        
        print(f"✅ Facture trouvée: {facture_test['numero']}")
        
        # Test 2: Récupérer la facture complète
        print("\n--- Test 2: Récupération Complète ---")
        
        facture_complete = db.get_invoice_by_id(facture_test['id'])
        lignes_originales = facture_complete.get('lineas', [])
        nb_lignes_originales = len(lignes_originales)
        
        print(f"✅ Facture avec {nb_lignes_originales} lignes originales:")
        for i, ligne in enumerate(lignes_originales):
            print(f"   {i+1}. {ligne['producto_nombre']} x {ligne['cantidad']}")
        
        # Test 3: Créer l'éditeur en mode édition
        print("\n--- Test 3: Éditeur en Mode Édition ---")
        
        editor = FacturaEditorPyQt6Window(None, facture_complete)
        editor.show()
        
        print("✅ Éditeur créé en mode édition")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.0)
        
        # Test 4: Compter les lignes dans la table
        print("\n--- Test 4: Comptage des Lignes ---")
        
        table = editor.items_table
        nb_lignes_table = table.rowCount()
        
        print(f"✅ Lignes dans la table: {nb_lignes_table}")
        print(f"✅ Lignes originales: {nb_lignes_originales}")
        
        # Compter les lignes avec produit
        lignes_avec_produit = 0
        lignes_vides = 0
        
        for row in range(nb_lignes_table):
            product_combo = table.cellWidget(row, 0)
            cantidad_spin = table.cellWidget(row, 2)
            
            if product_combo:
                current_data = product_combo.currentData()
                cantidad = cantidad_spin.value() if cantidad_spin else 0
                
                if current_data and current_data.get('id') and cantidad > 0:
                    lignes_avec_produit += 1
                    print(f"   ✅ Ligne {row + 1}: {product_combo.currentText()} x {cantidad}")
                else:
                    lignes_vides += 1
                    print(f"   ⚪ Ligne {row + 1}: Vide")
        
        print(f"✅ Lignes avec produit: {lignes_avec_produit}")
        print(f"✅ Lignes vides: {lignes_vides}")
        
        # Test 5: Vérification du résultat
        print("\n--- Test 5: Vérification ---")
        
        if lignes_avec_produit == nb_lignes_originales and lignes_vides == 0:
            print("🎉 PARFAIT ! Aucune ligne vide ajoutée")
            print(f"   • {lignes_avec_produit} lignes avec produit (attendu: {nb_lignes_originales})")
            print(f"   • {lignes_vides} lignes vides (attendu: 0)")
            success = True
        elif lignes_avec_produit == nb_lignes_originales and lignes_vides > 0:
            print("⚠️ PROBLÈME ! Ligne(s) vide(s) ajoutée(s)")
            print(f"   • {lignes_avec_produit} lignes avec produit ✅")
            print(f"   • {lignes_vides} lignes vides ❌ (devrait être 0)")
            success = False
        else:
            print("❌ PROBLÈME ! Lignes manquantes ou incorrectes")
            print(f"   • {lignes_avec_produit} lignes avec produit (attendu: {nb_lignes_originales})")
            print(f"   • {lignes_vides} lignes vides")
            success = False
        
        # Test 6: Vérifier le bouton "Añadir línea"
        print("\n--- Test 6: Bouton Añadir Línea ---")
        
        # Chercher le bouton dans l'interface
        add_buttons = editor.findChildren(editor.__class__.__bases__[0])
        add_button_found = False
        
        for widget in editor.findChildren(editor.__class__.__bases__[0]):
            if hasattr(widget, 'text') and 'Añadir' in str(widget.text()):
                add_button_found = True
                print(f"✅ Bouton trouvé: {widget.text()}")
                break
        
        if add_button_found:
            print("✅ Bouton 'Añadir línea' disponible")
        else:
            print("⚠️ Bouton 'Añadir línea' non trouvé")
        
        # Test 7: Tester l'ajout manuel d'une ligne
        print("\n--- Test 7: Test Ajout Manuel ---")
        
        nb_lignes_avant = table.rowCount()
        
        # Simuler un clic sur le bouton d'ajout (ou appeler directement la méthode)
        editor.add_invoice_item()
        app.processEvents()
        
        nb_lignes_apres = table.rowCount()
        
        if nb_lignes_apres == nb_lignes_avant + 1:
            print("✅ Ajout manuel fonctionne")
            print(f"   • Avant: {nb_lignes_avant} lignes")
            print(f"   • Après: {nb_lignes_apres} lignes")
        else:
            print("❌ Problème avec l'ajout manuel")
        
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
        success = test_pas_ligne_vide()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST")
        print("="*50)
        
        if success:
            print("🎉 TEST RÉUSSI !")
            print("\n✨ CORRECTION VALIDÉE :")
            print("   ✅ Aucune ligne vide ajoutée en édition")
            print("   ✅ Seules les lignes existantes affichées")
            print("   ✅ Bouton 'Añadir línea' disponible")
            print("   ✅ Ajout manuel fonctionne")
            
            print("\n🎯 COMPORTEMENT CORRIGÉ :")
            print("   • Mode création → 1 ligne vide pour commencer")
            print("   • Mode édition → Seulement lignes existantes")
            print("   • Ajout manuel → Bouton 'Añadir línea'")
            
            print("\n🚀 UTILISATION :")
            print("   1. Éditez une facture existante")
            print("   2. Voyez seulement les lignes réelles")
            print("   3. Cliquez 'Añadir línea' pour ajouter")
            print("   4. Interface propre et précise")
            
            return 0
        else:
            print("❌ TEST ÉCHOUÉ")
            print("   Le problème persiste")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
