# -*- coding: utf-8 -*-
"""
Factory pour générer des données de test pour les tests de comportement
"""

from datetime import datetime, timedelta
import random
from typing import Dict, List

class TestDataFactory:
    """Factory pour créer des données de test cohérentes"""
    
    @staticmethod
    def create_test_client(index=1) -> Dict:
        """Créer un client de test"""
        return {
            'nombre': f'Cliente Test {index}',
            'nif': f'12345678{index:02d}',
            'email': f'cliente{index}@test.com',
            'telefono': f'+34 91{index:02d}123456',
            'direccion': f'Calle Test {index}, 28001 Madrid'
        }
    
    @staticmethod
    def create_test_product(index=1) -> Dict:
        """Créer un produit de test"""
        return {
            'nombre': f'Producto Test {index}',
            'referencia': f'REF{index:03d}',
            'precio_venta': round(10.0 + (index * 5.5), 2),
            'iva': 21.0,
            'categoria': 'Categoria Test',
            'descripcion': f'Descripción del producto de test número {index}',
            'stock': 10 + index
        }
    
    @staticmethod
    def create_test_organization() -> Dict:
        """Créer des données d'organisation de test"""
        return {
            'nombre_empresa': 'Empresa Test S.L.',
            'cif': 'B12345678',
            'telefono': '+34 911234567',
            'email': 'info@empresatest.com',
            'direccion': 'Calle Mayor, 1\n28001 Madrid',
            'logo_path': '',
            'logo_orientation': 'horizontal',
            'numero_inicial_factura': 1,
            'directorio_imagenes': 'imagenes/',
            'directorio_logos': 'logos/',
            'directorio_pdfs': 'pdfs/'
        }
    
    @staticmethod
    def create_test_invoice_status(index=1) -> Dict:
        """Créer un état de facture de test"""
        statuses = [
            {'nombre': 'Borrador', 'color': '#FFA500', 'permite_modificacion': True},
            {'nombre': 'Enviada', 'color': '#0066CC', 'permite_modificacion': False},
            {'nombre': 'Pagada', 'color': '#00AA00', 'permite_modificacion': False},
            {'nombre': 'Cancelada', 'color': '#CC0000', 'permite_modificacion': False}
        ]
        
        if index <= len(statuses):
            status = statuses[index - 1].copy()
        else:
            status = {
                'nombre': f'Estado Test {index}',
                'color': f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}',
                'permite_modificacion': random.choice([True, False])
            }
        
        status.update({
            'descripcion': f'Descripción del estado {status["nombre"]}',
            'orden': index
        })
        
        return status
    
    @staticmethod
    def create_test_invoice(client_id=1, products_data=None) -> Dict:
        """Créer une facture de test (alias pour create_test_factura)"""
        return TestDataFactory.create_test_factura(client_id, products_data)

    @staticmethod
    def create_test_factura(client_id=1, products_data=None) -> Dict:
        """Créer une facture de test"""
        if products_data is None:
            products_data = [
                {'producto_id': 1, 'cantidad': 2, 'precio_unitario': 15.50, 'iva': 21.0, 'descuento': 0.0},
                {'producto_id': 2, 'cantidad': 1, 'precio_unitario': 25.00, 'iva': 21.0, 'descuento': 5.0}
            ]
        
        subtotal = sum(p['cantidad'] * p['precio_unitario'] * (1 - p['descuento']/100) for p in products_data)
        total_iva = sum(p['cantidad'] * p['precio_unitario'] * (1 - p['descuento']/100) * p['iva']/100 for p in products_data)
        total_descuentos = sum(p['cantidad'] * p['precio_unitario'] * p['descuento']/100 for p in products_data)

        return {
            'numero_factura': f'FACT-TEST-{datetime.now().strftime("%Y%m%d")}-001',
            'numero': f'FACT-TEST-{datetime.now().strftime("%Y%m%d")}-001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente_id': client_id,
            'estado': 'Borrador',
            'productos': products_data,
            'subtotal': subtotal,
            'iva': total_iva,
            'iva_total': total_iva,
            'total': subtotal + total_iva,
            'total_descuentos': total_descuentos
        }
    
    @staticmethod
    def create_multiple_clients(count=5) -> List[Dict]:
        """Créer plusieurs clients de test"""
        return [TestDataFactory.create_test_client(i) for i in range(1, count + 1)]
    
    @staticmethod
    def create_multiple_products(count=5) -> List[Dict]:
        """Créer plusieurs produits de test"""
        return [TestDataFactory.create_test_product(i) for i in range(1, count + 1)]
    
    @staticmethod
    def create_search_test_data() -> Dict:
        """Créer des données pour tester la recherche avancée"""
        return {
            'search_text': 'Test',
            'date_from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'date_to': datetime.now().strftime('%Y-%m-%d'),
            'amount_min': 10.0,
            'amount_max': 1000.0,
            'client_filter': 'Cliente Test 1',
            'status_filter': 'Borrador'
        }
    
    @staticmethod
    def create_stock_adjustment_data() -> List[Dict]:
        """Créer des données pour tester les ajustements de stock"""
        return [
            {'producto_id': 1, 'nuevo_stock': 25, 'stock_minimo': 5},
            {'producto_id': 2, 'nuevo_stock': 15, 'stock_minimo': 3},
            {'producto_id': 3, 'nuevo_stock': 0, 'stock_minimo': 2}  # Stock bas
        ]

    @staticmethod
    def create_product_data(index=1) -> Dict:
        """Créer des données de produit (alias de create_test_product)"""
        return TestDataFactory.create_test_product(index)

    @staticmethod
    def create_client_data(index=1) -> Dict:
        """Créer des données de client (alias de create_test_client)"""
        return TestDataFactory.create_test_client(index)
