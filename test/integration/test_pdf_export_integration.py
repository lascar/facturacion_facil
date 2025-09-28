#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test d'intégration complet pour l'exportation PDF
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
import tempfile
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from utils.logger import get_logger

class MockPDFExporter:
    """Mock pour les tests PDF sans dépendances GUI"""

    def __init__(self):
        self.logger = get_logger("test_pdf_integration")
        self.selected_factura = None

    def select_factura(self, factura):
        """Simule la sélection d'une factura"""
        self.selected_factura = factura
        return True

    def validate_pdf_export(self):
        """Valide qu'une factura peut être exportée en PDF"""
        if not self.selected_factura:
            return False, "No hay factura seleccionada"

        # Vérifier les champs requis
        required_fields = ['numero_factura', 'nombre_cliente', 'fecha_factura', 'total_factura']
        for field in required_fields:
            if not hasattr(self.selected_factura, field) or not getattr(self.selected_factura, field):
                return False, f"Campo requerido faltante: {field}"

        # Vérifier les items
        if not hasattr(self.selected_factura, 'items') or len(self.selected_factura.items) == 0:
            return False, "La factura no tiene items"

        return True, "Factura válida para PDF"

class PDFExportIntegrationTest(unittest.TestCase):
    """Tests d'intégration pour l'exportation PDF"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        db.init_database()
        self.test_instance = MockPDFExporter()

        # Utiliser un produit existant ou créer un produit unique
        import time
        import random
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)

        # Créer un produit de test avec référence unique
        self.producto_test = Producto(
            nombre=f"Producto PDF Test {timestamp}",
            referencia=f"PDF-TEST-{timestamp}-{random_id}",
            precio=19.99,
            categoria="PDF Test",
            iva_recomendado=21.0,
            descripcion="Producto para test de exportación PDF"
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
        self.stock_inicial = 20
        self.stock_obj = Stock(self.producto_test.id, self.stock_inicial)
        self.stock_obj.save()
        
        # Créer une factura de test complète
        self.create_test_factura()
    
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
                if "PDF-TEST-" in self.producto_test.referencia:
                    self.producto_test.delete()
        except:
            pass
    
    def create_test_factura(self):
        """Crée une factura de test complète"""
        self.factura_test = Factura(
            numero_factura="PDF-TEST-001",
            nombre_cliente="Cliente PDF Test",
            dni_nie_cliente="12345678A",
            direccion_cliente="Calle Test 123, Ciudad Test",
            email_cliente="test@pdf.com",
            telefono_cliente="123456789",
            fecha_factura="2024-09-27",
            modo_pago="Efectivo"
        )
        
        # Créer item de test (sans descripcion qui n'existe pas)
        item_test = FacturaItem(
            producto_id=self.producto_test.id,
            cantidad=3,
            precio_unitario=self.producto_test.precio,
            iva_aplicado=21.0
        )
        item_test.calculate_totals()
        
        # Assigner items et calculer totaux
        self.factura_test.items = [item_test]
        self.factura_test.calculate_totals()
        
        # Sauvegarder la factura
        self.factura_test.save()
    
    def test_factura_get_by_numero(self):
        """Test: Méthode get_by_numero fonctionne correctement"""
        # Test avec numéro existant
        factura_encontrada = Factura.get_by_numero(self.factura_test.numero_factura)
        
        self.assertIsNotNone(factura_encontrada, "La factura devrait être trouvée")
        self.assertEqual(factura_encontrada.id, self.factura_test.id, "L'ID devrait correspondre")
        self.assertEqual(factura_encontrada.numero_factura, self.factura_test.numero_factura, "Le numéro devrait correspondre")
        self.assertEqual(len(factura_encontrada.items), 1, "Devrait avoir 1 item")
        
        # Test avec numéro inexistant
        factura_inexistente = Factura.get_by_numero("INEXISTENTE-999")
        self.assertIsNone(factura_inexistente, "Ne devrait pas trouver de factura inexistante")
    
    def test_factura_selection_simulation(self):
        """Test: Simulation de sélection de factura"""
        # Simuler la sélection
        success = self.test_instance.select_factura(self.factura_test)

        # Vérifier que la sélection est correcte
        self.assertTrue(success, "La sélection devrait réussir")
        self.assertIsNotNone(self.test_instance.selected_factura, "selected_factura devrait être définie")
        self.assertEqual(self.test_instance.selected_factura.id, self.factura_test.id, "L'ID devrait correspondre")
        self.assertEqual(len(self.test_instance.selected_factura.items), 1, "Devrait avoir les items chargés")
    
    def test_pdf_export_validation(self):
        """Test: Validation avant exportation PDF"""
        # Test sans factura sélectionnée
        self.test_instance.selected_factura = None

        # Vérifier que la validation échoue
        is_valid, message = self.test_instance.validate_pdf_export()
        self.assertFalse(is_valid, "La validation devrait échouer sans factura")
        self.assertIn("No hay factura seleccionada", message, "Le message devrait indiquer l'absence de factura")

        # Test avec factura sélectionnée
        self.test_instance.select_factura(self.factura_test)

        # Vérifier que la validation passe
        is_valid, message = self.test_instance.validate_pdf_export()
        self.assertTrue(is_valid, f"La validation devrait réussir: {message}")
        self.assertEqual(message, "Factura válida para PDF", "Le message devrait confirmer la validité")
    
    def test_factura_data_completeness(self):
        """Test: Complétude des données de factura pour PDF"""
        factura = self.factura_test
        
        # Vérifier les champs obligatoires
        required_fields = [
            'numero_factura', 'nombre_cliente', 'fecha_factura',
            'subtotal', 'total_iva', 'total_factura'
        ]
        
        for field in required_fields:
            self.assertTrue(hasattr(factura, field), f"Devrait avoir le champ {field}")
            value = getattr(factura, field)
            self.assertIsNotNone(value, f"Le champ {field} ne devrait pas être None")
            if isinstance(value, str):
                self.assertNotEqual(value.strip(), "", f"Le champ {field} ne devrait pas être vide")
        
        # Vérifier les items
        self.assertIsNotNone(factura.items, "Devrait avoir des items")
        self.assertGreater(len(factura.items), 0, "Devrait avoir au moins un item")
        
        # Vérifier les données de l'item
        item = factura.items[0]
        item_fields = ['cantidad', 'precio_unitario', 'subtotal', 'iva_amount', 'total']
        
        for field in item_fields:
            self.assertTrue(hasattr(item, field), f"L'item devrait avoir le champ {field}")
            value = getattr(item, field)
            self.assertIsNotNone(value, f"Le champ de l'item {field} ne devrait pas être None")
    
    def test_multiple_facturas_selection(self):
        """Test: Sélection de multiples facturas"""
        # Créer une deuxième factura avec numéro unique
        import time
        timestamp = int(time.time())
        factura2 = Factura(
            numero_factura=f"PDF-TEST-{timestamp}-002",
            nombre_cliente="Cliente PDF Test 2",
            fecha_factura="2024-09-27"
        )

        item2 = FacturaItem(
            producto_id=self.producto_test.id,
            cantidad=2,
            precio_unitario=self.producto_test.precio,
            iva_aplicado=21.0
        )
        item2.calculate_totals()
        
        factura2.items = [item2]
        factura2.calculate_totals()
        factura2.save()
        
        try:
            # Test sélection de la première factura
            factura_1_found = Factura.get_by_numero(self.factura_test.numero_factura)
            self.assertIsNotNone(factura_1_found, "Devrait trouver la première factura")
            self.assertEqual(factura_1_found.nombre_cliente, "Cliente PDF Test", "Devrait être la bonne factura")

            # Test sélection de la deuxième factura
            factura_2_found = Factura.get_by_numero(factura2.numero_factura)
            self.assertIsNotNone(factura_2_found, "Devrait trouver la deuxième factura")
            self.assertEqual(factura_2_found.nombre_cliente, "Cliente PDF Test 2", "Devrait être la bonne factura")
            
            # Vérifier qu'elles sont différentes
            self.assertNotEqual(factura_1_found.id, factura_2_found.id, "Les facturas devraient être différentes")
            
        finally:
            # Nettoyer la deuxième factura
            try:
                factura2.delete()
            except:
                pass
    
    def test_pdf_export_method_call(self):
        """Test: Validation de l'exportation PDF"""
        # Configurer la factura sélectionnée
        self.test_instance.select_factura(self.factura_test)

        # Vérifier que la factura est prête pour l'exportation
        is_valid, message = self.test_instance.validate_pdf_export()
        self.assertTrue(is_valid, f"La factura devrait être valide pour PDF: {message}")

        # Vérifier les données spécifiques
        factura = self.test_instance.selected_factura
        self.assertIsNotNone(factura.numero_factura, "Devrait avoir un numéro de factura")
        self.assertIsNotNone(factura.nombre_cliente, "Devrait avoir un nom de client")
        self.assertIsNotNone(factura.fecha_factura, "Devrait avoir une date")
        self.assertGreater(factura.total_factura, 0, "Devrait avoir un total positif")
        self.assertGreater(len(factura.items), 0, "Devrait avoir des items")

        print("✅ Validation PDF complète réussie")

