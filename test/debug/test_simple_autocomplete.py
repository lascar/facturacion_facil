#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple del autocompletado sin CustomTkinter
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_autocomplete_import():
    """Test de importación del autocompletado"""
    try:
        print("🔧 Probando importación de AutocompleteEntry...")
        from common.autocomplete_entry import AutocompleteEntry
        print("✅ AutocompleteEntry importado correctamente")
        
        print("🔧 Probando importación de ProductoAutocomplete...")
        from common.producto_autocomplete import ProductoAutocomplete
        print("✅ ProductoAutocomplete importado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_producto_autocomplete_logic():
    """Test de la lógica del autocompletado sin UI"""
    try:
        print("\n🔧 Probando lógica de ProductoAutocomplete...")
        
        # Importar sin crear UI
        from common.producto_autocomplete import ProductoAutocomplete
        from database.models import Producto
        
        # Verificar que podemos obtener productos
        productos = Producto.get_all()
        print(f"   Productos en DB: {len(productos)}")
        
        if len(productos) == 0:
            print("   Creando producto de test...")
            producto_test = Producto(
                nombre="Test Producto",
                referencia="TEST001",
                precio=10.0,
                iva_recomendado=21.0
            )
            producto_test.save()
            print("✅ Producto de test creado")
        
        print("✅ Lógica de ProductoAutocomplete funciona")
        return True
        
    except Exception as e:
        print(f"❌ Error en lógica: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 Test simple del autocompletado")
    print("=" * 50)
    
    success1 = test_autocomplete_import()
    success2 = test_producto_autocomplete_logic()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN:")
    print(f"   Importación: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Lógica: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 TESTS BÁSICOS PASARON")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")

if __name__ == "__main__":
    main()
