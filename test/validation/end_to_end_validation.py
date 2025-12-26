#!/usr/bin/env python3
"""
Validation End-to-End de l'application Facturacion Facil
Teste le workflow complet: Produit → Client → Facture
"""

import tempfile
import os
import logging
from datetime import datetime

# Désactiver le logging pour la validation
logging.disable(logging.CRITICAL)

from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.organizacion_service import OrganizacionService
from services.factura_service import FacturaService
from utils.exceptions import (
    ProductValidationError,
    ClientValidationError,
    InvoiceValidationError,
    InsufficientStockError,
    DatabaseError
)


class EndToEndValidator:
    """Validateur end-to-end de l'application"""
    
    def __init__(self):
        # Créer une DB temporaire
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Initialiser les services
        self.producto_service = ProductoService(self.db_path)
        self.cliente_service = ClienteService(self.db_path)
        self.organizacion_service = OrganizacionService(self.db_path)
        self.factura_service = FacturaService(self.db_path)
        
        self.tests_passed = 0
        self.tests_failed = 0
    
    def cleanup(self):
        """Nettoyer la DB temporaire"""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def assert_true(self, condition, message):
        """Assertion personnalisée"""
        if condition:
            self.tests_passed += 1
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            print(f"  ❌ {message}")
    
    def test_1_organizacion(self):
        """Test 1: Créer et lire l'organisation"""
        print("\n1. Test Organisation")
        print("-" * 60)
        
        # Créer l'organisation
        org_id = self.organizacion_service.create_organizacion({
            'nombre': 'Mi Empresa SL',
            'cif': 'A12345678',
            'email': 'info@miempresa.com',
            'numero_factura_inicial': 1
        })
        self.assert_true(org_id is not None, "Organisation créée")
        
        # Lire l'organisation
        org = self.organizacion_service.get_organizacion()
        self.assert_true(org is not None, "Organisation lue")
        self.assert_true(org['nombre'] == 'Mi Empresa SL', "Nom correct")
        self.assert_true(org['cif'] == 'A12345678', "CIF correct")
    
    def test_2_productos(self):
        """Test 2: CRUD Produits"""
        print("\n2. Test Produits")
        print("-" * 60)
        
        # Créer un produit
        producto_id = self.producto_service.create_producto({
            'nombre': 'Camiseta Roja',
            'precio_venta': 19.99,
            'iva_recomendado': 21.0,
            'stock': 100
        })
        self.assert_true(producto_id is not None, "Produit créé")
        
        # Lire le produit
        producto = self.producto_service.get_producto_by_id(producto_id)
        self.assert_true(producto is not None, "Produit lu")
        self.assert_true(producto['nombre'] == 'Camiseta Roja', "Nom correct")
        self.assert_true(producto['stock_actual'] == 100, "Stock correct")
        
        # Mettre à jour le produit (en préservant le stock)
        success = self.producto_service.update_producto({
            'id': producto_id,
            'nombre': 'Camiseta Roja XL',
            'precio_venta': 24.99,
            'referencia': 'CAM-ROJA-XL',
            'stock': 100  # Préserver le stock
        })
        self.assert_true(success, "Produit mis à jour")

        # Vérifier la mise à jour
        producto = self.producto_service.get_producto_by_id(producto_id)
        self.assert_true(producto['nombre'] == 'Camiseta Roja XL', "Nom mis à jour")
        self.assert_true(producto['precio_venta'] == 24.99, "Prix mis à jour")
        self.assert_true(producto['stock_actual'] == 100, "Stock préservé")
        
        return producto_id
    
    def test_3_clientes(self):
        """Test 3: CRUD Clients"""
        print("\n3. Test Clients")
        print("-" * 60)
        
        # Créer un client
        cliente_id = self.cliente_service.create_cliente({
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'nif': '12345678A',
            'direccion': 'Calle Mayor 123',
            'telefono': '666777888'
        })
        self.assert_true(cliente_id is not None, "Client créé")
        
        # Lire le client
        cliente = self.cliente_service.get_cliente_by_id(cliente_id)
        self.assert_true(cliente is not None, "Client lu")
        self.assert_true(cliente['nombre'] == 'Juan Pérez', "Nom correct")
        self.assert_true(cliente['email'] == 'juan@example.com', "Email correct")
        
        # Mettre à jour le client
        success = self.cliente_service.update_cliente({
            'id': cliente_id,
            'nombre': 'Juan Pérez García',
            'telefono': '666777999'
        })
        self.assert_true(success, "Client mis à jour")
        
        # Vérifier la mise à jour
        cliente = self.cliente_service.get_cliente_by_id(cliente_id)
        self.assert_true(cliente['nombre'] == 'Juan Pérez García', "Nom mis à jour")
        
        return cliente_id
    
    def test_4_facturas(self, producto_id, cliente_id):
        """Test 4: CRUD Factures"""
        print("\n4. Test Factures")
        print("-" * 60)
        
        # Récupérer les données du client
        cliente = self.cliente_service.get_cliente_by_id(cliente_id)
        
        # Créer une facture
        factura_data = {
            'numero': self.factura_service.generate_factura_number(),
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': cliente['id'],
                'nombre': cliente['nombre'],
                'nif': cliente['nif'],
                'direccion': cliente['direccion']
            },
            'lineas': [{
                'producto_id': producto_id,
                'cantidad': 2,
                'precio_unitario': 24.99,
                'iva': 21.0
            }]
        }
        
        # Calculer les totaux
        totales = self.factura_service.calculate_totals(factura_data['lineas'])
        factura_data.update(totales)
        
        self.assert_true(totales['subtotal'] == 49.98, "Subtotal correct")
        self.assert_true(totales['iva_total'] == 10.50, "IVA correct")
        self.assert_true(totales['total'] == 60.48, "Total correct")
        
        # Créer la facture
        factura_id = self.factura_service.create_factura(factura_data)
        self.assert_true(factura_id is not None, "Facture créée")
        
        # Lire la facture
        factura = self.factura_service.get_factura_by_id(factura_id)
        self.assert_true(factura is not None, "Facture lue")
        self.assert_true(len(factura['lineas']) == 1, "Ligne de facture présente")
        
        # Vérifier le stock
        producto = self.producto_service.get_producto_by_id(producto_id)
        self.assert_true(producto['stock_actual'] == 98, "Stock mis à jour (100 - 2)")
        
        return factura_id
    
    def test_5_validation(self, producto_id):
        """Test 5: Validation des erreurs"""
        print("\n5. Test Validation")
        print("-" * 60)
        
        # Test stock insuffisant
        try:
            self.factura_service._validate_stock_availability([{
                'producto_id': producto_id,
                'cantidad': 200  # Plus que le stock disponible (98)
            }])
            self.assert_true(False, "Stock insuffisant détecté")
        except InsufficientStockError:
            self.assert_true(True, "Stock insuffisant détecté")
        
        # Test prix négatif
        try:
            self.producto_service.create_producto({
                'nombre': 'Test',
                'precio_venta': -10
            })
            self.assert_true(False, "Prix négatif détecté")
        except ProductValidationError:
            self.assert_true(True, "Prix négatif détecté")
        
        # Test email invalide
        try:
            self.cliente_service.create_cliente({
                'nombre': 'Test',
                'email': 'invalid-email'
            })
            self.assert_true(False, "Email invalide détecté")
        except ClientValidationError:
            self.assert_true(True, "Email invalide détecté")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("=" * 60)
        print("VALIDATION END-TO-END - FACTURACION FACIL")
        print("=" * 60)
        
        try:
            self.test_1_organizacion()
            producto_id = self.test_2_productos()
            cliente_id = self.test_3_clientes()
            factura_id = self.test_4_facturas(producto_id, cliente_id)
            self.test_5_validation(producto_id)
            
            print("\n" + "=" * 60)
            print("RÉSULTATS")
            print("=" * 60)
            print(f"✅ Tests réussis: {self.tests_passed}")
            print(f"❌ Tests échoués: {self.tests_failed}")
            print(f"📊 Total: {self.tests_passed + self.tests_failed}")
            
            if self.tests_failed == 0:
                print("\n🎊 VALIDATION COMPLÈTE RÉUSSIE ! 🎊")
                return True
            else:
                print("\n⚠️  VALIDATION ÉCHOUÉE")
                return False
                
        finally:
            self.cleanup()


if __name__ == '__main__':
    validator = EndToEndValidator()
    success = validator.run_all_tests()
    exit(0 if success else 1)

