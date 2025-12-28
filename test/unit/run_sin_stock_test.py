#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter les tests sin_stock sans pytest
"""

import sys
import os
import tempfile

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.database import Database


def run_test(test_name, test_func):
    """Exécute un test et affiche le résultat"""
    try:
        test_func()
        print(f"✅ {test_name}")
        return True
    except AssertionError as e:
        print(f"❌ {test_name}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ {test_name}")
        print(f"   Exception: {e}")
        return False


def test_create_product_with_stock():
    """Test: Créer un produit avec gestion de stock"""
    test_db_fd, temp_db = tempfile.mkstemp(suffix='.db')
    os.close(test_db_fd)
    
    try:
        db = Database(temp_db)
        
        product_id = db.add_product({
            'nombre': 'Camiseta Roja',
            'referencia': 'CAM001',
            'precio_venta': 15.99,
            'stock': 100,
            'sin_stock': False
        })
        
        assert product_id is not None
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is not None, "Produit avec stock devrait avoir une entrée dans table stock"
        assert stock_entry[0] == 100, "Stock devrait être 100"
    finally:
        if os.path.exists(temp_db):
            os.unlink(temp_db)


def test_create_product_without_stock():
    """Test: Créer un produit sans gestion de stock"""
    test_db_fd, temp_db = tempfile.mkstemp(suffix='.db')
    os.close(test_db_fd)
    
    try:
        db = Database(temp_db)
        
        product_id = db.add_product({
            'nombre': 'Servicio de Consultoría',
            'referencia': 'SRV001',
            'precio_venta': 50.00,
            'stock': 0,
            'sin_stock': True
        })
        
        assert product_id is not None
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is None, "Produit 'sin stock' ne devrait PAS avoir d'entrée dans table stock"
    finally:
        if os.path.exists(temp_db):
            os.unlink(temp_db)


def test_change_from_stock_to_sin_stock():
    """Test: Changer un produit de 'con stock' à 'sin stock'"""
    test_db_fd, temp_db = tempfile.mkstemp(suffix='.db')
    os.close(test_db_fd)
    
    try:
        db = Database(temp_db)
        
        product_id = db.add_product({
            'nombre': 'Producto Test',
            'referencia': 'TEST001',
            'precio_venta': 10.00,
            'stock': 50,
            'sin_stock': False
        })
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        assert stock_entry is not None, "Devrait avoir une entrée dans stock"
        
        db.update_product({
            'id': product_id,
            'nombre': 'Producto Test',
            'referencia': 'TEST001',
            'precio_venta': 10.00,
            'categoria': '',
            'descripcion': '',
            'stock': 0,
            'sin_stock': True
        })
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is None, "L'entrée dans stock devrait avoir été supprimée"
    finally:
        if os.path.exists(temp_db):
            os.unlink(temp_db)


def test_change_from_sin_stock_to_stock():
    """Test: Changer un produit de 'sin stock' à 'con stock'"""
    test_db_fd, temp_db = tempfile.mkstemp(suffix='.db')
    os.close(test_db_fd)

    try:
        db = Database(temp_db)

        product_id = db.add_product({
            'nombre': 'Servicio Test',
            'referencia': 'SRV002',
            'precio_venta': 30.00,
            'stock': 0,
            'sin_stock': True
        })

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        assert stock_entry is None, "Ne devrait PAS avoir d'entrée dans stock"

        db.update_product({
            'id': product_id,
            'nombre': 'Servicio Test',
            'referencia': 'SRV002',
            'precio_venta': 30.00,
            'categoria': '',
            'descripcion': '',
            'stock': 25,
            'sin_stock': False
        })

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()

        assert stock_entry is not None, "L'entrée dans stock devrait avoir été créée"
        assert stock_entry[0] == 25, "Stock devrait être 25"
    finally:
        if os.path.exists(temp_db):
            os.unlink(temp_db)


def main():
    """Exécute tous les tests"""
    print("=" * 70)
    print("🧪 TESTS UNITAIRES - Système 'Sin Stock'")
    print("=" * 70)
    print()

    tests = [
        ("test_create_product_with_stock", test_create_product_with_stock),
        ("test_create_product_without_stock", test_create_product_without_stock),
        ("test_change_from_stock_to_sin_stock", test_change_from_stock_to_sin_stock),
        ("test_change_from_sin_stock_to_stock", test_change_from_sin_stock_to_stock),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 70)
    print(f"Résultats: {passed} passés, {failed} échoués sur {len(tests)} tests")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

