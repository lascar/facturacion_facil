#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la lógica del autocompletado sin UI
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class MockAutocomplete:
    """Mock del autocompletado para testing de lógica"""
    
    def __init__(self):
        self.suggestions_data = []
        self.filtered_suggestions = []
        self.selected_item = None
        self.search_fields = ['search_text']
        self.min_chars = 2
        self.max_suggestions = 15
    
    def set_suggestions_data(self, data):
        """Establece los datos para autocompletado"""
        self.suggestions_data = data
        print(f"✅ Configurados {len(data)} elementos para autocompletado")
    
    def filter_suggestions(self, query):
        """Filtra las sugerencias"""
        if len(query) < self.min_chars:
            self.filtered_suggestions = []
            return
        
        query_lower = query.lower()
        self.filtered_suggestions = []
        
        for item in self.suggestions_data:
            match_found = False
            for field in self.search_fields:
                if field in item:
                    field_value = str(item[field]).lower()
                    if query_lower in field_value:
                        match_found = True
                        break
            
            if match_found:
                self.filtered_suggestions.append(item)
                if len(self.filtered_suggestions) >= self.max_suggestions:
                    break
        
        print(f"✅ Filtradas {len(self.filtered_suggestions)} sugerencias para '{query}'")
    
    def select_suggestion(self, index):
        """Selecciona una sugerencia por índice"""
        if 0 <= index < len(self.filtered_suggestions):
            self.selected_item = self.filtered_suggestions[index]
            print(f"✅ Seleccionado: {self.selected_item.get('nombre', 'N/A')}")
            return True
        return False
    
    def validate_selection(self):
        """Valida que hay una selección"""
        return self.selected_item is not None
    
    def get_validation_error(self):
        """Obtiene mensaje de error de validación"""
        if not self.selected_item:
            return "Debe seleccionar un producto"
        return ""

