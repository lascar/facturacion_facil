#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérification rapide de l'héritage et des méthodes disponibles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def quick_inheritance_check():
    """Vérification rapide de l'héritage"""
    
    print("🔍 VÉRIFICATION RAPIDE - Héritage FacturasWindow")
    print("=" * 60)
    
    try:
        # Importer les classes
        from ui.facturas import FacturasWindow
        from ui.facturas_methods import FacturasMethodsMixin
        from common.ui_components import BaseWindow
        
        print("✅ Imports réussis")
        
        # Vérifier l'ordre d'héritage
        print(f"\n📋 MRO (Method Resolution Order):")
        for i, cls in enumerate(FacturasWindow.__mro__, 1):
            print(f"   {i}. {cls.__name__} ({cls.__module__})")
        
        # Vérifier les méthodes clés
        print(f"\n🔍 Vérification des méthodes:")
        
        methods_to_check = [
            'guardar_factura',
            'update_stock_after_save',
            'debug_guardar_factura',
            'validate_factura_form',
            'show_stock_impact_summary',
            'show_stock_confirmation_dialog_direct',
            'show_simple_confirmation_dialog'
        ]
        
        for method_name in methods_to_check:
            # Dans FacturasMethodsMixin
            in_mixin = hasattr(FacturasMethodsMixin, method_name)
            # Dans FacturasWindow
            in_window = hasattr(FacturasWindow, method_name)
            
            print(f"   {method_name}:")
            print(f"      Mixin: {'✅' if in_mixin else '❌'}")
            print(f"      Window: {'✅' if in_window else '❌'}")
            
            if in_window:
                method = getattr(FacturasWindow, method_name)
                print(f"      Définie dans: {method.__qualname__}")
        
        # Test de création d'instance
        print(f"\n🧪 Test de création d'instance:")
        
        try:
            import customtkinter as ctk
            
            # Créer une app minimale
            app = ctk.CTk()
            app.withdraw()  # Cacher
            
            # Créer instance
            facturas_window = FacturasWindow(app)
            print("   ✅ Instance créée avec succès")
            
            # Vérifier les méthodes sur l'instance
            for method_name in methods_to_check:
                if hasattr(facturas_window, method_name):
                    method = getattr(facturas_window, method_name)
                    print(f"   ✅ {method_name}: {type(method)}")
                else:
                    print(f"   ❌ {method_name}: Non disponible")
            
            # Fermer
            app.quit()
            app.destroy()
            
        except Exception as e:
            print(f"   ❌ Erreur création instance: {e}")
        
        # Vérifier le code source de guardar_factura
        print(f"\n📄 Code source de guardar_factura:")
        
        if hasattr(FacturasMethodsMixin, 'guardar_factura'):
            import inspect
            method = getattr(FacturasMethodsMixin, 'guardar_factura')
            
            try:
                source_lines = inspect.getsourcelines(method)[0]
                print(f"   📍 Fichier: {inspect.getfile(method)}")
                print(f"   📍 Ligne: {inspect.getsourcelines(method)[1]}")
                print(f"   📍 Nombre de lignes: {len(source_lines)}")
                
                # Chercher l'appel à update_stock_after_save
                update_call_found = False
                for line_num, line in enumerate(source_lines, 1):
                    if 'update_stock_after_save' in line:
                        print(f"   ✅ Appel update_stock_after_save trouvé ligne {line_num}: {line.strip()}")
                        update_call_found = True
                
                if not update_call_found:
                    print(f"   ❌ Appel update_stock_after_save NON trouvé")
                
                # Montrer les premières lignes
                print(f"   📄 Premières lignes:")
                for i, line in enumerate(source_lines[:5], 1):
                    print(f"      {i:2d}: {line.rstrip()}")
                
            except Exception as e:
                print(f"   ❌ Erreur lecture code source: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans vérification: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_button_command():
    """Vérifier la commande du bouton guardar"""
    
    print(f"\n🔘 VÉRIFICATION - Commande du bouton")
    print("-" * 40)
    
    try:
        # Lire le fichier facturas.py
        facturas_file = "ui/facturas.py"
        
        with open(facturas_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher la définition du bouton guardar
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'guardar_btn' in line and 'command=' in line:
                print(f"   📍 Ligne {i}: {line.strip()}")
                
                # Vérifier les lignes autour
                start = max(0, i-3)
                end = min(len(lines), i+2)
                
                print(f"   📄 Contexte:")
                for j in range(start, end):
                    marker = ">>>" if j == i-1 else "   "
                    print(f"   {marker} {j+1:3d}: {lines[j]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lecture fichier: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VÉRIFICATION RAPIDE DE L'HÉRITAGE")
    print("=" * 60)
    
    success1 = quick_inheritance_check()
    success2 = check_button_command()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"   Vérification héritage: {'✅ OK' if success1 else '❌ ERREUR'}")
    print(f"   Vérification bouton: {'✅ OK' if success2 else '❌ ERREUR'}")
    
    if success1 and success2:
        print("\n✅ HÉRITAGE SEMBLE CORRECT")
        print("Le problème est probablement dans l'exécution ou les données")
        print("\n📋 Prochaines étapes:")
        print("   1. Exécuter test avec interface debug")
        print("   2. Vérifier les logs pendant l'utilisation")
        print("   3. Tester avec données réelles")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("Corriger les problèmes d'héritage avant de continuer")
    
    print("\n📚 Scripts disponibles:")
    print("   • demo_interface_debug_test.py - Test avec interface")
    print("   • demo_simple_stock_test.py - Test basique (déjà exécuté)")
    print("   • logs/facturacion_facil.log - Logs détaillés")
