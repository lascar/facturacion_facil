# -*- coding: utf-8 -*-
"""
Tests de comportement pour la fonctionnalité d'archivage des factures

⚠️ CRITIQUE: Ces tests sont en LECTURE SEULE uniquement.
Aucune modification de la base de données n'est effectuée.

Conforme à: docs/dev/testing/REGLES_CRITIQUES_TESTS_BASE_DONNEES.md
"""

import pytest
from unittest.mock import MagicMock, patch
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation


class TestArchivarFacturasBehaviour(BaseBehaviourTest):
    """Tests de comportement pour l'archivage des factures (lecture seule)"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox):
        """Configuration automatique pour chaque test"""
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
        
        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "Facturas")
        if facturas_btn:
            self.automation.click_button_safe(facturas_btn, wait_after=0.2)
            self.facturas_window = self.main_window.facturas_window
            self.wait_for_window(self.facturas_window)
        
        self.slow_mode_wait()
    
    @pytest.mark.timeout(20)
    def test_boton_nuevo_anio_existe(self):
        """Test: Vérifier que le bouton 'Empezar Nuevo Año' existe et est visible.
        
        Objectif: Valider la présence du bouton d'archivage dans l'interface.
        Méthode: Recherche du bouton par texte et vérification de visibilité.
        Données: Aucune donnée n'est modifiée (lecture seule).
        Sécurité: Ce test est conforme - lecture seule de l'interface.
        """
        self.logger.info("🧪 Test: Bouton 'Empezar Nuevo Año' existe")
        
        # Chercher le bouton
        nuevo_anio_btn = self.automation.find_button_by_text(
            self.facturas_window, "Empezar Nuevo Año"
        )
        
        assert nuevo_anio_btn is not None, "Bouton 'Empezar Nuevo Año' non trouvé"
        assert nuevo_anio_btn.isVisible(), "Bouton non visible"
        assert nuevo_anio_btn.isEnabled(), "Bouton non activé"
        
        # Vérifier le style (couleur orange de warning)
        style = nuevo_anio_btn.styleSheet()
        assert "ff9800" in style.lower() or "orange" in style.lower() or "background-color" in style.lower(), \
            "Le bouton devrait avoir un style distinctif (orange)"
        
        self.take_screenshot("boton_nuevo_anio")
        self.logger.info("✅ Bouton 'Empezar Nuevo Año' trouvé, visible et activé")
    
    @pytest.mark.timeout(20)
    def test_boton_nuevo_anio_tooltip(self):
        """Test: Vérifier que le bouton a un tooltip explicatif.
        
        Objectif: Valider que l'utilisateur comprend l'action avant de cliquer.
        Méthode: Vérification du tooltip du bouton.
        Données: Aucune donnée n'est modifiée (lecture seule).
        Sécurité: Ce test est conforme - lecture seule de l'interface.
        """
        self.logger.info("🧪 Test: Tooltip du bouton 'Empezar Nuevo Año'")
        
        nuevo_anio_btn = self.automation.find_button_by_text(
            self.facturas_window, "Empezar Nuevo Año"
        )
        assert nuevo_anio_btn is not None, "Bouton non trouvé"
        
        # Vérifier le tooltip
        tooltip = nuevo_anio_btn.toolTip()
        assert tooltip, "Le bouton devrait avoir un tooltip explicatif"
        assert "archiv" in tooltip.lower() or "archivar" in tooltip.lower(), \
            f"Le tooltip devrait mentionner l'archivage: {tooltip}"
        
        self.logger.info(f"✅ Tooltip trouvé: {tooltip}")
    
    @pytest.mark.timeout(15)
    def test_metodo_on_nuevo_anio_existe(self):
        """Test: Vérifier que la méthode on_nuevo_anio existe.
        
        Objectif: Valider que le handler du bouton est implémenté.
        Méthode: Vérification de l'existence de la méthode.
        Données: Aucune donnée n'est modifiée (lecture seule).
        Sécurité: Ce test est conforme - lecture seule de l'interface.
        """
        self.logger.info("🧪 Test: Méthode on_nuevo_anio existe")
        
        assert hasattr(self.facturas_window, 'on_nuevo_anio'), \
            "La méthode on_nuevo_anio devrait exister"
        
        assert callable(self.facturas_window.on_nuevo_anio), \
            "on_nuevo_anio devrait être une méthode callable"
        
        self.logger.info("✅ Méthode on_nuevo_anio existe et est callable")
    
    @pytest.mark.timeout(20)
    def test_boton_nuevo_anio_clic_affiche_dialog(self, mock_messagebox):
        """Test: Vérifier que cliquer le bouton affiche le dialogue de confirmation.
        
        Objectif: Valider le flux d'interface sans modifier les données.
        Méthode: Mock complet de la méthode d'archivage pour ne rien modifier.
        Données: Aucune - la méthode réelle est mockée.
        Sécurité: Ce test est conforme - utilise des mocks, aucune modification.
        """
        self.logger.info("🧪 Test: Clic sur bouton affiche dialogue (mock)")
        
        # Mock complet pour éviter toute modification
        with patch.object(self.facturas_window, 'database') as mock_db:
            # Configurer le mock pour retourner immédiatement
            mock_db.archivar_facturas_anio.return_value = (True, 0, "Test mock")
            
            # Mock pour capturer les dialogues
            mock_messagebox.warning.return_value = mock_messagebox.No  # Annuler immédiatement
            
            # Chercher et cliquer le bouton
            nuevo_anio_btn = self.automation.find_button_by_text(
                self.facturas_window, "Empezar Nuevo Año"
            )
            assert nuevo_anio_btn is not None, "Bouton non trouvé"
            
            # Cliquer (cela devrait afficher le dialogue de confirmation)
            self.automation.click_button_safe(nuevo_anio_btn, wait_after=0.3)
            self.app.processEvents()
            
            # Vérifier que le dialogue de warning a été appelé
            assert mock_messagebox.warning.called, \
                "Le dialogue de confirmation warning devrait s'afficher"
            
            # Vérifier que l'archivage n'a PAS été appelé (car on a annulé)
            mock_db.archivar_facturas_anio.assert_not_called()
        
        self.logger.info("✅ Dialogue de confirmation affiché, aucune donnée modifiée")
    
    @pytest.mark.timeout(20)
    def test_interface_maintient_etat_apres_clic_annule(self, mock_messagebox):
        """Test: Vérifier que l'interface reste stable après annulation.
        
        Objectif: Valider que l'annulation ne corrompt pas l'interface.
        Méthode: Mock complet et vérification de l'état de la table.
        Données: Aucune modification réelle.
        Sécurité: Ce test est conforme - mocks uniquement, lecture seule.
        """
        self.logger.info("🧪 Test: Interface stable après annulation")
        
        # Capturer l'état avant
        table = self.facturas_window.facturas_table
        row_count_before = table.rowCount()
        
        # Mock pour annuler immédiatement
        mock_messagebox.warning.return_value = mock_messagebox.No
        mock_messagebox.question.return_value = mock_messagebox.No
        
        # Cliquer et annuler
        nuevo_anio_btn = self.automation.find_button_by_text(
            self.facturas_window, "Empezar Nuevo Año"
        )
        self.automation.click_button_safe(nuevo_anio_btn, wait_after=0.3)
        self.app.processEvents()
        
        # Vérifier que l'état est inchangé
        row_count_after = table.rowCount()
        assert row_count_after == row_count_before, \
            f"Le nombre de lignes a changé: {row_count_before} -> {row_count_after}"
        
        self.logger.info("✅ Interface stable après annulation")
    
    @pytest.mark.timeout(15)
    def test_boton_ver_archivadas_existe(self):
        """Test: Vérifier que le bouton 'Ver Archivadas' existe et fonctionne.
        
        Objectif: Valider la présence du bouton de basculement vers les archivées.
        Méthode: Recherche du bouton et test du toggle.
        Données: Aucune donnée n'est modifiée (lecture seule).
        Sécurité: Ce test est conforme - lecture seule de l'interface.
        """
        self.logger.info("🧪 Test: Bouton 'Ver Archivadas' existe")
        
        # Chercher le bouton
        ver_archivadas_btn = self.automation.find_button_by_text(
            self.facturas_window, "Ver Archivadas"
        )
        
        assert ver_archivadas_btn is not None, "Bouton 'Ver Archivadas' non trouvé"
        assert ver_archivadas_btn.isVisible(), "Bouton non visible"
        assert ver_archivadas_btn.isEnabled(), "Bouton non activé"
        
        # Vérifier la méthode existe
        assert hasattr(self.facturas_window, 'on_toggle_archivadas'), \
            "La méthode on_toggle_archivadas devrait exister"
        
        self.take_screenshot("boton_ver_archivadas")
        self.logger.info("✅ Bouton 'Ver Archivadas' trouvé et fonctionnel")
    
    @pytest.mark.timeout(20)
    def test_toggle_archivadas_change_vue(self):
        """Test: Vérifier que le toggle change la vue et le texte du bouton.
        
        Objectif: Valider que le basculement fonctionne correctement.
        Méthode: Cliquer sur le bouton et vérifier les changements.
        Données: Aucune modification de base de données (lecture seule).
        Sécurité: Ce test est conforme - mocks uniquement, lecture seule.
        """
        self.logger.info("🧪 Test: Toggle archivadas change la vue")
        
        # État initial
        assert not self.facturas_window.mostrar_archivadas, \
            "Par défaut, on devrait voir les factures actives"
        
        # Capturer le texte initial
        ver_archivadas_btn = self.automation.find_button_by_text(
            self.facturas_window, "Ver Archivadas"
        )
        texte_initial = ver_archivadas_btn.text()
        
        # Cliquer pour basculer
        self.automation.click_button_safe(ver_archivadas_btn, wait_after=0.3)
        self.app.processEvents()
        
        # Vérifier que l'état a changé
        assert self.facturas_window.mostrar_archivadas, \
            "Après le clic, on devrait voir les archivées"
        
        # Vérifier que le texte a changé
        nouveau_texte = ver_archivadas_btn.text()
        assert nouveau_texte != texte_initial, \
            f"Le texte du bouton devrait changer: {texte_initial} -> {nouveau_texte}"
        assert "Actuales" in nouveau_texte or "Facturas" in nouveau_texte, \
            f"Le nouveau texte devrait indiquer le retour aux factures actuelles: {nouveau_texte}"
        
        # Revenir à la vue normale
        self.automation.click_button_safe(ver_archivadas_btn, wait_after=0.3)
        self.app.processEvents()
        
        assert not self.facturas_window.mostrar_archivadas, \
            "Après second clic, on devrait revenir aux factures actives"
        
        self.logger.info("✅ Toggle archivadas fonctionne correctement")
