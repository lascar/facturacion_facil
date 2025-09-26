#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour le LogoManager et la persistance du logo
"""

import os
import tempfile
import pytest
from PIL import Image
from database.models import Organizacion
from utils.logo_manager import LogoManager
from test.utils.test_database_manager import isolated_test_db


class TestLogoManagerIntegration:
    """Tests d'intégration pour LogoManager et persistance"""
    
    @pytest.fixture
    def temp_logo(self):
        """Crée un logo temporaire pour les tests"""
        temp_dir = tempfile.mkdtemp()
        logo_path = os.path.join(temp_dir, "source_logo.png")
        
        # Créer une image de test
        img = Image.new('RGB', (200, 100), color='green')
        img.save(logo_path)
        
        yield logo_path
        
        # Nettoyage
        if os.path.exists(logo_path):
            os.remove(logo_path)
        os.rmdir(temp_dir)
    
    def test_logo_manager_workflow_complete(self, temp_logo):
        """Test complet du workflow LogoManager + Organizacion"""
        with isolated_test_db("test_logo_manager_workflow") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Test complet LogoManager + Organizacion")
                print(f"=" * 50)
                
                # Étape 1: Initialiser LogoManager
                print(f"\n1️⃣ Initialisation du LogoManager")
                logo_manager = LogoManager()
                
                print(f"   📁 Répertoire logos: {logo_manager.logo_directory}")
                print(f"   ✅ Répertoire existe: {os.path.exists(logo_manager.logo_directory)}")
                
                # Vérifier que le répertoire est créé
                assert os.path.exists(logo_manager.logo_directory), "Répertoire logos non créé"
                
                # Étape 2: Sauvegarder logo avec LogoManager
                print(f"\n2️⃣ Sauvegarde du logo avec LogoManager")
                print(f"   📁 Logo source: {temp_logo}")
                print(f"   📊 Taille source: {os.path.getsize(temp_logo)} bytes")
                
                permanent_logo_path = logo_manager.save_logo(temp_logo, "Test Company")
                
                print(f"   📁 Logo permanent: {permanent_logo_path}")
                print(f"   ✅ Sauvegarde réussie: {permanent_logo_path is not None}")
                
                assert permanent_logo_path is not None, "Échec sauvegarde logo"
                assert os.path.exists(permanent_logo_path), f"Logo permanent n'existe pas: {permanent_logo_path}"
                assert permanent_logo_path != temp_logo, "Logo pas copié (même chemin)"
                
                # Vérifier que le logo est dans le bon répertoire
                assert logo_manager.logo_directory in permanent_logo_path, "Logo pas dans le répertoire permanent"
                
                print(f"   📊 Taille permanent: {os.path.getsize(permanent_logo_path)} bytes")
                
                # Étape 3: Créer organisation avec logo permanent
                print(f"\n3️⃣ Création organisation avec logo permanent")
                org = Organizacion(
                    nombre="Test Company LogoManager",
                    direccion="123 LogoManager Street",
                    telefono="123-456-789",
                    email="test@logomanager.com",
                    cif="B12345678",
                    logo_path=permanent_logo_path
                )
                org.save()
                
                print(f"   🏢 Organisation créée: {org.nombre}")
                print(f"   🖼️  Logo path: {org.logo_path}")
                
                # Étape 4: Vérifier persistance immédiate
                print(f"\n4️⃣ Vérification persistance immédiate")
                org_check = Organizacion.get()
                
                print(f"   🏢 Nom récupéré: '{org_check.nombre}'")
                print(f"   🖼️  Logo path récupéré: '{org_check.logo_path}'")
                print(f"   📁 Fichier existe: {os.path.exists(org_check.logo_path) if org_check.logo_path else False}")
                
                assert org_check.logo_path == permanent_logo_path, f"Logo path incorrect: {org_check.logo_path}"
                assert os.path.exists(org_check.logo_path), f"Fichier logo n'existe pas: {org_check.logo_path}"
                
                # Étape 5: Simuler redémarrage de l'application
                print(f"\n5️⃣ Simulation redémarrage application")
                
                # Créer un nouveau LogoManager (simule redémarrage)
                logo_manager_2 = LogoManager()
                print(f"   📁 Nouveau répertoire logos: {logo_manager_2.logo_directory}")
                print(f"   ✅ Même répertoire: {logo_manager_2.logo_directory == logo_manager.logo_directory}")
                
                # Récupérer organisation après "redémarrage"
                org_after_restart = Organizacion.get()
                
                print(f"   🏢 Nom après redémarrage: '{org_after_restart.nombre}'")
                print(f"   🖼️  Logo path après redémarrage: '{org_after_restart.logo_path}'")
                print(f"   📁 Fichier existe après redémarrage: {os.path.exists(org_after_restart.logo_path) if org_after_restart.logo_path else False}")
                
                assert org_after_restart.logo_path == permanent_logo_path, "Logo path perdu après redémarrage"
                assert os.path.exists(org_after_restart.logo_path), "Fichier logo perdu après redémarrage"
                
                # Étape 6: Test mise à jour du logo
                print(f"\n6️⃣ Test mise à jour du logo")
                
                # Créer un nouveau logo temporaire
                temp_dir2 = tempfile.mkdtemp()
                logo_path2 = os.path.join(temp_dir2, "new_logo.png")
                img2 = Image.new('RGB', (200, 100), color='blue')
                img2.save(logo_path2)
                
                try:
                    # Mettre à jour avec LogoManager
                    new_permanent_logo = logo_manager.update_logo(
                        org_after_restart.logo_path, 
                        logo_path2, 
                        "Test Company Updated"
                    )
                    
                    print(f"   🖼️  Nouveau logo permanent: {new_permanent_logo}")
                    print(f"   ✅ Mise à jour réussie: {new_permanent_logo is not None}")
                    
                    assert new_permanent_logo is not None, "Échec mise à jour logo"
                    assert os.path.exists(new_permanent_logo), "Nouveau logo n'existe pas"
                    assert not os.path.exists(permanent_logo_path), "Ancien logo pas supprimé"
                    
                    # Sauvegarder la nouvelle organisation
                    org_after_restart.logo_path = new_permanent_logo
                    org_after_restart.save()
                    
                    # Vérifier la persistance de la mise à jour
                    org_updated = Organizacion.get()
                    print(f"   🖼️  Logo final en base: '{org_updated.logo_path}'")
                    print(f"   📁 Fichier final existe: {os.path.exists(org_updated.logo_path) if org_updated.logo_path else False}")
                    
                    assert org_updated.logo_path == new_permanent_logo, "Mise à jour logo pas persistée"
                    assert os.path.exists(org_updated.logo_path), "Fichier logo final n'existe pas"
                    
                    print(f"   ✅ Mise à jour persistée avec succès")
                    
                finally:
                    # Nettoyer le logo temporaire 2
                    if os.path.exists(logo_path2):
                        os.remove(logo_path2)
                    os.rmdir(temp_dir2)
                
                # Étape 7: Test nettoyage
                print(f"\n7️⃣ Test nettoyage des logos orphelins")
                
                # Lister les logos avant nettoyage
                logos_before = logo_manager.list_logos()
                print(f"   📊 Logos avant nettoyage: {len(logos_before)}")
                
                # Nettoyer (garder seulement le logo actuel)
                cleaned_count = logo_manager.cleanup_orphaned_logos(org_updated.logo_path)
                print(f"   🗑️  Logos nettoyés: {cleaned_count}")
                
                # Lister les logos après nettoyage
                logos_after = logo_manager.list_logos()
                print(f"   📊 Logos après nettoyage: {len(logos_after)}")
                
                # Vérifier que le logo actuel existe toujours
                assert os.path.exists(org_updated.logo_path), "Logo actuel supprimé par erreur"
                
                print(f"\n🎉 Test complet LogoManager réussi!")
                
            finally:
                database.db = original_db
    
    def test_logo_manager_directory_creation(self):
        """Test de création du répertoire logos"""
        print(f"\n🔍 Test création répertoire LogoManager")
        print(f"=" * 40)
        
        # Créer LogoManager
        logo_manager = LogoManager()
        
        print(f"   📁 Répertoire: {logo_manager.logo_directory}")
        print(f"   ✅ Existe: {os.path.exists(logo_manager.logo_directory)}")
        print(f"   ✅ Accessible en écriture: {os.access(logo_manager.logo_directory, os.W_OK)}")
        
        # Vérifications
        assert os.path.exists(logo_manager.logo_directory), "Répertoire logos non créé"
        assert os.path.isdir(logo_manager.logo_directory), "Chemin logos n'est pas un répertoire"
        assert os.access(logo_manager.logo_directory, os.W_OK), "Répertoire logos non accessible en écriture"
        
        print(f"   ✅ Répertoire LogoManager fonctionnel")
    
    def test_logo_persistence_real_scenario(self, temp_logo):
        """Test de scénario réel : sélection logo + redémarrage"""
        with isolated_test_db("test_real_scenario") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Test scénario réel de persistance")
                print(f"=" * 40)
                
                # Simuler le workflow de l'interface utilisateur
                logo_manager = LogoManager()
                
                # 1. Utilisateur sélectionne un logo (simule select_logo())
                print(f"\n1️⃣ Simulation sélection logo utilisateur")
                organization_name = "Ma Super Entreprise"
                permanent_logo = logo_manager.save_logo(temp_logo, organization_name)
                
                print(f"   📁 Logo source: {temp_logo}")
                print(f"   📁 Logo permanent: {permanent_logo}")
                print(f"   ✅ Copie réussie: {permanent_logo is not None}")
                
                assert permanent_logo is not None, "Échec copie logo"
                assert os.path.exists(permanent_logo), "Logo permanent n'existe pas"
                
                # 2. Utilisateur sauvegarde l'organisation (simule save_organizacion())
                print(f"\n2️⃣ Simulation sauvegarde organisation")
                org = Organizacion(
                    nombre=organization_name,
                    direccion="123 Rue de l'Entreprise",
                    telefono="+33 1 23 45 67 89",
                    email="contact@superentreprise.fr",
                    cif="FR12345678901",
                    logo_path=permanent_logo
                )
                org.save()
                
                print(f"   🏢 Organisation sauvegardée: {org.nombre}")
                print(f"   🖼️  Logo path: {org.logo_path}")
                
                # 3. Utilisateur ferme l'application
                print(f"\n3️⃣ Simulation fermeture application")
                print(f"   💾 Données sauvegardées en base")
                
                # 4. Utilisateur redémarre l'application (simule load_organizacion_data())
                print(f"\n4️⃣ Simulation redémarrage et chargement")
                
                # Nouveau LogoManager (simule nouveau démarrage)
                logo_manager_restart = LogoManager()
                
                # Charger organisation depuis la base
                org_loaded = Organizacion.get()
                
                print(f"   🏢 Organisation chargée: {org_loaded.nombre}")
                print(f"   🖼️  Logo path chargé: {org_loaded.logo_path}")
                print(f"   📁 Fichier logo existe: {os.path.exists(org_loaded.logo_path) if org_loaded.logo_path else False}")
                
                # Vérifications finales
                assert org_loaded.nombre == organization_name, "Nom organisation perdu"
                assert org_loaded.logo_path == permanent_logo, "Chemin logo perdu"
                assert os.path.exists(org_loaded.logo_path), "Fichier logo perdu"
                
                # 5. Vérifier que le logo peut être chargé dans l'interface
                print(f"\n5️⃣ Simulation chargement logo dans interface")
                
                # Simuler load_logo_image()
                if org_loaded.logo_path and os.path.exists(org_loaded.logo_path):
                    # Tester ouverture de l'image
                    try:
                        with Image.open(org_loaded.logo_path) as img:
                            print(f"   🖼️  Image chargée: {img.size} pixels")
                            print(f"   🎨 Format: {img.format}")
                        logo_loadable = True
                    except Exception as e:
                        print(f"   ❌ Erreur chargement image: {e}")
                        logo_loadable = False
                else:
                    logo_loadable = False
                
                assert logo_loadable, "Logo non chargeable dans l'interface"
                
                print(f"\n🎉 Scénario réel de persistance réussi!")
                print(f"   ✅ Logo sélectionné et copié")
                print(f"   ✅ Organisation sauvegardée")
                print(f"   ✅ Données persistées après redémarrage")
                print(f"   ✅ Logo chargeable dans l'interface")
                
            finally:
                database.db = original_db


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
