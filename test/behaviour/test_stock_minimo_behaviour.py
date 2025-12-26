# -*- coding: utf-8 -*-
"""
Tests de comportement pour le stock minimal
"""

import pytest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database
from services.informes_service import InformesService


class TestStockMinimoBehaviour:
    """Tests BDD pour le stock minimal"""
    
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Configuration pour chaque test"""
        # Créer une base de données temporaire
        self.db_path = str(tmp_path / "test_stock_minimo.db")
        self.db = Database(self.db_path)
        # La base de données est initialisée automatiquement dans __init__
        self.informes_service = InformesService(self.db_path)

        yield

        # Nettoyage
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_stock_minimo_column_exists(self):
        """
        GIVEN une base de données initialisée
        WHEN je vérifie la structure de la table stock
        THEN la colonne stock_minimo doit exister
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Vérifier que la colonne stock_minimo existe
        cursor.execute("PRAGMA table_info(stock)")
        columns = [row[1] for row in cursor.fetchall()]
        
        assert 'stock_minimo' in columns, "La colonne stock_minimo doit exister dans la table stock"
    
    def test_stock_minimo_default_value(self):
        """
        GIVEN un nouveau produit
        WHEN je crée un stock pour ce produit sans spécifier stock_minimo
        THEN le stock_minimo doit être 0 par défaut
        """
        # Créer un produit
        producto_id = self.db.add_product({
            'nombre': 'Producto Test',
            'referencia': 'TEST-001',
            'precio': 10.0,
            'categoria': 'Test'
        })
        
        # Créer un stock
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stock (producto_id, cantidad_disponible)
            VALUES (?, ?)
        """, (producto_id, 5))
        conn.commit()
        
        # Vérifier le stock_minimo
        cursor.execute("SELECT stock_minimo FROM stock WHERE producto_id = ?", (producto_id,))
        stock_minimo = cursor.fetchone()[0]
        
        assert stock_minimo == 0, "Le stock_minimo par défaut doit être 0"
    
    def test_informe_stock_includes_stock_minimo(self):
        """
        GIVEN des produits avec stock_minimo défini
        WHEN je génère un informe de stock
        THEN l'informe doit inclure le stock_minimo pour chaque produit
        """
        # Créer un produit
        producto_id = self.db.add_product({
            'nombre': 'Producto Test',
            'referencia': 'TEST-001',
            'precio': 10.0,
            'categoria': 'Test'
        })
        
        # Créer un stock avec stock_minimo
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stock (producto_id, cantidad_disponible, stock_minimo)
            VALUES (?, ?, ?)
        """, (producto_id, 5, 10))
        conn.commit()
        
        # Générer l'informe
        informe = self.informes_service.get_informe_stock()
        
        # Vérifier que le stock_minimo est inclus
        assert 'productos' in informe
        assert len(informe['productos']) > 0
        
        producto = informe['productos'][0]
        assert 'stock_minimo' in producto, "Le stock_minimo doit être inclus dans l'informe"
        assert producto['stock_minimo'] == 10, "Le stock_minimo doit être 10"
    
    def test_informe_stock_multiple_products_with_stock_minimo(self):
        """
        GIVEN plusieurs produits avec différents stock_minimo
        WHEN je génère un informe de stock
        THEN chaque produit doit avoir son stock_minimo correct
        """
        # Créer plusieurs produits
        productos_data = [
            {'nombre': 'Producto 1', 'referencia': 'P1', 'precio': 10.0, 'stock': 5, 'minimo': 10},
            {'nombre': 'Producto 2', 'referencia': 'P2', 'precio': 20.0, 'stock': 15, 'minimo': 5},
            {'nombre': 'Producto 3', 'referencia': 'P3', 'precio': 30.0, 'stock': 0, 'minimo': 20},
        ]
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        for data in productos_data:
            producto_id = self.db.add_product({
                'nombre': data['nombre'],
                'referencia': data['referencia'],
                'precio': data['precio'],
                'categoria': 'Test'
            })
            
            cursor.execute("""
                INSERT INTO stock (producto_id, cantidad_disponible, stock_minimo)
                VALUES (?, ?, ?)
            """, (producto_id, data['stock'], data['minimo']))
        
        conn.commit()
        
        # Générer l'informe
        informe = self.informes_service.get_informe_stock()

        # Vérifier que tous les produits ont leur stock_minimo correct
        assert len(informe['productos']) == 3

        for i, producto in enumerate(informe['productos']):
            expected_minimo = productos_data[i]['minimo']
            assert producto['stock_minimo'] == expected_minimo, \
                f"Le stock_minimo de {producto['nombre']} doit être {expected_minimo}"
            assert producto['stock_actual'] == productos_data[i]['stock'], \
                f"Le stock_actual de {producto['nombre']} doit être {productos_data[i]['stock']}"
