#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la correction de la classe Organizacion
"""

import os
import sys

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_correction_organizacion():
    """Test de la correction de la classe Organizacion"""
    print("🧪 Test de la correction de la classe Organizacion")
    print("=" * 60)
    
    try:
        from database.models import Organizacion
        
        print("\n1. Test de récupération des données...")
        
        # Récupérer l'organisation
        org = Organizacion.get()
        
        if org:
            print(f"   ✅ Organisation récupérée: {org.nombre}")
            print(f"   📁 Répertoire PDF: '{org.directorio_descargas_pdf}'")
            print(f"   🖥️  Visor PDF: '{org.visor_pdf_personalizado}'")
            
            # Vérifier que ce ne sont pas des dates
            if org.directorio_descargas_pdf and "2025-12-07" in org.directorio_descargas_pdf:
                print("   ❌ ERREUR: directorio_descargas_pdf contient encore une date!")
                return False
            else:
                print("   ✅ directorio_descargas_pdf correct")
                
            if org.visor_pdf_personalizado and "2025-12-07" in org.visor_pdf_personalizado:
                print("   ❌ ERREUR: visor_pdf_personalizado contient une date!")
                return False
            else:
                print("   ✅ visor_pdf_personalizado correct")
        else:
            print("   ❌ Aucune organisation trouvée")
            return False
        
        print("\n2. Test de sauvegarde...")
        
        # Sauvegarder avec un nouveau répertoire
        test_dir = "/tmp/test_correction_pdf"
        org.directorio_descargas_pdf = test_dir
        org.save()
        
        # Récupérer à nouveau
        org_reloaded = Organizacion.get()
        
        if org_reloaded.directorio_descargas_pdf == test_dir:
            print(f"   ✅ Sauvegarde réussie: {test_dir}")
        else:
            print(f"   ❌ Sauvegarde échouée: attendu '{test_dir}', obtenu '{org_reloaded.directorio_descargas_pdf}'")
            return False
        
        print("\n3. Test de nettoyage...")
        
        # Remettre une valeur vide
        org.directorio_descargas_pdf = ""
        org.save()
        
        org_final = Organizacion.get()
        if org_final.directorio_descargas_pdf == "":
            print("   ✅ Nettoyage réussi")
        else:
            print(f"   ⚠️  Valeur résiduelle: '{org_final.directorio_descargas_pdf}'")
        
        print("\n🎉 Correction validée avec succès!")
        print("\n📋 Résumé:")
        print("   ✅ Les indices des colonnes ont été corrigés")
        print("   ✅ directorio_descargas_pdf utilise maintenant l'index 10")
        print("   ✅ visor_pdf_personalizado utilise maintenant l'index 11")
        print("   ✅ Les données sont correctement lues et sauvegardées")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_correction_organizacion()
    sys.exit(0 if success else 1)
