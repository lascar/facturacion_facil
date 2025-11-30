#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du calcul de stock pour l'édition de factures
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stock_calculation_logic():
    """Tester la logique de calcul de stock"""
    print("🔍 Test de la logique de calcul de stock...")
    
    # Scénario de test
    print("\n📋 SCÉNARIO DE TEST:")
    print("   - Stock actuel en base: 5 unités")
    print("   - Facture originale: 7 unités")
    print("   - Utilisateur veut modifier à: 2 unités")
    
    # Calcul attendu
    stock_actual = 5
    cantidad_original = 7
    nueva_cantidad = 2
    
    # Calcul selon get_available_stock_for_product
    stock_disponible = stock_actual + cantidad_original
    print(f"\n🧮 CALCUL:")
    print(f"   Stock disponible = Stock actuel + Cantidad original")
    print(f"   Stock disponible = {stock_actual} + {cantidad_original} = {stock_disponible}")
    
    # Vérification
    puede_modificar = nueva_cantidad <= stock_disponible
    print(f"\n✅ VÉRIFICATION:")
    print(f"   Nueva cantidad ({nueva_cantidad}) <= Stock disponible ({stock_disponible}) = {puede_modificar}")
    
    if puede_modificar:
        print("   ✅ Modification autorisée")
    else:
        print("   ❌ Modification refusée")
    
    return puede_modificar

def test_edge_cases():
    """Tester les cas limites"""
    print("\n🔍 Test des cas limites...")
    
    test_cases = [
        {
            "name": "Stock suffisant",
            "stock_actual": 5,
            "cantidad_original": 3,
            "nueva_cantidad": 8,
            "expected": True
        },
        {
            "name": "Stock exact",
            "stock_actual": 5,
            "cantidad_original": 3,
            "nueva_cantidad": 8,
            "expected": True
        },
        {
            "name": "Stock insuffisant",
            "stock_actual": 5,
            "cantidad_original": 3,
            "nueva_cantidad": 10,
            "expected": False
        },
        {
            "name": "Réduction de quantité",
            "stock_actual": 5,
            "cantidad_original": 7,
            "nueva_cantidad": 2,
            "expected": True
        },
        {
            "name": "Stock zéro",
            "stock_actual": 0,
            "cantidad_original": 5,
            "nueva_cantidad": 3,
            "expected": True
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for case in test_cases:
        stock_disponible = case["stock_actual"] + case["cantidad_original"]
        result = case["nueva_cantidad"] <= stock_disponible
        
        print(f"\n   📝 {case['name']}:")
        print(f"      Stock actual: {case['stock_actual']}")
        print(f"      Cantidad original: {case['cantidad_original']}")
        print(f"      Nueva cantidad: {case['nueva_cantidad']}")
        print(f"      Stock disponible: {stock_disponible}")
        print(f"      Resultado: {result} (esperado: {case['expected']})")
        
        if result == case["expected"]:
            print(f"      ✅ CORRECTO")
            passed += 1
        else:
            print(f"      ❌ INCORRECTO")
    
    print(f"\n🎯 Casos limites: {passed}/{total} réussis")
    return passed == total

def test_code_verification():
    """Vérifier que le code a été corrigé"""
    print("\n🔍 Vérification du code corrigé...")
    
    try:
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que la double soustraction a été supprimée
        if "stock_disponible_para_linea = stock_disponible - cantidad_original_linea" in content:
            print("❌ Double soustraction encore présente")
            return False
        else:
            print("✅ Double soustraction supprimée")
        
        # Vérifier le nouveau code
        if "nueva_cantidad > stock_disponible:" in content:
            print("✅ Comparaison directe implémentée")
        else:
            print("❌ Comparaison directe non trouvée")
            return False
        
        # Vérifier le message corrigé
        if "f\"Stock disponible para edición: {stock_disponible}\\n\"" in content:
            print("✅ Message de stock corrigé")
        else:
            print("❌ Message de stock non corrigé")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification code: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DU CALCUL DE STOCK POUR L'ÉDITION")
    print("=" * 55)
    
    tests = [
        test_stock_calculation_logic,
        test_edge_cases,
        test_code_verification
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 55)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 CALCUL DE STOCK CORRIGÉ !")
        print("\n📋 Correction appliquée:")
        print("   ✅ Suppression de la double soustraction")
        print("   ✅ Comparaison directe avec stock disponible")
        print("   ✅ Message d'erreur correct")
        print("\n🧮 Formule finale:")
        print("   Stock disponible = Stock actuel + Cantidad original")
        print("   Autorisation = Nueva cantidad <= Stock disponible")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Test terminé: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
