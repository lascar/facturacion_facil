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
    @pytest.fixture(autouse=True)
    def setup(self, patched_models_db):
        """Setup avec patched_models_db"""
        self.db = patched_models_db
        yield


    def test_create_product_with_stock(self):
        """Test: Créer un produit avec gestion de stock"""
        product_id = self.db.add_product({
            'nombre': 'Camiseta Roja',
            'referencia': 'CAM001',
            'precio_venta': 15.99,
            'stock': 100,
            'sin_stock': False
        })

        # Vérifier que le produit a été créé
        assert product_id is not None

        # Vérifier qu'il y a une entrée dans la table stock
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()

        assert stock_entry is not None, "Produit avec stock devrait avoir une entrée dans table stock"
        assert stock_entry[0] == 100, "Stock devrait être 100"

    def test_create_product_without_stock(self):
        """Test: Créer un produit sans gestion de stock"""
        product_id = self.db.add_product({
            'nombre': 'Servicio de Consultoría',
            'referencia': 'SRV001',
            'precio_venta': 50.00,
            'stock': 0,
            'sin_stock': True
        })

        # Vérifier que le produit a été créé
        assert product_id is not None

        # Vérifier qu'il N'Y A PAS d'entrée dans la table stock
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()

        assert stock_entry is None, "Produit 'sin stock' ne devrait PAS avoir d'entrée dans table stock"



    def test_change_from_sin_stock_to_stock(self):
        """Test: Changer un produit de 'sin stock' à 'con stock'"""
        # Créer un produit sin stock
        product_id = self.db.add_product({
            'nombre': 'Servicio Test',
            'referencia': 'SRV002',
            'precio_venta': 30.00,
            'stock': 0,
            'sin_stock': True
        })

        # Vérifier qu'il n'a PAS d'entrée dans stock
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()
        assert stock_entry is None, "Ne devrait PAS avoir d'entrée dans stock"

        # Changer à 'con stock'
        self.db.update_product({
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
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
        stock_entry = cursor.fetchone()
        conn.close()

        assert stock_entry is not None, "L'entrée dans stock devrait avoir été créée"
        assert stock_entry[0] == 25, "Stock devrait être 25"



    def test_get_product_by_id_returns_sin_stock_flag(self):
        """Test: get_product_by_id retourne le flag sin_stock"""
        # Créer un produit sin stock
        product_id = self.db.add_product({
            'nombre': 'Test Product',
            'referencia': 'TEST123',
            'precio_venta': 15.00,
            'stock': 0,
            'sin_stock': True
        })

        # Récupérer le produit
        product = self.db.get_product_by_id(product_id)

        assert product is not None
        assert 'sin_stock' in product
        assert product['sin_stock'] == 1, "sin_stock devrait être 1 (True)"

    def test_get_all_products_returns_sin_stock_flag(self):
        """Test: get_all_products retourne le flag sin_stock pour tous les produits"""
        # Créer des produits
        self.db.add_product({
            'nombre': 'Con Stock',
            'referencia': 'CS001',
            'precio_venta': 10.00,
            'stock': 100,
            'sin_stock': False
        })

        self.db.add_product({
            'nombre': 'Sin Stock',
            'referencia': 'SS001',
            'precio_venta': 20.00,
            'stock': 0,
            'sin_stock': True
        })

        # Récupérer tous les produits
        products = self.db.get_all_products()

        assert len(products) >= 2

        for product in products:
            assert 'sin_stock' in product, "Chaque produit devrait avoir le champ sin_stock"
            assert product['sin_stock'] in [0, 1], "sin_stock devrait être 0 ou 1"

