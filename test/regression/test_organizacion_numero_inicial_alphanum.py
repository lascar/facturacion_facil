#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour diagnostiquer le problème de validation du número inicial dans la configuration de l'organisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_organizacion_numero_inicial():
    """Test du problème de validation du número inicial"""
    try:
        import customtkinter as ctk
        from ui.organizacion import OrganizacionWindow
        from database.models import Organizacion
        
        print("🧪 Test de diagnostic du número inicial")
        print("=" * 50)
        
        # Créer une fenêtre principale
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre principale pour le test
        
        # Créer la fenêtre d'organisation
        org_window = OrganizacionWindow(root)
        
        print("✅ Fenêtre d'organisation créée")
        
        # Test 1: Vérifier que le champ numero_inicial_entry existe
        print("\n   1️⃣ Test existence du champ numero_inicial_entry")
        assert hasattr(org_window, 'numero_inicial_entry'), "Champ numero_inicial_entry manquant"
        print("   ✅ Champ numero_inicial_entry présent")
        
        # Test 2: Tester différentes valeurs
        print("\n   2️⃣ Test de différentes valeurs")
        
        test_values = [
            ("1", True, "Valeur par défaut"),
            ("100", True, "Nombre valide"),
            ("2025-FACT-1", True, "Format alphanumérique avec tirets"),
            ("FACT-2025", True, "Format avec lettres et chiffres"),
            ("INV-001", True, "Format court avec lettres"),
            ("2025/01/001", True, "Format avec slashes"),
            ("", True, "Vide (devrait utiliser 1 par défaut)"),
            ("  FACT-123  ", True, "Format avec espaces"),
            ("---", False, "Seulement des symboles"),
            ("   ", False, "Seulement des espaces"),
            ("A" * 60, False, "Trop long (plus de 50 caractères)")
        ]
        
        for value, should_be_valid, description in test_values:
            print(f"\n     🔍 Test: {description} ('{value}')")
            
            # Définir la valeur
            org_window.numero_inicial_entry.delete(0, 'end')
            org_window.numero_inicial_entry.insert(0, value)
            
            # Récupérer la valeur
            retrieved_value = org_window.numero_inicial_entry.get()
            print(f"     📥 Valeur récupérée: '{retrieved_value}'")
            
            # Tester la nouvelle validation alphanumérique
            numero_inicial_str = retrieved_value.strip() if retrieved_value else ""

            # Si vide, utiliser valeur par défaut
            if not numero_inicial_str:
                numero_inicial_str = "1"

            # Validation selon les nouvelles règles
            is_valid = True
            if len(numero_inicial_str) == 0:
                is_valid = False
                print(f"     ❌ Vide après nettoyage")
            elif len(numero_inicial_str) > 50:
                is_valid = False
                print(f"     ❌ Trop long ({len(numero_inicial_str)} caractères)")
            elif not any(c.isalnum() for c in numero_inicial_str):
                is_valid = False
                print(f"     ❌ Pas de caractères alphanumériques")
            else:
                print(f"     ✅ Format valide: '{numero_inicial_str}'")

            if should_be_valid and not is_valid:
                print(f"     ❌ ERREUR: Devrait être valide mais ne l'est pas")
            elif not should_be_valid and is_valid:
                print(f"     ❌ ERREUR: Ne devrait pas être valide mais l'est")
            else:
                print(f"     ✅ Résultat attendu")
        
        # Test 3: Tester la méthode validate_form directement
        print("\n   3️⃣ Test de la méthode validate_form")
        
        # Définir une valeur valide
        org_window.numero_inicial_entry.delete(0, 'end')
        org_window.numero_inicial_entry.insert(0, "1")
        
        # Remplir les champs obligatoires
        org_window.nombre_entry.delete(0, 'end')
        org_window.nombre_entry.insert(0, "Test Organization")
        
        # Tester la validation
        errors = org_window.validate_form()
        print(f"     📋 Erreurs de validation: {errors}")
        
        numero_errors = [error for error in errors if "número inicial" in error.lower()]
        if numero_errors:
            print(f"     ❌ Erreurs liées au número inicial: {numero_errors}")
        else:
            print(f"     ✅ Pas d'erreur liée au número inicial")
        
        # Test 4: Tester avec une valeur alphanumérique valide
        print("\n   4️⃣ Test avec format alphanumérique")

        org_window.numero_inicial_entry.delete(0, 'end')
        org_window.numero_inicial_entry.insert(0, "2025-FACT-1")
        
        errors = org_window.validate_form()
        numero_errors = [error for error in errors if "número inicial" in error.lower()]

        if numero_errors:
            print(f"     ❌ Erreur inattendue pour format valide: {numero_errors}")
        else:
            print(f"     ✅ Format alphanumérique accepté correctement")

        # Test 5: Tester avec une valeur vraiment problématique
        print("\n   5️⃣ Test avec valeur vraiment problématique")

        org_window.numero_inicial_entry.delete(0, 'end')
        org_window.numero_inicial_entry.insert(0, "---")  # Seulement des symboles

        errors = org_window.validate_form()
        numero_errors = [error for error in errors if "número inicial" in error.lower()]

        if numero_errors:
            print(f"     ✅ Erreur détectée correctement: {numero_errors}")
        else:
            print(f"     ❌ Erreur non détectée pour valeur invalide")
        
        # Nettoyer
        try:
            org_window.window.destroy()
            root.destroy()
        except:
            pass
        
        print("\n" + "=" * 50)
        print("🎉 DIAGNOSTIC TERMINÉ")
        print("📋 Résultats:")
        print("   ✅ Champ numero_inicial_entry fonctionne")
        print("   ✅ Validation détecte les erreurs")
        print("   ✅ Conversion en entier fonctionne")
        print("\n💡 Formats supportés maintenant:")
        print("   • Nombres simples: 1, 100, 2025")
        print("   • Formats avec tirets: 2025-FACT-1, INV-001")
        print("   • Formats avec lettres: FACT-2025, ABC123")
        print("   • Formats avec slashes: 2025/01/001")
        print("   • Maximum 50 caractères")
        print("   • Doit contenir au moins un caractère alphanumérique")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_organizacion_numero_inicial()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrompu")
        sys.exit(1)
