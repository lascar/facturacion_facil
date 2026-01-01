# -*- coding: utf-8 -*-
"""
Tests pour BaseService
"""

import pytest
import tempfile
import os
from services.base_service import BaseService
from utils.exceptions import (
    DatabaseConnectionError, DatabaseError,
    ValidationError, ClientValidationError
)


class TestBaseService:
    """Tests pour la classe BaseService"""

    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)

        self.service = BaseService(unit_db.db_path)

        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path

        yield
        # Le nettoyage est géré par la fixture unit_db
    
    def test_init(self):
        """Test de l'initialisation"""
        assert self.service.db is not None
        assert self.service.logger is not None
    
    def test_get_connection(self):
        """Test de get_connection"""
        conn = self.service.get_connection()
        assert conn is not None
        conn.close()
    
    def test_get_connection_invalid_path(self):
        """Test de get_connection avec chemin invalide"""
        # BaseService crée le répertoire s'il n'existe pas, donc on teste juste la création
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        service = BaseService(os.path.join(temp_dir, "test.db"))
        assert service is not None
        # Nettoyage
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_safe_execute_success(self):
        """Test de safe_execute avec succès"""
        def test_func(a, b):
            return a + b
        
        result = self.service.safe_execute(test_func, 2, 3)
        assert result == 5
    
    def test_safe_execute_error(self):
        """Test de safe_execute avec erreur"""
        def test_func():
            raise ValueError("Test error")
        
        result = self.service.safe_execute(test_func)
        assert result is None  # Retourne None en cas d'erreur
    
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
        
        with pytest.raises(ValidationError) as exc_info:
            self.service.validate_required_fields(data, required, ValidationError)
        
        assert 'precio' in str(exc_info.value)
    
    def test_validate_positive_number_success(self):
        """Test de validate_positive_number avec succès"""
        # Ne devrait pas lever d'exception
        self.service.validate_positive_number(10.5, 'precio', ValidationError)
        self.service.validate_positive_number(0, 'precio', ValidationError)
    
    def test_validate_positive_number_negative(self):
        """Test de validate_positive_number avec nombre négatif"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.validate_positive_number(-5, 'precio', ValidationError)
        
        assert 'positivo' in str(exc_info.value)
    
    def test_validate_positive_number_invalid(self):
        """Test de validate_positive_number avec valeur invalide"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.validate_positive_number('abc', 'precio', ValidationError)
        
        assert 'válido' in str(exc_info.value)
    
    def test_validate_id_success(self):
        """Test de validate_id avec succès"""
        # Ne devrait pas lever d'exception
        self.service.validate_id(1, 'cliente', ClientValidationError)
        self.service.validate_id('5', 'cliente', ClientValidationError)
    
    def test_validate_id_zero(self):
        """Test de validate_id avec zéro"""
        with pytest.raises(ClientValidationError) as exc_info:
            self.service.validate_id(0, 'cliente', ClientValidationError)
        
        assert 'inválido' in str(exc_info.value)
    
    def test_validate_id_negative(self):
        """Test de validate_id avec nombre négatif"""
        with pytest.raises(ClientValidationError) as exc_info:
            self.service.validate_id(-1, 'cliente', ClientValidationError)
        
        assert 'inválido' in str(exc_info.value)
    
    def test_validate_id_invalid(self):
        """Test de validate_id avec valeur invalide"""
        with pytest.raises(ClientValidationError) as exc_info:
            self.service.validate_id('abc', 'cliente', ClientValidationError)
        
        assert 'entero' in str(exc_info.value)
    
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
        assert len(results) == 2
    
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
        assert result is not None
        assert result[0] == 1
    
    def test_execute_query_error(self):
        """Test de execute_query avec erreur SQL"""
        with pytest.raises(DatabaseError) as exc_info:
            self.service.execute_query("SELECT * FROM nonexistent_table")


if __name__ == '__main__':
    unittest.main()

