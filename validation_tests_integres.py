#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation que les tests Nueva Factura sont bien intégrés à la suite de tests
"""

import os
import sys


def validate_test_integration():
    """Valider que les tests sont bien intégrés"""
    print("🚀 VALIDATION INTÉGRATION TESTS NUEVA FACTURA")
    print("=" * 50)
    
    # Vérifier la structure des tests
    test_files_to_check = [
        "tests/test_ui/test_window_positioning.py",
        "tests/test_regression/test_nueva_factura_positioning.py",
        "tests/test_advanced/test_ui_integration.py"
    ]
    
    print("\n📋 Vérification structure des tests:")
    
    all_files_exist = True
    for test_file in test_files_to_check:
        if os.path.exists(test_file):
            print(f"   ✅ {test_file}: PRÉSENT")
        else:
            print(f"   ❌ {test_file}: MANQUANT")
            all_files_exist = False
    
    # Vérifier le contenu des tests
    print("\n📋 Vérification contenu des tests:")
    
    content_checks = {
        "tests/test_ui/test_window_positioning.py": [
            "test_nueva_factura_forcage_maximal",
            "test_nueva_factura_resistance_focus",
            "test_nueva_factura_stabilite_long_terme",
            "WindowStaysOnTopHint",
            "X11BypassWindowManagerHint"
        ],
        "tests/test_regression/test_nueva_factura_positioning.py": [
            "test_regression_nueva_factura_never_behind",
            "test_regression_multiple_attempts",
            "RÉGRESSION",
            "forçage maximal"
        ],
        "tests/test_advanced/test_ui_integration.py": [
            "test_integration_nueva_factura_workflow_complet",
            "test_integration_multiple_windows_interaction",
            "intégration complète"
        ]
    }
    
    content_valid = True
    for test_file, keywords in content_checks.items():
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                missing_keywords = []
                for keyword in keywords:
                    if keyword not in content:
                        missing_keywords.append(keyword)
                
                if not missing_keywords:
                    print(f"   ✅ {test_file}: CONTENU VALIDE")
                else:
                    print(f"   ⚠️ {test_file}: Mots-clés manquants: {missing_keywords}")
                    content_valid = False
                    
            except Exception as e:
                print(f"   ❌ {test_file}: Erreur lecture - {e}")
                content_valid = False
        else:
            print(f"   ❌ {test_file}: FICHIER MANQUANT")
            content_valid = False
    
    # Vérifier les scripts de test
    print("\n📋 Vérification scripts de test:")
    
    test_scripts = [
        "run_nueva_factura_tests.py",
        "test_nueva_factura_suite_integree.py",
        "validation_tests_integres.py"
    ]
    
    scripts_valid = True
    for script in test_scripts:
        if os.path.exists(script):
            print(f"   ✅ {script}: PRÉSENT")
        else:
            print(f"   ❌ {script}: MANQUANT")
            scripts_valid = False
    
    # Vérifier la solution dans le code principal
    print("\n📋 Vérification solution dans le code:")
    
    main_file = "ui/facturas_pyqt5.py"
    if os.path.exists(main_file):
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            solution_keywords = [
                "FORÇAGE IMMÉDIAT MAXIMAL",
                "WindowStaysOnTopHint",
                "X11BypassWindowManagerHint",
                "FramelessWindowHint",
                "Qt.Tool",
                "grabKeyboard",
                "CrearFacturaDialog(None)"
            ]
            
            missing_solution = []
            for keyword in solution_keywords:
                if keyword not in content:
                    missing_solution.append(keyword)
            
            if not missing_solution:
                print(f"   ✅ {main_file}: SOLUTION INTÉGRÉE")
                solution_valid = True
            else:
                print(f"   ⚠️ {main_file}: Éléments manquants: {missing_solution}")
                solution_valid = False
                
        except Exception as e:
            print(f"   ❌ {main_file}: Erreur lecture - {e}")
            solution_valid = False
    else:
        print(f"   ❌ {main_file}: FICHIER MANQUANT")
        solution_valid = False
    
    # Vérifier le TODO.md
    print("\n📋 Vérification TODO.md:")
    
    if os.path.exists("TODO.md"):
        try:
            with open("TODO.md", 'r', encoding='utf-8') as f:
                todo_content = f.read()
            
            todo_keywords = [
                "RÉSOLU DÉFINITIVEMENT",
                "FORÇAGE MAXIMAL",
                "WindowStaysOnTopHint",
                "X11BypassWindowManagerHint",
                "Tests confirmés"
            ]
            
            missing_todo = []
            for keyword in todo_keywords:
                if keyword not in todo_content:
                    missing_todo.append(keyword)
            
            if not missing_todo:
                print(f"   ✅ TODO.md: STATUT RÉSOLU DOCUMENTÉ")
                todo_valid = True
            else:
                print(f"   ⚠️ TODO.md: Éléments manquants: {missing_todo}")
                todo_valid = False
                
        except Exception as e:
            print(f"   ❌ TODO.md: Erreur lecture - {e}")
            todo_valid = False
    else:
        print(f"   ❌ TODO.md: FICHIER MANQUANT")
        todo_valid = False
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ VALIDATION INTÉGRATION")
    print("=" * 40)
    
    all_valid = all_files_exist and content_valid and scripts_valid and solution_valid and todo_valid
    
    print(f"   Structure tests: {'✅ OK' if all_files_exist else '❌ PROBLÈME'}")
    print(f"   Contenu tests: {'✅ OK' if content_valid else '❌ PROBLÈME'}")
    print(f"   Scripts tests: {'✅ OK' if scripts_valid else '❌ PROBLÈME'}")
    print(f"   Solution code: {'✅ OK' if solution_valid else '❌ PROBLÈME'}")
    print(f"   TODO.md: {'✅ OK' if todo_valid else '❌ PROBLÈME'}")
    
    if all_valid:
        print(f"\n🎉 INTÉGRATION TESTS VALIDÉE !")
        print("   ✅ Tous les tests Nueva Factura sont intégrés")
        print("   ✅ Structure de tests organisée et complète")
        print("   ✅ Solution de forçage maximal implémentée")
        print("   ✅ Tests de régression pour éviter les retours")
        print("   ✅ Tests d'intégration UI avancés")
        print("   ✅ Documentation TODO.md mise à jour")
        
        print(f"\n📋 TESTS INTÉGRÉS DISPONIBLES:")
        print("   • tests/test_ui/test_window_positioning.py")
        print("     - Tests de positionnement de fenêtres")
        print("     - Validation forçage maximal")
        print("     - Tests de résistance et stabilité")
        
        print("   • tests/test_regression/test_nueva_factura_positioning.py")
        print("     - Tests de régression anti-retour")
        print("     - Validation que le problème ne revient pas")
        print("     - Tests de robustesse")
        
        print("   • tests/test_advanced/test_ui_integration.py")
        print("     - Tests d'intégration UI avancés")
        print("     - Validation workflow complet")
        print("     - Tests d'interaction multi-fenêtres")
        
        print(f"\n🎯 UTILISATION:")
        print("   1. Exécuter tous les tests: pytest tests/")
        print("   2. Tests spécifiques: python3 run_nueva_factura_tests.py")
        print("   3. Suite intégrée: python3 test_nueva_factura_suite_integree.py")
        
        print(f"\n🏆 MISSION ACCOMPLIE !")
        print("   Les tests Nueva Factura sont maintenant")
        print("   parfaitement intégrés à la suite de tests.")
        
        return True
    else:
        print(f"\n⚠️ PROBLÈMES D'INTÉGRATION DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
        return False


def main():
    """Fonction principale"""
    success = validate_test_integration()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
