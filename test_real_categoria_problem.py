#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test réaliste du problème de catégorie
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_real_scenario():
    """Test le scénario réel d'utilisation"""
    print("🧪 TEST SCÉNARIO RÉEL - PROBLÈME CATÉGORIE")
    print("=" * 45)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre principale
        print("\n1️⃣ Création application principale:")
        main_window = MainWindowPyQt5()
        
        # Première ouverture de la fenêtre des produits
        print("\n2️⃣ Première ouverture fenêtre produits:")
        main_window.open_productos()
        productos_window = main_window.productos_window
        
        print(f"   📊 Produits chargés: {len(productos_window.productos)}")
        
        if not productos_window.productos:
            print("   ⚠️ Aucun produit - impossible de tester")
            return True
        
        # Sélectionner le premier produit
        print("\n3️⃣ Sélection du premier produit:")
        product = productos_window.productos[0]
        
        # Simuler la sélection via la table (comme un vrai utilisateur)
        productos_window.products_table.selectRow(0)
        productos_window.on_product_selected()
        
        combo = productos_window.categoria_combo
        print(f"   📝 Produit: {product['nombre']}")
        print(f"   📝 Catégorie produit: '{product.get('categoria')}'")
        print(f"   📝 Catégorie combo: '{combo.currentText()}'")
        print(f"   📝 Index combo: {combo.currentIndex()}")
        
        # Vérifier que la catégorie s'affiche
        expected_categoria = product.get('categoria')
        actual_categoria = combo.currentText()
        
        if expected_categoria and actual_categoria == expected_categoria:
            print("   ✅ Catégorie correctement affichée")
            result1 = True
        elif not expected_categoria and not actual_categoria:
            print("   ✅ Pas de catégorie (normal)")
            result1 = True
        else:
            print(f"   ❌ Problème: attendu '{expected_categoria}', obtenu '{actual_categoria}'")
            result1 = False
        
        # Fermer la fenêtre
        print("\n4️⃣ Fermeture de la fenêtre:")
        productos_window.hide()
        
        # Réouvrir la fenêtre (scénario réel)
        print("\n5️⃣ Réouverture de la fenêtre:")
        main_window.open_productos()  # Ceci devrait rafraîchir les données
        
        print(f"   📊 Produits après réouverture: {len(productos_window.productos)}")
        
        # Re-sélectionner le même produit
        if productos_window.productos:
            print("\n6️⃣ Re-sélection du produit:")
            product = productos_window.productos[0]
            
            # Simuler la sélection via la table
            productos_window.products_table.selectRow(0)
            productos_window.on_product_selected()
            
            print(f"   📝 Produit: {product['nombre']}")
            print(f"   📝 Catégorie produit: '{product.get('categoria')}'")
            print(f"   📝 Catégorie combo: '{combo.currentText()}'")
            print(f"   📝 Index combo: {combo.currentIndex()}")
            
            # Vérifier que la catégorie s'affiche toujours
            expected_categoria = product.get('categoria')
            actual_categoria = combo.currentText()
            
            if expected_categoria and actual_categoria == expected_categoria:
                print("   ✅ Catégorie toujours correcte après réouverture")
                result2 = True
            elif not expected_categoria and not actual_categoria:
                print("   ✅ Pas de catégorie (normal)")
                result2 = True
            else:
                print(f"   ❌ Problème après réouverture: attendu '{expected_categoria}', obtenu '{actual_categoria}'")
                
                # Debug détaillé
                print(f"   🔍 Debug combo après réouverture:")
                for i in range(combo.count()):
                    text = combo.itemText(i)
                    marker = " ← ACTUEL" if i == combo.currentIndex() else ""
                    print(f"      Option {i}: '{text}'{marker}")
                
                result2 = False
        else:
            print("   ⚠️ Aucun produit après réouverture")
            result2 = True
        
        return result1 and result2
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def main():
    """Fonction principale"""
    print("🚀 TEST RÉALISTE PROBLÈME CATÉGORIE")
    print("=" * 40)
    
    success = test_real_scenario()
    
    print(f"\n🎯 RÉSULTAT FINAL:")
    if success:
        print("   ✅ TEST RÉUSSI")
        print("   💡 Le problème de catégorie devrait être résolu")
        print("   🔄 Redémarre l'application pour voir les changements")
    else:
        print("   ❌ PROBLÈME DÉTECTÉ")
        print("   🔍 Vérifier les détails du debug ci-dessus")
    
    print(f"\n📋 INSTRUCTIONS POUR TESTER:")
    print("   1. Lance l'application: python3 main.py")
    print("   2. Clique sur 'Productos'")
    print("   3. Clique sur un produit dans la liste de gauche")
    print("   4. Vérifie que la catégorie apparaît dans le combo de droite")
    print("   5. Ferme la fenêtre et rouvre-la")
    print("   6. Re-sélectionne le même produit")
    print("   7. La catégorie devrait toujours s'afficher")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
