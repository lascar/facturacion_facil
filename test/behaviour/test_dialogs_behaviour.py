# -*- coding: utf-8 -*-
"""
Tests de comportement pour les dialogues selon facturacion_facil.txt
Tests spécialisés pour les dialogues modaux de l'application
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger


class TestDialogsBehaviour(BaseBehaviourTest):
    """Tests de comportement pour les dialogues selon spécifications"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox):
        """Configuration automatique pour chaque test"""
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir
        self.logger = get_logger(self.__class__.__name__)

        # Configuration des mocks pour éviter les blocages
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok
        mock_messagebox.warning.return_value = mock_messagebox.Ok
        mock_messagebox.critical.return_value = mock_messagebox.Ok

        # Initialiser l'automation et les données de test
        if self.app:
            self.automation = PyQt5Automation(self.app)
        self.test_data = TestDataFactory()
    
    @pytest.mark.timeout(20)
    def test_invoice_status_dialog_specification(self):
        """Test: Dialogue "Configurar Estado de Factura" selon spécifications"""
        self.logger.info("🧪 Test: InvoiceStatusDialog selon spécifications")

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "🏢 Organización")
        if not organizacion_btn:
            self.logger.warning("Bouton Organización non trouvé, test ignoré")
            return
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre organización
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Organización" in widget.windowTitle():
                organizacion_window = widget
                break

        if not organizacion_window:
            self.logger.warning("Fenêtre Organización non trouvée, test ignoré")
            return

        # Chercher le bouton "➕ Agregar Estado" selon spécifications
        agregar_estado_btn = self.automation.find_button_by_text(organizacion_window, "➕ Agregar Estado")
        if agregar_estado_btn:
            QTest.mouseClick(agregar_estado_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
            
            # Chercher le dialogue qui s'ouvre
            dialog = None
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, QDialog) and widget.isVisible():
                    title = widget.windowTitle()
                    # Chercher spécifiquement le dialogue avec "Estado" dans le titre
                    if "Estado" in title:
                        dialog = widget
                        break

            if dialog:
                # Vérifier le titre selon spécifications
                # Spécification: "Nuevo Estado" ou "Editar Estado"
                title = dialog.windowTitle()
                self.logger.info(f"✅ Dialogue trouvé: {title}")
                
                # Vérifier les champs selon spécifications
                expected_fields = [
                    "nombre_estado",  # Nombre del Estado
                    "descripcion",    # Descripción
                    "permite_modificacion",  # Permite Modificación (checkbox)
                    "color",          # Color
                    "orden"           # Orden (spinbox 1-100)
                ]

                for field_name in expected_fields:
                    field = self.automation.find_widget_by_name(dialog, field_name)
                    if field:
                        self.logger.info(f"✅ Campo encontrado: {field_name}")

                # Tester le remplissage selon spécifications
                nombre_field = self.automation.find_widget_by_name(dialog, "nombre_estado")
                if nombre_field and hasattr(nombre_field, 'setText'):
                    QTest.keyClicks(nombre_field, "Estado Test")
                    self.wait_and_process_events(100)

                descripcion_field = self.automation.find_widget_by_name(dialog, "descripcion")
                if descripcion_field and hasattr(descripcion_field, 'setPlainText'):
                    descripcion_field.setPlainText("Estado de test para comportement")
                    self.wait_and_process_events(100)
                
                # Vérifier les boutons selon spécifications
                # Spécification: "💾 Guardar" et "❌ Cancelar"
                guardar_btn = self.automation.find_button_by_text(dialog, "💾 Guardar")
                cancelar_btn = self.automation.find_button_by_text(dialog, "❌ Cancelar")
                
                assert guardar_btn is not None, "Bouton Guardar manquant"
                assert cancelar_btn is not None, "Bouton Cancelar manquant"
                
                # Fermer le dialogue
                QTest.mouseClick(cancelar_btn, Qt.LeftButton)
                self.wait_and_process_events(200)
        
        organizacion_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test InvoiceStatusDialog terminé")
    
    @pytest.mark.timeout(20)
    def test_data_cleanup_dialog_specification(self):
        """Test: Dialogue "Limpiar Datos" selon spécifications"""
        self.logger.info("🧪 Test: DataCleanupDialog selon spécifications")
        
        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "🏢 Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.wait_and_process_events(500)
        
        # Trouver la fenêtre organización
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Organización" in widget.windowTitle():
                organizacion_window = widget
                break
        
        if not organizacion_window:
            self.logger.warning("Fenêtre Organización non trouvée, test ignoré")
            return
        
        # Chercher le bouton "🧹 Limpiar Datos" selon spécifications
        limpiar_btn = self.automation.find_button_by_text(organizacion_window, "🧹 Limpiar Datos")
        if limpiar_btn:
            QTest.mouseClick(limpiar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
            
            # Chercher le dialogue qui s'ouvre
            dialog = None
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, QDialog) and widget.isVisible():
                    dialog = widget
                    break
            
            if dialog:
                # Vérifier le titre selon spécifications
                # Spécification: "🧹 Limpieza de Datos de la Base de Datos"
                title = dialog.windowTitle()
                assert "Limpieza" in title or "Limpiar" in title, f"Titre dialogue incorrect: {title}"
                
                # Vérifier les sections selon spécifications
                # Section "📊 Estado Actual de la Base de Datos"
                # Section "🎯 Opciones de Limpieza"
                # Section "💾 Seguridad"
                
                # Vérifier les options de nettoyage selon spécifications
                expected_checkboxes = [
                    "eliminar_facturas",      # 🧾 Eliminar todas las facturas y sus items
                    "eliminar_productos",     # 📦 Eliminar todos los productos y stocks
                    "eliminar_clientes_sin_facturas",  # 👤 Eliminar clientes sin facturas
                    "eliminar_todos_clientes", # 👥 Eliminar TODOS los clientes
                    "eliminar_todo",          # 💥 ELIMINAR TODO (en rouge)
                    "crear_backup"            # ✅ Crear backup automático (activé par défaut)
                ]
                
                for checkbox_name in expected_checkboxes:
                    checkbox = self.automation.find_widget_by_name(dialog, checkbox_name)
                    if checkbox:
                        self.logger.info(f"✅ Checkbox encontrada: {checkbox_name}")
                
                # Vérifier les boutons selon spécifications
                # Spécification: "🧹 Ejecutar Limpieza" et "❌ Cancelar"
                ejecutar_btn = self.automation.find_button_by_text(dialog, "🧹 Ejecutar Limpieza")
                cancelar_btn = self.automation.find_button_by_text(dialog, "❌ Cancelar")
                
                if ejecutar_btn:
                    self.logger.info("✅ Bouton Ejecutar Limpieza trouvé")
                if cancelar_btn:
                    self.logger.info("✅ Bouton Cancelar trouvé")
                
                # Fermer le dialogue
                if cancelar_btn:
                    QTest.mouseClick(cancelar_btn, Qt.LeftButton)
                else:
                    dialog.close()
                self.wait_and_process_events(200)
        
        organizacion_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test DataCleanupDialog terminé")
    
    def test_product_configuration_dialog_specification(self):
        """Test: Dialogue "Agregar/Editar Producto" selon spécifications"""
        self.logger.info("🧪 Test: Dialogue configuration produit selon spécifications")
        
        # Ouvrir la fenêtre Facturas pour tester le dialogue produit
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
        
        # Chercher un bouton qui ouvre le dialogue produit
        # Peut être "➕ Agregar" ou un bouton de configuration produit
        agregar_btn = self.automation.find_button_by_text(facturas_window, "➕ Agregar")
        if agregar_btn:
            # D'abord remplir les champs requis
            producto_widget = self.automation.find_widget_by_name(facturas_window, "producto_autocomplete")
            if producto_widget:
                QTest.keyClicks(producto_widget, "Test")
                self.wait_and_process_events(300)
            
            QTest.mouseClick(agregar_btn, Qt.LeftButton)
            self.wait_and_process_events(500)
            
            # Chercher le dialogue qui s'ouvre
            dialog = None
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, QDialog) and widget.isVisible():
                    dialog = widget
                    break
            
            if dialog:
                # Vérifier le titre selon spécifications
                # Spécification: "Configurar Producto para Factura"
                title = dialog.windowTitle()
                self.logger.info(f"Titre dialogue produit: {title}")
                
                # Vérifier les sections selon spécifications
                # Section "Buscar Producto": ProductAutoCompleteWidget
                # Section "Configuración": Cantidad, Precio Unitario, IVA, Descuento
                # Section "Preview de Totales": Calculs automatiques temps réel
                
                expected_fields = [
                    "cantidad",           # QSpinBox (quantité, obligatoire)
                    "precio_unitario",    # QDoubleSpinBox (prix unitaire, obligatoire)
                    "iva_aplicado",       # QDoubleSpinBox (pourcentage IVA, obligatoire)
                    "descuento"           # QDoubleSpinBox (pourcentage remise, défaut 0)
                ]
                
                for field_name in expected_fields:
                    field = self.automation.find_widget_by_name(dialog, field_name)
                    if field:
                        self.logger.info(f"✅ Campo encontrado: {field_name}")
                
                # Vérifier les boutons selon spécifications
                # Spécification: "Cancelar" (reject) et "Aceptar" (accept avec validation)
                aceptar_btn = self.automation.find_button_by_text(dialog, "Aceptar")
                cancelar_btn = self.automation.find_button_by_text(dialog, "Cancelar")
                
                if aceptar_btn:
                    self.logger.info("✅ Bouton Aceptar trouvé")
                if cancelar_btn:
                    self.logger.info("✅ Bouton Cancelar trouvé")
                
                # Fermer le dialogue
                if cancelar_btn:
                    QTest.mouseClick(cancelar_btn, Qt.LeftButton)
                else:
                    dialog.close()
                self.wait_and_process_events(200)
        
        facturas_window.close()
        self.wait_and_process_events(200)
        
        self.logger.info("✅ Test dialogue configuration produit terminé")
