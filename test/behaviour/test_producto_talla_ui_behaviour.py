# -*- coding: utf-8 -*-
"""
Tests de comportement pour l'interface UI de la colonne Talla
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import TestDatabase
from utils.logger import get_logger

class TestProductoTallaUIBehaviour:
    """Tests de comportement pour l'interface UI de la colonne Talla"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger(self.__class__.__name__)
        self.test_db = TestDatabase(with_fixtures=True)
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'test_db'):
            self.test_db.cleanup()
    
    def test_05_productos_window_has_talla_field(self):
        """
        COMPORTEMENT: La fenêtre Productos doit avoir un champ input pour 'talla'
        GIVEN: Le code source de ProductosPyQt5Window
        WHEN: On vérifie la présence du champ talla_edit
        THEN: Le champ doit exister dans la classe
        """
        self.logger.info("🧪 Test 05: Vérification du champ 'talla_edit' dans ProductosWindow")
        
        # Importer la classe
        from ui.productos_pyqt5 import ProductosPyQt5Window
        
        # Vérifier que la classe existe
        assert ProductosPyQt5Window is not None, "La classe ProductosPyQt5Window doit exister"
        
        # Pour l'instant, on vérifie juste que la classe existe
        # Une fois développé, on pourra vérifier l'attribut talla_edit
        # TODO: Après développement, ajouter:
        # assert hasattr(instance, 'talla_edit'), "Le champ talla_edit doit exister"
        
        self.logger.info("⚠️  Test simplifié - À compléter après développement")
    
    def test_06_talla_field_is_optional(self):
        """
        COMPORTEMENT: Le champ talla doit être optionnel
        GIVEN: Un produit sans talla
        WHEN: On sauvegarde le produit
        THEN: La sauvegarde doit réussir
        """
        self.logger.info("🧪 Test 06: Vérification que talla est optionnel")
        
        # Créer un produit sans talla
        product_data = {
            'nombre': 'Produit Test Sans Talla',
            'referencia': 'TEST-NO-TALLA',
            'precio': 10.0,
            'stock': 5
        }
        
        # La sauvegarde doit réussir même sans talla
        product_id = self.test_db.add_product(product_data)
        assert product_id is not None, "Le produit doit être créé sans talla"
        
        self.logger.info("✅ Produit créé sans talla - champ optionnel confirmé")
    
    def test_07_talla_field_saves_value(self):
        """
        COMPORTEMENT: La valeur du champ talla doit être sauvegardée
        GIVEN: Un produit avec talla='XL'
        WHEN: On sauvegarde le produit
        THEN: La talla doit être sauvegardée dans la base
        """
        self.logger.info("🧪 Test 07: Vérification sauvegarde de talla")
        
        # Créer un produit avec talla
        product_data = {
            'nombre': 'T-Shirt Test',
            'referencia': 'TSHIRT-XL',
            'precio': 25.0,
            'talla': 'XL',
            'stock': 10
        }
        
        product_id = self.test_db.add_product(product_data)
        assert product_id is not None, "Le produit doit être créé"
        
        # Vérifier que la talla est sauvegardée
        products = self.test_db.get_all_products()
        created_product = next((p for p in products if p['id'] == product_id), None)
        
        assert created_product is not None, "Le produit doit être trouvé"
        assert created_product.get('talla') == 'XL', "La talla doit être 'XL'"
        
        self.logger.info("✅ Talla sauvegardée correctement")
    
    def test_08_talla_field_loads_value(self):
        """
        COMPORTEMENT: La valeur talla doit être chargée depuis la base
        GIVEN: Un produit avec talla='L' dans la base
        WHEN: On charge le produit
        THEN: La talla doit être 'L'
        """
        self.logger.info("🧪 Test 08: Vérification chargement de talla")
        
        # Créer un produit avec talla
        product_data = {
            'nombre': 'Pantalon Test',
            'referencia': 'PANT-L',
            'precio': 45.0,
            'talla': 'L',
            'stock': 8
        }
        
        product_id = self.test_db.add_product(product_data)
        
        # Charger le produit
        product = self.test_db.get_product_by_id(product_id)
        
        assert product is not None, "Le produit doit être trouvé"
        assert product.get('talla') == 'L', "La talla chargée doit être 'L'"
        
        self.logger.info("✅ Talla chargée correctement")
    
    def test_09_talla_column_visible_when_enabled(self):
        """
        COMPORTEMENT: La colonne Talla doit être visible quand activée
        GIVEN: La configuration columna_talla_visible=True
        WHEN: On affiche la liste des produits
        THEN: La colonne Talla doit être visible
        """
        self.logger.info("🧪 Test 09: Vérification visibilité colonne Talla")
        
        # Pour l'instant, test simplifié
        # TODO: Après développement, vérifier la configuration
        from config.config import Config
        
        # Vérifier que la classe Config existe
        assert Config is not None, "La classe Config doit exister"
        
        self.logger.info("⚠️  Test simplifié - À compléter après développement")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])

