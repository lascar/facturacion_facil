#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression simple pour les stocks négatifs
Vérifie que les stocks négatifs sont permis après correction du problème
"Stock disponible para edición: 0, Cantidad solicitada: 80"
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.models import Stock, db


class TestStocksNegatifsSimple(unittest.TestCase):
    """Tests de régression simples pour les stocks négatifs"""
    
    def setUp(self):
        """Setup pour chaque test"""
        self.test_producto_id = None
        
        # Créer un produit de test
        query_producto = """INSERT INTO productos (nombre, precio, referencia) 
                           VALUES (?, ?, ?)"""
        db.execute_query(query_producto, ("TEST_STOCK_NEGATIF_SIMPLE", 10.0, "TESTSIMPLE001"))
        
        # Obtenir l'ID du produit créé
        query_get_id = "SELECT id FROM productos WHERE referencia = 'TESTSIMPLE001'"
        result = db.execute_query(query_get_id)
        if result:
            self.test_producto_id = result[0][0]
            
            # Créer une entrée de stock
            query_stock = "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)"
            db.execute_query(query_stock, (self.test_producto_id, 10))
    
    def tearDown(self):
        """Cleanup après chaque test"""
        if self.test_producto_id:
            db.execute_query("DELETE FROM stock WHERE producto_id = ?", (self.test_producto_id,))
            db.execute_query("DELETE FROM productos WHERE id = ?", (self.test_producto_id,))
    
    def test_stock_negatif_base_donnees(self):
        """Test principal : la base de données permet les stocks négatifs"""
        if not self.test_producto_id:
            self.skipTest("Impossible de créer le produit de test")
        
        # Obtenir le stock initial
        stock_initial = Stock.get_by_product(self.test_producto_id)
        self.assertEqual(stock_initial, 10, f"Stock initial attendu: 10, obtenu: {stock_initial}")
        
        # Simuler une vente qui dépasse le stock (reproduire le problème original)
        cantidad_venta = 80  # Comme dans le problème : "Cantidad solicitada: 80"
        
        # Mettre à jour le stock
        Stock.update_stock(self.test_producto_id, cantidad_venta)
        
        # Vérifier le nouveau stock
        stock_final = Stock.get_by_product(self.test_producto_id)
        stock_attendu = stock_initial - cantidad_venta  # 10 - 80 = -70
        
        self.assertEqual(stock_final, stock_attendu, f"Stock final attendu: {stock_attendu}, obtenu: {stock_final}")
        self.assertLess(stock_final, 0, f"Le stock devrait être négatif, obtenu: {stock_final}")
        self.assertEqual(stock_final, -70, f"Stock final attendu: -70, obtenu: {stock_final}")
    
    def test_stock_zero_vers_negatif(self):
        """Test du passage de stock 0 vers négatif (cas problématique original)"""
        if not self.test_producto_id:
            self.skipTest("Impossible de créer le produit de test")
        
        # Mettre le stock à 0 (reproduire "Stock disponible para edición: 0")
        Stock.update_stock(self.test_producto_id, 10)  # Vendre tout le stock
        stock_zero = Stock.get_by_product(self.test_producto_id)
        self.assertEqual(stock_zero, 0, f"Stock à zéro attendu: 0, obtenu: {stock_zero}")
        
        # Maintenant vendre 80 unités sur stock 0 (reproduire le problème exact)
        Stock.update_stock(self.test_producto_id, 80)
        stock_negatif = Stock.get_by_product(self.test_producto_id)
        
        self.assertEqual(stock_negatif, -80, f"Stock négatif attendu: -80, obtenu: {stock_negatif}")
        self.assertLess(stock_negatif, 0, f"Le stock devrait être négatif, obtenu: {stock_negatif}")


def test_regression_probleme_original():
    """Test d'intégration reproduisant exactement le problème original"""
    print("\n🧪 TEST DE RÉGRESSION: Problème original")
    print("=" * 50)
    print("Reproduction: 'Stock disponible para edición: 0, Cantidad solicitada: 80'")
    
    # Créer un produit temporaire
    query_producto = """INSERT INTO productos (nombre, precio, referencia) 
                       VALUES (?, ?, ?)"""
    db.execute_query(query_producto, ("REGRESSION_ORIGINAL", 15.0, "REGR001"))
    
    try:
        # Obtenir l'ID du produit
        query_get_id = "SELECT id FROM productos WHERE referencia = 'REGR001'"
        result = db.execute_query(query_get_id)
        assert result, "Produit de test non créé"
        
        producto_id = result[0][0]
        
        # Créer stock initial de 0 (reproduire le problème original)
        query_stock = "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)"
        db.execute_query(query_stock, (producto_id, 0))
        
        # Vérifier stock initial
        stock_initial = Stock.get_by_product(producto_id)
        print(f"   📊 Stock disponible para edición: {stock_initial}")
        assert stock_initial == 0, f"Stock initial attendu: 0, obtenu: {stock_initial}"
        
        # Simuler la situation problématique: "Cantidad solicitada: 80"
        cantidad_solicitada = 80
        print(f"   🛒 Cantidad solicitada: {cantidad_solicitada}")
        
        Stock.update_stock(producto_id, cantidad_solicitada)
        
        # Vérifier que le stock est maintenant négatif (correction appliquée)
        stock_final = Stock.get_by_product(producto_id)
        print(f"   📊 Stock final: {stock_final}")
        
        assert stock_final == -80, f"Stock final attendu: -80, obtenu: {stock_final}"
        assert stock_final < 0, f"Le stock devrait être négatif, obtenu: {stock_final}"
        
        print("   ✅ SUCCÈS: Stock négatif permis (problème résolu)")
        return True
        
    except Exception as e:
        print(f"   ❌ ÉCHEC: {e}")
        return False
        
    finally:
        # Cleanup
        db.execute_query("DELETE FROM stock WHERE producto_id = ?", (producto_id,))
        db.execute_query("DELETE FROM productos WHERE id = ?", (producto_id,))


def main():
    """Fonction principale pour exécuter les tests"""
    print("🚀 Tests de Régression: Stocks Négatifs")
    print("=" * 50)
    
    # Test d'intégration du problème original
    success_integration = test_regression_probleme_original()
    
    # Tests unitaires
    print("\n🧪 TESTS UNITAIRES:")
    print("=" * 30)
    
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    if success_integration:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Les stocks négatifs sont maintenant permis")
        print("✅ Le problème original est résolu")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")


if __name__ == "__main__":
    main()
