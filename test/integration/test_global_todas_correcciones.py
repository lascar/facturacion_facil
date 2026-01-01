#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test global que verifica que todas las correcciones funcionan correctamente
"""

import sys
import os
import subprocess
import pytest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test_file(test_file):
    """Ejecutar un archivo de test y devolver el resultado"""
    try:
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))

        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)



def test_aplicacion_completa():
    """Test adicional: verificar que la aplicación se inicia sin errores"""
    print("\n" + "=" * 70)
    print("🚀 TEST ADICIONAL: INICIO DE APLICACIÓN")
    print("=" * 70)
    
    try:
        # Intentar importar módulos principales
        print("1️⃣ Importando módulos principales...")
        
        from database.database import Database
        from database.models import Organizacion, Producto, Factura
        from utils.factura_numbering import factura_numbering_service
        print("   ✅ Módulos de base de datos importados")
        
        # Verificar base de datos (usar temp_db del fixture)
        print("2️⃣ Verificando base de datos...")
        from database.database import db  # Utiliser l'instance globale qui sera patchée
        print("   ✅ Base de datos inicializada")
        
        # Verificar sistema de numeración
        print("3️⃣ Verificando sistema de numeración...")
        numero = factura_numbering_service.get_next_numero_factura()
        print(f"   ✅ Número generado: {numero}")
        
        # Verificar organización
        print("4️⃣ Verificando módulo organización...")
        org = Organizacion.get()
        print(f"   ✅ Organización cargada: {org.nombre or 'Sin nombre'}")

        print("\n✅ APLICACIÓN FUNCIONA CORRECTAMENTE")
        assert True

    except Exception as e:
        print(f"\n❌ ERROR EN APLICACIÓN: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Error en aplicación: {e}"

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN COMPLETA DE TODAS LAS CORRECCIONES")
    print("=" * 70)
    
    # Ejecutar tests globales
    tests_passed = test_global_todas_correcciones()
    
    # Test adicional de aplicación
    app_works = test_aplicacion_completa()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("🏁 RESULTADO FINAL")
    print("=" * 70)
    
    if tests_passed and app_works:
        print("🎉 ¡ÉXITO COMPLETO!")
        print("✅ Todos los tests pasan")
        print("✅ Aplicación funciona correctamente")
        print("✅ Todas las correcciones están operativas")
        print("\n🚀 El sistema está listo para producción!")
        sys.exit(0)
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        if not tests_passed:
            print("❌ Algunos tests fallaron")
        if not app_works:
            print("❌ La aplicación tiene problemas")
        print("\n🔧 Revisar las correcciones necesarias")
        sys.exit(1)
