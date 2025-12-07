#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour la correction des fausses alertes de modifications
dans la fenêtre de configuration d'organisation.

Ce test valide que data_modified reste False après le chargement des données,
évitant ainsi les fausses alertes "Des modifications non sauvegardées seront perdues".

CONFORMITÉ AUX RÈGLES CRITIQUES :
- ✅ Utilise UNIQUEMENT la base de données de production existante
- ✅ Tests en lecture seule sans modification de données
- ✅ Validation d'interface utilisateur uniquement
- ✅ Aucune base temporaire ou modification de structure

Ce test peut être exécuté avec pytest ou directement avec Python.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ui.organizacion_pyqt5 import OrganizacionPyQt5Window

# Import conditionnel de pytest
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


class TestOrganizacionFalseModifiedRegression:
    """Tests de régression pour les fausses alertes de modification."""
    
    def setup_method(self):
        """Configuration pour chaque test."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    if PYTEST_AVAILABLE:
        setup_method = pytest.fixture(autouse=True)(setup_method)
    
    def test_load_organizacion_no_false_modified(self):
        """Test de régression: load_organizacion ne doit pas marquer comme modifié."""
        # Créer la fenêtre d'organisation
        window = OrganizacionPyQt5Window()
        
        # Charger les données (cela ne devrait pas marquer comme modifié)
        window.load_organizacion()
        
        # Vérifier que data_modified est False après le chargement
        assert not window.data_modified, (
            f"RÉGRESSION: data_modified devrait être False après chargement, "
            f"mais il est {window.data_modified}. "
            f"Cela causerait une fausse alerte de fermeture."
        )
        
        window.close()
    
    def test_load_organization_data_no_false_modified(self):
        """Test de régression: load_organization_data ne doit pas marquer comme modifié."""
        window = OrganizacionPyQt5Window()
        
        # Simuler des données d'organisation
        test_data = {
            'nombre': 'Test Company',
            'cif': '12345678A',
            'telefono': '123456789',
            'email': 'test@example.com',
            'direccion': 'Test Address',
            'logo_path': '',
            'numero_factura_inicial': '1',
            'directorio_imagenes_defecto': '',
            'directorio_logos_storage': '',
            'directorio_descargas_pdf': ''
        }
        
        # Charger les données directement
        window.load_organization_data(test_data)
        
        # Vérifier que data_modified est False
        assert not window.data_modified, (
            f"RÉGRESSION: load_organization_data ne devrait pas marquer comme modifié, "
            f"mais data_modified est {window.data_modified}"
        )
        
        window.close()
    
    def test_clear_form_no_false_modified(self):
        """Test de régression: clear_form ne doit pas marquer comme modifié."""
        window = OrganizacionPyQt5Window()
        
        # Charger des données d'abord
        window.load_organizacion()
        assert not window.data_modified, "Données initiales devraient être non modifiées"
        
        # Appeler clear_form (cela ne devrait pas marquer comme modifié)
        window.clear_form()
        
        # Vérifier que data_modified reste False
        assert not window.data_modified, (
            f"RÉGRESSION: clear_form ne devrait pas marquer comme modifié, "
            f"mais data_modified est {window.data_modified}"
        )
        
        window.close()
    
    def test_real_modification_still_detected(self):
        """Test de régression: les vraies modifications doivent toujours être détectées."""
        window = OrganizacionPyQt5Window()
        
        # Charger les données (non modifié)
        window.load_organizacion()
        assert not window.data_modified, "État initial devrait être non modifié"
        
        # Faire une vraie modification
        original_text = window.nombre_edit.text()
        window.nombre_edit.setText("Modification Test")
        
        # Vérifier que la modification est détectée
        assert window.data_modified, (
            "RÉGRESSION: Les vraies modifications ne sont plus détectées. "
            "Le système de détection de modifications est cassé."
        )
        
        # Restaurer l'état original
        window.nombre_edit.setText(original_text)
        
        window.close()
    
    def test_reload_resets_modified_state(self):
        """Test de régression: le rechargement doit remettre data_modified à False."""
        window = OrganizacionPyQt5Window()
        
        # Charger et modifier
        window.load_organizacion()
        window.nombre_edit.setText("Test Modification")
        assert window.data_modified, "Modification devrait être détectée"
        
        # Recharger
        window.load_organizacion()
        
        # Vérifier que data_modified est remis à False
        assert not window.data_modified, (
            f"RÉGRESSION: Le rechargement ne remet pas data_modified à False, "
            f"il reste {window.data_modified}"
        )
        
        window.close()


def run_standalone_tests():
    """Exécuter les tests en mode standalone (sans pytest)."""
    print("🚀 Tests de régression: Fausses alertes de modification")
    print("=" * 65)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    test_instance = TestOrganizacionFalseModifiedRegression()
    test_instance.setup_method()
    
    tests = [
        ("load_organizacion ne marque pas comme modifié", test_instance.test_load_organizacion_no_false_modified),
        ("load_organization_data ne marque pas comme modifié", test_instance.test_load_organization_data_no_false_modified),
        ("clear_form ne marque pas comme modifié", test_instance.test_clear_form_no_false_modified),
        ("vraies modifications toujours détectées", test_instance.test_real_modification_still_detected),
        ("rechargement remet à False", test_instance.test_reload_resets_modified_state)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"🧪 Test: {test_name}")
            test_func()
            print(f"✅ RÉUSSI")
            passed += 1
        except Exception as e:
            print(f"❌ ÉCHEC: {e}")
        print("-" * 65)
    
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests de régression sont passés!")
        print("✅ La correction des fausses alertes fonctionne correctement")
        return True
    else:
        print("❌ Certains tests de régression ont échoué")
        print("⚠️  Risque de régression sur les fausses alertes de modification")
        return False


if __name__ == "__main__":
    success = run_standalone_tests()
    sys.exit(0 if success else 1)
