#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de diagnóstico para problemas de importación
"""

import sys
import os
from pathlib import Path

def diagnose_import_problem():
    """Diagnosticar problemas de importación"""
    print("🔍 DIAGNÓSTICO DE IMPORTACIÓN")
    print("=" * 40)
    
    # 1. Verificar Python y sistema
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Sistema: {sys.platform}")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🛤️  Python path: {sys.path[:3]}...")  # Solo primeros 3
    
    # 2. Verificar estructura de archivos
    print("\n📁 ESTRUCTURA DE ARCHIVOS:")
    
    files_to_check = [
        'main.py',
        'common/__init__.py',
        'common/simple_producto_autocomplete.py',
        'ui/__init__.py',
        'ui/producto_factura_dialog.py',
        'ui/facturas_methods.py',
    ]
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} - NO EXISTE")
    
    # 3. Verificar importaciones paso a paso
    print("\n🔍 PRUEBAS DE IMPORTACIÓN:")
    
    import_tests = [
        ("import sys", "Sistema básico"),
        ("import os", "OS básico"),
        ("import pathlib", "Pathlib"),
        ("import customtkinter", "CustomTkinter"),
        ("import tkinter", "Tkinter"),
        ("from database.models import Producto", "Modelos de base de datos"),
        ("from utils.logger import get_logger", "Logger"),
        ("import common", "Paquete common"),
        ("from common import simple_producto_autocomplete", "Módulo específico"),
        ("from common.simple_producto_autocomplete import SimpleProductoAutocomplete", "Clase específica"),
    ]
    
    for import_cmd, description in import_tests:
        try:
            exec(import_cmd)
            print(f"  ✅ {description}")
        except Exception as e:
            print(f"  ❌ {description}: {e}")
    
    # 4. Verificar contenido del archivo problemático
    print("\n📄 VERIFICACIÓN DE ARCHIVO:")
    
    file_path = Path('common/simple_producto_autocomplete.py')
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  📏 Tamaño: {len(content)} caracteres")
            print(f"  📝 Líneas: {len(content.splitlines())}")
            
            # Verificar primeras líneas
            lines = content.splitlines()[:10]
            print("  🔍 Primeras líneas:")
            for i, line in enumerate(lines, 1):
                print(f"    {i:2d}: {line[:60]}{'...' if len(line) > 60 else ''}")
            
            # Verificar si hay caracteres problemáticos
            if '\r\n' in content:
                print("  ⚠️  Contiene terminadores Windows (\\r\\n)")
            if '\x00' in content:
                print("  ❌ Contiene caracteres nulos")
            
        except Exception as e:
            print(f"  ❌ Error leyendo archivo: {e}")
    
    # 5. Verificar cache de Python
    print("\n🗂️  CACHE DE PYTHON:")
    
    cache_dirs = [
        'common/__pycache__',
        '__pycache__',
    ]
    
    for cache_dir in cache_dirs:
        cache_path = Path(cache_dir)
        if cache_path.exists():
            cache_files = list(cache_path.glob('*.pyc'))
            print(f"  📁 {cache_dir}: {len(cache_files)} archivos .pyc")
            
            # Verificar archivo específico
            target_cache = cache_path / 'simple_producto_autocomplete.cpython-*.pyc'
            matching_cache = list(cache_path.glob('simple_producto_autocomplete.cpython-*.pyc'))
            if matching_cache:
                print(f"    ✅ Cache encontrado: {matching_cache[0].name}")
            else:
                print(f"    ❌ Cache no encontrado para simple_producto_autocomplete")
    
    # 6. Sugerencias de solución
    print("\n💡 SUGERENCIAS DE SOLUCIÓN:")
    print("  1. Limpiar cache: rm -rf __pycache__ common/__pycache__")
    print("  2. Verificar encoding: archivo debe ser UTF-8")
    print("  3. Verificar permisos de archivo")
    print("  4. Reinstalar dependencias: pip install --force-reinstall customtkinter")
    print("  5. Verificar PYTHONPATH")

def create_minimal_test():
    """Crear test mínimo del módulo problemático"""
    print("\n🧪 CREANDO TEST MÍNIMO...")
    
    test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test mínimo para simple_producto_autocomplete
"""

def test_import():
    """Test de importación paso a paso"""
    print("🧪 Test de importación...")
    
    try:
        print("  1. Importando customtkinter...")
        import customtkinter as ctk
        print("    ✅ customtkinter OK")
        
        print("  2. Importando tkinter...")
        import tkinter as tk
        print("    ✅ tkinter OK")
        
        print("  3. Importando typing...")
        from typing import List, Dict, Callable, Optional
        print("    ✅ typing OK")
        
        print("  4. Importando database.models...")
        from database.models import Producto, Stock
        print("    ✅ database.models OK")
        
        print("  5. Importando utils.logger...")
        from utils.logger import get_logger
        print("    ✅ utils.logger OK")
        
        print("  6. Importando el módulo problemático...")
        from common.simple_producto_autocomplete import SimpleProductoAutocomplete
        print("    ✅ SimpleProductoAutocomplete OK")
        
        print("🎉 TODAS LAS IMPORTACIONES EXITOSAS")
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        import traceback
        print(f"    📄 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_import()
'''
    
    with open('test_import_minimal.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("  ✅ Creado: test_import_minimal.py")
    print("  💡 Ejecuta: python test_import_minimal.py")

if __name__ == "__main__":
    try:
        diagnose_import_problem()
        create_minimal_test()
        
        print("\n" + "="*40)
        print("🎯 DIAGNÓSTICO COMPLETADO")
        print("💡 Ejecuta también: python test_import_minimal.py")
        
    except Exception as e:
        print(f"\n❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()
