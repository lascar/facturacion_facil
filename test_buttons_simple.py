#!/usr/bin/env python3
"""
Test simple para verificar que los botones funcionan
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_methods_exist():
    """Test simple para verificar que los métodos de botones existen"""
    print("🔍 Verificando métodos de botones...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Verificar que los métodos existen
        assert hasattr(ProductosWindow, 'guardar_producto'), "Método guardar_producto no existe"
        assert hasattr(ProductosWindow, 'seleccionar_imagen'), "Método seleccionar_imagen no existe"
        
        # Verificar que son callable
        assert callable(ProductosWindow.guardar_producto), "guardar_producto no es callable"
        assert callable(ProductosWindow.seleccionar_imagen), "seleccionar_imagen no es callable"
        
        print("✅ Métodos de botones existen y son callable")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_translations_for_buttons():
    """Test de traducciones para botones"""
    print("\n🔍 Verificando traducciones de botones...")
    
    try:
        from utils.translations import get_text
        
        # Traducciones necesarias para botones
        button_translations = {
            "guardar": "Guardar",
            "seleccionar_imagen": "Seleccionar Imagen",
            "nuevo_producto": "Nuevo Producto",
            "cancelar": "Cancelar"
        }
        
        for key, expected in button_translations.items():
            value = get_text(key)
            print(f"   {key}: '{value}'")
            assert value == expected, f"Traducción incorrecta para {key}: esperado '{expected}', obtenido '{value}'"
        
        print("✅ Traducciones de botones correctas")
        return True
        
    except Exception as e:
        print(f"❌ Error en traducciones: {e}")
        return False

def test_logging_setup():
    """Test de configuración de logging"""
    print("\n🔍 Verificando configuración de logging...")
    
    try:
        from utils.logger import get_logger, log_user_action
        
        # Test de logger específico
        logger = get_logger("productos")
        logger.info("Test de logging para productos")
        
        # Test de función específica
        log_user_action("Test acción", "Test detalles")
        
        print("✅ Logging configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en logging: {e}")
        return False

def test_config_system():
    """Test del sistema de configuración"""
    print("\n🔍 Verificando sistema de configuración...")
    
    try:
        from utils.config import app_config
        
        # Test de métodos de configuración
        default_dir = app_config.get_default_image_directory()
        formats = app_config.get_supported_formats()
        display_size = app_config.get_image_display_size()
        
        print(f"   Directorio por defecto: {default_dir}")
        print(f"   Formatos soportados: {formats}")
        print(f"   Tamaño de display: {display_size}")
        
        assert isinstance(default_dir, str), "Directorio por defecto debe ser string"
        assert isinstance(formats, list), "Formatos debe ser lista"
        assert isinstance(display_size, tuple), "Display size debe ser tupla"
        
        print("✅ Sistema de configuración funciona")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_database_models():
    """Test de modelos de base de datos"""
    print("\n🔍 Verificando modelos de base de datos...")
    
    try:
        from database.models import Producto
        
        # Verificar que la clase existe y tiene métodos necesarios
        assert hasattr(Producto, 'save'), "Método save no existe en Producto"
        assert hasattr(Producto, 'get_all'), "Método get_all no existe en Producto"
        
        print("✅ Modelos de base de datos disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def simulate_button_clicks():
    """Simula clics en botones para verificar logging"""
    print("\n🔍 Simulando clics en botones...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        
        # Crear instancia mock
        instance = Mock()
        instance.logger = Mock()
        instance.imagen_path = ""
        
        # Mock de widgets necesarios para guardar_producto
        instance.nombre_entry = Mock()
        instance.referencia_entry = Mock()
        instance.precio_entry = Mock()
        instance.categoria_entry = Mock()
        instance.iva_entry = Mock()
        instance.descripcion_text = Mock()
        
        # Configurar valores válidos
        instance.nombre_entry.get.return_value = "Producto Test"
        instance.referencia_entry.get.return_value = "TEST-001"
        instance.precio_entry.get.return_value = "10.50"
        instance.categoria_entry.get.return_value = "Test"
        instance.iva_entry.get.return_value = "21.0"
        instance.descripcion_text.get.return_value = "Descripción test"
        
        # Simular clic en seleccionar imagen
        print("   🖱️  Simulando clic en 'Seleccionar Imagen'...")
        with patch('tkinter.filedialog.askopenfilename', return_value=""):
            ProductosWindow.seleccionar_imagen(instance)
        print("   ✅ Clic en seleccionar imagen simulado")
        
        # Simular clic en guardar (con mocks adicionales)
        print("   🖱️  Simulando clic en 'Guardar'...")
        with patch.object(ProductosWindow, 'validate_form', return_value=[]), \
             patch('tkinter.messagebox.showinfo'), \
             patch.object(ProductosWindow, 'load_productos'), \
             patch.object(ProductosWindow, 'limpiar_formulario'):
            
            ProductosWindow.guardar_producto(instance)
        print("   ✅ Clic en guardar simulado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🧪 Test Simple de Botones de Productos")
    print("=" * 50)
    
    tests = [
        ("Métodos de botones", test_button_methods_exist),
        ("Traducciones", test_translations_for_buttons),
        ("Configuración de logging", test_logging_setup),
        ("Sistema de configuración", test_config_system),
        ("Modelos de base de datos", test_database_models),
        ("Simulación de clics", simulate_button_clicks)
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
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("\n📋 Los botones deberían funcionar correctamente:")
        print("   1. ✅ Métodos de botones existen")
        print("   2. ✅ Traducciones correctas")
        print("   3. ✅ Logging configurado")
        print("   4. ✅ Configuración disponible")
        print("   5. ✅ Modelos de DB disponibles")
        print("   6. ✅ Simulación exitosa")
        print("\n🔍 Si los botones no funcionan en la GUI, puede ser un problema de entorno.")
        print("📁 Revisa los logs en el directorio 'logs/' para más detalles.")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON!")
        print("Esto puede explicar por qué los botones no funcionan.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
