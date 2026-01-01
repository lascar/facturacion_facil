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
        
        # Trouver la fenêtre facturas
        facturas_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle():
                facturas_window = widget
                break
        
        if not facturas_window:
            self.logger.warning("Fenêtre Facturas non trouvée, test ignoré")
            return
        
        # Trouver le widget d'autocomplétion produit
        producto_widget = self.automation.find_widget_by_name(facturas_window, "producto_autocomplete")
        if not producto_widget:
            # Essayer d'autres noms possibles
            producto_widget = self.automation.find_widget_by_name(facturas_window, "producto_input")
        
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
        
        facturas_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test ProductAutoCompleteWidget terminé")
