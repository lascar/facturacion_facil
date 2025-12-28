"""
Tests de comportement pour la hauteur minimale de la liste des produits dans factura
"""
import pytest
from PyQt5.QtWidgets import QTableWidget
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from ui.facturas_pyqt5 import FacturasPyQt5Window


class TestProductosListMinimumHeight(BaseBehaviourTest):
    """Tests de comportement pour la hauteur minimale de la liste des produits"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir):
        """Setup pour chaque test"""
        # Initialiser les attributs de la classe de base
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir

        # Créer la fenêtre Facturas
        self.facturas_window = FacturasPyQt5Window()
        self.facturas_window.show()
        self.app.processEvents()

        yield

        # Nettoyage
        if hasattr(self, 'facturas_window') and self.facturas_window:
            self.facturas_window.close()
            self.facturas_window.deleteLater()
            self.app.processEvents()
    
    @pytest.mark.timeout(10)
    def test_productos_table_has_minimum_height(self):
        """
        COMPORTEMENT: La table des produits doit avoir une hauteur minimale pour afficher 4 lignes
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On vérifie la hauteur minimale de la table des produits
        THEN: La hauteur minimale doit être d'au moins 220px
        """
        self.logger.info("🧪 Test: Hauteur minimale de la table des produits")
        
        # Vérifier que la table existe
        assert hasattr(self.facturas_window, 'productos_table'), "La table des produits doit exister"
        assert isinstance(self.facturas_window.productos_table, QTableWidget), "productos_table doit être un QTableWidget"
        
        # Vérifier la hauteur minimale
        min_height = self.facturas_window.productos_table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale de la table: {min_height}px")
        
        # La hauteur minimale doit être d'au moins 220px
        # (header ~40-50px + 4 lignes × ~35-40px + marges ~20px = 220px)
        # Windows nécessite plus d'espace que Linux
        assert min_height >= 220, f"La hauteur minimale doit être d'au moins 220px, trouvé: {min_height}px"
        
        self.logger.info("✅ La table a une hauteur minimale correcte pour afficher 4 lignes")
    
    @pytest.mark.timeout(10)
    def test_productos_table_displays_at_least_4_rows_visually(self):
        """
        COMPORTEMENT: La table doit pouvoir afficher au moins 4 lignes sans scroll
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On calcule le nombre de lignes visibles
        THEN: Au moins 4 lignes doivent être visibles
        """
        self.logger.info("🧪 Test: Nombre de lignes visibles dans la table des produits")
        
        # Obtenir les dimensions de la table
        table_height = self.facturas_window.productos_table.height()
        self.logger.info(f"📏 Hauteur actuelle de la table: {table_height}px")
        
        # Obtenir la hauteur d'une ligne
        row_height = self.facturas_window.productos_table.rowHeight(0) if self.facturas_window.productos_table.rowCount() > 0 else 30
        self.logger.info(f"📏 Hauteur d'une ligne: {row_height}px")
        
        # Obtenir la hauteur du header
        header_height = self.facturas_window.productos_table.horizontalHeader().height()
        self.logger.info(f"📏 Hauteur du header: {header_height}px")
        
        # Calculer le nombre de lignes visibles
        # (hauteur_table - hauteur_header) / hauteur_ligne
        visible_area = table_height - header_height
        visible_rows = visible_area // row_height
        
        self.logger.info(f"📊 Nombre de lignes visibles calculé: {visible_rows}")
        
        # Au moins 4 lignes doivent être visibles
        assert visible_rows >= 4, f"Au moins 4 lignes doivent être visibles, trouvé: {visible_rows}"
        
        self.logger.info("✅ La table affiche au moins 4 lignes visibles")
    
    @pytest.mark.timeout(10)
    def test_productos_table_minimum_height_persists_after_resize(self):
        """
        COMPORTEMENT: La hauteur minimale doit persister après redimensionnement
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On redimensionne la fenêtre
        THEN: La hauteur minimale de la table doit rester >= 220px
        """
        self.logger.info("🧪 Test: Persistance de la hauteur minimale après redimensionnement")
        
        # Hauteur minimale initiale
        initial_min_height = self.facturas_window.productos_table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale initiale: {initial_min_height}px")
        
        # Redimensionner la fenêtre (plus petite)
        self.facturas_window.resize(600, 400)
        self.app.processEvents()
        
        # Vérifier que la hauteur minimale n'a pas changé
        min_height_after_resize = self.facturas_window.productos_table.minimumHeight()
        self.logger.info(f"📏 Hauteur minimale après redimensionnement: {min_height_after_resize}px")
        
        assert min_height_after_resize == initial_min_height, \
            f"La hauteur minimale doit rester constante: {initial_min_height}px, trouvé: {min_height_after_resize}px"
        
        assert min_height_after_resize >= 220, \
            f"La hauteur minimale doit rester >= 220px, trouvé: {min_height_after_resize}px"
        
        self.logger.info("✅ La hauteur minimale persiste après redimensionnement")

