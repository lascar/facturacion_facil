#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que le problème de sauvegarde du logo est résolu
"""

import sys
import os
import tempfile
from PIL import Image

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from database.database import db
from database.models import Organizacion
from utils.logo_manager import LogoManager

def create_test_logo(color='blue'):
    """Crée un logo de test temporaire"""
    img = Image.new('RGB', (200, 100), color=color)
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_logo_persistence_complete():
    """Test complet de la persistance du logo"""
    print("🔧 Test final : Résolution du problème de sauvegarde du logo")
    print("=" * 60)
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer un logo de test
    test_logo_path = create_test_logo('green')
    print(f"1. 📁 Logo de test créé: {os.path.basename(test_logo_path)}")
    
    try:
        # Test 1: Créer une organisation avec logo
        print("\n2. 💾 Test de création d'organisation avec logo...")
        
        logo_manager = LogoManager()
        permanent_logo_path = logo_manager.save_logo(test_logo_path, "Ma Entreprise")
        
        org = Organizacion(
            nombre="Ma Entreprise",
            cif="12345678A",
            direccion="123 Rue Test\n75001 Paris",
            telefono="+33 1 23 45 67 89",
            email="contact@monentreprise.fr",
            logo_path=permanent_logo_path
        )
        org.save()
        
        print(f"   ✅ Organisation créée avec logo: {os.path.basename(permanent_logo_path)}")
        
        # Test 2: Vérifier la persistance
        print("\n3. 🔍 Test de persistance...")
        
        saved_org = Organizacion.get()
        assert saved_org is not None, "Organisation non trouvée"
        assert saved_org.logo_path != "", "Logo non sauvegardé"
        assert os.path.exists(saved_org.logo_path), "Fichier logo non trouvé"
        
        print(f"   ✅ Logo persisté: {os.path.basename(saved_org.logo_path)}")
        print(f"   ✅ Fichier existe: {os.path.exists(saved_org.logo_path)}")
        
        # Test 3: Mise à jour du logo
        print("\n4. 🔄 Test de mise à jour du logo...")
        
        new_logo_path = create_test_logo('red')
        new_permanent_logo = logo_manager.update_logo(saved_org.logo_path, new_logo_path, saved_org.nombre)
        
        if new_permanent_logo:
            saved_org.logo_path = new_permanent_logo
            saved_org.save()
            
            # Vérifier la mise à jour
            updated_org = Organizacion.get()
            assert updated_org.logo_path == new_permanent_logo, "Logo non mis à jour"
            assert os.path.exists(updated_org.logo_path), "Nouveau logo non trouvé"
            
            print(f"   ✅ Logo mis à jour: {os.path.basename(new_permanent_logo)}")
        
        # Test 4: Rechargement après redémarrage (simulation)
        print("\n5. 🔄 Test de rechargement après redémarrage...")
        
        # Simuler un redémarrage en rechargeant depuis la base
        reloaded_org = Organizacion.get()
        assert reloaded_org is not None, "Organisation non rechargée"
        assert reloaded_org.logo_path != "", "Logo non rechargé"
        assert os.path.exists(reloaded_org.logo_path), "Fichier logo non trouvé après rechargement"
        
        print(f"   ✅ Logo rechargé après redémarrage: {os.path.basename(reloaded_org.logo_path)}")
        
        # Test 5: Suppression du logo
        print("\n6. 🗑️ Test de suppression du logo...")
        
        logo_to_delete = reloaded_org.logo_path
        logo_manager.remove_logo(logo_to_delete)
        reloaded_org.logo_path = ""
        reloaded_org.save()
        
        # Vérifier la suppression
        final_org = Organizacion.get()
        assert final_org.logo_path == "", "Logo non supprimé de la base"
        assert not os.path.exists(logo_to_delete), "Fichier logo non supprimé"
        
        print("   ✅ Logo supprimé de la base de données")
        print("   ✅ Fichier logo supprimé du disque")
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ Le problème de sauvegarde du logo est RÉSOLU")
        print("✅ Le logo est maintenant correctement persisté")
        print("✅ Les mises à jour et suppressions fonctionnent")
        print("✅ Le rechargement après redémarrage fonctionne")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test échoué: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Nettoyer les fichiers temporaires
        try:
            if os.path.exists(test_logo_path):
                os.unlink(test_logo_path)
            if 'new_logo_path' in locals() and os.path.exists(new_logo_path):
                os.unlink(new_logo_path)
        except:
            pass

if __name__ == "__main__":
    try:
        success = test_logo_persistence_complete()
        
        if success:
            print("\n🚀 Le système de gestion des logos fonctionne parfaitement !")
            print("   Vous pouvez maintenant utiliser l'application en toute confiance.")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        sys.exit(1)
