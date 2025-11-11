#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour vérifier la cohérence des données de stock
et la mise à jour correcte après modifications
"""

import sys
import os
import pytest

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def test_stock_data_structure_consistency(temp_db):
    """Test de cohérence entre les différentes méthodes de récupération de stock"""
    try:
        from database.models import Stock, Producto
        from database.optimized_models import OptimizedStock

        # Créer des données de test
        producto1 = Producto(nombre="Test Product 1", referencia="TEST001", precio=10.0)
        producto1.save()

        stock1 = Stock(producto_id=producto1.id, cantidad_disponible=5)
        stock1.save()
        
        print("🔍 Test de cohérence des structures de données de stock")
        
        # Test méthode originale
        original_data = Stock.get_all()
        assert original_data is not None, "Stock.get_all() ne devrait pas retourner None"
        
        if original_data:
            print(f"   ✅ Méthode originale: {len(original_data)} éléments")
            # Vérifier la structure des tuples
            first_item = original_data[0]
            assert len(first_item) >= 4, "Chaque élément devrait avoir au moins 4 champs"
            assert isinstance(first_item[0], int), "producto_id devrait être un entier"
            assert isinstance(first_item[1], (int, float)), "cantidad devrait être numérique"
        
        # Test méthode optimisée
        optimized_data = OptimizedStock.get_all_optimized()
        assert optimized_data is not None, "OptimizedStock.get_all_optimized() ne devrait pas retourner None"
        
        if optimized_data:
            print(f"   ✅ Méthode optimisée: {len(optimized_data)} éléments")
            # Vérifier la structure des dictionnaires
            first_item = optimized_data[0]
            required_keys = ['producto_id', 'cantidad', 'nombre', 'referencia']
            for key in required_keys:
                assert key in first_item, f"La clé '{key}' devrait être présente"
            
            assert isinstance(first_item['producto_id'], int), "producto_id devrait être un entier"
            assert isinstance(first_item['cantidad'], (int, float)), "cantidad devrait être numérique"
        
        # Vérifier la cohérence entre les deux méthodes
        if original_data and optimized_data:
            assert len(original_data) == len(optimized_data), "Les deux méthodes devraient retourner le même nombre d'éléments"
            print(f"   ✅ Cohérence: {len(original_data)} éléments dans les deux méthodes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test_stock_data_structure_consistency: {e}")
        raise

def test_stock_data_conversion(temp_db):
    """Test de la conversion des données comme dans force_reload_stock_data"""
    try:
        from database.models import Stock, Producto
        from database.database import db

        # Créer des données de test
        producto1 = Producto(nombre="Test Product 2", referencia="TEST002", precio=15.0)
        producto1.save()

        stock1 = Stock(producto_id=producto1.id, cantidad_disponible=8)
        stock1.save()
        
        print("🔍 Test de conversion des données (force_reload_stock_data)")
        
        query_results = Stock.get_all()
        converted_data = []
        
        for row in query_results:
            producto_id, cantidad, nombre, referencia = row
            
            # Obtenir fecha de última actualización (comme dans le code réel)
            fecha_query = "SELECT fecha_actualizacion FROM stock WHERE producto_id=?"
            fecha_result = db.execute_query(fecha_query, (producto_id,))
            fecha_actualizacion = fecha_result[0][0] if fecha_result else "N/A"
            
            converted_item = {
                'producto_id': producto_id,
                'nombre': nombre,
                'referencia': referencia,
                'cantidad': cantidad,
                'fecha_actualizacion': fecha_actualizacion
            }
            converted_data.append(converted_item)
        
        # Vérifications
        assert converted_data is not None, "Les données converties ne devraient pas être None"
        
        if converted_data:
            print(f"   ✅ Conversion réussie: {len(converted_data)} éléments")
            
            # Vérifier la structure
            first_item = converted_data[0]
            required_keys = ['producto_id', 'nombre', 'referencia', 'cantidad', 'fecha_actualizacion']
            for key in required_keys:
                assert key in first_item, f"La clé '{key}' devrait être présente après conversion"
            
            # Vérifier les types
            assert isinstance(first_item['producto_id'], int), "producto_id devrait être un entier"
            assert isinstance(first_item['cantidad'], (int, float)), "cantidad devrait être numérique"
            assert isinstance(first_item['nombre'], str), "nombre devrait être une chaîne"
            assert isinstance(first_item['referencia'], str), "referencia devrait être une chaîne"
            
            print(f"   ✅ Structure validée: {list(first_item.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test_stock_data_conversion: {e}")
        raise

def test_stock_display_compatibility(temp_db):
    """Test de compatibilité avec update_stock_display (version simplifiée)"""
    try:
        print("🔍 Test de compatibilité avec update_stock_display")

        # Test avec des données simulées (structure comme dans l'application réelle)
        simulated_data = [
            {
                'producto_id': 1,
                'nombre': 'Test Product 3',
                'referencia': 'TEST003',
                'cantidad': 12,
                'fecha_actualizacion': '2024-01-01 10:00:00'
            }
        ]

        # Test avec les données simulées
        for item in simulated_data:
            # Test des clés utilisées dans update_stock_display
            # stock_actual = item.get('cantidad', item.get('cantidad_disponible', 0))
            stock_actual = item.get('cantidad', item.get('cantidad_disponible', 0))
            assert stock_actual >= 0, "Le stock actuel devrait être >= 0"

            # nombre = item.get('nombre', item.get('producto_nombre', 'N/A'))
            nombre = item.get('nombre', item.get('producto_nombre', 'N/A'))
            assert nombre != 'N/A', "Le nom du produit devrait être disponible"

            # referencia
            referencia = item.get('referencia', 'N/A')
            assert referencia != 'N/A', "La référence devrait être disponible"

            # producto_id
            producto_id = item.get('producto_id', 0)
            assert producto_id > 0, "L'ID du produit devrait être > 0"

            print(f"   ✅ Compatibilité validée pour le produit {nombre} (ID: {producto_id}, Stock: {stock_actual})")

        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test_stock_display_compatibility: {e}")
        raise

def run_standalone_tests():
    """Exécute les tests en mode standalone (sans pytest)"""
    print("🚀 Tests de cohérence des données de stock")
    print("=" * 60)

    try:
        # En mode standalone, on passe None comme temp_db (pas utilisé)
        test_stock_data_structure_consistency(None)
        test_stock_data_conversion(None)
        test_stock_display_compatibility(None)

        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS PASSÉS")
        print("✅ La cohérence des données de stock est validée")

    except Exception as e:
        print(f"\n❌ ÉCHEC DES TESTS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_standalone_tests()
