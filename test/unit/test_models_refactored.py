#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour les modèles refactorisés
Vérifie l'équivalence entre models.py et models_refactored.py

Phase 2 de la refactorisation Pythonic
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.models import Cliente, Producto
from database.models_refactored import (
    ClienteRefactored,
    ProductoRefactored,
    cliente_to_refactored,
    producto_to_refactored
)
from test.base_test_with_fixtures import BaseTestWithFixtures


class TestClienteRefactored(BaseTestWithFixtures):
    """Tests pour ClienteRefactored"""

    def test_dataclass_creation(self):
        """Vérifie que la dataclass se crée correctement"""
        cliente = ClienteRefactored(
            nombre="Test Cliente",
            dni_nie="12345678A",
            direccion="Calle Test 123",
            email="test@example.com",
            telefono="666777888"
        )

        assert cliente.nombre == "Test Cliente"
        assert cliente.dni_nie == "12345678A"
        assert cliente.direccion == "Calle Test 123"
        assert cliente.email == "test@example.com"
        assert cliente.telefono == "666777888"
        assert cliente.id is None

    def test_dataclass_default_values(self):
        """Vérifie les valeurs par défaut"""
        cliente = ClienteRefactored()

        assert cliente.nombre == ""
        assert cliente.dni_nie == ""
        assert cliente.direccion == ""
        assert cliente.email == ""
        assert cliente.telefono == ""
        assert cliente.id is None

    def test_dataclass_repr(self):
        """Vérifie que __repr__ est généré automatiquement"""
        cliente = ClienteRefactored(nombre="Test", dni_nie="123")
        repr_str = repr(cliente)

        assert "ClienteRefactored" in repr_str
        assert "nombre='Test'" in repr_str
        assert "dni_nie='123'" in repr_str

    def test_dataclass_equality(self):
        """Vérifie que __eq__ est généré automatiquement"""
        cliente1 = ClienteRefactored(nombre="Test", dni_nie="123")
        cliente2 = ClienteRefactored(nombre="Test", dni_nie="123")
        cliente3 = ClienteRefactored(nombre="Other", dni_nie="456")

        assert cliente1 == cliente2
        assert cliente1 != cliente3

    def test_save_and_get_all(self):
        """Vérifie que save() et get_all() fonctionnent"""
        # Créer un client
        cliente = ClienteRefactored(
            nombre="Cliente Test",
            dni_nie="11111111A",
            direccion="Test Address",
            email="test@test.com",
            telefono="111222333"
        )

        # Sauvegarder
        cliente_id = cliente.save()
        assert cliente_id is not None
        assert cliente.id == cliente_id

        # Récupérer tous les clients
        clientes = ClienteRefactored.get_all()
        assert len(clientes) > 0

        # Vérifier que notre client est dans la liste
        found = any(c.id == cliente_id for c in clientes)
        assert found

    def test_get_by_id(self):
        """Vérifie que get_by_id() fonctionne"""
        # Créer et sauvegarder
        cliente = ClienteRefactored(nombre="Test GetById", dni_nie="22222222B")
        cliente_id = cliente.save()

        # Récupérer par ID
        retrieved = ClienteRefactored.get_by_id(cliente_id)

        assert retrieved is not None
        assert retrieved.id == cliente_id
        assert retrieved.nombre == "Test GetById"
        assert retrieved.dni_nie == "22222222B"

    def test_search(self):
        """Vérifie que search() fonctionne avec list comprehension"""
        # Créer un client avec un nom unique
        cliente = ClienteRefactored(
            nombre="SearchableCliente",
            dni_nie="33333333C",
            email="searchable@test.com"
        )
        cliente.save()

        # Rechercher
        results = ClienteRefactored.search("Searchable")

        assert len(results) > 0
        assert any(c.nombre == "SearchableCliente" for c in results)

    def test_delete(self):
        """Vérifie que delete() fonctionne"""
        # Créer et sauvegarder
        cliente = ClienteRefactored(nombre="ToDelete", dni_nie="44444444D")
        cliente_id = cliente.save()

        # Vérifier qu'il existe
        assert ClienteRefactored.get_by_id(cliente_id) is not None

        # Supprimer
        cliente.delete()

        # Vérifier qu'il n'existe plus
        assert ClienteRefactored.get_by_id(cliente_id) is None





class TestProductoRefactored(BaseTestWithFixtures):
    """Tests pour ProductoRefactored"""

    def test_dataclass_creation(self):
        """Vérifie que la dataclass Producto se crée correctement"""
        producto = ProductoRefactored(
            nombre="Test Producto",
            referencia="REF001",
            precio=99.99,
            categoria="Test",
            descripcion="Descripción test",
            iva_recomendado=21.0
        )

        assert producto.nombre == "Test Producto"
        assert producto.referencia == "REF001"
        assert producto.precio == 99.99
        assert producto.categoria == "Test"
        assert producto.iva_recomendado == 21.0

    def test_producto_default_iva(self):
        """Vérifie que DEFAULT_IVA est utilisé"""
        from config.constants import DEFAULT_IVA

        producto = ProductoRefactored(nombre="Test")
        assert producto.iva_recomendado == DEFAULT_IVA

    def test_save_and_get_all(self):
        """Vérifie que save() et get_all() fonctionnent pour Producto"""
        import time
        # Utiliser un timestamp pour garantir l'unicité de la référence
        unique_ref = f"TEST{int(time.time() * 1000) % 1000000}"

        producto = ProductoRefactored(
            nombre="Producto Test",
            referencia=unique_ref,
            precio=50.0,
            categoria="Categoria Test"
        )

        producto_id = producto.save()
        assert producto_id is not None
        assert producto.id == producto_id

        productos = ProductoRefactored.get_all()
        assert len(productos) > 0

        found = any(p.id == producto_id for p in productos)
        assert found


class TestConversionFunctions:
    """Tests pour les fonctions de conversion"""

    def test_cliente_to_refactored(self):
        """Vérifie la conversion Cliente -> ClienteRefactored"""
        cliente_original = Cliente(
            id=1,
            nombre="Test Cliente",
            dni_nie="12345678A",
            direccion="Calle Test",
            email="test@test.com",
            telefono="666777888"
        )

        cliente_refactored = cliente_to_refactored(cliente_original)

        assert cliente_refactored.id == cliente_original.id
        assert cliente_refactored.nombre == cliente_original.nombre
        assert cliente_refactored.dni_nie == cliente_original.dni_nie

    def test_producto_to_refactored(self):
        """Vérifie la conversion Producto -> ProductoRefactored"""
        producto_original = Producto(
            id=1,
            nombre="Test Producto",
            referencia="REF001",
            precio=99.99,
            categoria="Test"
        )

        producto_refactored = producto_to_refactored(producto_original)

        assert producto_refactored.id == producto_original.id
        assert producto_refactored.nombre == producto_original.nombre
        assert producto_refactored.precio == producto_original.precio


class TestPythonicFeatures:
    """Tests pour vérifier les features Pythonic"""

    def test_dataclass_features(self):
        """Vérifie que les features de dataclass sont actives"""
        from dataclasses import is_dataclass

        assert is_dataclass(ClienteRefactored)
        assert is_dataclass(ProductoRefactored)

    def test_type_annotations_present(self):
        """Vérifie que les type annotations sont présentes"""
        annotations = ClienteRefactored.__annotations__

        assert 'nombre' in annotations
        assert 'dni_nie' in annotations
        assert 'id' in annotations
