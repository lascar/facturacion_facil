#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier que les produits apparaissent dans le dialog de création de facture
"""

import sys
import os
sys.path.append('.')

# Configurer PyQt5
os.environ['QT_API'] = 'pyqt5'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import CrearFacturaDialog
from database.database import Database
from utils.logger import get_logger
import tempfile
import shutil

def test_productos_en_crear_factura():
    """Test simple pour vérifier les produits dans le dialog - AVEC BASE DE DONNÉES DE TEST"""
    logger = get_logger("test_crear_factura")

    print("🧪 TEST: Productos en Dialog Crear Factura")
    print("=" * 45)
    print("⚠️  USANDO BASE DE DATOS DE TEST (NO PRODUCCIÓN)")
    print()

    # Créer une base de données temporaire pour le test
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_facturacion.db')

    # Sauvegarder la configuration originale
    original_db_path = None
    if hasattr(Database, '_db_path'):
        original_db_path = Database._db_path

    try:
        # Configurer la base de données de test
        Database._db_path = test_db_path

        print(f"📁 Base de datos de test: {test_db_path}")
        print("📦 Creando productos de test...")

        # Créer la base de données de test avec des produits
        db = Database()

        # Ajouter des produits de test
        productos_test = [
            {
                'nombre': 'Producto Test 1',
                'referencia': 'TEST-001',
                'precio_venta': 25.50,
                'precio_compra': 15.00,
                'categoria': 'Test',
                'descripcion': 'Producto para test de interfaz',
                'iva_recomendado': 21.0,
                'stock_actual': 10,
                'stock_minimo': 2
            },
            {
                'nombre': 'Producto Test 2',
                'referencia': 'TEST-002',
                'precio_venta': 45.75,
                'precio_compra': 30.00,
                'categoria': 'Test',
                'descripcion': 'Segundo producto para test',
                'iva_recomendado': 10.0,
                'stock_actual': 5,
                'stock_minimo': 1
            }
        ]

        for producto_data in productos_test:
            result = db.add_product(producto_data)
            if result:
                print(f"  ✅ Agregado: {producto_data['nombre']}")
            else:
                print(f"  ❌ Error agregando: {producto_data['nombre']}")

        # Verificar productos creados
        productos = db.get_all_products()
        print(f"✅ Productos de test creados: {len(productos)}")

        if productos:
            for i, producto in enumerate(productos, 1):
                print(f"  {i}. {producto['nombre']} - {producto['precio_venta']:.2f}€ (Stock: {producto['stock_actual']})")

        print()
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        print("🎯 Creando dialog de crear factura...")
        dialog = CrearFacturaDialog()
        
        # Variable pour stocker le résultat
        test_result = {"success": False, "message": ""}
        
        def verificar_combo():
            """Vérifier le contenu du combo après chargement"""
            try:
                print(f"📋 Items en combo: {dialog.producto_combo.count()}")
                
                if dialog.producto_combo.count() == 0:
                    test_result["message"] = "❌ ERROR: Combo vacío"
                    app.quit()
                    return
                
                print("📝 Contenido del combo:")
                for i in range(dialog.producto_combo.count()):
                    texto = dialog.producto_combo.itemText(i)
                    data = dialog.producto_combo.itemData(i)
                    print(f"  {i}: {texto}")
                    
                    if data and isinstance(data, dict):
                        print(f"      → ID: {data.get('id')}, Precio: {data.get('precio_venta')}")
                
                if dialog.producto_combo.count() > 1:
                    test_result["success"] = True
                    test_result["message"] = "✅ ÉXITO: Productos aparecen correctamente"
                else:
                    test_result["message"] = "⚠️  ADVERTENCIA: Solo hay item 'Seleccionar producto...'"
                
                # Cerrar después de verificar
                QTimer.singleShot(500, app.quit)
                
            except Exception as e:
                test_result["message"] = f"❌ ERROR en verificación: {e}"
                app.quit()
        
        # Verificar después de que se carguen los datos
        QTimer.singleShot(1000, verificar_combo)
        
        # Mostrar el dialog
        dialog.show()
        
        # Ejecutar por tiempo limitado
        QTimer.singleShot(3000, app.quit)  # Timeout de seguridad
        
        print("🚀 Mostrando dialog (se cerrará automáticamente)...")
        app.exec_()
        
        print()
        print("=" * 45)
        print(test_result["message"])
        
        return test_result["success"]

    except Exception as e:
        logger.error(f"Error en test: {e}")
        print(f"❌ ERROR: {e}")
        return False

    finally:
        # Restaurer la configuration originale
        if original_db_path:
            Database._db_path = original_db_path

        # Nettoyer la base de données temporaire
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"🧹 Base de datos de test eliminada: {temp_dir}")
        except Exception as e:
            print(f"⚠️  Error limpiando test DB: {e}")

def main():
    """Función principal"""
    print("🚀 TEST SIMPLE - PRODUCTOS EN CREAR FACTURA")
    print("=" * 50)
    print()
    
    success = test_productos_en_crear_factura()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 TEST EXITOSO")
        print()
        print("✅ Los productos aparecen correctamente en el dialog")
        print("💡 La corrección de 'precio_venta' funciona")
        print()
        print("🎯 PRÓXIMOS PASOS:")
        print("   1. Ejecute la aplicación: python main.py")
        print("   2. Vaya a Gestión de Facturas → Crear Nueva Factura")
        print("   3. Verifique que puede seleccionar productos")
        print("   4. Agregue productos a la factura")
    else:
        print("❌ TEST FALLÓ")
        print()
        print("🔧 POSIBLES SOLUCIONES:")
        print("   1. Verifique que hay productos en la base de datos")
        print("   2. Verifique que PyQt5 está instalado")
        print("   3. Revise los logs para más detalles")
        print("   4. Ejecute: python test_productos_factura.py")
    
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
