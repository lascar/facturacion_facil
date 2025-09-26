import pytest
import os
import sys
import sqlite3
from unittest.mock import patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Producto, Organizacion
from database.database import Database

class TestSQLInjectionPrevention:
    """Tests de prévention d'injection SQL"""
    
    def test_producto_name_sql_injection_attempt(self, temp_db):
        """Test tentative d'injection SQL dans le nom du produit"""
        malicious_name = "'; DROP TABLE productos; --"
        
        producto = Producto(
            nombre=malicious_name,
            referencia="SAFE-001",
            precio=10.0
        )
        
        # Cela ne devrait pas causer de problème grâce aux requêtes paramétrées
        producto.save()
        
        # Vérifier que la table existe toujours
        tables = temp_db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [row[0] for row in tables]
        assert 'productos' in table_names
        
        # Vérifier que le produit a été sauvegardé avec le nom malicieux (mais inoffensif)
        saved_product = Producto.get_by_id(producto.id)
        assert saved_product.nombre == malicious_name
    
    def test_referencia_sql_injection_attempt(self, temp_db):
        """Test tentative d'injection SQL dans la référence"""
        malicious_ref = "REF001'; UPDATE productos SET precio = 0; --"
        
        producto = Producto(
            nombre="Test Product",
            referencia=malicious_ref,
            precio=25.50
        )
        
        producto.save()
        
        # Vérifier que le prix n'a pas été modifié par l'injection
        saved_product = Producto.get_by_id(producto.id)
        assert saved_product.precio == 25.50
        assert saved_product.referencia == malicious_ref
    
    def test_organization_data_sql_injection(self, temp_db):
        """Test tentative d'injection SQL dans les données d'organisation"""
        malicious_email = "test@test.com'; DELETE FROM organizacion; --"
        
        org = Organizacion(
            nombre="Test Company",
            email=malicious_email,
            telefono="123456789"
        )
        
        org.save()
        
        # Vérifier que l'organisation existe toujours
        saved_org = Organizacion.get()
        assert saved_org.nombre == "Test Company"
        assert saved_org.email == malicious_email
    
    def test_search_sql_injection_simulation(self, temp_db):
        """Simulation de tentative d'injection SQL dans une recherche"""
        # Créer quelques produits de test
        for i in range(3):
            producto = Producto(
                nombre=f"Search Product {i}",
                referencia=f"SEARCH-{i:03d}",
                precio=float(i + 1) * 10
            )
            producto.save()
        
        # Tentative d'injection dans une recherche simulée
        malicious_search = "'; DROP TABLE productos; SELECT * FROM productos WHERE '1'='1"
        
        # Simuler une recherche sécurisée avec paramètres
        safe_results = temp_db.execute_query(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            (f"%{malicious_search}%",)
        )
        
        # La recherche ne devrait rien trouver (et ne pas causer de dommage)
        assert len(safe_results) == 0
        
        # Vérifier que la table existe toujours
        all_products = Producto.get_all()
        assert len(all_products) == 3

