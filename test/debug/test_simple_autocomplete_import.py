#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de importación del autocompletado
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_import_simple_autocomplete():
    """Test de importación del autocompletado simple"""
    try:
        print("🔧 Probando importación de SimpleProductoAutocomplete...")
        from common.simple_producto_autocomplete import SimpleProductoAutocomplete
        print("✅ SimpleProductoAutocomplete importado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en importación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_dialog():
    """Test de importación del diálogo modificado"""
    try:
        print("🔧 Probando importación del diálogo modificado...")
        # Solo importar, no crear instancia
        import ui.producto_factura_dialog
        print("✅ Diálogo modificado importado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en importación del diálogo: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test básico de funcionalidad sin UI"""
    try:
        print("🔧 Probando funcionalidad básica...")
        
        # Simular datos de productos
        from database.models import Producto
        
        # Verificar que podemos crear un producto
        producto_test = Producto(
            nombre="Test Simple Autocomplete",
            referencia="TESTSAC001",
            precio=50.0,
            iva_recomendado=21.0
        )
        
        print(f"   Producto de test: {producto_test.nombre}")
        print("✅ Funcionalidad básica correcta")
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 Test de importación del autocompletado simple")
    print("=" * 60)
    
    success1 = test_import_simple_autocomplete()
    success2 = test_import_dialog()
    success3 = test_basic_functionality()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Importación autocompletado: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Importación diálogo: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"   Funcionalidad básica: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if success1 and success2 and success3:
        print("\n🎉 TODOS LOS TESTS DE IMPORTACIÓN PASARON")
        print("El autocompletado simple está listo para usar.")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Probar el diálogo de producto en la aplicación")
        print("   2. Verificar que el autocompletado funciona correctamente")
        print("   3. Ajustar la interfaz si es necesario")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("Revisar los errores mostrados arriba.")

if __name__ == "__main__":
    main()
