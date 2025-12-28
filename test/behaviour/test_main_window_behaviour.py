# -*- coding: utf-8 -*-
"""
Tests de comportement pour la fenêtre principale
"""

import pytest
import time
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation

class TestMainWindowBehaviour(BaseBehaviourTest):
    """Tests de comportement pour MainWindowPyQt5"""

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
        self.slow_mode_wait()
    
    def test_main_window_startup(self):
        """Test du démarrage de la fenêtre principale"""
        self.logger.info("🧪 Test: Démarrage de la fenêtre principale")
        
        # Vérifier que la fenêtre principale est visible
        self.assert_window_visible(self.main_window, "MainWindow")
        
        # Vérifier le titre de la fenêtre
        expected_title = "Facturación Fácil - PyQt5"
        actual_title = self.main_window.windowTitle()
        assert expected_title in actual_title, f"Titre attendu: {expected_title}, obtenu: {actual_title}"
        
        # Prendre une capture d'écran
        self.take_screenshot("main_window_startup")
        
        self.logger.info("✅ Test démarrage réussi")
    
    def test_main_window_buttons_present(self):
        """Test de la présence des boutons principaux"""
        self.logger.info("🧪 Test: Présence des boutons principaux")
        
        # Liste des boutons attendus (texte partiel)
        expected_buttons = [
            "Productos",
            "Organización",
            "Stock",
            "Facturas",
            "Clientes"
        ]
        
        # Vérifier la présence de chaque bouton
        for button_text in expected_buttons:
            button = self.automation.find_button_by_text(self.main_window, button_text)
            assert button is not None, f"Bouton '{button_text}' non trouvé"
            self.assert_button_enabled(button, button_text)
            self.logger.info(f"✅ Bouton '{button_text}' présent et activé")
        
        self.take_screenshot("main_window_buttons")
        self.logger.info("✅ Test boutons principaux réussi")
    
    def test_open_productos_window(self):
        """Test d'ouverture de la fenêtre Productos"""
        self.logger.info("🧪 Test: Ouverture fenêtre Productos")
        
        # Trouver et cliquer sur le bouton Productos
        productos_btn = self.automation.find_button_by_text(self.main_window, "Productos")
        assert productos_btn is not None, "Bouton Productos non trouvé"
        
        # Cliquer sur le bouton
        success = self.automation.click_button_safe(productos_btn, wait_after=0.2)
        assert success, "Échec du clic sur le bouton Productos"
        
        # Vérifier que la fenêtre Productos s'ouvre
        productos_window = self.main_window.productos_window
        assert productos_window is not None, "Fenêtre Productos non créée"
        
        # Attendre que la fenêtre soit visible
        assert self.wait_for_window(productos_window, timeout=1), "Fenêtre Productos non visible"
        
        self.take_screenshot("productos_window_opened")
        self.logger.info("✅ Test ouverture Productos réussi")
    
    def test_open_clientes_window(self):
        """Test d'ouverture de la fenêtre Clientes"""
        self.logger.info("🧪 Test: Ouverture fenêtre Clientes")
        
        # Trouver et cliquer sur le bouton Clientes
        clientes_btn = self.automation.find_button_by_text(self.main_window, "Clientes")
        assert clientes_btn is not None, "Bouton Clientes non trouvé"
        
        # Cliquer sur le bouton
        success = self.automation.click_button_safe(clientes_btn, wait_after=0.2)
        assert success, "Échec du clic sur le bouton Clientes"
        
        # Vérifier que la fenêtre Clientes s'ouvre
        clientes_window = self.main_window.clientes_window
        assert clientes_window is not None, "Fenêtre Clientes non créée"
        
        # Attendre que la fenêtre soit visible
        assert self.wait_for_window(clientes_window, timeout=1), "Fenêtre Clientes non visible"
        
        self.take_screenshot("clientes_window_opened")
        self.logger.info("✅ Test ouverture Clientes réussi")
    
    def test_open_facturas_window(self):
        """Test d'ouverture de la fenêtre Facturas"""
        self.logger.info("🧪 Test: Ouverture fenêtre Facturas")
        
        # Trouver et cliquer sur le bouton Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "Facturas")
        assert facturas_btn is not None, "Bouton Facturas non trouvé"
        
        # Cliquer sur le bouton
        success = self.automation.click_button_safe(facturas_btn, wait_after=0.2)
        assert success, "Échec du clic sur le bouton Facturas"
        
        # Vérifier que la fenêtre Facturas s'ouvre
        facturas_window = self.main_window.facturas_window
        assert facturas_window is not None, "Fenêtre Facturas non créée"
        
        # Attendre que la fenêtre soit visible
        assert self.wait_for_window(facturas_window, timeout=1), "Fenêtre Facturas non visible"
        
        self.take_screenshot("facturas_window_opened")
        self.logger.info("✅ Test ouverture Facturas réussi")
    
    def test_open_organizacion_window(self):
        """Test d'ouverture de la fenêtre Organización"""
        self.logger.info("🧪 Test: Ouverture fenêtre Organización")
        
        # Trouver et cliquer sur le bouton Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        assert organizacion_btn is not None, "Bouton Organización non trouvé"
        
        # Cliquer sur le bouton
        success = self.automation.click_button_safe(organizacion_btn, wait_after=0.2)
        assert success, "Échec du clic sur le bouton Organización"
        
        # Vérifier que la fenêtre Organización s'ouvre
        organizacion_window = self.main_window.organizacion_window
        assert organizacion_window is not None, "Fenêtre Organización non créée"
        
        # Attendre que la fenêtre soit visible
        assert self.wait_for_window(organizacion_window, timeout=1), "Fenêtre Organización non visible"
        
        self.take_screenshot("organizacion_window_opened")
        self.logger.info("✅ Test ouverture Organización réussi")
    
    def test_open_stock_window(self):
        """Test d'ouverture de la fenêtre Stock"""
        self.logger.info("🧪 Test: Ouverture fenêtre Stock")
        
        # Trouver et cliquer sur le bouton Stock
        stock_btn = self.automation.find_button_by_text(self.main_window, "Stock")
        assert stock_btn is not None, "Bouton Stock non trouvé"
        
        # Cliquer sur le bouton
        success = self.automation.click_button_safe(stock_btn, wait_after=0.2)
        assert success, "Échec du clic sur le bouton Stock"
        
        # Vérifier que la fenêtre Stock s'ouvre
        stock_window = self.main_window.stock_window
        assert stock_window is not None, "Fenêtre Stock non créée"
        
        # Attendre que la fenêtre soit visible
        assert self.wait_for_window(stock_window, timeout=1), "Fenêtre Stock non visible"
        
        self.take_screenshot("stock_window_opened")
        self.logger.info("✅ Test ouverture Stock réussi")
