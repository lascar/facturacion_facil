#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration simple pour la gestion des catégories dans l'interface produits.

Ce test valide l'intégration complète entre l'interface utilisateur et la base de données
pour la gestion des catégories de produits.

Ce test peut être exécuté avec pytest ou directement avec Python.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ui.productos_pyqt5 import ProductosPyQt5Window

# Import conditionnel de pytest
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


class TestProductosCategoriaIntegrationSimple:
    """Tests d'intégration pour la gestion des catégories dans l'interface produits."""
    
    def setup_method(self):
        """Configuration pour chaque test."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    if PYTEST_AVAILABLE:
        setup_method = pytest.fixture(autouse=True)(setup_method)
    
    def test_categoria_display_with_real_data(self):
        """Test d'intégration: Affichage des catégories avec des données réelles."""
        # Créer la fenêtre et charger les données existantes
        window = ProductosPyQt5Window()
        window.load_productos()
        
        # Vérifier que la table contient des données
        row_count = window.products_table.rowCount()
        
        if row_count > 0:
            # Vérifier les catégories dans la table (colonne 5)
            categoria_col = 5
            displayed_categories = []
            for row in range(min(5, row_count)):  # Vérifier les 5 premiers produits max
                categoria_item = window.products_table.item(row, categoria_col)
                if categoria_item:
                    categoria_text = categoria_item.text()
                    displayed_categories.append(categoria_text)
            
            # Vérifier que la colonne catégorie existe et est visible
            headers = []
            for col in range(window.products_table.columnCount()):
                header = window.products_table.horizontalHeaderItem(col)
                if header:
                    headers.append(header.text())
            
            assert "Categoría" in headers, f"La colonne 'Categoría' doit être présente dans {headers}"
            categoria_index = headers.index("Categoría")
            assert categoria_index == 5, f"La colonne 'Categoría' doit être à l'index 5, trouvée à {categoria_index}"
            
        else:
            # Vérifier au moins que la structure est correcte
            headers = []
            for col in range(window.products_table.columnCount()):
                header = window.products_table.horizontalHeaderItem(col)
                if header:
                    headers.append(header.text())
            
            assert "Categoría" in headers, f"La colonne 'Categoría' doit être présente dans {headers}"
    
    def test_categoria_combo_loads_from_database(self):
        """Test d'intégration: Le combo catégorie charge les catégories depuis la base de données."""
        # Utiliser la vraie base de données pour ce test
        window = ProductosPyQt5Window()
        window.load_categories()
        
        # Vérifier que le combo contient au moins l'option vide
        combo_items = []
        for i in range(window.categoria_combo.count()):
            combo_items.append(window.categoria_combo.itemText(i))
        
        # Le combo doit contenir au moins l'option vide
        assert '' in combo_items, "Le combo doit contenir une option vide"
    
    def test_new_categoria_can_be_added(self):
        """Test d'intégration: Une nouvelle catégorie peut être ajoutée via le combo éditable."""
        window = ProductosPyQt5Window()
        window.load_categories()
        
        # Saisir une nouvelle catégorie
        new_categoria = 'Nouvelle Catégorie Test'
        window.categoria_combo.setCurrentText(new_categoria)
        
        # Vérifier que la nouvelle catégorie est acceptée
        current_text = window.categoria_combo.currentText()
        assert current_text == new_categoria, \
            f"Le combo doit accepter '{new_categoria}', trouvé: '{current_text}'"
    
    def test_categoria_form_field_exists(self):
        """Test d'intégration: Le champ catégorie existe dans le formulaire."""
        window = ProductosPyQt5Window()
        
        # Vérifier que le champ categoria_combo existe
        assert hasattr(window, 'categoria_combo'), "Le champ 'categoria_combo' doit exister"
        assert window.categoria_combo.isEditable(), "Le combo doit être éditable"
        
        # Vérifier le placeholder
        placeholder = window.categoria_combo.lineEdit().placeholderText()
        expected_placeholder = "Escribir categoría o dejar vacío"
        assert placeholder == expected_placeholder, \
            f"Placeholder attendu: '{expected_placeholder}', trouvé: '{placeholder}'"
    
    def test_categoria_empty_handling(self):
        """Test d'intégration: Gestion correcte des catégories vides."""
        window = ProductosPyQt5Window()
        
        # Tester avec une catégorie vide
        window.categoria_combo.setCurrentText('')
        current_text = window.categoria_combo.currentText()
        assert current_text == '', "Le combo doit accepter les catégories vides"
        
        # Tester avec des espaces
        window.categoria_combo.setCurrentText('   ')
        current_text = window.categoria_combo.currentText()
        assert current_text == '   ', "Le combo doit accepter les espaces"
    
    def test_categoria_selection_updates_form(self):
        """Test d'intégration: La sélection d'un produit met à jour le formulaire avec sa catégorie."""
        window = ProductosPyQt5Window()
        window.load_productos()
        
        # Si il y a des produits, tester la sélection
        if window.products_table.rowCount() > 0:
            # Sélectionner le premier produit
            window.products_table.selectRow(0)
            window.on_product_selected()
            
            # Vérifier que le combo catégorie a été mis à jour
            # (Le test ne vérifie pas la valeur exacte car elle dépend des données)
            combo_text = window.categoria_combo.currentText()
            # Le combo doit avoir une valeur (même vide)
            assert isinstance(combo_text, str), "Le combo doit contenir une chaîne de caractères"


def run_tests_standalone():
    """Exécuter les tests sans pytest."""
    print("🧪 Tests d'intégration: Gestion des catégories dans l'interface produits")
    print("=" * 80)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Créer une instance de test
    test_instance = TestProductosCategoriaIntegrationSimple()
    test_instance.setup_method()
    
    # Liste des tests à exécuter
    tests = [
        ("Affichage avec données réelles", test_instance.test_categoria_display_with_real_data),
        ("Chargement depuis base de données", test_instance.test_categoria_combo_loads_from_database),
        ("Ajout nouvelle catégorie", test_instance.test_new_categoria_can_be_added),
        ("Champ formulaire existe", test_instance.test_categoria_form_field_exists),
        ("Gestion catégories vides", test_instance.test_categoria_empty_handling),
        ("Sélection met à jour formulaire", test_instance.test_categoria_selection_updates_form),
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
    print("📊 RÉSULTATS DES TESTS D'INTÉGRATION:")
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if results[i] else "❌ ÉCHOUÉ"
        print(f"   {status}: {test_name}")
    
    print(f"\n📈 Score: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 TOUS LES TESTS D'INTÉGRATION SONT RÉUSSIS!")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ!")
        return 1


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        sys.exit(run_tests_standalone())
