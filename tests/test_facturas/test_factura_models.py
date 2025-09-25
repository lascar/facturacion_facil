# -*- coding: utf-8 -*-
"""
Tests para los modelos de Factura y FacturaItem
"""
import pytest
import tempfile
import os
from datetime import datetime
from database.models import Factura, FacturaItem, Producto
from database.database import Database

class TestFacturaModel:
    """Tests para el modelo Factura"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para tests"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        # Crear instancia temporal de base de datos
        temp_db = Database(temp_file.name)
        
        yield temp_db
        
        # Limpiar
        os.unlink(temp_file.name)
    
    @pytest.fixture
    def sample_producto(self, temp_db):
        """Crea un producto de ejemplo"""
        producto = Producto(
            nombre="Producto Test",
            referencia="TEST-001",
            precio=10.0,
            categoria="Test",
            iva_recomendado=21.0
        )
        # Usar la base de datos temporal
        original_db = Producto.__dict__.get('db')
        Producto.db = temp_db
        producto.save()
        yield producto
        # Restaurar
        if original_db:
            Producto.db = original_db
    
    def test_factura_creation(self, temp_db):
        """Test creación básica de factura"""
        factura = Factura(
            numero_factura="001-2025",
            fecha_factura="2025-01-01",
            nombre_cliente="Cliente Test",
            subtotal=100.0,
            total_iva=21.0,
            total_factura=121.0,
            modo_pago="efectivo"
        )

        assert factura.numero_factura == "001-2025"
        assert factura.nombre_cliente == "Cliente Test"
        assert factura.subtotal == 100.0
        assert factura.total_iva == 21.0
        assert factura.total_factura == 121.0
        assert factura.modo_pago == "efectivo"
        assert factura.items == []
    
    def test_factura_save_and_retrieve(self, temp_db):
        """Test guardar y recuperar factura"""
        # Usar la base de datos temporal
        original_db = Factura.__dict__.get('db')
        Factura.db = temp_db
        
        try:
            factura = Factura(
                numero_factura="002-2025",
                fecha_factura="2025-01-02",
                nombre_cliente="Cliente Test 2",
                dni_nie_cliente="12345678A",
                direccion_cliente="Calle Test 123",
                email_cliente="test@example.com",
                telefono_cliente="123456789",
                subtotal=200.0,
                total_iva=42.0,
                total_factura=242.0,
                modo_pago="tarjeta"
            )

            factura.save()
            assert factura.id is not None

            # Recuperar factura
            retrieved = Factura.get_by_id(factura.id)
            assert retrieved is not None
            assert retrieved.numero_factura == "002-2025"
            assert retrieved.nombre_cliente == "Cliente Test 2"
            assert retrieved.dni_nie_cliente == "12345678A"
            assert retrieved.email_cliente == "test@example.com"
            assert retrieved.modo_pago == "tarjeta"
            
        finally:
            if original_db:
                Factura.db = original_db
    
    def test_factura_get_all(self, temp_db):
        """Test obtener todas las facturas"""
        original_db = Factura.__dict__.get('db')
        Factura.db = temp_db
        
        try:
            # Crear varias facturas
            for i in range(3):
                factura = Factura(
                    numero_factura=f"00{i+1}-2025",
                    fecha_factura=f"2025-01-0{i+1}",
                    nombre_cliente=f"Cliente {i+1}",
                    subtotal=100.0 * (i+1),
                    total_iva=21.0 * (i+1),
                    total_factura=121.0 * (i+1)
                )
                factura.save()

            # Obtener todas
            facturas = Factura.get_all()
            assert len(facturas) == 3

            # Verificar orden (más recientes primero)
            assert facturas[0].numero_factura == "003-2025"
            assert facturas[1].numero_factura == "002-2025"
            assert facturas[2].numero_factura == "001-2025"
            
        finally:
            if original_db:
                Factura.db = original_db
    
    def test_factura_delete(self, temp_db):
        """Test eliminar factura"""
        original_db = Factura.__dict__.get('db')
        Factura.db = temp_db
        
        try:
            factura = Factura(
                numero_factura="2025-DELETE",
                fecha_factura="2025-01-01",
                nombre_cliente="Cliente Delete",
                subtotal=100.0,
                total_iva=21.0,
                total_factura=121.0
            )
            factura.save()
            factura_id = factura.id
            
            # Verificar que existe
            retrieved = Factura.get_by_id(factura_id)
            assert retrieved is not None
            
            # Eliminar
            factura.delete()
            
            # Verificar que no existe
            retrieved = Factura.get_by_id(factura_id)
            assert retrieved is None
            
        finally:
            if original_db:
                Factura.db = original_db
    
    def test_factura_calculate_totals(self, temp_db, sample_producto):
        """Test cálculo automático de totales"""
        original_db_factura = Factura.__dict__.get('db')
        original_db_item = FacturaItem.__dict__.get('db')
        Factura.db = temp_db
        FacturaItem.db = temp_db
        
        try:
            factura = Factura(
                numero_factura="2025-CALC",
                fecha_factura="2025-01-01",
                nombre_cliente="Cliente Calc"
            )
            
            # Agregar items
            item1 = FacturaItem(
                producto_id=sample_producto.id,
                cantidad=2,
                precio_unitario=10.0,
                iva_aplicado=21.0,
                descuento=0.0
            )
            item1.calculate_totals()
            
            item2 = FacturaItem(
                producto_id=sample_producto.id,
                cantidad=1,
                precio_unitario=20.0,
                iva_aplicado=21.0,
                descuento=10.0  # 10% descuento
            )
            item2.calculate_totals()
            
            factura.items = [item1, item2]
            factura.calculate_totals()
            
            # Verificar cálculos
            # Item1: 2 * 10.0 = 20.0 subtotal, 4.2 IVA, 24.2 total
            # Item2: 1 * 20.0 = 20.0, con 10% desc = 18.0 subtotal, 3.78 IVA, 21.78 total
            expected_subtotal = 20.0 + 18.0  # 38.0
            expected_iva = 4.2 + 3.78  # 7.98
            expected_total = 24.2 + 21.78  # 45.98
            
            assert abs(factura.subtotal - expected_subtotal) < 0.01
            assert abs(factura.total_iva - expected_iva) < 0.01
            assert abs(factura.total_factura - expected_total) < 0.01
            
        finally:
            if original_db_factura:
                Factura.db = original_db_factura
            if original_db_item:
                FacturaItem.db = original_db_item
    
    def test_get_next_numero(self, temp_db):
        """Test generación de siguiente número de factura"""
        original_db = Factura.__dict__.get('db')
        Factura.db = temp_db
        
        try:
            # Sin facturas existentes
            next_numero = Factura.get_next_numero()
            current_year = datetime.now().year
            assert next_numero == f"1-{current_year}"

            # Crear una factura
            factura = Factura(
                numero_factura=next_numero,
                fecha_factura="2025-01-01",
                nombre_cliente="Cliente Test",
                subtotal=100.0,
                total_iva=21.0,
                total_factura=121.0
            )
            factura.save()

            # Siguiente número debería incrementar
            next_numero_2 = Factura.get_next_numero()
            assert next_numero_2 == f"2-{current_year}"
            
        finally:
            if original_db:
                Factura.db = original_db

class TestFacturaItemModel:
    """Tests para el modelo FacturaItem"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para tests"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        temp_db = Database(temp_file.name)
        
        yield temp_db
        
        os.unlink(temp_file.name)
    
    def test_factura_item_creation(self):
        """Test creación básica de FacturaItem"""
        item = FacturaItem(
            factura_id=1,
            producto_id=1,
            cantidad=2,
            precio_unitario=15.0,
            iva_aplicado=21.0,
            descuento=5.0
        )
        
        assert item.factura_id == 1
        assert item.producto_id == 1
        assert item.cantidad == 2
        assert item.precio_unitario == 15.0
        assert item.iva_aplicado == 21.0
        assert item.descuento == 5.0
    
    def test_factura_item_calculate_totals(self):
        """Test cálculo de totales en FacturaItem"""
        item = FacturaItem(
            cantidad=3,
            precio_unitario=20.0,
            iva_aplicado=21.0,
            descuento=10.0
        )
        
        item.calculate_totals()
        
        # Cálculos esperados:
        # Subtotal base: 3 * 20.0 = 60.0
        # Descuento: 60.0 * 0.10 = 6.0
        # Subtotal con descuento: 60.0 - 6.0 = 54.0
        # IVA: 54.0 * 0.21 = 11.34
        # Total: 54.0 + 11.34 = 65.34
        
        assert abs(item.subtotal - 54.0) < 0.01
        assert abs(item.descuento_amount - 6.0) < 0.01
        assert abs(item.iva_amount - 11.34) < 0.01
        assert abs(item.total - 65.34) < 0.01
    
    def test_factura_item_no_discount(self):
        """Test cálculo sin descuento"""
        item = FacturaItem(
            cantidad=2,
            precio_unitario=25.0,
            iva_aplicado=10.0,
            descuento=0.0
        )
        
        item.calculate_totals()
        
        # Cálculos esperados:
        # Subtotal: 2 * 25.0 = 50.0
        # Descuento: 0.0
        # IVA: 50.0 * 0.10 = 5.0
        # Total: 50.0 + 5.0 = 55.0
        
        assert abs(item.subtotal - 50.0) < 0.01
        assert abs(item.descuento_amount - 0.0) < 0.01
        assert abs(item.iva_amount - 5.0) < 0.01
        assert abs(item.total - 55.0) < 0.01
    
    def test_factura_item_save_and_retrieve(self, temp_db):
        """Test guardar y recuperar FacturaItem"""
        original_db = FacturaItem.__dict__.get('db')
        FacturaItem.db = temp_db
        
        try:
            item = FacturaItem(
                factura_id=1,
                producto_id=1,
                cantidad=4,
                precio_unitario=12.5,
                iva_aplicado=21.0,
                descuento=15.0
            )
            item.calculate_totals()
            item.save()
            
            assert item.id is not None
            
            # Recuperar items por factura_id
            items = FacturaItem.get_by_factura_id(1)
            assert len(items) == 1
            
            retrieved_item = items[0]
            assert retrieved_item.factura_id == 1
            assert retrieved_item.producto_id == 1
            assert retrieved_item.cantidad == 4
            assert retrieved_item.precio_unitario == 12.5
            assert retrieved_item.iva_aplicado == 21.0
            assert retrieved_item.descuento == 15.0
            
        finally:
            if original_db:
                FacturaItem.db = original_db
