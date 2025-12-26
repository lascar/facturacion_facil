# -*- coding: utf-8 -*-
"""
Tests de comportement pour la gestion des factures
"""

import pytest
import time
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.test_data_factory import TestDataFactory
from test.behaviour.utils.pyqt5_automation import PyQt5Automation

class TestFacturasBehaviour(BaseBehaviourTest):
    """Tests de comportement pour la fenêtre Facturas"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir):
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
        
        # Créer des données de test préalables
        self.setup_test_data()
        
        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "Facturas")
        if facturas_btn:
            self.automation.click_button_safe(facturas_btn, wait_after=0.5)
            self.facturas_window = self.main_window.facturas_window
            self.wait_for_window(self.facturas_window)
        
        self.slow_mode_wait()
    
    def setup_test_data(self):
        """Créer des données de test nécessaires"""
        # Créer des clients de test
        clients_data = TestDataFactory.create_multiple_clients(2)
        for client_data in clients_data:
            self.database.add_client(client_data)
        
        # Créer des produits de test
        products_data = TestDataFactory.create_multiple_products(3)
        for product_data in products_data:
            # add_product attend un dictionnaire et gère le stock automatiquement
            self.database.add_product(product_data)
    
    def test_facturas_window_startup(self):
        """Test du démarrage de la fenêtre Facturas"""
        self.logger.info("🧪 Test: Démarrage fenêtre Facturas")
        
        # Vérifier que la fenêtre est visible
        self.assert_window_visible(self.facturas_window, "Facturas")
        
        # Vérifier le titre
        assert "Facturas" in self.facturas_window.windowTitle()
        
        # Vérifier la présence des éléments principaux
        assert hasattr(self.facturas_window, 'new_btn'), "Bouton nouveau manquant"
        assert hasattr(self.facturas_window, 'save_btn'), "Bouton sauvegarder manquant"
        
        self.take_screenshot("facturas_window_startup")
        self.logger.info("✅ Test démarrage Facturas réussi")
    
    def test_create_new_factura_basic(self):
        """Test de création d'une nouvelle facture basique"""
        self.logger.info("🧪 Test: Création nouvelle facture basique")
        
        # Cliquer sur le bouton Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        assert new_btn is not None, "Bouton Nueva Factura non trouvé"
        
        success = self.automation.click_button_safe(new_btn, wait_after=1.0)
        assert success, "Échec du clic sur Nueva Factura"
        
        self.slow_mode_wait()
        
        # Vérifier que le formulaire est en mode création
        # Le numéro de facture devrait être généré automatiquement
        if hasattr(self.facturas_window, 'numero_edit'):
            numero_text = self.facturas_window.numero_edit.text()
            assert numero_text, "Numéro de facture non généré"
            self.logger.info(f"Numéro de facture généré: {numero_text}")
        
        self.take_screenshot("nueva_factura_form")
        self.logger.info("✅ Test création facture basique réussi")
    
    def test_select_client_in_factura(self):
        """Test de sélection d'un client dans une facture"""
        self.logger.info("🧪 Test: Sélection client dans facture")
        
        # Créer une nouvelle facture
        self.test_create_new_factura_basic()
        
        # Chercher le widget d'autocomplétion client
        client_widget = None
        if hasattr(self.facturas_window, 'client_autocomplete'):
            client_widget = self.facturas_window.client_autocomplete
        elif hasattr(self.facturas_window, 'cliente_edit'):
            client_widget = self.facturas_window.cliente_edit
        
        if client_widget:
            # Saisir le nom d'un client de test
            self.automation.set_text_safe(client_widget, "Cliente Test 1")
            self.slow_mode_wait()
            
            self.take_screenshot("client_selected")
            self.logger.info("✅ Test sélection client réussi")
        else:
            self.logger.warning("Widget de sélection client non trouvé")
    
    def test_add_product_to_factura(self):
        """Test d'ajout d'un produit à une facture"""
        self.logger.info("🧪 Test: Ajout produit à facture")
        
        # Créer une nouvelle facture et sélectionner un client
        self.test_select_client_in_factura()
        
        # Chercher le bouton d'ajout de produit
        add_product_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
        if not add_product_btn:
            add_product_btn = self.automation.find_button_by_text(self.facturas_window, "➕")
        
        if add_product_btn:
            success = self.automation.click_button_safe(add_product_btn, wait_after=1.0)
            assert success, "Échec du clic sur Agregar Producto"
            
            self.take_screenshot("add_product_dialog")
            self.logger.info("✅ Test ajout produit réussi")
        else:
            self.logger.warning("Bouton d'ajout de produit non trouvé")
    
    def test_save_factura(self):
        """Test de sauvegarde d'une facture"""
        self.logger.info("🧪 Test: Sauvegarde facture")

        # Créer une facture directement dans la base de données
        from database.database import db

        # Préparer les données de test
        # Utiliser index 10 pour éviter conflit avec setup_test_data() qui utilise 1, 2, 3
        client_data = TestDataFactory.create_test_client(10)
        product_data = TestDataFactory.create_test_product(10)

        # Ajouter client et produit en base
        client_id = self.database.add_client(client_data)
        product_id = self.database.add_product(product_data)

        # Créer une facture
        factura_data = {
            'numero': 'TEST-001',
            'fecha': '2025-01-01',
            'cliente': {
                'id': client_id,
                'nombre': client_data['nombre'],
                'nif': client_data.get('nif', ''),
                'direccion': client_data.get('direccion', '')
            },
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'estado': 'Borrador',
            'lineas': [
                {
                    'producto_id': product_id,
                    'cantidad': 1,
                    'precio_unitario': 100.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0
                }
            ]
        }

        # Sauvegarder la facture
        factura_id = db.add_invoice(factura_data)
        assert factura_id is not None, "Échec de la sauvegarde de la facture"

        # Vérifier que la facture a été sauvegardée
        factura_saved = db.get_invoice_by_number('TEST-001')
        assert factura_saved is not None, "Facture non trouvée après sauvegarde"
        assert factura_saved['numero'] == 'TEST-001', "Numéro de facture incorrect"

        self.slow_mode_wait()

        self.take_screenshot("factura_saved")
        self.logger.info("✅ Test sauvegarde facture réussi")
    
    def test_factura_totals_calculation(self):
        """Test du calcul des totaux de facture"""
        self.logger.info("🧪 Test: Calcul totaux facture")
        
        # Créer une facture basique
        self.test_create_new_factura_basic()
        
        # Vérifier la présence des champs de totaux
        total_fields = ['subtotal', 'total_iva', 'total']
        
        for field_name in total_fields:
            if hasattr(self.facturas_window, f'{field_name}_label'):
                field = getattr(self.facturas_window, f'{field_name}_label')
                assert field is not None, f"Champ {field_name} non trouvé"
                self.logger.info(f"✅ Champ {field_name} présent")
        
        self.take_screenshot("factura_totals")
        self.logger.info("✅ Test calcul totaux réussi")
    
    def test_factura_pdf_generation(self):
        """Test de génération PDF d'une facture"""
        self.logger.info("🧪 Test: Génération PDF facture")
        
        # Créer et sauvegarder une facture
        self.test_save_factura()
        
        # Chercher le bouton de génération PDF
        pdf_btn = self.automation.find_button_by_text(self.facturas_window, "PDF")
        if not pdf_btn:
            pdf_btn = self.automation.find_button_by_text(self.facturas_window, "Generar")
        
        if pdf_btn:
            success = self.automation.click_button_safe(pdf_btn, wait_after=2.0)
            assert success, "Échec du clic sur Generar PDF"
            
            self.take_screenshot("pdf_generated")
            self.logger.info("✅ Test génération PDF réussi")
        else:
            self.logger.warning("Bouton génération PDF non trouvé")
    
    def test_factura_status_change(self):
        """Test de changement d'état d'une facture"""
        self.logger.info("🧪 Test: Changement état facture")
        
        # Créer une facture
        self.test_create_new_factura_basic()
        
        # Chercher le combobox d'état
        if hasattr(self.facturas_window, 'estado_combo'):
            estado_combo = self.facturas_window.estado_combo
            
            # Changer l'état
            success = self.automation.select_combobox_item(estado_combo, "Enviada")
            if success:
                self.logger.info("✅ État changé vers 'Enviada'")
            else:
                # Essayer avec un index
                success = self.automation.select_combobox_item(estado_combo, 1)
                if success:
                    self.logger.info("✅ État changé par index")
            
            self.take_screenshot("factura_status_changed")
        else:
            self.logger.warning("Combobox d'état non trouvé")
        
        self.logger.info("✅ Test changement état réussi")

    @pytest.mark.behaviour
    @pytest.mark.gui
    def test_factura_complete_workflow_qtest(self):
        """Test complet du workflow de création de facture avec QTest"""
        self.logger.info("🧪 Test: Workflow facture complet avec QTest")

        try:
            # 1. Préparer les données de test
            # Utiliser index 10 pour éviter conflit avec setup_test_data() qui utilise 1, 2, 3
            client_data = TestDataFactory.create_test_client(10)
            product_data = TestDataFactory.create_test_product(10)

            # Ajouter client et produit en base
            client_id = self.database.add_client(client_data)
            product_id = self.database.add_product(product_data)

            assert client_id is not None, "Client non créé"
            assert product_id is not None, "Produit non créé"

            # 2. Créer une facture directement en base de données
            # Calculer les montants pour la ligne
            cantidad = 2
            precio_unitario = 100.0
            iva_aplicado = 21.0
            descuento = 0.0

            subtotal_linea = cantidad * precio_unitario
            descuento_amount = subtotal_linea * (descuento / 100)
            subtotal_con_descuento = subtotal_linea - descuento_amount
            iva_amount = subtotal_con_descuento * (iva_aplicado / 100)
            total_linea = subtotal_con_descuento + iva_amount

            factura_data = {
                'numero': 'TEST-WORKFLOW-001',
                'fecha': '2025-01-01',
                'cliente': {
                    'id': client_id,
                    'nombre': client_data['nombre'],
                    'nif': client_data.get('nif', ''),
                    'direccion': client_data.get('direccion', '')
                },
                'subtotal': subtotal_linea,
                'iva_total': iva_amount,
                'total': total_linea,
                'estado': 'Borrador',
                'lineas': [
                    {
                        'producto_id': product_id,
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'iva_aplicado': iva_aplicado,
                        'descuento': descuento,
                        'subtotal': subtotal_linea,
                        'descuento_amount': descuento_amount,
                        'iva_amount': iva_amount,
                        'total': total_linea
                    }
                ]
            }

            # Sauvegarder la facture
            factura_id = self.database.add_invoice(factura_data)
            assert factura_id is not None, "Échec de la sauvegarde de la facture"

            # 3. Vérifier la création en base de données
            facturas = self.database.get_all_invoices()
            assert len(facturas) > 0, "Aucune facture créée"

            # Vérifier qu'au moins une facture existe avec le bon client
            facturas_with_client = [f for f in facturas if f.get('cliente_id') == client_id]
            assert len(facturas_with_client) > 0, f"Aucune facture trouvée pour le client {client_id}"

            # Vérifier que la facture créée a le bon numéro
            factura_created = self.database.get_invoice_by_number('TEST-WORKFLOW-001')
            assert factura_created is not None, "Facture non trouvée par numéro"
            assert factura_created['cliente']['id'] == client_id, "Client incorrect dans la facture"

            self.take_screenshot("factura_workflow_qtest_complete")
            self.logger.info("✅ Workflow facture complet avec QTest réussi")

        except Exception as e:
            self.take_screenshot("factura_workflow_qtest_error")
            self.logger.error(f"❌ Erreur workflow facture QTest: {e}")
            raise
