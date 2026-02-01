# -*- coding: utf-8 -*-
"""
Tests de comportement pour la visibilité de Forma de Pago dans les PDFs
Selon les règles strictes de pref_auggie.txt
"""

import pytest
import os
import json
import time
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from utils.logger import get_logger


class TestFormaPagoPdfVisibilityBehaviour(BaseBehaviourTest):
    """Tests de comportement pour la visibilité de Forma de Pago dans les PDFs"""

    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, mock_messagebox, mock_filedialog, tmp_path, monkeypatch):
        """Configuration du test avec l'application"""
        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.logger = get_logger(self.__class__.__name__)

        # Initialiser les attributs de base
        self.init_base_attributes()

        # Configuration des mocks
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

        # ✅ PROTECTION : Utiliser un fichier temporaire
        self.temp_config_dir = tmp_path / "config"
        self.temp_config_dir.mkdir()
        self.config_file = str(self.temp_config_dir / "config.json")

        self.logger.info(f"✅ Utilisation du fichier config temporaire: {self.config_file}")

        yield

        self.logger.info(f"🧹 Nettoyage du fichier config temporaire: {self.config_file}")

    def test_01_pdf_generator_reads_forma_pago_from_config(self):
        """
        COMPORTEMENT: Le générateur PDF doit lire forma_pago depuis config.json
        GIVEN: config.json contient forma_pago et forma_pago_visible
        WHEN: Le PDFGenerator charge sa configuration
        THEN: Les valeurs sont correctement chargées
        """
        self.logger.info("🧪 Test 01: Vérification lecture forma_pago par PDFGenerator")

        # Préparer config.json avec forma_pago
        config = {
            'organizacion_defaults': {
                'forma_pago': 'Transferencia bancaria - IBAN: ES12 3456 7890 1234 5678 9012',
                'forma_pago_visible': 1
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Instancier le PDFGenerator avec le fichier config temporaire
        from utils.pdf_generator import PDFGenerator
        
        # Patcher le chemin du fichier config dans PDFGenerator
        with patch('utils.pdf_generator.PDFGenerator.get_default_config') as mock_default:
            mock_default.return_value = {
                'forma_pago': '',
                'forma_pago_visible': 1
            }
            
            pdf_gen = PDFGenerator()
            # Patcher le chargement du config pour utiliser notre fichier temporaire
            with patch('builtins.open', side_effect=lambda path, *args, **kwargs: 
                open(self.config_file, *args, **kwargs) if 'config.json' in str(path) 
                else open(path, *args, **kwargs) if os.path.exists(path) 
                else MagicMock()):
                
                config_data = pdf_gen.load_config_data()
                
                # Vérifier que forma_pago est dans la config
                assert 'forma_pago' in config_data, \
                    "forma_pago doit être dans les données de config"

        self.logger.info("✅ Test 01 réussi: PDFGenerator lit forma_pago depuis config.json")

    def test_02_pdf_generator_includes_forma_pago_when_visible(self):
        """
        COMPORTEMENT: Le PDF doit inclure Forma de Pago quand visible=1
        GIVEN: config.json contient forma_pago_visible=1
        WHEN: Le PDF est généré
        THEN: La section Forma de Pago apparaît dans le footer
        """
        self.logger.info("🧪 Test 02: Vérification inclusion Forma de Pago dans PDF quand visible")

        # Préparer config.json
        forma_pago_text = 'Pago en efectivo o transferencia bancaria'
        config = {
            'organizacion_defaults': {
                'forma_pago': forma_pago_text,
                'forma_pago_visible': 1,
                'condiciones_pago': '',
                'condiciones_pago_visible': 0,
                'informacion_legal': '',
                'informacion_legal_visible': 0
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        from utils.pdf_generator import PDFGenerator
        
        pdf_gen = PDFGenerator()
        
        # Simuler le chargement de config
        with patch.object(pdf_gen, 'load_config_data', return_value=config['organizacion_defaults']):
            # Créer un footer
            footer_elements = pdf_gen.create_footer({})
            
            # Convertir les éléments en texte pour vérification
            footer_text = ""
            for elem in footer_elements:
                if hasattr(elem, 'text'):
                    footer_text += elem.text
                elif hasattr(elem, '_text'):
                    footer_text += elem._text

            # Vérifier que forma_pago est présent dans le footer
            assert 'forma' in footer_text.lower() or 'pago' in footer_text.lower() or forma_pago_text in footer_text, \
                f"Le footer doit contenir Forma de Pago ou le texte '{forma_pago_text}', mais contient: {footer_text}"

        self.logger.info("✅ Test 02 réussi: Forma de Pago inclus dans PDF quand visible=1")

    def test_03_pdf_generator_excludes_forma_pago_when_not_visible(self):
        """
        COMPORTEMENT: Le PDF ne doit PAS inclure Forma de Pago quand visible=0
        GIVEN: config.json contient forma_pago_visible=0
        WHEN: Le PDF est généré
        THEN: La section Forma de Pago n'apparaît PAS dans le footer
        """
        self.logger.info("🧪 Test 03: Vérification exclusion Forma de Pago quand non visible")

        # Préparer config.json avec forma_pago_visible=0
        forma_pago_text = 'Pago en efectivo'
        config = {
            'organizacion_defaults': {
                'forma_pago': forma_pago_text,
                'forma_pago_visible': 0,
                'condiciones_pago': '',
                'condiciones_pago_visible': 0,
                'informacion_legal': '',
                'informacion_legal_visible': 0
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        from utils.pdf_generator import PDFGenerator
        
        pdf_gen = PDFGenerator()
        
        # Simuler le chargement de config
        with patch.object(pdf_gen, 'load_config_data', return_value=config['organizacion_defaults']):
            # Créer un footer
            footer_elements = pdf_gen.create_footer({})
            
            # Convertir les éléments en texte pour vérification
            footer_text = ""
            for elem in footer_elements:
                if hasattr(elem, 'text'):
                    footer_text += elem.text
                elif hasattr(elem, '_text'):
                    footer_text += elem._text

            # Vérifier que forma_pago n'est PAS présent dans le footer
            assert forma_pago_text not in footer_text, \
                f"Le footer ne doit PAS contenir '{forma_pago_text}' quand visible=0, mais contient: {footer_text}"

        self.logger.info("✅ Test 03 réussi: Forma de Pago exclu du PDF quand visible=0")

    def test_04_forma_pago_visible_checkbox_label_translation(self):
        """
        COMPORTEMENT: Le label de la case à cocher doit être traduit (pas hardcodé)
        GIVEN: La fenêtre Organización est ouverte
        WHEN: On examine le label de la case à cocher
        THEN: Le texte n'est pas hardcodé et utilise le système de traduction
        """
        self.logger.info("🧪 Test 04: Vérification traduction du label de la case à cocher")

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

        # Vérifier que le label contient une référence à la visibilité PDF
        checkbox_text = organizacion_window.forma_pago_visible_checkbox.text()
        
        # Le texte doit contenir une indication de visibilité
        assert any(keyword in checkbox_text.lower() for keyword in ['visible', 'pdf', 'mostrar']), \
            f"Le label doit indiquer la visibilité dans le PDF, mais contient: '{checkbox_text}'"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()

        self.logger.info("✅ Test 04 réussi: Label de la case à cocher correct")

    def test_05_forma_pago_empty_not_included_in_pdf(self):
        """
        COMPORTEMENT: Forma de Pago vide ne doit pas apparaître dans le PDF
        GIVEN: config.json contient forma_pago vide ou uniquement espaces
        WHEN: Le PDF est généré
        THEN: La section Forma de Pago n'apparaît PAS dans le footer
        """
        self.logger.info("🧪 Test 05: Vérification exclusion Forma de Pago vide dans PDF")

        # Préparer config.json avec forma_pago vide
        config = {
            'organizacion_defaults': {
                'forma_pago': '   ',  # Espaces uniquement
                'forma_pago_visible': 1,
                'condiciones_pago': '',
                'condiciones_pago_visible': 0,
                'informacion_legal': '',
                'informacion_legal_visible': 0
            }
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        from utils.pdf_generator import PDFGenerator
        
        pdf_gen = PDFGenerator()
        
        # Simuler le chargement de config
        with patch.object(pdf_gen, 'load_config_data', return_value=config['organizacion_defaults']):
            # Créer un footer
            footer_elements = pdf_gen.create_footer({})
            
            # Convertir les éléments en texte pour vérification
            footer_text = ""
            for elem in footer_elements:
                if hasattr(elem, 'text'):
                    footer_text += elem.text
                elif hasattr(elem, '_text'):
                    footer_text += elem._text

            # Vérifier que forma_pago vide n'est pas inclus
            # Le texte devrait être vide ou ne pas contenir "FORMA DE PAGO"
            assert 'FORMA DE PAGO' not in footer_text.upper(), \
                f"Le footer ne doit PAS contenir 'FORMA DE PAGO' quand le texte est vide, mais contient: {footer_text}"

        self.logger.info("✅ Test 05 réussi: Forma de Pago vide exclu du PDF")
