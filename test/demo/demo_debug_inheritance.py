#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diagnostic de l'héritage et des méthodes dans FacturasWindow
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import inspect
from ui.facturas import FacturasWindow
from ui.facturas_methods import FacturasMethodsMixin
from common.ui_components import BaseWindow

def debug_inheritance():
    """Diagnostiquer l'héritage et les méthodes disponibles"""
    
    print("🔍 DIAGNOSTIC - Héritage et Méthodes")
    print("=" * 50)
    
    print("1️⃣ Vérification de l'héritage...")
    print(f"   FacturasWindow MRO: {[cls.__name__ for cls in FacturasWindow.__mro__]}")
    
    print("\n2️⃣ Vérification des méthodes clés...")
    
    methods_to_check = [
        'guardar_factura',
        'update_stock_after_save',
        'show_stock_impact_summary',
        'validate_factura_form',
        'validate_stock_availability'
    ]
    
    for method_name in methods_to_check:
        print(f"\n   🔍 Méthode: {method_name}")
        
        # Vérifier dans FacturasMethodsMixin
        if hasattr(FacturasMethodsMixin, method_name):
            method = getattr(FacturasMethodsMixin, method_name)
            print(f"      ✅ Existe dans FacturasMethodsMixin")
            print(f"         Fichier: {inspect.getfile(method)}")
            print(f"         Ligne: {inspect.getsourcelines(method)[1]}")
        else:
            print(f"      ❌ NO existe dans FacturasMethodsMixin")
        
        # Vérifier dans FacturasWindow
        if hasattr(FacturasWindow, method_name):
            method = getattr(FacturasWindow, method_name)
            print(f"      ✅ Disponible dans FacturasWindow")
            print(f"         Définie dans: {method.__qualname__}")
        else:
            print(f"      ❌ NO disponible dans FacturasWindow")
    
    print("\n3️⃣ Vérification de la résolution de méthodes...")
    
    # Créer une instance fictive pour tester
    try:
        import customtkinter as ctk
        app = ctk.CTk()
        app.withdraw()  # Cacher la fenêtre
        
        # Créer instance de FacturasWindow
        facturas_window = FacturasWindow(app)
        
        print("   ✅ Instance FacturasWindow créée avec succès")
        
        # Vérifier les méthodes sur l'instance
        for method_name in methods_to_check:
            if hasattr(facturas_window, method_name):
                method = getattr(facturas_window, method_name)
                print(f"      ✅ {method_name}: {method}")
                print(f"         Type: {type(method)}")
                print(f"         Callable: {callable(method)}")
            else:
                print(f"      ❌ {method_name}: NO disponible sur l'instance")
        
        # Fermer l'application
        app.quit()
        app.destroy()
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la création de l'instance: {e}")
    
    print("\n4️⃣ Vérification du code source...")
    
    try:
        # Vérifier le code source de guardar_factura
        if hasattr(FacturasMethodsMixin, 'guardar_factura'):
            method = getattr(FacturasMethodsMixin, 'guardar_factura')
            source_lines = inspect.getsourcelines(method)[0]
            
            print(f"   📄 Code source de guardar_factura (premières lignes):")
            for i, line in enumerate(source_lines[:10], 1):
                print(f"      {i:2d}: {line.rstrip()}")
            
            # Chercher l'appel à update_stock_after_save
            update_stock_call_found = False
            for line_num, line in enumerate(source_lines, 1):
                if 'update_stock_after_save' in line:
                    print(f"   ✅ Appel à update_stock_after_save trouvé ligne {line_num}: {line.strip()}")
                    update_stock_call_found = True
            
            if not update_stock_call_found:
                print(f"   ❌ Appel à update_stock_after_save NOT trouvé dans guardar_factura")
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification du code source: {e}")
    
    print("\n5️⃣ Vérification des imports...")
    
    # Vérifier les imports dans facturas.py
    try:
        import ui.facturas as facturas_module
        
        print("   📦 Imports dans ui.facturas:")
        
        # Vérifier si FacturasMethodsMixin est importé
        if hasattr(facturas_module, 'FacturasMethodsMixin'):
            print("      ✅ FacturasMethodsMixin importé")
        else:
            print("      ❌ FacturasMethodsMixin NOT importé")
        
        # Vérifier les autres imports importants
        important_imports = ['Stock', 'Factura', 'FacturaItem', 'Producto']
        for imp in important_imports:
            if hasattr(facturas_module, imp):
                print(f"      ✅ {imp} importé")
            else:
                print(f"      ❌ {imp} NOT importé")
    
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification des imports: {e}")

