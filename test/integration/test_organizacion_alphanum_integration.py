#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour la nouvelle fonctionnalité de numéro initial alphanumérique
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_organizacion_alphanum_integration():
    """Test d'intégration complet pour les numéros alphanumériques"""
    try:
        import customtkinter as ctk
        from ui.organizacion import OrganizacionWindow
        from database.models import Organizacion
        
        print("🧪 Test d'intégration: Numéros alphanumériques")
        print("=" * 60)
        
        # Créer une fenêtre principale
        root = ctk.CTk()
        root.withdraw()
        
        # Test 1: Sauvegarder avec format alphanumérique
        print("\n   1️⃣ Test sauvegarde avec format alphanumérique")
        
        org_window = OrganizacionWindow(root)
        
        # Remplir les champs obligatoires
        org_window.nombre_entry.delete(0, 'end')
        org_window.nombre_entry.insert(0, "Test Organization Alpha")
        
        # Définir un numéro initial alphanumérique
        test_numero = "2025-FACT-001"
        org_window.numero_inicial_entry.delete(0, 'end')
        org_window.numero_inicial_entry.insert(0, test_numero)
        
        # Valider le formulaire
        errors = org_window.validate_form()
        assert len(errors) == 0, f"Erreurs de validation inattendues: {errors}"
        print(f"     ✅ Validation réussie pour: '{test_numero}'")
        
        # Simuler la sauvegarde (sans fermer la fenêtre)
        try:
            organizacion = Organizacion(
                nombre=org_window.nombre_entry.get().strip(),
                cif=org_window.cif_entry.get().strip(),
                direccion=org_window.direccion_entry.get().strip(),
                telefono=org_window.telefono_entry.get().strip(),
                email=org_window.email_entry.get().strip(),
                logo_path="",
                directorio_imagenes_defecto=org_window.directorio_entry.get().strip(),
                numero_factura_inicial=org_window.numero_inicial_entry.get().strip() or "1",
                directorio_descargas_pdf=org_window.directorio_pdf_entry.get().strip(),
                visor_pdf_personalizado=org_window.visor_pdf_entry.get().strip()
            )
            
            organizacion.save()
            print(f"     ✅ Sauvegarde réussie")
            
        except Exception as e:
            print(f"     ❌ Erreur de sauvegarde: {e}")
            raise
        
        org_window.window.destroy()
        
        # Test 2: Recharger et vérifier
        print("\n   2️⃣ Test rechargement des données")
        
        org_reloaded = Organizacion.get()
        assert org_reloaded is not None, "Organisation non trouvée après sauvegarde"
        assert org_reloaded.numero_factura_inicial == test_numero, \
            f"Numéro initial incorrect: '{org_reloaded.numero_factura_inicial}' != '{test_numero}'"
        
        print(f"     ✅ Numéro rechargé correctement: '{org_reloaded.numero_factura_inicial}'")
        
        # Test 3: Interface de rechargement
        print("\n   3️⃣ Test interface de rechargement")
        
        org_window2 = OrganizacionWindow(root)
        
        # Vérifier que le champ est rempli correctement
        loaded_numero = org_window2.numero_inicial_entry.get()
        assert loaded_numero == test_numero, \
            f"Numéro dans l'interface incorrect: '{loaded_numero}' != '{test_numero}'"
        
        print(f"     ✅ Interface rechargée correctement: '{loaded_numero}'")
        
        org_window2.window.destroy()
        
        # Test 4: Différents formats
        print("\n   4️⃣ Test différents formats alphanumériques")
        
        test_formats = [
            "INV-2025-001",
            "FACTURA_123",
            "2025/FACT/001",
            "F001",
            "123ABC",
            "SÉRIE-A-001"
        ]
        
        for test_format in test_formats:
            org_window3 = OrganizacionWindow(root)
            
            # Remplir les champs
            org_window3.nombre_entry.delete(0, 'end')
            org_window3.nombre_entry.insert(0, f"Test {test_format}")
            
            org_window3.numero_inicial_entry.delete(0, 'end')
            org_window3.numero_inicial_entry.insert(0, test_format)
            
            # Valider
            errors = org_window3.validate_form()
            assert len(errors) == 0, f"Erreurs pour format '{test_format}': {errors}"
            
            # Sauvegarder
            organizacion = Organizacion(
                nombre=f"Test {test_format}",
                numero_factura_inicial=test_format
            )
            organizacion.save()
            
            # Vérifier
            org_check = Organizacion.get()
            assert org_check.numero_factura_inicial == test_format, \
                f"Format mal sauvegardé: '{org_check.numero_factura_inicial}' != '{test_format}'"
            
            print(f"     ✅ Format '{test_format}' validé")
            
            org_window3.window.destroy()
        
        # Nettoyer
        root.destroy()
        
        print("\n" + "=" * 60)
        print("🎉 TEST D'INTÉGRATION RÉUSSI")
        print("📋 Fonctionnalités validées:")
        print("   ✅ Validation alphanumérique")
        print("   ✅ Sauvegarde en base de données")
        print("   ✅ Rechargement des données")
        print("   ✅ Interface utilisateur")
        print("   ✅ Différents formats supportés")
        print("\n✨ Le numéro initial alphanumérique fonctionne parfaitement !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le test d'intégration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_organizacion_alphanum_integration()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrompu")
        sys.exit(1)
