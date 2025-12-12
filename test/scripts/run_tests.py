#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour exécuter les tests de Facturación Fácil
"""

import sys
import os
import subprocess

def run_tests():
    """Exécute tous les tests avec pytest"""

    print("🧪 Ejecutando tests de Facturación Fácil...")
    print("=" * 50)

    # Déterminer la commande Python à utiliser
    python_cmd = sys.executable

    # Commandes de test
    commands = [
        # Tests basiques avec couverture
        [python_cmd, "-m", "pytest", "-v", "--cov=.", "--cov-report=term-missing"],

        # Générer rapport HTML de couverture
        [python_cmd, "-m", "pytest", "--cov=.", "--cov-report=html"],
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n📋 Étape {i}/{len(commands)}: {' '.join(cmd)}")
        print("-" * 30)
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print(f"✅ Étape {i} terminée avec succès")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur dans l'étape {i}: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Commande non trouvée: {cmd[0]}")
            print("💡 Installez pytest avec: pip install -r requirements-dev.txt")
            return False
    
    print("\n🎉 Tous les tests sont terminés!")
    print("📊 Rapport de couverture HTML généré dans: htmlcov/index.html")
    return True

def run_specific_tests():
    """Exécute des tests spécifiques selon les arguments"""
    
    if len(sys.argv) < 2:
        return run_tests()
    
    test_type = sys.argv[1].lower()
    
    python_cmd = sys.executable

    test_commands = {
        "unit": [python_cmd, "-m", "pytest", "test/unit/", "-v"],
        "integration": [python_cmd, "-m", "pytest", "test/integration/", "-v"],
        "productos": [python_cmd, "-m", "pytest", "-k", "productos_factura", "-v"],
        "productos-unit": [python_cmd, "-m", "pytest", "test/unit/test_productos_factura.py", "-v"],
        "productos-integration": [python_cmd, "-m", "pytest", "test/integration/test_productos_factura_integration.py", "-v"],
        "ui": [python_cmd, "-m", "pytest", "test/", "-k", "ui", "-v"],
        "utils": [python_cmd, "-m", "pytest", "test/utils/", "-v"],
        "advanced": [python_cmd, "-m", "pytest", "test/", "-v"],
        "parametrized": [python_cmd, "-m", "pytest", "test/unit/test_parametrized.py", "-v"],
        "property": [python_cmd, "-m", "pytest", "test/property_based/", "-v"],
        "performance": [python_cmd, "-m", "pytest", "test/performance/", "-v"],
        "regression": [python_cmd, "-m", "pytest", "test/regression/", "-v"],
        "stress": [python_cmd, "-m", "pytest", "test/stress/", "-v"],
        "security": [python_cmd, "-m", "pytest", "test/unit/test_security.py", "-v"],
        "benchmark": [python_cmd, "-m", "pytest", "--benchmark-only", "-v"],
        "fast": [python_cmd, "-m", "pytest", "-v", "-m", "not slow"],
        "slow": [python_cmd, "-m", "pytest", "-v", "-m", "slow"],
        "parallel": [python_cmd, "-m", "pytest", "-n", "auto", "-v"],
        "coverage": [python_cmd, "-m", "pytest", "--cov=.", "--cov-report=html", "--cov-report=term"],
        "lint": [python_cmd, "-m", "flake8", "."],
        "format": [python_cmd, "-m", "black", ".", "--check"],
    }
    
    if test_type in test_commands:
        cmd = test_commands[test_type]
        print(f"🧪 Ejecutando: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ {test_type} tests completados")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en {test_type} tests: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Comando no encontrado: {cmd[0]}")
            return False
    else:
        print(f"❌ Tipo de test desconocido: {test_type}")
        print("📋 Tipos disponibles:")
        print("  Básicos: unit, integration, ui, utils, advanced")
        print("  Productos: productos, productos-unit, productos-integration")
        print("  Avanzados: parametrized, property, performance, regression, stress, security")
        print("  Especiales: benchmark, fast, slow, parallel, coverage")
        print("  Calidad: lint, format")
        return False

def show_help():
    """Affiche l'aide"""
    help_text = """
🧪 Script de Tests - Facturación Fácil

Uso:
    python run_tests.py [tipo]

Tipos de tests disponibles:
    (sin argumentos)  - Ejecuta todos los tests con cobertura

    Tests básicos:
    unit             - Tests unitarios (base de datos, modelos)
    integration      - Tests de integración (workflows completos)
    ui               - Tests de interfaz de usuario
    utils            - Tests de utilidades
    advanced         - Todos los tests avanzados

    Tests de productos (NUEVO):
    productos        - Todos los tests de productos en facturas
    productos-unit   - Tests unitarios de productos
    productos-integration - Tests d'intégration de productos

    Tests avanzados:
    parametrized     - Tests parametrizados con múltiples casos
    property         - Tests basados en propiedades (Hypothesis)
    performance      - Tests de rendimiento y benchmarks
    regression       - Tests de régression (bugs corrigés)
    stress           - Tests de stress et charge
    security         - Tests de seguridad y validación

    Tests especiales:
    benchmark        - Solo benchmarks de rendimiento
    fast             - Tests rápidos (excluye 'slow')
    slow             - Solo tests lentos
    parallel         - Tests en paralelo (requiere pytest-xdist)
    coverage         - Tests con reporte de cobertura detallado

    Calidad de código:
    lint             - Verificación de estilo con flake8
    format           - Verificación de formato con black

Ejemplos:
    python run_tests.py                    # Todos los tests
    python run_tests.py unit               # Tests unitaires
    python run_tests.py advanced           # Tests avanzados
    python run_tests.py performance        # Tests de rendimiento
    python run_tests.py security           # Tests de seguridad
    python run_tests.py benchmark          # Solo benchmarks
    python run_tests.py parallel           # Tests en paralelo
    python run_tests.py coverage           # Con cobertura
    python run_tests.py lint               # Verificación estilo

Instalación de dependencias:
    pip install -r requirements-dev.txt
"""
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
    else:
        success = run_specific_tests()
        sys.exit(0 if success else 1)
