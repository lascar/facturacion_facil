#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de bout en bout pour le logo dans les PDFs
"""

import os
import tempfile
import pytest
from PIL import Image, ImageDraw
from database.models import Organizacion, Factura, FacturaItem, Producto
from utils.pdf_generator import PDFGenerator
from test.utils.test_database_manager import isolated_test_db


class TestPDFLogoEndToEnd:
    """Tests de bout en bout pour le logo dans les PDFs"""
    
    def test_complete_pdf_logo_workflow(self):
        """Test complet du workflow avec logo"""
        with isolated_test_db("test_logo_workflow") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # 1. Créer un logo temporaire
                temp_dir = tempfile.mkdtemp()
                logo_path = os.path.join(temp_dir, "test_company_logo.png")
                
                # Créer un logo simple mais reconnaissable
                img = Image.new('RGB', (200, 100), color='#2E86AB')
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 190, 90], fill='#F18F01', outline='white', width=2)
                draw.ellipse([150, 30, 180, 60], fill='white')
                img.save(logo_path)
                
                # 2. Configurer organisation avec logo
                org = Organizacion(
                    nombre="Test Company Logo",
                    direccion="123 Logo Street, Test City",
                    telefono="+34 123 456 789",
                    email="test@logocompany.com",
                    cif="B12345678",
                    logo_path=logo_path
                )
                org.save()
                
                # Vérifier que l'organisation a été sauvegardée avec le logo
                org_retrieved = Organizacion.get()
                assert org_retrieved is not None
                assert org_retrieved.logo_path == logo_path
                assert os.path.exists(org_retrieved.logo_path)
                
                # 3. Créer un produit
                producto = Producto(
                    nombre="Producto con Logo",
                    referencia="LOGO-001",
                    precio=100.0,
                    categoria="Test",
                    descripcion="Producto para test de logo",
                    iva_recomendado=21.0
                )
                producto.save()
                
                # 4. Créer une facture
                factura = Factura(
                    numero_factura="LOGO-TEST-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Logo Test",
                    dni_nie_cliente="12345678A",
                    direccion_cliente="456 Client Avenue",
                    email_cliente="cliente@test.com",
                    telefono_cliente="+34 987 654 321",
                    subtotal=100.0,
                    total_iva=21.0,
                    total_factura=121.0,
                    modo_pago="tarjeta"
                )
                factura.save()
                
                # 5. Ajouter item à la facture
                item = FacturaItem(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=1,
                    precio_unitario=100.0,
                    iva_aplicado=21.0,
                    descuento=0.0
                )
                item.calculate_totals()
                item.save()
                factura.items = [item]
                
                # 6. Générer PDF avec logo
                pdf_generator = PDFGenerator()
                
                # Test de la méthode create_logo_image
                logo_img = pdf_generator.create_logo_image(logo_path)
                assert logo_img is not None, "Le logo n'a pas pu être chargé"
                
                # Générer le PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                    pdf_path = temp_pdf.name
                
                try:
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False
                    )
                    
                    # 7. Vérifications finales
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    
                    # Vérifier que le PDF a une taille raisonnable (avec logo)
                    pdf_size = os.path.getsize(pdf_path)
                    assert pdf_size > 2000, f"PDF trop petit ({pdf_size} bytes), le logo pourrait manquer"
                    
                    print(f"✅ Test de bout en bout réussi!")
                    print(f"   📄 PDF généré: {os.path.basename(pdf_path)}")
                    print(f"   📊 Taille: {pdf_size} bytes")
                    print(f"   🖼️  Logo inclus: {os.path.basename(logo_path)}")
                    print(f"   🏢 Entreprise: {org.nombre}")
                    print(f"   💰 Total facture: {factura.total_factura}€")
                    
                finally:
                    # Nettoyer le PDF
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                
                # Nettoyer le logo temporaire
                if os.path.exists(logo_path):
                    os.unlink(logo_path)
                os.rmdir(temp_dir)
                
            finally:
                database.db = original_db
    
    def test_pdf_without_logo_fallback(self):
        """Test que le PDF se génère correctement même sans logo"""
        with isolated_test_db("test_no_logo_fallback") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Organisation sans logo
                org = Organizacion(
                    nombre="Company Without Logo",
                    direccion="No Logo Street",
                    telefono="+34 111 222 333",
                    email="nologo@company.com",
                    cif="B87654321",
                    logo_path=""  # Pas de logo
                )
                org.save()
                
                # Produit simple
                producto = Producto(
                    nombre="Producto Sin Logo",
                    referencia="NOLOGO-001",
                    precio=50.0
                )
                producto.save()
                
                # Facture simple
                factura = Factura(
                    numero_factura="NOLOGO-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Sin Logo",
                    subtotal=50.0,
                    total_iva=10.5,
                    total_factura=60.5,
                    modo_pago="efectivo"
                )
                factura.save()
                
                # Item
                item = FacturaItem(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=1,
                    precio_unitario=50.0,
                    iva_aplicado=21.0,
                    descuento=0.0
                )
                item.calculate_totals()
                item.save()
                factura.items = [item]
                
                # Générer PDF
                pdf_generator = PDFGenerator()
                
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                    pdf_path = temp_pdf.name
                
                try:
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False
                    )
                    
                    # Vérifications
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    assert os.path.getsize(pdf_path) > 1000
                    
                    print(f"✅ Test sans logo réussi!")
                    print(f"   📄 PDF généré sans logo: {os.path.basename(pdf_path)}")
                    print(f"   📊 Taille: {os.path.getsize(pdf_path)} bytes")
                    
                finally:
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                
            finally:
                database.db = original_db
    
    def test_logo_error_handling(self):
        """Test de gestion d'erreurs avec logo invalide"""
        with isolated_test_db("test_logo_errors") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                # Organisation avec logo inexistant
                org = Organizacion(
                    nombre="Company Invalid Logo",
                    direccion="Invalid Logo Street",
                    telefono="+34 444 555 666",
                    email="invalid@company.com",
                    cif="B99999999",
                    logo_path="/path/inexistant/logo.png"  # Logo inexistant
                )
                org.save()
                
                # Facture simple
                factura = Factura(
                    numero_factura="INVALID-LOGO-001",
                    fecha_factura="2024-01-15",
                    nombre_cliente="Cliente Logo Invalido",
                    subtotal=25.0,
                    total_iva=5.25,
                    total_factura=30.25,
                    modo_pago="tarjeta"
                )
                factura.save()
                factura.items = []
                
                # Générer PDF (doit fonctionner malgré le logo invalide)
                pdf_generator = PDFGenerator()
                
                # Test de la méthode create_logo_image avec logo invalide
                logo_img = pdf_generator.create_logo_image("/path/inexistant/logo.png")
                assert logo_img is None, "create_logo_image devrait retourner None pour un logo invalide"
                
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                    pdf_path = temp_pdf.name
                
                try:
                    # Le PDF doit se générer même avec un logo invalide
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=False
                    )
                    
                    assert result_path == pdf_path
                    assert os.path.exists(pdf_path)
                    assert os.path.getsize(pdf_path) > 500
                    
                    print(f"✅ Test gestion d'erreurs réussi!")
                    print(f"   📄 PDF généré malgré logo invalide")
                    print(f"   📊 Taille: {os.path.getsize(pdf_path)} bytes")
                    
                finally:
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                
            finally:
                database.db = original_db


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
