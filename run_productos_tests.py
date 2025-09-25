#!/usr/bin/env python3
"""
Script para ejecutar solo los tests del módulo de productos
"""

import sys
import os
import subprocess
from pathlib import Path

def run_productos_tests():
    """Ejecuta los tests del módulo de productos"""
    print("🧪 EJECUTANDO TESTS DEL MÓDULO DE PRODUCTOS")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("tests/test_ui/test_productos.py").exists():
        print("❌ Error: Tests de productos no encontrados")
        print("   Asegúrese de ejecutar desde el directorio raíz del proyecto")
        return False
    
    # Activar entorno virtual si existe
    venv_activate = Path("../bin/activate")
    if venv_activate.exists():
        print("🐍 Activando entorno virtual...")
        activate_cmd = f"source {venv_activate} && "
    else:
        print("⚠️  Entorno virtual no encontrado, usando Python del sistema")
        activate_cmd = ""
    
    # Comandos de test relacionados con productos
    test_commands = [
        {
            "name": "Tests de UI de Productos",
            "cmd": f"{activate_cmd}pytest tests/test_ui/test_productos.py -v",
            "description": "Interfaz de usuario de productos"
        },
        {
            "name": "Tests de Modelos de Productos",
            "cmd": f"{activate_cmd}pytest tests/test_database/test_models.py::TestProducto -v",
            "description": "Modelo Producto y operaciones CRUD"
        },
        {
            "name": "Tests de Stock",
            "cmd": f"{activate_cmd}pytest tests/test_database/test_models.py::TestStock -v",
            "description": "Gestión de stock de productos"
        },
        {
            "name": "Tests de Regresión - Selección de Imágenes",
            "cmd": f"{activate_cmd}pytest tests/test_regression/test_image_selection.py -v",
            "description": "Funcionalidad de selección de imágenes"
        },
        {
            "name": "Tests de Regresión - Mejoras UI",
            "cmd": f"{activate_cmd}pytest tests/test_regression/test_ui_improvements.py -v",
            "description": "Mejoras en la interfaz de usuario"
        }
    ]
    
    results = []
    total_tests = 0
    passed_tests = 0
    
    for test_group in test_commands:
        print(f"\n🔍 {test_group['name']}")
        print(f"   {test_group['description']}")
        print("-" * 60)
        
        try:
            # Ejecutar comando con bash explícitamente
            result = subprocess.run(
                test_group['cmd'],
                shell=True,
                executable='/bin/bash',  # Usar bash explícitamente
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos timeout
            )
            
            if result.returncode == 0:
                print("✅ PASARON")
                status = "PASS"
                
                # Extraer número de tests del output
                output_lines = result.stdout.split('\n')
                for line in output_lines:
                    if "passed" in line and "failed" not in line:
                        try:
                            # Buscar patrón como "X passed"
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "passed" and i > 0:
                                    count = int(parts[i-1])
                                    total_tests += count
                                    passed_tests += count
                                    break
                        except (ValueError, IndexError):
                            pass
                
            else:
                print("❌ FALLARON")
                status = "FAIL"
                print(f"   Error: {result.stderr}")
                
                # Mostrar output para debug
                if result.stdout:
                    print("   Output:")
                    for line in result.stdout.split('\n')[:10]:  # Primeras 10 líneas
                        if line.strip():
                            print(f"   {line}")
            
            results.append({
                "name": test_group['name'],
                "status": status,
                "returncode": result.returncode
            })
            
        except subprocess.TimeoutExpired:
            print("⏰ TIMEOUT - Test tardó más de 2 minutos")
            results.append({
                "name": test_group['name'],
                "status": "TIMEOUT",
                "returncode": -1
            })
        except Exception as e:
            print(f"💥 ERROR - {str(e)}")
            results.append({
                "name": test_group['name'],
                "status": "ERROR",
                "returncode": -1
            })
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS DE PRODUCTOS")
    print("=" * 60)
    
    passed_groups = sum(1 for r in results if r['status'] == 'PASS')
    total_groups = len(results)
    
    for result in results:
        status_icon = {
            'PASS': '✅',
            'FAIL': '❌',
            'TIMEOUT': '⏰',
            'ERROR': '💥'
        }.get(result['status'], '❓')
        
        print(f"{status_icon} {result['name']}")
    
    print(f"\n📈 Grupos de tests: {passed_groups}/{total_groups} pasaron")
    if total_tests > 0:
        print(f"📈 Tests individuales: {passed_tests}/{total_tests} pasaron")
    
    if passed_groups == total_groups:
        print("\n🎉 ¡TODOS LOS TESTS DE PRODUCTOS PASARON!")
        print("\n💡 El módulo de productos está listo para usar:")
        print("   1. python main.py")
        print("   2. Clic en 'Productos'")
        print("   3. Gestionar productos")
        return True
    else:
        print(f"\n⚠️  {total_groups - passed_groups} grupos de tests fallaron")
        print("   Revise los errores arriba para más detalles")
        return False

