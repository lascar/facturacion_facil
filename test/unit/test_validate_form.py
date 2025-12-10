#!/usr/bin/env python3
"""
Test específico para validate_form
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_validate_form_directly():
    """Test directo de validate_form"""
    print("🔍 Test directo de validate_form...")
    
    try:
        from ui.productos_pyqt5 import ProductosPyQt5Window as ProductosWindow
        from unittest.mock import Mock
        
        # Crear instancia mock
        instance = Mock()
        instance.logger = Mock()
        
        # Mock de widgets con valores válidos
        instance.nombre_entry = Mock()
        instance.referencia_entry = Mock()
        instance.precio_entry = Mock()
        instance.iva_entry = Mock()
        
        # Configurar valores válidos
        instance.nombre_entry.get.return_value = "Producto Test"
        instance.referencia_entry.get.return_value = "TEST-001"
        instance.precio_entry.get.return_value = "10.50"
        instance.iva_entry.get.return_value = "21.0"
        
        # Llamar validate_form
        result = ProductosWindow.validate_form(instance)
        
        print(f"   Resultado: {result}")
        print(f"   Tipo: {type(result)}")
        print(f"   Es lista: {isinstance(result, list)}")
        
        # Verificar que es una lista
        assert isinstance(result, list), f"validate_form debe retornar lista, retornó {type(result)}"
        
        # Con valores válidos, no debería haber errores
        assert len(result) == 0, f"Con valores válidos no debería haber errores, pero hay: {result}"
        
        print("✅ validate_form con valores válidos funciona")
        
        # Test con valores inválidos
        instance.nombre_entry.get.return_value = ""  # Nombre vacío
        instance.precio_entry.get.return_value = "abc"  # Precio inválido
        
        result_invalid = ProductosWindow.validate_form(instance)
        
        print(f"   Resultado con errores: {result_invalid}")
        print(f"   Tipo: {type(result_invalid)}")
        print(f"   Cantidad de errores: {len(result_invalid) if isinstance(result_invalid, list) else 'No es lista'}")
        
        assert isinstance(result_invalid, list), f"validate_form debe retornar lista, retornó {type(result_invalid)}"
        assert len(result_invalid) > 0, "Con valores inválidos debería haber errores"
        
        print("✅ validate_form con valores inválidos funciona")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de validate_form: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_translations_used_in_validate():
    """Test de traducciones usadas en validate_form"""
    print("\n🔍 Test de traducciones en validate_form...")
    
    try:
        from utils.translations import get_text
        
        # Traducciones usadas en validate_form
        translations_needed = [
            "nombre",
            "referencia", 
            "campo_requerido",
            "precio_invalido",
            "iva_invalido"
        ]
        
        for key in translations_needed:
            value = get_text(key)
            print(f"   {key}: '{value}' (tipo: {type(value)})")
            
            # Verificar que no es None
            assert value is not None, f"Traducción {key} es None"
            assert isinstance(value, str), f"Traducción {key} no es string: {type(value)}"
            assert len(value) > 0, f"Traducción {key} está vacía"
        
        print("✅ Todas las traducciones necesarias existen")
        return True
        
    except Exception as e:
        print(f"❌ Error en traducciones: {e}")
        return False

def test_join_operation():
    """Test específico de la operación join"""
    print("\n🔍 Test de operación join...")
    
    try:
        # Test con lista normal
        errors_list = ["Error 1", "Error 2", "Error 3"]
        result = "\n".join(errors_list)
        print(f"   Join con lista: '{result}'")
        
        # Test con lista vacía
        empty_list = []
        result_empty = "\n".join(empty_list)
        print(f"   Join con lista vacía: '{result_empty}'")
        
        # Test con diferentes tipos que podrían causar problemas
        problematic_values = [
            None,
            "string simple",
            123,
            ["lista", "dentro", "de", "lista"]
        ]
        
        for value in problematic_values:
            try:
                if value is None:
                    print(f"   Probando join con None: Error esperado")
                    "\n".join(value)
                elif isinstance(value, str):
                    print(f"   Probando join con string: Error esperado")
                    "\n".join(value)  # Esto debería funcionar (itera caracteres)
                elif isinstance(value, int):
                    print(f"   Probando join con int: Error esperado")
                    "\n".join(value)
                elif isinstance(value, list):
                    result = "\n".join(value)
                    print(f"   Join con lista anidada: '{result}'")
            except Exception as e:
                print(f"   Error con {type(value)}: {e}")
        
        print("✅ Test de join completado")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de join: {e}")
        return False

def test_mock_behavior():
    """Test del comportamiento de Mock"""
    print("\n🔍 Test de comportamiento de Mock...")
    
    try:
        from unittest.mock import Mock
        
        # Crear mock como en el test que falla
        instance = Mock()
        instance.logger = Mock()
        
        # Mock de widgets
        instance.nombre_entry = Mock()
        instance.referencia_entry = Mock()
        instance.precio_entry = Mock()
        instance.iva_entry = Mock()
        
        # Configurar valores
        instance.nombre_entry.get.return_value = "Test"
        instance.referencia_entry.get.return_value = "TEST-001"
        instance.precio_entry.get.return_value = "10.50"
        instance.iva_entry.get.return_value = "21.0"
        
        # Verificar que los mocks funcionan
        print(f"   nombre_entry.get(): '{instance.nombre_entry.get()}'")
        print(f"   referencia_entry.get(): '{instance.referencia_entry.get()}'")
        print(f"   precio_entry.get(): '{instance.precio_entry.get()}'")
        print(f"   iva_entry.get(): '{instance.iva_entry.get()}'")
        
        # Verificar strip()
        print(f"   nombre_entry.get().strip(): '{instance.nombre_entry.get().strip()}'")
        
        print("✅ Mocks funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de mocks: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Test Específico de validate_form")
    print("=" * 50)
    
    tests = [
        ("Traducciones en validate_form", test_translations_used_in_validate),
        ("Operación join", test_join_operation),
        ("Comportamiento de Mock", test_mock_behavior),
        ("validate_form directo", test_validate_form_directly)
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
        print("🎉 ¡VALIDATE_FORM FUNCIONA CORRECTAMENTE!")
        print("El problema debe estar en otro lugar.")
    else:
        print("⚠️  PROBLEMAS EN VALIDATE_FORM DETECTADOS!")
        print("Esto explica el error en guardar_producto.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
