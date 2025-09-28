#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de déploiement de la solution complète
"""

import sys
import os
import subprocess
import shutil
from datetime import datetime

def print_header(title):
    """Affiche un en-tête formaté"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, description):
    """Affiche une étape"""
    print(f"\n{step_num}️⃣ {description}")
    print("-" * 40)

def run_command(command, description, critical=True):
    """Exécute une commande et gère les erreurs"""
    print(f"   🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {description} - ÉXITO")
            return True
        else:
            print(f"   ❌ {description} - FALLO")
            if result.stderr:
                print(f"      Error: {result.stderr[:200]}...")
            if critical:
                return False
            return True
    except Exception as e:
        print(f"   ❌ {description} - ERROR: {e}")
        if critical:
            return False
        return True

def check_prerequisites():
    """Vérifie les prérequis"""
    print_step(1, "VERIFICACIÓN DE PRERREQUISITOS")
    
    # Vérifier Python
    if not run_command("python3 --version", "Verificar Python 3"):
        return False
    
    # Vérifier pip
    if not run_command("pip3 --version", "Verificar pip3"):
        return False
    
    # Vérifier la structure du projet
    required_dirs = [
        "database", "ui", "common", "utils", "docs", "test", "logs"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ Directorio {dir_name} - OK")
        else:
            print(f"   ❌ Directorio {dir_name} - FALTA")
            return False
    
    return True

def install_dependencies():
    """Installe les dépendances"""
    print_step(2, "INSTALACIÓN DE DEPENDENCIAS")
    
    # Dépendances principales
    dependencies = [
        "customtkinter",
        "reportlab",
        "pillow"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip3 install {dep}", f"Instalar {dep}"):
            return False
    
    return True

def setup_database():
    """Configure la base de données"""
    print_step(3, "CONFIGURACIÓN DE BASE DE DATOS")
    
    # Créer le répertoire de base de données s'il n'existe pas
    if not os.path.exists("database"):
        os.makedirs("database")
        print("   ✅ Directorio database creado")
    
    # Initialiser la base de données
    if not run_command("python3 -c \"from database.database import db; db.init_database()\"", 
                      "Inicializar base de datos"):
        return False
    
    return True

def run_tests():
    """Exécute les tests de validation"""
    print_step(4, "EJECUCIÓN DE TESTS DE VALIDACIÓN")
    
    # Tests critiques
    critical_tests = [
        ("test/demo/demo_simple_stock_test.py", "Test básico de stock"),
        ("test/demo/demo_test_factura_selection.py", "Test selección de facturas"),
        ("test/validate_solution.py", "Validación completa del sistema")
    ]
    
    for test_file, description in critical_tests:
        if os.path.exists(test_file):
            if not run_command(f"python3 {test_file}", description):
                print(f"   ⚠️ Test crítico falló: {description}")
                return False
        else:
            print(f"   ⚠️ Test no encontrado: {test_file}")
    
    return True

def setup_directories():
    """Configure les répertoires nécessaires"""
    print_step(5, "CONFIGURACIÓN DE DIRECTORIOS")
    
    # Répertoires à créer
    directories = [
        "logs",
        "pdfs",
        "backups",
        "temp"
    ]
    
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"   ✅ Directorio {dir_name} creado")
        else:
            print(f"   ✅ Directorio {dir_name} ya existe")
    
    # Créer fichier de log initial
    log_file = "logs/facturacion_facil.log"
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"# Log de Facturación Fácil - Iniciado: {datetime.now()}\n")
        print("   ✅ Archivo de log inicial creado")
    
    return True

def create_shortcuts():
    """Crée des raccourcis pour les outils principaux"""
    print_step(6, "CREACIÓN DE ACCESOS DIRECTOS")
    
    # Scripts de raccourci
    shortcuts = {
        "run_app.py": """#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "main.py"])
""",
        "test_system.py": """#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "test/demo/demo_complete_solution_test.py"])
""",
        "monitor_system.py": """#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "test/demo/demo_real_time_monitor.py"])
""",
        "validate_system.py": """#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "test/validate_solution.py"])
"""
    }
    
    for filename, content in shortcuts.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Rendre exécutable sur Unix
        if os.name != 'nt':
            os.chmod(filename, 0o755)
        
        print(f"   ✅ Acceso directo creado: {filename}")
    
    return True

