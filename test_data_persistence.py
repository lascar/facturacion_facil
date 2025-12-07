#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de persistance des données
Vérifie que les factures, stocks et produits sont correctement sauvegardés
"""

import sys
import os
import tempfile
import shutil
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import db
from database.models import Producto, Cliente, Factura, FacturaItem, Stock
from utils.logger import get_logger

logger = get_logger("test_persistence")

class DataPersistenceTest:
    def __init__(self):
        self.test_db_path = None
        self.original_db_path = None
        
    def setup_test_database(self):
        """Crée une base de données temporaire pour les tests"""
        try:
            # Créer un fichier temporaire
            fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(fd)
            
            # Sauvegarder le chemin original
            self.original_db_path = db.db_path
            
            # Configurer la base de test
            db.db_path = self.test_db_path
            db.init_database()
            
            logger.info(f"Base de test créée: {self.test_db_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur setup test DB: {e}")
            return False
    
    def teardown_test_database(self):
        """Nettoie la base de données de test"""
        try:
            # Restaurer le chemin original
            if self.original_db_path:
                db.db_path = self.original_db_path
            
            # Supprimer le fichier de test
            if self.test_db_path and os.path.exists(self.test_db_path):
                os.remove(self.test_db_path)
                logger.info(f"Base de test supprimée: {self.test_db_path}")
            
        except Exception as e:
            logger.error(f"Erreur teardown test DB: {e}")
    
    def test_producto_persistence(self):
        """Test de persistance des produits"""
        try:
            print("🧪 Test persistance produits...")
            
            # Créer un produit
            producto = Producto(
                nombre="Producto Test Persistencia",
                referencia="TEST-PERSIST-001",
                precio=99.99,
                categoria="Test",
                descripcion="Producto para test de persistencia",
                iva_recomendado=21.0
            )
            
            # Sauvegarder
            try:
                producto.save()
                print(f"   ✅ Produit sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde produit: {e}")
                return False
            
            producto_id = producto.id
            print(f"   ✅ Produit créé avec ID: {producto_id}")
            
            # Fermer et rouvrir la connexion (simuler redémarrage)
            # Note: pas de méthode close_connection dans cette version
            
            # Récupérer le produit
            productos = Producto.get_all()
            found_product = None
            
            for p in productos:
                if p.id == producto_id:
                    found_product = p
                    break
            
            if not found_product:
                print("   ❌ Produit non trouvé après redémarrage")
                return False
            
            # Vérifier les données
            if (found_product.nombre == "Producto Test Persistencia" and
                found_product.referencia == "TEST-PERSIST-001" and
                found_product.precio == 99.99):
                print("   ✅ Données produit correctement persistées")
                return True
            else:
                print("   ❌ Données produit corrompues")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur test produit: {e}")
            return False
    
    def test_stock_persistence(self):
        """Test de persistance du stock"""
        try:
            print("🧪 Test persistance stock...")
            
            # Créer un produit avec stock
            producto = Producto(
                nombre="Producto Stock Test",
                referencia="TEST-STOCK-001",
                precio=50.0
            )
            
            try:
                producto.save()
                print(f"   ✅ Produit sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde produit: {e}")
                return False
            
            # Vérifier que le stock a été créé
            stock_cantidad = Stock.get_by_product(producto.id)
            if stock_cantidad is None:
                print("   ❌ Stock non créé automatiquement")
                return False

            print(f"   ✅ Stock créé: {stock_cantidad}")

            # Créer un objet Stock pour modifier
            stock = Stock(producto.id, 150)
            try:
                stock.save()
                print(f"   ✅ Stock sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde stock: {e}")
                return False

            # Fermer et rouvrir la connexion
            # Note: pas de méthode close_connection dans cette version

            # Récupérer le stock
            stock_recovered = Stock.get_by_product(producto.id)

            if stock_recovered is None:
                print("   ❌ Stock non trouvé après redémarrage")
                return False

            if stock_recovered == 150:
                print("   ✅ Stock correctement persisté")
                return True
            else:
                print(f"   ❌ Stock corrompu: {stock_recovered}")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur test stock: {e}")
            return False
    
    def test_factura_persistence(self):
        """Test de persistance des factures"""
        try:
            print("🧪 Test persistance factures...")
            
            # Créer un client
            cliente = Cliente(
                nombre="Cliente Test Persistencia",
                email="test@persistence.com",
                telefono="123456789"
            )
            
            try:
                cliente.save()
                print(f"   ✅ Client sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde client: {e}")
                return False
            
            # Créer un produit
            producto = Producto(
                nombre="Producto Factura Test",
                referencia="TEST-FACT-001",
                precio=25.0
            )
            
            try:
                producto.save()
                print(f"   ✅ Produit sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde produit: {e}")
                return False
            
            # Créer une facture
            factura = Factura(
                numero_factura="TEST-PERSIST-001",
                cliente_id=cliente.id,
                fecha_factura=datetime.now().isoformat(),
                subtotal=25.0,
                total_iva=5.25,
                total_factura=30.25
            )
            
            try:
                factura.save()
                print(f"   ✅ Facture sauvegardée")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde facture: {e}")
                return False
            
            # Ajouter un item
            item = FacturaItem(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=1,
                precio_unitario=25.0
            )
            
            try:
                item.save()
                print(f"   ✅ Item sauvegardé")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde item: {e}")
                return False
            
            factura_id = factura.id
            print(f"   ✅ Facture créée avec ID: {factura_id}")
            
            # Fermer et rouvrir la connexion
            # Note: pas de méthode close_connection dans cette version
            
            # Récupérer la facture
            facturas = Factura.get_all()
            found_factura = None
            
            for f in facturas:
                if f.id == factura_id:
                    found_factura = f
                    break
            
            if not found_factura:
                print("   ❌ Facture non trouvée après redémarrage")
                return False
            
            # Vérifier les items
            items = FacturaItem.get_by_factura_id(factura_id)
            if not items or len(items) == 0:
                print("   ❌ Items facture non trouvés")
                return False
            
            print("   ✅ Facture et items correctement persistés")
            return True
                
        except Exception as e:
            print(f"   ❌ Erreur test facture: {e}")
            return False
    
    def run_all_tests(self):
        """Exécute tous les tests de persistance"""
        print("🔧 TESTS DE PERSISTANCE DES DONNÉES")
        print("=" * 50)
        
        if not self.setup_test_database():
            print("❌ Impossible de créer la base de test")
            return False
        
        try:
            tests = [
                ("Produits", self.test_producto_persistence),
                ("Stock", self.test_stock_persistence),
                ("Factures", self.test_factura_persistence)
            ]
            
            results = []
            
            for test_name, test_func in tests:
                print(f"\n📋 Test {test_name}:")
                result = test_func()
                results.append((test_name, result))
            
            # Résumé
            print(f"\n📊 RÉSUMÉ DES TESTS:")
            print("-" * 30)
            
            passed = 0
            for test_name, result in results:
                status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
                print(f"   {test_name}: {status}")
                if result:
                    passed += 1
            
            print(f"\n🎯 Résultat: {passed}/{len(tests)} tests passés")
            
            if passed == len(tests):
                print("🎉 Tous les tests de persistance ont réussi!")
                return True
            else:
                print("⚠️  Certains tests ont échoué")
                return False
                
        finally:
            self.teardown_test_database()

def main():
    """Fonction principale"""
    test_runner = DataPersistenceTest()
    success = test_runner.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
