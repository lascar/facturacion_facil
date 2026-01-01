# -*- coding: utf-8 -*-
"""
Test de comportement pour la hauteur minimale de la liste des factures
"""

import pytest
from PyQt5.QtWidgets import QTableWidget
from test.behaviour.base_behaviour_test import BaseBehaviourTest


class TestFacturasListMinimumHeight(BaseBehaviourTest):
    """Tests de comportement pour la hauteur minimale de la liste des factures"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox, mock_filedialog):
        """Configuration automatique pour chaque test"""
        # Initialiser les attributs de la classe de base
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir

        # Ouvrir la fenêtre Facturas
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        self.facturas_window = FacturasPyQt5Window()
        self.facturas_window.show()
        self.app.processEvents()

        yield

        # Nettoyage
        if hasattr(self, 'facturas_window') and self.facturas_window:
            self.facturas_window.close()
            self.app.processEvents()
    
    @pytest.mark.timeout(10)
    def test_facturas_table_has_minimum_height(self):
        """
        COMPORTEMENT: La table des factures doit avoir une hauteur minimale pour afficher 6 lignes
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On vérifie la hauteur minimale de la table
        THEN: La hauteur minimale doit être d'au moins 300px
        """
        self.logger.info("🧪 Test: Hauteur minimale de la table des factures")

        # Vérifier que la table existe
        assert hasattr(self.facturas_window, 'facturas_table'), "La table des factures doit exister"
        assert isinstance(self.facturas_window.facturas_table, QTableWidget), "facturas_table doit être un QTableWidget"

        # Vérifier la hauteur minimale
        min_height = self.facturas_window.facturas_table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale de la table: {min_height}px")

        # La hauteur minimale doit être d'au moins 300px
        # (header ~40-50px + 6 lignes × ~35-40px + marges ~20px = 300px)
        # Windows nécessite plus d'espace que Linux
        assert min_height >= 300, f"La hauteur minimale doit être d'au moins 300px, trouvé: {min_height}px"

        self.logger.info("✅ La table a une hauteur minimale correcte pour afficher 6 lignes")
    
    @pytest.mark.timeout(10)
    def test_facturas_table_displays_at_least_6_rows_visually(self):
        """
        COMPORTEMENT: La table doit pouvoir afficher au moins 6 lignes sans scroll
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On calcule le nombre de lignes visibles
        THEN: Au moins 6 lignes doivent être visibles
        """
        self.logger.info("🧪 Test: Nombre de lignes visibles dans la table")
        
        table = self.facturas_window.facturas_table
        
        # Obtenir la hauteur de la table
        table_height = table.height()
        self.logger.info(f"📏 Hauteur actuelle de la table: {table_height}px")
        
        # Obtenir la hauteur d'une ligne (row height)
        row_height = table.rowHeight(0) if table.rowCount() > 0 else 30  # 30px par défaut
        self.logger.info(f"📏 Hauteur d'une ligne: {row_height}px")
        
        # Obtenir la hauteur du header
        header_height = table.horizontalHeader().height()
        self.logger.info(f"📏 Hauteur du header: {header_height}px")
        
        # Calculer le nombre de lignes visibles
        # (hauteur_table - hauteur_header) / hauteur_ligne
        visible_area = table_height - header_height
        visible_rows = visible_area // row_height
        
        self.logger.info(f"📊 Nombre de lignes visibles calculé: {visible_rows}")
        
        # Au moins 6 lignes doivent être visibles
        assert visible_rows >= 6, f"Au moins 6 lignes doivent être visibles, trouvé: {visible_rows}"
        
        self.logger.info("✅ La table peut afficher au moins 6 lignes sans scroll")
    
    @pytest.mark.timeout(10)
    def test_facturas_table_minimum_height_persists_after_resize(self):
        """
        COMPORTEMENT: La hauteur minimale doit persister même après redimensionnement
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On redimensionne la fenêtre
        THEN: La hauteur minimale de la table doit rester >= 220px
        """
        self.logger.info("🧪 Test: Persistance de la hauteur minimale après redimensionnement")
        
        table = self.facturas_window.facturas_table
        
        # Vérifier la hauteur minimale initiale
        initial_min_height = table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale initiale: {initial_min_height}px")
        
        # Redimensionner la fenêtre (plus petite)
        self.facturas_window.resize(800, 400)
        self.app.processEvents()
        
        # Vérifier que la hauteur minimale n'a pas changé
        min_height_after_resize = table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale après redimensionnement: {min_height_after_resize}px")
        
        assert min_height_after_resize == initial_min_height, \
            f"La hauteur minimale doit rester constante: {initial_min_height}px, trouvé: {min_height_after_resize}px"
        
        assert min_height_after_resize >= 220, \
            f"La hauteur minimale doit rester >= 220px, trouvé: {min_height_after_resize}px"
        
        self.logger.info("✅ La hauteur minimale persiste après redimensionnement")

