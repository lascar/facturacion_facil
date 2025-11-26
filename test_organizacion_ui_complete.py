#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de l'interface d'organisation avec sauvegarde du logo
"""

import sys
import os
import tempfile
from PIL import Image

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from ui.organizacion_pyqt6 import OrganizacionPyQt6Window
from database.database import db
from database.models import Organizacion

def create_test_logo():
    """Crée un logo de test temporaire"""
    img = Image.new('RGB', (200, 100), color='red')
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_organizacion_ui():
    """Test de l'interface d'organisation"""
    print("🧪 Test de l'interface d'organisation avec sauvegarde...")
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer l'application Qt
    app = QApplication.instance() or QApplication([])
    
    # Créer un logo de test
    test_logo_path = create_test_logo()
    print(f"   📁 Logo de test créé: {test_logo_path}")
    
    try:
        # Créer la fenêtre d'organisation
        org_window = OrganizacionPyQt6Window()
        
        # Vérifier que les méthodes existent
        assert hasattr(org_window, 'load_organization_data'), "Méthode load_organization_data manquante"
        assert hasattr(org_window, 'save_organization'), "Méthode save_organization manquante"
        assert hasattr(org_window, 'select_logo'), "Méthode select_logo manquante"
        assert hasattr(org_window, 'logo_manager'), "LogoManager manquant"
        
        print("   ✅ Fenêtre d'organisation créée avec toutes les méthodes")
        
        # Simuler la sélection d'un logo
        org_window.selected_logo_path = test_logo_path
        
        # Remplir les champs
        org_window.company_name_edit.setText("Test Company UI")
        org_window.nif_edit.setText("87654321B")
        org_window.address_edit.setPlainText("Test Address\n12345 Test City")
        org_window.phone_edit.setText("987654321")
        org_window.email_edit.setText("test@ui.com")
        
        print("   ✅ Champs remplis")
        
        # Sauvegarder
        org_window.save_organization()
        
        print("   ✅ Sauvegarde effectuée")
        
        # Vérifier que les données ont été sauvegardées
        saved_org = Organizacion.get()
        assert saved_org is not None, "Organisation non sauvegardée"
        assert saved_org.nombre == "Test Company UI", f"Nom incorrect: {saved_org.nombre}"
        assert saved_org.cif == "87654321B", f"CIF incorrect: {saved_org.cif}"
        assert saved_org.logo_path != "", "Logo non sauvegardé"
        assert os.path.exists(saved_org.logo_path), "Fichier logo non trouvé"
        
        print(f"   ✅ Données sauvegardées: {saved_org.nombre}")
        print(f"   ✅ Logo sauvegardé: {saved_org.logo_path}")
        
        # Test de rechargement des données
        org_window2 = OrganizacionPyQt6Window()
        org_window2.load_organization_data()
        
        # Vérifier que les données sont rechargées
        assert org_window2.company_name_edit.text() == "Test Company UI", "Nom non rechargé"
        assert org_window2.nif_edit.text() == "87654321B", "CIF non rechargé"
        assert org_window2.current_logo_path == saved_org.logo_path, "Logo non rechargé"
        
        print("   ✅ Données rechargées correctement")
        
        # Test de suppression du logo
        org_window2.remove_logo()
        org_window2.save_organization()
        
        # Vérifier la suppression
        final_org = Organizacion.get()
        assert final_org.logo_path == "", "Logo non supprimé"
        
        print("   ✅ Suppression du logo réussie")
        
        print("\n🎉 Test complet de l'interface d'organisation réussi !")
        return True
        
    except Exception as e:
        print(f"\n❌ Test échoué: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Nettoyer
        try:
            if os.path.exists(test_logo_path):
                os.unlink(test_logo_path)
        except:
            pass

if __name__ == "__main__":
    try:
        success = test_organizacion_ui()
        
        if success:
            print("\n✅ L'interface d'organisation avec sauvegarde du logo fonctionne parfaitement !")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        sys.exit(1)
