#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para identificar el error del autocompletado
"""
import sys
import os
import traceback

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_autocomplete_basic():
    """Test básico del autocompletado"""
    print("🔧 Test básico del autocompletado...")
    
    try:
        import customtkinter as ctk
        from common.autocomplete_entry import AutocompleteEntry
        
        # Crear ventana de test
        root = ctk.CTk()
        root.withdraw()  # Ocultar
        
        # Test 1: Crear AutocompleteEntry básico
        print("1. Creando AutocompleteEntry básico...")
        autocomplete = AutocompleteEntry(root)
        print("✅ AutocompleteEntry creado correctamente")
        
        # Test 2: Configurar datos
        print("2. Configurando datos de test...")
        test_data = [
            {'text': 'Producto 1', 'id': 1},
            {'text': 'Producto 2', 'id': 2}
        ]
        autocomplete.set_suggestions_data(test_data)
        print("✅ Datos configurados correctamente")
        
        # Test 3: Filtrar sugerencias
        print("3. Probando filtrado...")
        autocomplete.filter_suggestions("Producto")
        print(f"✅ Filtrado: {len(autocomplete.filtered_suggestions)} resultados")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en test básico: {e}")
        traceback.print_exc()
        return False

def test_producto_autocomplete():
    """Test del autocompletado de productos"""
    print("\n🔧 Test del autocompletado de productos...")
    
    try:
        import customtkinter as ctk
        from common.producto_autocomplete import ProductoAutocomplete
        
        # Crear ventana de test
        root = ctk.CTk()
        root.withdraw()  # Ocultar
        
        # Test 1: Crear ProductoAutocomplete
        print("1. Creando ProductoAutocomplete...")
        producto_autocomplete = ProductoAutocomplete(root)
        print("✅ ProductoAutocomplete creado correctamente")
        
        # Test 2: Verificar datos cargados
        print("2. Verificando datos cargados...")
        print(f"   Productos cargados: {len(producto_autocomplete.suggestions_data)}")
        
        if len(producto_autocomplete.suggestions_data) > 0:
            primer_producto = producto_autocomplete.suggestions_data[0]
            print(f"   Primer producto: {primer_producto.get('nombre', 'N/A')}")
            print("✅ Datos cargados correctamente")
        else:
            print("⚠️ No hay productos en la base de datos")
        
        # Test 3: Probar filtrado
        print("3. Probando filtrado...")
        producto_autocomplete.filter_suggestions("test")
        print(f"✅ Filtrado completado: {len(producto_autocomplete.filtered_suggestions)} resultados")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en test de productos: {e}")
        traceback.print_exc()
        return False

def test_dialog_integration():
    """Test de integración con el diálogo"""
    print("\n🔧 Test de integración con diálogo...")
    
    try:
        import customtkinter as ctk
        from ui.producto_factura_dialog import ProductoFacturaDialog
        from database.models import Producto
        
        # Crear ventana de test
        root = ctk.CTk()
        root.withdraw()  # Ocultar
        
        # Crear productos de test si no existen
        productos = Producto.get_all()
        if len(productos) == 0:
            print("   Creando producto de test...")
            producto_test = Producto(
                nombre="Producto Test",
                referencia="TEST001",
                precio=10.0,
                iva_recomendado=21.0
            )
            producto_test.save()
            print("✅ Producto de test creado")
        
        # Test 1: Crear diálogo
        print("1. Creando diálogo de producto...")
        dialog = ProductoFacturaDialog(root)
        print("✅ Diálogo creado correctamente")
        
        # Test 2: Verificar autocompletado en el diálogo
        print("2. Verificando autocompletado en diálogo...")
        if hasattr(dialog, 'producto_autocomplete'):
            print("✅ Autocompletado encontrado en diálogo")
            autocomplete = dialog.producto_autocomplete
            print(f"   Productos disponibles: {len(autocomplete.suggestions_data)}")
        else:
            print("❌ Autocompletado no encontrado en diálogo")
            return False
        
        # Cerrar diálogo
        if hasattr(dialog, 'dialog') and dialog.dialog.winfo_exists():
            dialog.dialog.destroy()
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en test de integración: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal de debug"""
    print("🚀 Iniciando debug del sistema de autocompletado...")
    print("=" * 60)
    
    # Test 1: Autocompletado básico
    success1 = test_autocomplete_basic()
    
    # Test 2: Autocompletado de productos
    success2 = test_producto_autocomplete()
    
    # Test 3: Integración con diálogo
    success3 = test_dialog_integration()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS:")
    print(f"   Autocompletado básico: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Autocompletado productos: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"   Integración diálogo: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if success1 and success2 and success3:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("El sistema de autocompletado está funcionando correctamente.")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("Revisar los errores mostrados arriba.")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    main()