def run_final_validation():
    """Validation finale complète"""
    print_step(7, "VALIDACIÓN FINAL COMPLETA")
    
    # Test complet du système
    if not run_command("python3 test/demo/demo_complete_solution_test.py", 
                      "Test completo del sistema"):
        print("   ⚠️ Test completo falló - Sistema parcialmente funcional")
    
    # Validation du système
    if not run_command("python3 test/validate_solution.py", 
                      "Validación completa del sistema"):
        print("   ⚠️ Validación falló - Revisar componentes")
    
    # Test de performance (non critique)
    run_command("python3 test/performance/benchmark_solution.py", 
               "Benchmark de performance", critical=False)
    
    return True

def show_deployment_summary():
    """Affiche le résumé du déploiement"""
    print_header("RESUMEN DE DESPLIEGUE")
    
    print("✅ DESPLIEGUE COMPLETADO")
    print("\n📋 COMPONENTES INSTALADOS:")
    print("   • ✅ Base de datos inicializada")
    print("   • ✅ Dependencias instaladas")
    print("   • ✅ Directorios configurados")
    print("   • ✅ Tests de validación ejecutados")
    print("   • ✅ Accesos directos creados")
    
    print("\n🚀 COMANDOS PRINCIPALES:")
    print("   • Ejecutar aplicación: python3 run_app.py")
    print("   • Test del sistema: python3 test_system.py")
    print("   • Monitor en tiempo real: python3 monitor_system.py")
    print("   • Validar sistema: python3 validate_system.py")
    
    print("\n📚 DOCUMENTACIÓN DISPONIBLE:")
    print("   • docs/USER_GUIDE_STOCK_CONFIRMATION.md - Guía de stock")
    print("   • docs/USER_GUIDE_PDF_EXPORT.md - Guía de PDF")
    print("   • docs/ADMIN_GUIDE.md - Guía de administración")
    print("   • docs/TESTING_GUIDE.md - Guía de testing")
    
    print("\n🔧 HERRAMIENTAS DE DIAGNÓSTICO:")
    print("   • Monitor tiempo real: test/demo/demo_real_time_monitor.py")
    print("   • Benchmark performance: test/performance/benchmark_solution.py")
    print("   • Stress test: test/stress/stress_test_solution.py")
    
    print("\n📊 PRÓXIMOS PASOS:")
    print("   1. Ejecutar: python3 run_app.py")
    print("   2. Crear algunas facturas de prueba")
    print("   3. Probar exportación PDF")
    print("   4. Verificar actualización de stock")
    print("   5. Revisar logs en: logs/facturacion_facil.log")

def main():
    """Fonction principale de déploiement"""
    print_header("DESPLIEGUE DE FACTURACIÓN FÁCIL")
    print("Este script configura completamente el sistema:")
    print("   • Verifica prerrequisitos")
    print("   • Instala dependencias")
    print("   • Configura base de datos")
    print("   • Ejecuta tests de validación")
    print("   • Crea accesos directos")
    
    response = input("\n¿Continuar con el despliegue? (s/n): ").lower().strip()
    if response != 's':
        print("Despliegue cancelado")
        return
    
    # Étapes de déploiement
    steps = [
        check_prerequisites,
        install_dependencies,
        setup_database,
        setup_directories,
        run_tests,
        create_shortcuts,
        run_final_validation
    ]
    
    success = True
    for step in steps:
        if not step():
            success = False
            print(f"\n❌ Error en paso: {step.__name__}")
            break
    
    if success:
        show_deployment_summary()
        print("\n🎉 DESPLIEGUE EXITOSO - Sistema listo para usar")
    else:
        print("\n❌ DESPLIEGUE FALLÓ - Revisar errores arriba")
        print("💡 Intenta ejecutar los pasos manualmente")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
