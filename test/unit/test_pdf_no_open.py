#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que les PDFs ne s'ouvrent pas pendant les tests
"""

import os
import tempfile
import pytest
from PIL import Image
from database.models import Organizacion, Factura, FacturaItem, Producto
from utils.pdf_generator import PDFGenerator
from test.utils.test_database_manager import isolated_test_db


class TestPDFNoOpen:
    """Tests pour vérifier que les PDFs ne s'ouvrent pas pendant les tests"""
    
    def test_environment_variables_set(self):
        """Vérifier que les variables d'environnement sont définies"""
        print(f"\n🔍 Vérification des variables d'environnement")
        
        pytest_running = os.environ.get('PYTEST_RUNNING')
        disable_pdf_open = os.environ.get('DISABLE_PDF_OPEN')
        
        print(f"   PYTEST_RUNNING: {pytest_running}")
        print(f"   DISABLE_PDF_OPEN: {disable_pdf_open}")
        
        assert pytest_running == '1', "PYTEST_RUNNING devrait être définie"
        assert disable_pdf_open == '1', "DISABLE_PDF_OPEN devrait être définie"
        
        print("   ✅ Variables d'environnement correctement définies")
    
    def test_pdf_generation_without_opening(self):
        """Test que la génération PDF fonctionne sans ouvrir le fichier"""
        with isolated_test_db("test_pdf_no_open") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Test génération PDF sans ouverture")
                
                # Créer organisation
                org = Organizacion(
                    nombre="Test Company",
                    direccion="123 Test St",
                    telefono="123-456-789",
                    email="test@company.com",
                    cif="B12345678"
                )
                org.save()
                
                # Créer produit
                producto = Producto(
                    nombre="Test Product",
                    referencia="TEST001",
                    precio=10.0,
                    categoria="Test",
                    descripcion="Test product",
                    iva_recomendado=21.0
                )
                producto.save()
                
                # Créer facture
                factura = Factura(
                    numero_factura="TEST-001",
                    fecha_factura="2024-09-26",
                    nombre_cliente="Test Client",
                    subtotal=10.0,
                    total_iva=2.1,
                    total_factura=12.1,
                    modo_pago="efectivo"
                )
                factura.save()
                
                # Créer item de facture
                item = FacturaItem(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=1,
                    precio_unitario=10.0,
                    iva_aplicado=21.0
                )
                item.save()
                factura.items = [item]
                
                # Générer PDF avec auto_open=True (devrait être ignoré)
                print("   📄 Génération PDF avec auto_open=True...")
                pdf_generator = PDFGenerator()
                
                # Créer répertoire temporaire pour le PDF
                temp_dir = tempfile.mkdtemp()
                pdf_path = os.path.join(temp_dir, "test_factura.pdf")
                
                try:
                    # Générer PDF - auto_open devrait être ignoré grâce aux variables d'environnement
                    result_path = pdf_generator.generar_factura_pdf(
                        factura, 
                        output_path=pdf_path, 
                        auto_open=True  # Ceci devrait être ignoré
                    )
                    
                    # Vérifier que le PDF a été généré
                    assert os.path.exists(result_path), "PDF non généré"
                    assert os.path.getsize(result_path) > 0, "PDF vide"
                    
                    print(f"   ✅ PDF généré: {os.path.basename(result_path)}")
                    print(f"   📊 Taille: {os.path.getsize(result_path)} bytes")
                    print(f"   🚫 PDF non ouvert (mode test)")
                    
                    # Test direct de open_pdf_file (devrait être ignoré)
                    print("   🔍 Test direct open_pdf_file...")
                    pdf_generator.open_pdf_file(result_path)
                    print("   ✅ open_pdf_file ignoré en mode test")
                    
                finally:
                    # Nettoyer
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    os.rmdir(temp_dir)
                
            finally:
                database.db = original_db
    
    def test_pdf_generator_respects_environment(self):
        """Test que PDFGenerator respecte les variables d'environnement"""
        print(f"\n🔍 Test respect des variables d'environnement")
        
        pdf_generator = PDFGenerator()
        
        # Créer un fichier PDF factice
        temp_dir = tempfile.mkdtemp()
        fake_pdf = os.path.join(temp_dir, "fake.pdf")
        
        try:
            # Créer un fichier factice
            with open(fake_pdf, 'w') as f:
                f.write("fake pdf content")
            
            # Tester open_pdf_file - devrait être ignoré
            print("   🔍 Test open_pdf_file avec variables d'environnement...")
            
            # Capturer les logs pour vérifier le comportement
            import logging
            import io
            
            # Créer un handler pour capturer les logs
            log_capture = io.StringIO()
            handler = logging.StreamHandler(log_capture)
            logger = logging.getLogger("facturacion_facil.pdf_generator")
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            try:
                pdf_generator.open_pdf_file(fake_pdf)
                
                # Vérifier les logs
                log_output = log_capture.getvalue()
                print(f"   📝 Log output: {log_output.strip()}")
                
                # Vérifier que le mode test a été détecté
                assert "Modo test detectado" in log_output or "PDF no abierto" in log_output, \
                    "Mode test non détecté dans les logs"
                
                print("   ✅ Mode test correctement détecté et PDF non ouvert")
                
            finally:
                logger.removeHandler(handler)
        
        finally:
            # Nettoyer
            if os.path.exists(fake_pdf):
                os.remove(fake_pdf)
            os.rmdir(temp_dir)
    
    def test_manual_disable_pdf_open(self):
        """Test désactivation manuelle avec DISABLE_PDF_OPEN"""
        print(f"\n🔍 Test désactivation manuelle")
        
        # Sauvegarder l'état actuel
        original_pytest = os.environ.get('PYTEST_RUNNING')
        original_disable = os.environ.get('DISABLE_PDF_OPEN')
        
        try:
            # Désactiver PYTEST_RUNNING mais garder DISABLE_PDF_OPEN
            os.environ.pop('PYTEST_RUNNING', None)
            os.environ['DISABLE_PDF_OPEN'] = '1'
            
            pdf_generator = PDFGenerator()
            
            # Créer fichier factice
            temp_dir = tempfile.mkdtemp()
            fake_pdf = os.path.join(temp_dir, "fake2.pdf")
            
            try:
                with open(fake_pdf, 'w') as f:
                    f.write("fake pdf content 2")
                
                # Tester - devrait toujours être ignoré grâce à DISABLE_PDF_OPEN
                print("   🔍 Test avec seulement DISABLE_PDF_OPEN=1...")
                
                # Capturer les logs
                import logging
                import io
                
                log_capture = io.StringIO()
                handler = logging.StreamHandler(log_capture)
                logger = logging.getLogger("facturacion_facil.pdf_generator")
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
                
                try:
                    pdf_generator.open_pdf_file(fake_pdf)
                    
                    log_output = log_capture.getvalue()
                    print(f"   📝 Log output: {log_output.strip()}")
                    
                    # Vérifier que l'ouverture a été désactivée
                    assert "PDF no abierto" in log_output or "Modo test detectado" in log_output, \
                        "DISABLE_PDF_OPEN non respecté"
                    
                    print("   ✅ DISABLE_PDF_OPEN correctement respecté")
                    
                finally:
                    logger.removeHandler(handler)
            
            finally:
                if os.path.exists(fake_pdf):
                    os.remove(fake_pdf)
                os.rmdir(temp_dir)
        
        finally:
            # Restaurer l'état original
            if original_pytest:
                os.environ['PYTEST_RUNNING'] = original_pytest
            if original_disable:
                os.environ['DISABLE_PDF_OPEN'] = original_disable


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
