#!/usr/bin/env python3
"""
Tests pour valider l'isolation des bases de données de test
Vérifie que chaque test utilise une DB séparée et que le nettoyage fonctionne
"""

import pytest
import os
import threading
import tempfile
from database.models import Producto, Organizacion
from test.utils.test_database_manager import test_db_manager, isolated_test_db, isolated_test_environment

class TestDatabaseIsolation:
    """Tests pour l'isolation des bases de données"""
    @pytest.fixture(autouse=True)
    def setup(self, patched_models_db):
        """Setup avec patched_models_db"""
        self.db = patched_models_db
        yield

    
    def test_temp_db_isolation(self, unit_db):
        """Test que temp_db est isolée pour chaque test"""
        # Ajouter un produit
        producto = Producto(
            nombre="Test Isolation 1",
            referencia="ISO-001",
            precio=10.0
        )
        producto.save()
        
        # Vérifier qu'il existe
        productos = Producto.get_all()
        assert len(productos) == 1
        assert productos[0].nombre == "Test Isolation 1"
    
    def test_temp_db_isolation_second_test(self, unit_db):
        """Test que la DB est vide pour ce nouveau test"""
        # Cette DB devrait être vide (nouveau test = nouvelle DB)
        productos = Producto.get_all()
        assert len(productos) == 0, "La base de données devrait être vide pour ce nouveau test"
        
        # Ajouter un produit différent
        producto = Producto(
            nombre="Test Isolation 2",
            referencia="ISO-002",
            precio=20.0
        )
        producto.save()
        
        # Vérifier qu'il existe
        productos = Producto.get_all()
        assert len(productos) == 1
        assert productos[0].nombre == "Test Isolation 2"
    
    @pytest.mark.isolated_db
    def test_isolated_db_fixture(self, isolated_db):
        """Test avec fixture isolated_db"""
        from database import database

        # Sauvegarder l'instance globale originale
        original_db = database.db

        try:
            # Remplacer temporairement l'instance globale
            database.db = isolated_db

            # Ajouter un produit
            producto = Producto(
                nombre="Test Isolated",
                referencia="ISOL-001",
                precio=15.0
            )
            producto.save()

            # Vérifier qu'il existe
            productos = Producto.get_all()
            assert len(productos) == 1
            assert productos[0].nombre == "Test Isolated"

        finally:
            # Restaurer l'instance globale originale
            database.db = original_db
    
    @pytest.mark.clean_db
    def test_clean_db_fixture(self, clean_db):
        """Test avec fixture clean_db"""
        # La DB devrait être complètement vide
        productos = Producto.get_all()
        assert len(productos) == 0
        
        # Ajouter des données
        for i in range(3):
            producto = Producto(
                nombre=f"Clean Test {i}",
                referencia=f"CLEAN-{i:03d}",
                precio=float(i * 10)
            )
            producto.save()
        
        # Vérifier les données
        productos = Producto.get_all()
        assert len(productos) == 3
    
    def test_isolated_environment_context_manager(self):
        """Test du context manager isolated_environment"""
        from database import database

        with isolated_test_environment("test_context") as env:
            test_db = env['db']
            temp_dir = env['temp_dir']

            # Vérifier que la DB et le répertoire existent
            assert os.path.exists(env['db_path'])
            assert os.path.exists(temp_dir)

            # Sauvegarder l'instance globale originale
            original_db = database.db

            try:
                # Remplacer temporairement l'instance globale
                database.db = test_db

                producto = Producto(
                    nombre="Context Test",
                    referencia="CTX-001",
                    precio=25.0
                )
                producto.save()

                productos = Producto.get_all()
                assert len(productos) == 1

            finally:
                # Restaurer l'instance globale originale
                database.db = original_db
        
        # Après le context manager, les ressources devraient être nettoyées
        # (mais on ne peut pas tester directement car le nettoyage est asynchrone)
    
    def test_database_manager_stats(self):
        """Test des statistiques du gestionnaire de DB"""
        # Créer quelques bases de données de test
        db1, path1 = test_db_manager.create_test_database("stats_test_1")
        db2, path2 = test_db_manager.create_test_database("stats_test_2")
        
        # Créer un répertoire de test
        temp_dir = test_db_manager.create_test_directory("stats_test_dir")
        
        # Obtenir les statistiques
        stats = test_db_manager.get_test_stats()
        
        # Vérifier les statistiques
        current_thread = threading.get_ident()
        assert current_thread in stats['databases_by_thread']
        assert stats['databases_by_thread'][current_thread] >= 2
        assert current_thread in stats['directories_by_thread']
        assert stats['directories_by_thread'][current_thread] >= 1
        
        # Le nettoyage sera fait automatiquement par pytest_runtest_teardown
    
    def test_database_reset_functionality(self, unit_db):
        """Test de la fonctionnalité de remise à zéro de la base de données"""
        # Ajouter des données
        producto = Producto(
            nombre="Reset Test",
            referencia="RESET-001",
            precio=30.0
        )
        producto.save()
        
        # Vérifier que les données existent
        productos = Producto.get_all()
        assert len(productos) == 1
        
        # Remettre à zéro
        test_db_manager.reset_database(unit_db)
        
        # Vérifier que les données ont été supprimées
        productos = Producto.get_all()
        assert len(productos) == 0
        
        # NOTE: Organizacion n'est plus dans la DB mais dans config.json
        # donc elle n'est pas affectée par le reset de la DB
    

    
    def test_database_path_uniqueness(self):
        """Test que chaque DB de test a un chemin unique"""
        paths = set()
        
        # Créer plusieurs bases de données
        for i in range(5):
            db, path = test_db_manager.create_test_database(f"unique_test_{i}")
            assert path not in paths, f"Chemin dupliqué: {path}"
            paths.add(path)
            assert os.path.exists(path), f"Fichier DB n'existe pas: {path}"
        
        # Vérifier que tous les chemins sont différents
        assert len(paths) == 5, "Tous les chemins devraient être uniques"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
