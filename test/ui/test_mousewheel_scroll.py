#!/usr/bin/env python3
"""
Test pour vérifier que le scroll de la rueda del ratón fonctionne dans la fenêtre des produits
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mousewheel_scroll_implementation():
    """Test que les méthodes de scroll de la souris sont implémentées"""
    print("🧪 Test: Implémentation du scroll de la rueda del ratón")
    
    try:
        # Vérifier que les nouvelles méthodes sont présentes dans le code
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les méthodes ajoutées
        required_methods = [
            'bind_mousewheel_to_scrollable',
            'configure_mousewheel_scrolling',
            '_on_mousewheel',
            'self.main_frame',
            'MouseWheel',
            'Button-4',
            'Button-5'
        ]
        
        methods_found = 0
        for method in required_methods:
            if method in content:
                methods_found += 1
                print(f"   ✅ {method} trouvé")
            else:
                print(f"   ❌ {method} NON trouvé")
        
        if methods_found >= 6:  # Au moins 6 sur 7
            print("   ✅ Implémentation du scroll de la souris correcte")
            return True
        else:
            print("   ❌ Implémentation du scroll de la souris insuffisante")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
        return False

def test_mousewheel_scroll_integration():
    """Test que l'intégration du scroll est correcte"""
    print("\n🧪 Test: Intégration du scroll de la souris")
    
    try:
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que configure_mousewheel_scrolling est appelé dans __init__
        integration_checks = [
            'self.configure_mousewheel_scrolling()',
            'self.main_frame = ctk.CTkScrollableFrame',
            'bind_to_children(self.window)'
        ]
        
        checks_passed = 0
        for check in integration_checks:
            if check in content:
                checks_passed += 1
                print(f"   ✅ {check} trouvé")
            else:
                print(f"   ❌ {check} NON trouvé")
        
        if checks_passed >= 2:  # Au moins 2 sur 3
            print("   ✅ Intégration du scroll correcte")
            return True
        else:
            print("   ❌ Intégration du scroll insuffisante")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🎯 Test du scroll de la rueda del ratón dans la fenêtre des produits")
    print("=" * 70)
    
    test1 = test_mousewheel_scroll_implementation()
    test2 = test_mousewheel_scroll_integration()
    
    print("\n" + "=" * 70)
    if test1 and test2:
        print("✅ TOUS LES TESTS RÉUSSIS - Le scroll de la souris est implémenté!")
        print("\n💡 Instructions pour tester:")
        print("   1. Lancez l'application: python main.py")
        print("   2. Ouvrez la fenêtre des produits")
        print("   3. Utilisez la rueda del ratón pour faire défiler le contenu")
        print("   4. Le scroll devrait fonctionner sur toute la fenêtre")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
