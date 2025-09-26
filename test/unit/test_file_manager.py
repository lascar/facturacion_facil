#!/usr/bin/env python3
"""
Tests unitaires pour le FileManager et ImageFileManager
Tests de la nouvelle architecture factorée
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def create_test_image(path, format='PNG'):
    """Créer une image de test valide avec PIL"""
    try:
        from PIL import Image
        
        # Créer une image simple 10x10 pixels
        if format.upper() == 'JPEG':
            img = Image.new('RGB', (10, 10), color='red')
            img.save(path, 'JPEG')
        else:
            img = Image.new('RGBA', (10, 10), color='blue')
            img.save(path, 'PNG')
            
    except Exception as e:
        print(f"Erreur création image test: {e}")
        # Fallback: créer un fichier vide
        with open(path, 'w') as f:
            f.write("")

def test_file_manager_basic():
    """Test des fonctionnalités de base du FileManager"""
    print("🧪 Test: FileManager fonctionnalités de base")
    
    try:
        from utils.file_manager import FileManager
        
        # Créer un répertoire temporaire pour les tests
        temp_source_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_source_dir, 'test_file.txt')
        
        # Créer un fichier de test
        with open(temp_file_path, 'w') as f:
            f.write("Test content")
        
        try:
            # Créer FileManager avec répertoire temporaire
            file_manager = FileManager(base_directory=temp_source_dir, subdirectory="test_files")
            
            print(f"   📁 Répertoire stockage: {file_manager.storage_directory}")
            print(f"   📄 Fichier source: {temp_file_path}")
            
            # Test 1: Sauvegarder fichier
            print("\n   1️⃣ Test sauvegarde fichier")
            
            saved_path = file_manager.save_file(temp_file_path, "test_prefix")
            
            assert saved_path is not None, "Sauvegarde fichier échouée"
            assert os.path.exists(saved_path), f"Fichier sauvegardé n'existe pas: {saved_path}"
            assert saved_path.startswith(file_manager.storage_directory), f"Fichier pas dans bon répertoire: {saved_path}"
            
            print(f"   ✅ Fichier sauvegardé: {os.path.basename(saved_path)}")
            
            # Test 2: Vérifier info fichier
            print("\n   2️⃣ Test info fichier")
            
            info = file_manager.get_file_info(saved_path)
            
            assert info['exists'] == True, "Fichier info indique qu'il n'existe pas"
            assert info['size'] > 0, f"Taille fichier incorrecte: {info['size']}"
            assert info['extension'] == '.txt', f"Extension incorrecte: {info['extension']}"
            
            print(f"   ✅ Info fichier: {info['extension']} ({info['size']} bytes)")
            
            # Test 3: Lister fichiers
            print("\n   3️⃣ Test listage fichiers")
            
            files = file_manager.list_files()
            
            assert len(files) >= 1, f"Aucun fichier trouvé: {files}"
            assert saved_path in files, f"Fichier sauvegardé non trouvé dans liste: {saved_path}"
            
            print(f"   ✅ Fichiers trouvés: {len(files)}")
            
            # Test 4: Supprimer fichier
            print("\n   4️⃣ Test suppression fichier")
            
            success = file_manager.remove_file(saved_path)
            
            assert success == True, "Suppression fichier échouée"
            assert not os.path.exists(saved_path), f"Fichier toujours présent après suppression: {saved_path}"
            
            print("   ✅ Fichier supprimé avec succès")
            
            print("\n🎉 TOUS LES TESTS FILEMANAGER PASSENT")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_source_dir):
                    shutil.rmtree(temp_source_dir)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_file_manager():
    """Test du ImageFileManager spécialisé"""
    print("\n🧪 Test: ImageFileManager spécialisé")
    
    try:
        from utils.file_manager import ImageFileManager
        
        # Créer un répertoire temporaire pour les tests
        temp_source_dir = tempfile.mkdtemp()
        temp_image_path = os.path.join(temp_source_dir, 'test_image.png')
        temp_invalid_path = os.path.join(temp_source_dir, 'invalid.txt')
        
        # Créer une image de test et un fichier invalide
        create_test_image(temp_image_path, 'PNG')
        with open(temp_invalid_path, 'w') as f:
            f.write("Not an image")
        
        try:
            # Créer ImageFileManager
            image_manager = ImageFileManager(subdirectory="test_images")
            
            print(f"   📁 Répertoire images: {image_manager.storage_directory}")
            print(f"   🖼️ Image source: {temp_image_path}")
            print(f"   📄 Fichier invalide: {temp_invalid_path}")
            
            # Test 1: Validation d'image
            print("\n   1️⃣ Test validation images")
            
            is_valid_image = image_manager.is_valid_image(temp_image_path)
            is_invalid_image = image_manager.is_valid_image(temp_invalid_path)
            
            assert is_valid_image == True, f"Image valide non reconnue: {temp_image_path}"
            assert is_invalid_image == False, f"Fichier invalide reconnu comme image: {temp_invalid_path}"
            
            print("   ✅ Validation images fonctionne")
            
            # Test 2: Sauvegarder image valide
            print("\n   2️⃣ Test sauvegarde image valide")
            
            saved_image = image_manager.save_file(temp_image_path, "test_image")
            
            assert saved_image is not None, "Sauvegarde image valide échouée"
            assert os.path.exists(saved_image), f"Image sauvegardée n'existe pas: {saved_image}"
            
            print(f"   ✅ Image valide sauvegardée: {os.path.basename(saved_image)}")
            
            # Test 3: Rejeter fichier invalide
            print("\n   3️⃣ Test rejet fichier invalide")
            
            saved_invalid = image_manager.save_file(temp_invalid_path, "invalid_image")
            
            assert saved_invalid is None, f"Fichier invalide accepté: {saved_invalid}"
            
            print("   ✅ Fichier invalide correctement rejeté")
            
            # Test 4: Info image détaillée
            print("\n   4️⃣ Test info image détaillée")
            
            image_info = image_manager.get_image_info(saved_image)
            
            assert image_info['exists'] == True, "Image info indique qu'elle n'existe pas"
            assert image_info['format'] == 'PNG', f"Format incorrect: {image_info['format']}"
            assert image_info['dimensions'] == (10, 10), f"Dimensions incorrectes: {image_info['dimensions']}"
            
            print(f"   ✅ Info image: {image_info['format']} {image_info['size_str']}")
            
            # Test 5: Lister images
            print("\n   5️⃣ Test listage images")
            
            images = image_manager.list_images()
            
            assert len(images) >= 1, f"Aucune image trouvée: {images}"
            assert saved_image in images, f"Image sauvegardée non trouvée: {saved_image}"
            
            print(f"   ✅ Images trouvées: {len(images)}")
            
            # Nettoyage
            image_manager.remove_file(saved_image)
            
            print("\n🎉 TOUS LES TESTS IMAGEFILEMANAGER PASSENT")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_source_dir):
                    shutil.rmtree(temp_source_dir)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logo_manager_refactored():
    """Test du LogoManager refactoré"""
    print("\n🧪 Test: LogoManager refactoré")
    
    try:
        from utils.logo_manager import LogoManager
        
        # Créer un répertoire temporaire pour les tests
        temp_source_dir = tempfile.mkdtemp()
        temp_logo_path = os.path.join(temp_source_dir, 'test_logo.png')
        create_test_image(temp_logo_path, 'PNG')
        
        try:
            # Créer LogoManager
            logo_manager = LogoManager()
            
            print(f"   📁 Répertoire logos: {logo_manager.logo_directory}")
            print(f"   🖼️ Logo source: {temp_logo_path}")
            
            # Test 1: Sauvegarder logo (utilise FileManager en interne)
            print("\n   1️⃣ Test sauvegarde logo refactoré")
            
            saved_logo = logo_manager.save_logo(temp_logo_path, "Test Company")
            
            assert saved_logo is not None, "Sauvegarde logo échouée"
            assert os.path.exists(saved_logo), f"Logo sauvegardé n'existe pas: {saved_logo}"
            assert "Test_Company_logo" in os.path.basename(saved_logo), f"Nom logo incorrect: {saved_logo}"
            
            print(f"   ✅ Logo sauvegardé: {os.path.basename(saved_logo)}")
            
            # Test 2: Info logo (utilise ImageFileManager)
            print("\n   2️⃣ Test info logo refactoré")
            
            logo_info = logo_manager.get_logo_info(saved_logo)
            
            assert logo_info['exists'] == True, "Logo info indique qu'il n'existe pas"
            assert logo_info['format'] == 'PNG', f"Format incorrect: {logo_info['format']}"
            assert 'dimensions' in logo_info, "Dimensions manquantes dans info"
            
            print(f"   ✅ Info logo: {logo_info['format']} {logo_info.get('size_str', 'N/A')}")
            
            # Test 3: Lister logos (utilise ImageFileManager)
            print("\n   3️⃣ Test listage logos refactoré")
            
            logos = logo_manager.list_logos()
            
            assert len(logos) >= 1, f"Aucun logo trouvé: {logos}"
            assert saved_logo in logos, f"Logo sauvegardé non trouvé: {saved_logo}"
            
            print(f"   ✅ Logos trouvés: {len(logos)}")
            
            # Test 4: Supprimer logo (utilise FileManager)
            print("\n   4️⃣ Test suppression logo refactoré")
            
            success = logo_manager.remove_logo(saved_logo)
            
            assert success == True, "Suppression logo échouée"
            assert not os.path.exists(saved_logo), f"Logo toujours présent: {saved_logo}"
            
            print("   ✅ Logo supprimé avec succès")
            
            print("\n🎉 LOGOMANAGER REFACTORÉ FONCTIONNE")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_source_dir):
                    shutil.rmtree(temp_source_dir)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Tests unitaires - Architecture factorée")
    print("=" * 50)
    
    success1 = test_file_manager_basic()
    success2 = test_image_file_manager()
    success3 = test_logo_manager_refactored()
    
    if success1 and success2 and success3:
        print("\n🎉 TOUS LES TESTS DE L'ARCHITECTURE FACTORÉE PASSENT")
        print("\n✅ FACTORISATION VALIDÉE:")
        print("   • FileManager: Gestion générique de fichiers")
        print("   • ImageFileManager: Spécialisation pour images")
        print("   • LogoManager: Simplifié et réutilise les composants")
        print("   • Code plus simple et maintenable")
        print("\n💡 L'architecture factorée est opérationnelle !")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ÉCHOUENT")
        sys.exit(1)
