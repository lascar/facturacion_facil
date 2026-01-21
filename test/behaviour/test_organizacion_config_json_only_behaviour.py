# -*- coding: utf-8 -*-
"""
Tests de comportement pour vérifier que OrganizacionWindow utilise UNIQUEMENT config.json
(et non la base de données) comme source de vérité.
Selon les règles strictes de pref_auggie.txt
"""

import pytest
import os
import json
import time
import tempfile
import shutil
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from utils.logger import get_logger


class TestOrganizacionConfigJsonOnlyBehaviour(BaseBehaviourTest):
    """Tests de comportement pour vérifier que config.json est la SEULE source de vérité"""

    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, mock_messagebox, mock_filedialog):
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

        # Créer une copie de backup de config.json
        self.config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
        self.config_backup = self.config_file + '.backup_test'
        if os.path.exists(self.config_file):
            shutil.copy(self.config_file, self.config_backup)

        yield

        # Restaurer config.json après le test
        if os.path.exists(self.config_backup):
            shutil.copy(self.config_backup, self.config_file)
            os.remove(self.config_backup)

    def test_01_organizacion_window_no_database_imports(self):
        """
        COMPORTEMENT: OrganizacionWindow ne doit PAS importer de modules de base de données
        GIVEN: Le fichier ui/organizacion_pyqt5.py
        WHEN: On vérifie les imports
        THEN: Aucun import de database ou OrganizacionService n'est présent
        """
        self.logger.info("🧪 Test 01: Vérification absence imports base de données")
        
        organizacion_file = os.path.join(os.path.dirname(__file__), '..', '..', 'ui', 'organizacion_pyqt5.py')
        
        with open(organizacion_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier qu'il n'y a PAS d'import de database
        assert 'from database import database' not in content, \
            "OrganizacionWindow ne doit PAS importer 'from database import database'"
        
        # Vérifier qu'il n'y a PAS d'import de OrganizacionService
        assert 'from services.organizacion_service import OrganizacionService' not in content, \
            "OrganizacionWindow ne doit PAS importer OrganizacionService"
        
        self.logger.info("✅ Test 01 réussi: Aucun import de base de données")

    def test_02_organizacion_loads_from_config_json_only(self):
        """
        COMPORTEMENT: OrganizacionWindow doit charger les données depuis config.json UNIQUEMENT
        GIVEN: config.json contient des données d'organisation
        WHEN: On ouvre la fenêtre Organización
        THEN: Les champs sont remplis avec les données de config.json
        """
        self.logger.info("🧪 Test 02: Vérification chargement depuis config.json uniquement")
        
        # Préparer des données de test dans config.json
        test_data = {
            "organizacion_defaults": {
                "nombre": "Test Empresa BDD",
                "direccion": "Calle Test 123",
                "telefono": "+34 999 888 777",
                "email": "test@bdd.com",
                "cif": "B99999999",
                "numero_factura_inicial": "100",
                "directorio_imagenes_defecto": "images_test",
                "directorio_descargas_pdf": "facturas_test/",
                "directorio_informes": "informes_test/",
                "directorio_logos_storage": "logo_test/",
                "logo_path": "logo/test.png",
                "logo_orientation": "landscape",
                "condiciones_pago": "Condiciones de test",
                "informacion_legal": "Info legal de test"
            }
        }
        
        # Sauvegarder dans config.json
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        # Ouvrir la fenêtre Organización
        organizacion_btn = self.automation.find_button_by_text(self.main_window, "Organización")
        assert organizacion_btn is not None, "Bouton Organización non trouvé"
        
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
        
        # Vérifier que les données sont chargées depuis config.json
        assert organizacion_window.nombre_edit.text() == "Test Empresa BDD", \
            f"Nom attendu: 'Test Empresa BDD', obtenu: '{organizacion_window.nombre_edit.text()}'"
        
        assert organizacion_window.email_edit.text() == "test@bdd.com", \
            f"Email attendu: 'test@bdd.com', obtenu: '{organizacion_window.email_edit.text()}'"

        self.logger.info("✅ Test 02 réussi: Données chargées depuis config.json")

    @pytest.mark.timeout(30)
    def test_03_organizacion_saves_to_config_json_only(self):
        """
        COMPORTEMENT: OrganizacionWindow doit sauvegarder dans config.json UNIQUEMENT
        GIVEN: La fenêtre Organización est ouverte avec des données modifiées
        WHEN: On clique sur le bouton Guardar
        THEN: Les données sont sauvegardées dans config.json (et non dans la base de données)
        """
        self.logger.info("🧪 Test 03: Vérification sauvegarde dans config.json uniquement")

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

        # Modifier les données
        test_nombre = "Nueva Empresa Test BDD"
        test_email = "nuevo@test.com"
        test_telefono = "+34 111 222 333"

        organizacion_window.nombre_edit.setText(test_nombre)
        organizacion_window.email_edit.setText(test_email)
        organizacion_window.telefono_edit.setText(test_telefono)
        self.app.processEvents()

        # Trouver et cliquer sur le bouton Guardar
        save_btn = None
        for btn in organizacion_window.findChildren(QPushButton):
            if "Guardar" in btn.text():
                save_btn = btn
                break

        assert save_btn is not None, "Bouton Guardar non trouvé"

        # Cliquer sur Guardar
        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Vérifier que les données sont dans config.json
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        org_data = config.get('organizacion_defaults', {})

        assert org_data.get('nombre') == test_nombre, \
            f"Nom dans config.json attendu: '{test_nombre}', obtenu: '{org_data.get('nombre')}'"

        assert org_data.get('email') == test_email, \
            f"Email dans config.json attendu: '{test_email}', obtenu: '{org_data.get('email')}'"

        assert org_data.get('telefono') == test_telefono, \
            f"Téléphone dans config.json attendu: '{test_telefono}', obtenu: '{org_data.get('telefono')}'"

        self.logger.info("✅ Test 03 réussi: Données sauvegardées dans config.json")

    def test_04_organizacion_window_has_no_organizacion_service(self):
        """
        COMPORTEMENT: OrganizacionWindow ne doit PAS avoir d'attribut organizacion_service
        GIVEN: La fenêtre Organización est ouverte
        WHEN: On vérifie les attributs de l'instance
        THEN: L'attribut organizacion_service n'existe PAS
        """
        self.logger.info("🧪 Test 04: Vérification absence organizacion_service")

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

        # Vérifier que organizacion_service n'existe PAS
        assert not hasattr(organizacion_window, 'organizacion_service'), \
            "OrganizacionWindow ne doit PAS avoir d'attribut 'organizacion_service'"

        self.logger.info("✅ Test 04 réussi: Pas d'attribut organizacion_service")

    def test_05_organizacion_uses_save_all_to_config_json(self):
        """
        COMPORTEMENT: OrganizacionWindow doit utiliser save_all_to_config_json pour sauvegarder
        GIVEN: La classe OrganizacionPyQt5Window
        WHEN: On vérifie l'existence de la méthode save_all_to_config_json
        THEN: La méthode existe et est utilisée pour sauvegarder
        """
        self.logger.info("🧪 Test 05: Vérification méthode save_all_to_config_json")

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

        # Vérifier que la méthode save_all_to_config_json existe
        assert hasattr(organizacion_window, 'save_all_to_config_json'), \
            "La méthode save_all_to_config_json doit exister"

        # Vérifier que c'est bien une méthode callable
        assert callable(organizacion_window.save_all_to_config_json), \
            "save_all_to_config_json doit être une méthode callable"

        self.logger.info("✅ Test 05 réussi: Méthode save_all_to_config_json existe")

    @pytest.mark.timeout(30)
    def test_06_organizacion_persistence_across_reopens(self):
        """
        COMPORTEMENT: Les données doivent persister entre les ouvertures de la fenêtre
        GIVEN: Des données ont été sauvegardées dans config.json
        WHEN: On ferme et rouvre la fenêtre Organización
        THEN: Les données sont toujours présentes
        """
        self.logger.info("🧪 Test 06: Vérification persistance des données")

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

        # Modifier et sauvegarder
        test_nombre = "Empresa Persistente BDD"
        organizacion_window.nombre_edit.setText(test_nombre)
        self.app.processEvents()

        # Sauvegarder
        save_btn = None
        for btn in organizacion_window.findChildren(QPushButton):
            if "Guardar" in btn.text():
                save_btn = btn
                break

        assert save_btn is not None, "Bouton Guardar non trouvé"
        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Vérifier que config.json a bien été mis à jour
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        saved_nombre = config.get('organizacion_defaults', {}).get('nombre', '')
        self.logger.info(f"Nom dans config.json après sauvegarde: '{saved_nombre}'")

        assert saved_nombre == test_nombre, \
            f"Nom dans config.json attendu: '{test_nombre}', obtenu: '{saved_nombre}'"

        # Fermer la fenêtre
        organizacion_window.close()
        self.app.processEvents()
        time.sleep(0.3)

        # Rouvrir la fenêtre
        QTest.mouseClick(organizacion_btn, Qt.LeftButton)
        self.app.processEvents()
        time.sleep(0.5)

        # Trouver la nouvelle fenêtre
        organizacion_window_new = None
        for widget in self.app.topLevelWidgets():
            if hasattr(widget, 'windowTitle') and "Configuración de la Organización" in widget.windowTitle():
                if widget.isVisible():
                    organizacion_window_new = widget
                    break

        assert organizacion_window_new is not None, "Fenêtre Organización non trouvée après réouverture"

        # Vérifier que les données sont toujours là
        actual_nombre = organizacion_window_new.nombre_edit.text()
        self.logger.info(f"Nom dans le formulaire après réouverture: '{actual_nombre}'")

        # Vérifier à nouveau config.json
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_check = json.load(f)

        config_nombre = config_check.get('organizacion_defaults', {}).get('nombre', '')
        self.logger.info(f"Nom dans config.json après réouverture: '{config_nombre}'")

        assert actual_nombre == test_nombre, \
            f"Nom attendu après réouverture: '{test_nombre}', obtenu: '{actual_nombre}' (config.json contient: '{config_nombre}')"

        self.logger.info("✅ Test 06 réussi: Données persistantes entre les ouvertures")


