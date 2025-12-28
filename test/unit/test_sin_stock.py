#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour le système "sin stock"
Vérifie que les produits "sin stock" n'ont pas d'entrée dans la table stock
"""

import pytest
from database.database import Database


class TestSinStock:
    """Tests pour la fonctionnalité 'sin stock' des produits"""

    def test_create_product_with_stock(self, temp_db):
        """Test: Créer un produit avec gestion de stock"""
        db = Database(temp_db)
        
        product_id = db.add_product({
            'nombre': 'Camiseta Roja',
            'referencia': 'CAM001',
            'precio_venta': 15.99,
            'stock': 100,
            'sin_stock': False
        })
        
        # Vérifier que le produit a été créé
        assert product_id is not None
        
        # Vérifier qu'il y a une entrée dans la table stock
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is not None, "Produit avec stock devrait avoir une entrée dans table stock"
        assert stock_entry[0] == 100, "Stock devrait être 100"

    def test_create_product_without_stock(self, temp_db):
        """Test: Créer un produit sans gestion de stock"""
        db = Database(temp_db)
        
        product_id = db.add_product({
            'nombre': 'Servicio de Consultoría',
            'referencia': 'SRV001',
            'precio_venta': 50.00,
            'stock': 0,
            'sin_stock': True
        })
        
        # Vérifier que le produit a été créé
        assert product_id is not None
        
        # Vérifier qu'il N'Y A PAS d'entrée dans la table stock
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is None, "Produit 'sin stock' ne devrait PAS avoir d'entrée dans table stock"

    def test_change_from_stock_to_sin_stock(self, temp_db):
        """Test: Changer un produit de 'con stock' à 'sin stock'"""
        db = Database(temp_db)
        
        # Créer un produit avec stock
        product_id = db.add_product({
            'nombre': 'Producto Test',
            'referencia': 'TEST001',
            'precio_venta': 10.00,
            'stock': 50,
            'sin_stock': False
        })
        
        # Vérifier qu'il a une entrée dans stock
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        assert stock_entry is not None, "Devrait avoir une entrée dans stock"
        
        # Changer à 'sin stock'
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
        
        # Vérifier que l'entrée a été supprimée
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        
        assert stock_entry is None, "L'entrée dans stock devrait avoir été supprimée"

    def test_change_from_sin_stock_to_stock(self, temp_db):
        """Test: Changer un produit de 'sin stock' à 'con stock'"""
        db = Database(temp_db)
        
        # Créer un produit sin stock
        product_id = db.add_product({
            'nombre': 'Servicio Test',
            'referencia': 'SRV002',
            'precio_venta': 30.00,
            'stock': 0,
            'sin_stock': True
        })
        
        # Vérifier qu'il n'a PAS d'entrée dans stock
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        assert stock_entry is None, "Ne devrait PAS avoir d'entrée dans stock"
        
        # Changer à 'con stock'
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
        
        # Vérifier que l'entrée a été créée
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()

        assert stock_entry is not None, "L'entrée dans stock devrait avoir été créée"
        assert stock_entry[0] == 25, "Stock devrait être 25"

    def test_stock_table_only_contains_managed_products(self, temp_db):
        """Test: La table stock ne contient que les produits qui gèrent le stock"""
        db = Database(temp_db)

        # Créer plusieurs produits
        product1_id = db.add_product({
            'nombre': 'Producto Con Stock 1',
            'referencia': 'STOCK001',
            'precio_venta': 10.00,
            'stock': 100,
            'sin_stock': False
        })

        product2_id = db.add_product({
            'nombre': 'Producto Sin Stock 1',
            'referencia': 'NOSTOCK001',
            'precio_venta': 20.00,
            'stock': 0,
            'sin_stock': True
        })

        product3_id = db.add_product({
            'nombre': 'Producto Con Stock 2',
            'referencia': 'STOCK002',
            'precio_venta': 30.00,
            'stock': 50,
            'sin_stock': False
        })

        product4_id = db.add_product({
            'nombre': 'Producto Sin Stock 2',
            'referencia': 'NOSTOCK002',
            'precio_venta': 40.00,
            'stock': 0,
            'sin_stock': True
        })

        # Vérifier le contenu de la table stock
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT producto_id FROM stock ORDER BY producto_id")
        stock_entries = cursor.fetchall()
        conn.close()

        # Devrait avoir exactement 2 entrées (les produits avec stock)
        assert len(stock_entries) == 2, f"Devrait avoir 2 entrées dans stock, trouvé {len(stock_entries)}"

        stock_product_ids = [entry[0] for entry in stock_entries]
        assert product1_id in stock_product_ids, "Producto Con Stock 1 devrait être dans stock"
        assert product3_id in stock_product_ids, "Producto Con Stock 2 devrait être dans stock"
        assert product2_id not in stock_product_ids, "Producto Sin Stock 1 ne devrait PAS être dans stock"
        assert product4_id not in stock_product_ids, "Producto Sin Stock 2 ne devrait PAS être dans stock"

    def test_get_product_by_id_returns_sin_stock_flag(self, temp_db):
        """Test: get_product_by_id retourne le flag sin_stock"""
        db = Database(temp_db)

        # Créer un produit sin stock
        product_id = db.add_product({
            'nombre': 'Test Product',
            'referencia': 'TEST123',
            'precio_venta': 15.00,
            'stock': 0,
            'sin_stock': True
        })

        # Récupérer le produit
        product = db.get_product_by_id(product_id)

        assert product is not None
        assert 'sin_stock' in product
        assert product['sin_stock'] == 1, "sin_stock devrait être 1 (True)"

    def test_get_all_products_returns_sin_stock_flag(self, temp_db):
        """Test: get_all_products retourne le flag sin_stock pour tous les produits"""
        db = Database(temp_db)

        # Créer des produits
        db.add_product({
            'nombre': 'Con Stock',
            'referencia': 'CS001',
            'precio_venta': 10.00,
            'stock': 100,
            'sin_stock': False
        })

        db.add_product({
            'nombre': 'Sin Stock',
            'referencia': 'SS001',
            'precio_venta': 20.00,
            'stock': 0,
            'sin_stock': True
        })

        # Récupérer tous les produits
        products = db.get_all_products()

        assert len(products) >= 2

        for product in products:
            assert 'sin_stock' in product, "Chaque produit devrait avoir le champ sin_stock"
            assert product['sin_stock'] in [0, 1], "sin_stock devrait être 0 ou 1"

