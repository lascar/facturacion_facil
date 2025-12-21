#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système de stock après migration
"""

import sys
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.models import Producto, Stock
from database.database_improved import DatabaseImproved

def test_complete_stock_system():
    """Test complet du système de stock après migration"""
    
    print("=== Test Complet Système Stock Après Migration ===\n")
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    print(f"Base de test: {db_path}")
    
    try:
        # Étape 1: Exécuter la migration
        print("\n1. Exécution de la migration...")
        migration_manager = MigrationManager(db_path)
        success = migration_manager.remove_stock_columns_from_productos()
        assert success, "La migration devrait réussir"
        print("✅ Migration exécutée")
        
        # Étape 2: Tester la création de produits avec le nouveau système
        print("\n2. Test création de produits...")
        db_improved = DatabaseImproved(db_path)
        
        # Créer un produit via DatabaseImproved
        product_data = {
            'nombre': 'Producto Test Nuevo',
            'referencia': 'NUEVO001',
            'precio': 25.50,
            'categoria': 'Test',
            'descripcion': 'Producto de test',
            'stock_actual': 100
        }
        
        success = db_improved.add_product(product_data)
        assert success, "La création de produit devrait réussir"
        print("✅ Produit créé avec succès")
        
        # Étape 3: Vérifier que le stock est bien dans la table stock
        print("\n3. Vérification du stock...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier que le produit n'a pas de colonnes stock
        cursor.execute("PRAGMA table_info(productos)")
        productos_columns = [col[1] for col in cursor.fetchall()]
        assert 'stock_actual' not in productos_columns, "stock_actual ne devrait plus exister"
        assert 'stock_minimo' not in productos_columns, "stock_minimo ne devrait plus exister"
        
        # Vérifier que le stock est dans la table stock
        cursor.execute("SELECT producto_id, cantidad_disponible FROM stock WHERE producto_id = 1")
        stock_row = cursor.fetchone()
        assert stock_row is not None, "Le stock devrait exister"
        assert stock_row[1] == 100, "Le stock devrait être 100"
        
        conn.close()
        print("✅ Stock correctement stocké dans la table stock")
        
        # Étape 4: Tester les modèles Python
        print("\n4. Test des modèles Python...")
        
        # Tester Producto.get_stock_actual()
        producto = Producto(id=1, nombre="Test")
        stock_actual = producto.get_stock_actual(db_path)
        assert stock_actual == 100, f"Stock actual devrait être 100, obtenu: {stock_actual}"
        print("✅ Producto.get_stock_actual() fonctionne")

        # Tester Stock.get_by_product()
        stock_from_model = Stock.get_by_product(1, db_path)
        assert stock_from_model == 100, f"Stock depuis modèle devrait être 100, obtenu: {stock_from_model}"
        print("✅ Stock.get_by_product() fonctionne")
        
        # Étape 5: Tester la mise à jour de stock
        print("\n5. Test mise à jour de stock...")
        
        # Mettre à jour via Stock.update_stock()
        Stock.update_stock(1, 20, db_path)  # Vendre 20 unités

        new_stock = Stock.get_by_product(1, db_path)
        assert new_stock == 80, f"Nouveau stock devrait être 80, obtenu: {new_stock}"
        print("✅ Mise à jour de stock fonctionne")
        
        # Étape 6: Tester get_all_products avec stock
        print("\n6. Test récupération produits avec stock...")
        
        products = db_improved.get_all_products()
        assert len(products) > 0, "Devrait avoir au moins un produit"
        
        product = products[0]
        assert 'stock_actual' in product, "Le produit devrait avoir stock_actual"
        assert product['stock_actual'] == 80, f"Stock devrait être 80, obtenu: {product['stock_actual']}"
        assert product['stock_minimo'] == 5, "Stock minimo devrait être 5 par défaut"
        print("✅ Récupération produits avec stock fonctionne")
        
        # Étape 7: Tester Stock.get_all()
        print("\n7. Test Stock.get_all()...")

        all_stock = Stock.get_all(db_path)
        assert len(all_stock) > 0, "Devrait avoir au moins une entrée stock"

        stock_entry = all_stock[0]
        assert stock_entry[0] == 1, "Producto ID devrait être 1"
        assert stock_entry[1] == 80, "Cantidad disponible devrait être 80"
        print("✅ Stock.get_all() fonctionne")
        
        print("\n🎉 Tous les tests sont passés ! Le système de stock fonctionne parfaitement après migration.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Nettoyer
        test_db.cleanup()

if __name__ == "__main__":
    success = test_complete_stock_system()
    sys.exit(0 if success else 1)