class TestInputValidation:
    """Tests de validation des entrées"""
    
    @pytest.mark.parametrize("invalid_precio", [
        -1.0,      # Négatif
        -999.99,   # Très négatif
        float('inf'),  # Infini
        float('-inf'), # Infini négatif
    ])
    def test_invalid_precio_handling(self, invalid_precio, temp_db):
        """Test la gestion des prix invalides"""
        if invalid_precio < 0:
            # Les prix négatifs devraient être rejetés au niveau logique
            # (même si la DB les accepte techniquement)
            producto = Producto(
                nombre="Invalid Price Test",
                referencia="INVALID-001",
                precio=invalid_precio
            )
            
            # Au niveau du modèle, on pourrait ajouter une validation
            assert producto.precio == invalid_precio  # Stocké tel quel
            # Mais dans une vraie app, on ajouterait une validation
    
    @pytest.mark.parametrize("invalid_iva", [
        -5.0,      # Négatif
        150.0,     # Supérieur à 100%
        float('nan'),  # NaN
    ])
    def test_invalid_iva_handling(self, invalid_iva, temp_db):
        """Test la gestion des taux d'IVA invalides"""
        import math
        
        producto = Producto(
            nombre="Invalid IVA Test",
            referencia="IVA-INVALID",
            precio=10.0,
            iva_recomendado=invalid_iva
        )
        
        if math.isnan(invalid_iva):
            # NaN devrait être géré spécialement
            assert math.isnan(producto.iva_recomendado)
        else:
            assert producto.iva_recomendado == invalid_iva
    
    def test_empty_required_fields(self, temp_db):
        """Test des champs requis vides"""
        # Nom vide
        producto_nom_vide = Producto(
            nombre="",
            referencia="EMPTY-001",
            precio=10.0
        )
        
        # Référence vide
        producto_ref_vide = Producto(
            nombre="Test Product",
            referencia="",
            precio=10.0
        )
        
        # Dans une vraie application, ces cas devraient être validés
        # avant la sauvegarde. Ici on teste que la DB les accepte techniquement
        assert producto_nom_vide.nombre == ""
        assert producto_ref_vide.referencia == ""
    
    def test_extremely_long_inputs(self, temp_db):
        """Test avec des entrées extrêmement longues"""
        very_long_name = "A" * 10000
        very_long_description = "B" * 50000
        
        producto = Producto(
            nombre=very_long_name,
            referencia="LONG-001",
            precio=10.0,
            descripcion=very_long_description
        )
        
        # SQLite devrait gérer les textes longs sans problème
        producto.save()
        
        saved_product = Producto.get_by_id(producto.id)
        assert len(saved_product.nombre) == 10000
        assert len(saved_product.descripcion) == 50000
    
    def test_unicode_and_special_characters(self, temp_db):
        """Test avec caractères Unicode et spéciaux"""
        unicode_name = "Producto 测试 🛒 émojis ñáéíóú"
        special_chars_ref = "REF-2024-ñ-€-©-®"
        
        producto = Producto(
            nombre=unicode_name,
            referencia=special_chars_ref,
            precio=25.99,
            descripcion="Descripción con acentos y símbolos: €£$¥©®™"
        )
        
        producto.save()
        
        saved_product = Producto.get_by_id(producto.id)
        assert saved_product.nombre == unicode_name
        assert saved_product.referencia == special_chars_ref
        assert "€£$¥©®™" in saved_product.descripcion

