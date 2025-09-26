#!/usr/bin/env python3
"""
Test de régression pour la persistance du logo de l'entreprise
Bug: Le logo ne reste pas après redémarrage de l'application
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_logo_persistence():
    """Test que le logo de l'organisation persiste après sauvegarde et rechargement"""
    print("🧪 Test: Persistance du logo de l'organisation")

    try:
        from database.models import Organizacion
        from database.database import Database

        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')

        # Créer une image temporaire pour le test
        temp_image_dir = tempfile.mkdtemp()
        temp_image_path = os.path.join(temp_image_dir, 'test_logo.png')

        # Créer un fichier image factice
        with open(temp_image_path, 'wb') as f:
            # Créer un PNG minimal valide (1x1 pixel transparent)
            png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            f.write(png_data)

        try:
            # Créer nouvelle instance de base de données
            db = Database(temp_db_path)

            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path

            print(f"   📁 Base de données temporaire: {temp_db_path}")
            print(f"   🖼️ Image temporaire: {temp_image_path}")

            # Test 1: Créer et sauvegarder organisation avec logo
            print("\n   1️⃣ Création organisation avec logo")

            org = Organizacion(
                nombre="Test Empresa",
                cif="B12345678",
                direccion="Calle Test 123",
                telefono="123456789",
                email="test@empresa.com",
                logo_path=temp_image_path
            )

            # Vérifier que le logo_path est défini
            assert org.logo_path == temp_image_path, f"Logo path incorrect: {org.logo_path}"
            print(f"   ✅ Logo path défini: {org.logo_path}")

            # Sauvegarder
            org.save()
            print("   ✅ Organisation sauvegardée")

            # Test 2: Vérifier sauvegarde en base de données
            print("\n   2️⃣ Vérification sauvegarde en base")

            # Vérifier directement en base de données
            query = "SELECT logo_path FROM organizacion WHERE id=1"
            results = global_db.execute_query(query)

            assert len(results) > 0, "Aucune organisation trouvée en base"
            logo_path_db = results[0][0]

            print(f"   📊 Logo en base: {logo_path_db}")
            assert logo_path_db == temp_image_path, f"Logo path en base incorrect: {logo_path_db}"
            print("   ✅ Logo correctement sauvegardé en base")

            # Test 3: Recharger organisation et vérifier persistance
            print("\n   3️⃣ Rechargement et vérification persistance")

            org_reloaded = Organizacion.get()

            print(f"   📊 Logo rechargé: {org_reloaded.logo_path}")
            assert org_reloaded.logo_path == temp_image_path, f"Logo path perdu après rechargement: {org_reloaded.logo_path}"
            print("   ✅ Logo persiste après rechargement")

            # Test 4: Simuler redémarrage application (nouvelle instance DB)
            print("\n   4️⃣ Simulation redémarrage application")

            # Créer nouvelle instance de base de données (simule redémarrage)
            db2 = Database(temp_db_path)

            org_after_restart = Organizacion.get()

            print(f"   📊 Logo après redémarrage: {org_after_restart.logo_path}")
            assert org_after_restart.logo_path == temp_image_path, f"Logo path perdu après redémarrage: {org_after_restart.logo_path}"
            print("   ✅ Logo persiste après redémarrage simulé")

            # Test 5: Vérifier que le fichier image existe toujours
            print("\n   5️⃣ Vérification existence fichier image")

            assert os.path.exists(org_after_restart.logo_path), f"Fichier image n'existe plus: {org_after_restart.logo_path}"
            print("   ✅ Fichier image existe toujours")

            print("\n🎉 TOUS LES TESTS PASSENT - Logo persiste correctement")
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

def test_logo_update_persistence():
    """Test que la mise à jour du logo persiste correctement"""
    print("\n🧪 Test: Persistance mise à jour du logo")

    try:
        from database.models import Organizacion
        from database.database import Database

        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')

        # Créer deux images temporaires
        temp_image_dir = tempfile.mkdtemp()
        temp_image1_path = os.path.join(temp_image_dir, 'logo1.png')
        temp_image2_path = os.path.join(temp_image_dir, 'logo2.png')

        # Créer fichiers images factices
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'

        with open(temp_image1_path, 'wb') as f:
            f.write(png_data)
        with open(temp_image2_path, 'wb') as f:
            f.write(png_data)

        try:
            # Initialiser la base de données
            db = Database(temp_db_path)

            # Créer organisation avec premier logo
            org = Organizacion(
                nombre="Test Empresa",
                logo_path=temp_image1_path
            )
            org.save()

            print(f"   📊 Premier logo: {org.logo_path}")

            # Mettre à jour avec deuxième logo
            org.logo_path = temp_image2_path
            org.save()

            print(f"   📊 Deuxième logo: {org.logo_path}")

            # Vérifier persistance
            org_reloaded = Organizacion.get()

            print(f"   📊 Logo après rechargement: {org_reloaded.logo_path}")
            assert org_reloaded.logo_path == temp_image2_path, f"Mise à jour logo non persistée: {org_reloaded.logo_path}"

            print("   ✅ Mise à jour du logo persiste correctement")
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

if __name__ == "__main__":
    print("🔧 Tests de régression - Persistance du logo")
    print("=" * 50)

    success1 = test_logo_persistence()
    success2 = test_logo_update_persistence()

    if success1 and success2:
        print("\n🎉 TOUS LES TESTS DE RÉGRESSION PASSENT")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ÉCHOUENT")
        sys.exit(1)