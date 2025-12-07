#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug spécifique pour le combo box des catégories
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.productos_pyqt5 import ProductosPyQt5Window
from database.database_improved import DatabaseImproved

def debug_categoria_combo():
    """Debug le combo box des catégories"""
    print("🔍 DEBUG COMBO BOX CATÉGORIES")
    print("=" * 35)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre
        window = ProductosPyQt5Window()
        
        print("\n1️⃣ État initial du combo:")
        combo = window.categoria_combo
        print(f"   📊 Nombre d'options: {combo.count()}")
        for i in range(combo.count()):
            text = combo.itemText(i)
            print(f"   📝 Option {i}: '{text}'")
        print(f"   📝 Texte actuel: '{combo.currentText()}'")
        print(f"   📝 Index actuel: {combo.currentIndex()}")
        
        print("\n2️⃣ Données produits chargées:")
        if window.productos:
            producto = window.productos[0]
            print(f"   📝 Produit: {producto.get('nombre')}")
            print(f"   📝 Catégorie du produit: '{producto.get('categoria')}'")
            print(f"   📝 Type: {type(producto.get('categoria'))}")
            
            print("\n3️⃣ Test de recherche dans le combo:")
            categoria = producto.get('categoria')
            if categoria:
                index = combo.findText(categoria)
                print(f"   📝 findText('{categoria}') = {index}")
                
                # Test avec strip
                categoria_stripped = categoria.strip()
                index_stripped = combo.findText(categoria_stripped)
                print(f"   📝 findText('{categoria_stripped}') = {index_stripped}")
                
                # Test case insensitive
                from PyQt5.QtCore import Qt
                index_case = combo.findText(categoria, Qt.MatchFixedString | Qt.MatchCaseSensitive)
                print(f"   📝 findText case sensitive = {index_case}")
                
                index_no_case = combo.findText(categoria, Qt.MatchFixedString)
                print(f"   📝 findText case insensitive = {index_no_case}")
            
            print("\n4️⃣ Simulation de sélection:")
            # Simuler la sélection du produit
            window.selected_producto_id = producto.get('id')
            
            print("   🔄 Avant load_product_data:")
            print(f"      Combo texte: '{combo.currentText()}'")
            print(f"      Combo index: {combo.currentIndex()}")
            
            # Charger les données
            window.load_product_data(producto)
            
            print("   🔄 Après load_product_data:")
            print(f"      Combo texte: '{combo.currentText()}'")
            print(f"      Combo index: {combo.currentIndex()}")
            
            # Vérifier si la catégorie est maintenant sélectionnée
            if combo.currentText() == categoria:
                print("   ✅ Catégorie correctement sélectionnée")
            else:
                print(f"   ❌ Problème: attendu '{categoria}', obtenu '{combo.currentText()}'")
        
        print("\n5️⃣ Test rechargement des catégories:")
        # Forcer le rechargement des catégories
        window.load_categories()
        
        print(f"   📊 Après rechargement - Nombre d'options: {combo.count()}")
        for i in range(combo.count()):
            text = combo.itemText(i)
            print(f"   📝 Option {i}: '{text}'")
        
        # Re-tester la sélection
        if window.productos:
            producto = window.productos[0]
            categoria = producto.get('categoria')
            if categoria:
                index = combo.findText(categoria)
                print(f"   📝 Après rechargement - findText('{categoria}') = {index}")
                
                if index >= 0:
                    combo.setCurrentIndex(index)
                    print(f"   ✅ Catégorie sélectionnée manuellement: '{combo.currentText()}'")
                else:
                    print(f"   ❌ Impossible de sélectionner la catégorie")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur debug: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_load_categories_method():
    """Test la méthode load_categories"""
    print("\n🔍 TEST MÉTHODE load_categories()")
    print("=" * 35)
    
    try:
        db = DatabaseImproved()
        
        # Test direct de get_product_categories
        categories = db.get_product_categories()
        print(f"   📊 DB get_product_categories(): {categories}")
        
        # Créer l'app et la fenêtre
        app = QApplication(sys.argv)
        window = ProductosPyQt5Window()
        
        # Vider le combo et le recharger manuellement
        combo = window.categoria_combo
        combo.clear()
        print(f"   📊 Combo vidé: {combo.count()} options")
        
        # Appeler load_categories
        window.load_categories()
        print(f"   📊 Après load_categories(): {combo.count()} options")
        
        for i in range(combo.count()):
            text = combo.itemText(i)
            print(f"   📝 Option {i}: '{text}'")
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur test load_categories: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DEBUG COMPLET COMBO CATÉGORIES")
    print("=" * 40)
    
    # Test 1: Méthode load_categories
    test1_ok = test_load_categories_method()
    
    # Test 2: Debug combo complet
    test2_ok = debug_categoria_combo()
    
    # Résumé
    print("\n🎯 RÉSUMÉ DEBUG:")
    print(f"   Test load_categories: {'✅ OK' if test1_ok else '❌ ÉCHEC'}")
    print(f"   Test combo complet: {'✅ OK' if test2_ok else '❌ ÉCHEC'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 DEBUG TERMINÉ")
        print("   Vérifier les détails ci-dessus pour identifier le problème")
    else:
        print("\n⚠️ ERREURS DÉTECTÉES")
    
    return test1_ok and test2_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
