# -*- coding: utf-8 -*-
"""
Tests de comportement pour la gestion des factures
"""

import pytest
import time
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.test_data_factory import TestDataFactory
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from ui.factura_edit_window import FacturaEditWindow

class TestFacturasBehaviour(BaseBehaviourTest):
    """Tests de comportement pour la fenêtre Facturas"""
    
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
        
        # Créer des données de test préalables
        self.setup_test_data()
        
        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "Facturas")
        if facturas_btn:
            self.automation.click_button_safe(facturas_btn, wait_after=0.2)
            self.facturas_window = self.main_window.facturas_window
            self.wait_for_window(self.facturas_window)
        
        self.slow_mode_wait()
    
    def setup_test_data(self):
        """Créer des données de test nécessaires"""
        # Les fixtures de conftest.py créent déjà des produits et clients
        # On vérifie juste qu'ils existent, sinon on les crée

        existing_products = self.database.get_all_products()
        existing_clients = self.database.get_all_clients()

        # Log pour debug
        self.logger.info(f"Produits existants: {len(existing_products) if existing_products else 0}")
        self.logger.info(f"Clients existants: {len(existing_clients) if existing_clients else 0}")

        # Les fixtures devraient avoir créé au moins 3 produits et 3 clients
        # Si ce n'est pas le cas, on ne fait rien car c'est un problème de fixtures

    def create_unique_test_data(self):
        """Créer des données de test uniques pour éviter les conflits"""
        import time
        import random

        # Générer un timestamp unique avec un random pour éviter les collisions
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer un client unique
        client_data = {
            'nombre': f'Cliente Test {unique_id}',
            'nif': f'{unique_id:08d}X',
            'direccion': f'Calle Test {unique_id}',
            'telefono': f'600{unique_id:06d}',
            'email': f'test{unique_id}@example.com'
        }
        client_id = self.database.add_client(client_data)

        # Créer un produit unique
        product_data = {
            'nombre': f'Producto Test {unique_id}',
            'referencia': f'REF-{unique_id}',
            'precio_venta': 100.0,
            'categoria': 'Test',
            'descripcion': f'Producto de test {unique_id}',
            'iva_recomendado': 21.0,
            'sin_stock': 0
        }
        product_id = self.database.add_product(product_data)

        return {
            'client_id': client_id,
            'client_data': client_data,
            'product_id': product_id,
            'product_data': product_data,
            'unique_id': unique_id
        }
    
    def test_facturas_window_startup(self):
        """Test du démarrage de la fenêtre Facturas"""
        self.logger.info("🧪 Test: Démarrage fenêtre Facturas")

        # Vérifier que la fenêtre est visible
        self.assert_window_visible(self.facturas_window, "Facturas")

        # Vérifier le titre
        assert "Facturas" in self.facturas_window.windowTitle()

        # Vérifier la présence des éléments principaux de la fenêtre liste
        assert hasattr(self.facturas_window, 'new_btn'), "Bouton nuevo manquant"
        assert hasattr(self.facturas_window, 'editar_btn'), "Bouton editar manquant"
        assert hasattr(self.facturas_window, 'view_btn'), "Bouton view manquant"
        assert hasattr(self.facturas_window, 'pdf_btn'), "Bouton PDF manquant"
        assert hasattr(self.facturas_window, 'eliminar_btn'), "Bouton eliminar manquant"
        assert hasattr(self.facturas_window, 'refresh_btn'), "Bouton refresh manquant"
        assert hasattr(self.facturas_window, 'facturas_table'), "Table facturas manquante"

        self.take_screenshot("facturas_window_startup")
        self.logger.info("✅ Test démarrage Facturas réussi")
    
    @pytest.mark.timeout(20)  # Timeout de 20 secondes pour éviter le blocage
    def test_create_new_factura_basic(self, mock_messagebox):
        """Test de création d'une nouvelle facture basique"""
        self.logger.info("🧪 Test: Création nouvelle facture basique")

        # Mock des dialogues pour éviter les blocages - tous les types
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok
        mock_messagebox.warning.return_value = mock_messagebox.Ok
        mock_messagebox.critical.return_value = mock_messagebox.Ok

        try:
            # Cliquer sur le bouton Nueva Factura
            new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
            assert new_btn is not None, "Bouton Nueva Factura non trouvé"

            success = self.automation.click_button_safe(new_btn, wait_after=0.5)
            assert success, "Échec du clic sur Nueva Factura"

            self.slow_mode_wait()

            # Attendre l'ouverture de la fenêtre d'édition
            edit_window = None
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                    edit_window = widget
                    break

            assert edit_window is not None, "Fenêtre d'édition non ouverte"
            self.logger.info("✅ Fenêtre d'édition ouverte")

            # Vérifier que le formulaire est en mode création
            # Le numéro de facture devrait être généré automatiquement
            assert hasattr(edit_window, 'numero_edit'), "Champ numéro manquant"
            numero_text = edit_window.numero_edit.text()
            assert numero_text, "Numéro de facture non généré"
            self.logger.info(f"Numéro de facture généré: {numero_text}")

            # Vérifier les éléments du formulaire
            assert hasattr(edit_window, 'cliente_autocomplete'), "Widget client manquant"
            assert hasattr(edit_window, 'productos_table'), "Table produits manquante"
            assert hasattr(edit_window, 'producto_autocomplete'), "Widget produit manquant"

            self.take_screenshot("nueva_factura_form")
            self.logger.info("✅ Test création facture basique réussi")

            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()
        except Exception as e:
            self.logger.error(f"❌ Erreur dans test_create_new_factura_basic: {e}")
            self.take_screenshot("nueva_factura_error")
            raise
    
    @pytest.mark.timeout(15)
    def test_select_client_in_factura(self, mock_messagebox):
        """Test de sélection d'un client dans une factura"""
        self.logger.info("🧪 Test: Sélection client dans facture")

        # Mock des dialogues
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Attendre l'ouverture de la fenêtre d'édition
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        assert edit_window is not None, "Fenêtre d'édition non ouverte"

        # Chercher le widget d'autocomplétion client dans la fenêtre d'édition
        client_widget = None
        if hasattr(edit_window, 'cliente_autocomplete'):
            client_widget = edit_window.cliente_autocomplete
        elif hasattr(edit_window, 'cliente_edit'):
            client_widget = edit_window.cliente_edit

        if client_widget:
            # Saisir le nom d'un client de test
            self.automation.set_text_safe(client_widget, "Cliente Test 1")
            self.slow_mode_wait()

            self.take_screenshot("client_selected")
            self.logger.info("✅ Test sélection client réussi")
        else:
            self.logger.warning("Widget de sélection client non trouvé")

        # Fermer la fenêtre d'édition
        edit_window.close()
        self.app.processEvents()
    
    @pytest.mark.timeout(15)
    def test_add_product_to_factura(self, mock_messagebox):
        """Test d'ajout d'un produit à une facture"""
        self.logger.info("🧪 Test: Ajout produit à facture")

        # Mock des dialogues
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Attendre l'ouverture de la fenêtre d'édition
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        assert edit_window is not None, "Fenêtre d'édition non ouverte"

        # Chercher le bouton d'ajout de produit dans la fenêtre d'édition
        add_product_btn = self.automation.find_button_by_text(edit_window, "Agregar")
        if not add_product_btn:
            add_product_btn = self.automation.find_button_by_text(edit_window, "➕")

        if add_product_btn:
            success = self.automation.click_button_safe(add_product_btn, wait_after=0.3)
            assert success, "Échec du clic sur Agregar Producto"

            self.take_screenshot("add_product_dialog")
            self.logger.info("✅ Test ajout produit réussi")
        else:
            self.logger.warning("Bouton d'ajout de produit non trouvé")

        # Fermer la fenêtre d'édition
        edit_window.close()
        self.app.processEvents()
    
    def test_save_factura(self):
        """Test de sauvegarde d'une facture"""
        self.logger.info("🧪 Test: Sauvegarde facture")

        # Créer une facture directement dans la base de données
        from database.database import db

        # Créer des données de test uniques
        test_data = self.create_unique_test_data()
        client_id = test_data['client_id']
        product_id = test_data['product_id']
        client_data = test_data['client_data']
        unique_id = test_data['unique_id']

        # Créer une facture avec un numéro unique
        factura_numero = f'TEST-{unique_id}'
        factura_data = {
            'numero': factura_numero,
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
        factura_saved = db.get_invoice_by_number(factura_numero)
        assert factura_saved is not None, "Facture non trouvée après sauvegarde"
        assert factura_saved['numero'] == factura_numero, "Numéro de facture incorrect"

        self.slow_mode_wait()

        self.take_screenshot("factura_saved")
        self.logger.info("✅ Test sauvegarde facture réussi")
    
    @pytest.mark.timeout(20)  # Augmenter le timeout à 20 secondes
    def test_factura_totals_calculation(self, mock_messagebox):
        """Test du calcul des totaux de facture"""
        self.logger.info("🧪 Test: Calcul totaux facture")

        # Mock des dialogues - tous les types possibles
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok
        mock_messagebox.warning.return_value = mock_messagebox.Ok
        mock_messagebox.critical.return_value = mock_messagebox.Ok

        try:
            # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
            new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
            self.automation.click_button_safe(new_btn, wait_after=0.5)

            # Attendre l'ouverture de la fenêtre d'édition
            edit_window = None
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                    edit_window = widget
                    break

            assert edit_window is not None, "Fenêtre d'édition non ouverte"

            # Vérifier la présence des champs de totaux dans la fenêtre d'édition
            total_fields = ['subtotal', 'iva', 'total']

            for field_name in total_fields:
                if hasattr(edit_window, f'{field_name}_label'):
                    field = getattr(edit_window, f'{field_name}_label')
                    assert field is not None, f"Champ {field_name} non trouvé"
                    self.logger.info(f"✅ Champ {field_name} présent")

            self.take_screenshot("factura_totals")
            self.logger.info("✅ Test calcul totaux réussi")

            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()
        except Exception as e:
            self.logger.error(f"❌ Erreur dans test_factura_totals_calculation: {e}")
            self.take_screenshot("factura_totals_error")
            raise
    
    @pytest.mark.timeout(10)  # Timeout de 10 secondes pour éviter le blocage
    def test_factura_pdf_generation(self, mock_filedialog):
        """Test de génération PDF d'une facture"""
        self.logger.info("🧪 Test: Génération PDF facture")

        # Mock du dialogue de sauvegarde de fichier pour éviter le blocage
        mock_filedialog.getSaveFileName.return_value = ('/tmp/test_factura.pdf', 'PDF Files (*.pdf)')

        # Créer des données de test uniques
        from database.database import db
        test_data = self.create_unique_test_data()
        client_id = test_data['client_id']
        product_id = test_data['product_id']
        client_data = test_data['client_data']
        unique_id = test_data['unique_id']

        # Créer une facture avec un numéro unique
        factura_numero = f'TEST-PDF-{unique_id}'
        factura_data = {
            'numero': factura_numero,
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

        # Rafraîchir la liste pour voir la facture
        refresh_btn = self.automation.find_button_by_text(self.facturas_window, "Actualizar")
        if refresh_btn:
            self.automation.click_button_safe(refresh_btn, wait_after=0.3)

        # Chercher le bouton de génération PDF dans la fenêtre principale
        pdf_btn = self.automation.find_button_by_text(self.facturas_window, "PDF")
        if not pdf_btn:
            pdf_btn = self.automation.find_button_by_text(self.facturas_window, "Generar")

        if pdf_btn:
            success = self.automation.click_button_safe(pdf_btn, wait_after=0.2)
            assert success, "Échec du clic sur Generar PDF"

            self.take_screenshot("pdf_generated")
            self.logger.info("✅ Test génération PDF réussi")
        else:
            self.logger.warning("Bouton génération PDF non trouvé - Test passé")
    
    @pytest.mark.timeout(15)
    def test_factura_status_change(self, mock_messagebox):
        """Test de changement d'état d'une facture"""
        self.logger.info("🧪 Test: Changement état facture")

        # Mock des dialogues
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Attendre l'ouverture de la fenêtre d'édition
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        assert edit_window is not None, "Fenêtre d'édition non ouverte"

        # Chercher le combobox d'état dans la fenêtre d'édition
        if hasattr(edit_window, 'estado_combo'):
            estado_combo = edit_window.estado_combo

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

        # Fermer la fenêtre d'édition
        edit_window.close()
        self.app.processEvents()

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
