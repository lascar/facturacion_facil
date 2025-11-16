#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation complète du système stocks-factures 2024
Script de validation globale avec tous les tests
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_test(test_file, description):
    """Exécute un test et retourne le résultat"""
    print(f"\n🧪 {description}")
    print("-" * 50)
    
    try:
        # Exécuter le test
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {description} - RÉUSSI")
            return True
        else:
            print(f"❌ {description} - ÉCHOUÉ")
            print(f"Erreur: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERREUR: {e}")
        return False

def validation_complete():
    """Validation complète du système"""
    print("🎯 VALIDATION COMPLÈTE SYSTÈME STOCKS-FACTURES 2024")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Liste des tests à exécuter
    tests = [
        ("demo_relation_stocks_factures.py", "Démonstration Relation Stocks-Factures"),
        ("test_relation_stocks_factures_complet.py", "Test Complet End-to-End"),
        ("test_bouton_actualizar.py", "Test Bouton Actualizar Corrigé"),
        ("test_symboles_boutons.py", "Test Boutons +/- avec Symboles"),
    ]
    
    results = []
    
    print("🚀 EXÉCUTION DE LA SUITE DE TESTS")
    print("=" * 40)
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            success = run_test(test_file, description)
            results.append((description, success))
        else:
            print(f"⚠️ {description} - FICHIER NON TROUVÉ: {test_file}")
            results.append((description, False))
    
    # Résumé des résultats
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE LA VALIDATION COMPLÈTE")
    print("=" * 70)
    
    total_tests = len(results)
    tests_reussis = sum(1 for _, success in results if success)
    tests_echoues = total_tests - tests_reussis
    
    print(f"📈 STATISTIQUES:")
    print(f"   • Total des tests: {total_tests}")
    print(f"   • Tests réussis: {tests_reussis}")
    print(f"   • Tests échoués: {tests_echoues}")
    print(f"   • Taux de réussite: {(tests_reussis/total_tests)*100:.1f}%")
    
    print(f"\n📋 DÉTAIL DES RÉSULTATS:")
    for description, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"   • {description}: {status}")
    
    # Validation globale
    if tests_reussis == total_tests:
        print(f"\n🎉 VALIDATION COMPLÈTE RÉUSSIE À 100% !")
        print(f"\n✨ SYSTÈME VALIDÉ:")
        print(f"   ✅ Relation stocks-factures parfaitement opérationnelle")
        print(f"   ✅ Bouton Actualizar corrigé et fonctionnel")
        print(f"   ✅ Interface utilisateur cohérente")
        print(f"   ✅ Base de données synchronisée")
        print(f"   ✅ Notifications et feedback utilisateur")
        print(f"   ✅ Logs et traçabilité complets")
        
        print(f"\n🚀 PRÊT POUR UTILISATION EN PRODUCTION !")
        
        # Instructions d'utilisation
        print(f"\n📖 UTILISATION RECOMMANDÉE:")
        print(f"   1. python main.py → Créer factures normalement")
        print(f"   2. Stock → '🔄 Actualizar' → Voir changements")
        print(f"   3. Utiliser +/- pour ajustements rapides")
        print(f"   4. '📝 Editar Stock' pour modifications précises")
        
        return True
    else:
        print(f"\n❌ VALIDATION INCOMPLÈTE")
        print(f"   {tests_echoues} test(s) ont échoué")
        print(f"   Vérifiez les erreurs ci-dessus")
        return False

def verification_fichiers():
    """Vérifie la présence des fichiers essentiels"""
    print("\n🔍 VÉRIFICATION DES FICHIERS ESSENTIELS")
    print("-" * 40)
    
    fichiers_essentiels = [
        "ui/stock_pyqt6.py",
        "database/database.py", 
        "ui/factura_editor_pyqt6.py",
        "GUIDE_COMPLET_STOCKS_FACTURES_2024.md",
        "DOCUMENTATION_TECHNIQUE_STOCKS.md"
    ]
    
    tous_presents = True
    
    for fichier in fichiers_essentiels:
        if os.path.exists(fichier):
            print(f"   ✅ {fichier}")
        else:
            print(f"   ❌ {fichier} - MANQUANT")
            tous_presents = False
    
    if tous_presents:
        print("✅ Tous les fichiers essentiels sont présents")
    else:
        print("❌ Certains fichiers essentiels sont manquants")
    
    return tous_presents

def main():
    """Fonction principale"""
    try:
        # Vérification des fichiers
        fichiers_ok = verification_fichiers()
        
        if not fichiers_ok:
            print("\n❌ Impossible de continuer - fichiers manquants")
            return 1
        
        # Validation complète
        success = validation_complete()
        
        if success:
            print(f"\n🎊 VALIDATION GLOBALE RÉUSSIE !")
            print(f"Le système stocks-factures est parfaitement opérationnel.")
            return 0
        else:
            print(f"\n⚠️ VALIDATION GLOBALE INCOMPLÈTE")
            print(f"Certains tests ont échoué - vérifiez les détails ci-dessus.")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Validation interrompue par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
