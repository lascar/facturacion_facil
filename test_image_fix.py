#!/usr/bin/env python3
"""
Test rápido para verificar la corrección del error de imagen_display
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_image_display_fix():
    """Test para verificar que el error de imagen_display está corregido"""
    print("🔧 Test de corrección del error imagen_display...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Crear un mock de parent
        parent = Mock()
        parent.winfo_exists.return_value = True
        
        # Crear la ventana (esto debería funcionar sin errores)
        print("✅ Creando ventana de productos...")
        window = ProductosWindow(parent)
        
        # Verificar que los atributos existen
        print("✅ Verificando atributos de imagen...")
        assert hasattr(window, 'imagen_display'), "imagen_display no existe"
        assert hasattr(window, 'quitar_imagen_btn'), "quitar_imagen_btn no existe"
        assert hasattr(window, 'imagen_label'), "imagen_label no existe"
        assert hasattr(window, 'imagen_path'), "imagen_path no existe"
        
        # Verificar que update_image_display funciona
        print("✅ Probando update_image_display...")
        window.update_image_display()  # No debería dar error
        
        # Verificar que quitar_imagen funciona
        print("✅ Probando quitar_imagen...")
        window.quitar_imagen()  # No debería dar error
        
        # Verificar que limpiar_formulario funciona
        print("✅ Probando limpiar_formulario...")
        window.limpiar_formulario()  # No debería dar error
        
        print("🎉 ¡Todos los tests pasaron! El error está corregido.")
        return True
        
    except Exception as e:
        print(f"❌ Error en el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_method_safety():
    """Test para verificar que los métodos son seguros sin widgets"""
    print("\n🛡️ Test de seguridad de métodos...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Crear una instancia sin widgets
        instance = object.__new__(ProductosWindow)
        instance.imagen_path = ""
        
        # Estos métodos deberían ser seguros de llamar
        print("✅ Probando update_image_display sin widgets...")
        instance.update_image_display()  # Debería retornar sin error
        
        print("✅ Probando quitar_imagen sin widgets...")
        instance.quitar_imagen()  # Debería retornar sin error
        
        print("🎉 Los métodos son seguros sin widgets!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de seguridad: {e}")
        return False

def test_config_system():
    """Test para verificar que el sistema de configuración funciona"""
    print("\n⚙️ Test del sistema de configuración...")
    
    try:
        from utils.config import app_config
        
        # Test de métodos básicos
        default_dir = app_config.get_default_image_directory()
        print(f"✅ Directorio por defecto: {default_dir}")
        
        display_size = app_config.get_image_display_size()
        print(f"✅ Tamaño de display: {display_size}")
        
        formats = app_config.get_supported_formats()
        print(f"✅ Formatos soportados: {formats}")
        
        print("🎉 Sistema de configuración funciona correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de configuración: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Test de Corrección del Error imagen_display")
    print("=" * 50)
    
    tests = [
        ("Corrección imagen_display", test_image_display_fix),
        ("Seguridad de métodos", test_method_safety),
        ("Sistema de configuración", test_config_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡CORRECCIÓN EXITOSA!")
        print("El error 'imagen_display' ha sido corregido completamente.")
        print("\n📋 Cambios realizados:")
        print("   1. ✅ Verificación de atributos en update_image_display()")
        print("   2. ✅ Verificación de atributos en quitar_imagen()")
        print("   3. ✅ Manejo seguro de widgets no inicializados")
        print("   4. ✅ Mensajes de debug informativos")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON!")
        print("Revisa los errores arriba para más detalles.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
