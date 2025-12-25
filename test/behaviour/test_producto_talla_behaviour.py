# -*- coding: utf-8 -*-
"""
Tests de comportement pour la fonctionnalité Talla (Taille) des produits
Suit le workflow BDD (Behaviour-Driven Development)
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database_improved import DatabaseImproved
from database.test_database import TestDatabase
from utils.logger import get_logger


class TestProductoTallaBehaviour:
    """Tests de comportement pour la colonne Talla des produits"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger(self.__class__.__name__)

        # Créer une base de test isolée
        self.test_db = TestDatabase(with_fixtures=True)
        self.db_path = self.test_db.db_path

        self.logger.info(f"📁 Base de test: {self.db_path}")

    def teardown_method(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'test_db'):
            self.test_db.cleanup()
    
    # ==================== TESTS BASE DE DONNÉES ====================
    
    def test_01_database_has_talla_column(self):
        """
        COMPORTEMENT: La table productos doit avoir une colonne 'talla' TEXT optionnelle
        GIVEN: Une base de données initialisée
        WHEN: On vérifie la structure de la table productos
        THEN: La colonne 'talla' doit exister et être de type TEXT
        """
        self.logger.info("🧪 Test 01: Vérification colonne 'talla' dans la base de données")
        
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifier que la colonne talla existe
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        conn.close()

        assert 'talla' in column_names, "La colonne 'talla' doit exister dans la table productos"
        self.logger.info("✅ Colonne 'talla' trouvée dans la table productos")
    
    def test_02_add_product_with_talla(self):
        """
        COMPORTEMENT: On doit pouvoir créer un produit avec une talla
        GIVEN: Une base de données avec la colonne talla
        WHEN: On crée un produit avec talla='M'
        THEN: Le produit est créé avec la talla correcte
        """
        self.logger.info("🧪 Test 02: Création d'un produit avec talla")

        product_data = {
            'nombre': 'Camiseta Test',
            'referencia': 'CAM-TEST-001',
            'precio': 19.99,
            'categoria': 'Ropa',
            'descripcion': 'Camiseta de test',
            'talla': 'M',
            'stock': 10
        }

        # Créer le produit
        product_id = self.test_db.add_product(product_data)
        assert product_id is not None, "Le produit doit être créé"

        # Vérifier que la talla est sauvegardée
        products = self.test_db.get_all_products()
        created_product = next((p for p in products if p['id'] == product_id), None)

        assert created_product is not None, "Le produit créé doit être trouvé"
        assert created_product.get('talla') == 'M', "La talla doit être 'M'"

        self.logger.info(f"✅ Produit créé avec talla='M' (ID: {product_id})")
    
    def test_03_add_product_without_talla(self):
        """
        COMPORTEMENT: On doit pouvoir créer un produit sans talla (optionnel)
        GIVEN: Une base de données avec la colonne talla
        WHEN: On crée un produit sans spécifier de talla
        THEN: Le produit est créé avec talla=None ou ''
        """
        self.logger.info("🧪 Test 03: Création d'un produit sans talla (optionnel)")

        product_data = {
            'nombre': 'Ordinateur Test',
            'referencia': 'ORD-TEST-001',
            'precio': 899.99,
            'categoria': 'Informatique',
            'descripcion': 'Ordinateur sans talla',
            'stock': 5
        }

        # Créer le produit sans talla
        product_id = self.test_db.add_product(product_data)
        assert product_id is not None, "Le produit doit être créé"

        # Vérifier que le produit existe sans talla
        products = self.test_db.get_all_products()
        created_product = next((p for p in products if p['id'] == product_id), None)

        assert created_product is not None, "Le produit créé doit être trouvé"
        talla_value = created_product.get('talla')
        assert talla_value in [None, ''], f"La talla doit être None ou vide, reçu: {talla_value}"

        self.logger.info(f"✅ Produit créé sans talla (ID: {product_id})")
    
    def test_04_update_product_talla(self):
        """
        COMPORTEMENT: On doit pouvoir modifier la talla d'un produit existant
        GIVEN: Un produit existant avec talla='S'
        WHEN: On modifie la talla en 'L'
        THEN: La talla est mise à jour correctement
        """
        self.logger.info("🧪 Test 04: Modification de la talla d'un produit")

        # Créer un produit avec talla='S'
        product_data = {
            'nombre': 'Pantalon Test',
            'referencia': 'PAN-TEST-001',
            'precio': 39.99,
            'talla': 'S',
            'stock': 15
        }
        product_id = self.test_db.add_product(product_data)

        # Modifier la talla
        update_data = {
            'id': product_id,
            'nombre': 'Pantalon Test',
            'referencia': 'PAN-TEST-001',
            'precio_venta': 39.99,
            'talla': 'L',
            'stock': 15
        }
        self.test_db.update_product(update_data)

        # Vérifier la modification
        products = self.test_db.get_all_products()
        updated_product = next((p for p in products if p['id'] == product_id), None)

        assert updated_product.get('talla') == 'L', "La talla doit être mise à jour à 'L'"
        self.logger.info(f"✅ Talla modifiée de 'S' à 'L' (ID: {product_id})")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])

