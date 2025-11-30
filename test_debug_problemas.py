#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de debug pour les problèmes identifiés
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stock_display_logic():
    """Tester la logique d'affichage du stock"""
    print("🔍 Test de la logique d'affichage du stock...")
    
    try:
        # Simuler les données de produits
        productos_test = [
            {'id': 1, 'nombre': 'Producto A', 'stock_actual': 0, 'precio_venta': 10.0},
            {'id': 2, 'nombre': 'Producto B', 'stock_actual': 5, 'precio_venta': 15.0},
            {'id': 3, 'nombre': 'Producto C', 'stock_actual': 10, 'precio_venta': 20.0}
        ]
        
        print("\n📋 PRODUCTOS DE TEST:")
        for producto in productos_test:
            stock = producto.get('stock_actual', 0)
            display_text = f"{producto['nombre']} - {producto['precio_venta']:.2f}€ (Stock: {stock})"
            print(f"   ID {producto['id']}: {display_text}")
        
        print("\n🔍 ANÁLISIS:")
        print("   - CrearFacturaDialog (ventana izquierda): Muestra stock actual de base de datos")
        print("   - EditarFacturaDialog (ventana derecha): Muestra stock actual + cantidad original")
        
        # Simuler le calcul pour l'édition
        factura_data = {
            'lineas': [
                {'producto_id': 2, 'cantidad': 3}  # Producto B con 3 unidades en factura
            ]
        }
        
        for producto in productos_test:
            if producto['id'] == 2:  # Producto B
                stock_actual = producto['stock_actual']  # 5
                cantidad_original = 3  # De la factura
                stock_disponible = stock_actual + cantidad_original  # 5 + 3 = 8
                
                print(f"\n   📊 PRODUCTO B (ID 2) EN EDICIÓN:")
                print(f"      Stock actual en base: {stock_actual}")
                print(f"      Cantidad en factura original: {cantidad_original}")
                print(f"      Stock disponible para edición: {stock_disponible}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test stock: {e}")
        return False

def test_dialog_flow_analysis():
    """Analyser le flux des dialogues"""
    print("\n🔍 Analyse du flux des dialogues...")
    
    try:
        print("📋 FLUX NORMAL ATTENDU:")
        print("   1. Utilisateur clique 'Editar' sur une facture")
        print("   2. edit_factura() s'exécute")
        print("   3. EditarFacturaDialog s'ouvre")
        print("   4. Utilisateur modifie et clique 'OK'")
        print("   5. guardar_factura() s'exécute")
        print("   6. Message de succès s'affiche")
        print("   7. self.accept() ferme le dialogue")
        print("   8. edit_factura() reçoit QDialog.Accepted")
        print("   9. load_facturas() recharge la liste")
        print("  10. FIN - Retour à la fenêtre principale")
        
        print("\n🚨 PROBLÈME IDENTIFIÉ:")
        print("   Après l'étape 10, une nouvelle fenêtre de création s'ouvre")
        print("   Cela suggère que new_factura() est appelée quelque part")
        
        print("\n🔍 CAUSES POSSIBLES:")
        print("   A. Signal accidentel émis après self.accept()")
        print("   B. Connexion de signal incorrecte")
        print("   C. Événement clavier/souris mal géré")
        print("   D. Callback ou timer qui déclenche new_factura()")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur analyse flux: {e}")
        return False

def test_signal_connections():
    """Vérifier les connexions de signaux"""
    print("\n🔍 Vérification des connexions de signaux...")
    
    try:
        # Vérifier le code des connexions
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher toutes les connexions
        connections = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '.connect(' in line and 'new_factura' in line:
                connections.append((i+1, line.strip()))
        
        print("📋 CONNEXIONS TROUVÉES POUR new_factura:")
        for line_num, line in connections:
            print(f"   Ligne {line_num}: {line}")
        
        if len(connections) == 1:
            print("✅ Une seule connexion trouvée (normal)")
        else:
            print(f"⚠️  {len(connections)} connexions trouvées (potentiel problème)")
        
        # Chercher d'autres appels à new_factura
        calls = []
        for i, line in enumerate(lines):
            if 'new_factura(' in line and 'def new_factura' not in line and '.connect(' not in line:
                calls.append((i+1, line.strip()))
        
        print("\n📋 APPELS DIRECTS À new_factura:")
        if calls:
            for line_num, line in calls:
                print(f"   Ligne {line_num}: {line}")
        else:
            print("   Aucun appel direct trouvé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification signaux: {e}")
        return False

def test_debug_logs():
    """Vérifier que les logs de debug sont en place"""
    print("\n🔍 Vérification des logs de debug...")
    
    try:
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        debug_checks = [
            ("new_factura() appelée", "Log d'ouverture nouvelle facture"),
            ("EditarFacturaDialog - Producto:", "Log de stock éditeur"),
            ("CrearFacturaDialog - Producto:", "Log de stock création"),
            ("edit_factura() - Editando factura", "Log début édition"),
            ("edit_factura() - Resultado del diálogo", "Log résultat dialogue")
        ]
        
        print("📋 LOGS DE DEBUG AJOUTÉS:")
        for search_text, description in debug_checks:
            if search_text in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - NON TROUVÉ")
        
        print("\n💡 INSTRUCTIONS POUR DEBUG:")
        print("   1. Lancez l'application")
        print("   2. Activez les logs debug si nécessaire")
        print("   3. Éditez une facture")
        print("   4. Observez les logs pour voir l'ordre des événements")
        print("   5. Identifiez quand new_factura() est appelée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification logs: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 DEBUG DES PROBLÈMES IDENTIFIÉS")
    print("=" * 50)
    
    tests = [
        test_stock_display_logic,
        test_dialog_flow_analysis,
        test_signal_connections,
        test_debug_logs
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 DEBUG PRÉPARÉ !")
        print("\n📋 Prochaines étapes:")
        print("   1. Lancez l'application avec les logs debug")
        print("   2. Reproduisez le problème d'édition")
        print("   3. Analysez les logs pour identifier la cause")
        print("   4. Corrigez la connexion/signal problématique")
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
