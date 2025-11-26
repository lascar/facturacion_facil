#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que la sauvegarde du logo fonctionne
"""

import sys
import os
import tempfile
import shutil
from PIL import Image

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from PyQt6.QtWidgets import QApplication
from database.database import db
from database.models import Organizacion
from utils.logo_manager import LogoManager

def create_test_logo():
    """Crée un logo de test temporaire"""
    # Créer une image simple de test
    img = Image.new('RGB', (200, 100), color='blue')
    
    # Sauvegarder dans un fichier temporaire
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    
    return temp_file.name

def test_logo_persistence():
    """Test de la persistance du logo"""
    print("🧪 Test de la persistance du logo...")
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer un logo de test
    test_logo_path = create_test_logo()
    print(f"   📁 Logo de test créé: {test_logo_path}")
    
    try:
        # Créer une organisation avec logo
        logo_manager = LogoManager()
        
        # Sauvegarder le logo
        permanent_logo_path = logo_manager.save_logo(test_logo_path, "Test Company")
        print(f"   💾 Logo sauvegardé: {permanent_logo_path}")
        
        assert permanent_logo_path is not None, "Le logo n'a pas été sauvegardé"
        assert os.path.exists(permanent_logo_path), "Le fichier logo permanent n'existe pas"
        
        # Créer et sauvegarder l'organisation
        org = Organizacion(
            nombre="Test Company",
            cif="12345678A",
            direccion="Test Address",
            telefono="123456789",
            email="test@company.com",
            logo_path=permanent_logo_path
        )
        org.save()
        print("   💾 Organisation sauvegardée avec logo")
        
        # Vérifier que l'organisation a été sauvegardée
        saved_org = Organizacion.get()
        assert saved_org is not None, "L'organisation n'a pas été sauvegardée"
        assert saved_org.logo_path == permanent_logo_path, "Le chemin du logo n'a pas été sauvegardé"
        assert os.path.exists(saved_org.logo_path), "Le fichier logo n'existe pas après sauvegarde"
        
        print("   ✅ Logo persisté correctement en base de données")
        
        # Test de mise à jour du logo
        new_test_logo = create_test_logo()
        new_permanent_logo = logo_manager.update_logo(permanent_logo_path, new_test_logo, "Test Company")
        
        if new_permanent_logo:
            org.logo_path = new_permanent_logo
            org.save()
            
            # Vérifier la mise à jour
            updated_org = Organizacion.get()
            assert updated_org.logo_path == new_permanent_logo, "Le logo n'a pas été mis à jour"
            assert os.path.exists(updated_org.logo_path), "Le nouveau logo n'existe pas"
            
            print("   ✅ Mise à jour du logo réussie")
        
        # Test de suppression du logo
        if org.logo_path:
            logo_manager.remove_logo(org.logo_path)
            org.logo_path = ""
            org.save()
            
            # Vérifier la suppression
            final_org = Organizacion.get()
            assert final_org.logo_path == "", "Le logo n'a pas été supprimé de la base"
            
            print("   ✅ Suppression du logo réussie")
        
        print("\n🎉 Tous les tests de persistance du logo sont passés !")
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
            if 'new_test_logo' in locals() and os.path.exists(new_test_logo):
                os.unlink(new_test_logo)
        except:
            pass

if __name__ == "__main__":
    try:
        # Créer l'application Qt (nécessaire pour certains tests)
        app = QApplication.instance() or QApplication([])
        
        success = test_logo_persistence()
        
        if success:
            print("\n✅ Le système de persistance du logo fonctionne correctement !")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        sys.exit(1)
