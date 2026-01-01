# -*- coding: utf-8 -*-
"""
Tests unitaires pour ClienteService
"""

import pytest
import tempfile
import os
from services.cliente_service import ClienteService
from utils.exceptions import (
    ClientValidationError, ClientNotFoundError,
    DatabaseError
)


class TestClienteService:
    """Tests pour ClienteService"""

    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)

        self.service = ClienteService(unit_db.db_path)

        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path

        yield
        # Le nettoyage est géré par la fixture unit_db
    
    def test_create_cliente_success(self):
        """Test création d'un client avec succès"""
        cliente_data = {
            'nombre': 'Cliente Test',
            'nif': '12345678A',
            'email': 'test@example.com',
            'telefono': '123456789',
            'direccion': 'Calle Test 123'
        }
        
        cliente_id = self.service.create_cliente(cliente_data)
        assert cliente_id is not None
        assert cliente_id > 0
    
    def test_create_cliente_missing_nombre(self):
        """Test création d'un client sans nom"""
        cliente_data = {
            'email': 'test@example.com'
        }
        
        with pytest.raises(ClientValidationError):
            self.service.create_cliente(cliente_data)
    
    def test_create_cliente_invalid_email(self):
        """Test création d'un client avec email invalide"""
        cliente_data = {
            'nombre': 'Cliente Test',
            'email': 'invalid-email'  # Sans @
        }
        
        with pytest.raises(ClientValidationError):
            self.service.create_cliente(cliente_data)
    
    def test_get_all_clientes(self):
        """Test récupération de tous les clients"""
        # Créer quelques clients
        for i in range(3):
            self.service.create_cliente({
                'nombre': f'Cliente {i}',
                'email': f'cliente{i}@example.com'
            })
        
        clientes = self.service.get_all_clientes()
        assert isinstance(clientes, list)
        assert len(clientes) >= 3
    
    def test_get_cliente_by_id_success(self):
        """Test récupération d'un client par ID"""
        # Créer un client
        cliente_id = self.service.create_cliente({
            'nombre': 'Cliente Test',
            'email': 'test@example.com'
        })
        
        # Récupérer le client
        cliente = self.service.get_cliente_by_id(cliente_id)
        assert cliente is not None
        assert cliente['nombre'] == 'Cliente Test'
    
    def test_get_cliente_by_id_not_found(self):
        """Test récupération d'un client inexistant"""
        with pytest.raises(ClientNotFoundError):
            self.service.get_cliente_by_id(99999)
    
    def test_get_cliente_by_id_invalid_id(self):
        """Test récupération avec ID invalide"""
        with pytest.raises(ClientValidationError):
            self.service.get_cliente_by_id(-1)
    
    def test_update_cliente_success(self):
        """Test mise à jour d'un client"""
        # Créer un client
        cliente_id = self.service.create_cliente({
            'nombre': 'Cliente Original',
            'email': 'original@example.com'
        })
        
        # Mettre à jour
        success = self.service.update_cliente({
            'id': cliente_id,
            'nombre': 'Cliente Actualizado',
            'email': 'actualizado@example.com'
        })
        
        assert success
        
        # Vérifier la mise à jour
        cliente = self.service.get_cliente_by_id(cliente_id)
        assert cliente['nombre'] == 'Cliente Actualizado'
    
    def test_update_cliente_missing_id(self):
        """Test mise à jour sans ID"""
        with pytest.raises(ClientValidationError):
            self.service.update_cliente({
                'nombre': 'Cliente Test'
            })
    
    def test_delete_cliente_success(self):
        """Test suppression d'un client"""
        # Créer un client
        cliente_id = self.service.create_cliente({
            'nombre': 'Cliente Test',
            'email': 'test@example.com'
        })
        
        # Supprimer
        success = self.service.delete_cliente(cliente_id)
        assert success
        
        # Vérifier la suppression
        with pytest.raises(ClientNotFoundError):
            self.service.get_cliente_by_id(cliente_id)

    def test_update_cliente_not_found(self):
        """Test mise à jour d'un client inexistant"""
        with pytest.raises(ClientNotFoundError):
            self.service.update_cliente({
                'id': 99999,
                'nombre': 'Cliente Test',
                'email': 'test@example.com'
            })

    def test_delete_cliente_not_found(self):
        """Test suppression d'un client inexistant - devrait retourner False"""
        # delete_client retourne False si le client n'existe pas
        success = self.service.delete_cliente(99999)
        assert not success

    def test_create_cliente_empty_email(self):
        """Test création d'un client avec email vide (devrait passer)"""
        cliente_data = {
            'nombre': 'Cliente Test',
            'email': ''  # Email vide est accepté
        }

        cliente_id = self.service.create_cliente(cliente_data)
        assert cliente_id is not None

    def test_create_cliente_without_nif(self):
        """Test création d'un client sans NIF (NIF est optionnel)"""
        cliente_data = {
            'nombre': 'Cliente Sin NIF',
            'email': 'sinnif@example.com',
            'telefono': '666777888',
            'direccion': 'Calle Test 123'
            # NIF omis intentionnellement
        }

        cliente_id = self.service.create_cliente(cliente_data)
        assert cliente_id is not None

        # Vérifier que le client a été créé sans NIF
        cliente = self.service.get_cliente_by_id(cliente_id)
        assert cliente['nombre'] == 'Cliente Sin NIF'
        assert cliente.get('nif', '') == ''  # NIF devrait être vide


if __name__ == '__main__':
    unittest.main()

