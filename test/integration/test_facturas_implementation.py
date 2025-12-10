#!/usr/bin/env python3
"""
Test para verificar la implementación del módulo de facturas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test que todos los imports funcionan correctamente"""
    print("🧪 Test: Imports del módulo de facturas")
    
    try:
        # Test imports básicos
        from database.models import Factura, FacturaItem
        print("   ✅ Modelos de factura importados")
        
        from common.validators import FormValidator, CalculationHelper
        print("   ✅ Validadores comunes importados")
        
        from common.ui_components import BaseWindow, ImageSelector, FormHelper
        print("   ✅ Componentes UI comunes importados")
        
        from ui.facturas_pyqt5 import FacturasPyQt5Window as FacturasWindow
        print("   ✅ Ventana de facturas importada")
        
        from ui.facturas_methods import FacturasMethodsMixin
        print("   ✅ Métodos de facturas importados")
        
        # ProductoFacturaDialog supprimé (CustomTkinter, pas PyQt5)
        print("   ✅ Imports PyQt5 validés")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        return False

def test_database_tables():
    """Test que las tablas de base de datos existen"""
    print("\n🧪 Test: Tablas de base de datos")
    
    try:
        from database.database import db
        
        # Verificar que las tablas existen
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = db.execute_query(tables_query)
        table_names = [table[0] for table in tables]
        
        required_tables = ['facturas', 'factura_items', 'productos', 'organizacion', 'stock']
        
        for table in required_tables:
            if table in table_names:
                print(f"   ✅ Tabla '{table}' existe")
            else:
                print(f"   ❌ Tabla '{table}' NO existe")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error al verificar tablas: {e}")
        return False

def test_factura_model():
    """Test del modelo Factura"""
    print("\n🧪 Test: Modelo Factura")
    
    try:
        from database.models import Factura
        
        # Test crear factura
        factura = Factura(
            numero_factura="TEST-001",
            fecha_factura="2025-01-01",
            nombre_cliente="Cliente Test",
            subtotal=100.0,
            total_iva=21.0,
            total_factura=121.0
        )
        
        print("   ✅ Factura creada correctamente")
        
        # Test métodos estáticos
        next_numero = Factura.get_next_numero()
        print(f"   ✅ Siguiente número de factura: {next_numero}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en modelo Factura: {e}")
        return False

def test_validators():
    """Test de validadores comunes"""
    print("\n🧪 Test: Validadores comunes")
    
    try:
        from common.validators import FormValidator, CalculationHelper
        
        # Test validaciones
        error = FormValidator.validate_precio("10.50")
        if error is None:
            print("   ✅ Validación de precio correcta")
        else:
            print(f"   ❌ Error en validación de precio: {error}")
            return False
        
        error = FormValidator.validate_cantidad("5")
        if error is None:
            print("   ✅ Validación de cantidad correcta")
        else:
            print(f"   ❌ Error en validación de cantidad: {error}")
            return False
        
        # Test cálculos
        result = CalculationHelper.calculate_line_total(10.0, 2, 21.0, 0)
        expected_total = 24.2  # (10 * 2) * 1.21
        if abs(result['total'] - expected_total) < 0.01:
            print("   ✅ Cálculo de línea correcto")
        else:
            print(f"   ❌ Error en cálculo: esperado {expected_total}, obtenido {result['total']}")
            return False
        
        # Test formateo
        formatted = CalculationHelper.format_currency(123.45)
        if "123.45" in formatted and "€" in formatted:
            print("   ✅ Formateo de moneda correcto")
        else:
            print(f"   ❌ Error en formateo: {formatted}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en validadores: {e}")
        return False

def test_translations():
    """Test de traducciones"""
    print("\n🧪 Test: Traducciones")
    
    try:
        from utils.translations import get_text
        
        # Test traducciones clave
        key_translations = [
            "facturas", "nueva_factura", "numero_factura", "fecha_factura",
            "nombre_cliente", "subtotal", "total_iva", "total_factura",
            "guardar", "cancelar", "agregar_producto"
        ]
        
        missing_translations = []
        for key in key_translations:
            text = get_text(key)
            if text == key:  # Si devuelve la clave, no está traducido
                missing_translations.append(key)
            else:
                print(f"   ✅ '{key}' -> '{text}'")
        
        if missing_translations:
            print(f"   ⚠️  Traducciones faltantes: {missing_translations}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en traducciones: {e}")
        return False

def test_ui_components():
    """Test de componentes UI (sin crear ventanas)"""
    print("\n🧪 Test: Componentes UI")
    
    try:
        from common.ui_components import FormHelper
        
        # Test FormHelper (métodos estáticos)
        print("   ✅ FormHelper disponible")
        
        # Test que las clases se pueden importar
        from ui.facturas_pyqt5 import FacturasPyQt5Window as FacturasWindow
        # ProductoFacturaDialog supprimé (CustomTkinter, pas PyQt5)

        print("   ✅ Clases UI PyQt5 importadas correctamente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en componentes UI: {e}")
        return False

def main():
    """Función principal de test"""
    print("🎯 Test de implementación del módulo de facturas")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_tables,
        test_factura_model,
        test_validators,
        test_translations,
        test_ui_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("   ⚠️  Test falló")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("✅ TODOS LOS TESTS PASARON - El módulo de facturas está listo!")
        print("\n💡 Para probar la interfaz:")
        print("   1. Ejecute: python main.py")
        print("   2. Haga clic en 'Facturas'")
        print("   3. Pruebe crear una nueva factura")
        return True
    else:
        print("❌ ALGUNOS TESTS FALLARON - Revise los errores arriba")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
