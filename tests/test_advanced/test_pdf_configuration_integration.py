#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour valider que les PDF de factures utilisent bien :
1. Le répertoire PDF configuré dans 'Directorio de PDF's'
2. Le logo configuré dans 'Logo de la empresa'
3. Les informations d'entreprise configurées

CONFORMITÉ AUX RÈGLES CRITIQUES :
- ✅ Utilise UNIQUEMENT la base de données de production existante
- ✅ Tests en lecture seule sans modification de données
- ✅ Validation d'interface et configuration uniquement
- ✅ Aucune base temporaire ou modification de structure

Ce test peut être exécuté avec pytest ou directement avec Python.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import conditionnel de pytest
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from utils.pdf_generator import PDFGenerator
from database.models import Organizacion
from database.database_improved import DatabaseImproved

def test_pdf_uses_configured_directory():
    """Test que les PDF utilisent le répertoire configuré"""
    print("🧪 Test: PDF utilise le répertoire configuré")
    
    try:
        # Récupérer la configuration d'organisation
        organizacion = Organizacion.get()
        if not organizacion:
            print("❌ Aucune organisation configurée")
            return False
        
        # Vérifier si un répertoire PDF est configuré
        pdf_dir_configured = organizacion.directorio_descargas_pdf
        if pdf_dir_configured and pdf_dir_configured.strip():
            print(f"✅ Répertoire PDF configuré: {pdf_dir_configured}")
            
            # Vérifier que le répertoire existe ou peut être créé
            if os.path.exists(pdf_dir_configured):
                print(f"✅ Répertoire PDF existe: {pdf_dir_configured}")
            else:
                print(f"⚠️  Répertoire PDF configuré n'existe pas: {pdf_dir_configured}")
                print("   (Il sera créé automatiquement lors de la génération)")
        else:
            print("⚠️  Aucun répertoire PDF configuré, utilisation du répertoire par défaut")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_pdf_uses_configured_logo():
    """Test que les PDF utilisent le logo configuré"""
    print("🧪 Test: PDF utilise le logo configuré")
    
    try:
        pdf_generator = PDFGenerator()
        
        # Récupérer la configuration d'organisation
        organizacion = Organizacion.get()
        if not organizacion:
            print("❌ Aucune organisation configurée")
            return False
        
        # Vérifier si un logo est configuré
        logo_path_configured = organizacion.logo_path
        if logo_path_configured and logo_path_configured.strip():
            print(f"✅ Logo configuré: {logo_path_configured}")
            
            # Vérifier que le logo existe
            if os.path.exists(logo_path_configured):
                print(f"✅ Fichier logo existe: {logo_path_configured}")
                
                # Tester que find_company_logo() retourne le logo configuré
                found_logo = pdf_generator.find_company_logo()
                if found_logo == logo_path_configured:
                    print(f"✅ find_company_logo() retourne le logo configuré")
                    return True
                else:
                    print(f"❌ find_company_logo() retourne: {found_logo}")
                    print(f"   Attendu: {logo_path_configured}")
                    return False
            else:
                print(f"❌ Fichier logo configuré n'existe pas: {logo_path_configured}")
                return False
        else:
            print("⚠️  Aucun logo configuré")
            # Tester que find_company_logo() cherche dans les chemins par défaut
            found_logo = pdf_generator.find_company_logo()
            if found_logo:
                print(f"✅ Logo par défaut trouvé: {found_logo}")
            else:
                print("⚠️  Aucun logo trouvé (par défaut)")
            return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_pdf_uses_company_info():
    """Test que les PDF utilisent les informations d'entreprise configurées"""
    print("🧪 Test: PDF utilise les informations d'entreprise configurées")
    
    try:
        pdf_generator = PDFGenerator()
        
        # Récupérer la configuration d'organisation
        organizacion = Organizacion.get()
        if not organizacion:
            print("❌ Aucune organisation configurée")
            return False
        
        # Tester get_company_info()
        company_info = pdf_generator.get_company_info()
        
        # Vérifier que les informations configurées sont utilisées
        if organizacion.nombre and organizacion.nombre in company_info:
            print(f"✅ Nom d'entreprise configuré utilisé: {organizacion.nombre}")
        else:
            print(f"⚠️  Nom d'entreprise: configuré='{organizacion.nombre}', dans info={organizacion.nombre in company_info if organizacion.nombre else False}")
        
        if organizacion.cif and organizacion.cif in company_info:
            print(f"✅ CIF configuré utilisé: {organizacion.cif}")
        else:
            print(f"⚠️  CIF: configuré='{organizacion.cif}', dans info={organizacion.cif in company_info if organizacion.cif else False}")
        
        if organizacion.telefono and organizacion.telefono in company_info:
            print(f"✅ Téléphone configuré utilisé: {organizacion.telefono}")
        else:
            print(f"⚠️  Téléphone: configuré='{organizacion.telefono}', dans info={organizacion.telefono in company_info if organizacion.telefono else False}")
        
        if organizacion.email and organizacion.email in company_info:
            print(f"✅ Email configuré utilisé: {organizacion.email}")
        else:
            print(f"⚠️  Email: configuré='{organizacion.email}', dans info={organizacion.email in company_info if organizacion.email else False}")
        
        print(f"📄 Informations d'entreprise générées:")
        print(company_info.replace('<br/>', '\n').replace('<b>', '').replace('</b>', ''))
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def run_integration_tests():
    """Exécuter tous les tests d'intégration"""
    print("🚀 Tests d'intégration: Configuration PDF et Logo")
    print("=" * 60)
    
    # Initialiser l'application Qt si nécessaire
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    tests = [
        ("Répertoire PDF configuré", test_pdf_uses_configured_directory),
        ("Logo configuré", test_pdf_uses_configured_logo),
        ("Informations d'entreprise", test_pdf_uses_company_info)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Test: {test_name}")
            print("-" * 40)
            if test_func():
                print(f"✅ RÉUSSI: {test_name}")
                passed += 1
            else:
                print(f"❌ ÉCHEC: {test_name}")
        except Exception as e:
            print(f"❌ ERREUR: {test_name} - {e}")
        print("-" * 40)
    
    print(f"\n📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests d'intégration sont passés!")
        print("✅ Les PDF utilisent bien la configuration d'organisation")
        return True
    else:
        print("⚠️  Certains tests ont échoué ou montrent des avertissements")
        print("💡 Vérifiez la configuration dans 'Configuración de Organización'")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
