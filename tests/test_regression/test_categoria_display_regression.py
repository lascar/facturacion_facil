#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour l'affichage des catégories dans l'interface de gestion des produits.

Ce test vérifie que les corrections appliquées pour résoudre le problème de visibilité
des catégories restent fonctionnelles et évite les régressions futures.

Problème résolu: "la catégorie du produit n'est pas dans la fenetre de gauche ni de droite de gestion de producto"
Solution: Configuration optimisée des largeurs de colonnes dans la table des produits.

Ce test peut être exécuté avec pytest ou directement avec Python.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QHeaderView

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ui.productos_pyqt5 import ProductosPyQt5Window

# Import conditionnel de pytest
try:
    import pytest
    from unittest.mock import patch, MagicMock
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


class TestCategoriaDisplayRegression:
    """Tests de régression pour l'affichage des catégories dans l'interface produits."""

    def setup_method(self):
        """Configuration pour chaque test."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

    if PYTEST_AVAILABLE:
        setup_method = pytest.fixture(autouse=True)(setup_method)
    
    def test_categoria_column_exists_in_table_headers(self):
        """Test de régression: Vérifier que la colonne 'Categoría' existe dans les headers de la table."""
        # Arrange
        window = ProductosPyQt5Window()
        
        # Act
        headers = []
        for col in range(window.products_table.columnCount()):
            header = window.products_table.horizontalHeaderItem(col)
            if header:
                headers.append(header.text())
        
        # Assert
        assert "Categoría" in headers, "La colonne 'Categoría' doit être présente dans les headers de la table"
        categoria_index = headers.index("Categoría")
        assert categoria_index == 5, f"La colonne 'Categoría' doit être à l'index 5, trouvée à l'index {categoria_index}"
    
    def test_categoria_column_resize_mode_configured(self):
        """Test de régression: Vérifier que la colonne 'Categoría' a le bon mode de redimensionnement."""
        # Arrange
        window = ProductosPyQt5Window()
        header = window.products_table.horizontalHeader()
        
        # Act
        categoria_resize_mode = header.sectionResizeMode(5)  # Index 5 = Categoría
        
        # Assert
        assert categoria_resize_mode == QHeaderView.ResizeToContents, \
            f"La colonne 'Categoría' doit avoir le mode ResizeToContents, trouvé: {categoria_resize_mode}"
    
    def test_categoria_combo_exists_in_form(self):
        """Test de régression: Vérifier que le champ categoria_combo existe dans le formulaire."""
        # Arrange
        window = ProductosPyQt5Window()
        
        # Act & Assert
        assert hasattr(window, 'categoria_combo'), "Le champ 'categoria_combo' doit exister dans le formulaire"
        assert window.categoria_combo.isEditable(), "Le combo 'categoria_combo' doit être éditable"
    
    def test_categoria_combo_placeholder_configured(self):
        """Test de régression: Vérifier que le placeholder du combo catégorie est configuré."""
        # Arrange
        window = ProductosPyQt5Window()
        
        # Act
        placeholder = window.categoria_combo.lineEdit().placeholderText()
        
        # Assert
        expected_placeholder = "Escribir categoría o dejar vacío"
        assert placeholder == expected_placeholder, \
            f"Le placeholder doit être '{expected_placeholder}', trouvé: '{placeholder}'"
    
    def test_categoria_data_flow_in_table_update(self):
        """Test de régression: Vérifier que les données de catégorie sont correctement affichées dans la table."""
        # Arrange
        window = ProductosPyQt5Window()
        
        # Mock des données de produits avec catégories
        mock_productos = [
            {
                'id': 1,
                'nombre': 'Producto Test 1',
                'referencia': 'REF001',
                'precio_venta': 100.0,
                'stock_actual': 10,
                'categoria': 'Electrónicos'
            },
            {
                'id': 2,
                'nombre': 'Producto Test 2',
                'referencia': 'REF002',
                'precio_venta': 50.0,
                'stock_actual': 5,
                'categoria': 'Servicios'
            },
            {
                'id': 3,
                'nombre': 'Producto Test 3',
                'referencia': 'REF003',
                'precio_venta': 25.0,
                'stock_actual': 0,
                'categoria': None  # Catégorie vide
            }
        ]
        
        # Act
        window.productos = mock_productos
        window.update_products_table()
        
        # Assert
        assert window.products_table.rowCount() == 3, "La table doit contenir 3 lignes"
        
        # Vérifier les catégories dans la table (colonne 5)
        categoria_col = 5
        assert window.products_table.item(0, categoria_col).text() == 'Electrónicos'
        assert window.products_table.item(1, categoria_col).text() == 'Servicios'
        assert window.products_table.item(2, categoria_col).text() == ''  # None devient chaîne vide
    
    def test_categoria_combo_loads_existing_categories(self):
        """Test de régression: Vérifier que le combo charge les catégories existantes."""
        # Arrange
        window = ProductosPyQt5Window()

        # Act - Charger les catégories (utilise la vraie base de données)
        window.load_categories()

        # Assert - Vérifier que le combo contient au moins l'option vide
        combo_items = []
        for i in range(window.categoria_combo.count()):
            combo_items.append(window.categoria_combo.itemText(i))

        # Le combo doit contenir au moins l'option vide
        assert '' in combo_items, "Le combo doit contenir une option vide"

        # Si il y a des catégories en base, elles doivent être chargées
        print(f"   📋 Catégories chargées: {combo_items}")
    
    def test_no_default_categories_regression(self):
        """Test de régression: Vérifier qu'aucune catégorie par défaut n'est ajoutée."""
        # Arrange
        window = ProductosPyQt5Window()

        # Act
        window.load_categories()

        # Assert
        combo_items = []
        for i in range(window.categoria_combo.count()):
            combo_items.append(window.categoria_combo.itemText(i))

        # Ne doit contenir que l'option vide et les catégories existantes, pas de catégories par défaut
        forbidden_categories = ['Producto', 'Servicio', 'Material', 'Otro']
        for forbidden_cat in forbidden_categories:
            assert forbidden_cat not in combo_items, \
                f"La catégorie par défaut '{forbidden_cat}' ne doit pas être présente"

        print(f"   📋 Catégories actuelles: {combo_items}")
        print("   ✅ Aucune catégorie par défaut trouvée")
    
    def test_table_headers_order_regression(self):
        """Test de régression: Vérifier l'ordre correct des colonnes dans la table."""
        # Arrange
        window = ProductosPyQt5Window()
        
        # Act
        headers = []
        for col in range(window.products_table.columnCount()):
            header = window.products_table.horizontalHeaderItem(col)
            if header:
                headers.append(header.text())
        
        # Assert
        expected_headers = ["ID", "Nombre", "Referencia", "Precio", "Stock", "Categoría"]
        assert headers == expected_headers, \
            f"L'ordre des headers doit être {expected_headers}, trouvé: {headers}"
    
    def test_all_columns_resize_modes_configured(self):
        """Test de régression: Vérifier que tous les modes de redimensionnement sont configurés."""
        # Arrange
        window = ProductosPyQt5Window()
        header = window.products_table.horizontalHeader()
        
        # Act & Assert
        expected_modes = {
            0: QHeaderView.ResizeToContents,  # ID
            1: QHeaderView.Stretch,           # Nombre
            2: QHeaderView.ResizeToContents,  # Referencia
            3: QHeaderView.ResizeToContents,  # Precio
            4: QHeaderView.ResizeToContents,  # Stock
            5: QHeaderView.ResizeToContents,  # Categoría
        }
        
        for col, expected_mode in expected_modes.items():
            actual_mode = header.sectionResizeMode(col)
            assert actual_mode == expected_mode, \
                f"La colonne {col} doit avoir le mode {expected_mode}, trouvé: {actual_mode}"


