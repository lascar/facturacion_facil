#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour les stocks négatifs
Vérifie que les stocks négatifs sont permis après correction du problème
"Stock disponible para edición: 0, Cantidad solicitada: 80"
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.models import Stock, db


class TestStocksNegatifsRegression(unittest.TestCase):
    """Tests de régression pour les stocks négatifs"""

    def setUp(self):
        """Setup pour chaque test"""
        # Setup : créer un produit de test
        self.test_producto_id = None

        # Créer un produit de test
        query_producto = """INSERT INTO productos (nombre, precio, referencia)
                           VALUES (?, ?, ?)"""
        db.execute_query(query_producto, ("TEST_STOCK_NEGATIF_REGRESSION", 10.0, "TESTREGR001"))

        # Obtenir l'ID du produit créé
        query_get_id = "SELECT id FROM productos WHERE referencia = 'TESTREGR001'"
        result = db.execute_query(query_get_id)
        if result:
            self.test_producto_id = result[0][0]

            # Créer une entrée de stock
            query_stock = "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)"
            db.execute_query(query_stock, (self.test_producto_id, 10))

    def tearDown(self):
        """Cleanup après chaque test"""
        # Cleanup : supprimer le produit de test
        if self.test_producto_id:
            db.execute_query("DELETE FROM stock WHERE producto_id = ?", (self.test_producto_id,))
            db.execute_query("DELETE FROM productos WHERE id = ?", (self.test_producto_id,))
    
    def test_stock_negatif_permis_base_donnees(self):
        """Test que la base de données permet les stocks négatifs"""
        if not self.test_producto_id:
            self.skipTest("Impossible de créer le produit de test")
        
        # Obtenir le stock initial
        stock_initial = Stock.get_by_product(self.test_producto_id)
        self.assertEqual(stock_initial, 10, f"Stock initial attendu: 10, obtenu: {stock_initial}")
        
        # Simuler une vente qui dépasse le stock
        cantidad_venta = 60  # Dépasser le stock de 50
        
        # Mettre à jour le stock
        Stock.update_stock(self.test_producto_id, cantidad_venta)
        
        # Vérifier le nouveau stock
        stock_final = Stock.get_by_product(self.test_producto_id)
        stock_attendu = stock_initial - cantidad_venta  # 10 - 60 = -50
        
        self.assertEqual(stock_final, stock_attendu, f"Stock final attendu: {stock_attendu}, obtenu: {stock_final}")
        self.assertLess(stock_final, 0, f"Le stock devrait être négatif, obtenu: {stock_final}")
        self.assertEqual(stock_final, -50, f"Stock final attendu: -50, obtenu: {stock_final}")
    
    def test_stock_negatif_multiple_operations(self):
        """Test des stocks négatifs avec plusieurs opérations"""
        if not self.test_producto_id:
            self.skipTest("Impossible de créer le produit de test")
        
        # Opération 1: Vente normale
        Stock.update_stock(self.test_producto_id, 5)
        stock_apres_vente1 = Stock.get_by_product(self.test_producto_id)
        assert stock_apres_vente1 == 5, f"Après vente 1, stock attendu: 5, obtenu: {stock_apres_vente1}"
        
        # Opération 2: Vente qui rend le stock négatif
        Stock.update_stock(self.test_producto_id, 20)
        stock_apres_vente2 = Stock.get_by_product(self.test_producto_id)
        assert stock_apres_vente2 == -15, f"Après vente 2, stock attendu: -15, obtenu: {stock_apres_vente2}"
        
        # Opération 3: Vente supplémentaire sur stock déjà négatif
        Stock.update_stock(self.test_producto_id, 10)
        stock_apres_vente3 = Stock.get_by_product(self.test_producto_id)
        assert stock_apres_vente3 == -25, f"Après vente 3, stock attendu: -25, obtenu: {stock_apres_vente3}"
        
        # Opération 4: Réapprovisionnement
        Stock.update_stock(self.test_producto_id, -30)  # Ajout de stock (quantité négative)
        stock_apres_reappro = Stock.get_by_product(self.test_producto_id)
        assert stock_apres_reappro == 5, f"Après réappro, stock attendu: 5, obtenu: {stock_apres_reappro}"
    
    def test_stock_negatif_zero_boundary(self):
        """Test du comportement aux limites (passage par zéro)"""
        if not self.test_producto_id:
            pytest.skip("Impossible de créer le produit de test")
        
        # Vendre exactement le stock disponible
        Stock.update_stock(self.test_producto_id, 10)
        stock_zero = Stock.get_by_product(self.test_producto_id)
        assert stock_zero == 0, f"Stock à zéro attendu: 0, obtenu: {stock_zero}"
        
        # Vendre une unité de plus pour passer en négatif
        Stock.update_stock(self.test_producto_id, 1)
        stock_negatif = Stock.get_by_product(self.test_producto_id)
        assert stock_negatif == -1, f"Stock négatif attendu: -1, obtenu: {stock_negatif}"
    
    def test_stock_negatif_grandes_quantites(self):
        """Test avec de grandes quantités négatives"""
        if not self.test_producto_id:
            pytest.skip("Impossible de créer le produit de test")
        
        # Vente très importante
        cantidad_muy_grande = 1000
        Stock.update_stock(self.test_producto_id, cantidad_muy_grande)
        
        stock_final = Stock.get_by_product(self.test_producto_id)
        stock_attendu = 10 - cantidad_muy_grande  # -990
        
        assert stock_final == stock_attendu, f"Stock final attendu: {stock_attendu}, obtenu: {stock_final}"
        assert stock_final == -990, f"Stock final attendu: -990, obtenu: {stock_final}"


