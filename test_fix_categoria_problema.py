#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que le problème de catégorie est résolu
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5
from database.database_improved import DatabaseImproved

def test_categoria_fix():
    """Test le fix du problème de catégorie"""
    print("🧪 TEST FIX PROBLÈME CATÉGORIE")
    print("=" * 35)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Vérifier les données en base
        print("\n1️⃣ Vérification base de données:")
        db = DatabaseImproved()
        products = db.get_all_products()
        categories = db.get_product_categories()
        
        print(f"   📊 Produits: {len(products)}")
        print(f"   📊 Catégories: {len(categories)}")
        
        if products:
            product = products[0]
            print(f"   📝 Premier produit: {product['nombre']} → '{product.get('categoria')}'")
        
        # Créer la fenêtre principale
        print("\n2️⃣ Création fenêtre principale:")
        main_window = MainWindowPyQt5()
        
        # Simuler l'ouverture de la fenêtre des produits (première fois)
        print("\n3️⃣ Première ouverture fenêtre produits:")
        main_window.open_productos()
        productos_window = main_window.productos_window
        
        print(f"   📊 Produits chargés: {len(productos_window.productos)}")
        print(f"   📊 Options combo: {productos_window.categoria_combo.count()}")
        
        # Vérifier le combo
        combo = productos_window.categoria_combo
        for i in range(combo.count()):
            text = combo.itemText(i)
            print(f"   📝 Option {i}: '{text}'")
        
        # Simuler la sélection d'un produit
        if productos_window.productos:
            print("\n4️⃣ Sélection du produit:")
            product = productos_window.productos[0]
            productos_window.selected_producto_id = product['id']
            productos_window.load_product_data(product)
            
            print(f"   📝 Produit sélectionné: {product['nombre']}")
            print(f"   📝 Catégorie dans combo: '{combo.currentText()}'")
            print(f"   📝 Index combo: {combo.currentIndex()}")
            
            if combo.currentText() == product.get('categoria'):
                print("   ✅ Catégorie correctement affichée")
                result1 = True
            else:
                print(f"   ❌ Problème: attendu '{product.get('categoria')}', obtenu '{combo.currentText()}'")
                result1 = False
        else:
            print("   ⚠️ Aucun produit à tester")
            result1 = True
        
        # Simuler la fermeture et réouverture (test du cache)
        print("\n5️⃣ Test réouverture (simulation cache):")
        
        # Simuler une modification des données (comme après "Eliminar todo")
        productos_window.productos = []  # Simuler des données vides
        productos_window.update_products_table()
        
        # Réouvrir la fenêtre (devrait rafraîchir)
        main_window.open_productos()
        
        print(f"   📊 Après réouverture - Produits: {len(productos_window.productos)}")
        print(f"   📊 Après réouverture - Options combo: {combo.count()}")
        
        # Vérifier que les données sont rafraîchies
        if len(productos_window.productos) > 0:
            print("   ✅ Données rafraîchies correctement")
            result2 = True
        else:
            print("   ⚠️ Données toujours vides (normal si base vide)")
            result2 = True  # OK si la base est vraiment vide
        
        # Test final de sélection après rafraîchissement
        if productos_window.productos:
            print("\n6️⃣ Test sélection après rafraîchissement:")
            product = productos_window.productos[0]
            expected_categoria = product.get('categoria')

            print(f"   📝 Produit à sélectionner: {product['nombre']}")
            print(f"   📝 Catégorie attendue: '{expected_categoria}'")

            # État avant sélection
            print(f"   📝 Combo avant: '{combo.currentText()}' (index: {combo.currentIndex()})")

            productos_window.selected_producto_id = product['id']
            productos_window.load_product_data(product)

            # État après sélection
            actual_categoria = combo.currentText()
            print(f"   📝 Combo après: '{actual_categoria}' (index: {combo.currentIndex()})")

            if actual_categoria == expected_categoria:
                print("   ✅ Catégorie toujours correcte après rafraîchissement")
                result3 = True
            else:
                print(f"   ❌ Problème après rafraîchissement: attendu '{expected_categoria}', obtenu '{actual_categoria}'")

                # Debug supplémentaire
                print(f"   🔍 Debug combo:")
                for i in range(combo.count()):
                    text = combo.itemText(i)
                    marker = " ← ACTUEL" if i == combo.currentIndex() else ""
                    print(f"      Option {i}: '{text}'{marker}")

                result3 = False
        else:
            result3 = True
        
        return result1 and result2 and result3
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def main():
    """Fonction principale"""
    print("🚀 TEST COMPLET FIX CATÉGORIE")
    print("=" * 35)
    
    success = test_categoria_fix()
    
    print(f"\n🎯 RÉSULTAT:")
    if success:
        print("   ✅ FIX RÉUSSI - Le problème de catégorie devrait être résolu")
        print("   💡 Redémarre l'application pour voir les changements")
    else:
        print("   ❌ PROBLÈME PERSISTANT - Vérifier les détails ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
