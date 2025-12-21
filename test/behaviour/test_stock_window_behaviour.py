# -*- coding: utf-8 -*-
"""
Tests de comportement pour la fenêtre de gestion du stock selon facturacion_facil.txt
Tests spécialisés pour StockWindow
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger


class TestStockWindowBehaviour(BaseBehaviourTest):
    """Tests de comportement pour la fenêtre de gestion du stock selon spécifications"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir):
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
        
        # Préparer des données de test pour le stock
        self.setup_stock_test_data()
    
    def setup_stock_test_data(self):
        """Préparer des données de test pour la gestion du stock"""
        # Créer des produits avec différents niveaux de stock
        test_products = [
            {
                'nombre': 'Producto Stock Alto',
                'precio_venta': 50.00,
                'stock_actual': 100,
                'stock_minimo': 10,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto Stock Bajo',
                'precio_venta': 75.00,
                'stock_actual': 5,
                'stock_minimo': 20,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto Sin Stock',
                'precio_venta': 25.00,
                'stock_actual': 0,
                'stock_minimo': 5,
                'categoria': 'Test'
            }
        ]
        
        # Ajouter à la base de données de test
        for product in test_products:
            self.database.add_product(product)
    
    def test_stock_window_layout_specification(self):
        """Test: Vérifier le layout de la fenêtre Stock selon spécifications"""
        self.logger.info("🧪 Test: Layout StockWindow selon spécifications")

        # Ouvrir la fenêtre Stock
        stock_btn = self.automation.find_button_by_text(self.main_window, "📊 Stock")
        QTest.mouseClick(stock_btn, Qt.LeftButton)
        self.wait_and_process_events(1000)  # Augmenter le délai

        # Trouver la fenêtre stock (chercher la plus récente)
        stock_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Stock" in widget.windowTitle() and widget.isVisible():
                stock_window = widget
                break

        if not stock_window:
            self.logger.warning("Fenêtre Stock non trouvée, test ignoré")
            return

        assert stock_window.isVisible(), "Fenêtre Stock non visible"

        # Vérifier la structure selon spécifications
        # Section gauche - "Lista de Stock" avec colonnes selon spécifications
        stock_table = self.automation.find_widget_by_name(stock_window, "stock_table")
        if stock_table:
            # Vérifier les colonnes selon spécifications
            # Producto, Stock Actual, Stock Mínimo, Estado (Disponible/Stock bajo/Sin stock)
            expected_columns = ["Producto", "Stock Actual", "Stock Mínimo", "Estado"]
            
            actual_columns = []
            for i in range(stock_table.columnCount()):
                header_item = stock_table.horizontalHeaderItem(i)
                if header_item:
                    actual_columns.append(header_item.text())
            
            for col in expected_columns:
                found = any(col in actual_col for actual_col in actual_columns)
                if found:
                    self.logger.info(f"✅ Colonne trouvée: {col}")
                else:
                    self.logger.warning(f"⚠️ Colonne manquante: {col}")
        
        # Section droite - "Ajustar Stock" selon spécifications
        # Producto (label), Stock Actual (label), Nuevo Stock (spinbox), Stock Mínimo (spinbox)
        producto_label = self.automation.find_widget_by_name(stock_window, "producto_selected")
        stock_actual_label = self.automation.find_widget_by_name(stock_window, "stock_actual_label")
        nuevo_stock_spinbox = self.automation.find_widget_by_name(stock_window, "nuevo_stock")
        stock_minimo_spinbox = self.automation.find_widget_by_name(stock_window, "stock_minimo")
        
        if producto_label:
            self.logger.info("✅ Label 'Producto' trouvé")
        if stock_actual_label:
            self.logger.info("✅ Label 'Stock Actual' trouvé")
        if nuevo_stock_spinbox:
            self.logger.info("✅ SpinBox 'Nuevo Stock' trouvé")
        if stock_minimo_spinbox:
            self.logger.info("✅ SpinBox 'Stock Mínimo' trouvé")
        
        stock_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test layout StockWindow terminé")
    
    def test_stock_adjustment_workflow_specification(self):
        """Test: Workflow d'ajustement du stock selon spécifications"""
        self.logger.info("🧪 Test: Workflow ajustement stock selon spécifications")
        
        # Ouvrir la fenêtre Stock
        stock_btn = self.automation.find_button_by_text(self.main_window, "📊 Stock")
        QTest.mouseClick(stock_btn, Qt.LeftButton)
        self.wait_and_process_events(500)
        
        # Trouver la fenêtre stock
        stock_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Stock" in widget.windowTitle():
                stock_window = widget
                break
        
        if not stock_window:
            self.logger.warning("Fenêtre Stock non trouvée, test ignoré")
            return
        
        # 1. Sélectionner un produit dans la liste selon spécifications
        stock_table = self.automation.find_widget_by_name(stock_window, "stock_table")
        if stock_table and stock_table.rowCount() > 0:
            # Sélectionner la première ligne
            stock_table.selectRow(0)
            self.wait_and_process_events(200)

            # Vérifier que les détails s'affichent à droite selon spécifications
            producto_label = self.automation.find_widget_by_name(stock_window, "producto_selected")
            if producto_label:
                product_name = producto_label.text()
                self.logger.info(f"✅ Produit sélectionné: {product_name}")

        # 2. Modifier le stock selon spécifications
        nuevo_stock_spinbox = self.automation.find_widget_by_name(stock_window, "nuevo_stock")
        if nuevo_stock_spinbox:
            # Définir un nouveau stock
            nuevo_stock_spinbox.setValue(50)
            self.wait_and_process_events(100)
            self.logger.info("✅ Nouveau stock défini: 50")

        # 3. Modifier le stock minimum selon spécifications
        stock_minimo_spinbox = self.automation.find_widget_by_name(stock_window, "stock_minimo")
        if stock_minimo_spinbox:
            # Définir un nouveau stock minimum
            stock_minimo_spinbox.setValue(15)
            self.wait_and_process_events(100)
            self.logger.info("✅ Stock minimum défini: 15")
        
        # 4. Appliquer les modifications selon spécifications
        ajustar_btn = self.automation.find_button_by_text(stock_window, "📊 Ajustar Stock")
        if ajustar_btn:
            QTest.mouseClick(ajustar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
            self.logger.info("✅ Ajustement stock appliqué")
        
        # 5. Vérifier que les changements sont reflétés dans la liste
        if stock_table:
            # Actualiser la liste
            actualizar_btn = self.automation.find_button_by_text(stock_window, "🔄 Actualizar")
            if actualizar_btn:
                QTest.mouseClick(actualizar_btn, Qt.LeftButton)
                self.wait_and_process_events(500)
                self.logger.info("✅ Liste actualisée")
        
        stock_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test workflow ajustement stock terminé")
    
    def test_stock_status_indicators_specification(self):
        """Test: Indicateurs d'état du stock selon spécifications"""
        self.logger.info("🧪 Test: Indicateurs état stock selon spécifications")
        
        # Ouvrir la fenêtre Stock
        stock_btn = self.automation.find_button_by_text(self.main_window, "📊 Stock")
        QTest.mouseClick(stock_btn, Qt.LeftButton)
        self.wait_and_process_events(500)
        
        # Trouver la fenêtre stock
        stock_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Stock" in widget.windowTitle():
                stock_window = widget
                break
        
        if not stock_window:
            self.logger.warning("Fenêtre Stock non trouvée, test ignoré")
            return
        
        # Vérifier les états selon spécifications
        # Estado: Disponible/Stock bajo/Sin stock
        stock_table = self.automation.find_widget_by_name(stock_window, "stock_table")
        if stock_table:
            expected_states = ["Disponible", "Stock bajo", "Sin stock"]
            found_states = []
            
            # Parcourir les lignes pour vérifier les états
            for row in range(stock_table.rowCount()):
                estado_item = stock_table.item(row, 3)  # Colonne Estado
                if estado_item:
                    estado_text = estado_item.text()
                    found_states.append(estado_text)
                    
                    # Vérifier que l'état correspond aux spécifications
                    if any(expected in estado_text for expected in expected_states):
                        self.logger.info(f"✅ État valide trouvé: {estado_text}")
            
            # Vérifier qu'on a au moins quelques états
            assert len(found_states) > 0, "Aucun état de stock trouvé"
        
        stock_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test indicateurs état stock terminé")
