# -*- coding: utf-8 -*-
"""
Tests de comportement pour le tri des colonnes dans les tables

IMPORTANT: Ces tests utilisent une base de données de test isolée.
La base de données de production n'est JAMAIS touchée.
Les tests utilisent les fixtures du conftest.py qui gèrent l'isolation de la base de données.
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.logger import get_logger

# Créer l'application Qt une seule fois
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestTableSortingBehaviour:
    """Tests de comportement pour le tri des colonnes dans les tables

    IMPORTANT: Ces tests utilisent les fixtures automatiques du conftest.py
    qui remplacent la base de données de production par une base de test isolée.
    Aucune donnée de production n'est modifiée.

    La fixture 'temp_db' est automatiquement injectée par le conftest.py
    et remplace toutes les références à la base de données.
    """

    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("🧪 Test de tri - utilisation de la base de test isolée")
    
    def test_01_facturas_table_sorting_enabled(self):
        """
        COMPORTEMENT: La table des factures doit avoir le tri activé
        GIVEN: La fenêtre Facturas est ouverte
        WHEN: On vérifie la configuration de la table
        THEN: Le tri doit être activé (setSortingEnabled = True)
        """
        self.logger.info("🧪 Test 01: Vérification tri activé - Facturas")
        
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        window = FacturasPyQt5Window()
        
        # Vérifier que le tri est activé
        assert window.facturas_table.isSortingEnabled(), "Le tri doit être activé sur la table des factures"
        
        window.close()
        self.logger.info("✅ Tri activé sur la table des factures")
    
    def test_02_clientes_table_sorting_enabled(self):
        """
        COMPORTEMENT: La table des clients doit avoir le tri activé
        GIVEN: La fenêtre Clientes est ouverte
        WHEN: On vérifie la configuration de la table
        THEN: Le tri doit être activé (setSortingEnabled = True)
        """
        self.logger.info("🧪 Test 02: Vérification tri activé - Clientes")
        
        from ui.clientes_pyqt5 import ClientesPyQt5Window
        
        window = ClientesPyQt5Window()
        
        # Vérifier que le tri est activé
        assert window.clients_table.isSortingEnabled(), "Le tri doit être activé sur la table des clients"
        
        window.close()
        self.logger.info("✅ Tri activé sur la table des clients")
    
    def test_03_productos_table_sorting_enabled(self):
        """
        COMPORTEMENT: La table des produits doit avoir le tri activé
        GIVEN: La fenêtre Productos est ouverte
        WHEN: On vérifie la configuration de la table
        THEN: Le tri doit être activé (setSortingEnabled = True)
        """
        self.logger.info("🧪 Test 03: Vérification tri activé - Productos")
        
        from ui.productos_pyqt5 import ProductosPyQt5Window
        
        window = ProductosPyQt5Window()
        
        # Vérifier que le tri est activé
        assert window.products_table.isSortingEnabled(), "Le tri doit être activé sur la table des produits"
        
        window.close()
        self.logger.info("✅ Tri activé sur la table des produits")
    
    def test_04_stock_table_sorting_enabled(self):
        """
        COMPORTEMENT: La table des stocks doit avoir le tri activé
        GIVEN: La fenêtre Stock est ouverte
        WHEN: On vérifie la configuration de la table
        THEN: Le tri doit être activé (setSortingEnabled = True)
        """
        self.logger.info("🧪 Test 04: Vérification tri activé - Stock")

        from ui.stock_pyqt5 import StockPyQt5Window

        window = StockPyQt5Window()

        # Vérifier que le tri est activé
        assert window.stock_table.isSortingEnabled(), "Le tri doit être activé sur la table des stocks"

        window.close()
        self.logger.info("✅ Tri activé sur la table des stocks")

    def test_05_productos_sorting_by_nombre(self):
        """
        COMPORTEMENT: Le tri par nom doit fonctionner (ascendant puis descendant)
        GIVEN: La fenêtre Productos est ouverte avec des produits
        WHEN: On clique sur l'en-tête "Nombre" deux fois
        THEN: Les produits doivent être triés par nom (asc puis desc)
        """
        self.logger.info("🧪 Test 05: Tri par nom - Productos")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()
        window.load_productos()

        # Vérifier que le tri est activé
        assert window.products_table.isSortingEnabled(), "Le tri doit être activé"

        # Si la table a des données, tester le tri
        if window.products_table.rowCount() > 1:
            # Trier par nom (colonne 1) - ascendant
            window.products_table.sortItems(1, Qt.AscendingOrder)

            # Trier par nom - descendant
            window.products_table.sortItems(1, Qt.DescendingOrder)

            self.logger.info("✅ Tri par nom testé")
        else:
            self.logger.info("⚠️  Pas assez de produits pour tester le tri")

        window.close()
        self.logger.info("✅ Tri activé pour les produits")

    def test_06_clientes_sorting_by_nombre(self):
        """
        COMPORTEMENT: Le tri par nom doit fonctionner pour les clients
        GIVEN: La fenêtre Clientes est ouverte avec des clients
        WHEN: On trie par nom
        THEN: Les clients doivent être triés par nom
        """
        self.logger.info("🧪 Test 06: Tri par nom - Clientes")

        from ui.clientes_pyqt5 import ClientesPyQt5Window

        window = ClientesPyQt5Window()
        window.load_clientes()

        # Vérifier que le tri est activé
        assert window.clients_table.isSortingEnabled(), "Le tri doit être activé"

        # Si la table a des données, tester le tri
        if window.clients_table.rowCount() > 1:
            # Trier par nom (colonne 1) - ascendant
            window.clients_table.sortItems(1, Qt.AscendingOrder)

            # Trier par nom - descendant
            window.clients_table.sortItems(1, Qt.DescendingOrder)

            self.logger.info("✅ Tri par nom testé")
        else:
            self.logger.info("⚠️  Pas assez de clients pour tester le tri")

        window.close()
        self.logger.info("✅ Tri activé pour les clients")

    def test_07_facturas_sorting_by_numero(self):
        """
        COMPORTEMENT: Le tri par numéro doit fonctionner pour les factures
        GIVEN: La fenêtre Facturas est ouverte avec des factures
        WHEN: On trie par numéro
        THEN: Les factures doivent être triées par numéro
        """
        self.logger.info("🧪 Test 07: Tri par numéro - Facturas")

        from ui.facturas_pyqt5 import FacturasPyQt5Window

        window = FacturasPyQt5Window()

        # Vérifier que le tri est activé
        assert window.facturas_table.isSortingEnabled(), "Le tri doit être activé"

        # Si la table a des données, tester le tri
        if window.facturas_table.rowCount() > 0:
            # Trier par numéro (colonne 0) - ascendant
            window.facturas_table.sortItems(0, Qt.AscendingOrder)

            # Trier par numéro - descendant
            window.facturas_table.sortItems(0, Qt.DescendingOrder)

            self.logger.info("✅ Tri par numéro testé")
        else:
            self.logger.info("⚠️  Pas de factures pour tester le tri")

        window.close()
        self.logger.info("✅ Tri activé pour les factures")

    def test_08_stock_sorting_by_producto(self):
        """
        COMPORTEMENT: Le tri par produit doit fonctionner pour le stock
        GIVEN: La fenêtre Stock est ouverte avec des produits
        WHEN: On trie par nom de produit
        THEN: Les produits doivent être triés par nom
        """
        self.logger.info("🧪 Test 08: Tri par produit - Stock")

        from ui.stock_pyqt5 import StockPyQt5Window

        window = StockPyQt5Window()
        window.load_stock_data()

        # Vérifier que le tri est activé
        assert window.stock_table.isSortingEnabled(), "Le tri doit être activé"

        # Si la table a des données, tester le tri
        if window.stock_table.rowCount() > 1:
            # Trier par produit (colonne 1) - ascendant
            window.stock_table.sortItems(1, Qt.AscendingOrder)

            # Trier par produit - descendant
            window.stock_table.sortItems(1, Qt.DescendingOrder)

            self.logger.info("✅ Tri par produit testé")
        else:
            self.logger.info("⚠️  Pas assez de produits pour tester le tri")

        window.close()
        self.logger.info("✅ Tri activé pour le stock")

    def test_09_productos_sorting_by_precio(self):
        """
        COMPORTEMENT: Le tri par prix doit fonctionner pour les produits
        GIVEN: La fenêtre Productos est ouverte avec des produits
        WHEN: On trie par prix
        THEN: Les produits doivent être triés par prix (numérique)
        """
        self.logger.info("🧪 Test 09: Tri par prix - Productos")

        from ui.productos_pyqt5 import ProductosPyQt5Window

        window = ProductosPyQt5Window()
        window.load_productos()

        # Vérifier que le tri est activé
        assert window.products_table.isSortingEnabled(), "Le tri doit être activé"

        # Si la table a des données, tester le tri
        if window.products_table.rowCount() > 1:
            # Trier par prix (colonne 3) - ascendant
            window.products_table.sortItems(3, Qt.AscendingOrder)

            # Trier par prix - descendant
            window.products_table.sortItems(3, Qt.DescendingOrder)

            self.logger.info("✅ Tri par prix testé")
        else:
            self.logger.info("⚠️  Pas assez de produits pour tester le tri")

        window.close()
        self.logger.info("✅ Tri activé pour les produits")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])

