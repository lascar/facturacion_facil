#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test d'intégration complet pour la mise à jour du stock lors de la facturation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem, StockMovement
from ui.facturas_methods import FacturasMethodsMixin
from utils.logger import get_logger

class MockWindow:
    """Mock window pour les tests"""
    def __init__(self):
        pass

class TestableFacturasMethodsMixin(FacturasMethodsMixin):
    """Version testable du mixin"""
    
    def __init__(self):
        self.logger = get_logger("test_integration")
        self.current_factura = None
        self.factura_items = []
        self.window = MockWindow()
        self.dialog_response = True  # Par défaut, confirmer
    
    def _show_message(self, msg_type, title, message):
        """Mock pour les messages"""
        if msg_type == "yesno":
            return self.dialog_response
        return None
    
    def show_stock_confirmation_dialog_direct(self, title, message):
        """Mock pour le dialogue direct"""
        return self.dialog_response
    
    def show_simple_confirmation_dialog(self, message):
        """Mock pour le dialogue simple"""
        return self.dialog_response

class StockUpdateIntegrationTest(unittest.TestCase):
    """Tests d'intégration pour la mise à jour du stock"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        db.init_database()
        self.test_instance = TestableFacturasMethodsMixin()

        # Utiliser un produit existant ou créer un produit unique
        import time
        import random
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)

        # Créer un produit de test avec référence unique
        self.producto_test = Producto(
            nombre=f"Producto Integration Test {timestamp}",
            referencia=f"INT-TEST-{timestamp}-{random_id}",
            precio=25.99,
            categoria="Integration",
            iva_recomendado=21.0
        )

        try:
            self.producto_test.save()
        except Exception as e:
            # Si le produit existe déjà, utiliser un produit existant
            productos = Producto.get_all()
            if productos:
                self.producto_test = productos[0]
            else:
                raise e
        
        # Stock initial
        self.stock_inicial = 10
        self.stock_obj = Stock(self.producto_test.id, self.stock_inicial)
        self.stock_obj.save()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        try:
            if hasattr(self, 'factura_test') and hasattr(self.factura_test, 'id') and self.factura_test.id:
                self.factura_test.delete()
        except:
            pass

        try:
            if hasattr(self, 'producto_test') and hasattr(self.producto_test, 'id') and self.producto_test.id:
                # Ne supprimer que si c'est un produit de test créé par nous
                if "INT-TEST-" in self.producto_test.referencia:
                    self.producto_test.delete()
        except:
            pass
    
    def create_test_factura(self, cantidad_venta=3):
        """Crée une factura de test"""
        import time
        timestamp = int(time.time())
        self.factura_test = Factura(
            numero_factura=f"INT-TEST-{timestamp}",
            nombre_cliente="Cliente Integration Test",
            fecha_factura="2024-09-27"
        )
        
        item_test = FacturaItem(
            producto_id=self.producto_test.id,
            cantidad=cantidad_venta,
            precio_unitario=self.producto_test.precio,
            iva_aplicado=21.0
        )
        item_test.calculate_totals()
        
        self.test_instance.current_factura = self.factura_test
        self.test_instance.factura_items = [item_test]
        
        self.factura_test.items = [item_test]
        self.factura_test.calculate_totals()
        
        return cantidad_venta
    
    def test_stock_update_with_confirmation(self):
        """Test: Mise à jour du stock avec confirmation utilisateur"""
        cantidad_venta = self.create_test_factura(3)
        
        # Configurer pour confirmer
        self.test_instance.dialog_response = True
        
        # Exécuter le processus complet
        result = self.test_instance.show_stock_impact_summary()
        self.assertTrue(result, "L'utilisateur devrait confirmer")
        
        # Simuler la sauvegarde et mise à jour du stock
        self.factura_test.save()
        self.test_instance.update_stock_after_save()
        
        # Vérifier que le stock a été mis à jour
        stock_final = Stock.get_by_product(self.producto_test.id)
        stock_esperado = self.stock_inicial - cantidad_venta
        
        self.assertEqual(stock_final, stock_esperado,
                        f"Stock devrait être {stock_esperado}, mais est {stock_final}")
        
        # Vérifier qu'un mouvement de stock a été enregistré
        movimientos = StockMovement.get_by_product(self.producto_test.id, limit=1)
        self.assertGreater(len(movimientos), 0, "Un mouvement de stock devrait être enregistré")
        
        mouvement = movimientos[0]
        self.assertEqual(mouvement.tipo, "VENTA", "Le type de mouvement devrait être VENTA")
        self.assertEqual(mouvement.cantidad, -cantidad_venta, "La quantité du mouvement devrait être négative pour une vente")
    
    def test_stock_update_with_cancellation(self):
        """Test: Annulation par l'utilisateur - stock non mis à jour"""
        cantidad_venta = self.create_test_factura(3)
        
        # Configurer pour annuler
        self.test_instance.dialog_response = False
        
        # Exécuter le processus
        result = self.test_instance.show_stock_impact_summary()
        self.assertFalse(result, "L'utilisateur devrait annuler")
        
        # Le stock ne devrait pas changer
        stock_final = Stock.get_by_product(self.producto_test.id)
        self.assertEqual(stock_final, self.stock_inicial,
                        f"Stock devrait rester {self.stock_inicial}, mais est {stock_final}")
    
    def test_stock_update_low_stock_warning(self):
        """Test: Avertissement pour stock bas"""
        # Réduire le stock à un niveau bas
        Stock.update_stock(self.producto_test.id, 7)  # Laisse 3 unités
        
        cantidad_venta = self.create_test_factura(1)
        
        # Configurer pour confirmer
        self.test_instance.dialog_response = True
        
        # Vérifier que la validation détecte le stock bas
        errors = self.test_instance.validate_stock_availability()
        self.assertEqual(len(errors), 0, "Ne devrait pas y avoir d'erreurs pour stock bas mais suffisant")
        
        # Le dialogue devrait apparaître pour stock bas
        result = self.test_instance.show_stock_impact_summary()
        self.assertTrue(result, "Le dialogue devrait apparaître et être confirmé")
    
    def test_stock_update_insufficient_stock(self):
        """Test: Stock insuffisant - vente non autorisée"""
        cantidad_venta = self.create_test_factura(15)  # Plus que le stock disponible
        
        # Vérifier que la validation détecte le stock insuffisant
        errors = self.test_instance.validate_stock_availability()
        self.assertGreater(len(errors), 0, "Devrait y avoir des erreurs pour stock insuffisant")
        
        # Vérifier le message d'erreur
        error_message = errors[0]
        self.assertIn("stock insuficiente", error_message.lower())
    
    def test_multiple_products_stock_update(self):
        """Test: Mise à jour du stock pour plusieurs produits"""
        # Créer un deuxième produit
        producto2 = Producto(
            nombre="Producto Integration Test 2",
            referencia="INT-TEST-002",
            precio=15.50,
            categoria="Integration"
        )
        producto2.save()
        
        stock2_inicial = 8
        stock2_obj = Stock(producto2.id, stock2_inicial)
        stock2_obj.save()
        
        try:
            # Créer factura avec deux produits
            self.factura_test = Factura(
                numero_factura="INT-TEST-MULTI",
                nombre_cliente="Cliente Multi Test",
                fecha_factura="2024-09-27"
            )
            
            # Premier item
            item1 = FacturaItem(
                producto_id=self.producto_test.id,
                cantidad=2,
                precio_unitario=self.producto_test.precio,
                iva_aplicado=21.0
            )
            item1.calculate_totals()
            
            # Deuxième item
            item2 = FacturaItem(
                producto_id=producto2.id,
                cantidad=3,
                precio_unitario=producto2.precio,
                iva_aplicado=21.0
            )
            item2.calculate_totals()
            
            self.test_instance.current_factura = self.factura_test
            self.test_instance.factura_items = [item1, item2]
            
            self.factura_test.items = [item1, item2]
            self.factura_test.calculate_totals()
            
            # Configurer pour confirmer
            self.test_instance.dialog_response = True
            
            # Exécuter le processus
            result = self.test_instance.show_stock_impact_summary()
            self.assertTrue(result)
            
            # Simuler sauvegarde et mise à jour
            self.factura_test.save()
            self.test_instance.update_stock_after_save()
            
            # Vérifier les deux stocks
            stock1_final = Stock.get_by_product(self.producto_test.id)
            stock2_final = Stock.get_by_product(producto2.id)
            
            self.assertEqual(stock1_final, self.stock_inicial - 2)
            self.assertEqual(stock2_final, stock2_inicial - 3)
            
        finally:
            # Nettoyer le deuxième produit
            try:
                producto2.delete()
            except:
                pass
    
    def test_dialog_fallback_system(self):
        """Test: Système de fallback des dialogues"""
        cantidad_venta = self.create_test_factura(2)
        
        # Test que les différentes méthodes de dialogue retournent des résultats cohérents
        
        # Test dialogue direct (mock)
        result1 = self.test_instance.show_stock_confirmation_dialog_direct(
            "Test", "Message de test"
        )
        self.assertEqual(result1, self.test_instance.dialog_response)
        
        # Test dialogue simple (mock)
        result2 = self.test_instance.show_simple_confirmation_dialog("Message de test")
        self.assertEqual(result2, self.test_instance.dialog_response)
        
        # Test flux complet
        result3 = self.test_instance.show_stock_impact_summary()
        self.assertEqual(result3, self.test_instance.dialog_response)

def run_integration_tests():
    """Exécute tous les tests d'intégration"""
    
    print("🧪 TESTS D'INTÉGRATION - Mise à jour du stock")
    print("=" * 60)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(StockUpdateIntegrationTest)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION:")
    print(f"   Tests exécutés: {result.testsRun}")
    print(f"   Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Échecs: {len(result.failures)}")
    print(f"   Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TOUS LES TESTS D'INTÉGRATION RÉUSSIS")
        print("🎉 La solution de mise à jour du stock fonctionne parfaitement")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifier les erreurs ci-dessus")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
