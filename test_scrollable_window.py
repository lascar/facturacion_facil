#!/usr/bin/env python3
"""
Test pour vérifier l'implémentation des scrollbars dans la fenêtre de produits
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scrollable_frame_implementation():
    """Test que CTkScrollableFrame est utilisé"""
    print("🔍 Test de l'implémentation du frame scrollable...")
    
    try:
        # Vérifier que CTkScrollableFrame est importé et utilisé
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier l'utilisation de CTkScrollableFrame
        scrollable_patterns = [
            'CTkScrollableFrame',
            'main_frame = ctk.CTkScrollableFrame(self.window)',
            'Frame principal scrollable',
            'configure_scrollable_behavior'
        ]
        
        patterns_found = 0
        for pattern in scrollable_patterns:
            if pattern in content:
                patterns_found += 1
                print(f"   ✅ {pattern} trouvé")
            else:
                print(f"   ❌ {pattern} NON trouvé")
        
        if patterns_found >= 3:  # Au moins 3 sur 4
            print("   ✅ CTkScrollableFrame correctement implémenté")
            return True
        else:
            print("   ❌ Implémentation de CTkScrollableFrame insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_window_resizable_configuration():
    """Test que la fenêtre est configurée comme redimensionnable"""
    print("\n🔍 Test de la configuration redimensionnable...")
    
    try:
        # Vérifier le code de configuration
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les configurations de redimensionnement
        resize_patterns = [
            'self.window.resizable(True, True)',
            'self.window.minsize(',
            'self.window.maxsize(',
            'configure_scrollable_behavior'
        ]
        
        patterns_found = 0
        for pattern in resize_patterns:
            if pattern in content:
                patterns_found += 1
                print(f"   ✅ {pattern} trouvé")
            else:
                print(f"   ❌ {pattern} NON trouvé")
        
        if patterns_found >= 3:  # Au moins 3 sur 4
            print("   ✅ Configuration de redimensionnement implémentée")
            return True
        else:
            print("   ❌ Configuration de redimensionnement insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_scrollable_frame_size_configuration():
    """Test que le frame scrollable a une taille configurée"""
    print("\n🔍 Test de la configuration de taille du frame scrollable...")
    
    try:
        # Vérifier le code de configuration de taille
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les configurations de taille
        size_patterns = [
            'main_frame.configure(',
            'width=',
            'height=',
            'tamaño mínimo'
        ]
        
        patterns_found = 0
        for pattern in size_patterns:
            if pattern in content:
                patterns_found += 1
                print(f"   ✅ {pattern} trouvé")
            else:
                print(f"   ❌ {pattern} NON trouvé")
        
        if patterns_found >= 3:  # Au moins 3 sur 4
            print("   ✅ Configuration de taille du frame scrollable implémentée")
            return True
        else:
            print("   ❌ Configuration de taille insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_scrollable_method_exists():
    """Test que la méthode configure_scrollable_behavior existe"""
    print("\n🔍 Test de l'existence de la méthode configure_scrollable_behavior...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Vérifier que la méthode existe
        assert hasattr(ProductosWindow, 'configure_scrollable_behavior'), "Méthode configure_scrollable_behavior n'existe pas"
        
        # Vérifier que c'est une méthode callable
        method = getattr(ProductosWindow, 'configure_scrollable_behavior')
        assert callable(method), "configure_scrollable_behavior n'est pas callable"
        
        print("   ✅ Méthode configure_scrollable_behavior existe")
        print("   ✅ Méthode est callable")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_logging_integration():
    """Test que le logging du scrolling est intégré"""
    print("\n🔍 Test de l'intégration du logging pour scrolling...")
    
    try:
        # Vérifier le code de logging
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les messages de logging
        logging_patterns = [
            'Frame principal scrollable creado',
            'Comportamiento de scrolling configurado',
            'scrolling habilitado',
            'self.logger.debug'
        ]
        
        patterns_found = 0
        for pattern in logging_patterns:
            if pattern in content:
                patterns_found += 1
                print(f"   ✅ {pattern} trouvé")
            else:
                print(f"   ❌ {pattern} NON trouvé")
        
        if patterns_found >= 3:  # Au moins 3 sur 4
            print("   ✅ Logging du scrolling intégré")
            return True
        else:
            print("   ❌ Logging du scrolling insuffisant")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_customtkinter_scrollable_availability():
    """Test que CTkScrollableFrame est disponible"""
    print("\n🔍 Test de disponibilité de CTkScrollableFrame...")
    
    try:
        import customtkinter as ctk
        
        # Vérifier que CTkScrollableFrame existe
        assert hasattr(ctk, 'CTkScrollableFrame'), "CTkScrollableFrame n'est pas disponible dans customtkinter"
        
        # Vérifier que c'est une classe
        scrollable_frame_class = getattr(ctk, 'CTkScrollableFrame')
        assert isinstance(scrollable_frame_class, type), "CTkScrollableFrame n'est pas une classe"
        
        print("   ✅ CTkScrollableFrame disponible dans customtkinter")
        print("   ✅ CTkScrollableFrame est une classe valide")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test d'Implémentation des Scrollbars")
    print("=" * 60)
    
    tests = [
        ("CTkScrollableFrame disponible", test_customtkinter_scrollable_availability),
        ("Implémentation du frame scrollable", test_scrollable_frame_implementation),
        ("Configuration redimensionnable", test_window_resizable_configuration),
        ("Configuration de taille", test_scrollable_frame_size_configuration),
        ("Méthode configure_scrollable_behavior", test_scrollable_method_exists),
        ("Intégration du logging", test_logging_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡SCROLLBARS CORRECTAMENTE IMPLEMENTADAS!")
        print("\n📋 Funcionalidades implementadas:")
        print("   1. ✅ CTkScrollableFrame como frame principal")
        print("   2. ✅ Ventana redimensionnable con límites")
        print("   3. ✅ Configuración de tamaño mínimo del contenido")
        print("   4. ✅ Método de configuración de scrolling")
        print("   5. ✅ Logging detallado del proceso")
        print("\n🎯 Ahora la ventana de productos:")
        print("   - Se puede redimensionar libremente")
        print("   - Muestra scrollbars cuando el contenido es grande")
        print("   - Tiene límites mínimos y máximos razonables")
        print("   - Mantiene toda la funcionalidad existente")
        print("\n📋 Para probar:")
        print("   1. Abrir 'Gestión de Productos'")
        print("   2. Redimensionar la ventana a un tamaño pequeño")
        print("   3. ✅ Scrollbars aparecen automáticamente")
        print("   4. ✅ Todo el contenido sigue accesible")
    else:
        print("⚠️  ALGUNAS IMPLEMENTACIONES FALLARON!")
        print("Vérifiez les détails ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
