import pytest
import sqlite3
import tempfile
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import Database

class TestDatabase:
    """Tests pour la classe Database"""
    
    def test_database_initialization(self, temp_db):
        """Test que la base de données s'initialise correctement"""
        assert isinstance(temp_db, Database)
        assert os.path.exists(temp_db.db_path)
    
    def test_database_tables_creation(self, temp_db):
        """Test que toutes les tables sont créées"""
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        # Vérifier que les tables existent
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['productos', 'organizacion', 'stock', 'facturas', 'factura_items']
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
        
        conn.close()
    
    def test_productos_table_structure(self, temp_db):
        """Test la structure de la table productos"""
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(productos)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        expected_columns = {
            'id': 'INTEGER',
            'nombre': 'TEXT',
            'referencia': 'TEXT',
            'precio': 'REAL',
            'categoria': 'TEXT',
            'descripcion': 'TEXT',
            'imagen_path': 'TEXT',
            'iva_recomendado': 'REAL',
            'fecha_creacion': 'TIMESTAMP'
        }
        
        for col_name, col_type in expected_columns.items():
            assert col_name in columns, f"Column {col_name} not found"
            assert columns[col_name] == col_type, f"Column {col_name} has wrong type"
        
        conn.close()
    
    def test_execute_query_select(self, temp_db):
        """Test l'exécution de requêtes SELECT"""
        # Insérer des données de test
        temp_db.execute_query(
            "INSERT INTO productos (nombre, referencia, precio) VALUES (?, ?, ?)",
            ("Test Product", "TEST001", 25.50)
        )
        
        # Tester SELECT
        results = temp_db.execute_query("SELECT * FROM productos WHERE referencia = ?", ("TEST001",))
        
        assert len(results) == 1
        assert results[0][1] == "Test Product"  # nom
        assert results[0][2] == "TEST001"       # référence
        assert results[0][3] == 25.50           # prix
    
    def test_execute_query_insert(self, temp_db):
        """Test l'exécution de requêtes INSERT"""
        lastrowid = temp_db.execute_query(
            "INSERT INTO productos (nombre, referencia, precio) VALUES (?, ?, ?)",
            ("New Product", "NEW001", 15.75)
        )
        
        assert lastrowid is not None
        assert lastrowid > 0
        
        # Vérifier que l'insertion a fonctionné
        results = temp_db.execute_query("SELECT COUNT(*) FROM productos")
        assert results[0][0] == 1
    
    def test_execute_query_update(self, temp_db):
        """Test l'exécution de requêtes UPDATE"""
        # Insérer un produit
        temp_db.execute_query(
            "INSERT INTO productos (nombre, referencia, precio) VALUES (?, ?, ?)",
            ("Original", "ORIG001", 10.00)
        )
        
        # Mettre à jour
        temp_db.execute_query(
            "UPDATE productos SET precio = ? WHERE referencia = ?",
            (20.00, "ORIG001")
        )
        
        # Vérifier la mise à jour
        results = temp_db.execute_query("SELECT precio FROM productos WHERE referencia = ?", ("ORIG001",))
        assert results[0][0] == 20.00
    
    def test_execute_query_delete(self, temp_db):
        """Test l'exécution de requêtes DELETE"""
        # Insérer un produit
        temp_db.execute_query(
            "INSERT INTO productos (nombre, referencia, precio) VALUES (?, ?, ?)",
            ("To Delete", "DEL001", 5.00)
        )
        
        # Vérifier qu'il existe
        results = temp_db.execute_query("SELECT COUNT(*) FROM productos")
        assert results[0][0] == 1
        
        # Supprimer
        temp_db.execute_query("DELETE FROM productos WHERE referencia = ?", ("DEL001",))
        
        # Vérifier la suppression
        results = temp_db.execute_query("SELECT COUNT(*) FROM productos")
        assert results[0][0] == 0
    
    def test_get_next_factura_number(self, temp_db):
        """Test la génération du numéro de facture avec nouveau format"""
        from datetime import datetime

        # Premier numéro (nouveau format: numero-año)
        numero1 = temp_db.get_next_factura_number()
        year = datetime.now().year
        expected1 = f"1-{year}"
        assert numero1 == expected1

        # Simuler une facture existante
        temp_db.execute_query(
            "INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura) VALUES (?, ?, ?, ?, ?, ?)",
            (numero1, f"{year}-01-01", "Test Client", 100.0, 21.0, 121.0)
        )

        # Deuxième numéro
        numero2 = temp_db.get_next_factura_number()
        expected2 = f"2-{year}"
        assert numero2 == expected2
    
    def test_database_connection_error_handling(self):
        """Test la gestion d'erreurs de connexion"""
        # Tenter de créer une base de données dans un répertoire invalide
        with pytest.raises(Exception):
            invalid_db = Database("/invalid/path/test.db")
    
    @pytest.mark.slow
    def test_database_performance(self, temp_db, faker_instance):
        """Test de performance de la base de données"""
        import time
        
        # Insérer beaucoup de produits
        start_time = time.time()
        
        for i in range(100):
            temp_db.execute_query(
                "INSERT INTO productos (nombre, referencia, precio) VALUES (?, ?, ?)",
                (f"Product {i}", f"PERF{i:03d}", faker_instance.pyfloat(positive=True, max_value=100))
            )
        
        insert_time = time.time() - start_time
        
        # Tester la sélection
        start_time = time.time()
        results = temp_db.execute_query("SELECT * FROM productos")
        select_time = time.time() - start_time
        
        # Vérifications
        assert len(results) == 100
        assert insert_time < 5.0  # Moins de 5 secondes pour 100 insertions
        assert select_time < 1.0  # Moins de 1 seconde pour sélectionner 100 lignes
