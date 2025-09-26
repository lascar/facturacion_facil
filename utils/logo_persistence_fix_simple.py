#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaire simple de correction de la persistance du logo
"""

import os
import sys
import tempfile
from PIL import Image

# Ajouter le répertoire racine au path si nécessaire
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Organizacion
from utils.logo_manager import LogoManager


def diagnose_logo_issues():
    """Diagnostiquer les problèmes de logo"""
    print("🔍 Diagnostic des problèmes de logo...")
    
    issues = []
    
    # Vérifier l'organisation
    org = Organizacion.get()
    if not org or not org.nombre:
        issues.append("no_organization")
        print("   ⚠️  Aucune organisation configurée")
        return issues
    
    print(f"   ✅ Organisation trouvée: {org.nombre}")
    
    # Vérifier le logo configuré
    if not org.logo_path:
        issues.append("no_logo_configured")
        print("   ⚠️  Aucun logo configuré")
        return issues
    
    print(f"   ✅ Logo configuré: {org.logo_path}")
    
    # Vérifier l'existence du fichier
    if not os.path.exists(org.logo_path):
        issues.append("logo_file_missing")
        print(f"   ❌ Fichier logo manquant: {org.logo_path}")
        return issues
    
    print("   ✅ Fichier logo existe")
    
    # Vérifier le répertoire permanent
    logo_manager = LogoManager()
    if logo_manager.logo_directory not in org.logo_path:
        issues.append("logo_not_permanent")
        print(f"   ⚠️  Logo pas dans répertoire permanent: {org.logo_path}")
    else:
        print("   ✅ Logo dans répertoire permanent")
    
    # Vérifier la chargeabilité
    try:
        with Image.open(org.logo_path) as img:
            print(f"   ✅ Logo chargeable: {img.size}")
    except Exception as e:
        issues.append("logo_not_loadable")
        print(f"   ❌ Logo non chargeable: {e}")
    
    if not issues:
        print("   🎉 Aucun problème de logo détecté")
    
    return issues


def create_demo_organization():
    """Créer une organisation de démonstration avec logo"""
    print("🎨 Création d'une organisation de démonstration...")
    
    try:
        logo_manager = LogoManager()
        
        # Créer un logo de démonstration
        temp_dir = tempfile.mkdtemp()
        temp_logo = os.path.join(temp_dir, "demo_logo.png")
        
        # Créer une image simple
        img = Image.new('RGB', (200, 100), color='#2E86AB')
        img.save(temp_logo)
        
        # Copier vers répertoire permanent
        permanent_logo = logo_manager.save_logo(temp_logo, "Empresa Demo")
        
        if permanent_logo:
            # Créer organisation
            org = Organizacion(
                nombre="Empresa Demo",
                direccion="123 Calle Demo, Madrid, España",
                telefono="+34 91 123 45 67",
                email="demo@empresa.com",
                cif="B12345678",
                logo_path=permanent_logo
            )
            org.save()
            
            print(f"   ✅ Organisation créée: {org.nombre}")
            print(f"   ✅ Logo configuré: {permanent_logo}")
            
            # Nettoyer
            os.remove(temp_logo)
            os.rmdir(temp_dir)
            
            return True
        else:
            print("   ❌ Échec création logo permanent")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur création organisation: {e}")
        return False


def move_logo_to_permanent():
    """Déplacer le logo vers le répertoire permanent"""
    print("🔧 Déplacement du logo vers le répertoire permanent...")
    
    try:
        org = Organizacion.get()
        if not org or not org.logo_path:
            return False
        
        logo_manager = LogoManager()
        
        # Copier vers répertoire permanent
        permanent_logo = logo_manager.save_logo(org.logo_path, org.nombre)
        
        if permanent_logo:
            # Mettre à jour l'organisation
            org.logo_path = permanent_logo
            org.save()
            
            print(f"   ✅ Logo déplacé vers: {permanent_logo}")
            return True
        else:
            print("   ❌ Échec déplacement logo")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur déplacement logo: {e}")
        return False


def fix_logo_persistence():
    """Corriger les problèmes de persistance du logo"""
    print("🔧 Correction des problèmes de persistance...")
    
    issues = diagnose_logo_issues()
    
    if "no_organization" in issues:
        print("   → Création d'une organisation de démonstration...")
        return create_demo_organization()
    
    if "no_logo_configured" in issues:
        print("   → Aucun logo à corriger")
        return True
    
    if "logo_file_missing" in issues:
        print("   → Fichier logo manquant - impossible de corriger automatiquement")
        print("   💡 Solution: sélectionner un nouveau logo dans l'interface")
        return False
    
    if "logo_not_permanent" in issues:
        print("   → Déplacement vers répertoire permanent...")
        return move_logo_to_permanent()
    
    if "logo_not_loadable" in issues:
        print("   → Logo corrompu - impossible de corriger automatiquement")
        print("   💡 Solution: sélectionner un nouveau logo dans l'interface")
        return False
    
    print("   → Aucune correction nécessaire")
    return True


def verify_logo_persistence():
    """Vérifier que le logo persiste correctement"""
    print("🔍 Vérification de la persistance...")
    
    # Test 1: Vérifier l'état actuel
    issues = diagnose_logo_issues()
    if issues:
        print(f"   ❌ Problèmes détectés: {issues}")
        return False
    
    # Test 2: Simuler redémarrage (nouvelle instance)
    org = Organizacion.get()
    if not org or not org.logo_path:
        print("   ❌ Aucune organisation ou logo après redémarrage simulé")
        return False
    
    # Test 3: Vérifier l'existence du fichier
    if not os.path.exists(org.logo_path):
        print(f"   ❌ Fichier logo manquant après redémarrage: {org.logo_path}")
        return False
    
    # Test 4: Vérifier la chargeabilité
    try:
        with Image.open(org.logo_path) as img:
            print(f"   ✅ Logo persistant et chargeable: {img.size}")
            return True
    except Exception as e:
        print(f"   ❌ Logo non chargeable après redémarrage: {e}")
        return False


def main():
    """Fonction principale"""
    print("🔧 Utilitaire de correction de la persistance du logo")
    print("=" * 55)
    
    # Étape 1: Diagnostic
    print("\n📋 Étape 1: Diagnostic...")
    issues = diagnose_logo_issues()
    
    # Étape 2: Correction
    print("\n🔧 Étape 2: Correction...")
    fix_success = fix_logo_persistence()
    
    if not fix_success:
        print("\n❌ Correction échouée!")
        return False
    
    # Étape 3: Vérification
    print("\n✅ Étape 3: Vérification...")
    verify_success = verify_logo_persistence()
    
    if verify_success:
        print("\n🎉 Correction complète réussie!")
        print("Le logo devrait maintenant persister entre les redémarrages.")
        return True
    else:
        print("\n❌ Échec de la vérification!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
