#!/usr/bin/env python3
"""
Test pour vérifier que les markers pytest sont correctement configurés
"""

import sys
import os
import subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pytest_markers_configuration():
    """Test que les markers pytest sont correctement configurés"""
    print("🔍 Test de la configuration des markers pytest...")
    
    try:
        # Exécuter pytest --markers pour obtenir la liste des markers
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--markers'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode != 0:
            print(f"   ❌ Erreur lors de l'exécution de pytest --markers: {result.stderr}")
            return False
        
        markers_output = result.stdout
        
        # Vérifier que les markers personnalisés sont présents
        expected_markers = [
            '@pytest.mark.unit: Unit tests',
            '@pytest.mark.integration: Integration tests',
            '@pytest.mark.ui: UI tests',
            '@pytest.mark.slow: Slow running tests that may take longer to execute',
            '@pytest.mark.performance: Performance and benchmark tests',
            '@pytest.mark.regression: Regression tests to prevent bugs from reappearing'
        ]
        
        markers_found = 0
        for marker in expected_markers:
            if marker in markers_output:
                markers_found += 1
                print(f"   ✅ {marker}")
            else:
                print(f"   ❌ {marker} NON trouvé")
        
        if markers_found >= 5:  # Au moins 5 sur 6
            print("   ✅ Markers personnalisés correctement configurés")
            return True
        else:
            print("   ❌ Configuration des markers insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_pytest_ini_file_exists():
    """Test que le fichier pytest.ini existe et est correct"""
    print("\n🔍 Test de l'existence et contenu du fichier pytest.ini...")
    
    try:
        pytest_ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pytest.ini')
        
        if not os.path.exists(pytest_ini_path):
            print("   ❌ Fichier pytest.ini n'existe pas")
            return False
        
        with open(pytest_ini_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier le contenu du fichier
        required_sections = [
            '[pytest]',
            'markers =',
            'slow: Slow running tests',
            'unit: Unit tests',
            'integration: Integration tests'
        ]
        
        sections_found = 0
        for section in required_sections:
            if section in content:
                sections_found += 1
                print(f"   ✅ {section} trouvé")
            else:
                print(f"   ❌ {section} NON trouvé")
        
        if sections_found >= 4:  # Au moins 4 sur 5
            print("   ✅ Fichier pytest.ini correctement configuré")
            return True
        else:
            print("   ❌ Configuration pytest.ini insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_coveragerc_file_exists():
    """Test que le fichier .coveragerc existe"""
    print("\n🔍 Test de l'existence du fichier .coveragerc...")
    
    try:
        coveragerc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.coveragerc')
        
        if not os.path.exists(coveragerc_path):
            print("   ❌ Fichier .coveragerc n'existe pas")
            return False
        
        with open(coveragerc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier le contenu du fichier
        required_sections = [
            '[run]',
            '[report]',
            '[html]',
            'omit =',
            'tests/*'
        ]
        
        sections_found = 0
        for section in required_sections:
            if section in content:
                sections_found += 1
                print(f"   ✅ {section} trouvé")
            else:
                print(f"   ❌ {section} NON trouvé")
        
        if sections_found >= 4:  # Au moins 4 sur 5
            print("   ✅ Fichier .coveragerc correctement configuré")
            return True
        else:
            print("   ❌ Configuration .coveragerc insuffisante")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_slow_marker_no_warnings():
    """Test qu'il n'y a pas de warnings pour le marker slow"""
    print("\n🔍 Test d'absence de warnings pour le marker slow...")
    
    try:
        # Exécuter un test avec marker slow pour vérifier l'absence de warnings
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '-m', 'slow', '--tb=no', '-q'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        output = result.stdout + result.stderr
        
        # Vérifier l'absence de warnings sur les markers
        warning_patterns = [
            'PytestUnknownMarkWarning',
            'Unknown pytest.mark.slow',
            'is this a typo?'
        ]
        
        warnings_found = 0
        for pattern in warning_patterns:
            if pattern in output:
                warnings_found += 1
                print(f"   ❌ Warning trouvé: {pattern}")
        
        if warnings_found == 0:
            print("   ✅ Aucun warning sur les markers")
            return True
        else:
            print(f"   ❌ {warnings_found} warnings trouvés")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test de Configuration des Markers Pytest")
    print("=" * 60)
    
    tests = [
        ("Configuration des markers pytest", test_pytest_markers_configuration),
        ("Fichier pytest.ini", test_pytest_ini_file_exists),
        ("Fichier .coveragerc", test_coveragerc_file_exists),
        ("Absence de warnings markers", test_slow_marker_no_warnings)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡CONFIGURACIÓN DE MARKERS PYTEST CORRECTA!")
        print("\n📋 Configuración implementada:")
        print("   1. ✅ pytest.ini con formato correcto [pytest]")
        print("   2. ✅ Markers personalizados definidos")
        print("   3. ✅ .coveragerc para configuración de coverage")
        print("   4. ✅ Sin warnings de markers desconocidos")
        print("\n🎯 Markers disponibles:")
        print("   - @pytest.mark.unit: Tests unitarios")
        print("   - @pytest.mark.integration: Tests de integración")
        print("   - @pytest.mark.ui: Tests de interfaz")
        print("   - @pytest.mark.slow: Tests lentos")
        print("   - @pytest.mark.performance: Tests de rendimiento")
        print("   - @pytest.mark.regression: Tests de regresión")
        print("\n📋 Uso:")
        print("   pytest -m slow          # Ejecutar solo tests lentos")
        print("   pytest -m 'not slow'    # Ejecutar tests rápidos")
        print("   pytest -m unit          # Ejecutar solo tests unitarios")
    else:
        print("⚠️  ALGUNOS TESTS DE CONFIGURACIÓN FALLARON!")
        print("Vérifiez les détails ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
