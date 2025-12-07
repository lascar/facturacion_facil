#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar los tests de limpieza de datos
Conforme a las preferencias de desarrollo
"""

import sys
import os
import subprocess

def main():
    """Ejecuta los tests de limpieza de datos"""
    print("🧪 EJECUTANDO TESTS DE LIMPIEZA DE DATOS")
    print("=" * 45)
    print()
    
    # Obtener el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    test_file = os.path.join(project_root, 'test', 'integration', 'test_data_cleanup_integration.py')
    
    # Verificar que el archivo de test existe
    if not os.path.exists(test_file):
        print(f"❌ Error: Archivo de test no encontrado: {test_file}")
        return 1
    
    print(f"📁 Directorio del proyecto: {os.path.abspath(project_root)}")
    print(f"🧪 Archivo de test: {os.path.relpath(test_file, project_root)}")
    print()
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir(project_root)
        
        # Ejecutar el test
        print("🚀 Iniciando tests...")
        result = subprocess.run([
            sys.executable, 
            test_file
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ TESTS COMPLETADOS EXITOSAMENTE")
            print("   El sistema de limpieza de datos funciona correctamente")
            return 0
        else:
            print(f"\n❌ TESTS FALLARON (código: {result.returncode})")
            return result.returncode
            
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
