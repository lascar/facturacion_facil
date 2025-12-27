# -*- coding: utf-8 -*-
"""
Tests de comportement pour la fenêtre Productos - Layout et organisation
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QScrollArea

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import TestDatabase
from utils.logger import get_logger

# Créer l'application Qt une seule fois
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestProductosWindowLayoutBehaviour:
    """Tests de comportement pour le layout de la fenêtre Productos"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger(self.__class__.__name__)
        self.test_db = TestDatabase(with_fixtures=True)
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'test_db'):
            self.test_db.cleanup()
    
    def test_01_productos_window_opens(self):
        """
        COMPORTEMENT: La fenêtre Productos doit s'ouvrir correctement
        GIVEN: L'application est lancée
        WHEN: On ouvre la fenêtre Productos
        THEN: La fenêtre doit s'ouvrir sans erreur
        """
        self.logger.info("🧪 Test 01: Ouverture de la fenêtre Productos")
        
        from ui.productos_pyqt5 import ProductosPyQt5Window
        
        window = ProductosPyQt5Window()
        assert window is not None, "La fenêtre doit être créée"
        
        window.close()
        self.logger.info("✅ Fenêtre Productos ouverte avec succès")
    
    def test_02_form_has_all_fields(self):
        """
        COMPORTEMENT: Le formulaire doit avoir tous les champs requis
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie les champs du formulaire
        THEN: Tous les champs doivent être présents
        """
        self.logger.info("🧪 Test 02: Vérification des champs du formulaire")
        
        from ui.productos_pyqt5 import ProductosPyQt5Window
        
        window = ProductosPyQt5Window()
        
        # Vérifier tous les champs
        assert hasattr(window, 'nombre_edit'), "Le champ nombre_edit doit exister"
        assert hasattr(window, 'referencia_edit'), "Le champ referencia_edit doit exister"
        assert hasattr(window, 'categoria_combo'), "Le champ categoria_combo doit exister"
        assert hasattr(window, 'precio_edit'), "Le champ precio_edit doit exister"
        assert hasattr(window, 'iva_edit'), "Le champ iva_edit doit exister"
        assert hasattr(window, 'talla_edit'), "Le champ talla_edit doit exister"
        assert hasattr(window, 'stock_edit'), "Le champ stock_edit doit exister"
        assert hasattr(window, 'descripcion_edit'), "Le champ descripcion_edit doit exister"
        
        window.close()
        self.logger.info("✅ Tous les champs sont présents")
    
    def test_03_referencia_categoria_talla_on_same_line(self):
        """
        COMPORTEMENT: Referencia, Categoría et Talla doivent être sur la même ligne
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie le layout du formulaire
        THEN: Referencia, Categoría et Talla doivent être dans un QHBoxLayout
        """
        self.logger.info("🧪 Test 03: Vérification Referencia, Categoría et Talla sur la même ligne")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier que les widgets existent
        assert window.referencia_edit is not None, "referencia_edit doit exister"
        assert window.categoria_combo is not None, "categoria_combo doit exister"
        assert window.talla_edit is not None, "talla_edit doit exister"

        # Vérifier que le parent du referencia_edit contient aussi categoria_combo et talla_edit
        # (ils doivent être dans le même layout horizontal)
        ref_parent = window.referencia_edit.parent()
        cat_parent = window.categoria_combo.parent()
        talla_parent = window.talla_edit.parent()

        # Les trois doivent avoir le même parent (le widget contenant le QHBoxLayout)
        assert ref_parent == cat_parent, "Referencia et Categoría doivent avoir le même parent"
        assert ref_parent == talla_parent, "Referencia et Talla doivent avoir le même parent"

        window.close()
        self.logger.info("✅ Referencia, Categoría et Talla sont sur la même ligne")
    
    def test_04_form_is_scrollable(self):
        """
        COMPORTEMENT: Le formulaire doit être scrollable
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie le conteneur du formulaire
        THEN: Le formulaire doit être dans un QScrollArea
        """
        self.logger.info("🧪 Test 04: Vérification que le formulaire est scrollable")
        
        from ui.productos_pyqt5 import ProductosPyQt5Window
        
        window = ProductosPyQt5Window()
        
        # Chercher un QScrollArea dans la fenêtre
        scroll_areas = window.findChildren(QScrollArea)
        
        assert len(scroll_areas) > 0, "Il doit y avoir au moins un QScrollArea"
        
        window.close()
        self.logger.info("✅ Le formulaire est scrollable")
    
    def test_05_no_facturas_table(self):
        """
        COMPORTEMENT: Il ne doit PAS y avoir de table des factures
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie les attributs de la fenêtre
        THEN: Il ne doit pas y avoir d'attribut facturas_table
        """
        self.logger.info("🧪 Test 05: Vérification absence de table des factures")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier qu'il n'y a PAS de table des factures
        assert not hasattr(window, 'facturas_table'), "Il ne doit PAS y avoir de facturas_table"

        window.close()
        self.logger.info("✅ Pas de table des factures (comme demandé)")

    def test_06_precio_iva_on_same_line(self):
        """
        COMPORTEMENT: Precio et IVA doivent être sur la même ligne
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie le layout du formulaire
        THEN: Precio et IVA doivent avoir le même parent
        """
        self.logger.info("🧪 Test 06: Vérification Precio et IVA sur la même ligne")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier que les widgets existent
        assert window.precio_edit is not None, "precio_edit doit exister"
        assert window.iva_edit is not None, "iva_edit doit exister"

        # Vérifier que les deux ont le même parent
        precio_parent = window.precio_edit.parent()
        iva_parent = window.iva_edit.parent()

        assert precio_parent == iva_parent, "Precio et IVA doivent avoir le même parent"

        window.close()
        self.logger.info("✅ Precio et IVA sont sur la même ligne")

    def test_07_talla_stock_on_same_line(self):
        """
        COMPORTEMENT: Talla et Stock doivent être sur la même ligne
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie le layout du formulaire
        THEN: Talla et Stock doivent avoir le même parent
        """
        self.logger.info("🧪 Test 07: Vérification Talla et Stock sur la même ligne")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier que les widgets existent
        assert window.talla_edit is not None, "talla_edit doit exister"
        assert window.stock_edit is not None, "stock_edit doit exister"

        # Vérifier que les deux ont le même parent
        talla_parent = window.talla_edit.parent()
        stock_parent = window.stock_edit.parent()

        assert talla_parent == stock_parent, "Talla et Stock doivent avoir le même parent"

        window.close()
        self.logger.info("✅ Talla et Stock sont sur la même ligne")

    def test_08_products_table_exists(self):
        """
        COMPORTEMENT: La table des produits doit exister
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie les attributs de la fenêtre
        THEN: La table products_table doit exister
        """
        self.logger.info("🧪 Test 08: Vérification de la table des produits")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier que la table des produits existe
        assert hasattr(window, 'products_table'), "La table products_table doit exister"
        assert window.products_table is not None, "products_table ne doit pas être None"

        window.close()
        self.logger.info("✅ La table des produits existe")

    def test_09_products_table_has_talla_column(self):
        """
        COMPORTEMENT: La table des produits doit avoir une colonne Talla
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie les colonnes de la table
        THEN: La colonne Talla doit être présente
        """
        self.logger.info("🧪 Test 09: Vérification de la colonne Talla dans la table")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()

        # Vérifier les headers de la table
        expected_headers = ["ID", "Nombre", "Referencia", "Precio", "Talla", "Stock", "Categoría"]
        actual_headers = []
        for col in range(window.products_table.columnCount()):
            header_item = window.products_table.horizontalHeaderItem(col)
            if header_item:
                actual_headers.append(header_item.text())

        assert actual_headers == expected_headers, f"Headers incorrects: {actual_headers}"
        assert "Talla" in actual_headers, "La colonne Talla doit être présente"

        window.close()
        self.logger.info("✅ La colonne Talla est présente dans la table")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])

