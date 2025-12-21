# -*- coding: utf-8 -*-
"""
Utilitaires pour l'automatisation des interfaces PyQt5 avec QTest
Remplace Selenium pour les tests de comportement PyQt5
"""

import time
from PyQt5.QtWidgets import (
    QPushButton, QLineEdit, QComboBox, QTableWidget,
    QSpinBox, QDoubleSpinBox, QTextEdit, QDateEdit, QDialog, QMainWindow
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QKeySequence

from utils.logger import get_logger

class PyQt5Automation:
    """Classe utilitaire pour automatiser les interactions PyQt5 avec QTest"""

    def __init__(self, app):
        self.app = app
        self.logger = get_logger(self.__class__.__name__)
        self.default_wait = 100  # ms pour QTest.qWait()
    
    def find_button_by_text(self, parent, text):
        """Trouver un bouton par son texte"""
        try:
            buttons = parent.findChildren(QPushButton)
            for button in buttons:
                if text.lower() in button.text().lower():
                    return button
            return None
        except Exception as e:
            self.logger.error(f"Erreur recherche bouton '{text}': {e}")
            return None
    
    def find_input_by_name(self, parent, object_name):
        """Trouver un champ de saisie par son nom d'objet"""
        try:
            return parent.findChild(QLineEdit, object_name)
        except Exception as e:
            self.logger.error(f"Erreur recherche input '{object_name}': {e}")
            return None
    
    def find_combobox_by_name(self, parent, object_name):
        """Trouver une combobox par son nom d'objet"""
        try:
            return parent.findChild(QComboBox, object_name)
        except Exception as e:
            self.logger.error(f"Erreur recherche combobox '{object_name}': {e}")
            return None
    
    def find_table_by_name(self, parent, object_name):
        """Trouver un tableau par son nom d'objet"""
        try:
            return parent.findChild(QTableWidget, object_name)
        except Exception as e:
            self.logger.error(f"Erreur recherche table '{object_name}': {e}")
            return None

    def find_widget_by_name(self, parent, object_name):
        """Trouver un widget par son nom d'objet (générique)"""
        try:
            from PyQt5.QtWidgets import QWidget
            return parent.findChild(QWidget, object_name)
        except Exception as e:
            self.logger.error(f"Erreur recherche widget '{object_name}': {e}")
            return None

    def click_button_safe(self, button, wait_after=0.2):
        """Cliquer sur un bouton de manière sécurisée"""
        try:
            if button and button.isEnabled() and button.isVisible():
                button.click()
                self.app.processEvents()
                time.sleep(wait_after)
                return True
            else:
                self.logger.warning("Bouton non cliquable")
                return False
        except Exception as e:
            self.logger.error(f"Erreur clic bouton: {e}")
            return False
    
    def set_text_safe(self, field, text, wait_after=0.1):
        """Définir le texte d'un champ de manière sécurisée"""
        try:
            if field and field.isEnabled() and field.isVisible():
                field.clear()
                field.setText(text)
                self.app.processEvents()
                time.sleep(wait_after)
                return True
            else:
                self.logger.warning("Champ non modifiable")
                return False
        except Exception as e:
            self.logger.error(f"Erreur saisie texte: {e}")
            return False
    
    def select_combobox_item(self, combobox, text_or_index, wait_after=0.1):
        """Sélectionner un élément dans une combobox"""
        try:
            if not combobox or not combobox.isEnabled():
                return False
                
            if isinstance(text_or_index, int):
                # Sélection par index
                if 0 <= text_or_index < combobox.count():
                    combobox.setCurrentIndex(text_or_index)
                else:
                    return False
            else:
                # Sélection par texte
                index = combobox.findText(text_or_index)
                if index >= 0:
                    combobox.setCurrentIndex(index)
                else:
                    return False
            
            self.app.processEvents()
            time.sleep(wait_after)
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur sélection combobox: {e}")
            return False
    
    def select_table_row(self, table, row_index, wait_after=0.1):
        """Sélectionner une ligne dans un tableau"""
        try:
            if not table or row_index < 0 or row_index >= table.rowCount():
                return False
                
            table.selectRow(row_index)
            self.app.processEvents()
            time.sleep(wait_after)
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur sélection ligne tableau: {e}")
            return False
    
    def wait_for_widget_visible(self, widget, timeout=5):
        """Attendre qu'un widget soit visible"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if widget and widget.isVisible():
                self.app.processEvents()
                return True
            self.app.processEvents()
            time.sleep(0.1)
        return False
    
    def simulate_key_sequence(self, widget, key_sequence, wait_after=0.1):
        """Simuler une séquence de touches"""
        try:
            if widget and widget.isVisible():
                QTest.keySequence(widget, key_sequence)
                self.app.processEvents()
                time.sleep(wait_after)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erreur simulation touches: {e}")
            return False

    # === MÉTHODES SPÉCIALISÉES POUR TESTS DE COMPORTEMENT ===

    def open_dialog_from_button(self, parent_window, button_text, expected_dialog_class=None):
        """Ouvrir un dialogue en cliquant sur un bouton et attendre qu'il apparaisse"""
        try:
            # Trouver et cliquer sur le bouton
            button = self.find_button_by_text(parent_window, button_text)
            if not button:
                self.logger.error(f"Bouton '{button_text}' non trouvé")
                return None

            # Cliquer sur le bouton
            QTest.mouseClick(button, Qt.LeftButton)
            QTest.qWait(self.default_wait)
            self.app.processEvents()

            # Attendre qu'un dialogue apparaisse
            dialog = None
            for _ in range(10):  # Attendre jusqu'à 1 seconde
                QTest.qWait(100)
                self.app.processEvents()

                # Chercher un dialogue ouvert
                for widget in self.app.allWidgets():
                    if isinstance(widget, QDialog) and widget.isVisible():
                        if expected_dialog_class is None or isinstance(widget, expected_dialog_class):
                            dialog = widget
                            break

                if dialog:
                    break

            if dialog:
                self.logger.info(f"✅ Dialogue ouvert après clic sur '{button_text}'")
                return dialog
            else:
                self.logger.error(f"❌ Aucun dialogue ouvert après clic sur '{button_text}'")
                return None

        except Exception as e:
            self.logger.error(f"Erreur ouverture dialogue: {e}")
            return None

    def fill_form_fields(self, parent, field_data):
        """Remplir plusieurs champs de formulaire"""
        try:
            filled_count = 0
            for field_name, value in field_data.items():
                if self.set_widget_value_by_name(parent, field_name, value):
                    filled_count += 1
                    self.logger.debug(f"✅ Champ '{field_name}' rempli avec '{value}'")
                else:
                    self.logger.warning(f"⚠️ Champ '{field_name}' non trouvé ou non rempli")

            self.logger.info(f"✅ {filled_count}/{len(field_data)} champs remplis")
            return filled_count == len(field_data)

        except Exception as e:
            self.logger.error(f"Erreur remplissage formulaire: {e}")
            return False

    def save_and_close_dialog(self, dialog, save_button_text="Guardar"):
        """Sauvegarder et fermer un dialogue"""
        try:
            # Trouver le bouton de sauvegarde
            save_button = self.find_button_by_text(dialog, save_button_text)
            if not save_button:
                self.logger.error(f"Bouton '{save_button_text}' non trouvé")
                return False

            # Cliquer sur sauvegarder
            QTest.mouseClick(save_button, Qt.LeftButton)
            QTest.qWait(self.default_wait)
            self.app.processEvents()

            # Attendre que le dialogue se ferme
            for _ in range(10):  # Attendre jusqu'à 1 seconde
                QTest.qWait(100)
                self.app.processEvents()
                if not dialog.isVisible():
                    break

            success = not dialog.isVisible()
            if success:
                self.logger.info(f"✅ Dialogue sauvegardé et fermé")
            else:
                self.logger.error(f"❌ Dialogue non fermé après sauvegarde")

            return success

        except Exception as e:
            self.logger.error(f"Erreur sauvegarde dialogue: {e}")
            return False

    def verify_table_contains_data(self, table_widget, expected_data, column_mapping=None):
        """Vérifier qu'un tableau contient les données attendues"""
        try:
            if not isinstance(table_widget, QTableWidget):
                self.logger.error("Widget n'est pas un QTableWidget")
                return False

            row_count = table_widget.rowCount()
            if row_count == 0:
                self.logger.error("Tableau vide")
                return False

            # Vérifier si les données attendues sont présentes
            found_matches = 0
            for expected_item in expected_data:
                for row in range(row_count):
                    match = True
                    for key, expected_value in expected_item.items():
                        # Utiliser le mapping de colonnes si fourni
                        col = column_mapping.get(key, 0) if column_mapping else 0

                        if col < table_widget.columnCount():
                            item = table_widget.item(row, col)
                            actual_value = item.text() if item else ""

                            if str(expected_value).lower() not in actual_value.lower():
                                match = False
                                break

                    if match:
                        found_matches += 1
                        break

            success = found_matches == len(expected_data)
            if success:
                self.logger.info(f"✅ Toutes les données trouvées dans le tableau ({found_matches}/{len(expected_data)})")
            else:
                self.logger.error(f"❌ Données manquantes dans le tableau ({found_matches}/{len(expected_data)})")

            return success

        except Exception as e:
            self.logger.error(f"Erreur vérification tableau: {e}")
            return False
