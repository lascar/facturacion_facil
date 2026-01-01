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
        # Générer un identifiant unique
        import time
        import random
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer un produit (le stock est créé automatiquement)
        producto_id = self.db.add_product({
            'nombre': f'Producto Test {unique_id}',
            'referencia': f'TEST-{unique_id}',
            'precio': 10.0,
            'categoria': 'Test'
        })

        # Vérifier le stock_minimo par défaut
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stock_minimo FROM stock WHERE producto_id = ?", (producto_id,))
        stock_minimo = cursor.fetchone()[0]
        conn.close()

        assert stock_minimo == 0, "Le stock_minimo par défaut doit être 0"
    
    def test_informe_stock_includes_stock_minimo(self):
        """
        GIVEN des produits avec stock_minimo défini
        WHEN je génère un informe de stock
        THEN l'informe doit inclure le stock_minimo pour chaque produit
        """
        # Générer un identifiant unique
        import time
        import random
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer un produit (le stock est créé automatiquement)
        producto_id = self.db.add_product({
            'nombre': f'Producto Test {unique_id}',
            'referencia': f'TEST-{unique_id}',
            'precio': 10.0,
            'categoria': 'Test'
        })

        # Mettre à jour le stock avec stock_minimo
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stock SET cantidad_disponible = ?, stock_minimo = ?
            WHERE producto_id = ?
        """, (5, 10, producto_id))
        conn.commit()
        conn.close()

        # Générer l'informe
        informe = self.informes_service.get_informe_stock()

        # Vérifier que le stock_minimo est inclus
        assert 'productos' in informe
        assert len(informe['productos']) > 0

        # Trouver notre produit créé
        producto = next((p for p in informe['productos'] if p['referencia'] == f'TEST-{unique_id}'), None)
        assert producto is not None, f"Produit TEST-{unique_id} non trouvé dans l'informe"
        assert 'stock_minimo' in producto, "Le stock_minimo doit être inclus dans l'informe"
        assert producto['stock_minimo'] == 10, "Le stock_minimo doit être 10"
    
    def test_informe_stock_multiple_products_with_stock_minimo(self):
        """
        GIVEN plusieurs produits avec différents stock_minimo
        WHEN je génère un informe de stock
        THEN chaque produit doit avoir son stock_minimo correct
        """
        # Générer un identifiant unique
        import time
        import random
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer plusieurs produits
        productos_data = [
            {'nombre': f'Producto 1 {unique_id}', 'referencia': f'P1-{unique_id}', 'precio': 10.0, 'stock': 5, 'minimo': 10},
            {'nombre': f'Producto 2 {unique_id}', 'referencia': f'P2-{unique_id}', 'precio': 20.0, 'stock': 15, 'minimo': 5},
            {'nombre': f'Producto 3 {unique_id}', 'referencia': f'P3-{unique_id}', 'precio': 30.0, 'stock': 0, 'minimo': 20},
        ]

        for data in productos_data:
            producto_id = self.db.add_product({
                'nombre': data['nombre'],
                'referencia': data['referencia'],
                'precio': data['precio'],
                'categoria': 'Test'
            })

            # Mettre à jour le stock avec une connexion séparée
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE stock SET cantidad_disponible = ?, stock_minimo = ?
                WHERE producto_id = ?
            """, (data['stock'], data['minimo'], producto_id))
            conn.commit()
            conn.close()

        # Générer l'informe
        informe = self.informes_service.get_informe_stock()

        # Vérifier que tous les produits ont leur stock_minimo correct
        # Filtrer seulement nos produits créés dans ce test
        productos_test = [p for p in informe['productos'] if p.get('referencia') and str(unique_id) in p['referencia']]
        assert len(productos_test) == 3, f"Il doit y avoir 3 produits de test, trouvé {len(productos_test)}"

        # Trier par référence pour avoir un ordre prévisible
        productos_test.sort(key=lambda p: p['referencia'])
        productos_data_sorted = sorted(productos_data, key=lambda d: d['referencia'])

        for i, producto in enumerate(productos_test):
            expected_minimo = productos_data_sorted[i]['minimo']
            assert producto['stock_minimo'] == expected_minimo, \
                f"Le stock_minimo de {producto['nombre']} doit être {expected_minimo}"
            assert producto['stock_actual'] == productos_data_sorted[i]['stock'], \
                f"Le stock_actual de {producto['nombre']} doit être {productos_data_sorted[i]['stock']}"
