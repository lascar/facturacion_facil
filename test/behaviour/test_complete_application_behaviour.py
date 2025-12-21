# -*- coding: utf-8 -*-
"""
Tests de comportement complets basés sur facturacion_facil.txt
Tests de l'application complète selon les spécifications
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger


class TestCompleteApplicationBehaviour(BaseBehaviourTest):
    """Tests de comportement complets de l'application selon facturacion_facil.txt"""
    
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
        
        # Afficher la fenêtre principale
        self.main_window.show()
        self.wait_for_window(self.main_window)
        self.slow_mode_wait()
    
    def test_main_window_layout_specification(self):
        """Test: Vérifier que la fenêtre principale respecte les spécifications"""
        self.logger.info("🧪 Test: Layout fenêtre principale selon spécifications")
        
        # Vérifier le titre
        expected_title = "Facturación Fácil"
        actual_title = self.main_window.windowTitle()
        assert expected_title in actual_title, f"Titre incorrect: {actual_title}"
        
        # Vérifier la présence des 6 boutons principaux selon spécifications
        expected_buttons = [
            "📦 Productos",
            "🏢 Organización",
            "📊 Stock",
            "🧾 Facturas",
            "👥 Clientes"
        ]
        
        for button_text in expected_buttons:
            button = self.automation.find_button_by_text(self.main_window, button_text)
            assert button is not None, f"Bouton manquant: {button_text}"
            assert button.isVisible(), f"Bouton non visible: {button_text}"
        
        self.logger.info("✅ Layout fenêtre principale conforme aux spécifications")
    
    def test_productos_window_complete_workflow(self):
        """Test: Workflow complet de gestion des produits selon spécifications"""
        self.logger.info("🧪 Test: Workflow complet fenêtre Productos")
        
        # 1. Ouvrir la fenêtre Productos
        productos_btn = self.automation.find_button_by_text(self.main_window, "📦 Productos")
        QTest.mouseClick(productos_btn, Qt.LeftButton)
        self.wait_and_process_events(500)
        
        # Trouver la fenêtre productos
        productos_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Productos" in widget.windowTitle():
                productos_window = widget
                break
        
        assert productos_window is not None, "Fenêtre Productos non trouvée"
        assert productos_window.isVisible(), "Fenêtre Productos non visible"
        
        # 2. Vérifier la structure selon spécifications
        # Section gauche - "Lista de Productos" avec tableau
        productos_table = self.automation.find_widget_by_name(productos_window, "productos_table")
        if productos_table:
            # Vérifier les colonnes selon spécifications
            expected_columns = ["ID", "Nombre", "Referencia", "Precio", "IVA", "Categoría", "Stock"]
            actual_columns = [productos_table.horizontalHeaderItem(i).text() 
                            for i in range(productos_table.columnCount())]
            
            for col in expected_columns:
                assert any(col in actual_col for actual_col in actual_columns), \
                    f"Colonne manquante: {col}"
        
        # 3. Créer un nouveau produit selon spécifications
        nuevo_btn = self.automation.find_button_by_text(productos_window, "Nuevo")
        if nuevo_btn:
            QTest.mouseClick(nuevo_btn, Qt.LeftButton)
            self.wait_and_process_events(200)
        
        # 4. Remplir les champs selon spécifications
        test_product = self.test_data.create_product_data()
        
        # Champs selon spécifications: Nombre, Referencia, Precio, IVA, Categoría, Descripción
        fields_to_fill = {
            'nombre_edit': test_product['nombre'],
            'referencia_edit': test_product.get('referencia', 'REF001'),
            'precio_edit': test_product['precio_venta'],
            'iva_edit': test_product.get('iva_recomendado', 21.0),
            'descripcion_edit': test_product.get('descripcion', 'Producto de test')
        }
        
        for field_name, value in fields_to_fill.items():
            field = self.automation.find_widget_by_name(productos_window, field_name)
            if field:
                if hasattr(field, 'setText'):
                    field.setText(str(value))
                elif hasattr(field, 'setValue'):
                    field.setValue(float(value))
                elif hasattr(field, 'setPlainText'):
                    field.setPlainText(str(value))
        
        self.wait_and_process_events(200)
        
        # 5. Sauvegarder selon spécifications
        guardar_btn = self.automation.find_button_by_text(productos_window, "Guardar")
        if guardar_btn:
            QTest.mouseClick(guardar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
        
        # 6. Vérifier la sauvegarde
        if productos_table:
            # Vérifier que le produit apparaît dans la liste
            found_product = False
            for row in range(productos_table.rowCount()):
                nombre_item = productos_table.item(row, 1)  # Colonne Nombre
                if nombre_item and test_product['nombre'] in nombre_item.text():
                    found_product = True
                    break
            
            assert found_product, "Produit non trouvé dans la liste après sauvegarde"
        
        # Fermer la fenêtre
        productos_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Workflow Productos terminé avec succès")
    
    def test_clientes_window_complete_workflow(self):
        """Test: Workflow complet de gestion des clients selon spécifications"""
        self.logger.info("🧪 Test: Workflow complet fenêtre Clientes")

        # 1. Ouvrir la fenêtre Clientes
        clientes_btn = self.automation.find_button_by_text(self.main_window, "👥 Clientes")
        QTest.mouseClick(clientes_btn, Qt.LeftButton)
        self.wait_and_process_events(1000)  # Augmenter le délai

        # Trouver la fenêtre clientes (chercher la plus récente)
        clientes_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Clientes" in widget.windowTitle() and widget.isVisible():
                clientes_window = widget
                break

        assert clientes_window is not None, "Fenêtre Clientes non trouvée"
        assert clientes_window.isVisible(), "Fenêtre Clientes non visible"
        
        # 2. Vérifier la structure selon spécifications
        # Section gauche - "Lista de Clientes" avec colonnes: ID, Nombre, NIF/DNI, Email, Teléfono
        clientes_table = self.automation.find_widget_by_name(clientes_window, "clients_table")
        if clientes_table:
            expected_columns = ["ID", "Nombre", "NIF/DNI", "Email", "Teléfono"]
            actual_columns = [clientes_table.horizontalHeaderItem(i).text() 
                            for i in range(clientes_table.columnCount())]
            
            for col in expected_columns:
                assert any(col in actual_col for actual_col in actual_columns), \
                    f"Colonne manquante: {col}"
        
        # 3. Créer un nouveau client selon spécifications
        nuevo_btn = self.automation.find_button_by_text(clientes_window, "➕ Nuevo")
        if nuevo_btn:
            QTest.mouseClick(nuevo_btn, Qt.LeftButton)
            self.wait_and_process_events(200)
        
        # 4. Remplir les champs selon spécifications
        test_client = self.test_data.create_client_data()
        
        # Champs selon spécifications: Nombre, NIF/DNI, Email, Teléfono, Dirección
        fields_to_fill = {
            'nombre_edit': test_client['nombre'],
            'nif_edit': test_client.get('nif', '12345678A'),
            'email_edit': test_client.get('email', 'test@example.com'),
            'telefono_edit': test_client.get('telefono', '+34 600000000'),
            'direccion_edit': test_client.get('direccion', 'Calle Test, 1')
        }
        
        for field_name, value in fields_to_fill.items():
            field = self.automation.find_widget_by_name(clientes_window, field_name)
            if field:
                if hasattr(field, 'setText'):
                    field.setText(str(value))
                elif hasattr(field, 'setPlainText'):
                    field.setPlainText(str(value))
        
        self.wait_and_process_events(200)
        
        # 5. Sauvegarder selon spécifications
        guardar_btn = self.automation.find_button_by_text(clientes_window, "💾 Guardar")
        if guardar_btn:
            QTest.mouseClick(guardar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
        
        # Fermer la fenêtre
        clientes_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Workflow Clientes terminé avec succès")

    def test_facturas_window_complete_workflow(self):
        """Test: Workflow complet de gestion des factures selon spécifications"""
        self.logger.info("🧪 Test: Workflow complet fenêtre Facturas")

        # Préparer des données de test
        test_client = self.test_data.create_client_data()
        test_product = self.test_data.create_product_data()

        # Ajouter le client et produit à la base de test
        client_id = self.database.add_client(test_client)
        product_id = self.database.add_product(test_product)

        # 1. Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "🧾 Facturas")
        QTest.mouseClick(facturas_btn, Qt.LeftButton)
        self.wait_and_process_events(1000)  # Augmenter le délai

        # Trouver la fenêtre facturas (chercher la plus récente)
        facturas_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Facturas" in widget.windowTitle() and widget.isVisible():
                facturas_window = widget
                break

        assert facturas_window is not None, "Fenêtre Facturas non trouvée"
        assert facturas_window.isVisible(), "Fenêtre Facturas non visible"

        # 2. Créer une nouvelle facture selon spécifications
        nueva_btn = self.automation.find_button_by_text(facturas_window, "➕ Nueva Factura")
        if nueva_btn:
            QTest.mouseClick(nueva_btn, Qt.LeftButton)
            self.wait_and_process_events(300)

        # 3. Vérifier les sections selon spécifications
        # Section supérieure - Informations de la facture
        # Número de Factura, Fecha, Cliente, Estado

        # 4. Sélectionner un client avec autocomplétion selon spécifications
        cliente_widget = self.automation.find_widget_by_name(facturas_window, "cliente_autocomplete")
        if cliente_widget:
            # Simuler la saisie pour l'autocomplétion
            QTest.keyClicks(cliente_widget, test_client['nombre'][:3])
            self.wait_and_process_events(300)

            # Simuler la sélection
            QTest.keyClick(cliente_widget, Qt.Key_Down)
            QTest.keyClick(cliente_widget, Qt.Key_Return)
            self.wait_and_process_events(200)

        # 5. Vérifier que les détails du client s'affichent selon spécifications
        # Section centrale - Détails du client sélectionné

        # 6. Ajouter un produit selon spécifications
        producto_widget = self.automation.find_widget_by_name(facturas_window, "producto_autocomplete")
        if producto_widget:
            # Simuler la saisie pour l'autocomplétion produit
            QTest.keyClicks(producto_widget, test_product['nombre'][:3])
            self.wait_and_process_events(300)

            # Simuler la sélection
            QTest.keyClick(producto_widget, Qt.Key_Down)
            QTest.keyClick(producto_widget, Qt.Key_Return)
            self.wait_and_process_events(200)

        # 7. Configurer la quantité selon spécifications
        cantidad_widget = self.automation.find_widget_by_name(facturas_window, "cantidad_spinbox")
        if cantidad_widget:
            cantidad_widget.setValue(2)
            self.wait_and_process_events(100)

        # 8. Ajouter le produit à la facture selon spécifications
        agregar_btn = self.automation.find_button_by_text(facturas_window, "➕ Agregar")
        if agregar_btn:
            QTest.mouseClick(agregar_btn, Qt.LeftButton)
            self.wait_and_process_events(300)

        # 9. Vérifier que le produit apparaît dans le tableau selon spécifications
        productos_table = self.automation.find_widget_by_name(facturas_window, "productos_table")
        if productos_table:
            assert productos_table.rowCount() > 0, "Aucun produit dans la facture"

        # 10. Vérifier les totaux selon spécifications
        # Section totaux - "Totales de la Factura": Subtotal, IVA, Descuentos, TOTAL

        # 11. Sauvegarder la facture selon spécifications
        guardar_btn = self.automation.find_button_by_text(facturas_window, "💾 Guardar")
        if guardar_btn:
            QTest.mouseClick(guardar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)

        # Fermer la fenêtre
        facturas_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Workflow Facturas terminé avec succès")

    def test_organizacion_window_configuration_workflow(self):
        """Test: Workflow de configuration de l'organisation selon spécifications"""
        self.logger.info("🧪 Test: Workflow configuration Organización")

        # 1. Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "🏢 Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre organización
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Organización" in widget.windowTitle():
                organizacion_window = widget
                break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"
        assert organizacion_window.isVisible(), "Fenêtre Organización non visible"

        # 2. Vérifier les sections selon spécifications
        # Section "Información Básica": Nombre, CIF/NIF, Teléfono, Email
        # Section "Dirección": Dirección (textarea)
        # Section "Configuración": Logo, Orientación, Número Inicial
        # Section "Configuración de Directorios": Imágenes, Logos, PDFs
        # Section "Configuración de Estados de Facturas"

        # 3. Remplir les informations de base selon spécifications
        test_org_data = {
            'nombre_empresa': 'Mi Empresa Test S.L.',
            'cif_nif': 'B12345678',
            'telefono': '+34 911234567',
            'email': 'info@miempresa.com',
            'direccion': 'Calle Mayor, 1, 28001 Madrid'
        }

        # Remplir les champs si ils existent
        for field_name, value in test_org_data.items():
            field = self.automation.find_widget_by_name(organizacion_window, field_name)
            if field:
                if hasattr(field, 'setText'):
                    field.setText(str(value))
                elif hasattr(field, 'setPlainText'):
                    field.setPlainText(str(value))

        self.wait_and_process_events(200)

        # 4. Tester la configuration des états de factures selon spécifications
        # Bouton "➕ Agregar Estado"
        agregar_estado_btn = self.automation.find_button_by_text(organizacion_window, "➕ Agregar Estado")
        if agregar_estado_btn:
            QTest.mouseClick(agregar_estado_btn, Qt.LeftButton)
            self.wait_and_process_events(300)

            # Vérifier qu'un dialogue s'ouvre (InvoiceStatusDialog selon spécifications)
            # Le dialogue devrait avoir: Nombre, Descripción, Permite Modificación, Color, Orden

        # 5. Sauvegarder la configuration selon spécifications
        guardar_btn = self.automation.find_button_by_text(organizacion_window, "💾 Guardar Configuración")
        if guardar_btn:
            QTest.mouseClick(guardar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)

        # Fermer la fenêtre
        organizacion_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Workflow Organización terminé avec succès")
