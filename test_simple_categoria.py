#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour reproduire le problème de catégorie
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_simple():
    """Test simple du problème"""
    print("🧪 TEST SIMPLE PROBLÈME CATÉGORIE")
    print("=" * 35)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre principale
        main_window = MainWindowPyQt5()
        
        # Ouvrir la fenêtre des produits
        print("\n1️⃣ Ouverture fenêtre produits:")
        main_window.open_productos()
        productos_window = main_window.productos_window
        
        if not productos_window.productos:
            print("   ⚠️ Aucun produit - impossible de tester")
            return True
        
        # Sélectionner le premier produit
        print("\n2️⃣ Sélection du produit:")
        product = productos_window.productos[0]
        
        # Simuler la sélection comme un utilisateur réel
        productos_window.products_table.selectRow(0)
        productos_window.on_product_selected()
        
        combo = productos_window.categoria_combo
        expected = product.get('categoria')
        actual = combo.currentText()
        
        print(f"   📝 Produit: {product['nombre']}")
        print(f"   📝 Catégorie attendue: '{expected}'")
        print(f"   📝 Catégorie affichée: '{actual}'")
        print(f"   📝 Index combo: {combo.currentIndex()}")
        
        # Debug du combo
        print(f"   🔍 Options du combo:")
        for i in range(combo.count()):
            text = combo.itemText(i)
            marker = " ← SÉLECTIONNÉ" if i == combo.currentIndex() else ""
            print(f"      {i}: '{text}'{marker}")
        
        if expected and actual == expected:
            print("   ✅ SUCCÈS: Catégorie correctement affichée")
            return True
        elif not expected and not actual:
            print("   ✅ SUCCÈS: Pas de catégorie (normal)")
            return True
        else:
            print(f"   ❌ ÉCHEC: Attendu '{expected}', obtenu '{actual}'")
            return False
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def main():
    """Fonction principale"""
    print("🚀 TEST SIMPLE CATÉGORIE")
    print("=" * 25)
    
    success = test_simple()
    
    print(f"\n🎯 RÉSULTAT:")
    if success:
        print("   ✅ TEST RÉUSSI")
        print("   💡 La catégorie s'affiche correctement")
    else:
        print("   ❌ PROBLÈME CONFIRMÉ")
        print("   🔍 La catégorie ne s'affiche pas dans le combo")
    
    print(f"\n📋 POUR TESTER MANUELLEMENT:")
    print("   1. Lance: python3 main.py")
    print("   2. Clique sur 'Productos'")
    print("   3. Clique sur 'producto1' dans la liste de gauche")
    print("   4. Vérifie si 'cat1' apparaît dans le combo de droite")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
