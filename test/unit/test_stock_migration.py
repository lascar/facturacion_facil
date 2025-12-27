#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la migration de suppression des colonnes stock de la table productos
"""

import sys
import os
import sqlite3
import tempfile
import shutil
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.models import Producto, Stock

@pytest.mark.skip(reason="Migration already completed - productos table no longer has stock_actual/stock_minimo columns")
def test_stock_migration():
    """Test de la migration de suppression des colonnes stock"""
    
    print("=== Test Migration Suppression Colonnes Stock ===\n")
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    print(f"Base de test: {db_path}")
    
    try:
        # Étape 1: Créer des données de test avec stock
        print("\n1. Création de données de test...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insérer des produits avec stock_actual et stock_minimo
        test_products = [
            ("Producto Test 1", "TEST001", 10.50, "Test", "Description 1", "", 21.0, 100, 10),
            ("Producto Test 2", "TEST002", 25.00, "Test", "Description 2", "", 21.0, 50, 5),
            ("Producto Test 3", "TEST003", 15.75, "Test", "Description 3", "", 21.0, 0, 15)
        ]
        
        for product in test_products:
            cursor.execute("""
                INSERT INTO productos (nombre, referencia, precio, categoria, descripcion, 
                                     imagen_path, iva_recomendado, stock_actual, stock_minimo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, product)
        
        conn.commit()
        
        # Créer quelques entrées dans la table stock (certaines différentes de stock_actual)
        cursor.execute("INSERT INTO stock (producto_id, cantidad_disponible) VALUES (1, 95)")  # Différent de stock_actual
        cursor.execute("INSERT INTO stock (producto_id, cantidad_disponible) VALUES (2, 50)")  # Identique
        # Pas d'entrée pour le produit 3 pour tester la migration
        
        conn.commit()
        conn.close()
        
        print("✅ Données de test créées")
        
        # Étape 2: Vérifier l'état avant migration
        print("\n2. Vérification état avant migration...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier structure productos
        cursor.execute("PRAGMA table_info(productos)")
        productos_columns = [col[1] for col in cursor.fetchall()]
        print(f"Colonnes productos avant: {productos_columns}")
        
        assert 'stock_actual' in productos_columns, "stock_actual devrait être présent avant migration"
        assert 'stock_minimo' in productos_columns, "stock_minimo devrait être présent avant migration"
        
        # Vérifier données
        cursor.execute("SELECT id, nombre, stock_actual, stock_minimo FROM productos ORDER BY id")
        productos_before = cursor.fetchall()
        print(f"Productos avant migration: {productos_before}")
        
        cursor.execute("SELECT producto_id, cantidad_disponible FROM stock ORDER BY producto_id")
        stock_before = cursor.fetchall()
        print(f"Stock avant migration: {stock_before}")
        
        conn.close()
        
        # Étape 3: Exécuter la migration
        print("\n3. Exécution de la migration...")
        migration_manager = MigrationManager(db_path)
        success = migration_manager.remove_stock_columns_from_productos()
        
        assert success, "La migration devrait réussir"
        print("✅ Migration exécutée avec succès")
        
        # Étape 4: Vérifier l'état après migration
        print("\n4. Vérification état après migration...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier structure productos
        cursor.execute("PRAGMA table_info(productos)")
        productos_columns_after = [col[1] for col in cursor.fetchall()]
        print(f"Colonnes productos après: {productos_columns_after}")
        
        assert 'stock_actual' not in productos_columns_after, "stock_actual devrait être supprimé"
        assert 'stock_minimo' not in productos_columns_after, "stock_minimo devrait être supprimé"
        assert 'id' in productos_columns_after, "id devrait être conservé"
        assert 'nombre' in productos_columns_after, "nombre devrait être conservé"
        assert 'precio' in productos_columns_after, "precio devrait être conservé"
        
        # Vérifier que les données productos sont conservées
        cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
        productos_after = cursor.fetchall()
        print(f"Productos après migration: {productos_after}")
        
        assert len(productos_after) == 3, "Tous les produits devraient être conservés"
        assert productos_after[0][1] == "Producto Test 1", "Les données devraient être conservées"
        
        # Vérifier que les données stock sont correctement migrées
        cursor.execute("SELECT producto_id, cantidad_disponible FROM stock ORDER BY producto_id")
        stock_after = cursor.fetchall()
        print(f"Stock après migration: {stock_after}")
        
        # Devrait avoir 3 entrées maintenant (y compris le produit 3 qui n'en avait pas)
        assert len(stock_after) == 3, "Toutes les entrées stock devraient exister"
        
        # Vérifier les valeurs migrées
        stock_dict = {row[0]: row[1] for row in stock_after}
        assert stock_dict[1] == 100, "Stock du produit 1 devrait être migré depuis stock_actual"
        assert stock_dict[2] == 50, "Stock du produit 2 devrait être conservé"
        assert stock_dict[3] == 0, "Stock du produit 3 devrait être créé avec stock_actual"
        
        conn.close()
        
        print("✅ Toutes les vérifications sont passées")
        
        # Étape 5: Test de migration déjà effectuée
        print("\n5. Test migration déjà effectuée...")
        success_again = migration_manager.remove_stock_columns_from_productos()
        assert success_again, "La migration devrait réussir même si déjà effectuée"
        print("✅ Migration idempotente validée")
        
        print("\n🎉 Test de migration terminé avec succès !")
        assert True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Test failed"
        
    finally:
        # Nettoyer
        test_db.cleanup()

if __name__ == "__main__":
    success = test_stock_migration()
    sys.exit(0 if success else 1)
