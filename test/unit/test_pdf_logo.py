#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que le logo de l'entreprise apparaît dans les PDFs
"""

import os
import tempfile
import pytest
from PIL import Image
from database.models import Organizacion, Factura, FacturaItem, Producto
from utils.pdf_generator import PDFGenerator
from test.utils.test_database_manager import isolated_test_db


class TestPDFLogo:
    """Tests pour le logo dans les PDFs"""
    
    @pytest.fixture
    def temp_logo(self):
        """Crée un logo temporaire pour les tests"""
        temp_dir = tempfile.mkdtemp()
        logo_path = os.path.join(temp_dir, "test_logo.png")
        
        # Créer une image de test (logo simple)
        img = Image.new('RGB', (200, 100), color='blue')
        img.save(logo_path)
        
        yield logo_path
        
        # Nettoyage
        if os.path.exists(logo_path):
            os.remove(logo_path)
        os.rmdir(temp_dir)
    
    def test_pdf_with_logo(self, temp_logo):
        """Test génération PDF avec logo"""
        with isolated_test_db("test_pdf_logo") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Créer organisation avec logo
                org = Organizacion(
                    nombre="Test Company",
                    direccion="123 Test Street",
                    telefono="123-456-789",
                    email="test@company.com",
                    cif="B12345678",
                    logo_path=temp_logo
                )
                org.save()
                
                # Créer un produit de test
                producto = Producto(
                    nombre="Producto Test",
                    referencia="TEST-001",
                    precio=10.0,
                    categoria="Test",
                    descripcion="Producto de prueba"
                )
                producto.save()
                
                # Créer factura de test
                factura = Factura(
                    numero_factura="TEST-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Test",
                    dni_nie_cliente="12345678A",
                    direccion_cliente="456 Client Street",
                    email_cliente="client@test.com",
                    telefono_cliente="987-654-321",
                    subtotal=10.0,
                    total_iva=2.1,
                    total_factura=12.1,
                    modo_pago="efectivo"
                )
                factura.save()
                
                # Añadir item a la factura
                item = FacturaItem(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=1,
                    precio_unitario=10.0,
                    iva_aplicado=21.0,
                    descuento=0.0
                )
                item.calculate_totals()
                item.save()
                factura.items = [item]
                
                # Generar PDF
                pdf_generator = PDFGenerator()
                
                # Crear archivo temporal para el PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                    pdf_path = temp_pdf.name
                
                try:
                    # Generar PDF sin abrir automáticamente
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False
                    )
                    
                    # Verificar que el PDF se generó
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    assert os.path.getsize(pdf_path) > 0
                    
                    print(f"✅ PDF generado exitosamente: {os.path.basename(pdf_path)}")
                    print(f"📄 Tamaño del PDF: {os.path.getsize(pdf_path)} bytes")
                    
                finally:
                    # Limpiar archivo PDF
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                        
            finally:
                database.db = original_db
    
    def test_pdf_without_logo(self):
        """Test génération PDF sin logo"""
        with isolated_test_db("test_pdf_no_logo") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Créer organisation sans logo
                org = Organizacion(
                    nombre="Test Company No Logo",
                    direccion="123 Test Street",
                    telefono="123-456-789",
                    email="test@company.com",
                    cif="B12345678",
                    logo_path=""  # Sin logo
                )
                org.save()
                
                # Créer un produit de test
                producto = Producto(
                    nombre="Producto Test",
                    referencia="TEST-002",
                    precio=15.0
                )
                producto.save()
                
                # Créer factura de test
                factura = Factura(
                    numero_factura="TEST-002",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Test",
                    subtotal=15.0,
                    total_iva=3.15,
                    total_factura=18.15,
                    modo_pago="tarjeta"
                )
                factura.save()
                
                # Añadir item a la factura
                item = FacturaItem(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=1,
                    precio_unitario=15.0,
                    iva_aplicado=21.0,
                    descuento=0.0
                )
                item.calculate_totals()
                item.save()
                factura.items = [item]
                
                # Generar PDF
                pdf_generator = PDFGenerator()
                
                # Crear archivo temporal para el PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                    pdf_path = temp_pdf.name
                
                try:
                    # Generar PDF sin abrir automáticamente
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False
                    )
                    
                    # Verificar que el PDF se generó
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    assert os.path.getsize(pdf_path) > 0
                    
                    print(f"✅ PDF sin logo generado exitosamente: {os.path.basename(pdf_path)}")
                    
                finally:
                    # Limpiar archivo PDF
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                        
            finally:
                database.db = original_db
    
    def test_create_logo_image_method(self, temp_logo):
        """Test del método create_logo_image"""
        pdf_generator = PDFGenerator()
        
        # Test con logo válido
        logo_img = pdf_generator.create_logo_image(temp_logo)
        assert logo_img is not None
        
        # Test con logo inexistente
        logo_img_none = pdf_generator.create_logo_image("/path/inexistente.png")
        assert logo_img_none is None
        
        # Test con path vacío
        logo_img_empty = pdf_generator.create_logo_image("")
        assert logo_img_empty is None
        
        print("✅ Método create_logo_image funciona correctamente")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
