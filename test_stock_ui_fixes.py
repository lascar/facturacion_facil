#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections UI pour la synchronisation des stocks après migration
"""

import sys
import os
import sqlite3

# Ajouter le répertoire racine au path
sys.path.append('.')

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.database_improved import DatabaseImproved
from database.models import Stock

def test_database_improved_get_all_products():
    """Tester que database_improved.get_all_products() fonctionne après migration"""
    print("=== Test DatabaseImproved.get_all_products() ===")
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    
    # Exécuter la migration
    migration_manager = MigrationManager(db_path)
    migration_manager.remove_stock_columns_from_productos()
    
    # Créer des données de test
    db_improved = DatabaseImproved(db_path)
    products = [
        {
            'nombre': 'Producto Test 1',
            'referencia': 'TEST001',
            'precio': 25.50,
            'categoria': 'Test',
            'stock_actual': 100
        },
        {
            'nombre': 'Producto Test 2',
            'referencia': 'TEST002',
            'precio': 15.75,
            'categoria': 'Test',
            'stock_actual': 50
        }
    ]
    
    for product in products:
        db_improved.add_product(product)
    
    # Tester get_all_products
    all_products = db_improved.get_all_products()
    
    print(f"Nombre de produits récupérés: {len(all_products)}")
    
    for product in all_products:
        print(f"- {product['nombre']}: Stock {product['stock_actual']}")
        
        # Vérifier que stock_actual est présent et correct
        assert 'stock_actual' in product, "stock_actual devrait être présent"
        assert product['stock_actual'] > 0, "stock_actual devrait être > 0"
    
    test_db.cleanup()
    print("✅ DatabaseImproved.get_all_products() fonctionne correctement")
    return True

def test_stock_model_update_direct():
    """Tester Stock.update_stock_direct()"""
    print("\n=== Test Stock.update_stock_direct() ===")

    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path

    # Exécuter la migration
    migration_manager = MigrationManager(db_path)
    migration_manager.remove_stock_columns_from_productos()

    # Créer un produit directement avec DatabaseImproved en spécifiant le chemin
    db_improved = DatabaseImproved(db_path)

    # Ajouter le produit manuellement pour éviter les problèmes d'initialisation
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, referencia, precio, categoria)
            VALUES (?, ?, ?, ?)
        """, ('Test Product', 'TEST001', 25.50, 'Test'))
        product_id = cursor.lastrowid

        # Ajouter le stock
        cursor.execute("""
            INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (product_id, 100))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur création produit: {e}")
        test_db.cleanup()
        return False
    
    # Tester la mise à jour directe
    Stock.update_stock_direct(product_id, 75, db_path)

    # Vérifier que le stock a été mis à jour
    new_stock = Stock.get_by_product(product_id, db_path)
    print(f"Stock après mise à jour: {new_stock}")

    assert new_stock == 75, f"Stock devrait être 75, obtenu: {new_stock}"
    
    test_db.cleanup()
    print("✅ Stock.update_stock_direct() fonctionne correctement")
    return True

def test_stock_synchronization_flow():
    """Tester le flux complet de synchronisation"""
    print("\n=== Test Flux Synchronisation Complet ===")

    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path

    # Exécuter la migration
    migration_manager = MigrationManager(db_path)
    migration_manager.remove_stock_columns_from_productos()

    # Créer un produit manuellement
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, referencia, precio, categoria)
            VALUES (?, ?, ?, ?)
        """, ('Test Product', 'TEST001', 25.50, 'Test'))
        product_id = cursor.lastrowid

        # Ajouter le stock
        cursor.execute("""
            INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (product_id, 100))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur création produit: {e}")
        test_db.cleanup()
        return False
    
    print("1. Produit créé avec stock initial 100")

    # Simuler l'ajustement de stock depuis la fenêtre Stock
    Stock.update_stock_direct(product_id, 80, db_path)
    print("2. Stock ajusté à 80 via Stock.update_stock_direct()")

    # Vérifier que get_all_products() retourne le nouveau stock
    db_improved = DatabaseImproved(db_path)
    products = db_improved.get_all_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    assert product is not None, "Produit devrait être trouvé"
    assert product['stock_actual'] == 80, f"Stock devrait être 80, obtenu: {product['stock_actual']}"
    
    print("3. get_all_products() retourne le stock mis à jour: ✅")
    
    test_db.cleanup()
    print("✅ Flux de synchronisation complet fonctionne")
    return True

def main():
    """Fonction principale"""
    print("🔧 TEST CORRECTIONS UI SYNCHRONISATION STOCKS")
    print("=" * 60)
    
    try:
        # Test 1: DatabaseImproved
        test1_ok = test_database_improved_get_all_products()
        
        # Test 2: Stock model
        test2_ok = test_stock_model_update_direct()
        
        # Test 3: Flux complet
        test3_ok = test_stock_synchronization_flow()
        
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        if test1_ok and test2_ok and test3_ok:
            print("✅ Tous les tests passent !")
            print("🎉 Les corrections UI sont fonctionnelles")
            print("\n🔄 Prochaines étapes:")
            print("   1. Tester l'interface graphique")
            print("   2. Vérifier la synchronisation entre fenêtres")
            print("   3. Tester le bouton Actualizar")
        else:
            print("❌ Certains tests ont échoué")
            
    except Exception as e:
        print(f"❌ Erreur durant les tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
