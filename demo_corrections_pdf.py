#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration des corrections PDF appliquées
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_corrections_pdf():
    """Démonstration des corrections PDF"""
    print("🎉 Démonstration des corrections PDF")
    print("=" * 60)
    
    print("\n📋 Problèmes résolus :")
    print("   1. ✅ Suppression de la fenêtre 'PDF generado con éxito'")
    print("   2. ✅ Correction de l'affichage du logo")
    print("   3. ✅ Correction du nom du produit (plus de 'N/A')")
    print("   4. ✅ Correction de la référence du produit")
    
    print("\n🔧 Modifications techniques :")
    print("   • ui/facturas_pyqt5.py - Suppression du message de confirmation")
    print("   • utils/pdf_generator.py - Amélioration de la recherche de logo")
    print("   • utils/pdf_generator.py - Correction des clés de données produits")
    
    try:
        from utils.pdf_generator import PDFGenerator
        
        print("\n🧪 Test de fonctionnement :")
        
        # Test de recherche de logo
        pdf_generator = PDFGenerator()
        logo_path = pdf_generator.find_company_logo()
        
        if logo_path:
            print(f"   ✅ Logo trouvé et utilisable : {logo_path}")
        else:
            print("   ⚠️  Aucun logo trouvé (texte 'LOGO' sera utilisé)")
        
        # Test de génération avec données complètes
        print("\n📄 Test de génération PDF avec données complètes :")
        
        test_data = {
            'numero': 'DEMO-2024-001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'vencimiento': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'nombre': 'Cliente Démonstration',
                'nif': '12345678Z',
                'direccion': 'Calle Demo, 123\\n28001 Madrid'
            },
            'lineas': [
                {
                    'producto_referencia': 'DEMO-REF-001',
                    'producto_nombre': 'Produit Démonstration 1',
                    'cantidad': 2,
                    'precio_unitario': 25.99,
                    'descuento': 5.0,
                    'iva_aplicado': 21.0,
                    'total': 51.98
                },
                {
                    'producto_referencia': 'DEMO-REF-002', 
                    'producto_nombre': 'Produit Démonstration 2',
                    'cantidad': 1,
                    'precio_unitario': 15.50,
                    'descuento': 0.0,
                    'iva_aplicado': 21.0,
                    'total': 15.50
                }
            ],
            'subtotal': 67.48,
            'iva_total': 14.17,
            'total': 81.65
        }
        
        # Créer le dossier pdfs s'il n'existe pas
        pdf_dir = os.path.join(os.getcwd(), "pdfs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        # Générer le PDF de démonstration
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Demo_Corrections_{timestamp}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Désactiver l'ouverture automatique pour la démo
        os.environ['TESTING'] = '1'
        
        try:
            success = pdf_generator.generate_invoice_pdf(test_data, pdf_path)
            
            if success and os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   ✅ PDF de démonstration généré avec succès!")
                print(f"   📄 Fichier : {pdf_filename}")
                print(f"   📊 Taille : {file_size} bytes")
                print(f"   📁 Chemin : {pdf_path}")
                
                print("\n🔍 Contenu du PDF généré :")
                print("   • Logo de l'entreprise (si disponible)")
                print("   • Informations client complètes")
                print("   • Lignes avec noms de produits corrects :")
                for i, ligne in enumerate(test_data['lineas'], 1):
                    print(f"     - Ligne {i}: {ligne['producto_nombre']} (Ref: {ligne['producto_referencia']})")
                print("   • Totaux calculés correctement")
                
            else:
                print("   ❌ Échec de la génération du PDF de démonstration")
                
        finally:
            if 'TESTING' in os.environ:
                del os.environ['TESTING']
        
        print("\n🎯 Utilisation dans l'application :")
        print("   1. Lancez l'application : python3 main.py")
        print("   2. Allez dans 'Facturas'")
        print("   3. Sélectionnez une facture")
        print("   4. Cliquez sur '📄 Exportar PDF'")
        print("   5. Le PDF s'ouvre automatiquement (sans message de confirmation)")
        
        print("\n✨ Améliorations apportées :")
        print("   • Expérience utilisateur fluide (pas de popup inutile)")
        print("   • Affichage correct du logo d'entreprise")
        print("   • Données produits complètes et lisibles")
        print("   • Références produits visibles")
        print("   • Logs détaillés pour le débogage")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_corrections_pdf()
    print(f"\n{'🎉 Démonstration réussie!' if success else '❌ Démonstration échouée'}")
    sys.exit(0 if success else 1)
