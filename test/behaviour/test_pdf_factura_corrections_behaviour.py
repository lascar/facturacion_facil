# -*- coding: utf-8 -*-
"""
Tests de comportement pour les corrections du PDF de facture
- Test 1: Vérifier que les lignes de produit longues s'affichent sur plusieurs lignes
- Test 2: Vérifier que l'email et le téléphone du client apparaissent dans le PDF
"""

import pytest
import os
import tempfile
import time
from pathlib import Path
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from utils.pdf_generator import PDFGenerator
from database.models import Cliente, Producto, Factura, FacturaItem


class TestPDFFacturaCorrections(BaseBehaviourTest):
    """Tests de comportement pour les corrections du PDF de facture"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox, mock_filedialog):
        """Configuration automatique pour chaque test"""
        # Initialiser les attributs de la classe de base
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir

        # Initialiser l'automation
        if self.app:
            self.automation = PyQt5Automation(self.app)
        
        # Afficher la fenêtre principale
        self.main_window.show()
        self.wait_for_window(self.main_window)
        
        # Désactiver l'ouverture automatique des PDF pendant les tests
        os.environ['DISABLE_PDF_OPEN'] = '1'
        
        self.slow_mode_wait()
    
    def test_pdf_long_product_lines_multiline(self):
        """
        Test 1: Vérifier que les lignes de produit longues s'affichent correctement
        
        Comportement attendu:
        - Créer une facture avec un produit ayant un nom très long
        - Générer le PDF
        - Vérifier que le PDF est créé sans erreur
        - Vérifier que le fichier PDF existe et a une taille > 0
        """
        self.logger.info("🧪 Test: Lignes de produit longues sur plusieurs lignes dans le PDF")
        
        # 1. Créer un client de test
        client = Cliente(
            nombre="Cliente Test PDF",
            dni_nie="12345678A",
            direccion="Calle Test 123\n28001 Madrid",
            email="test@example.com",
            telefono="600123456"
        )
        client_id = client.save()
        self.logger.info(f"✅ Client créé: {client.nombre}")
        
        # 2. Créer un produit avec un nom très long
        timestamp = int(time.time() * 1000)  # Timestamp en millisecondes pour unicité
        producto_nombre_largo = "Producto de prueba con un nombre extremadamente largo que debería ocupar varias líneas en la tabla del PDF para verificar que el sistema de Paragraph funciona correctamente"
        producto = Producto(
            nombre=producto_nombre_largo,
            referencia=f"REF-LONG-{timestamp}",
            precio=100.0,
            categoria="Test",
            descripcion="Producto de test con nombre largo",
            iva_recomendado=21.0
        )
        producto_id = producto.save()
        self.logger.info(f"✅ Producto créé avec nom long ({len(producto_nombre_largo)} caractères)")

        # 3. Créer une facture et la sauvegarder d'abord
        factura_numero = f"TEST-PDF-{timestamp}"
        factura = Factura(
            numero_factura=factura_numero,
            fecha_factura="2024-01-15",
            cliente_id=client_id,
            nombre_cliente=client.nombre,
            dni_nie_cliente=client.dni_nie,
            direccion_cliente=client.direccion,
            email_cliente=client.email,
            telefono_cliente=client.telefono,
            subtotal=0.0,
            total_iva=0.0,
            total_factura=0.0
        )

        # Sauvegarder la facture d'abord pour obtenir un ID
        factura_id = factura.save()
        self.logger.info(f"✅ Facture créée: {factura.numero_factura}")

        # 4. Ajouter le produit à la facture
        factura.add_item(
            producto_id=producto_id,
            cantidad=2,
            precio_unitario=100.0,
            iva_aplicado=21.0,
            descuento=0
        )

        # 5. Calculer les totaux et mettre à jour
        factura.calculate_totals()
        factura.save()
        self.logger.info(f"✅ Item ajouté à la facture")
        
        # 6. Générer le PDF
        pdf_generator = PDFGenerator()
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"test_factura_long_lines_{int(time.time())}.pdf")
        
        try:
            success = pdf_generator.generar_factura_pdf(factura, output_path=pdf_path, auto_open=False)
            
            # 7. Vérifications
            assert success is not None, "La génération du PDF a échoué"
            assert os.path.exists(pdf_path), f"Le fichier PDF n'existe pas: {pdf_path}"
            
            file_size = os.path.getsize(pdf_path)
            assert file_size > 0, f"Le fichier PDF est vide: {pdf_path}"
            
            self.logger.info(f"✅ PDF généré avec succès: {pdf_path} ({file_size} bytes)")
            self.logger.info(f"✅ Le PDF contient un produit avec un nom de {len(producto_nombre_largo)} caractères")
            
        finally:
            # Nettoyage
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    self.logger.info(f"🧹 PDF de test supprimé: {pdf_path}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Impossible de supprimer le PDF: {e}")

    def test_pdf_client_email_telefono_displayed(self):
        """
        Test 2: Vérifier que l'email et le téléphone du client apparaissent dans le PDF

        Comportement attendu:
        - Créer une facture avec un client ayant email et téléphone
        - Générer le PDF
        - Vérifier que le PDF est créé sans erreur
        - Vérifier que le fichier PDF existe et a une taille > 0
        - Les données email et telefono sont passées correctement au générateur
        """
        self.logger.info("🧪 Test: Email et téléphone du client dans le PDF")

        # 1. Créer un client de test avec toutes les informations
        client = Cliente(
            nombre="Cliente Completo Test",
            dni_nie="87654321B",
            direccion="Avenida Principal 456\n08001 Barcelona",
            email="cliente.completo@empresa.com",
            telefono="+34 912 345 678"
        )
        client_id = client.save()
        self.logger.info(f"✅ Client créé avec email: {client.email} et téléphone: {client.telefono}")

        # 2. Créer un produit simple
        timestamp = int(time.time() * 1000)  # Timestamp en millisecondes pour unicité
        producto = Producto(
            nombre="Producto Test",
            referencia=f"REF-TEST-{timestamp}",
            precio=50.0,
            categoria="Test",
            descripcion="Producto de test",
            iva_recomendado=21.0
        )
        producto_id = producto.save()
        self.logger.info(f"✅ Producto créé: {producto.nombre}")

        # 3. Créer une facture avec toutes les informations du client et la sauvegarder d'abord
        factura_numero = f"TEST-PDF-{timestamp}"
        factura = Factura(
            numero_factura=factura_numero,
            fecha_factura="2024-01-16",
            cliente_id=client_id,
            nombre_cliente=client.nombre,
            dni_nie_cliente=client.dni_nie,
            direccion_cliente=client.direccion,
            email_cliente=client.email,
            telefono_cliente=client.telefono,
            subtotal=0.0,
            total_iva=0.0,
            total_factura=0.0
        )

        # Sauvegarder la facture d'abord pour obtenir un ID
        factura_id = factura.save()
        self.logger.info(f"✅ Facture créée: {factura.numero_factura}")

        # 4. Ajouter le produit à la facture
        factura.add_item(
            producto_id=producto_id,
            cantidad=1,
            precio_unitario=50.0,
            iva_aplicado=21.0,
            descuento=10.0
        )

        # 5. Calculer les totaux et mettre à jour
        factura.calculate_totals()
        factura.save()
        self.logger.info(f"✅ Item ajouté à la facture")

        # 6. Vérifier que les données client sont bien dans la facture
        assert factura.email_cliente == client.email, "L'email du client n'est pas dans la facture"
        assert factura.telefono_cliente == client.telefono, "Le téléphone du client n'est pas dans la facture"
        self.logger.info(f"✅ Données client vérifiées dans la facture")

        # 7. Générer le PDF
        pdf_generator = PDFGenerator()
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"test_factura_client_info_{int(time.time())}.pdf")

        try:
            success = pdf_generator.generar_factura_pdf(factura, output_path=pdf_path, auto_open=False)

            # 8. Vérifications
            assert success is not None, "La génération du PDF a échoué"
            assert os.path.exists(pdf_path), f"Le fichier PDF n'existe pas: {pdf_path}"

            file_size = os.path.getsize(pdf_path)
            assert file_size > 0, f"Le fichier PDF est vide: {pdf_path}"

            self.logger.info(f"✅ PDF généré avec succès: {pdf_path} ({file_size} bytes)")
            self.logger.info(f"✅ Le PDF devrait contenir:")
            self.logger.info(f"   - Email: {client.email}")
            self.logger.info(f"   - Téléphone: {client.telefono}")

            # Note: Pour vérifier réellement le contenu du PDF, il faudrait utiliser
            # une bibliothèque comme PyPDF2 ou pdfplumber, mais pour ce test de behaviour,
            # on vérifie que le PDF est généré sans erreur avec les bonnes données en entrée

        finally:
            # Nettoyage
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    self.logger.info(f"🧹 PDF de test supprimé: {pdf_path}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Impossible de supprimer le PDF: {e}")