def test_regression_stocks_negatifs_integration():
    """Test d'intégration pour vérifier que la correction fonctionne"""
    # Ce test vérifie que le problème original est résolu
    # "Stock disponible para edición: 0, Cantidad solicitada: 80"
    
    # Créer un produit temporaire
    query_producto = """INSERT INTO productos (nombre, precio, referencia) 
                       VALUES (?, ?, ?)"""
    db.execute_query(query_producto, ("INTEGRATION_TEST", 15.0, "INTTEST001"))
    
    try:
        # Obtenir l'ID du produit
        query_get_id = "SELECT id FROM productos WHERE referencia = 'INTTEST001'"
        result = db.execute_query(query_get_id)
        assert result, "Produit de test non créé"
        
        producto_id = result[0][0]
        
        # Créer stock initial de 0 (reproduire le problème original)
        query_stock = "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)"
        db.execute_query(query_stock, (producto_id, 0))
        
        # Vérifier stock initial
        stock_initial = Stock.get_by_product(producto_id)
        assert stock_initial == 0, f"Stock initial attendu: 0, obtenu: {stock_initial}"
        
        # Simuler la situation problématique: "Cantidad solicitada: 80"
        cantidad_solicitada = 80
        Stock.update_stock(producto_id, cantidad_solicitada)
        
        # Vérifier que le stock est maintenant négatif (correction appliquée)
        stock_final = Stock.get_by_product(producto_id)
        assert stock_final == -80, f"Stock final attendu: -80, obtenu: {stock_final}"
        
        # Vérifier que le stock négatif est bien persisté
        stock_verification = Stock.get_by_product(producto_id)
        assert stock_verification == -80, f"Stock persisté attendu: -80, obtenu: {stock_verification}"
        
    finally:
        # Cleanup
        db.execute_query("DELETE FROM stock WHERE producto_id = ?", (producto_id,))
        db.execute_query("DELETE FROM productos WHERE id = ?", (producto_id,))


if __name__ == "__main__":
    # Permettre l'exécution directe du test
    pytest.main([__file__, "-v"])
