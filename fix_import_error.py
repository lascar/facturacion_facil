#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir problemas de importación
"""

import os
import sys
import shutil
from pathlib import Path

def clean_python_cache():
    """Limpiar cache de Python"""
    print("🧹 Limpiando cache de Python...")
    
    cache_patterns = [
        '__pycache__',
        '*/__pycache__',
        '*/*/__pycache__',
        '*.pyc',
        '*/*.pyc',
        '*/*/*.pyc',
    ]
    
    removed_count = 0
    
    # Limpiar directorios __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"  🗑️  Eliminado: {cache_dir}")
                removed_count += 1
            except Exception as e:
                print(f"  ⚠️  No se pudo eliminar {cache_dir}: {e}")
    
    # Limpiar archivos .pyc individuales
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                try:
                    os.remove(pyc_file)
                    print(f"  🗑️  Eliminado: {pyc_file}")
                    removed_count += 1
                except Exception as e:
                    print(f"  ⚠️  No se pudo eliminar {pyc_file}: {e}")
    
    print(f"✅ Cache limpiado: {removed_count} elementos eliminados")

def verify_file_integrity():
    """Verificar integridad de archivos críticos"""
    print("\n🔍 Verificando integridad de archivos...")
    
    critical_files = [
        'common/__init__.py',
        'common/simple_producto_autocomplete.py',
        'ui/__init__.py',
        'ui/producto_factura_dialog.py',
        'database/__init__.py',
        'database/models.py',
        'utils/__init__.py',
        'utils/logger.py',
    ]
    
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            try:
                # Verificar que se puede leer
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar que no está vacío
                if len(content.strip()) == 0:
                    print(f"  ⚠️  {file_path} está vacío")
                else:
                    print(f"  ✅ {file_path} ({len(content)} chars)")
                
                # Verificar sintaxis Python
                try:
                    compile(content, file_path, 'exec')
                    print(f"    ✅ Sintaxis válida")
                except SyntaxError as e:
                    print(f"    ❌ Error de sintaxis: {e}")
                
            except Exception as e:
                print(f"  ❌ {file_path}: Error leyendo - {e}")
        else:
            print(f"  ❌ {file_path}: NO EXISTE")

def fix_init_files():
    """Asegurar que todos los archivos __init__.py existen"""
    print("\n📁 Verificando archivos __init__.py...")
    
    directories = [
        'common',
        'ui',
        'database',
        'utils',
    ]
    
    for directory in directories:
        init_file = Path(directory) / '__init__.py'
        if not init_file.exists():
            print(f"  📝 Creando: {init_file}")
            try:
                init_file.parent.mkdir(parents=True, exist_ok=True)
                init_file.write_text('# -*- coding: utf-8 -*-\n', encoding='utf-8')
                print(f"    ✅ Creado exitosamente")
            except Exception as e:
                print(f"    ❌ Error creando: {e}")
        else:
            print(f"  ✅ {init_file} existe")

def check_dependencies():
    """Verificar dependencias críticas"""
    print("\n📦 Verificando dependencias...")
    
    dependencies = [
        'customtkinter',
        'tkinter',
        'sqlite3',
        'pathlib',
        'typing',
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError as e:
            print(f"  ❌ {dep}: {e}")

def create_test_script():
    """Crear script de test para verificar la corrección"""
    print("\n🧪 Creando script de test...")
    
    test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de verificación después de la corrección
"""

def test_problematic_import():
    """Test del import problemático"""
    print("🧪 Probando importación problemática...")
    
    try:
        # Esta es la línea que fallaba
        from common.simple_producto_autocomplete import SimpleProductoAutocomplete
        print("✅ ÉXITO: SimpleProductoAutocomplete importado correctamente")
        
        # Verificar que la clase es usable
        print("🔍 Verificando clase...")
        print(f"  Clase: {SimpleProductoAutocomplete}")
        print(f"  Módulo: {SimpleProductoAutocomplete.__module__}")
        print(f"  Archivo: {SimpleProductoAutocomplete.__module__}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_import_chain():
    """Test de toda la cadena de importación"""
    print("\\n🔗 Probando cadena completa de importación...")
    
    try:
        from ui.producto_factura_dialog import ProductoFacturaDialog
        print("✅ ÉXITO: ProductoFacturaDialog importado correctamente")
        return True
    except Exception as e:
        print(f"❌ ERROR en cadena: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TEST DE VERIFICACIÓN POST-CORRECCIÓN")
    print("=" * 40)
    
    success1 = test_problematic_import()
    success2 = test_full_import_chain()
    
    if success1 and success2:
        print("\\n🎉 TODOS LOS TESTS PASARON")
        print("💡 El problema de importación está resuelto")
    else:
        print("\\n❌ ALGUNOS TESTS FALLARON")
        print("💡 Revisa los errores anteriores")
'''
    
    with open('test_fix_verification.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("  ✅ Creado: test_fix_verification.py")

def main():
    """Función principal de corrección"""
    print("🔧 CORRECCIÓN DE PROBLEMAS DE IMPORTACIÓN")
    print("=" * 45)
    
    # Verificar que estamos en el directorio correcto
    if not Path('main.py').exists():
        print("❌ Error: main.py no encontrado")
        print("💡 Ejecuta este script desde el directorio raíz del proyecto")
        return False
    
    # Pasos de corrección
    steps = [
        ("Limpiar cache de Python", clean_python_cache),
        ("Verificar integridad de archivos", verify_file_integrity),
        ("Corregir archivos __init__.py", fix_init_files),
        ("Verificar dependencias", check_dependencies),
        ("Crear script de test", create_test_script),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            step_func()
        except Exception as e:
            print(f"❌ Error en {step_name}: {e}")
    
    print("\n" + "="*45)
    print("🎯 CORRECCIÓN COMPLETADA")
    print("💡 Ejecuta ahora: python test_fix_verification.py")
    print("💡 Si funciona, ejecuta: python main.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Corrección cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
