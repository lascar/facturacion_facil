# -*- coding: utf-8 -*-
"""
Tests de comportement pour les cases à cocher de visibilité des conditions de paiement
et informations légales dans les PDFs
Selon les règles strictes de pref_auggie.txt
"""

import pytest
import os
import json
import time
from PyQt5.QtWidgets import QCheckBox, QPushButton
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from utils.logger import get_logger


class TestOrganizacionVisibilityCheckboxesBehaviour(BaseBehaviourTest):
    """Tests de comportement pour les cases à cocher de visibilité dans les PDFs"""

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
        # Créer un répertoire temporaire pour config
        self.temp_config_dir = tmp_path / "config"
        self.temp_config_dir.mkdir()
        self.config_file = str(self.temp_config_dir / "config.json")

        self.logger.info(f"✅ Utilisation du fichier config temporaire: {self.config_file}")

        yield

        # Nettoyage automatique par tmp_path
        self.logger.info(f"🧹 Nettoyage du fichier config temporaire: {self.config_file}")

    def test_01_checkboxes_exist_in_organizacion_window(self):
        """
        COMPORTEMENT: Les cases à cocher de visibilité doivent exister dans la fenêtre Organización
        GIVEN: L'application principale est lancée
        WHEN: On ouvre la fenêtre Organización
        THEN: Les cases à cocher condiciones_pago_visible et informacion_legal_visible existent
        """
        self.logger.info("🧪 Test 01: Vérification existence des cases à cocher")

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

        # ✅ PROTECTION : Patcher le chemin du fichier config pour utiliser le fichier temporaire
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")
        
        # Vérifier que les cases à cocher existent
        assert hasattr(organizacion_window, 'condiciones_pago_visible_checkbox'), \
            "La case à cocher condiciones_pago_visible_checkbox doit exister"
        assert hasattr(organizacion_window, 'informacion_legal_visible_checkbox'), \
            "La case à cocher informacion_legal_visible_checkbox doit exister"
        
        # Vérifier que ce sont bien des QCheckBox
        assert isinstance(organizacion_window.condiciones_pago_visible_checkbox, QCheckBox), \
            "condiciones_pago_visible_checkbox doit être un QCheckBox"
        assert isinstance(organizacion_window.informacion_legal_visible_checkbox, QCheckBox), \
            "informacion_legal_visible_checkbox doit être un QCheckBox"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 01 réussi: Les cases à cocher existent")

    def test_02_checkboxes_default_checked(self):
        """
        COMPORTEMENT: Les cases à cocher doivent être cochées par défaut
        GIVEN: config.json contient les valeurs par défaut (1)
        WHEN: On ouvre la fenêtre Organización
        THEN: Les deux cases sont cochées
        """
        self.logger.info("🧪 Test 02: Vérification état par défaut des cases à cocher")

        # Préparer config.json avec les valeurs par défaut
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'condiciones_pago': 'Test conditions',
                'informacion_legal': 'Test legal',
                'condiciones_pago_visible': 1,
                'informacion_legal_visible': 1
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Forcer la synchronisation du fichier
        import subprocess
        subprocess.run(['sync'], check=False)

        # Attendre que le fichier soit bien écrit
        time.sleep(0.5)

        # Vérifier que le fichier contient bien les bonnes valeurs
        with open(self.config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
            self.logger.info(f"Config chargée: {loaded_config}")
            assert loaded_config['organizacion_defaults']['condiciones_pago_visible'] == 1, \
                f"config.json doit contenir condiciones_pago_visible=1, mais contient {loaded_config['organizacion_defaults'].get('condiciones_pago_visible')}"
            assert loaded_config['organizacion_defaults']['informacion_legal_visible'] == 1, \
                f"config.json doit contenir informacion_legal_visible=1, mais contient {loaded_config['organizacion_defaults'].get('informacion_legal_visible')}"

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)
        
        # Trouver la fenêtre
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                organizacion_window = widget
                break
        
        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config pour utiliser le fichier temporaire
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Vérifier que les cases sont cochées par défaut
        assert organizacion_window.condiciones_pago_visible_checkbox.isChecked(), \
            "La case condiciones_pago_visible doit être cochée par défaut"
        assert organizacion_window.informacion_legal_visible_checkbox.isChecked(), \
            "La case informacion_legal_visible doit être cochée par défaut"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 02 réussi: Les cases sont cochées par défaut")

    @pytest.mark.timeout(30)
    def test_03_checkboxes_save_to_config_json(self):
        """
        COMPORTEMENT: Les états des cases à cocher doivent être sauvegardés dans config.json
        GIVEN: La fenêtre Organización est ouverte
        WHEN: On décoche les cases et on sauvegarde
        THEN: Les valeurs 0 sont sauvegardées dans config.json
        """
        self.logger.info("🧪 Test 03: Vérification sauvegarde des cases à cocher dans config.json")

        # Créer un fichier config temporaire avec les valeurs par défaut
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'condiciones_pago': 'Test conditions',
                'informacion_legal': 'Test legal',
                'condiciones_pago_visible': 1,
                'informacion_legal_visible': 1
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                organizacion_window = widget
                break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config pour utiliser le fichier temporaire
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Décocher les deux cases
        organizacion_window.condiciones_pago_visible_checkbox.setChecked(False)
        organizacion_window.informacion_legal_visible_checkbox.setChecked(False)
        self.app.processEvents()
        time.sleep(0.2)

        # Vérifier que les cases sont décochées
        assert not organizacion_window.condiciones_pago_visible_checkbox.isChecked(), \
            "La case condiciones_pago_visible doit être décochée"
        assert not organizacion_window.informacion_legal_visible_checkbox.isChecked(), \
            "La case informacion_legal_visible doit être décochée"

        # Sauvegarder
        save_btn = self.automation.find_button_by_text(organizacion_window, "Guardar")
        assert save_btn is not None, "Bouton Guardar non trouvé"

        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Vérifier que les valeurs sont sauvegardées dans config.json
        assert os.path.exists(self.config_file), "config.json doit exister"

        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        org_defaults = config.get('organizacion_defaults', {})

        assert 'condiciones_pago_visible' in org_defaults, \
            "condiciones_pago_visible doit être dans config.json"
        assert 'informacion_legal_visible' in org_defaults, \
            "informacion_legal_visible doit être dans config.json"

        assert org_defaults['condiciones_pago_visible'] == 0, \
            "condiciones_pago_visible doit être 0 (décoché)"
        assert org_defaults['informacion_legal_visible'] == 0, \
            "informacion_legal_visible doit être 0 (décoché)"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 03 réussi: Les états des cases sont sauvegardés dans config.json")

    @pytest.mark.timeout(30)
    def test_04_checkboxes_load_from_config_json(self):
        """
        COMPORTEMENT: Les états des cases à cocher doivent être chargés depuis config.json
        GIVEN: config.json contient condiciones_pago_visible=0 et informacion_legal_visible=0
        WHEN: On ouvre la fenêtre Organización
        THEN: Les cases sont décochées
        """
        self.logger.info("🧪 Test 04: Vérification chargement des cases à cocher depuis config.json")

        # Préparer config.json avec les cases décochées
        config = {
            'organizacion_defaults': {
                'nombre': 'Test Empresa',
                'condiciones_pago': 'Test conditions',
                'informacion_legal': 'Test legal',
                'condiciones_pago_visible': 0,
                'informacion_legal_visible': 0
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la fenêtre
        organizacion_window = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                organizacion_window = widget
                break

        assert organizacion_window is not None, "Fenêtre Organización non trouvée"

        # ✅ PROTECTION : Patcher le chemin du fichier config pour utiliser le fichier temporaire
        organizacion_window.config_file = self.config_file
        self.logger.info(f"✅ Fenêtre Organización utilise le fichier temporaire: {self.config_file}")

        # Recharger les données depuis le fichier temporaire
        organizacion_window.load_organizacion()
        self.app.processEvents()

        # Vérifier que les cases sont décochées
        assert not organizacion_window.condiciones_pago_visible_checkbox.isChecked(), \
            "La case condiciones_pago_visible doit être décochée (chargée depuis config.json)"
        assert not organizacion_window.informacion_legal_visible_checkbox.isChecked(), \
            "La case informacion_legal_visible doit être décochée (chargée depuis config.json)"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 04 réussi: Les états des cases sont chargés depuis config.json")
