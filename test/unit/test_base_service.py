# -*- coding: utf-8 -*-
"""
Tests pour BaseService
"""

import unittest
import tempfile
import os
from services.base_service import BaseService
from utils.exceptions import (
    DatabaseConnectionError, DatabaseError,
    ValidationError, ClientValidationError
)


class TestBaseService(unittest.TestCase):
    """Tests pour la classe BaseService"""
    
    def setUp(self):
        """Préparer les tests"""
        # Créer une base de données temporaire
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.service = BaseService(self.temp_db.name)
    
    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_init(self):
        """Test de l'initialisation"""
        self.assertIsNotNone(self.service.db)
        self.assertIsNotNone(self.service.logger)
    
    def test_get_connection(self):
        """Test de get_connection"""
        conn = self.service.get_connection()
        self.assertIsNotNone(conn)
        conn.close()
    
    def test_get_connection_invalid_path(self):
        """Test de get_connection avec chemin invalide"""
        # L'erreur se produit déjà lors de l'initialisation de Database
        # car les migrations tentent de se connecter
        with self.assertRaises((DatabaseConnectionError, Exception)):
            service = BaseService("/invalid/path/to/db.db")
    
    def test_safe_execute_success(self):
        """Test de safe_execute avec succès"""
        def test_func(a, b):
            return a + b
        
        result = self.service.safe_execute(test_func, 2, 3)
        self.assertEqual(result, 5)
    
    def test_safe_execute_error(self):
        """Test de safe_execute avec erreur"""
        def test_func():
            raise ValueError("Test error")
        
        result = self.service.safe_execute(test_func)
        self.assertIsNone(result)  # Retourne None en cas d'erreur
    
    def test_validate_required_fields_success(self):
        """Test de validate_required_fields avec succès"""
        data = {'nombre': 'Test', 'precio': 10.0}
        required = ['nombre', 'precio']
        
        # Ne devrait pas lever d'exception
        self.service.validate_required_fields(data, required, ValidationError)
    
    def test_validate_required_fields_missing(self):
        """Test de validate_required_fields avec champs manquants"""
        data = {'nombre': 'Test'}
        required = ['nombre', 'precio']
        
        with self.assertRaises(ValidationError) as cm:
            self.service.validate_required_fields(data, required, ValidationError)
        
        self.assertIn('precio', str(cm.exception))
    
    def test_validate_positive_number_success(self):
        """Test de validate_positive_number avec succès"""
        # Ne devrait pas lever d'exception
        self.service.validate_positive_number(10.5, 'precio', ValidationError)
        self.service.validate_positive_number(0, 'precio', ValidationError)
    
    def test_validate_positive_number_negative(self):
        """Test de validate_positive_number avec nombre négatif"""
        with self.assertRaises(ValidationError) as cm:
            self.service.validate_positive_number(-5, 'precio', ValidationError)
        
        self.assertIn('positivo', str(cm.exception))
    
    def test_validate_positive_number_invalid(self):
        """Test de validate_positive_number avec valeur invalide"""
        with self.assertRaises(ValidationError) as cm:
            self.service.validate_positive_number('abc', 'precio', ValidationError)
        
        self.assertIn('válido', str(cm.exception))
    
    def test_validate_id_success(self):
        """Test de validate_id avec succès"""
        # Ne devrait pas lever d'exception
        self.service.validate_id(1, 'cliente', ClientValidationError)
        self.service.validate_id('5', 'cliente', ClientValidationError)
    
    def test_validate_id_zero(self):
        """Test de validate_id avec zéro"""
        with self.assertRaises(ClientValidationError) as cm:
            self.service.validate_id(0, 'cliente', ClientValidationError)
        
        self.assertIn('inválido', str(cm.exception))
    
    def test_validate_id_negative(self):
        """Test de validate_id avec nombre négatif"""
        with self.assertRaises(ClientValidationError) as cm:
            self.service.validate_id(-1, 'cliente', ClientValidationError)
        
        self.assertIn('inválido', str(cm.exception))
    
    def test_validate_id_invalid(self):
        """Test de validate_id avec valeur invalide"""
        with self.assertRaises(ClientValidationError) as cm:
            self.service.validate_id('abc', 'cliente', ClientValidationError)
        
        self.assertIn('entero', str(cm.exception))
    
    def test_execute_query_fetch_all(self):
        """Test de execute_query avec fetch_all"""
        # Créer une table de test
        conn = self.service.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO test VALUES (1, 'Test1')")
        cursor.execute("INSERT INTO test VALUES (2, 'Test2')")
        conn.commit()
        conn.close()
        
        # Exécuter la requête
        results = self.service.execute_query("SELECT * FROM test")
        self.assertEqual(len(results), 2)
    
    def test_execute_query_fetch_one(self):
        """Test de execute_query avec fetch_one"""
        # Créer une table de test
        conn = self.service.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO test VALUES (1, 'Test1')")
        conn.commit()
        conn.close()
        
        # Exécuter la requête
        result = self.service.execute_query("SELECT * FROM test WHERE id = 1", fetch_one=True, fetch_all=False)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
    
    def test_execute_query_error(self):
        """Test de execute_query avec erreur SQL"""
        with self.assertRaises(DatabaseError):
            self.service.execute_query("SELECT * FROM nonexistent_table")


if __name__ == '__main__':
    unittest.main()