def run_productos_related_tests():
    """Ejecuta todos los tests relacionados con productos"""
    print("\n" + "=" * 60)
    print("🚀 EJECUTANDO TODOS LOS TESTS RELACIONADOS CON PRODUCTOS")
    print("=" * 60)
    
    venv_activate = Path("../bin/activate")
    if venv_activate.exists():
        activate_cmd = f"source {venv_activate} && "
    else:
        activate_cmd = ""
    
    # Tests relacionados con productos
    test_patterns = [
        "tests/test_ui/test_productos.py",
        "tests/test_database/test_models.py::TestProducto",
        "tests/test_database/test_models.py::TestStock",
        "tests/test_regression/test_image_selection.py",
        "tests/test_regression/test_ui_improvements.py"
    ]
    
    cmd = f"{activate_cmd}pytest {' '.join(test_patterns)} -v --tb=short"
    
    try:
        result = subprocess.run(cmd, shell=True, executable='/bin/bash', timeout=300)  # 5 minutos
        
        if result.returncode == 0:
            print("✅ TODOS LOS TESTS DE PRODUCTOS PASARON")
            return True
        else:
            print("❌ ALGUNOS TESTS FALLARON")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Tests tardaron más de 5 minutos")
        return False
    except Exception as e:
        print(f"💥 ERROR - {str(e)}")
        return False

def main():
    """Función principal"""
    print("🎯 SUITE DE TESTS DEL MÓDULO DE PRODUCTOS")
    print("Facturación Fácil - Tests Específicos de Productos")
    print("=" * 60)
    
    # Verificar estructura de proyecto
    required_files = [
        "tests/test_ui/test_productos.py",
        "tests/test_database/test_models.py",
        "tests/test_regression/test_image_selection.py",
        "tests/test_regression/test_ui_improvements.py"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print("❌ Archivos de test faltantes:")
        for f in missing_files:
            print(f"   - {f}")
        return False
    
    print("✅ Todos los archivos de test encontrados")
    
    # Ejecutar tests por grupos
    success_individual = run_productos_tests()
    
    # Ejecutar todos juntos
    success_all = run_productos_related_tests()
    
    # Resultado final
    print("\n" + "=" * 60)
    if success_individual and success_all:
        print("🎉 ¡ÉXITO TOTAL! El módulo de productos está completamente testado")
        print("\n🔧 Funcionalidades verificadas:")
        print("   ✅ Interfaz de usuario de productos")
        print("   ✅ Modelo de datos Producto")
        print("   ✅ Gestión de stock")
        print("   ✅ Selección de imágenes")
        print("   ✅ Mejoras de UI (scroll, etc.)")
        print("\n🚀 El módulo está listo para producción!")
        return True
    else:
        print("⚠️  Algunos tests fallaron. Revise los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
