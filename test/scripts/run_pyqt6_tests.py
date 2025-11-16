#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter tous les tests PyQt6
"""

import sys
import os
import subprocess
import time

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def run_test_file(test_file, description):
    """Exécute un fichier de test spécifique"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"📁 Fichier: {test_file}")
    print('='*60)
    
    if not os.path.exists(test_file):
        print(f"❌ Fichier de test non trouvé: {test_file}")
        return False
    
    try:
        start_time = time.time()
        
        # Exécuter pytest sur le fichier
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_file, 
            '-v', 
            '--tb=short',
            '--no-header'
        ], capture_output=True, text=True, cwd=project_root)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Durée: {duration:.2f}s")
        
        if result.returncode == 0:
            print("✅ Tests réussis!")
            print(result.stdout)
            return True
        else:
            print("❌ Tests échoués!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False

def run_pyqt6_tests():
    """Exécute tous les tests PyQt6"""
    print("🚀 EXÉCUTION DES TESTS PYQT6")
    print("="*60)
    print(f"📍 Répertoire de travail: {project_root}")
    
    # Vérifier que PyQt6 est installé
    try:
        import PyQt6
        print("✅ PyQt6 est disponible")
    except ImportError:
        print("❌ PyQt6 n'est pas installé. Installez-le avec: pip install PyQt6")
        return False
    
    # Définir les tests à exécuter
    tests = [
        ("test/integration/test_pyqt6_integration.py", "Tests d'intégration PyQt6"),
        ("test/ui/test_pyqt6_ui.py", "Tests UI PyQt6"),
        ("test/integration/test_gui_abstraction.py", "Tests d'abstraction GUI (avec PyQt6)"),
        ("test_pyqt6.py", "Tests de base PyQt6"),
    ]
    
    results = []
    total_start_time = time.time()
    
    for test_file, description in tests:
        test_path = os.path.join(project_root, test_file)
        success = run_test_file(test_path, description)
        results.append((test_file, description, success))
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Résumé des résultats
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES TESTS PYQT6")
    print('='*60)
    
    successful_tests = 0
    for test_file, description, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{description:<40} {status}")
        if success:
            successful_tests += 1
    
    print(f"\n📈 Résultats: {successful_tests}/{len(results)} tests réussis")
    print(f"⏱️  Durée totale: {total_duration:.2f}s")
    
    if successful_tests == len(results):
        print("\n🎉 TOUS LES TESTS PYQT6 ONT RÉUSSI!")
        print("\n✨ Votre migration PyQt6 est validée!")
        return True
    else:
        print(f"\n⚠️  {len(results) - successful_tests} test(s) ont échoué")
        print("Vérifiez les erreurs ci-dessus pour plus de détails.")
        return False

def run_performance_comparison():
    """Compare les performances entre les frameworks"""
    print(f"\n{'='*60}")
    print("⚡ COMPARAISON DES PERFORMANCES")
    print('='*60)
    
    try:
        comparison_script = os.path.join(project_root, "compare_frameworks.py")
        if os.path.exists(comparison_script):
            result = subprocess.run([sys.executable, comparison_script], 
                                  capture_output=True, text=True, cwd=project_root)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("❌ Erreur lors de la comparaison des performances")
                print(result.stderr)
        else:
            print("⚠️  Script de comparaison non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🔬 SUITE DE TESTS PYQT6")
    print("="*60)
    print("Ce script exécute tous les tests pour valider la migration PyQt6")
    
    # Exécuter les tests
    success = run_pyqt6_tests()
    
    # Comparaison des performances (optionnel)
    if success:
        run_performance_comparison()
    
    # Instructions finales
    print(f"\n{'='*60}")
    print("📋 PROCHAINES ÉTAPES")
    print('='*60)
    
    if success:
        print("""
✅ Migration PyQt6 validée avec succès!

🚀 Vous pouvez maintenant:
1. Lancer votre application: python main.py
2. Profiter des performances améliorées
3. Explorer les nouvelles fonctionnalités PyQt6

📚 Documentation:
- Tests PyQt6: test/integration/test_pyqt6_integration.py
- Tests UI: test/ui/test_pyqt6_ui.py
- Comparaison: compare_frameworks.py
""")
    else:
        print("""
⚠️  Certains tests ont échoué

🔧 Actions recommandées:
1. Vérifiez que PyQt6 est correctement installé
2. Examinez les erreurs de test ci-dessus
3. Corrigez les problèmes identifiés
4. Relancez les tests

💡 Aide:
- Validation: python validate_pyqt6_migration.py
- Tests de base: python test_pyqt6.py
""")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
