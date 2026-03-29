# -*- coding: utf-8 -*-
"""
Tests unitaires pour FacturaService
"""

import pytest
import tempfile
import os
from datetime import datetime
from services.factura_service import FacturaService
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from utils.exceptions import (
    InvoiceValidationError, InvoiceNotFoundError,
    DatabaseError, InsufficientStockError
)


class TestFacturaService:
    """Tests pour FacturaService"""

    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)

        self.service = FacturaService(unit_db.db_path)
        self.producto_service = ProductoService(unit_db.db_path)
        self.cliente_service = ClienteService(unit_db.db_path)

        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path

        # Créer un client de test
        self.cliente_id = self.cliente_service.create_cliente({
            'nombre': 'Cliente Test',
            'nif': '12345678A',
            'email': 'test@example.com',
            'direccion': 'Calle Test 123'
        })

        # Créer un produit de test
        self.producto_id = self.producto_service.create_producto({
            'nombre': 'Producto Test',
            'precio_venta': 10.50,
            'iva_recomendado': 21.0,
            'stock': 100
        })

        yield
        # Le nettoyage est géré par la fixture unit_db
    
    def test_create_factura_success(self):
        """Test création d'une facture avec succès"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.50,
            'iva_total': 2.21,
            'total': 12.71,
            'estado': 'Borrador',
            'lineas': [
                {
                    'producto_id': self.producto_id,
                    'cantidad': 1,
                    'precio_unitario': 10.50,
                    'iva': 21.0
                }
            ]
        }
        
        factura_id = self.service.create_factura(factura_data)
        assert factura_id is not None
        assert factura_id > 0
    
    def test_create_factura_missing_numero(self):
        """Test création d'une facture sans numéro"""
        factura_data = {
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'}
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_missing_fecha(self):
        """Test création d'une facture sans date"""
        factura_data = {
            'numero': 'FAC-0001',
            'cliente': {'nombre': 'Cliente Test'}
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_cliente(self):
        """Test création d'une facture avec client invalide"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {}  # Sans nom
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_negative_total(self):
        """Test création d'une facture avec total négatif"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'total': -10.50
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_linea_missing_producto(self):
        """Test création avec ligne sans producto_id"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'lineas': [
                {
                    'cantidad': 1,
                    'precio_unitario': 10.50
                }
            ]
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_linea_zero_cantidad(self):
        """Test création avec ligne à quantité zéro"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'lineas': [
                {
                    'producto_id': self.producto_id,
                    'cantidad': 0,  # Invalide
                    'precio_unitario': 10.50
                }
            ]
        }
        
        with pytest.raises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_calculate_totals_empty(self):
        """Test calcul des totaux avec liste vide"""
        totals = self.service.calculate_totals([])
        assert totals['subtotal'] == 0.0
        assert totals['iva_total'] == 0.0
        assert totals['total'] == 0.0
    
    def test_calculate_totals_success(self):
        """Test calcul des totaux avec succès"""
        lineas = [
            {
                'cantidad': 2,
                'precio_unitario': 10.0,
                'iva': 21.0
            },
            {
                'cantidad': 1,
                'precio_unitario': 5.0,
                'iva': 10.0
            }
        ]
        
        totals = self.service.calculate_totals(lineas)
        assert totals['subtotal'] == 25.0  # 20 + 5
        assert totals['iva_total'] == 4.7  # 4.2 + 0.5
        assert totals['total'] == 29.7  # 25 + 4.7

    def test_generate_factura_number_first(self, monkeypatch):
        """Test génération du premier numéro de facture avec le nouveau format"""
        # Patcher la config pour avoir un comportement prévisible
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: 1)
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: '')
        
        numero = self.service.generate_factura_number()
        # Nouveau format: 001-2026 (année courante)
        current_year = datetime.now().year
        assert numero == f'001-{current_year}'

    def test_generate_factura_number_increment(self, monkeypatch):
        """Test incrémentation du numéro de facture avec le nouveau format"""
        # Patcher la config
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: 1)
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: '')
        
        current_year = datetime.now().year
        
        # Créer une facture
        self.service.create_factura({
            'numero': f'001-{current_year}',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Générer le prochain numéro
        numero = self.service.generate_factura_number()
        assert numero == f'002-{current_year}'

    def test_get_all_facturas(self):
        """Test récupération de toutes les factures"""
        # Créer quelques factures
        for i in range(3):
            self.service.create_factura({
                'numero': f'FAC-000{i+1}',
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'cliente': {
                    'id': self.cliente_id,
                    'nombre': 'Cliente Test',
                    'nif': '12345678A',
                    'direccion': 'Calle Test 123'
                },
                'subtotal': 10.0,
                'iva_total': 2.1,
                'total': 12.1,
                'lineas': []
            })

        facturas = self.service.get_all_facturas()
        assert isinstance(facturas, list)
        assert len(facturas) >= 3

    def test_get_factura_by_id_success(self):
        """Test récupération d'une facture par ID"""
        # Créer une facture
        factura_id = self.service.create_factura({
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Récupérer la facture
        factura = self.service.get_factura_by_id(factura_id)
        assert factura is not None
        assert factura['numero'] == 'FAC-0001'

    def test_get_factura_by_id_not_found(self):
        """Test récupération d'une facture inexistante"""
        with pytest.raises(InvoiceNotFoundError):
            self.service.get_factura_by_id(99999)

    def test_delete_factura_success(self):
        """Test suppression d'une facture"""
        # Créer une facture
        factura_id = self.service.create_factura({
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Supprimer
        success = self.service.delete_factura(factura_id)
        assert success

        # Vérifier la suppression
        with pytest.raises(InvoiceNotFoundError):
            self.service.get_factura_by_id(factura_id)

    def test_update_factura_without_id(self):
        """Test update_factura sans ID - doit lever InvoiceValidationError"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'lineas': []
        }

        with pytest.raises(InvoiceValidationError) as context:
            self.service.update_factura(factura_data)

        assert "ID de factura requerido" in str(context.value)

    def test_update_factura_not_found(self):
        """Test update_factura avec ID inexistant - doit lever InvoiceNotFoundError"""
        factura_data = {
            'id': 99999,
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 0.0,
            'iva_total': 0.0,
            'total': 0.0,
            'lineas': []
        }

        with pytest.raises(InvoiceNotFoundError):
            self.service.update_factura(factura_data)

    def test_calculate_totals_empty_lineas(self):
        """Test calculate_totals avec liste vide"""
        result = self.service.calculate_totals([])

        assert result['subtotal'] == 0.0
        assert result['iva_total'] == 0.0
        assert result['total'] == 0.0

    def test_calculate_totals_invalid_data(self):
        """Test calculate_totals avec données invalides"""
        lineas = [
            {'cantidad': 'invalid', 'precio_unitario': 10.0, 'iva': 21.0}
        ]

        with pytest.raises(InvoiceValidationError) as context:
            self.service.calculate_totals(lineas)

        assert "Error calculando totales" in str(context.value)

    def test_generate_factura_number_with_existing(self, monkeypatch):
        """Test generate_factura_number avec factures existantes"""
        # Patcher la config
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: 1)
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: '')
        
        current_year = datetime.now().year
        
        # Créer une facture
        factura_data = {
            'numero': f'005-{current_year}',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': [{
                'producto_id': self.producto_id,
                'cantidad': 1,
                'precio_unitario': 10.0,
                'iva': 21.0
            }]
        }
        self.service.create_factura(factura_data)

        # Générer le prochain numéro
        next_number = self.service.generate_factura_number()
        assert next_number == f'006-{current_year}'

    def test_generate_factura_number_no_existing(self, monkeypatch):
        """Test generate_factura_number sans factures existantes"""
        # Patcher la config
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: 1)
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: '')
        
        # Créer un nouveau service avec une DB vide
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()

        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)

        try:
            from database.database import Database
            Database(temp_db.name)  # Initialiser la DB
            service = FacturaService(temp_db.name)
            current_year = datetime.now().year
            number = service.generate_factura_number()
            assert number == f'001-{current_year}'
        finally:
            # Restaurer TEST_DATABASE_PATH
            if old_test_db_path:
                os.environ['TEST_DATABASE_PATH'] = old_test_db_path
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)

    def test_validate_linea_precio_negativo(self):
        """Test validation d'une ligne avec prix négatif"""
        linea = {
            'producto_id': self.producto_id,
            'cantidad': 1,
            'precio_unitario': -10.0,
            'iva': 21.0
        }

        with pytest.raises(InvoiceValidationError) as context:
            self.service._validate_linea(linea, 0)

        assert "precio_unitario no puede ser negativo" in str(context.value)

    def test_validate_linea_precio_invalido(self):
        """Test validation d'une ligne avec prix invalide"""
        linea = {
            'producto_id': self.producto_id,
            'cantidad': 1,
            'precio_unitario': 'invalid',
            'iva': 21.0
        }

        with pytest.raises(InvoiceValidationError) as context:
            self.service._validate_linea(linea, 0)

        assert "precio_unitario inválido" in str(context.value)

    def test_validate_stock_producto_not_found(self):
        """Test validation stock avec produit inexistant"""
        lineas = [{
            'producto_id': 99999,
            'cantidad': 1,
            'precio_unitario': 10.0,
            'iva': 21.0
        }]

        with pytest.raises(InvoiceValidationError) as context:
            self.service._validate_stock_availability(lineas)

        assert "Producto 99999 no encontrado" in str(context.value)

    def test_validate_stock_insufficient(self):
        """Test validation stock insuffisant - maintenant autorisé avec warning"""
        # NOTE: Les stocks négatifs sont maintenant permis
        # Le produit a un stock de 100
        lineas = [{
            'producto_id': self.producto_id,
            'cantidad': 200,  # Plus que le stock disponible
            'precio_unitario': 10.0,
            'iva': 21.0
        }]

        # Ne devrait plus lever d'exception - juste un warning dans les logs
        self.service._validate_stock_availability(lineas)
        # Si on arrive ici, c'est que la validation a passé (stock négatif permis)


if __name__ == '__main__':
    unittest.main()

