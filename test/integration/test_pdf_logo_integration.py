#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour vérifier visuellement le logo dans les PDFs
"""

import os
import tempfile
import pytest
from PIL import Image, ImageDraw, ImageFont
from database.models import Organizacion, Factura, FacturaItem, Producto
from utils.pdf_generator import PDFGenerator
from test.utils.test_database_manager import isolated_test_db


class TestPDFLogoIntegration:
    """Tests d'intégration pour le logo dans les PDFs"""
    
    @pytest.fixture
    def company_logo(self):
        """Crée un logo d'entreprise réaliste pour les tests"""
        temp_dir = tempfile.mkdtemp()
        logo_path = os.path.join(temp_dir, "company_logo.png")
        
        # Créer un logo plus réaliste
        img = Image.new('RGB', (300, 150), color='white')
        draw = ImageDraw.Draw(img)
        
        # Dessiner un logo simple avec texte
        try:
            # Essayer d'utiliser une police par défaut
            font = ImageFont.load_default()
        except:
            font = None
        
        # Fond bleu
        draw.rectangle([10, 10, 290, 140], fill='#2E86AB', outline='#A23B72', width=3)
        
        # Texte de l'entreprise
        draw.text((50, 50), "ACME Corp", fill='white', font=font)
        draw.text((50, 80), "Solutions", fill='white', font=font)
        
        # Cercle décoratif
        draw.ellipse([200, 30, 270, 100], fill='#F18F01', outline='white', width=2)
        
        img.save(logo_path)
        
        yield logo_path
        
        # Nettoyage
        if os.path.exists(logo_path):
            os.remove(logo_path)
        os.rmdir(temp_dir)
    
    def test_generate_pdf_with_logo_visual_check(self, company_logo):
        """Test génération PDF avec logo - vérification visuelle"""
        with isolated_test_db("test_pdf_logo_visual") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Créer organisation avec logo
                org = Organizacion(
                    nombre="ACME Corporation",
                    direccion="123 Business Avenue, Madrid, España",
                    telefono="+34 91 123 45 67",
                    email="info@acmecorp.es",
                    cif="B12345678",
                    logo_path=company_logo
                )
                org.save()
                
                # Créer quelques produits
                productos = [
                    Producto(
                        nombre="Consultoría IT",
                        referencia="CONS-001",
                        precio=150.0,
                        categoria="Servicios",
                        descripcion="Consultoría en tecnologías de la información",
                        iva_recomendado=21.0
                    ),
                    Producto(
                        nombre="Desarrollo Web",
                        referencia="WEB-001", 
                        precio=2500.0,
                        categoria="Desarrollo",
                        descripcion="Desarrollo de aplicación web personalizada",
                        iva_recomendado=21.0
                    ),
                    Producto(
                        nombre="Mantenimiento",
                        referencia="MANT-001",
                        precio=80.0,
                        categoria="Servicios",
                        descripcion="Mantenimiento mensual de sistemas",
                        iva_recomendado=21.0
                    )
                ]
                
                for producto in productos:
                    producto.save()
                
                # Créer factura completa
                factura = Factura(
                    numero_factura="FAC-2024-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Empresa Cliente S.L.",
                    dni_nie_cliente="B87654321",
                    direccion_cliente="456 Client Street, Barcelona, España",
                    email_cliente="cliente@empresa.com",
                    telefono_cliente="+34 93 987 65 43",
                    subtotal=0.0,  # Se calculará
                    total_iva=0.0,  # Se calculará
                    total_factura=0.0,  # Se calculará
                    modo_pago="transferencia"
                )
                factura.save()
                
                # Añadir items a la factura
                items_data = [
                    (productos[0].id, 10, 150.0),  # 10 horas consultoría
                    (productos[1].id, 1, 2500.0),  # 1 desarrollo web
                    (productos[2].id, 3, 80.0)     # 3 meses mantenimiento
                ]
                
                items = []
                subtotal = 0.0
                total_iva = 0.0
                
                for producto_id, cantidad, precio_unitario in items_data:
                    item = FacturaItem(
                        factura_id=factura.id,
                        producto_id=producto_id,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        iva_aplicado=21.0,
                        descuento=0.0
                    )
                    item.calculate_totals()
                    item.save()
                    items.append(item)
                    
                    subtotal += item.subtotal
                    total_iva += item.iva_amount
                
                # Actualizar totales de la factura
                factura.subtotal = subtotal
                factura.total_iva = total_iva
                factura.total_factura = subtotal + total_iva
                factura.save()
                factura.items = items
                
                # Generar PDF
                pdf_generator = PDFGenerator()
                
                # Crear archivo en directorio temporal con nombre descriptivo
                output_dir = tempfile.mkdtemp()
                pdf_path = os.path.join(output_dir, "factura_con_logo_test.pdf")
                
                try:
                    # Generar PDF
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False  # No abrir automáticamente en tests
                    )
                    
                    # Verificaciones
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    assert os.path.getsize(pdf_path) > 0
                    
                    print(f"\n✅ PDF con logo generado exitosamente!")
                    print(f"📄 Archivo: {pdf_path}")
                    print(f"📊 Tamaño: {os.path.getsize(pdf_path)} bytes")
                    print(f"🏢 Empresa: {org.nombre}")
                    print(f"🖼️  Logo: {os.path.basename(company_logo)}")
                    print(f"💰 Total factura: {factura.total_factura:.2f}€")
                    print(f"\n🔍 Para verificar visualmente el logo, abra el archivo:")
                    print(f"   {pdf_path}")
                    
                    # Mantener el archivo para inspección manual
                    # (en un entorno de CI/CD, esto se podría omitir)
                    
                finally:
                    # En tests automatizados, limpiaríamos el archivo
                    # if os.path.exists(pdf_path):
                    #     os.unlink(pdf_path)
                    # os.rmdir(output_dir)
                    pass
                        
            finally:
                database.db = original_db
    
    def test_logo_positioning_and_scaling(self, company_logo):
        """Test específico para posicionamiento y escalado del logo"""
        with isolated_test_db("test_logo_positioning") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Crear organización con logo
                org = Organizacion(
                    nombre="Test Logo Positioning",
                    direccion="Test Address",
                    telefono="123456789",
                    email="test@test.com",
                    cif="B12345678",
                    logo_path=company_logo
                )
                org.save()
                
                # Crear factura mínima
                factura = Factura(
                    numero_factura="LOGO-TEST-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Test",
                    subtotal=100.0,
                    total_iva=21.0,
                    total_factura=121.0,
                    modo_pago="efectivo"
                )
                factura.save()
                factura.items = []  # Sin items para simplificar
                
                # Test del método create_logo_image
                pdf_generator = PDFGenerator()
                logo_img = pdf_generator.create_logo_image(company_logo)
                
                assert logo_img is not None
                print(f"✅ Logo cargado correctamente para posicionamiento")
                
                # Generar PDF para verificar posicionamiento
                output_dir = tempfile.mkdtemp()
                pdf_path = os.path.join(output_dir, "test_logo_positioning.pdf")
                
                result_path = pdf_generator.generar_factura_pdf(
                    factura, 
                    output_path=pdf_path, 
                    auto_open=False
                )
                
                assert os.path.exists(pdf_path)
                print(f"✅ PDF con logo posicionado generado: {pdf_path}")
                
            finally:
                database.db = original_db


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s para ver los prints