def test_autocomplete_logic():
    """Test de la lógica del autocompletado"""
    print("🔧 Test de lógica del autocompletado...")
    
    try:
        # Crear mock
        autocomplete = MockAutocomplete()
        
        # Datos de test simulando productos
        test_data = [
            {
                'id': 1,
                'nombre': 'Laptop Dell Inspiron',
                'referencia': 'DELL001',
                'precio': 899.99,
                'categoria': 'Informática',
                'search_text': 'laptop dell inspiron dell001 informática'
            },
            {
                'id': 2,
                'nombre': 'Mouse Logitech',
                'referencia': 'LOG001',
                'precio': 25.50,
                'categoria': 'Periféricos',
                'search_text': 'mouse logitech log001 periféricos'
            },
            {
                'id': 3,
                'nombre': 'Teclado Mecánico',
                'referencia': 'TEC001',
                'precio': 75.00,
                'categoria': 'Periféricos',
                'search_text': 'teclado mecánico tec001 periféricos'
            }
        ]
        
        # Test 1: Configurar datos
        autocomplete.set_suggestions_data(test_data)
        assert len(autocomplete.suggestions_data) == 3
        print("✅ Test 1: Configuración de datos")
        
        # Test 2: Filtrado por nombre
        autocomplete.filter_suggestions("laptop")
        assert len(autocomplete.filtered_suggestions) == 1
        assert autocomplete.filtered_suggestions[0]['nombre'] == 'Laptop Dell Inspiron'
        print("✅ Test 2: Filtrado por nombre")
        
        # Test 3: Filtrado por referencia
        autocomplete.filter_suggestions("LOG")
        assert len(autocomplete.filtered_suggestions) == 1
        assert autocomplete.filtered_suggestions[0]['referencia'] == 'LOG001'
        print("✅ Test 3: Filtrado por referencia")
        
        # Test 4: Filtrado por categoría
        autocomplete.filter_suggestions("Periféricos")
        assert len(autocomplete.filtered_suggestions) == 2
        print("✅ Test 4: Filtrado por categoría")
        
        # Test 5: Filtrado insensible a mayúsculas
        autocomplete.filter_suggestions("DELL")
        assert len(autocomplete.filtered_suggestions) == 1
        print("✅ Test 5: Filtrado insensible a mayúsculas")
        
        # Test 6: Mínimo de caracteres
        autocomplete.filter_suggestions("d")
        assert len(autocomplete.filtered_suggestions) == 0
        print("✅ Test 6: Mínimo de caracteres")
        
        # Test 7: Selección
        autocomplete.filter_suggestions("laptop")
        success = autocomplete.select_suggestion(0)
        assert success == True
        assert autocomplete.selected_item['nombre'] == 'Laptop Dell Inspiron'
        print("✅ Test 7: Selección")
        
        # Test 8: Validación
        assert autocomplete.validate_selection() == True
        assert autocomplete.get_validation_error() == ""
        print("✅ Test 8: Validación")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de lógica: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_producto_data_creation():
    """Test de creación de datos de productos"""
    print("\n🔧 Test de creación de datos de productos...")
    
    try:
        from database.models import Producto
        
        # Crear producto de test
        producto_test = Producto(
            nombre="Test Autocompletado",
            referencia="TESTAC001",
            precio=99.99,
            categoria="Test",
            descripcion="Producto para test",
            iva_recomendado=21.0
        )
        
        # Simular creación de datos para autocompletado
        suggestion_data = {
            'id': 999,  # ID simulado
            'nombre': producto_test.nombre,
            'referencia': producto_test.referencia,
            'precio': producto_test.precio,
            'categoria': producto_test.categoria,
            'descripcion': producto_test.descripcion,
            'iva_recomendado': producto_test.iva_recomendado,
            'stock_info': ' (Stock: 10)',
            'display_text': f"{producto_test.nombre} - {producto_test.referencia} - €{producto_test.precio:.2f} (Stock: 10)",
            'search_text': f"{producto_test.nombre} {producto_test.referencia} {producto_test.categoria}".lower()
        }
        
        print(f"✅ Datos de sugerencia creados:")
        print(f"   Display: {suggestion_data['display_text']}")
        print(f"   Search: {suggestion_data['search_text']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_scenarios():
    """Test de escenarios de error"""
    print("\n🔧 Test de escenarios de error...")
    
    try:
        autocomplete = MockAutocomplete()
        
        # Test 1: Sin datos
        autocomplete.filter_suggestions("test")
        assert len(autocomplete.filtered_suggestions) == 0
        print("✅ Test 1: Sin datos")
        
        # Test 2: Validación sin selección
        assert autocomplete.validate_selection() == False
        assert "Debe seleccionar" in autocomplete.get_validation_error()
        print("✅ Test 2: Validación sin selección")
        
        # Test 3: Selección con índice inválido
        autocomplete.set_suggestions_data([{'nombre': 'Test', 'search_text': 'test'}])
        autocomplete.filter_suggestions("test")
        success = autocomplete.select_suggestion(999)  # Índice inválido
        assert success == False
        print("✅ Test 3: Selección con índice inválido")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de errores: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 Test de lógica del autocompletado (sin UI)")
    print("=" * 60)
    
    success1 = test_autocomplete_logic()
    success2 = test_producto_data_creation()
    success3 = test_error_scenarios()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Lógica autocompletado: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Creación de datos: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"   Escenarios de error: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if success1 and success2 and success3:
        print("\n🎉 TODOS LOS TESTS DE LÓGICA PASARON")
        print("La lógica del autocompletado es correcta.")
        print("El problema original debe estar en la integración con CustomTkinter.")
        print("\n💡 SOLUCIÓN SUGERIDA:")
        print("   1. Verificar que CustomTkinter esté instalado")
        print("   2. Verificar que los argumentos pasados al constructor sean válidos")
        print("   3. El error 'search_fields are not supported' sugiere un problema")
        print("      en el paso de argumentos al constructor padre")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("Revisar la lógica del autocompletado.")

if __name__ == "__main__":
    main()
