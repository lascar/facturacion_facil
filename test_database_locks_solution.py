#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour valider la résolution des problèmes de verrouillage de base de données
"""

import sqlite3
import threading
import time
import tempfile
import os
from database.database_context_manager import DatabaseContextManager
from database.database_improved import DatabaseImproved

class DatabaseLockTester:
    """Testeur pour les problèmes de verrouillage de base de données"""
    
    def __init__(self):
        # Créer une base de données temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_locks.db")
        self.results = []
        self.errors = []
    
    def setup_test_database(self):
        """Crée une base de données de test"""
        db = DatabaseImproved(self.test_db_path)
        
        # Ajouter quelques données de test
        with db.get_transaction() as conn:
            cursor = conn.cursor()
            
            # Insérer des produits de test
            for i in range(10):
                cursor.execute("""
                    INSERT INTO productos (referencia, nombre, precio_unitario)
                    VALUES (?, ?, ?)
                """, (f"TEST-{i:03d}", f"Produit Test {i}", 10.0 + i))
            
            # Insérer des clients de test
            for i in range(5):
                cursor.execute("""
                    INSERT INTO clientes (nombre, dni_nie)
                    VALUES (?, ?)
                """, (f"Client Test {i}", f"12345678{i}"))
        
        print(f"✅ Base de données de test créée: {self.test_db_path}")
        return db
    
    def test_concurrent_reads(self, num_threads=5):
        """Test de lectures concurrentes"""
        print(f"🧪 Test de {num_threads} lectures concurrentes...")
        
        db = DatabaseContextManager(self.test_db_path)
        results = []
        errors = []
        
        def read_worker(worker_id):
            try:
                for i in range(10):
                    with db.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT COUNT(*) FROM productos")
                        count = cursor.fetchone()[0]
                        results.append(f"Worker {worker_id}: {count} produits")
                        time.sleep(0.01)  # Petite pause pour simuler du travail
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # Lancer les threads
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=read_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()
        
        execution_time = time.time() - start_time
        
        if errors:
            print(f"❌ Erreurs détectées: {len(errors)}")
            for error in errors[:3]:  # Afficher les 3 premières erreurs
                print(f"   {error}")
            return False
        else:
            print(f"✅ {len(results)} opérations réussies en {execution_time:.2f}s")
            return True
    
    def test_concurrent_writes(self, num_threads=3):
        """Test d'écritures concurrentes"""
        print(f"🧪 Test de {num_threads} écritures concurrentes...")
        
        db = DatabaseContextManager(self.test_db_path)
        results = []
        errors = []
        
        def write_worker(worker_id):
            try:
                for i in range(5):
                    with db.get_transaction() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO productos (referencia, nombre, precio_unitario)
                            VALUES (?, ?, ?)
                        """, (f"WRITE-{worker_id}-{i}", f"Produit Worker {worker_id}-{i}", 20.0))
                        results.append(f"Worker {worker_id}: Produit {i} créé")
                        time.sleep(0.02)  # Pause pour simuler du travail
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # Lancer les threads
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=write_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()
        
        execution_time = time.time() - start_time
        
        if errors:
            print(f"❌ Erreurs détectées: {len(errors)}")
            for error in errors[:3]:
                print(f"   {error}")
            return False
        else:
            print(f"✅ {len(results)} opérations réussies en {execution_time:.2f}s")
            return True
    
    def test_mixed_operations(self, num_threads=4):
        """Test d'opérations mixtes (lecture/écriture)"""
        print(f"🧪 Test de {num_threads} opérations mixtes...")
        
        db = DatabaseContextManager(self.test_db_path)
        results = []
        errors = []
        
        def mixed_worker(worker_id):
            try:
                for i in range(5):
                    if i % 2 == 0:
                        # Opération de lecture
                        with db.get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM productos")
                            count = cursor.fetchone()[0]
                            results.append(f"Worker {worker_id}: Lu {count} produits")
                    else:
                        # Opération d'écriture
                        with db.get_transaction() as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO clientes (nombre, dni_nie)
                                VALUES (?, ?)
                            """, (f"Client Mixed {worker_id}-{i}", f"MIX{worker_id}{i}"))
                            results.append(f"Worker {worker_id}: Client créé")
                    
                    time.sleep(0.01)
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # Lancer les threads
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=mixed_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()
        
        execution_time = time.time() - start_time
        
        if errors:
            print(f"❌ Erreurs détectées: {len(errors)}")
            for error in errors[:3]:
                print(f"   {error}")
            return False
        else:
            print(f"✅ {len(results)} opérations réussies en {execution_time:.2f}s")
            return True
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 TESTS DE RÉSOLUTION DES PROBLÈMES DE VERROUILLAGE")
        print("=" * 55)
        
        # Préparer la base de données
        self.setup_test_database()
        
        # Exécuter les tests
        tests = [
            ("Lectures concurrentes", self.test_concurrent_reads),
            ("Écritures concurrentes", self.test_concurrent_writes),
            ("Opérations mixtes", self.test_mixed_operations)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 30)
            
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}: RÉUSSI")
                else:
                    print(f"❌ {test_name}: ÉCHEC")
            except Exception as e:
                print(f"❌ {test_name}: ERREUR - {e}")
        
        # Résumé
        print(f"\n📊 RÉSUMÉ DES TESTS")
        print("=" * 20)
        print(f"✅ Tests réussis: {passed}/{total}")
        print(f"❌ Tests échoués: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 TOUS LES TESTS ONT RÉUSSI !")
            print("   Les problèmes de verrouillage sont résolus.")
            return True
        else:
            print(f"\n⚠️ {total - passed} test(s) ont échoué.")
            print("   Des problèmes de verrouillage persistent.")
            return False
    
    def cleanup(self):
        """Nettoie les fichiers de test"""
        try:
            if os.path.exists(self.test_db_path):
                os.remove(self.test_db_path)
            os.rmdir(self.temp_dir)
            print("🧹 Nettoyage des fichiers de test terminé")
        except Exception as e:
            print(f"⚠️ Erreur lors du nettoyage: {e}")

def main():
    """Fonction principale"""
    tester = DatabaseLockTester()
    
    try:
        success = tester.run_all_tests()
        return success
    finally:
        tester.cleanup()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
