# -*- coding: utf-8 -*-
"""
Tests de comportement pour le système de stock négatif
Vérifie que les stocks négatifs sont permis et fonctionnent correctement
"""

import pytest
import sys
import os
import uuid

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger


class TestStockNegativoBehaviour(BaseBehaviourTest):
    """Tests de comportement pour le système de stock négatif"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox, mock_filedialog):
        """Configuration automatique pour chaque test"""
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir
        self.logger = get_logger(self.__class__.__name__)

        # Générer un identifiant unique pour ce test
        self.test_id = str(uuid.uuid4())[:8]

        # Initialiser les données de test
        self.test_data = TestDataFactory()

        # Préparer des données de test
        self.setup_stock_negativo_test_data()
    
    def setup_stock_negativo_test_data(self):
        """Préparer des données de test pour les stocks négatifs"""
        # Créer un produit avec peu de stock
        test_products = [
            {
                'nombre': 'Producto Stock Bajo',
                'referencia': f'STOCKBAJO-{self.test_id}',
                'precio_venta': 50.00,
                'stock': 2,  # Stock très faible
                'sin_stock': False,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto Stock Cero',
                'referencia': f'STOCKCERO-{self.test_id}',
                'precio_venta': 75.00,
                'stock': 0,  # Stock à zéro
                'sin_stock': False,
                'categoria': 'Test'
            }
        ]
        
        # Ajouter à la base de données de test
        self.product_ids = {}
        for product in test_products:
            product_id = self.database.add_product(product)
            self.product_ids[product['nombre']] = product_id
            self.logger.info(f"Produit créé: {product['nombre']} (ID: {product_id}, stock: {product['stock']})")
    
    def test_01_factura_con_stock_insuficiente(self):
        """Test: Créer une facture avec stock insuffisant - doit fonctionner"""
        self.logger.info("🧪 Test: Crear factura con stock insuficiente")
        
        # Récupérer le produit avec stock faible
        producto_id = self.product_ids.get('Producto Stock Bajo')
        assert producto_id is not None, "Produit de test non trouvé"
        
        producto = self.database.get_product_by_id(producto_id)
        stock_inicial = producto.get('stock_actual', 0)
        self.logger.info(f"Stock inicial: {stock_inicial}")
        
        # Créer une facture avec une quantité supérieure au stock
        factura_data = {
            'numero': f'TEST-NEG-{self.test_id}',
            'fecha': '2024-12-25',
            'cliente': {'nombre': 'Cliente Test', 'nif': '12345678A'},
            'lineas': [{
                'producto_id': producto_id,
                'producto_nombre': 'Producto Stock Bajo',
                'cantidad': 10,  # Plus que le stock disponible (2)
                'precio_unitario': 50.0,
                'iva': 21.0,
                'subtotal': 500.0,
                'iva_amount': 105.0,
                'total': 605.0
            }],
            'subtotal': 500.0,
            'iva_total': 105.0,
            'total': 605.0
        }
        
        # Créer la facture - ne devrait pas lever d'exception
        try:
            from services.factura_service import FacturaService
            service = FacturaService(self.database.db_path)
            factura_id = service.create_factura(factura_data)
            
            self.logger.info(f"✅ Factura creada con ID: {factura_id}")
            assert factura_id is not None, "La facture devrait être créée"
            
            # Vérifier que le stock est maintenant négatif
            producto_despues = self.database.get_product_by_id(producto_id)
            stock_final = producto_despues.get('stock_actual', 0)
            self.logger.info(f"Stock final: {stock_final}")
            
            assert stock_final < 0, f"Le stock devrait être négatif, mais est {stock_final}"
            assert stock_final == stock_inicial - 10, f"Stock devrait être {stock_inicial - 10}, mais est {stock_final}"
            
            self.logger.info("✅ Test factura con stock negativo PASSED")
            
        except Exception as e:
            self.logger.error(f"❌ Error creando factura: {e}")
            raise
    
    def test_02_producto_con_stock_cero_en_factura(self):
        """Test: Produits avec stock=0 peuvent être facturés"""
        self.logger.info("🧪 Test: Facturar producto con stock cero")
        
        # Récupérer le produit avec stock à zéro
        producto_id = self.product_ids.get('Producto Stock Cero')
        assert producto_id is not None, "Produit de test non trouvé"
        
        producto = self.database.get_product_by_id(producto_id)
        stock_inicial = producto.get('stock_actual', 0)
        self.logger.info(f"Stock inicial: {stock_inicial}")
        assert stock_inicial == 0, "Le stock initial devrait être 0"
        
        # Créer une facture avec ce produit
        factura_data = {
            'numero': f'TEST-CERO-{self.test_id}',
            'fecha': '2024-12-25',
            'cliente': {'nombre': 'Cliente Test', 'nif': '12345678A'},
            'lineas': [{
                'producto_id': producto_id,
                'producto_nombre': 'Producto Stock Cero',
                'cantidad': 5,
                'precio_unitario': 75.0,
                'iva': 21.0,
                'subtotal': 375.0,
                'iva_amount': 78.75,
                'total': 453.75
            }],
            'subtotal': 375.0,
            'iva_total': 78.75,
            'total': 453.75
        }
        
        # Créer la facture - ne devrait pas lever d'exception
        from services.factura_service import FacturaService
        service = FacturaService(self.database.db_path)
        factura_id = service.create_factura(factura_data)
        
        self.logger.info(f"✅ Factura creada con ID: {factura_id}")
        assert factura_id is not None, "La facture devrait être créée"
        
        # Vérifier que le stock est maintenant négatif
        producto_despues = self.database.get_product_by_id(producto_id)
        stock_final = producto_despues.get('stock_actual', 0)
        self.logger.info(f"Stock final: {stock_final}")
        
        assert stock_final == -5, f"Le stock devrait être -5, mais est {stock_final}"
        
        self.logger.info("✅ Test producto con stock cero PASSED")
    
    def test_03_producto_stock_negativo_en_autocompletado(self):
        """Test: Les produits avec stock négatif apparaissent dans l'autocomplétion"""
        self.logger.info("🧪 Test: Producto con stock negativo en autocompletado")
        
        # D'abord créer un produit avec stock négatif
        producto_id = self.product_ids.get('Producto Stock Bajo')
        self.database.update_product_stock(producto_id, -10)  # Forcer stock négatif
        
        # Vérifier que le produit a un stock négatif
        producto = self.database.get_product_by_id(producto_id)
        self.logger.info(f"Producto stock actual: {producto.get('stock_actual')}")
        assert producto.get('stock_actual', 0) < 0, "Le stock devrait être négatif"
        
        # Tester le widget d'autocomplétion directement (sans UI graphique)
        from ui.product_autocomplete_widget import ProductAutoCompleteWidget
        
        # Charger tous les produits dans le widget
        widget = ProductAutoCompleteWidget()
        all_products = self.database.get_all_products()
        widget.load_products(all_products)
        
        # Vérifier que le produit avec stock négatif est bien dans la liste
        producto_encontrado = False
        for p in widget.products_data:
            if p.get('id') == producto_id:
                producto_encontrado = True
                self.logger.info(f"✅ Produit trouvé dans autocomplétion: {p.get('nombre')} (stock: {p.get('stock_actual')})")
                break
        
        assert producto_encontrado, "Le produit avec stock négatif devrait apparaître dans l'autocomplétion"
        
        # Vérifier que has_valid_product accepte le stock négatif
        widget.set_product(producto)
        assert widget.has_valid_product(), "has_valid_product() devrait retourner True même avec stock négatif"
        
        self.logger.info("✅ Test autocompletado con stock negativo PASSED")
    
    def test_04_actualizar_stock_a_negativo(self):
        """Test: Mise à jour directe du stock à une valeur négative"""
        self.logger.info("🧪 Test: Actualizar stock a valor negativo")
        
        producto_id = self.product_ids.get('Producto Stock Bajo')
        
        # Mettre à jour le stock à une valeur négative
        from services.stock_service import StockService
        service = StockService(self.database.db_path)
        
        # Cette opération ne devrait plus lever d'exception
        success = service.update_stock(producto_id, -50)
        
        self.logger.info(f"Stock actualizado a -50: {success}")
        assert success, "La mise à jour du stock négatif devrait réussir"
        
        # Vérifier que le stock est bien négatif
        producto = self.database.get_product_by_id(producto_id)
        stock_actual = producto.get('stock_actual', 0)
        
        self.logger.info(f"Stock actual: {stock_actual}")
        assert stock_actual == -50, f"Le stock devrait être -50, mais est {stock_actual}"
        
        self.logger.info("✅ Test actualizar stock a negativo PASSED")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
