#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter tous les tests liés à la solution Nueva Factura
Tests intégrés dans la suite de tests pour le forçage maximal
"""

import subprocess
import sys
import os


def run_test_suite():
    """Exécuter la suite de tests Nueva Factura"""
    print("🚀 EXÉCUTION SUITE DE TESTS NUEVA FACTURA")
    print("=" * 50)
    
    # Tests à exécuter dans l'ordre
    test_files = [
        "tests/test_ui/test_window_positioning.py",
        "tests/test_regression/test_nueva_factura_positioning.py", 
        "tests/test_advanced/test_ui_integration.py"
    ]
    
    results = {}
    
    for test_file in test_files:
        print(f"\n📋 Exécution: {test_file}")
        print("-" * 40)
        
        try:
            # Exécuter le test avec pytest
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--tb=short"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print(f"✅ {test_file}: SUCCÈS")
                results[test_file] = "SUCCÈS"
            else:
                print(f"❌ {test_file}: ÉCHEC")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                results[test_file] = "ÉCHEC"
                
        except Exception as e:
            print(f"❌ {test_file}: ERREUR - {e}")
            results[test_file] = f"ERREUR - {e}"
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ SUITE DE TESTS NUEVA FACTURA")
    print("=" * 50)
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file, status in results.items():
        status_icon = "✅" if status == "SUCCÈS" else "❌"
        print(f"{status_icon} {test_file}: {status}")
        if status == "SUCCÈS":
            success_count += 1
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Tests réussis: {success_count}/{total_count}")
    print(f"   Taux de réussite: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print(f"\n🎉 TOUS LES TESTS NUEVA FACTURA RÉUSSIS !")
        print("   ✅ Solution de forçage maximal validée")
        print("   ✅ Tests de régression passés")
        print("   ✅ Intégration UI confirmée")
        print("   ✅ Problème 'dialog en second plan' définitivement résolu")
        
        print(f"\n📋 SOLUTION INTÉGRÉE:")
        print("   • Tests de positionnement de fenêtres")
        print("   • Tests de régression anti-retour")
        print("   • Tests d'intégration UI avancés")
        print("   • Validation complète de la solution")
        
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print("   1. Les tests sont maintenant intégrés à la suite")
        print("   2. Exécuter 'pytest tests/' pour tous les tests")
        print("   3. La solution est protégée contre les régressions")
        print("   4. Le problème Nueva Factura est définitivement résolu")
        
        return True
    else:
        print(f"\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifier les détails ci-dessus")
        return False


def run_individual_test(test_name):
    """Exécuter un test individuel"""
    test_mapping = {
        "positioning": "tests/test_ui/test_window_positioning.py",
        "regression": "tests/test_regression/test_nueva_factura_positioning.py",
        "integration": "tests/test_advanced/test_ui_integration.py"
    }
    
    if test_name not in test_mapping:
        print(f"❌ Test '{test_name}' non trouvé")
        print(f"Tests disponibles: {', '.join(test_mapping.keys())}")
        return False
    
    test_file = test_mapping[test_name]
    print(f"🚀 Exécution test individuel: {test_file}")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_file, 
            "-v", 
            "--tb=long"
        ], cwd=os.getcwd())
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur exécution test: {e}")
        return False


def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        # Exécuter un test spécifique
        test_name = sys.argv[1]
        success = run_individual_test(test_name)
    else:
        # Exécuter toute la suite
        success = run_test_suite()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
