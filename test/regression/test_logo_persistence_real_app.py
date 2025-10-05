#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de persistance du logo dans l'application réelle
"""

import os
import sys
import tempfile
import pytest
from PIL import Image

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Organizacion
from utils.logo_manager import LogoManager


class TestLogoPersistenceRealApp:
    """Tests de persistance du logo dans l'application réelle"""
    
    def test_current_logo_status(self):
        """Vérifier l'état actuel du logo dans l'application"""
        print(f"\n🔍 Vérification de l'état actuel du logo")
        print(f"=" * 50)
        
        # Vérifier l'organisation actuelle
        org = Organizacion.get()
        
        if org and org.nombre:
            print(f"   🏢 Organisation trouvée: '{org.nombre}'")
            print(f"   🖼️  Logo path: '{org.logo_path}'")
            
            if org.logo_path:
                file_exists = os.path.exists(org.logo_path)
                print(f"   📁 Fichier logo existe: {file_exists}")
                
                if file_exists:
                    file_size = os.path.getsize(org.logo_path)
                    print(f"   📊 Taille fichier: {file_size} bytes")
                    
                    # Vérifier si c'est dans le répertoire permanent
                    logo_manager = LogoManager()
                    is_permanent = logo_manager.logo_directory in org.logo_path
                    print(f"   🏠 Dans répertoire permanent: {is_permanent}")
                    print(f"   📁 Répertoire permanent: {logo_manager.logo_directory}")
                    
                    if not is_permanent:
                        print(f"   ⚠️  PROBLÈME: Logo pas dans répertoire permanent!")
                        print(f"      Le logo pourrait être perdu au redémarrage")
                        
                        # Proposer une solution
                        print(f"\n   🔧 Solution suggérée:")
                        print(f"      1. Copier le logo vers le répertoire permanent")
                        print(f"      2. Mettre à jour le chemin en base de données")
                        
                        return False
                    else:
                        print(f"   ✅ Logo correctement stocké dans répertoire permanent")
                        return True
                else:
                    print(f"   ❌ PROBLÈME: Fichier logo n'existe pas!")
                    print(f"      Chemin: {org.logo_path}")
                    return False
            else:
                print(f"   ℹ️  Aucun logo configuré")
                return True
        else:
            print(f"   ℹ️  Aucune organisation configurée")
            return True
    
    def test_logo_directory_status(self):
        """Vérifier l'état du répertoire des logos"""
        print(f"\n🔍 Vérification du répertoire des logos")
        print(f"=" * 40)
        
        logo_manager = LogoManager()
        logo_dir = logo_manager.logo_directory
        
        print(f"   📁 Répertoire: {logo_dir}")
        print(f"   ✅ Existe: {os.path.exists(logo_dir)}")
        
        if os.path.exists(logo_dir):
            print(f"   ✅ Accessible en lecture: {os.access(logo_dir, os.R_OK)}")
            print(f"   ✅ Accessible en écriture: {os.access(logo_dir, os.W_OK)}")
            
            # Lister les logos existants
            logos = logo_manager.list_logos()
            print(f"   📊 Nombre de logos: {len(logos)}")
            
            for i, logo_path in enumerate(logos, 1):
                file_size = os.path.getsize(logo_path)
                print(f"      {i}. {os.path.basename(logo_path)} ({file_size} bytes)")
            
            return True
        else:
            print(f"   ❌ Répertoire n'existe pas!")
            return False
    
    def test_fix_logo_persistence_if_needed(self):
        """Corriger la persistance du logo si nécessaire"""
        print(f"\n🔧 Correction de la persistance du logo si nécessaire")
        print(f"=" * 55)
        
        org = Organizacion.get()
        
        if not org or not org.nombre:
            print(f"   ℹ️  Aucune organisation à corriger")
            return True
        
        if not org.logo_path:
            print(f"   ℹ️  Aucun logo à corriger")
            return True
        
        logo_manager = LogoManager()
        
        # Vérifier si le logo est dans le répertoire permanent
        is_permanent = logo_manager.logo_directory in org.logo_path
        file_exists = os.path.exists(org.logo_path)
        
        print(f"   🖼️  Logo actuel: {org.logo_path}")
        print(f"   📁 Fichier existe: {file_exists}")
        print(f"   🏠 Dans répertoire permanent: {is_permanent}")
        
        if file_exists and is_permanent:
            print(f"   ✅ Logo déjà correctement configuré")
            return True
        
        if file_exists and not is_permanent:
            print(f"   🔧 Correction nécessaire: copier vers répertoire permanent")
            
            # Copier le logo vers le répertoire permanent
            permanent_logo = logo_manager.save_logo(org.logo_path, org.nombre)
            
            if permanent_logo:
                print(f"   ✅ Logo copié: {permanent_logo}")
                
                # Mettre à jour l'organisation
                org.logo_path = permanent_logo
                org.save()
                
                print(f"   ✅ Organisation mise à jour")
                print(f"   🎉 Correction terminée avec succès!")
                return True
            else:
                print(f"   ❌ Échec de la copie du logo")
                return False
        
        if not file_exists:
            print(f"   ❌ Fichier logo n'existe pas, impossible de corriger")
            print(f"   💡 Solution: sélectionner un nouveau logo dans l'interface")
            return False
    
    def test_create_logo_for_testing(self):
        """Créer un logo de démonstration pour tester la persistance"""
        print(f"\n🎨 Création d'un logo de démonstration")
        print(f"=" * 40)
        
        # Créer un logo temporaire
        temp_dir = tempfile.mkdtemp()
        temp_logo = os.path.join(temp_dir, "demo_logo.png")
        
        # Créer une image de démonstration
        img = Image.new('RGB', (200, 100), color='purple')
        img.save(temp_logo)
        
        print(f"   🎨 Logo temporaire créé: {temp_logo}")
        
        try:
            # Utiliser le LogoManager pour le rendre permanent
            logo_manager = LogoManager()
            permanent_logo = logo_manager.save_logo(temp_logo, "Demo Company")
            
            if permanent_logo:
                print(f"   ✅ Logo permanent créé: {permanent_logo}")
                
                # Créer ou mettre à jour l'organisation
                org = Organizacion.get()
                if not org or not org.nombre:
                    org = Organizacion(
                        nombre="Demo Company",
                        direccion="123 Demo Street",
                        telefono="123-456-789",
                        email="demo@company.com",
                        cif="B12345678"
                    )
                
                org.logo_path = permanent_logo
                org.save()
                
                print(f"   ✅ Organisation mise à jour avec le logo de démonstration")
                print(f"   🎉 Logo de démonstration configuré!")
                
                # Vérifier immédiatement
                org_check = Organizacion.get()
                print(f"   🔍 Vérification: logo path = '{org_check.logo_path}'")
                print(f"   🔍 Fichier existe: {os.path.exists(org_check.logo_path) if org_check.logo_path else False}")
                
                return True
            else:
                print(f"   ❌ Échec création logo permanent")
                return False
                
        finally:
            # Nettoyer le logo temporaire
            if os.path.exists(temp_logo):
                os.remove(temp_logo)
            os.rmdir(temp_dir)
    
    def test_comprehensive_logo_diagnosis(self):
        """Diagnostic complet du système de logo"""
        print(f"\n🏥 Diagnostic complet du système de logo")
        print(f"=" * 45)
        
        results = {
            'organization_exists': False,
            'logo_configured': False,
            'logo_file_exists': False,
            'logo_in_permanent_dir': False,
            'logo_directory_ok': False,
            'logo_loadable': False
        }
        
        # 1. Vérifier l'organisation
        org = Organizacion.get()
        if org and org.nombre:
            results['organization_exists'] = True
            print(f"   ✅ Organisation: {org.nombre}")
            
            # 2. Vérifier le logo configuré
            if org.logo_path:
                results['logo_configured'] = True
                print(f"   ✅ Logo configuré: {org.logo_path}")
                
                # 3. Vérifier l'existence du fichier
                if os.path.exists(org.logo_path):
                    results['logo_file_exists'] = True
                    print(f"   ✅ Fichier logo existe")
                    
                    # 4. Vérifier le répertoire permanent
                    logo_manager = LogoManager()
                    if logo_manager.logo_directory in org.logo_path:
                        results['logo_in_permanent_dir'] = True
                        print(f"   ✅ Logo dans répertoire permanent")
                    else:
                        print(f"   ⚠️  Logo PAS dans répertoire permanent")
                    
                    # 5. Tester le chargement
                    try:
                        with Image.open(org.logo_path) as img:
                            results['logo_loadable'] = True
                            print(f"   ✅ Logo chargeable ({img.size})")
                    except Exception as e:
                        print(f"   ❌ Logo non chargeable: {e}")
                else:
                    print(f"   ❌ Fichier logo n'existe pas")
            else:
                print(f"   ℹ️  Aucun logo configuré")
        else:
            print(f"   ℹ️  Aucune organisation configurée")
        
        # 6. Vérifier le répertoire des logos
        logo_manager = LogoManager()
        if os.path.exists(logo_manager.logo_directory):
            results['logo_directory_ok'] = True
            print(f"   ✅ Répertoire logos OK: {logo_manager.logo_directory}")
        else:
            print(f"   ❌ Répertoire logos manquant: {logo_manager.logo_directory}")
        
        # Résumé
        print(f"\n   📊 Résumé du diagnostic:")
        for key, value in results.items():
            status = "✅" if value else "❌"
            print(f"      {status} {key.replace('_', ' ').title()}")
        
        # Recommandations
        print(f"\n   💡 Recommandations:")
        if not results['organization_exists']:
            print(f"      - Configurer une organisation dans l'interface")
        elif not results['logo_configured']:
            print(f"      - Sélectionner un logo dans les paramètres d'organisation")
        elif not results['logo_file_exists']:
            print(f"      - Le fichier logo a été supprimé, sélectionner un nouveau logo")
        elif not results['logo_in_permanent_dir']:
            print(f"      - Exécuter test_fix_logo_persistence_if_needed() pour corriger")
        elif not results['logo_loadable']:
            print(f"      - Le fichier logo est corrompu, sélectionner un nouveau logo")
        else:
            print(f"      - Système de logo entièrement fonctionnel! 🎉")
        
        return all(results.values())


if __name__ == "__main__":
    # Exécuter les tests de diagnostic
    tester = TestLogoPersistenceRealApp()
    
    print("🔍 DIAGNOSTIC DU SYSTÈME DE LOGO")
    print("=" * 50)
    
    # Test 1: État actuel
    tester.test_current_logo_status()
    
    # Test 2: Répertoire
    tester.test_logo_directory_status()
    
    # Test 3: Diagnostic complet
    tester.test_comprehensive_logo_diagnosis()
    
    # Test 4: Correction si nécessaire
    tester.test_fix_logo_persistence_if_needed()
    
    print(f"\n🎉 Diagnostic terminé!")
    print(f"Si le problème persiste, exécutez:")
    print(f"python test/regression/test_logo_persistence_real_app.py")
