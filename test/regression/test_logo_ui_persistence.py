#!/usr/bin/env python3
"""
Test de régression pour la persistance du logo via l'interface utilisateur
Bug rapporté: Le logo ne reste pas après fermeture/réouverture de l'application
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_logo_ui_workflow():
    """Test du workflow complet de sélection et persistance du logo via UI"""
    print("🧪 Test: Workflow UI complet du logo")
    
    try:
        from database.models import Organizacion
        from database.database import Database
        from ui.organizacion import OrganizacionWindow
        import customtkinter as ctk
        
        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')
        
        # Créer une image temporaire
        temp_image_dir = tempfile.mkdtemp()
        temp_image_path = os.path.join(temp_image_dir, 'test_logo.png')
        
        # Créer un fichier image factice
        with open(temp_image_path, 'wb') as f:
            # PNG minimal valide
            png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            f.write(png_data)
        
        try:
            # Initialiser la base de données
            db = Database(temp_db_path)
            
            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path
            
            print(f"   📁 Base de données temporaire: {temp_db_path}")
            print(f"   🖼️ Image temporaire: {temp_image_path}")
            
            # Test 1: Simuler sélection de logo via UI
            print("\n   1️⃣ Simulation sélection logo via UI")
            
            # Créer une organisation vide d'abord
            org_initial = Organizacion(
                nombre="Test Empresa",
                cif="B12345678"
            )
            org_initial.save()
            print("   ✅ Organisation initiale créée")
            
            # Simuler la sélection du logo (comme dans OrganizacionWindow.select_logo)
            logo_path = temp_image_path
            
            # Simuler la sauvegarde (comme dans OrganizacionWindow.save_organizacion)
            organizacion = Organizacion(
                nombre="Test Empresa",
                cif="B12345678",
                direccion="Calle Test 123",
                telefono="123456789",
                email="test@empresa.com",
                logo_path=logo_path,  # Le logo sélectionné
                directorio_imagenes_defecto="",
                numero_factura_inicial=1,
                directorio_descargas_pdf="",
                visor_pdf_personalizado=""
            )
            
            organizacion.save()
            print(f"   ✅ Organisation sauvegardée avec logo: {logo_path}")
            
            # Test 2: Vérifier sauvegarde immédiate
            print("\n   2️⃣ Vérification sauvegarde immédiate")
            
            org_check = Organizacion.get()
            print(f"   📊 Logo après sauvegarde: {org_check.logo_path}")
            assert org_check.logo_path == logo_path, f"Logo path incorrect après sauvegarde: {org_check.logo_path}"
            print("   ✅ Logo correctement sauvegardé")
            
            # Test 3: Simuler fermeture/réouverture application
            print("\n   3️⃣ Simulation fermeture/réouverture application")
            
            # Simuler fermeture (nouvelle instance DB)
            db2 = Database(temp_db_path)
            
            # Simuler réouverture et chargement (comme dans OrganizacionWindow.load_organizacion_data)
            org_reloaded = Organizacion.get()
            
            print(f"   📊 Logo après réouverture: {org_reloaded.logo_path}")
            assert org_reloaded.logo_path == logo_path, f"Logo path perdu après réouverture: {org_reloaded.logo_path}"
            print("   ✅ Logo persiste après réouverture")
            
            # Test 4: Vérifier que le fichier existe toujours
            print("\n   4️⃣ Vérification existence fichier")
            
            assert os.path.exists(org_reloaded.logo_path), f"Fichier logo n'existe plus: {org_reloaded.logo_path}"
            print("   ✅ Fichier logo existe toujours")
            
            # Test 5: Simuler chargement UI (comme dans load_organizacion_data)
            print("\n   5️⃣ Simulation chargement UI")
            
            # Simuler le code de load_organizacion_data
            if org_reloaded.logo_path and os.path.exists(org_reloaded.logo_path):
                logo_path_ui = org_reloaded.logo_path
                print(f"   📊 Logo chargé dans UI: {logo_path_ui}")
                assert logo_path_ui == logo_path, f"Logo path UI incorrect: {logo_path_ui}"
                print("   ✅ Logo correctement chargé dans UI")
            else:
                raise AssertionError(f"Logo non chargé dans UI: path={org_reloaded.logo_path}, exists={os.path.exists(org_reloaded.logo_path) if org_reloaded.logo_path else False}")
            
            print("\n🎉 TOUS LES TESTS PASSENT - Logo persiste correctement via UI")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)
                if os.path.exists(temp_image_dir):
                    shutil.rmtree(temp_image_dir)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logo_path_edge_cases():
    """Test des cas limites pour le logo_path"""
    print("\n🧪 Test: Cas limites logo_path")
    
    try:
        from database.models import Organizacion
        from database.database import Database
        
        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')
        
        try:
            # Initialiser la base de données
            db = Database(temp_db_path)
            
            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path
            
            # Test 1: Logo path vide
            print("\n   1️⃣ Test logo_path vide")
            
            org1 = Organizacion(
                nombre="Test 1",
                logo_path=""  # Vide
            )
            org1.save()
            
            org1_check = Organizacion.get()
            print(f"   📊 Logo path vide: '{org1_check.logo_path}'")
            assert org1_check.logo_path == "", f"Logo path vide non préservé: '{org1_check.logo_path}'"
            print("   ✅ Logo path vide correctement géré")
            
            # Test 2: Logo path None
            print("\n   2️⃣ Test logo_path None")
            
            # Simuler un logo_path None (peut arriver dans certains cas)
            query = "UPDATE organizacion SET logo_path=NULL WHERE id=1"
            global_db.execute_query(query)
            
            org2_check = Organizacion.get()
            print(f"   📊 Logo path None: {org2_check.logo_path}")
            # Le modèle devrait convertir None en chaîne vide
            assert org2_check.logo_path == "" or org2_check.logo_path is None, f"Logo path None mal géré: {org2_check.logo_path}"
            print("   ✅ Logo path None correctement géré")
            
            # Test 3: Logo path avec chemin inexistant
            print("\n   3️⃣ Test logo_path fichier inexistant")
            
            fake_path = "/chemin/inexistant/logo.png"
            org3 = Organizacion(
                nombre="Test 3",
                logo_path=fake_path
            )
            org3.save()
            
            org3_check = Organizacion.get()
            print(f"   📊 Logo path inexistant: {org3_check.logo_path}")
            assert org3_check.logo_path == fake_path, f"Logo path inexistant non préservé: {org3_check.logo_path}"
            print("   ✅ Logo path inexistant correctement sauvegardé")
            
            print("\n🎉 TOUS LES TESTS CAS LIMITES PASSENT")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_debug_current_database():
    """Test de debug pour examiner la base de données actuelle"""
    print("\n🔍 Debug: Examen base de données actuelle")
    
    try:
        from database.models import Organizacion
        from database.database import Database, db
        
        print(f"   📁 Base de données actuelle: {db.db_path}")
        
        # Vérifier si une organisation existe
        try:
            org = Organizacion.get()
            if org:
                print(f"   📊 Organisation trouvée:")
                print(f"       Nom: {org.nombre}")
                print(f"       Logo path: '{org.logo_path}'")
                print(f"       Logo existe: {os.path.exists(org.logo_path) if org.logo_path else False}")
            else:
                print("   📊 Aucune organisation trouvée")
        except Exception as e:
            print(f"   ❌ Erreur récupération organisation: {e}")
        
        # Vérifier directement en base
        try:
            query = "SELECT id, nombre, logo_path FROM organizacion"
            results = db.execute_query(query)
            print(f"   📊 Résultats directs base de données:")
            for row in results:
                print(f"       ID: {row[0]}, Nom: {row[1]}, Logo: '{row[2]}'")
        except Exception as e:
            print(f"   ❌ Erreur requête directe: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ERREUR DEBUG: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Tests de régression - Persistance Logo UI")
    print("=" * 50)
    
    # Test de debug d'abord
    debug_success = test_debug_current_database()
    
    # Tests principaux
    success1 = test_logo_ui_workflow()
    success2 = test_logo_path_edge_cases()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS DE RÉGRESSION PASSENT")
        print("\n💡 Si le problème persiste, il pourrait être lié à:")
        print("   • Permissions de fichiers")
        print("   • Chemins relatifs vs absolus")
        print("   • Nettoyage de cache d'images")
        print("   • Problèmes de synchronisation UI")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ÉCHOUENT")
        sys.exit(1)
