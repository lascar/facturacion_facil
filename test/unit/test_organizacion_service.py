# -*- coding: utf-8 -*-
"""
Tests unitaires pour OrganizacionService
"""

import pytest
import tempfile
import os
from services.organizacion_service import OrganizacionService
from utils.exceptions import (
    OrganizationValidationError, OrganizationNotFoundError,
    DatabaseError
)


class TestOrganizacionService:
    """Tests pour OrganizacionService"""
    
    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)
        
        self.service = OrganizacionService(unit_db.db_path)
        
        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path
        
        yield
        # Le nettoyage est géré par la fixture unit_db


    def test_create_organizacion_success(self):
        """Test création d'une organisation avec succès"""
        org_data = {
            'nombre': 'Mi Empresa',
            'cif': 'A12345678',
            'email': 'info@empresa.com',
            'telefono': '123456789',
            'direccion': 'Calle Principal 1',
            'numero_factura_inicial': '1'
        }
        
        success = self.service.create_organizacion(org_data)
        assert success
    
    def test_create_organizacion_missing_nombre(self):
        """Test création d'une organisation sans nom"""
        org_data = {
            'cif': 'A12345678'
        }
        
        with pytest.raises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_invalid_cif(self):
        """Test création d'une organisation avec CIF invalide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'cif': '123'  # Trop court
        }
        
        with pytest.raises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_invalid_email(self):
        """Test création d'une organisation avec email invalide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'email': 'invalid-email'  # Sans @
        }
        
        with pytest.raises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_numero_factura_simple(self):
        """Test création avec numéro de facture simple (numérique)"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '1'
        }

        success = self.service.create_organizacion(org_data)
        assert success

        # Vérifier que le numéro est bien sauvegardé
        org = self.service.get_organizacion()
        assert org['numero_factura_inicial'] == '1'

    def test_create_organizacion_numero_factura_alphanumeric(self):
        """Test création avec numéro de facture alphanumérique"""
        test_cases = [
            'fact-2005-1',
            'FAC-2025-001',
            'INV-2024-0001',
            '2025-FACT-1'
        ]

        for i, numero in enumerate(test_cases):
            org_data = {
                'nombre': 'Mi Empresa',
                'numero_factura_inicial': numero
            }

            # Premier test: create, les suivants: update
            if i == 0:
                success = self.service.create_organizacion(org_data)
            else:
                success = self.service.update_organizacion(org_data)

            assert success, f"Failed for numero: {numero}"

            # Vérifier que le numéro est bien sauvegardé
            org = self.service.get_organizacion()
            assert org['numero_factura_inicial'] == numero, f"Expected {numero}, got {org['numero_factura_inicial']}"

    def test_create_organizacion_numero_factura_empty(self):
        """Test création avec numéro de facture vide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': ''
        }

        with pytest.raises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        assert 'no puede estar vacío' in str(context.value)

    def test_create_organizacion_numero_factura_only_spaces(self):
        """Test création avec numéro de facture contenant seulement des espaces"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '   '
        }

        with pytest.raises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        assert 'no puede estar vacío' in str(context.value)

    def test_create_organizacion_numero_factura_no_alphanumeric(self):
        """Test création avec numéro de facture sans caractères alphanumériques"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '---'
        }

        with pytest.raises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        assert 'debe contener al menos un número o letra' in str(context.value)

    def test_create_organizacion_numero_factura_too_long(self):
        """Test création avec numéro de facture trop long"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': 'a' * 51  # Plus de 50 caractères
        }

        with pytest.raises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        assert 'demasiado largo' in str(context.value)
    
    def test_get_organizacion_exists(self):
        """Test récupération d'une organisation existante"""
        # Créer une organisation
        self.service.create_organizacion({
            'nombre': 'Mi Empresa',
            'cif': 'A12345678'
        })
        
        # Récupérer
        org = self.service.get_organizacion()
        assert org is not None
        assert org['nombre'] == 'Mi Empresa'
    
    def test_get_organizacion_not_exists(self):
        """Test récupération quand l'organisation n'existe pas"""
        org = self.service.get_organizacion()
        assert org is None
    
    def test_update_organizacion_success(self):
        """Test mise à jour d'une organisation"""
        # Créer une organisation
        self.service.create_organizacion({
            'nombre': 'Empresa Original',
            'cif': 'A12345678'
        })
        
        # Mettre à jour
        success = self.service.update_organizacion({
            'nombre': 'Empresa Actualizada',
            'cif': 'B87654321'
        })
        
        assert success
        
        # Vérifier la mise à jour
        org = self.service.get_organizacion()
        assert org['nombre'] == 'Empresa Actualizada'
    
    def test_update_organizacion_creates_if_not_exists(self):
        """Test que update crée l'organisation si elle n'existe pas"""
        # Vérifier qu'elle n'existe pas
        org = self.service.get_organizacion()
        assert org is None
        
        # Mettre à jour (devrait créer)
        success = self.service.update_organizacion({
            'nombre': 'Nueva Empresa',
            'cif': 'A12345678'
        })
        
        assert success
        
        # Vérifier la création
        org = self.service.get_organizacion()
        assert org is not None
        assert org['nombre'] == 'Nueva Empresa'

    def test_update_organizacion_invalid_cif(self):
        """Test mise à jour avec CIF trop court"""
        # Créer d'abord
        self.service.create_organizacion({
            'nombre': 'Mi Empresa',
            'cif': 'A12345678'
        })

        # Tenter de mettre à jour avec CIF invalide
        with pytest.raises(OrganizationValidationError):
            self.service.update_organizacion({
                'nombre': 'Mi Empresa',
                'cif': 'ABC'  # Trop court
            })


if __name__ == '__main__':
    unittest.main()

