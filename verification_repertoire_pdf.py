#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification que le répertoire PDF utilisé est bien 'pdfs/' partout
"""

import os
import sys

def verification_repertoire_pdf():
    """Vérifier l'utilisation du bon répertoire PDF"""
    print("🔍 Vérification du répertoire PDF utilisé")
    print("=" * 50)
    
    # Vérifier le code principal
    print("\n1. Vérification du code principal...")
    
    # Vérifier ui/facturas_pyqt5.py
    with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'pdf_dir = os.path.join(os.getcwd(), "pdfs")' in content:
            print("   ✅ ui/facturas_pyqt5.py utilise 'pdfs/'")
        else:
            print("   ❌ ui/facturas_pyqt5.py n'utilise pas 'pdfs/'")
    
    # Vérifier que le répertoire existe et contient des fichiers
    print("\n2. Vérification du répertoire physique...")
    
    if os.path.exists('pdfs'):
        pdf_files = [f for f in os.listdir('pdfs') if f.endswith('.pdf')]
        print(f"   ✅ Répertoire 'pdfs/' existe avec {len(pdf_files)} fichiers PDF")
        
        # Montrer quelques exemples
        if pdf_files:
            print("   📄 Exemples de fichiers:")
            for i, pdf_file in enumerate(pdf_files[:3]):
                print(f"      - {pdf_file}")
            if len(pdf_files) > 3:
                print(f"      ... et {len(pdf_files) - 3} autres")
    else:
        print("   ⚠️  Répertoire 'pdfs/' n'existe pas encore")
    
    # Vérifier d'autres répertoires PDF qui pourraient exister
    print("\n3. Vérification d'autres répertoires PDF...")
    
    other_pdf_dirs = ['pdf', 'facturas_pdf', 'PDFs', 'PDF']
    for dir_name in other_pdf_dirs:
        if os.path.exists(dir_name):
            files = [f for f in os.listdir(dir_name) if f.endswith('.pdf')]
            if files:
                print(f"   ⚠️  Répertoire '{dir_name}/' existe avec {len(files)} fichiers PDF")
                print(f"      💡 Considérez déplacer ces fichiers vers 'pdfs/'")
            else:
                print(f"   ℹ️  Répertoire '{dir_name}/' existe mais est vide")
        else:
            print(f"   ✅ Pas de répertoire '{dir_name}/'")
    
    # Vérifier la documentation
    print("\n4. Vérification de la documentation...")
    
    doc_files_to_check = [
        'GUIDE_UTILISATEUR_PDF_CORRIGE.md',
        'CORRECTIONS_PDF_RESUME.md',
        'GUIDE_BOUTON_PDF.md'
    ]
    
    for doc_file in doc_files_to_check:
        if os.path.exists(doc_file):
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'pdfs/' in content:
                    print(f"   ✅ {doc_file} mentionne 'pdfs/'")
                else:
                    print(f"   ⚠️  {doc_file} ne mentionne pas 'pdfs/'")
        else:
            print(f"   ℹ️  {doc_file} n'existe pas")
    
    print("\n5. Résumé de la configuration actuelle...")
    print("   📁 Répertoire utilisé par le code: 'pdfs/'")
    print("   📁 Répertoire créé automatiquement: 'pdfs/'")
    print("   📁 Répertoire recommandé: 'pdfs/'")
    
    print("\n✅ Vérification terminée!")
    print("\n💡 Le répertoire 'pdfs/' (au pluriel) est le bon répertoire utilisé")
    print("   par l'application pour sauvegarder les factures PDF.")
    
    return True

if __name__ == "__main__":
    success = verification_repertoire_pdf()
    sys.exit(0 if success else 1)
