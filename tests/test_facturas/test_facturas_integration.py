# -*- coding: utf-8 -*-
"""
Tests de integración para el módulo de facturas
"""
import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from database.models import Factura, FacturaItem, Producto, Stock
from database.database import Database
from common.validators import FormValidator, CalculationHelper

class TestFacturasIntegration:
    """Tests de integración para facturas"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para tests"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        temp_db = Database(temp_file.name)
        
        yield temp_db
        
        os.unlink(temp_file.name)
    
    @pytest.fixture
    def sample_productos(self, temp_db):
        """Crea productos de ejemplo"""
        # Usar la base de datos temporal
        original_db = Producto.__dict__.get('db')
        Producto.db = temp_db
        
        productos = []
        for i in range(3):
            producto = Producto(
                nombre=f"Producto {i+1}",
                referencia=f"PROD-{i+1:03d}",
                precio=10.0 * (i+1),
                categoria="Test",
                iva_recomendado=21.0,
                descripcion=f"Descripción del producto {i+1}"
            )
            producto.save()
            productos.append(producto)
        
        yield productos
        
        if original_db:
            Producto.db = original_db
    
    @pytest.fixture
    def sample_stock(self, temp_db, sample_productos):
        """Crea stock de ejemplo"""
        original_db = Stock.__dict__.get('db')
        Stock.db = temp_db
        
        stocks = []
        for producto in sample_productos:
            stock = Stock(
                producto_id=producto.id,
                cantidad_disponible=100
            )
            stock.save()
            stocks.append(stock)
        
        yield stocks
        
        if original_db:
            Stock.db = original_db
    
    def test_complete_factura_workflow(self, temp_db, sample_productos, sample_stock):
        """Test flujo completo de creación de factura"""
        # Configurar base de datos temporal
        original_db_factura = Factura.__dict__.get('db')
        original_db_item = FacturaItem.__dict__.get('db')
        Factura.db = temp_db
        FacturaItem.db = temp_db
        
        try:
            # 1. Crear nueva factura
            factura = Factura(
                numero_factura="2025-0001",
                fecha_factura="2025-01-15",
                nombre_cliente="Cliente Integración",
                dni_nie_cliente="12345678A",
                direccion_cliente="Calle Test 123\n28001 Madrid",
                email_cliente="cliente@test.com",
                telefono_cliente="+34 123 456 789",
                modo_pago="tarjeta"
            )
            
            # 2. Agregar productos a la factura
            # Producto 1: 2 unidades a 10€ con 21% IVA
            item1 = FacturaItem(
                producto_id=sample_productos[0].id,
                cantidad=2,
                precio_unitario=10.0,
                iva_aplicado=21.0,
                descuento=0.0
            )
            item1.calculate_totals()
            
            # Producto 2: 1 unidad a 20€ con 10% descuento y 21% IVA
            item2 = FacturaItem(
                producto_id=sample_productos[1].id,
                cantidad=1,
                precio_unitario=20.0,
                iva_aplicado=21.0,
                descuento=10.0
            )
            item2.calculate_totals()
            
            # Producto 3: 3 unidades a 30€ con 21% IVA
            item3 = FacturaItem(
                producto_id=sample_productos[2].id,
                cantidad=3,
                precio_unitario=30.0,
                iva_aplicado=21.0,
                descuento=0.0
            )
            item3.calculate_totals()
            
            factura.items = [item1, item2, item3]
            
            # 3. Calcular totales
            factura.calculate_totals()
            
            # Verificar cálculos
            # Item1: 2 * 10 = 20€ subtotal, 4.2€ IVA, 24.2€ total
            # Item2: 1 * 20 = 20€, -10% = 18€ subtotal, 3.78€ IVA, 21.78€ total
            # Item3: 3 * 30 = 90€ subtotal, 18.9€ IVA, 108.9€ total
            expected_subtotal = 20.0 + 18.0 + 90.0  # 128€
            expected_iva = 4.2 + 3.78 + 18.9  # 26.88€
            expected_total = 24.2 + 21.78 + 108.9  # 154.88€
            
            assert abs(factura.subtotal - expected_subtotal) < 0.01
            assert abs(factura.total_iva - expected_iva) < 0.01
            assert abs(factura.total_factura - expected_total) < 0.01
            
            # 4. Guardar factura
            factura.save()
            assert factura.id is not None
            
            # 5. Verificar que se guardó correctamente
            retrieved_factura = Factura.get_by_id(factura.id)
            assert retrieved_factura is not None
            assert retrieved_factura.numero_factura == "2025-0001"
            assert retrieved_factura.nombre_cliente == "Cliente Integración"
            assert len(retrieved_factura.items) == 3
            
            # 6. Verificar items guardados
            for i, item in enumerate(retrieved_factura.items):
                assert item.producto_id == sample_productos[i].id
                assert item.factura_id == factura.id
                
            # 7. Verificar que aparece en la lista de facturas
            all_facturas = Factura.get_all()
            assert len(all_facturas) == 1
            assert all_facturas[0].id == factura.id
            
        finally:
            if original_db_factura:
                Factura.db = original_db_factura
            if original_db_item:
                FacturaItem.db = original_db_item
    
    def test_factura_validation_workflow(self):
        """Test flujo de validación de facturas"""
        # Test datos válidos
        valid_data = {
            'numero_factura': '2025-0001',
            'fecha_factura': '2025-01-15',
            'nombre_cliente': 'Cliente Test',
            'dni_nie_cliente': '12345678A',
            'email_cliente': 'test@example.com',
            'telefono_cliente': '+34 123 456 789'
        }
        
        errors = []
        
        # Validar cada campo
        for field, value in valid_data.items():
            if field in ['numero_factura', 'fecha_factura', 'nombre_cliente']:
                error = FormValidator.validate_required_field(value, field)
                if error:
                    errors.append(error)
            elif field == 'dni_nie_cliente':
                error = FormValidator.validate_dni_nie(value)
                if error:
                    errors.append(error)
            elif field == 'email_cliente':
                error = FormValidator.validate_email(value)
                if error:
                    errors.append(error)
            elif field == 'telefono_cliente':
                error = FormValidator.validate_phone(value)
                if error:
                    errors.append(error)
        
        assert len(errors) == 0, f"Errores de validación: {errors}"
        
        # Test datos inválidos
        invalid_data = {
            'numero_factura': '',  # Requerido
            'fecha_factura': '',   # Requerido
            'nombre_cliente': '',  # Requerido
            'dni_nie_cliente': '123',  # Formato inválido
            'email_cliente': 'invalid-email',  # Formato inválido
            'telefono_cliente': 'abc123'  # Formato inválido
        }
        
        errors = []
        
        for field, value in invalid_data.items():
            if field in ['numero_factura', 'fecha_factura', 'nombre_cliente']:
                error = FormValidator.validate_required_field(value, field)
                if error:
                    errors.append(error)
            elif field == 'dni_nie_cliente':
                error = FormValidator.validate_dni_nie(value)
                if error:
                    errors.append(error)
            elif field == 'email_cliente':
                error = FormValidator.validate_email(value)
                if error:
                    errors.append(error)
            elif field == 'telefono_cliente':
                error = FormValidator.validate_phone(value)
                if error:
                    errors.append(error)
        
        assert len(errors) == 6, f"Debería haber 6 errores, encontrados: {len(errors)}"
    
    def test_stock_update_after_factura(self, temp_db, sample_productos, sample_stock):
        """Test actualización de stock después de crear factura"""
        original_db_stock = Stock.__dict__.get('db')
        original_db_factura = Factura.__dict__.get('db')
        original_db_item = FacturaItem.__dict__.get('db')

        Stock.db = temp_db
        Factura.db = temp_db
        FacturaItem.db = temp_db

        try:
            # Verificar stock inicial (get_by_product devuelve solo la cantidad)
            initial_stock_cantidad = Stock.get_by_product(sample_productos[0].id)
            assert initial_stock_cantidad == 100

            # Crear factura con productos
            factura = Factura(
                numero_factura="2025-STOCK",
                fecha_factura="2025-01-15",
                nombre_cliente="Cliente Stock",
                subtotal=0,
                total_iva=0,
                total_factura=0
            )

            # Agregar item que consume stock
            item = FacturaItem(
                producto_id=sample_productos[0].id,
                cantidad=5,  # Consumir 5 unidades
                precio_unitario=10.0,
                iva_aplicado=21.0,
                descuento=0.0
            )
            item.calculate_totals()

            factura.items = [item]
            factura.calculate_totals()
            factura.save()

            # Simular actualización de stock usando el método update_stock
            Stock.update_stock(sample_productos[0].id, item.cantidad)

            # Verificar que el stock se actualizó
            updated_stock_cantidad = Stock.get_by_product(sample_productos[0].id)
            assert updated_stock_cantidad == 95  # 100 - 5

        finally:
            if original_db_stock:
                Stock.db = original_db_stock
            if original_db_factura:
                Factura.db = original_db_factura
            if original_db_item:
                FacturaItem.db = original_db_item
    
    def test_factura_number_generation(self, temp_db):
        """Test generación automática de números de factura"""
        original_db = Factura.__dict__.get('db')
        Factura.db = temp_db
        
        try:
            # Primera factura
            numero1 = Factura.get_next_numero()
            current_year = datetime.now().year
            assert numero1 == f"1-{current_year}"

            # Crear la factura
            factura1 = Factura(
                numero_factura=numero1,
                fecha_factura="2025-01-01",
                nombre_cliente="Cliente 1",
                subtotal=100,
                total_iva=21,
                total_factura=121
            )
            factura1.save()

            # Segunda factura debería incrementar
            numero2 = Factura.get_next_numero()
            assert numero2 == f"2-{current_year}"

            # Crear segunda factura
            factura2 = Factura(
                numero_factura=numero2,
                fecha_factura="2025-01-02",
                nombre_cliente="Cliente 2",
                subtotal=200,
                total_iva=42,
                total_factura=242
            )
            factura2.save()

            # Tercera factura
            numero3 = Factura.get_next_numero()
            assert numero3 == f"3-{current_year}"
            
        finally:
            if original_db:
                Factura.db = original_db
    
    def test_complex_calculation_scenarios(self):
        """Test escenarios complejos de cálculo"""
        # Escenario 1: Múltiples productos con diferentes IVAs y descuentos
        scenarios = [
            # (precio_unitario, cantidad, iva, descuento, expected_total)
            (100.0, 1, 21.0, 0.0, 121.0),      # Básico: 100 * 1.21 = 121
            (100.0, 2, 21.0, 10.0, 217.8),    # Con descuento: (200 * 0.9) * 1.21 = 217.8
            (50.0, 3, 10.0, 5.0, 156.75),     # IVA reducido: (150 * 0.95) * 1.10 = 156.75
            (25.0, 4, 4.0, 20.0, 83.2),       # IVA superreducido: (100 * 0.8) * 1.04 = 83.2
        ]

        for precio, cantidad, iva, descuento, expected in scenarios:
            result = CalculationHelper.calculate_line_total(precio, cantidad, iva, descuento)
            assert abs(result['total'] - expected) < 0.01, \
                f"Error en cálculo: {precio}x{cantidad} con {iva}% IVA y {descuento}% desc. " \
                f"Esperado: {expected}, Obtenido: {result['total']}"
    
    def test_factura_crud_operations(self, temp_db, sample_productos):
        """Test operaciones CRUD completas en facturas"""
        original_db_factura = Factura.__dict__.get('db')
        original_db_item = FacturaItem.__dict__.get('db')
        Factura.db = temp_db
        FacturaItem.db = temp_db
        
        try:
            # CREATE
            factura = Factura(
                numero_factura="CRUD-2025",
                fecha_factura="2025-01-15",
                nombre_cliente="Cliente CRUD",
                subtotal=100,
                total_iva=21,
                total_factura=121,
                modo_pago="efectivo"
            )
            factura.save()
            assert factura.id is not None

            # READ
            retrieved = Factura.get_by_id(factura.id)
            assert retrieved is not None
            assert retrieved.numero_factura == "CRUD-2025"
            assert retrieved.modo_pago == "efectivo"
            
            # UPDATE
            retrieved.nombre_cliente = "Cliente CRUD Modificado"
            retrieved.modo_pago = "tarjeta"
            retrieved.save()
            
            updated = Factura.get_by_id(factura.id)
            assert updated.nombre_cliente == "Cliente CRUD Modificado"
            assert updated.modo_pago == "tarjeta"
            
            # DELETE
            updated.delete()
            deleted = Factura.get_by_id(factura.id)
            assert deleted is None
            
        finally:
            if original_db_factura:
                Factura.db = original_db_factura
            if original_db_item:
                FacturaItem.db = original_db_item