def demo_method_resolution():
    """Tester la résolution de méthodes avec un exemple simple"""
    
    print("\n🧪 TEST - Résolution de Méthodes")
    print("-" * 40)
    
    try:
        # Créer une classe de test qui simule FacturasWindow
        class TestFacturasWindow(BaseWindow, FacturasMethodsMixin):
            def __init__(self):
                # Simuler l'initialisation minimale
                self.logger = None
                self.current_factura = None
                self.factura_items = []
                self.window = None
            
            def _show_message(self, msg_type, title, message):
                print(f"[TEST MESSAGE] {msg_type}: {title} - {message}")
        
        # Créer instance de test
        test_instance = TestFacturasWindow()
        
        print("   ✅ Instance de test créée")
        
        # Vérifier les méthodes
        methods_to_test = ['guardar_factura', 'update_stock_after_save']
        
        for method_name in methods_to_test:
            if hasattr(test_instance, method_name):
                method = getattr(test_instance, method_name)
                print(f"   ✅ {method_name}: Disponible")
                print(f"      Type: {type(method)}")
                print(f"      Module: {method.__module__ if hasattr(method, '__module__') else 'N/A'}")
                print(f"      Qualname: {method.__qualname__ if hasattr(method, '__qualname__') else 'N/A'}")
            else:
                print(f"   ❌ {method_name}: NOT disponible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur dans le test de résolution: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_mixin_integrity():
    """Vérifier l'intégrité du mixin"""
    
    print("\n🔬 VÉRIFICATION - Intégrité du Mixin")
    print("-" * 40)
    
    try:
        # Vérifier que le mixin a toutes les méthodes attendues
        expected_methods = [
            'initialize_numero_factura',
            'validate_factura_form',
            'validate_stock_availability',
            'show_stock_impact_summary',
            'guardar_factura',
            'update_stock_after_save',
            'eliminar_factura'
        ]
        
        missing_methods = []
        for method_name in expected_methods:
            if not hasattr(FacturasMethodsMixin, method_name):
                missing_methods.append(method_name)
            else:
                print(f"   ✅ {method_name}")
        
        if missing_methods:
            print(f"   ❌ Méthodes manquantes: {missing_methods}")
            return False
        else:
            print("   ✅ Toutes les méthodes attendues sont présentes")
            return True
    
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DIAGNOSTIC COMPLET - Héritage FacturasWindow")
    print("=" * 60)
    
    # Test 1: Diagnostic de l'héritage
    debug_inheritance()
    
    # Test 2: Test de résolution de méthodes
    success1 = demo_method_resolution()
    
    # Test 3: Vérification de l'intégrité du mixin
    success2 = check_mixin_integrity()
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC:")
    print(f"   Test résolution méthodes: {'✅ ÉXITO' if success1 else '❌ FALLO'}")
    print(f"   Intégrité du mixin: {'✅ ÉXITO' if success2 else '❌ FALLO'}")
    
    if success1 and success2:
        print("\n✅ L'héritage semble correct")
        print("Le problème pourrait être ailleurs:")
        print("   • Dans l'exécution du code")
        print("   • Dans la base de données")
        print("   • Dans les données de test")
    else:
        print("\n❌ Problèmes détectés dans l'héritage")
        print("Vérifier la structure des classes et l'ordre d'héritage")
    
    print("\n📚 Prochaines étapes recommandées:")
    print("   1. Exécuter le test en temps réel")
    print("   2. Vérifier les logs pendant l'utilisation")
    print("   3. Tester avec des données réelles")
    print("   4. Vérifier la base de données directement")
