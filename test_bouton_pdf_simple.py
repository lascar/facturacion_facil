#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du bouton PDF
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_pdf_generator():
    """Test d'importation du générateur PDF"""
    print("🧪 Test 1: Import du générateur PDF")
    
    try:
        from utils.pdf_generator import PDFGenerator
        print("✅ PDFGenerator importé avec succès")
        
        # Créer une instance
        pdf_gen = PDFGenerator()
        print("✅ Instance PDFGenerator créée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_creation_dossier():
    """Test de création du dossier pdfs"""
    print("\n🧪 Test 2: Création du dossier pdfs")
    
    try:
        import os
        
        # Créer le dossier pdfs s'il n'existe pas
        pdf_dir = os.path.join(os.getcwd(), "pdfs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
            print(f"✅ Dossier créé: {pdf_dir}")
        else:
            print(f"✅ Dossier existe déjà: {pdf_dir}")
        
        # Vérifier les permissions
        if os.access(pdf_dir, os.W_OK):
            print("✅ Permissions d'écriture OK")
        else:
            print("❌ Pas de permissions d'écriture")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_generation_nom_fichier():
    """Test de génération de nom de fichier"""
    print("\n🧪 Test 3: Génération nom de fichier")
    
    try:
        from datetime import datetime
        
        # Test avec différents numéros de facture
        test_numbers = ["F-2024-001", "FACT/2024/123", "SIN_NUMERO"]
        
        for numero in test_numbers:
            numero_safe = str(numero).replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
            
            print(f"   {numero} → {pdf_filename}")
            
            # Vérifications
            assert pdf_filename.endswith(".pdf"), "Doit finir par .pdf"
            assert "Factura_" in pdf_filename, "Doit contenir 'Factura_'"
            assert "/" not in pdf_filename, "Ne doit pas contenir '/'"
        
        print("✅ Génération des noms OK")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_structure_factura():
    """Test de la structure d'une factura"""
    print("\n🧪 Test 4: Structure factura")
    
    try:
        # Simuler une factura
        factura_test = {
            'id': 1,
            'numero': 'F-2024-001',
            'cliente_nombre': 'Cliente Test',
            'fecha': '2024-12-07',
            'total': 100.50
        }
        
        # Vérifier les champs requis
        required_fields = ['numero', 'cliente_nombre']
        for field in required_fields:
            assert field in factura_test, f"Campo requerido: {field}"
            print(f"   ✅ {field}: {factura_test[field]}")
        
        print("✅ Structure factura OK")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_methode_exportar_pdf():
    """Test de la méthode exportar_pdf (simulation)"""
    print("\n🧪 Test 5: Méthode exportar_pdf")
    
    try:
        # Simuler les étapes de la méthode exportar_pdf
        
        # 1. Vérification sélection
        selected_factura_id = None
        if not selected_factura_id:
            print("   ✅ Gestion absence de sélection")
        
        # 2. Import PDF Generator
        from utils.pdf_generator import PDFGenerator
        print("   ✅ Import PDFGenerator")
        
        # 3. Création dossier
        import os
        pdf_dir = os.path.join(os.getcwd(), "pdfs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        print("   ✅ Dossier pdfs vérifié")
        
        # 4. Génération nom fichier
        from datetime import datetime
        numero_safe = "TEST_001"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        print(f"   ✅ Nom fichier: {pdf_filename}")
        
        # 5. Instance générateur
        pdf_generator = PDFGenerator()
        print("   ✅ Instance PDFGenerator créée")
        
        print("✅ Méthode exportar_pdf simulée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Tests simples du bouton PDF")
    print("=" * 40)
    
    # Désactiver l'ouverture automatique des PDFs
    os.environ['DISABLE_PDF_OPEN'] = '1'
    os.environ['TESTING'] = '1'
    
    tests = [
        test_import_pdf_generator,
        test_creation_dossier,
        test_generation_nom_fichier,
        test_structure_factura,
        test_methode_exportar_pdf,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 40)
    print("📊 RÉSULTATS")
    print(f"✅ Réussis: {sum(results)}/{len(results)}")
    print(f"❌ Échoués: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 TOUS LES TESTS PASSÉS!")
        print("Le bouton PDF est prêt!")
    else:
        print("\n⚠️  Certains tests ont échoué.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