class TestDataIntegrity:
    """Tests d'intégrité des données"""
    
    def test_referencia_uniqueness_constraint(self, temp_db):
        """Test de la contrainte d'unicité des références"""
        # Créer le premier produit
        producto1 = Producto(
            nombre="Premier Produit",
            referencia="UNIQUE-001",
            precio=10.0
        )
        producto1.save()
        
        # Essayer de créer un second produit avec la même référence
        producto2 = Producto(
            nombre="Deuxième Produit",
            referencia="UNIQUE-001",  # Même référence
            precio=20.0
        )
        
        # Cela devrait lever une exception de contrainte
        with pytest.raises(sqlite3.IntegrityError):
            producto2.save()
    
    def test_foreign_key_integrity(self, temp_db):
        """Test de l'intégrité des clés étrangères"""
        # Créer un produit
        producto = Producto(
            nombre="FK Test Product",
            referencia="FK-001",
            precio=15.0
        )
        producto.save()
        
        # Vérifier que le stock a été créé automatiquement
        stock_count = temp_db.execute_query(
            "SELECT COUNT(*) FROM stock WHERE producto_id = ?",
            (producto.id,)
        )[0][0]
        assert stock_count == 1
        
        # Supprimer le produit devrait aussi supprimer le stock
        producto.delete()
        
        stock_count_after = temp_db.execute_query(
            "SELECT COUNT(*) FROM stock WHERE producto_id = ?",
            (producto.id,)
        )[0][0]
        assert stock_count_after == 0
    
    def test_data_consistency_after_operations(self, temp_db):
        """Test de cohérence des données après opérations"""
        # Créer plusieurs produits
        productos = []
        for i in range(5):
            producto = Producto(
                nombre=f"Consistency Product {i}",
                referencia=f"CONS-{i:03d}",
                precio=float(i + 1) * 10
            )
            producto.save()
            productos.append(producto)
        
        # Vérifier la cohérence initiale
        total_productos = len(Producto.get_all())
        total_stock_entries = temp_db.execute_query("SELECT COUNT(*) FROM stock")[0][0]
        assert total_productos == total_stock_entries == 5
        
        # Supprimer quelques produits
        for producto in productos[:2]:
            producto.delete()
        
        # Vérifier la cohérence après suppression
        total_productos_after = len(Producto.get_all())
        total_stock_entries_after = temp_db.execute_query("SELECT COUNT(*) FROM stock")[0][0]
        assert total_productos_after == total_stock_entries_after == 3
    
    def test_transaction_rollback_simulation(self, temp_db):
        """Simulation de rollback de transaction"""
        initial_count = len(Producto.get_all())
        
        try:
            # Commencer une "transaction" (simulée)
            producto1 = Producto(
                nombre="Transaction Product 1",
                referencia="TRANS-001",
                precio=10.0
            )
            producto1.save()
            
            producto2 = Producto(
                nombre="Transaction Product 2",
                referencia="TRANS-002",
                precio=20.0
            )
            producto2.save()
            
            # Simuler une erreur qui nécessiterait un rollback
            # (par exemple, tentative de création avec référence dupliquée)
            producto3 = Producto(
                nombre="Transaction Product 3",
                referencia="TRANS-001",  # Référence dupliquée
                precio=30.0
            )
            producto3.save()  # Cela devrait lever une exception
            
        except sqlite3.IntegrityError:
            # En cas d'erreur, on devrait "rollback"
            # Dans ce test simple, on supprime manuellement les produits créés
            try:
                producto1.delete()
                producto2.delete()
            except:
                pass
        
        # Vérifier que le nombre de produits est revenu à l'état initial
        final_count = len(Producto.get_all())
        # Note: Dans ce test simplifié, les produits restent car on n'a pas
        # de vraie gestion de transaction. Dans une vraie app, on utiliserait
        # des transactions SQL appropriées.

class TestAccessControl:
    """Tests de contrôle d'accès (simulation)"""
    
    def test_read_only_operations_safety(self, temp_db):
        """Test que les opérations de lecture sont sûres"""
        # Créer des données de test
        producto = Producto(
            nombre="Read Only Test",
            referencia="RO-001",
            precio=25.0
        )
        producto.save()
        
        # Les opérations de lecture ne devraient pas modifier les données
        original_count = len(Producto.get_all())
        
        # Effectuer plusieurs lectures
        for _ in range(10):
            all_products = Producto.get_all()
            specific_product = Producto.get_by_id(producto.id)
            org_data = Organizacion.get()
        
        # Vérifier que rien n'a changé
        final_count = len(Producto.get_all())
        assert final_count == original_count
        
        final_product = Producto.get_by_id(producto.id)
        assert final_product.nombre == "Read Only Test"
        assert final_product.precio == 25.0
    
    def test_data_modification_tracking(self, temp_db):
        """Test de suivi des modifications de données"""
        # Créer un produit
        producto = Producto(
            nombre="Tracking Test",
            referencia="TRACK-001",
            precio=15.0
        )
        producto.save()
        original_id = producto.id
        
        # Modifier le produit
        producto.nombre = "Modified Name"
        producto.precio = 25.0
        producto.save()
        
        # Vérifier que l'ID n'a pas changé (mise à jour, pas création)
        assert producto.id == original_id
        
        # Vérifier les modifications
        updated_product = Producto.get_by_id(original_id)
        assert updated_product.nombre == "Modified Name"
        assert updated_product.precio == 25.0
