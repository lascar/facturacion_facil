# -*- coding: utf-8 -*-
"""
Tests unitaires pour OrganizacionService
"""

import unittest
import tempfile
import os
from services.organizacion_service import OrganizacionService
from utils.exceptions import (
    OrganizationValidationError, OrganizationNotFoundError,
    DatabaseError
)


class TestOrganizacionService(unittest.TestCase):
    """Tests pour OrganizacionService"""
    
    def setUp(self):
        """Préparer les tests"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.service = OrganizacionService(self.temp_db.name)
    
    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
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
        self.assertTrue(success)
    
    def test_create_organizacion_missing_nombre(self):
        """Test création d'une organisation sans nom"""
        org_data = {
            'cif': 'A12345678'
        }
        
        with self.assertRaises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_invalid_cif(self):
        """Test création d'une organisation avec CIF invalide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'cif': '123'  # Trop court
        }
        
        with self.assertRaises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_invalid_email(self):
        """Test création d'une organisation avec email invalide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'email': 'invalid-email'  # Sans @
        }
        
        with self.assertRaises(OrganizationValidationError):
            self.service.create_organizacion(org_data)
    
    def test_create_organizacion_numero_factura_simple(self):
        """Test création avec numéro de facture simple (numérique)"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '1'
        }

        success = self.service.create_organizacion(org_data)
        self.assertTrue(success)

        # Vérifier que le numéro est bien sauvegardé
        org = self.service.get_organizacion()
        self.assertEqual(org['numero_factura_inicial'], '1')

    def test_create_organizacion_numero_factura_alphanumeric(self):
        """Test création avec numéro de facture alphanumérique"""
        test_cases = [
            'fact-2005-1',
            'FAC-2025-001',
            'INV-2024-0001',
            '2025-FACT-1'
        ]

        for i, numero in enumerate(test_cases):
            with self.subTest(numero=numero):
                org_data = {
                    'nombre': 'Mi Empresa',
                    'numero_factura_inicial': numero
                }

                # Premier test: create, les suivants: update
                if i == 0:
                    success = self.service.create_organizacion(org_data)
                else:
                    success = self.service.update_organizacion(org_data)

                self.assertTrue(success)

                # Vérifier que le numéro est bien sauvegardé
                org = self.service.get_organizacion()
                self.assertEqual(org['numero_factura_inicial'], numero)

    def test_create_organizacion_numero_factura_empty(self):
        """Test création avec numéro de facture vide"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': ''
        }

        with self.assertRaises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        self.assertIn('no puede estar vacío', str(context.exception))

    def test_create_organizacion_numero_factura_only_spaces(self):
        """Test création avec numéro de facture contenant seulement des espaces"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '   '
        }

        with self.assertRaises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        self.assertIn('no puede estar vacío', str(context.exception))

    def test_create_organizacion_numero_factura_no_alphanumeric(self):
        """Test création avec numéro de facture sans caractères alphanumériques"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': '---'
        }

        with self.assertRaises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        self.assertIn('debe contener al menos un número o letra', str(context.exception))

    def test_create_organizacion_numero_factura_too_long(self):
        """Test création avec numéro de facture trop long"""
        org_data = {
            'nombre': 'Mi Empresa',
            'numero_factura_inicial': 'a' * 51  # Plus de 50 caractères
        }

        with self.assertRaises(OrganizationValidationError) as context:
            self.service.create_organizacion(org_data)

        self.assertIn('demasiado largo', str(context.exception))
    
    def test_get_organizacion_exists(self):
        """Test récupération d'une organisation existante"""
        # Créer une organisation
        self.service.create_organizacion({
            'nombre': 'Mi Empresa',
            'cif': 'A12345678'
        })
        
        # Récupérer
        org = self.service.get_organizacion()
        self.assertIsNotNone(org)
        self.assertEqual(org['nombre'], 'Mi Empresa')
    
    def test_get_organizacion_not_exists(self):
        """Test récupération quand l'organisation n'existe pas"""
        org = self.service.get_organizacion()
        self.assertIsNone(org)
    
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
        
        self.assertTrue(success)
        
        # Vérifier la mise à jour
        org = self.service.get_organizacion()
        self.assertEqual(org['nombre'], 'Empresa Actualizada')
    
    def test_update_organizacion_creates_if_not_exists(self):
        """Test que update crée l'organisation si elle n'existe pas"""
        # Vérifier qu'elle n'existe pas
        org = self.service.get_organizacion()
        self.assertIsNone(org)
        
        # Mettre à jour (devrait créer)
        success = self.service.update_organizacion({
            'nombre': 'Nueva Empresa',
            'cif': 'A12345678'
        })
        
        self.assertTrue(success)
        
        # Vérifier la création
        org = self.service.get_organizacion()
        self.assertIsNotNone(org)
        self.assertEqual(org['nombre'], 'Nueva Empresa')

    def test_update_organizacion_invalid_cif(self):
        """Test mise à jour avec CIF trop court"""
        # Créer d'abord
        self.service.create_organizacion({
            'nombre': 'Mi Empresa',
            'cif': 'A12345678'
        })

        # Tenter de mettre à jour avec CIF invalide
        with self.assertRaises(OrganizationValidationError):
            self.service.update_organizacion({
                'nombre': 'Mi Empresa',
                'cif': 'ABC'  # Trop court
            })


if __name__ == '__main__':
    unittest.main()

