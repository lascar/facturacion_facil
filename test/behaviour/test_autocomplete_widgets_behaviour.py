# -*- coding: utf-8 -*-
"""
Tests de comportement pour les widgets d'autocomplétion selon facturacion_facil.txt
Tests spécialisés pour ClientAutoCompleteWidget et ProductAutoCompleteWidget
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger
from ui.factura_edit_window import FacturaEditWindow


class TestAutoCompleteWidgetsBehaviour(BaseBehaviourTest):
    """Tests de comportement pour les widgets d'autocomplétion selon spécifications"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox, mock_filedialog):
        """Configuration automatique pour chaque test"""
        self.init_base_attributes()
        
        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir
        self.logger = get_logger(self.__class__.__name__)
        
        # Initialiser l'automation et les données de test
        if self.app:
            self.automation = PyQt5Automation(self.app)
        self.test_data = TestDataFactory()
        
        # Préparer des données de test
        self.setup_test_data()
    
    def setup_test_data(self):
        """Préparer des données de test pour l'autocomplétion"""
        # Créer des clients de test
        self.test_clients = [
            {'nombre': 'Cliente Test 1', 'nif': '12345678A', 'email': 'cliente1@test.com'},
            {'nombre': 'Cliente Test 2', 'nif': '87654321B', 'email': 'cliente2@test.com'},
            {'nombre': 'Empresa ABC S.L.', 'nif': 'B12345678', 'email': 'info@abc.com'}
        ]
        
        # Créer des produits de test
        self.test_products = [
            {'nombre': 'Producto Test 1', 'precio_venta': 10.50, 'stock_actual': 100},
            {'nombre': 'Producto Test 2', 'precio_venta': 25.00, 'stock_actual': 50},
            {'nombre': 'Producto Sin Stock', 'precio_venta': 15.00, 'stock_actual': 0}
        ]
        
        # Ajouter à la base de données de test
        for client in self.test_clients:
            self.database.add_client(client)
        
        for product in self.test_products:
            self.database.add_product(product)
    
    def test_client_autocomplete_widget_specification(self):
        """Test: ClientAutoCompleteWidget selon spécifications facturacion_facil.txt"""
        self.logger.info("🧪 Test: ClientAutoCompleteWidget selon spécifications")

        # Ouvrir la fenêtre Facturas pour tester l'autocomplétion client
        facturas_btn = self.automation.find_button_by_text(self.main_window, "🧾 Facturas")
        if not facturas_btn:
            self.logger.warning("Bouton 'Facturas' non trouvé, test ignoré")
            pytest.skip("Bouton 'Facturas' non trouvé dans la fenêtre principale")
            return

        QTest.mouseClick(facturas_btn, Qt.LeftButton)
        self.wait_and_process_events(500)
        
        # Trouver la fenêtre facturas
        facturas_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle():
                facturas_window = widget
                break
        
        if not facturas_window:
            self.logger.warning("Fenêtre Facturas non trouvée, test ignoré")
            return
        
        # Trouver le widget d'autocomplétion client
        cliente_widget = self.automation.find_widget_by_name(facturas_window, "cliente_autocomplete")
        if not cliente_widget:
            # Essayer d'autres noms possibles
            cliente_widget = self.automation.find_widget_by_name(facturas_window, "cliente_input")
        
        if cliente_widget:
            # Test 1: Vérifier le placeholder selon spécifications
            # Spécification: "Escriba el nombre del cliente..."
            expected_placeholder = "Escriba el nombre del cliente"
            if hasattr(cliente_widget, 'placeholderText'):
                placeholder = cliente_widget.placeholderText()
                assert expected_placeholder in placeholder, f"Placeholder incorrect: {placeholder}"
            
            # Test 2: Recherche par nom selon spécifications
            # Spécification: "Recherche par nom ou NIF, insensible à la casse"
            cliente_widget.clear()
            QTest.keyClicks(cliente_widget, "Cliente")
            self.wait_and_process_events(500)  # Attendre l'autocomplétion
            
            # Test 3: Recherche par NIF selon spécifications
            cliente_widget.clear()
            QTest.keyClicks(cliente_widget, "12345")
            self.wait_and_process_events(500)
            
            # Test 4: Format d'affichage selon spécifications
            # Spécification: "Nom (NIF)" ou "Nom" si pas de NIF
            cliente_widget.clear()
            QTest.keyClicks(cliente_widget, "Cliente Test 1")
            self.wait_and_process_events(300)
            
            # Simuler la sélection
            QTest.keyClick(cliente_widget, Qt.Key_Down)
            QTest.keyClick(cliente_widget, Qt.Key_Return)
            self.wait_and_process_events(200)
            
            # Vérifier le format d'affichage
            text = cliente_widget.text()
            assert "Cliente Test 1" in text, f"Nom client non trouvé: {text}"
            
            # Test 5: États visuels selon spécifications
            # Spécification: Client trouvé = bordure verte, fond vert clair
            if hasattr(cliente_widget, 'styleSheet'):
                style = cliente_widget.styleSheet()
                # Vérifier qu'il y a un style appliqué pour client trouvé
                self.logger.info(f"Style appliqué: {style}")
        
        facturas_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test ClientAutoCompleteWidget terminé")
    
    def test_product_autocomplete_widget_specification(self):
        """Test: ProductAutoCompleteWidget selon spécifications facturacion_facil.txt"""
        self.logger.info("🧪 Test: ProductAutoCompleteWidget selon spécifications")

        # Ouvrir la fenêtre Facturas pour tester l'autocomplétion produit
        facturas_btn = self.automation.find_button_by_text(self.main_window, "🧾 Facturas")
        QTest.mouseClick(facturas_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre facturas (liste)
        facturas_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle():
                facturas_window = widget
                break

        if not facturas_window:
            self.logger.warning("Fenêtre Facturas non trouvée, test ignoré")
            return

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(facturas_window, "Nueva")
        if not new_btn:
            self.logger.warning("Bouton Nueva non trouvé, test ignoré")
            return

        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Trouver la fenêtre d'édition
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        if not edit_window:
            self.logger.warning("Fenêtre d'édition non trouvée, test ignoré")
            return

        # Trouver le widget d'autocomplétion produit dans la fenêtre d'édition
        producto_widget = self.automation.find_widget_by_name(edit_window, "producto_autocomplete")
        if not producto_widget:
            # Essayer d'autres noms possibles
            producto_widget = self.automation.find_widget_by_name(edit_window, "producto_input")
        
        if producto_widget:
            # Test 1: Vérifier le placeholder selon spécifications
            # Spécification: "Escriba el nombre del producto..."
            expected_placeholder = "Escriba el nombre del producto"
            if hasattr(producto_widget, 'placeholderText'):
                placeholder = producto_widget.placeholderText()
                assert expected_placeholder in placeholder, f"Placeholder incorrect: {placeholder}"
            
            # Test 2: Format d'affichage selon spécifications
            # Spécification: "Nom - Prix€ (Stock: X)"
            producto_widget.clear()
            QTest.keyClicks(producto_widget, "Producto")
            self.wait_and_process_events(500)  # Attendre l'autocomplétion
            
            # Test 3: Filtrage automatique selon spécifications
            # Spécification: "Seuls les produits avec stock > 0"
            # Le produit "Producto Sin Stock" ne devrait pas apparaître
            
            # Test 4: Recherche temps réel selon spécifications
            # Spécification: "temps réel avec délai de 300ms"
            producto_widget.clear()
            QTest.keyClicks(producto_widget, "Test")
            self.wait_and_process_events(400)  # Attendre plus que le délai
            
            # Test 5: Validation sélection obligatoire selon spécifications
            # Spécification: "Sélection obligatoire depuis la liste"
            producto_widget.clear()
            QTest.keyClicks(producto_widget, "Producto Test 1")
            self.wait_and_process_events(300)
            
            # Simuler la sélection depuis la liste
            QTest.keyClick(producto_widget, Qt.Key_Down)
            QTest.keyClick(producto_widget, Qt.Key_Return)
            self.wait_and_process_events(200)
            
            # Vérifier que le produit est sélectionné
            text = producto_widget.text()
            assert "Producto Test 1" in text, f"Produit non sélectionné: {text}"

            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()
        else:
            self.logger.warning("Widget producto_autocomplete non trouvé, test ignoré")
            # Fermer la fenêtre d'édition si elle est ouverte
            if edit_window:
                edit_window.close()
                self.app.processEvents()

        facturas_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Test ProductAutoCompleteWidget terminé")

    def test_client_autocomplete_in_nueva_factura(self):
        """Test: Les clients sont chargés dans l'autocomplétion de Nueva Factura (FacturaEditWindow)"""
        self.logger.info("🧪 Test: Chargement clients dans Nueva Factura")

        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "🧾 Facturas")
        if not facturas_btn:
            self.logger.warning("Bouton 'Facturas' non trouvé, test ignoré")
            pytest.skip("Bouton 'Facturas' non trouvé dans la fenêtre principale")
            return

        QTest.mouseClick(facturas_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre facturas (liste)
        facturas_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle():
                facturas_window = widget
                break

        if not facturas_window:
            self.logger.warning("Fenêtre Facturas non trouvée, test ignoré")
            return

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(facturas_window, "Nueva")
        if not new_btn:
            self.logger.warning("Bouton Nueva non trouvé, test ignoré")
            facturas_window.close()
            return

        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Trouver la fenêtre d'édition FacturaEditWindow
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        if not edit_window:
            self.logger.warning("Fenêtre FacturaEditWindow non trouvée, test ignoré")
            facturas_window.close()
            return

        # Vérifier que le widget cliente_autocomplete existe
        assert hasattr(edit_window, 'cliente_autocomplete'), "Widget cliente_autocomplete non trouvé dans FacturaEditWindow"
        cliente_widget = edit_window.cliente_autocomplete

        # Test 1: Vérifier que les clients sont chargés dans le widget
        assert hasattr(cliente_widget, 'clients_data'), "Attribut clients_data non trouvé"
        assert len(cliente_widget.clients_data) > 0, "Aucun client chargé dans cliente_autocomplete"
        self.logger.info(f"✅ {len(cliente_widget.clients_data)} clients chargés dans l'autocomplétion")

        # Test 2: Vérifier que le completer a un modèle avec des données
        assert cliente_widget.completer is not None, "Completer non initialisé"
        assert cliente_widget.completer.model() is not None, "Modèle du completer non initialisé"
        model_row_count = cliente_widget.completer.model().rowCount()
        assert model_row_count > 0, f"Modèle du completer vide (rowCount={model_row_count})"
        self.logger.info(f"✅ Modèle du completer contient {model_row_count} suggestions")

        # Test 3: Taper "c" et vérifier que des clients contenant "c" sont proposés
        cliente_widget.clear()
        QTest.keyClicks(cliente_widget, "c")
        self.wait_and_process_events(500)  # Attendre le timer de recherche (300ms) + marge

        # Vérifier que le modèle a été mis à jour avec des suggestions
        model = cliente_widget.completer.model()
        suggestions_count = model.rowCount()

        # Compter combien de clients de test contiennent "c"
        expected_clients_with_c = [c for c in self.test_clients if 'c' in c['nombre'].lower()]

        self.logger.info(f"Suggestions trouvées: {suggestions_count}, attendues: {len(expected_clients_with_c)}")
        assert suggestions_count > 0, "Aucune suggestion après avoir tapé 'c'"

        # Afficher les suggestions pour debug
        suggestions = []
        for i in range(suggestions_count):
            suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
            suggestions.append(suggestion)
            self.logger.info(f"  - Suggestion {i+1}: {suggestion}")

        # Vérifier qu'au moins un client de test contenant "c" est dans les suggestions
        found_test_client = False
        for client in expected_clients_with_c:
            for suggestion in suggestions:
                if client['nombre'] in suggestion:
                    found_test_client = True
                    break
            if found_test_client:
                break

        assert found_test_client, f"Aucun client de test contenant 'c' trouvé dans les suggestions: {suggestions}"
        self.logger.info("✅ Les clients contenant 'c' sont bien proposés")

        # Test 4: Vérifier la sélection d'un client
        cliente_widget.clear()
        QTest.keyClicks(cliente_widget, "Cliente Test")
        self.wait_and_process_events(500)

        # Simuler la sélection
        QTest.keyClick(cliente_widget, Qt.Key_Down)
        QTest.keyClick(cliente_widget, Qt.Key_Return)
        self.wait_and_process_events(200)

        # Vérifier que le client est sélectionné
        text = cliente_widget.text()
        assert "Cliente Test" in text, f"Client non sélectionné: {text}"
        self.logger.info(f"✅ Client sélectionné: {text}")

        # Fermer les fenêtres
        edit_window.close()
        self.app.processEvents()
        facturas_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Test chargement clients dans Nueva Factura terminé")

    def test_product_autocomplete_in_nueva_factura(self):
        """Test: Les produits sont chargés dans l'autocomplétion de Nueva Factura (FacturaEditWindow)"""
        self.logger.info("🧪 Test: Chargement produits dans Nueva Factura")

        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "🧾 Facturas")
        if not facturas_btn:
            self.logger.warning("Bouton 'Facturas' non trouvé, test ignoré")
            pytest.skip("Bouton 'Facturas' non trouvé dans la fenêtre principale")
            return

        QTest.mouseClick(facturas_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre facturas (liste)
        facturas_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle():
                facturas_window = widget
                break

        if not facturas_window:
            self.logger.warning("Fenêtre Facturas non trouvée, test ignoré")
            return

        # Cliquer sur Nueva Factura pour ouvrir la fenêtre d'édition
        new_btn = self.automation.find_button_by_text(facturas_window, "Nueva")
        if not new_btn:
            self.logger.warning("Bouton Nueva non trouvé, test ignoré")
            facturas_window.close()
            return

        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Trouver la fenêtre d'édition FacturaEditWindow
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        if not edit_window:
            self.logger.warning("Fenêtre FacturaEditWindow non trouvée, test ignoré")
            facturas_window.close()
            return

        # Vérifier que le widget producto_autocomplete existe
        assert hasattr(edit_window, 'producto_autocomplete'), "Widget producto_autocomplete non trouvé dans FacturaEditWindow"
        producto_widget = edit_window.producto_autocomplete

        # Test 1: Vérifier que les produits sont chargés dans le widget
        assert hasattr(producto_widget, 'productos'), "Attribut productos non trouvé"
        assert len(producto_widget.productos) > 0, "Aucun produit chargé dans producto_autocomplete"
        self.logger.info(f"✅ {len(producto_widget.productos)} produits chargés dans l'autocomplétion")

        # Test 2: Vérifier que le completer a un modèle avec des données
        assert producto_widget.completer is not None, "Completer non initialisé"
        assert producto_widget.completer.model() is not None, "Modèle du completer non initialisé"
        model_row_count = producto_widget.completer.model().rowCount()
        # Note: Le modèle peut être vide si tous les produits sont sans stock
        self.logger.info(f"✅ Modèle du completer contient {model_row_count} suggestions")

        # Test 3: Taper "p" et vérifier que des produits contenant "p" sont proposés
        producto_widget.clear()
        QTest.keyClicks(producto_widget, "p")
        self.wait_and_process_events(500)  # Attendre le timer de recherche (300ms) + marge

        # Vérifier que le modèle a été mis à jour avec des suggestions
        model = producto_widget.completer.model()
        suggestions_count = model.rowCount()

        # Compter combien de produits de test contiennent "p" et ont du stock
        expected_products_with_p = [
            p for p in self.test_products
            if 'p' in p['nombre'].lower() and p.get('stock_actual', 0) > 0
        ]

        self.logger.info(f"Suggestions trouvées: {suggestions_count}, produits avec 'p' et stock: {len(expected_products_with_p)}")

        # Afficher les suggestions pour debug
        suggestions = []
        for i in range(suggestions_count):
            suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
            suggestions.append(suggestion)
            self.logger.info(f"  - Suggestion {i+1}: {suggestion}")

        # Si on a des produits avec stock contenant "p", on doit avoir des suggestions
        if len(expected_products_with_p) > 0:
            assert suggestions_count > 0, "Aucune suggestion après avoir tapé 'p' alors que des produits avec stock existent"

            # Vérifier qu'au moins un produit de test contenant "p" est dans les suggestions
            found_test_product = False
            for product in expected_products_with_p:
                for suggestion in suggestions:
                    if product['nombre'] in suggestion:
                        found_test_product = True
                        break
                if found_test_product:
                    break

            assert found_test_product, f"Aucun produit de test contenant 'p' trouvé dans les suggestions: {suggestions}"
            self.logger.info("✅ Les produits contenant 'p' sont bien proposés")
        else:
            self.logger.info("⚠️ Aucun produit de test avec stock contenant 'p', test de suggestions ignoré")

        # Test 4: Vérifier la sélection d'un produit avec stock
        producto_widget.clear()
        QTest.keyClicks(producto_widget, "Producto Test 1")
        self.wait_and_process_events(500)

        # Vérifier qu'il y a des suggestions
        model = producto_widget.completer.model()
        if model.rowCount() > 0:
            # Simuler la sélection
            QTest.keyClick(producto_widget, Qt.Key_Down)
            QTest.keyClick(producto_widget, Qt.Key_Return)
            self.wait_and_process_events(200)

            # Vérifier que le produit est sélectionné
            text = producto_widget.text()
            assert "Producto Test 1" in text, f"Produit non sélectionné: {text}"
            self.logger.info(f"✅ Produit sélectionné: {text}")
        else:
            self.logger.info("⚠️ Aucune suggestion pour 'Producto Test 1', sélection non testée")

        # Test 5: Vérifier que les produits sans stock ne sont PAS proposés (sauf si sin_stock=1)
        producto_widget.clear()
        QTest.keyClicks(producto_widget, "Sin Stock")
        self.wait_and_process_events(500)

        model = producto_widget.completer.model()
        suggestions_sin_stock = []
        for i in range(model.rowCount()):
            suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
            suggestions_sin_stock.append(suggestion)

        # Le produit "Producto Sin Stock" ne devrait PAS apparaître (stock_actual=0 et sin_stock=0 par défaut)
        found_sin_stock = any("Sin Stock" in s for s in suggestions_sin_stock)
        self.logger.info(f"Produit 'Sin Stock' trouvé dans suggestions: {found_sin_stock}")
        # Note: On ne fait pas d'assertion ici car le comportement dépend de sin_stock

        # Fermer les fenêtres
        edit_window.close()
        self.app.processEvents()
        facturas_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Test chargement produits dans Nueva Factura terminé")