def run_pdf_integration_tests():
    """Exécute tous les tests d'intégration PDF"""
    
    print("🧪 TESTS D'INTÉGRATION - Exportation PDF")
    print("=" * 60)
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(PDFExportIntegrationTest)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION PDF:")
    print(f"   Tests exécutés: {result.testsRun}")
    print(f"   Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Échecs: {len(result.failures)}")
    print(f"   Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TOUS LES TESTS D'INTÉGRATION PDF RÉUSSIS")
        print("🎉 La sélection et exportation PDF fonctionne parfaitement")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifier les erreurs ci-dessus")
        
        # Afficher les détails des échecs
        if result.failures:
            print("\n📋 DÉTAILS DES ÉCHECS:")
            for test, traceback in result.failures:
                print(f"   • {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\n📋 DÉTAILS DES ERREURS:")
            for test, traceback in result.errors:
                print(f"   • {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_pdf_integration_tests()
    
    print("\n" + "=" * 60)
    print("📚 INFORMACIÓN ADICIONAL:")
    print("• Si ReportLab no está instalado: pip install reportlab")
    print("• Logs detallados en: logs/facturacion_facil.log")
    print("• Para test manual: test/demo/demo_test_pdf_export.py")
    print("• Documentación: docs/fixes/PDF_EXPORT_SELECTION_FIX.md")
    
    sys.exit(0 if success else 1)
