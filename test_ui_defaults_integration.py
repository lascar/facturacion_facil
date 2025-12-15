#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour vérifier que l'interface affiche les valeurs par défaut
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from database.models import Organizacion
from test.utils.test_database_manager import isolated_test_db
from config.config import Config


def test_ui_defaults_integration():
    """Test d'intégration pour l'affichage des défauts dans l'interface"""
    print("=== Test d'intégration UI avec défauts ===")
    
    try:
        # 1. Utiliser la base de test (sécurité)
        print("\n1. Configuration de la base de test...")
        with isolated_test_db("ui_defaults_test") as test_db:
            print("   ✅ Base de test configurée")

            # 2. Vérifier qu'aucune organisation n'existe
            print("\n2. Vérification de l'état initial...")
            existing_org = test_db.get_organization_info()
            if existing_org:
                print(f"   ⚠️  Organisation existante trouvée: {existing_org}")
                print("   → Test avec données existantes")
            else:
                print("   ✅ Aucune organisation en base (état initial correct)")

            # 3. Simuler le comportement de load_organizacion()
            print("\n3. Simulation du comportement de load_organizacion()...")

            organization_data = test_db.get_organization_info()

            if organization_data:
                print("   → Données existantes trouvées, les charger")
                result_data = organization_data
                source = "base de données"
            else:
                print("   → Aucune organisation, charger les défauts")

                # Simuler load_default_organization_data()
                org_with_defaults = Organizacion.get_with_defaults()

                result_data = {
                    'id': None,
                    'nombre': org_with_defaults.nombre,
                    'direccion': org_with_defaults.direccion,
                    'telefono': org_with_defaults.telefono,
                    'email': org_with_defaults.email,
                    'cif': org_with_defaults.cif,
                    'logo_path': org_with_defaults.logo_path,
                    'numero_factura_inicial': org_with_defaults.numero_factura_inicial,
                    'directorio_imagenes_defecto': org_with_defaults.directorio_imagenes_defecto,
                    'directorio_descargas_pdf': org_with_defaults.directorio_descargas_pdf,
                    'directorio_logos_storage': org_with_defaults.directorio_logos_storage,
                    'logo_orientation': org_with_defaults.logo_orientation,
                    'visor_pdf_personalizado': org_with_defaults.visor_pdf_personalizado
                }
                source = "valeurs par défaut"

            # 4. Vérifier les données qui seraient affichées
            print(f"\n4. Données qui seraient affichées (source: {source})...")

            expected_fields = {
                'nombre': 'Mi Empresa',
                'email': 'contacto@miempresa.com',
                'telefono': '+34 123 456 789',
                'cif': 'B12345678',
                'directorio_imagenes_defecto': 'images',
                'directorio_descargas_pdf': 'facturas',
                'directorio_logos_storage': 'logos'
            }

            all_correct = True
            for field, expected_value in expected_fields.items():
                actual_value = result_data.get(field, '')
                if actual_value == expected_value:
                    print(f"   ✅ {field}: '{actual_value}' (correct)")
                else:
                    print(f"   ❌ {field}: '{actual_value}' (attendu: '{expected_value}')")
                    all_correct = False

            # Vérifier que le logo est vide
            logo_path = result_data.get('logo_path', '')
            if logo_path == '':
                print(f"   ✅ logo_path: '' (vide comme souhaité)")
            else:
                print(f"   ⚠️  logo_path: '{logo_path}' (non vide)")

            # 5. Simuler l'affichage dans l'interface
            print("\n5. Simulation de l'affichage dans l'interface...")
            print("   Champs qui seraient remplis:")
            print(f"     Nom: [{result_data.get('nombre', ''):<25}]")
            print(f"     Email: [{result_data.get('email', ''):<25}]")
            print(f"     Téléphone: [{result_data.get('telefono', ''):<25}]")
            print(f"     CIF: [{result_data.get('cif', ''):<25}]")
            print(f"     Images: [{result_data.get('directorio_imagenes_defecto', ''):<25}]")
            print(f"     PDF: [{result_data.get('directorio_descargas_pdf', ''):<25}]")
            print(f"     Logos: [{result_data.get('directorio_logos_storage', ''):<25}]")
            print(f"     Logo: [{result_data.get('logo_path', ''):<25}]")

            # 6. Résultat
            print("\n6. Résultat du test...")

            if all_correct:
                print("   ✅ SUCCÈS: L'interface affichera les bonnes valeurs par défaut")
                print("   🎯 Les utilisateurs verront des champs pré-remplis")
                print("   💡 Expérience utilisateur grandement améliorée")
                return True
            else:
                print("   ❌ ÉCHEC: Problème avec les valeurs par défaut")
                return False
        
    except Exception as e:
        print(f"\n❌ Erreur dans le test d'intégration: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_source():
    """Vérifier que les défauts viennent bien de config.json"""
    print("\n" + "="*50)
    print("VÉRIFICATION SOURCE CONFIG.JSON")
    print("="*50)
    
    try:
        # Vérifier que config.json existe et contient les défauts
        config_file = "config/config.json"
        if os.path.exists(config_file):
            print(f"✅ {config_file} existe")
            
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "organizacion_defaults" in config_data:
                print("✅ organizacion_defaults trouvé dans config.json")
                defaults = config_data["organizacion_defaults"]
                
                # Vérifier quelques valeurs clés
                key_values = ['nombre', 'email', 'directorio_descargas_pdf']
                for key in key_values:
                    if key in defaults:
                        print(f"   ✅ {key}: '{defaults[key]}'")
                    else:
                        print(f"   ❌ {key}: manquant")
                
                return True
            else:
                print("❌ organizacion_defaults manquant dans config.json")
                return False
        else:
            print(f"❌ {config_file} n'existe pas")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification config: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Test d'intégration UI avec défauts")
    print("Vérification que l'interface affiche les valeurs par défaut")
    
    # Test principal
    success = test_ui_defaults_integration()
    
    # Test de la source de configuration
    config_ok = test_config_source()
    
    print("\n" + "="*70)
    if success and config_ok:
        print("✅ TOUS LES TESTS RÉUSSIS")
        print("• L'interface affichera les valeurs par défaut")
        print("• Les défauts viennent de config.json")
        print("• L'expérience utilisateur est améliorée")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        if not success:
            print("• Problème avec l'affichage des défauts")
        if not config_ok:
            print("• Problème avec la source de configuration")
    print("="*70)
