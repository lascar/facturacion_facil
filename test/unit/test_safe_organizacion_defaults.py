#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour les valeurs par défaut de l'organisation
Suit les préférences de sécurité : utilise exclusivement get_test_database()
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.test_database import get_test_database
from database.models import Organizacion
from config.config import Config


class TestOrganizacionDefaults:
    """Tests pour les valeurs par défaut de l'organisation"""
    
    def setup_test_database(self):
        """Configuration automatique de la base de test pour chaque test"""
        # SÉCURITÉ : Utiliser exclusivement get_test_database()
        self.test_db = get_test_database()

        # Vérifier que nous utilisons bien une base de test
        assert "test" in self.test_db.db_path or "temp" in self.test_db.db_path, \
            "ERREUR CRITIQUE : Base de production utilisée dans les tests !"

        return self.test_db

    def teardown_test_database(self):
        """Nettoyage automatique après chaque test"""
        if hasattr(self, 'test_db'):
            # La base de test se nettoie automatiquement
            pass
    
    def test_organizacion_get_with_empty_database_returns_defaults(self):
        """Test que Organizacion.get_with_defaults() retourne des valeurs par défaut"""
        # ARRANGE : Tester directement la méthode get_with_defaults
        # (qui ne dépend pas de la base de données)

        # ACT : Récupérer l'organisation avec défauts
        org = Organizacion.get_with_defaults()
        print(f"DEBUG: Organisation avec défauts - nom: '{org.nombre}', email: '{org.email}'")

        # ASSERT : Vérifier que les valeurs par défaut sont présentes
        assert org.nombre == "Mi Empresa", f"Attendu 'Mi Empresa', obtenu '{org.nombre}'"
        assert org.direccion == "Calle Principal, 123\n12345 Ciudad", f"Adresse par défaut incorrecte: '{org.direccion}'"
        assert org.telefono == "+34 123 456 789", f"Téléphone par défaut incorrect: '{org.telefono}'"
        assert org.email == "contacto@miempresa.com", f"Email par défaut incorrect: '{org.email}'"
        assert org.cif == "B12345678", f"CIF par défaut incorrect: '{org.cif}'"
        assert org.numero_factura_inicial == "1", f"Numéro initial incorrect: '{org.numero_factura_inicial}'"

        # Vérifier les répertoires par défaut
        assert org.directorio_imagenes_defecto != "", "Le répertoire d'images par défaut ne doit pas être vide"
        assert org.directorio_descargas_pdf != "", "Le répertoire PDF par défaut ne doit pas être vide"

        # Vérifier le logo par défaut (doit être vide)
        assert org.logo_path == "", f"Le logo par défaut doit être vide, trouvé: '{org.logo_path}'"
    
    def test_organizacion_get_with_existing_data_preserves_values(self):
        """Test que les données existantes ne sont pas écrasées par les défauts"""
        # ARRANGE : Nettoyer d'abord, puis créer une organisation avec des données spécifiques
        self.test_db.execute_query("DELETE FROM organizacion")
        org_existante = Organizacion(
            nombre="Empresa Existente",
            direccion="Dirección Existente",
            telefono="987654321",
            email="existente@empresa.com",
            cif="A87654321"
        )
        org_existante.save()
        
        # ACT : Récupérer l'organisation
        org_recuperee = Organizacion.get()
        
        # ASSERT : Vérifier que les données existantes sont préservées
        assert org_recuperee.nombre == "Empresa Existente"
        assert org_recuperee.direccion == "Dirección Existente"
        assert org_recuperee.telefono == "987654321"
        assert org_recuperee.email == "existente@empresa.com"
        assert org_recuperee.cif == "A87654321"
    
    def test_config_has_organizacion_defaults(self):
        """Test que la configuration contient les valeurs par défaut pour l'organisation"""
        # ACT : Charger la configuration
        config = Config()

        # ASSERT : Vérifier que les défauts existent
        defaults = config.get("organizacion_defaults")
        assert defaults is not None, "La configuration doit contenir 'organizacion_defaults'"

        # Vérifier les champs obligatoires de base
        required_fields = ["nombre", "direccion", "telefono", "email", "cif", "numero_factura_inicial"]
        for field in required_fields:
            assert field in defaults, f"Le champ '{field}' doit être dans organizacion_defaults"
            assert defaults[field] != "", f"Le champ '{field}' ne doit pas être vide"

        # Vérifier les champs de répertoires et logo
        directory_fields = ["directorio_imagenes_defecto", "directorio_descargas_pdf", "directorio_logos_storage"]
        for field in directory_fields:
            assert field in defaults, f"Le champ '{field}' doit être dans organizacion_defaults"
            assert defaults[field] != "", f"Le champ '{field}' ne doit pas être vide"

        # Vérifier les structures de répertoires spécifiques (dans le répertoire de l'application)
        assert "images" in defaults["directorio_imagenes_defecto"], f"Le répertoire d'images doit contenir 'images': '{defaults['directorio_imagenes_defecto']}'"
        assert "logos" in defaults["directorio_logos_storage"], f"Le répertoire de logos doit contenir 'logos': '{defaults['directorio_logos_storage']}'"
        assert "facturas" in defaults["directorio_descargas_pdf"], f"Le répertoire PDF doit contenir 'facturas': '{defaults['directorio_descargas_pdf']}'"

        # Vérifier que les chemins sont relatifs à l'application (pas dans home)
        assert not defaults["directorio_imagenes_defecto"].startswith(str(Path.home())), f"Le répertoire d'images ne doit pas être dans home: '{defaults['directorio_imagenes_defecto']}'"
        assert not defaults["directorio_logos_storage"].startswith(str(Path.home())), f"Le répertoire de logos ne doit pas être dans home: '{defaults['directorio_logos_storage']}'"
        assert not defaults["directorio_descargas_pdf"].startswith(str(Path.home())), f"Le répertoire PDF ne doit pas être dans home: '{defaults['directorio_descargas_pdf']}'"

        # Vérifier le logo par défaut (doit être vide)
        assert "logo_path" in defaults, "Le champ 'logo_path' doit être dans organizacion_defaults"
        assert defaults["logo_path"] == "", f"Le logo par défaut doit être vide, trouvé: '{defaults['logo_path']}'"

        # Vérifier que les valeurs viennent du fichier JSON (pas du code Python)
        import json
        import os
        if os.path.exists("config/config.json"):
            with open("config/config.json", 'r', encoding='utf-8') as f:
                json_config = json.load(f)
                if "organizacion_defaults" in json_config:
                    print("   ✅ Les défauts sont dans config.json (correct)")
                    # Vérifier que les valeurs JSON correspondent aux valeurs chargées
                    json_defaults = json_config["organizacion_defaults"]
                    assert json_defaults["nombre"] == defaults["nombre"], "Les valeurs JSON doivent correspondre aux valeurs chargées"
                else:
                    print("   ⚠️  Les défauts ne sont pas encore dans config.json")
                    assert False, "Les défauts doivent être dans config.json, pas dans le code Python"
    
    def test_default_directories_are_valid_paths(self):
        """Test que les répertoires par défaut sont des chemins valides"""
        # ACT : Récupérer l'organisation avec défauts
        org = Organizacion.get()
        
        # ASSERT : Vérifier que les répertoires sont des chemins valides
        if org.directorio_imagenes_defecto:
            # Le chemin doit être un chemin valide (peut ne pas exister encore)
            assert os.path.isabs(org.directorio_imagenes_defecto) or \
                   Path(org.directorio_imagenes_defecto).is_absolute(), \
                   "Le répertoire d'images doit être un chemin absolu"
        
        if org.directorio_descargas_pdf:
            assert os.path.isabs(org.directorio_descargas_pdf) or \
                   Path(org.directorio_descargas_pdf).is_absolute(), \
                   "Le répertoire PDF doit être un chemin absolu"


def run_tests():
    """Exécuter tous les tests manuellement"""
    test_instance = TestOrganizacionDefaults()

    print("=== Tests des valeurs par défaut de l'organisation ===")

    try:
        # Setup
        test_instance.setup_test_database()

        # Test 3 - Configuration (indépendant de la base)
        print("\n1. Test de la configuration des défauts...")
        try:
            test_instance.test_config_has_organizacion_defaults()
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL: {e}")

        # Test 4 - Répertoires (indépendant de la base)
        print("\n2. Test de validité des répertoires par défaut...")
        try:
            test_instance.test_default_directories_are_valid_paths()
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL: {e}")

        # Test 1 - Base vide (doit être avant test 2)
        print("\n3. Test des valeurs par défaut avec base vide...")
        try:
            test_instance.test_organizacion_get_with_empty_database_returns_defaults()
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL: {e}")

        # Test 2 - Données existantes (après test 1)
        print("\n4. Test de préservation des données existantes...")
        try:
            test_instance.test_organizacion_get_with_existing_data_preserves_values()
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL: {e}")

    finally:
        # Cleanup
        test_instance.teardown_test_database()

    print("\n=== Fin des tests ===")


if __name__ == "__main__":
    run_tests()
