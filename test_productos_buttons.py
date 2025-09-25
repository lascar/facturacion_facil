#!/usr/bin/env python3
"""
Test de diagnostic pour los botones de la ventana de productos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_productos_window_structure():
    """Test de la estructura de ProductosWindow"""
    print("🔍 Test de estructura de ProductosWindow...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Crear un mock de parent
        parent = Mock()
        parent.winfo_exists.return_value = True
        
        # Intentar crear la ventana (sin GUI real)
        with Mock() as mock_toplevel:
            # Mock de CTkToplevel para evitar crear ventana real
            import customtkinter as ctk
            original_toplevel = ctk.CTkToplevel
            ctk.CTkToplevel = Mock(return_value=Mock())
            
            try:
                window = ProductosWindow(parent)
                
                # Verificar que los métodos existen
                assert hasattr(window, 'guardar_producto'), "Método guardar_producto no existe"
                assert hasattr(window, 'seleccionar_imagen'), "Método seleccionar_imagen no existe"
                assert callable(window.guardar_producto), "guardar_producto no es callable"
                assert callable(window.seleccionar_imagen), "seleccionar_imagen no es callable"
                
                print("✅ Métodos de botones existen y son callable")
                
                # Verificar variables de instancia
                assert hasattr(window, 'window'), "Atributo window no existe"
                assert hasattr(window, 'logger'), "Atributo logger no existe"
                assert hasattr(window, 'imagen_path'), "Atributo imagen_path no existe"
                
                print("✅ Atributos de instancia existen")
                
                return True
                
            finally:
                # Restaurar CTkToplevel original
                ctk.CTkToplevel = original_toplevel
        
    except Exception as e:
        print(f"❌ Error en test de estructura: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_methods_directly():
    """Test directo de los métodos de botones"""
    print("\n🔍 Test directo de métodos de botones...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        
        # Crear una instancia mock
        instance = Mock(spec=ProductosWindow)
        instance.logger = Mock()
        instance.imagen_path = ""
        instance.selected_producto = None
        
        # Mock de widgets necesarios
        instance.nombre_entry = Mock()
        instance.referencia_entry = Mock()
        instance.precio_entry = Mock()
        instance.categoria_entry = Mock()
        instance.iva_entry = Mock()
        instance.descripcion_text = Mock()
        instance.imagen_label = Mock()
        instance.update_image_display = Mock()
        
        # Configurar valores de retorno
        instance.nombre_entry.get.return_value = "Test Producto"
        instance.referencia_entry.get.return_value = "TEST-001"
        instance.precio_entry.get.return_value = "10.50"
        instance.categoria_entry.get.return_value = "Test"
        instance.iva_entry.get.return_value = "21.0"
        instance.descripcion_text.get.return_value = "Descripción test"
        
        # Test del método guardar_producto
        print("   🔧 Probando método guardar_producto...")
        with patch('tkinter.messagebox.showinfo'), \
             patch('tkinter.messagebox.showerror'), \
             patch.object(ProductosWindow, 'validate_form', return_value=[]), \
             patch.object(ProductosWindow, 'load_productos'), \
             patch.object(ProductosWindow, 'limpiar_formulario'):
            
            try:
                ProductosWindow.guardar_producto(instance)
                print("   ✅ Método guardar_producto ejecutado sin errores")
            except Exception as e:
                print(f"   ❌ Error en guardar_producto: {e}")
        
        # Test del método seleccionar_imagen
        print("   🔧 Probando método seleccionar_imagen...")
        with patch('tkinter.filedialog.askopenfilename', return_value=""):
            try:
                ProductosWindow.seleccionar_imagen(instance)
                print("   ✅ Método seleccionar_imagen ejecutado sin errores")
            except Exception as e:
                print(f"   ❌ Error en seleccionar_imagen: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de métodos: {e}")
        return False

def test_logging_in_methods():
    """Test de logging en los métodos"""
    print("\n🔍 Test de logging en métodos...")
    
    try:
        from utils.logger import get_logger
        
        # Verificar que el logger funciona
        logger = get_logger("productos")
        logger.info("Test de logging en productos")
        
        print("✅ Logger de productos funciona")
        
        # Verificar imports de logging
        from utils.logger import log_user_action, log_file_operation, log_exception
        
        log_user_action("Test acción", "Test detalles")
        log_file_operation("TEST", "/test/file", "Test operación")
        
        print("✅ Funciones de logging específicas funcionan")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de logging: {e}")
        return False

def test_translations():
    """Test de traducciones necesarias"""
    print("\n🔍 Test de traducciones...")
    
    try:
        from utils.translations import get_text
        
        # Verificar traducciones necesarias
        required_translations = [
            "guardar",
            "seleccionar_imagen",
            "gestion_productos",
            "error",
            "confirmar"
        ]
        
        for key in required_translations:
            value = get_text(key)
            assert value != key, f"Traducción faltante para {key}"
            print(f"   ✅ {key}: '{value}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de traducciones: {e}")
        return False

def test_imports():
    """Test de imports necesarios"""
    print("\n🔍 Test de imports...")
    
    try:
        # Test de imports principales
        import customtkinter as ctk
        print("✅ customtkinter importado")
        
        import tkinter as tk
        from tkinter import filedialog, messagebox
        print("✅ tkinter y componentes importados")
        
        from utils.translations import get_text
        print("✅ translations importado")
        
        from utils.config import app_config
        print("✅ config importado")
        
        from utils.logger import get_logger
        print("✅ logger importado")
        
        from database.models import Producto
        print("✅ models importado")
        
        from PIL import Image, ImageTk
        print("✅ PIL importado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Test de Diagnóstico - Botones de Productos")
    print("=" * 60)
    
    tests = [
        ("Imports necesarios", test_imports),
        ("Traducciones", test_translations),
        ("Logging en métodos", test_logging_in_methods),
        ("Estructura de ProductosWindow", test_productos_window_structure),
        ("Métodos de botones", test_button_methods_directly)
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
        print("🎉 ¡DIAGNÓSTICO EXITOSO!")
        print("\n📋 Los botones deberían funcionar correctamente.")
        print("Si aún hay problemas, puede ser un issue de GUI en el entorno.")
    else:
        print("⚠️  PROBLEMAS DETECTADOS!")
        print("Revisa los errores arriba para identificar el problema.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
