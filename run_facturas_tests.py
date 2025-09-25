#!/usr/bin/env python3
"""
Script para ejecutar solo los tests del módulo de facturas
"""

import sys
import os
import subprocess
from pathlib import Path

def run_facturas_tests():
    """Ejecuta los tests del módulo de facturas"""
    print("🧪 EJECUTANDO TESTS DEL MÓDULO DE FACTURAS")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("tests/test_facturas").exists():
        print("❌ Error: Directorio tests/test_facturas no encontrado")
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
    
    # Comandos de test
    test_commands = [
        {
            "name": "Tests de Modelos de Factura",
            "cmd": f"{activate_cmd}pytest tests/test_facturas/test_factura_models.py -v",
            "description": "Modelos Factura y FacturaItem"
        },
        {
            "name": "Tests de Validadores",
            "cmd": f"{activate_cmd}pytest tests/test_facturas/test_validators.py -v",
            "description": "FormValidator y CalculationHelper"
        },
        {
            "name": "Tests de Componentes UI",
            "cmd": f"{activate_cmd}pytest tests/test_facturas/test_ui_components.py -v",
            "description": "BaseWindow, ImageSelector, FormHelper"
        },
        {
            "name": "Tests de Integración",
            "cmd": f"{activate_cmd}pytest tests/test_facturas/test_facturas_integration.py -v",
            "description": "Flujos completos de facturas"
        },
        {
            "name": "Tests de UI de Facturas",
            "cmd": f"{activate_cmd}pytest tests/test_facturas/test_facturas_ui.py -v",
            "description": "Interfaz de usuario de facturas"
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
    print("📊 RESUMEN DE TESTS DE FACTURAS")
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
        print("\n🎉 ¡TODOS LOS TESTS DE FACTURAS PASARON!")
        print("\n💡 El módulo de facturas está listo para usar:")
        print("   1. python main.py")
        print("   2. Clic en 'Facturas'")
        print("   3. Crear nueva factura")
        return True
    else:
        print(f"\n⚠️  {total_groups - passed_groups} grupos de tests fallaron")
        print("   Revise los errores arriba para más detalles")
        return False

def run_all_facturas_tests_together():
    """Ejecuta todos los tests de facturas juntos"""
    print("\n" + "=" * 60)
    print("🚀 EJECUTANDO TODOS LOS TESTS DE FACTURAS JUNTOS")
    print("=" * 60)
    
    venv_activate = Path("../bin/activate")
    if venv_activate.exists():
        activate_cmd = f"source {venv_activate} && "
    else:
        activate_cmd = ""
    
    cmd = f"{activate_cmd}pytest tests/test_facturas/ -v --tb=short"
    
    try:
        result = subprocess.run(cmd, shell=True, executable='/bin/bash', timeout=300)  # 5 minutos
        
        if result.returncode == 0:
            print("✅ TODOS LOS TESTS DE FACTURAS PASARON")
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
    print("🎯 SUITE DE TESTS DEL MÓDULO DE FACTURAS")
    print("Facturación Fácil - Tests Específicos de Facturas")
    print("=" * 60)
    
    # Verificar estructura de proyecto
    required_files = [
        "tests/test_facturas/test_factura_models.py",
        "tests/test_facturas/test_validators.py",
        "tests/test_facturas/test_ui_components.py",
        "tests/test_facturas/test_facturas_integration.py",
        "tests/test_facturas/test_facturas_ui.py"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print("❌ Archivos de test faltantes:")
        for f in missing_files:
            print(f"   - {f}")
        return False
    
    print("✅ Todos los archivos de test encontrados")
    
    # Ejecutar tests por grupos
    success_individual = run_facturas_tests()
    
    # Ejecutar todos juntos
    success_all = run_all_facturas_tests_together()
    
    # Resultado final
    print("\n" + "=" * 60)
    if success_individual and success_all:
        print("🎉 ¡ÉXITO TOTAL! El módulo de facturas está completamente testado")
        print("\n🔧 Funcionalidades verificadas:")
        print("   ✅ Modelos de datos (Factura, FacturaItem)")
        print("   ✅ Validadores y cálculos financieros")
        print("   ✅ Componentes UI reutilizables")
        print("   ✅ Integración completa del sistema")
        print("   ✅ Interfaz de usuario")
        print("\n🚀 El módulo está listo para producción!")
        return True
    else:
        print("⚠️  Algunos tests fallaron. Revise los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
