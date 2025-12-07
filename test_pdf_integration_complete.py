#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration complet pour la génération PDF avec une vraie facture
"""

import os
import sys
import tempfile
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pdf_integration_complete():
    """Test d'intégration complet avec base de données"""
    print("🧪 Test d'intégration PDF complet")
    print("=" * 50)
    
    try:
        # Importer les modules nécessaires
        from database.database import Database
        from utils.pdf_generator import PDFGenerator

        # Initialiser la base de données
        db = Database()
        
        # 1. Vérifier qu'il y a des factures dans la base
        print("\n1. Vérification des factures existantes...")
        invoices = db.get_all_invoices()
        
        if not invoices:
            print("   ⚠️  Aucune facture trouvée dans la base de données")
            print("   💡 Créez une facture dans l'application pour tester")
            return True
        
        print(f"   ✅ {len(invoices)} facture(s) trouvée(s)")
        
        # Prendre la première facture
        first_invoice = invoices[0]
        print(f"   📄 Test avec facture: {first_invoice.get('numero', 'N/A')}")
        
        # 2. Récupérer les détails complets de la facture
        print("\n2. Récupération des détails de la facture...")
        invoice_data = db.get_invoice_by_id(first_invoice['id'])
        
        if not invoice_data:
            print("   ❌ Impossible de récupérer les détails de la facture")
            return False
        
        print(f"   ✅ Facture récupérée: {invoice_data.get('numero', 'N/A')}")
        print(f"   👤 Client: {invoice_data.get('cliente', {}).get('nombre', 'N/A')}")
        print(f"   📊 Total: {invoice_data.get('total', 0):.2f}€")
        print(f"   📝 Lignes: {len(invoice_data.get('lineas', []))}")
        
        # Afficher les détails des lignes
        for i, linea in enumerate(invoice_data.get('lineas', []), 1):
            print(f"      Ligne {i}: {linea.get('producto_nombre', 'N/A')} "
                  f"(Ref: {linea.get('producto_referencia', 'N/A')}) "
                  f"x{linea.get('cantidad', 0)} = {linea.get('total', 0):.2f}€")
        
        # 3. Générer le PDF
        print("\n3. Génération du PDF...")
        
        # Créer le dossier pdfs s'il n'existe pas
        pdf_dir = os.path.join(os.getcwd(), "pdfs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        # Nom du fichier PDF
        numero_safe = str(invoice_data.get('numero', 'TEST')).replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Test_Factura_{numero_safe}_{timestamp}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Désactiver l'ouverture automatique pour le test
        os.environ['TESTING'] = '1'
        
        try:
            pdf_generator = PDFGenerator()
            success = pdf_generator.generate_invoice_pdf(invoice_data, pdf_path)
            
            if success and os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   ✅ PDF généré avec succès!")
                print(f"   📄 Fichier: {pdf_filename}")
                print(f"   📁 Chemin: {pdf_path}")
                print(f"   📊 Taille: {file_size} bytes")
                
                # Vérifications du contenu
                print("\n4. Vérifications du contenu...")
                
                # Vérifier que le fichier n'est pas vide
                if file_size > 5000:
                    print("   ✅ Taille du fichier correcte (>5KB)")
                else:
                    print("   ⚠️  Fichier PDF petit (<5KB)")
                
                # Le fichier reste pour inspection manuelle
                print(f"\n📋 Le fichier PDF a été sauvegardé pour inspection:")
                print(f"   {pdf_path}")
                print(f"\n💡 Ouvrez ce fichier pour vérifier:")
                print(f"   - Le logo s'affiche correctement")
                print(f"   - Les noms des produits sont corrects")
                print(f"   - Les références des produits sont visibles")
                
                return True
                
            else:
                print("   ❌ Échec de la génération PDF")
                return False
                
        finally:
            # Nettoyer la variable d'environnement
            if 'TESTING' in os.environ:
                del os.environ['TESTING']
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_integration_complete()
    sys.exit(0 if success else 1)
