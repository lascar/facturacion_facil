#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique pour l'interface des produits et l'affichage des catégories
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.productos_pyqt5 import ProductosPyQt5Window
from database.database_improved import DatabaseImproved

def test_interface_productos():
    """Test l'interface des produits"""
    print("🧪 TEST INTERFACE PRODUITS - CATÉGORIES")
    print("=" * 45)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre des produits
        print("\n1️⃣ Création de l'interface produits...")
        window = ProductosPyQt5Window()
        
        # Vérifier les données chargées
        print(f"\n2️⃣ Données chargées:")
        print(f"   📊 Nombre de produits: {len(window.productos)}")
        
        if window.productos:
            for i, producto in enumerate(window.productos):
                print(f"   📝 Produit {i+1}: {producto.get('nombre')} → Catégorie: '{producto.get('categoria')}'")
        
        # Vérifier le combo des catégories
        print(f"\n3️⃣ Combo catégories:")
        combo = window.categoria_combo
        print(f"   📊 Nombre d'options: {combo.count()}")
        
        for i in range(combo.count()):
            text = combo.itemText(i)
            print(f"   📝 Option {i}: '{text}'")
        
        # Simuler la sélection d'un produit
        print(f"\n4️⃣ Test sélection produit:")
        if window.productos:
            # Sélectionner le premier produit
            window.selected_producto_id = window.productos[0]['id']
            window.load_product_data(window.productos[0])
            
            # Vérifier les valeurs dans le formulaire
            print(f"   📝 Nom: '{window.nombre_edit.text()}'")
            print(f"   📝 Catégorie sélectionnée: '{window.categoria_combo.currentText()}'")
            print(f"   📝 Index catégorie: {window.categoria_combo.currentIndex()}")
        
        # Vérifier la table
        print(f"\n5️⃣ Table des produits:")
        table = window.products_table
        print(f"   📊 Lignes dans la table: {table.rowCount()}")
        
        if table.rowCount() > 0:
            # Vérifier la première ligne
            for col in range(table.columnCount()):
                header = table.horizontalHeaderItem(col).text() if table.horizontalHeaderItem(col) else f"Col{col}"
                item = table.item(0, col)
                value = item.text() if item else "None"
                print(f"   📝 {header}: '{value}'")
        
        print("\n✅ Test interface terminé avec succès")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur test interface: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_direct_database():
    """Test direct de la base de données"""
    print("\n🔍 TEST DIRECT BASE DE DONNÉES")
    print("=" * 35)
    
    try:
        db = DatabaseImproved()
        
        # Test get_all_products
        products = db.get_all_products()
        print(f"   📊 get_all_products(): {len(products)} produits")
        
        if products:
            product = products[0]
            print(f"   📝 Premier produit:")
            print(f"      ID: {product.get('id')}")
            print(f"      Nom: {product.get('nombre')}")
            print(f"      Catégorie: '{product.get('categoria')}'")
            print(f"      Type catégorie: {type(product.get('categoria'))}")
        
        # Test get_product_categories
        categories = db.get_product_categories()
        print(f"   📊 get_product_categories(): {len(categories)} catégories")
        
        for cat in categories:
            print(f"   📝 Catégorie: '{cat}' (type: {type(cat)})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur test DB: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET INTERFACE CATÉGORIES")
    print("=" * 50)
    
    # Test 1: Base de données directe
    db_ok = test_direct_database()
    
    # Test 2: Interface (seulement si DB OK)
    interface_ok = False
    if db_ok:
        interface_ok = test_interface_productos()
    else:
        print("\n⚠️ Test interface ignoré (problème DB)")
    
    # Résumé
    print("\n🎯 RÉSUMÉ:")
    print(f"   Test base de données: {'✅ OK' if db_ok else '❌ ÉCHEC'}")
    print(f"   Test interface: {'✅ OK' if interface_ok else '❌ ÉCHEC'}")
    
    if db_ok and interface_ok:
        print("\n🎉 DIAGNOSTIC COMPLET RÉUSSI")
        print("   L'interface devrait afficher les catégories correctement")
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        if not db_ok:
            print("   → Problème au niveau base de données")
        if not interface_ok:
            print("   → Problème au niveau interface")
    
    return db_ok and interface_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