def run_tests_standalone():
    """Exécuter les tests sans pytest."""
    print("🧪 Tests de régression: Affichage des catégories dans l'interface produits")
    print("=" * 80)

    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Créer une instance de test
    test_instance = TestCategoriaDisplayRegression()
    test_instance.setup_method()

    # Liste des tests à exécuter
    tests = [
        ("Colonne Categoría existe", test_instance.test_categoria_column_exists_in_table_headers),
        ("Mode de redimensionnement", test_instance.test_categoria_column_resize_mode_configured),
        ("Champ categoria_combo", test_instance.test_categoria_combo_exists_in_form),
        ("Placeholder configuré", test_instance.test_categoria_combo_placeholder_configured),
        ("Affichage des données", test_instance.test_categoria_data_flow_in_table_update),
        ("Pas de catégories par défaut", test_instance.test_no_default_categories_regression),
        ("Ordre des headers", test_instance.test_table_headers_order_regression),
        ("Modes de toutes les colonnes", test_instance.test_all_columns_resize_modes_configured),
    ]

    # Exécuter les tests
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        try:
            test_func()
            print(f"   ✅ RÉUSSI")
            results.append(True)
        except Exception as e:
            print(f"   ❌ ÉCHOUÉ: {e}")
            results.append(False)

    # Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSULTATS DES TESTS DE RÉGRESSION:")

    success_count = sum(results)
    total_count = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if results[i] else "❌ ÉCHOUÉ"
        print(f"   {status}: {test_name}")

    print(f"\n📈 Score: {success_count}/{total_count} tests réussis")

    if success_count == total_count:
        print("🎉 TOUS LES TESTS DE RÉGRESSION SONT RÉUSSIS!")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ!")
        return 1


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        sys.exit(run_tests_standalone())
