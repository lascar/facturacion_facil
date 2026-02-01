# -*- coding: utf-8 -*-
"""
Tests de comportement pour le champ Forma de Pago (Mode de paiement)
Similaire à Condiciones de Pago - textarea avec case à cocher de visibilité PDF
Selon les règles strictes de pref_auggie.txt
"""

import pytest
import os
import json
import time
from PyQt5.QtWidgets import QCheckBox, QTextEdit, QGroupBox
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from utils.logger import get_logger


class TestOrganizacionFormaPagoBehaviour(BaseBehaviourTest):
    """Tests de comportement pour le champ Forma de Pago dans la configuration organisation"""

    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, mock_messagebox, mock_filedialog, tmp_path, monkeypatch):
        """Configuration du test avec l'application"""
        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.logger = get_logger(self.__class__.__name__)

        # Initialiser les attributs de base
        self.init_base_attributes()

        # Configuration des mocks pour éviter les blocages
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok
        mock_messagebox.warning.return_value = mock_messagebox.Ok
        mock_messagebox.critical.return_value = mock_messagebox.Ok
        mock_filedialog.getSaveFileName.return_value = ('/tmp/test_export.pdf', 'PDF Files (*.pdf)')
        mock_filedialog.getExistingDirectory.return_value = '/tmp'

        # Initialiser l'automation
        from test.behaviour.utils.pyqt5_automation import PyQt5Automation
        self.automation = PyQt5Automation(self.app)

        # Afficher la fenêtre principale
        self.main_window.show()
        self.app.processEvents()
        time.sleep(0.2)

        # ✅ PROTECTION : Utiliser un fichier temporaire au lieu de config/config.json
        self.temp_config_dir = tmp_path / "config"
        self.temp_config_dir.mkdir()
        self.config_file = str(self.temp_config_dir / "config.json")

        self.logger.info(f"✅ Utilisation du fichier config temporaire: {self.config_file}")

        yield

        # Nettoyage automatique par tmp_path
        self.logger.info(f"🧹 Nettoyage du fichier config temporaire: {self.config_file}")

    def test_01_forma_pago_widgets_exist_in_organizacion_window(self):
        """
        COMPORTEMENT: Les widgets Forma de Pago doivent exister dans la fenêtre Organización
        GIVEN: L'application principale est lancée
        WHEN: On ouvre la fenêtre Organización
        THEN: Le textarea forma_pago_edit et la case à cocher forma_pago_visible_checkbox existent
        """
        self.logger.info("🧪 Test 01: Vérification existence des widgets Forma de Pago")

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        assert organizacion_btn is not None, "Bouton Organización non trouvé"

        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre Organización
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                organizacion_window = widget
                break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")
        
        # Vérifier que le textarea forma_pago existe
        assert hasattr(organizacion_window, 'forma_pago_edit'), \
            "Le textarea forma_pago_edit doit exister"
        assert isinstance(organizacion_window.forma_pago_edit, QTextEdit), \
            "forma_pago_edit doit être un QTextEdit"
        
        # Vérifier que la case à cocher de visibilité existe
        assert hasattr(organizacion_window, 'forma_pago_visible_checkbox'), \
            "La case à cocher forma_pago_visible_checkbox doit exister"
        assert isinstance(organizacion_window.forma_pago_visible_checkbox, QCheckBox), \
            "forma_pago_visible_checkbox doit être un QCheckBox"
        
        # Vérifier que le GroupBox existe avec le bon titre
        assert hasattr(organizacion_window, 'forma_pago_group'), \
            "Le GroupBox forma_pago_group doit exister"
        assert isinstance(organizacion_window.forma_pago_group, QGroupBox), \
            "forma_pago_group doit être un QGroupBox"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 01 réussi: Les widgets Forma de Pago existent")

    def test_02_forma_pago_default_values(self):
        """
        COMPORTEMENT: Forma de Pago doit avoir des valeurs par défaut
        GIVEN: config.json contient les valeurs par défaut
        WHEN: On ouvre la fenêtre Organización
        THEN: Le textarea contient le texte par défaut et la case est cochée
        """
        self.logger.info("🧪 Test 02: Vérification valeurs par défaut de Forma de Pago")

        # Préparer config.json avec les valeurs par défaut
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'forma_pago': 'Transferencia bancaria - IBAN: ES00 0000 0000 0000 0000 0000',
                'forma_pago_visible': 1
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Forcer la synchronisation du fichier
        import subprocess
        subprocess.run(['sync'], check=False)
        time.sleep(0.5)

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)
        
        # Trouver la fenêtre (filtrer les QDialog)
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                if isinstance(widget, OrganizacionPyQt5Window):
                    organizacion_window = widget
                    break
        
        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Vérifier que le textarea contient la valeur par défaut
        forma_pago_text = organizacion_window.forma_pago_edit.toPlainText()
        assert 'Transferencia bancaria' in forma_pago_text, \
            f"Le textarea doit contenir la valeur par défaut, mais contient: {forma_pago_text}"
        
        # Vérifier que la case est cochée par défaut
        assert organizacion_window.forma_pago_visible_checkbox.isChecked(), \
            "La case forma_pago_visible doit être cochée par défaut"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 02 réussi: Valeurs par défaut correctes")

    @pytest.mark.timeout(30)
    def test_03_forma_pago_save_to_config_json(self):
        """
        COMPORTEMENT: Le contenu et l'état de visibilité de Forma de Pago doivent être sauvegardés
        GIVEN: La fenêtre Organización est ouverte
        WHEN: On modifie le texte, on décoche la case et on sauvegarde
        THEN: Les valeurs sont sauvegardées dans config.json
        """
        self.logger.info("🧪 Test 03: Vérification sauvegarde de Forma de Pago dans config.json")

        # Créer un fichier config temporaire
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'forma_pago': 'Texte initial',
                'forma_pago_visible': 1
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre (filtrer les QDialog)
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                if isinstance(widget, OrganizacionPyQt5Window):
                    organizacion_window = widget
                    break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Modifier le texte
        nuevo_texto = 'Pago en efectivo o tarjeta'
        organizacion_window.forma_pago_edit.setPlainText(nuevo_texto)
        self.app.processEvents()
        
        # Décocher la case
        organizacion_window.forma_pago_visible_checkbox.setChecked(False)
        self.app.processEvents()
        time.sleep(0.2)

        # Sauvegarder
        save_btn = self.automation.find_button_by_text(organizacion_window, "Guardar")
        assert save_btn is not None, "Bouton Guardar non trouvé"

        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Vérifier que les valeurs sont sauvegardées dans config.json
        assert os.path.exists(self.config_file), "config.json doit exister"

        with open(self.config_file, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)

        org_defaults = saved_config.get('organizacion_defaults', {})

        assert 'forma_pago' in org_defaults, \
            "forma_pago doit être dans config.json"
        assert 'forma_pago_visible' in org_defaults, \
            "forma_pago_visible doit être dans config.json"

        assert org_defaults['forma_pago'] == nuevo_texto, \
            f"forma_pago doit être '{nuevo_texto}', mais est '{org_defaults.get('forma_pago')}'"
        assert org_defaults['forma_pago_visible'] == 0, \
            "forma_pago_visible doit être 0 (décoché)"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 03 réussi: Forma de Pago sauvegardé dans config.json")

    @pytest.mark.timeout(30)
    def test_04_forma_pago_load_from_config_json(self):
        """
        COMPORTEMENT: Forma de Pago doit être chargé depuis config.json
        GIVEN: config.json contient forma_pago_visible=0 et un texte personnalisé
        WHEN: On ouvre la fenêtre Organización
        THEN: Le textarea contient le texte et la case est décochée
        """
        self.logger.info("🧪 Test 04: Vérification chargement de Forma de Pago depuis config.json")

        # Préparer config.json
        texto_personalizado = 'Solo transferencia bancaria - Plazo: 30 días'
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'forma_pago': texto_personalizado,
                'forma_pago_visible': 0
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre (filtrer les QDialog)
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                if isinstance(widget, OrganizacionPyQt5Window):
                    organizacion_window = widget
                    break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Vérifier que le textarea contient le texte personnalisé
        forma_pago_text = organizacion_window.forma_pago_edit.toPlainText()
        assert forma_pago_text == texto_personalizado, \
            f"Le textarea doit contenir '{texto_personalizado}', mais contient: '{forma_pago_text}'"
        
        # Vérifier que la case est décochée
        assert not organizacion_window.forma_pago_visible_checkbox.isChecked(), \
            "La case forma_pago_visible doit être décochée (chargée depuis config.json)"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 04 réussi: Forma de Pago chargé depuis config.json")

    def test_05_forma_pago_placeholder_text(self):
        """
        COMPORTEMENT: Le textarea Forma de Pago doit avoir un placeholder text
        GIVEN: La fenêtre Organización est ouverte
        WHEN: Le textarea est vide
        THEN: Un texte d'aide (placeholder) est affiché
        """
        self.logger.info("🧪 Test 05: Vérification du placeholder text de Forma de Pago")

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre (filtrer les QDialog)
        from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                if isinstance(widget, OrganizacionPyQt5Window):
                    organizacion_window = widget
                    break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config
        organizacion_window.config_file = self.config_file

        # Vider le textarea
        organizacion_window.forma_pago_edit.setPlainText('')
        self.app.processEvents()

        # Vérifier que le placeholder existe
        placeholder = organizacion_window.forma_pago_edit.placeholderText()
        assert placeholder is not None and len(placeholder) > 0, \
            "Le textarea doit avoir un placeholder text"
        assert 'pago' in placeholder.lower() or 'transferencia' in placeholder.lower() or 'efectivo' in placeholder.lower() or 'tarjeta' in placeholder.lower(), \
            f"Le placeholder doit contenir une référence au paiement, mais contient: '{placeholder}'"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 05 réussi: Placeholder text présent")
