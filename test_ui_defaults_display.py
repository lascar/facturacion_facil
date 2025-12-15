#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que les défauts s'affichent dans l'interface utilisateur
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from database.models import Organizacion
from config.config import Config


def test_ui_defaults_behavior():
    """Test du comportement de l'interface avec les défauts"""
    print("=== Test du comportement UI avec les défauts ===")
    
    try:
        # 1. Simuler le comportement actuel de load_organizacion()
        print("\n1. Simulation du comportement actuel...")
        
        # Simuler db.get_organization_info() qui retourne None
        organization_data = None  # Aucune organisation en base
        
        if organization_data:
            print("   → Données existantes trouvées, les charger")
        else:
            print("   → Aucune organisation en base, appel à clear_form()")
            print("   ❌ PROBLÈME: clear_form() vide les champs au lieu de les remplir")
        
        # 2. Tester le comportement souhaité
        print("\n2. Comportement souhaité...")
        
        # Utiliser Organizacion.get_with_defaults() pour obtenir les défauts
        org_with_defaults = Organizacion.get_with_defaults()
        
        # Convertir en format attendu par l'interface
        default_data = {
            'id': None,  # Pas d'ID car pas encore en base
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
        
        print("   → Données par défaut préparées pour l'interface:")
        for key, value in default_data.items():
            if key != 'id':  # Ignorer l'ID pour l'affichage
                print(f"     {key}: '{value}'")
        
        # 3. Vérifier que les valeurs ne sont pas vides
        print("\n3. Vérification des valeurs par défaut...")
        
        non_empty_fields = ['nombre', 'email', 'telefono', 'cif', 'directorio_imagenes_defecto', 
                           'directorio_descargas_pdf', 'directorio_logos_storage']
        
        all_good = True
        for field in non_empty_fields:
            value = default_data[field]
            if value and value.strip():
                print(f"   ✅ {field}: '{value}' (non vide)")
            else:
                print(f"   ❌ {field}: '{value}' (vide)")
                all_good = False
        
        # Vérifier que le logo est vide (comportement souhaité)
        if default_data['logo_path'] == '':
            print(f"   ✅ logo_path: '' (vide comme souhaité)")
        else:
            print(f"   ❌ logo_path: '{default_data['logo_path']}' (devrait être vide)")
            all_good = False
        
        # 4. Résumé du problème et de la solution
        print("\n4. Résumé...")
        
        if all_good:
            print("   ✅ Les valeurs par défaut sont correctes")
            print("   🔧 SOLUTION: Modifier load_organizacion() pour utiliser ces défauts")
        else:
            print("   ❌ Problème avec les valeurs par défaut")
            return False
        
        print("\n🎯 SOLUTION REQUISE:")
        print("   1. Modifier load_organizacion() dans organizacion_pyqt5.py")
        print("   2. Remplacer clear_form() par load_organization_data(default_data)")
        print("   3. Les champs afficheront les valeurs par défaut au lieu d'être vides")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur dans le test: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_before_after_ui():
    """Montrer la différence avant/après dans l'interface"""
    print("\n" + "="*60)
    print("COMPARAISON INTERFACE UTILISATEUR")
    print("="*60)
    
    print("\n🔴 AVANT (champs vides):")
    print("   Nom: [                    ]  ← Vide")
    print("   Email: [                    ]  ← Vide")
    print("   Téléphone: [                    ]  ← Vide")
    print("   CIF: [                    ]  ← Vide")
    print("   Images: [                    ]  ← Vide")
    print("   PDF: [                    ]  ← Vide")
    print("   Logos: [                    ]  ← Vide")
    print("   → Utilisateur doit tout saisir manuellement")
    
    print("\n🟢 APRÈS (champs pré-remplis):")
    org = Organizacion.get_with_defaults()
    print(f"   Nom: [{org.nombre:<20}]  ← Pré-rempli")
    print(f"   Email: [{org.email:<20}]  ← Pré-rempli")
    print(f"   Téléphone: [{org.telefono:<20}]  ← Pré-rempli")
    print(f"   CIF: [{org.cif:<20}]  ← Pré-rempli")
    print(f"   Images: [{org.directorio_imagenes_defecto:<20}]  ← Pré-rempli")
    print(f"   PDF: [{org.directorio_descargas_pdf:<20}]  ← Pré-rempli")
    print(f"   Logos: [{org.directorio_logos_storage:<20}]  ← Pré-rempli")
    print("   → Utilisateur peut modifier ou garder les valeurs")


if __name__ == "__main__":
    print("🧪 Test du comportement UI avec les défauts")
    print("Vérification que l'interface affiche les valeurs par défaut")
    
    success = test_ui_defaults_behavior()
    
    if success:
        show_before_after_ui()
        print("\n" + "="*70)
        print("✅ ANALYSE TERMINÉE")
        print("• Les valeurs par défaut sont prêtes")
        print("• Il faut modifier load_organizacion() pour les afficher")
        print("• L'interface sera beaucoup plus conviviale")
        print("="*70)
    else:
        print("\n❌ Des problèmes ont été détectés")
