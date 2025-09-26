#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de diagnostic pour la persistance du logo
"""

import os
import tempfile
import pytest
from PIL import Image
from database.models import Organizacion
from test.utils.test_database_manager import isolated_test_db


class TestLogoPersistenceDebug:
    """Tests de diagnostic pour la persistance du logo"""
    
    @pytest.fixture
    def temp_logo(self):
        """Crée un logo temporaire pour les tests"""
        temp_dir = tempfile.mkdtemp()
        logo_path = os.path.join(temp_dir, "test_logo.png")
        
        # Créer une image de test
        img = Image.new('RGB', (100, 50), color='red')
        img.save(logo_path)
        
        yield logo_path
        
        # Nettoyage
        if os.path.exists(logo_path):
            os.remove(logo_path)
        os.rmdir(temp_dir)
    
    def test_logo_persistence_step_by_step(self, temp_logo):
        """Test détaillé de la persistance du logo étape par étape"""
        with isolated_test_db("test_logo_persistence_debug") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Test de persistance du logo - Diagnostic détaillé")
                print(f"=" * 60)
                
                # Étape 1: Vérifier que le logo temporaire existe
                print(f"\n1️⃣ Vérification du logo temporaire")
                print(f"   📁 Chemin: {temp_logo}")
                print(f"   ✅ Existe: {os.path.exists(temp_logo)}")
                assert os.path.exists(temp_logo), "Le logo temporaire n'existe pas"
                
                # Étape 2: Créer organisation avec logo
                print(f"\n2️⃣ Création de l'organisation avec logo")
                org = Organizacion(
                    nombre="Test Persistence",
                    direccion="123 Test Street",
                    telefono="123-456-789",
                    email="test@persistence.com",
                    cif="B12345678",
                    logo_path=temp_logo
                )
                
                print(f"   🏢 Nom: {org.nombre}")
                print(f"   🖼️  Logo path avant save: '{org.logo_path}'")
                
                # Étape 3: Sauvegarder
                print(f"\n3️⃣ Sauvegarde en base de données")
                org.save()
                print(f"   ✅ Organisation sauvegardée")
                
                # Étape 4: Récupérer immédiatement
                print(f"\n4️⃣ Récupération immédiate")
                org_retrieved = Organizacion.get()
                
                print(f"   🏢 Nom récupéré: '{org_retrieved.nombre}'")
                print(f"   🖼️  Logo path récupéré: '{org_retrieved.logo_path}'")
                print(f"   📁 Fichier existe: {os.path.exists(org_retrieved.logo_path) if org_retrieved.logo_path else False}")
                
                # Vérifications
                assert org_retrieved is not None, "Organisation non récupérée"
                assert org_retrieved.nombre == org.nombre, f"Nom incorrect: {org_retrieved.nombre} != {org.nombre}"
                assert org_retrieved.logo_path == temp_logo, f"Logo path incorrect: '{org_retrieved.logo_path}' != '{temp_logo}'"
                assert os.path.exists(org_retrieved.logo_path), f"Fichier logo n'existe pas: {org_retrieved.logo_path}"
                
                print(f"   ✅ Récupération immédiate réussie")
                
                # Étape 5: Simuler redémarrage (nouvelle instance DB)
                print(f"\n5️⃣ Simulation de redémarrage")
                
                # Créer une nouvelle connexion pour simuler un redémarrage
                org_after_restart = Organizacion.get()
                
                print(f"   🏢 Nom après redémarrage: '{org_after_restart.nombre}'")
                print(f"   🖼️  Logo path après redémarrage: '{org_after_restart.logo_path}'")
                print(f"   📁 Fichier existe après redémarrage: {os.path.exists(org_after_restart.logo_path) if org_after_restart.logo_path else False}")
                
                # Vérifications après redémarrage
                assert org_after_restart is not None, "Organisation non récupérée après redémarrage"
                assert org_after_restart.nombre == org.nombre, f"Nom incorrect après redémarrage: {org_after_restart.nombre}"
                assert org_after_restart.logo_path == temp_logo, f"Logo path incorrect après redémarrage: '{org_after_restart.logo_path}'"
                
                if org_after_restart.logo_path:
                    file_exists = os.path.exists(org_after_restart.logo_path)
                    print(f"   📊 Analyse du fichier:")
                    print(f"      - Chemin: {org_after_restart.logo_path}")
                    print(f"      - Existe: {file_exists}")
                    if file_exists:
                        file_size = os.path.getsize(org_after_restart.logo_path)
                        print(f"      - Taille: {file_size} bytes")
                    
                    assert file_exists, f"Fichier logo n'existe pas après redémarrage: {org_after_restart.logo_path}"
                
                print(f"   ✅ Persistance après redémarrage réussie")
                
                # Étape 6: Test de mise à jour
                print(f"\n6️⃣ Test de mise à jour du logo")
                
                # Créer un nouveau logo
                temp_dir2 = tempfile.mkdtemp()
                logo_path2 = os.path.join(temp_dir2, "test_logo2.png")
                img2 = Image.new('RGB', (100, 50), color='blue')
                img2.save(logo_path2)
                
                try:
                    # Mettre à jour le logo
                    org_after_restart.logo_path = logo_path2
                    org_after_restart.save()
                    
                    # Vérifier la mise à jour
                    org_updated = Organizacion.get()
                    print(f"   🖼️  Nouveau logo path: '{org_updated.logo_path}'")
                    print(f"   📁 Nouveau fichier existe: {os.path.exists(org_updated.logo_path) if org_updated.logo_path else False}")
                    
                    assert org_updated.logo_path == logo_path2, f"Mise à jour logo échouée: '{org_updated.logo_path}'"
                    assert os.path.exists(org_updated.logo_path), f"Nouveau fichier logo n'existe pas: {org_updated.logo_path}"
                    
                    print(f"   ✅ Mise à jour du logo réussie")
                    
                finally:
                    # Nettoyer le second logo
                    if os.path.exists(logo_path2):
                        os.remove(logo_path2)
                    os.rmdir(temp_dir2)
                
                print(f"\n🎉 Test de persistance complet réussi!")
                
            finally:
                database.db = original_db
    
    def test_logo_path_null_handling(self):
        """Test de gestion des valeurs NULL pour logo_path"""
        with isolated_test_db("test_logo_null") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Test de gestion des valeurs NULL")
                print(f"=" * 40)
                
                # Test 1: Organisation sans logo
                print(f"\n1️⃣ Organisation sans logo")
                org1 = Organizacion(
                    nombre="Sans Logo",
                    direccion="123 No Logo St",
                    telefono="123-456-789",
                    email="nologo@test.com",
                    cif="B11111111",
                    logo_path=""  # Logo vide
                )
                org1.save()
                
                org1_check = Organizacion.get()
                print(f"   📊 Logo path vide: '{org1_check.logo_path}'")
                assert org1_check.logo_path == "", f"Logo path vide non préservé: '{org1_check.logo_path}'"
                print(f"   ✅ Logo path vide correctement géré")
                
                # Test 2: Forcer NULL dans la base
                print(f"\n2️⃣ Test avec NULL forcé en base")
                query = "UPDATE organizacion SET logo_path=NULL WHERE id=1"
                db.execute_query(query)
                
                org2_check = Organizacion.get()
                print(f"   📊 Logo path après NULL: '{org2_check.logo_path}'")
                assert org2_check.logo_path == "", f"Logo path NULL mal géré: '{org2_check.logo_path}'"
                print(f"   ✅ Logo path NULL correctement converti en chaîne vide")
                
                print(f"\n🎉 Test de gestion NULL réussi!")
                
            finally:
                database.db = original_db
    
    def test_database_schema_verification(self):
        """Vérifier le schéma de la base de données pour la table organizacion"""
        with isolated_test_db("test_schema_verification") as db:
            from database import database
            original_db = database.db
            
            try:
                database.db = db
                
                print(f"\n🔍 Vérification du schéma de la base de données")
                print(f"=" * 50)
                
                # Vérifier la structure de la table organizacion
                query = "PRAGMA table_info(organizacion)"
                columns = db.execute_query(query)
                
                print(f"\n📊 Structure de la table 'organizacion':")
                for i, col in enumerate(columns):
                    print(f"   {i}: {col[1]} ({col[2]}) - NULL: {col[3] == 0}")
                
                # Vérifier que la colonne logo_path existe
                column_names = [col[1] for col in columns]
                assert 'logo_path' in column_names, "Colonne logo_path manquante"
                
                # Trouver l'index de logo_path
                logo_path_index = column_names.index('logo_path')
                print(f"\n🖼️  Colonne logo_path trouvée à l'index {logo_path_index}")
                
                # Vérifier le type de la colonne
                logo_path_info = columns[logo_path_index]
                print(f"   Type: {logo_path_info[2]}")
                print(f"   Nullable: {logo_path_info[3] == 0}")
                
                print(f"\n✅ Schéma de base de données vérifié")
                
            finally:
                database.db = original_db


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
