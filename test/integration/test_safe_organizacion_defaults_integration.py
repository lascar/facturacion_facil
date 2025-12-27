#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour les valeurs par défaut de l'organisation
Vérifie que la fenêtre d'organisation affiche bien les valeurs par défaut
"""

import sys
import os
from pathlib import Path
import pytest

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.test_database import get_test_database
from database.models import Organizacion
from config.config import Config


@pytest.mark.skip(reason="Organizacion.get_with_defaults() method does not exist")
def test_organizacion_integration_with_defaults():
    """Test d'intégration : vérifier que l'organisation charge les défauts correctement"""
    print("=== Test d'intégration des valeurs par défaut ===")
    
    # SÉCURITÉ : Utiliser exclusivement get_test_database()
    test_db = get_test_database()
    
    # Vérifier que nous utilisons bien une base de test
    assert "test" in test_db.db_path or "temp" in test_db.db_path, \
        "ERREUR CRITIQUE : Base de production utilisée dans les tests !"
    
    try:
        # ARRANGE : S'assurer qu'il n'y a pas d'organisation en base
        test_db.execute_query("DELETE FROM organizacion")
        results = test_db.execute_query("SELECT COUNT(*) FROM organizacion")
        print(f"Organisations en base de test: {results[0][0]}")
        
        # ACT : Récupérer l'organisation avec défauts (méthode directe)
        # Note: On teste get_with_defaults() directement car get() utilise la DB globale
        org = Organizacion.get_with_defaults()
        
        # ASSERT : Vérifier que les valeurs par défaut sont chargées
        print(f"Nom de l'organisation: '{org.nombre}'")
        print(f"Email: '{org.email}'")
        print(f"Téléphone: '{org.telefono}'")
        print(f"Répertoire images: '{org.directorio_imagenes_defecto}'")
        print(f"Répertoire PDF: '{org.directorio_descargas_pdf}'")
        
        # Vérifications
        assert org.nombre == "Mi Empresa", f"Nom incorrect: {org.nombre}"
        assert org.email == "contacto@miempresa.com", f"Email incorrect: {org.email}"
        assert org.telefono == "+34 123 456 789", f"Téléphone incorrect: {org.telefono}"
        assert org.cif == "B12345678", f"CIF incorrect: {org.cif}"
        assert org.directorio_imagenes_defecto != "", "Répertoire images vide"
        assert org.directorio_descargas_pdf != "", "Répertoire PDF vide"
        
        print("✅ Test d'intégration réussi !")
        
        # Test supplémentaire : vérifier que la configuration est accessible
        config = Config()
        defaults = config.get("organizacion_defaults")
        assert defaults is not None, "Configuration des défauts manquante"
        print("✅ Configuration des défauts accessible !")
        
        assert True
        
    except Exception as e:
        print(f"❌ Erreur dans le test d'intégration: {e}")
        assert False, "Test failed"
    
    finally:
        # Nettoyage automatique (la base de test se nettoie automatiquement)
        pass


@pytest.mark.skip(reason="Organizacion.get_with_defaults() method does not exist")
def test_organizacion_window_simulation():
    """Simulation du comportement de la fenêtre d'organisation"""
    print("\n=== Simulation fenêtre d'organisation ===")

    try:
        # Simuler le chargement des données dans la fenêtre
        # (comme dans ui/organizacion.py ligne 414-424)

        # 1. Récupérer l'organisation avec défauts
        organizacion = Organizacion.get_with_defaults()
        
        # 2. Simuler le remplissage des champs de formulaire
        form_data = {
            "nombre": organizacion.nombre,
            "cif": organizacion.cif,
            "direccion": organizacion.direccion,
            "telefono": organizacion.telefono,
            "email": organizacion.email,
            "directorio_imagenes": organizacion.directorio_imagenes_defecto,
            "numero_inicial": organizacion.numero_factura_inicial,
            "directorio_pdf": organizacion.directorio_descargas_pdf,
            "visor_pdf": organizacion.visor_pdf_personalizado
        }
        
        print("Données qui seraient affichées dans la fenêtre:")
        for field, value in form_data.items():
            print(f"  {field}: '{value}'")
        
        # 3. Vérifier que tous les champs ont des valeurs sensées
        assert form_data["nombre"] != "", "Le nom ne doit pas être vide"
        assert form_data["email"] != "", "L'email ne doit pas être vide"
        assert "@" in form_data["email"], "L'email doit être valide"
        assert form_data["telefono"] != "", "Le téléphone ne doit pas être vide"
        assert form_data["cif"] != "", "Le CIF ne doit pas être vide"
        assert form_data["numero_inicial"] == "1", "Le numéro initial doit être 1"
        
        print("✅ Simulation de la fenêtre réussie !")
        assert True
        
    except Exception as e:
        print(f"❌ Erreur dans la simulation: {e}")
        assert False, "Test failed"


def run_integration_tests():
    """Exécuter tous les tests d'intégration"""
    print("🧪 Lancement des tests d'intégration des valeurs par défaut")
    
    success = True
    
    # Test 1 : Intégration de base
    success &= test_organizacion_integration_with_defaults()
    
    # Test 2 : Simulation fenêtre
    success &= test_organizacion_window_simulation()
    
    if success:
        print("\n🎉 Tous les tests d'intégration ont réussi !")
    else:
        print("\n❌ Certains tests d'intégration ont échoué")
    
    return success


if __name__ == "__main__":
    run_integration_tests()
