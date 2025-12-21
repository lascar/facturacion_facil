#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe de base pour les tests avec fixtures standardisées
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.test_database import TestDatabase
from database.fixtures import TestFixtures

class BaseTestWithFixtures(unittest.TestCase):
    """Classe de base pour les tests avec fixtures standardisées"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration une seule fois pour toute la classe de test"""
        print(f"\n🔧 Configuration de la classe de test: {cls.__name__}")
        
        # Créer la base de données de test avec fixtures
        cls.test_db = TestDatabase(with_fixtures=True)
        cls.fixtures = cls.test_db.fixtures
        
        # Obtenir les IDs des fixtures créées
        cls.fixture_data = cls.fixtures.get_fixtures_summary()
        
        print(f"   ✅ Base de test créée avec {cls.fixture_data['products_count']} produits, "
              f"{cls.fixture_data['clients_count']} clients, {cls.fixture_data['invoices_count']} factures")
    
    def setUp(self):
        """Configuration avant chaque test - remet la base à l'état initial"""
        print(f"\n🔄 Remise à l'état initial pour: {self._testMethodName}")
        
        # Remettre la base à l'état initial des fixtures
        self.fixture_data = self.test_db.reset_to_fixtures()
        
        print(f"   ✅ État initial restauré")
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Pas besoin de nettoyer, setUp() remet déjà à l'état initial
        pass
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage final de la classe de test"""
        print(f"\n🧹 Nettoyage final de la classe: {cls.__name__}")
        if hasattr(cls, 'test_db'):
            cls.test_db.cleanup()
        print("   ✅ Nettoyage terminé")
    
    # Méthodes utilitaires pour accéder aux fixtures
    
    def get_test_products(self):
        """Retourne les produits de test"""
        return self.fixture_data['products']
    
    def get_test_clients(self):
        """Retourne les clients de test"""
        return self.fixture_data['clients']
    
    def get_test_invoices(self):
        """Retourne les factures de test"""
        return self.fixture_data['invoices']
    
    def get_first_product(self):
        """Retourne le premier produit de test"""
        products = self.get_test_products()
        return products[0] if products else None
    
    def get_first_client(self):
        """Retourne le premier client de test"""
        clients = self.get_test_clients()
        return clients[0] if clients else None
    
    def get_first_invoice(self):
        """Retourne la première facture de test"""
        invoices = self.get_test_invoices()
        return invoices[0] if invoices else None
    
    def assert_fixtures_loaded(self):
        """Vérifie que les fixtures sont bien chargées"""
        self.assertEqual(self.fixture_data['products_count'], 3, "Devrait avoir 3 produits")
        self.assertEqual(self.fixture_data['clients_count'], 3, "Devrait avoir 3 clients")
        self.assertEqual(self.fixture_data['invoices_count'], 3, "Devrait avoir 3 factures")
    
    def print_fixtures_summary(self):
        """Affiche un résumé des fixtures pour debug"""
        print("\n📊 RÉSUMÉ DES FIXTURES:")
        print(f"   Produits: {self.fixture_data['products_count']}")
        for i, product in enumerate(self.get_test_products()[:3]):
            print(f"     {i+1}. {product.get('nombre', 'N/A')} - Stock: {product.get('stock_actual', 0)}")
        
        print(f"   Clients: {self.fixture_data['clients_count']}")
        for i, client in enumerate(self.get_test_clients()[:3]):
            print(f"     {i+1}. {client.get('nombre', 'N/A')}")
        
        print(f"   Factures: {self.fixture_data['invoices_count']}")
        for i, invoice in enumerate(self.get_test_invoices()[:3]):
            print(f"     {i+1}. {invoice.get('numero_factura', 'N/A')} - État: {invoice.get('estado', 'N/A')}")


class QuickTest(BaseTestWithFixtures):
    """Test rapide pour vérifier que les fixtures fonctionnent"""
    
    def test_fixtures_are_loaded(self):
        """Test que les fixtures sont correctement chargées"""
        print("\n🧪 Test de chargement des fixtures")
        
        # Vérifier les fixtures
        self.assert_fixtures_loaded()
        
        # Afficher le résumé
        self.print_fixtures_summary()
        
        # Vérifier les données spécifiques
        products = self.get_test_products()
        self.assertIsNotNone(products)
        self.assertTrue(len(products) >= 3)

        # Vérifier qu'on a bien les produits attendus (peu importe l'ordre)
        product_names = [p['nombre'] for p in products]
        self.assertIn('Laptop Dell Inspiron', product_names)
        self.assertIn('Souris Logitech MX', product_names)
        self.assertIn('Clavier Mécanique RGB', product_names)

        first_client = self.get_first_client()
        self.assertIsNotNone(first_client)
        self.assertEqual(first_client['nombre'], 'Empresa Tech Solutions')
        
        print("   ✅ Toutes les fixtures sont correctement chargées")
    
    def test_reset_between_tests(self):
        """Test que la base est remise à l'état initial entre les tests"""
        print("\n🧪 Test de remise à l'état initial")
        
        # Vérifier que nous avons bien les données attendues
        products = self.get_test_products()
        self.assertEqual(len(products), 3, "Devrait avoir 3 produits après reset")

        # Vérifier qu'on a bien les stocks initiaux
        stocks = [p['stock_actual'] for p in products]
        expected_stocks = [25, 150, 75]  # Stocks initiaux selon les fixtures
        self.assertEqual(sorted(stocks), sorted(expected_stocks), "Les stocks devraient être remis aux valeurs initiales")

        print(f"   ✅ Stocks après reset: {sorted(stocks)}")
        print("   ✅ Test de reset validé (setUp() remet automatiquement à l'état initial)")


if __name__ == '__main__':
    # Lancer les tests rapides
    unittest.main(verbosity=2)
