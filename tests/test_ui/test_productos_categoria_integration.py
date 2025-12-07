#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour la gestion des catégories dans l'interface produits.

Ce test valide l'intégration complète entre l'interface utilisateur et la base de données
pour la gestion des catégories de produits.
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ui.productos_pyqt5 import ProductosPyQt5Window
from database.database_improved import DatabaseImproved


class TestProductosCategoriaIntegration:
    """Tests d'intégration pour la gestion des catégories dans l'interface produits."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Configuration pour chaque test."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # Créer une base de données temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, 'test_facturacion.db')
        
        # Patcher le chemin de la base de données
        self.db_patcher = patch('database.database_improved.DatabaseImproved.DB_PATH', self.test_db_path)
        self.db_patcher.start()
        
        # Initialiser la base de données de test
        self.db = DatabaseImproved()
        
    def teardown_method(self):
        """Nettoyage après chaque test."""
        self.db_patcher.stop()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_categoria_display_with_real_data(self):
        """Test d'intégration: Affichage des catégories avec des données réelles."""
        # Arrange - Créer des produits avec différentes catégories
        test_products = [
            {
                'nombre': 'Laptop Gaming',
                'referencia': 'LAP001',
                'precio_venta': 1299.99,
                'categoria': 'Electrónicos',
                'descripcion': 'Laptop para gaming',
                'iva_recomendado': 21.0,
                'stock': 5
            },
            {
                'nombre': 'Consultoría IT',
                'referencia': 'CONS001',
                'precio_venta': 150.00,
                'categoria': 'Servicios',
                'descripcion': 'Servicio de consultoría',
                'iva_recomendado': 21.0,
                'stock': 0
            },
            {
                'nombre': 'Producto Sin Categoría',
                'referencia': 'SIN001',
                'precio_venta': 25.00,
                'categoria': None,
                'descripcion': 'Producto sin categoría',
                'iva_recomendado': 21.0,
                'stock': 10
            }
        ]
        
        # Ajouter les produits à la base de données
        product_ids = []
        for product_data in test_products:
            product_id = self.db.add_product(product_data)
            product_ids.append(product_id)
        
        # Act - Créer la fenêtre et charger les données
        window = ProductosPyQt5Window()
        window.load_data()
        
        # Assert - Vérifier l'affichage dans la table
        assert window.products_table.rowCount() == 3, "La table doit contenir 3 produits"
        
        # Vérifier les catégories dans la table (colonne 5)
        categoria_col = 5
        row_0_categoria = window.products_table.item(0, categoria_col).text()
        row_1_categoria = window.products_table.item(1, categoria_col).text()
        row_2_categoria = window.products_table.item(2, categoria_col).text()
        
        # Les catégories doivent être affichées correctement
        displayed_categories = [row_0_categoria, row_1_categoria, row_2_categoria]
        assert 'Electrónicos' in displayed_categories
        assert 'Servicios' in displayed_categories
        assert '' in displayed_categories  # Catégorie vide pour le produit sans catégorie
    
    def test_categoria_combo_loads_from_database(self):
        """Test d'intégration: Le combo catégorie charge les catégories depuis la base de données."""
        # Arrange - Créer des produits avec catégories
        categories_to_create = ['Electrónicos', 'Servicios', 'Material de Oficina']
        
        for i, categoria in enumerate(categories_to_create):
            product_data = {
                'nombre': f'Producto {i+1}',
                'referencia': f'REF{i+1:03d}',
                'precio_venta': 100.0 + i * 10,
                'categoria': categoria,
                'descripcion': f'Producto de categoría {categoria}',
                'iva_recomendado': 21.0,
                'stock': 10
            }
            self.db.add_product(product_data)
        
        # Act - Créer la fenêtre et charger les catégories
        window = ProductosPyQt5Window()
        window.load_categories()
        
        # Assert - Vérifier que les catégories sont dans le combo
        combo_items = []
        for i in range(window.categoria_combo.count()):
            combo_items.append(window.categoria_combo.itemText(i))
        
        # Le combo doit contenir l'option vide plus toutes les catégories
        assert '' in combo_items, "Le combo doit contenir une option vide"
        for categoria in categories_to_create:
            assert categoria in combo_items, f"La catégorie '{categoria}' doit être dans le combo"
    
    def test_product_selection_updates_categoria_form(self):
        """Test d'intégration: La sélection d'un produit met à jour le champ catégorie du formulaire."""
        # Arrange - Créer un produit avec catégorie
        product_data = {
            'nombre': 'Smartphone',
            'referencia': 'PHONE001',
            'precio_venta': 699.99,
            'categoria': 'Electrónicos',
            'descripcion': 'Smartphone dernière génération',
            'iva_recomendado': 21.0,
            'stock': 15
        }
        product_id = self.db.add_product(product_data)
        
        # Act - Créer la fenêtre, charger les données et sélectionner le produit
        window = ProductosPyQt5Window()
        window.load_data()
        
        # Simuler la sélection du premier produit
        window.products_table.selectRow(0)
        window.on_product_selected()
        
        # Assert - Vérifier que le formulaire affiche la bonne catégorie
        selected_categoria = window.categoria_combo.currentText()
        assert selected_categoria == 'Electrónicos', \
            f"Le formulaire doit afficher 'Electrónicos', trouvé: '{selected_categoria}'"
    
    def test_new_categoria_can_be_added_via_combo(self):
        """Test d'intégration: Une nouvelle catégorie peut être ajoutée via le combo éditable."""
        # Arrange
        window = ProductosPyQt5Window()
        window.load_categories()
        
        # Act - Saisir une nouvelle catégorie
        new_categoria = 'Nouvelle Catégorie Test'
        window.categoria_combo.setCurrentText(new_categoria)
        
        # Assert - Vérifier que la nouvelle catégorie est acceptée
        current_text = window.categoria_combo.currentText()
        assert current_text == new_categoria, \
            f"Le combo doit accepter la nouvelle catégorie '{new_categoria}', trouvé: '{current_text}'"
    
    def test_empty_categoria_handling(self):
        """Test d'intégration: Gestion correcte des catégories vides."""
        # Arrange - Créer un produit sans catégorie
        product_data = {
            'nombre': 'Produit Sans Catégorie',
            'referencia': 'NOCAT001',
            'precio_venta': 50.0,
            'categoria': None,
            'descripcion': 'Produit sans catégorie spécifique',
            'iva_recomendado': 21.0,
            'stock': 8
        }
        product_id = self.db.add_product(product_data)
        
        # Act - Créer la fenêtre et charger les données
        window = ProductosPyQt5Window()
        window.load_data()
        
        # Assert - Vérifier l'affichage de la catégorie vide
        categoria_col = 5
        categoria_text = window.products_table.item(0, categoria_col).text()
        assert categoria_text == '', "Une catégorie None doit s'afficher comme chaîne vide"
        
        # Sélectionner le produit et vérifier le formulaire
        window.products_table.selectRow(0)
        window.on_product_selected()
        
        selected_categoria = window.categoria_combo.currentText()
        assert selected_categoria == '', "Le formulaire doit afficher une catégorie vide pour un produit sans catégorie"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
