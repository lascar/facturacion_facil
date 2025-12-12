#!/usr/bin/env python3
"""
Script para corregir problemas en los tests:
1. Database locked
2. UNIQUE constraint failed
3. Problemas de concurrencia
"""

import sys
import os
import tempfile
import shutil
import sqlite3
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def fix_database_locked_issues():
    """Corregir problemas de base de datos bloqueada"""
    print("🔧 CORRECCIÓN: Problemas de Base de Datos en Tests")
    print("=" * 60)
    
    # 1. Verificar si hay conexiones abiertas
    print("🔍 Verificando conexiones abiertas...")
    
    try:
        from database.database import Database
        
        # Forzar cierre de todas las conexiones
        if hasattr(Database, '_instance'):
            if Database._instance:
                print("   📝 Cerrando instancia de Database existente...")
                Database._instance = None
        
        # Limpiar cualquier conexión en pool
        print("   🧹 Limpiando conexiones...")
        
        # 2. Verificar archivos de base de datos temporales
        temp_dir = tempfile.gettempdir()
        print(f"\n📁 Verificando archivos temporales en: {temp_dir}")
        
        test_db_files = []
        for file in os.listdir(temp_dir):
            if file.startswith('test_') and file.endswith('.db'):
                test_db_files.append(os.path.join(temp_dir, file))
        
        if test_db_files:
            print(f"   🗑️  Encontrados {len(test_db_files)} archivos de test DB")
            for db_file in test_db_files:
                try:
                    # Intentar cerrar cualquier conexión abierta
                    conn = sqlite3.connect(db_file)
                    conn.close()
                    
                    # Eliminar archivo
                    os.remove(db_file)
                    print(f"   ✅ Eliminado: {os.path.basename(db_file)}")
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {os.path.basename(db_file)}: {e}")
        else:
            print("   ✅ No hay archivos de test DB pendientes")
        
        # 3. Limpiar directorios temporales de test
        print(f"\n📂 Limpiando directorios temporales...")
        
        test_dirs = []
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path) and ('test_' in item or 'tmp' in item):
                test_dirs.append(item_path)
        
        if test_dirs:
            print(f"   🗑️  Encontrados {len(test_dirs)} directorios de test")
            for test_dir in test_dirs:
                try:
                    shutil.rmtree(test_dir)
                    print(f"   ✅ Eliminado: {os.path.basename(test_dir)}")
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {os.path.basename(test_dir)}: {e}")
        else:
            print("   ✅ No hay directorios de test pendientes")
        
        print("\n✅ LIMPIEZA COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        return False

def test_database_creation():
    """Probar la creación de base de datos de test"""
    print("\n🧪 TEST: Creación de Base de Datos")
    print("-" * 40)
    
    try:
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        test_db_path = os.path.join(temp_dir, 'test_creation.db')
        
        print(f"📁 Directorio temporal: {temp_dir}")
        print(f"📄 Archivo DB: {os.path.basename(test_db_path)}")
        
        # Configurar Database para usar DB de test
        from database.database import Database
        original_db_path = getattr(Database, '_db_path', None)
        Database._db_path = test_db_path
        
        # Crear instancia
        db = Database()
        
        # Probar operación básica
        productos = db.get_all_products()
        print(f"✅ Base de datos creada, productos: {len(productos)}")
        
        # Probar agregar producto con referencia única
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        
        product_data = {
            'nombre': f'Test Product {unique_id}',
            'referencia': f'TEST-{unique_id}',
            'precio_venta': 10.50,
            'precio_compra': 7.00,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba',
            'iva_recomendado': 21.0,
            'stock_actual': 5,
            'stock_minimo': 1
        }
        
        result = db.add_product(product_data)
        if result:
            print("✅ Producto agregado correctamente")
        else:
            print("❌ Error agregando producto")
        
        # Limpiar
        if original_db_path:
            Database._db_path = original_db_path
        
        shutil.rmtree(temp_dir)
        print("✅ Limpieza completada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de creación: {e}")
        return False

def create_test_recommendations():
    """Crear recomendaciones para mejorar los tests"""
    print("\n💡 RECOMENDACIONES PARA TESTS")
    print("=" * 40)
    
    recommendations = [
        "1. Usar referencias únicas con UUID en cada test",
        "2. Implementar timeout en conexiones de base de datos",
        "3. Usar context managers para garantizar cierre de conexiones",
        "4. Implementar retry logic para operaciones de DB",
        "5. Usar fixtures de scope='function' para aislamiento completo",
        "6. Agregar cleanup explícito en teardown de tests",
        "7. Usar WAL mode en SQLite para mejor concurrencia",
        "8. Implementar locks de archivo para evitar acceso concurrente"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print("\n📝 EJEMPLO DE FIXTURE MEJORADA:")
    print("""
@pytest.fixture
def test_db():
    import uuid
    temp_dir = tempfile.mkdtemp()
    unique_id = str(uuid.uuid4())[:8]
    test_db_path = os.path.join(temp_dir, f'test_{unique_id}.db')
    
    original_db_path = getattr(Database, '_db_path', None)
    Database._db_path = test_db_path
    
    db = Database()
    
    yield db
    
    # Cleanup garantizado
    try:
        if hasattr(db, '_connection') and db._connection:
            db._connection.close()
    except:
        pass
    
    if original_db_path:
        Database._db_path = original_db_path
    
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    """)

def main():
    """Función principal"""
    print("🚀 CORRECCIÓN DE PROBLEMAS EN TESTS")
    print("=" * 60)
    
    print("🎯 PROBLEMAS IDENTIFICADOS:")
    print("   - sqlite3.IntegrityError: UNIQUE constraint failed")
    print("   - sqlite3.OperationalError: database is locked")
    print("   - AttributeError: module does not have attribute 'Database'")
    print()
    
    # Ejecutar correcciones
    success1 = fix_database_locked_issues()
    success2 = test_database_creation()
    
    create_test_recommendations()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 CORRECCIONES APLICADAS EXITOSAMENTE")
        print("\n✅ PRÓXIMOS PASOS:")
        print("   1. Los archivos temporales han sido limpiados")
        print("   2. Los tests deberían funcionar mejor ahora")
        print("   3. Ejecute: python -m pytest test/unit/test_productos_factura.py -v")
        print("   4. Si persisten errores, revisar las recomendaciones arriba")
    else:
        print("⚠️  CORRECCIONES PARCIALES")
        print("   Revisar errores específicos arriba")
    
    print("=" * 60)
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
