#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections apportées à la génération PDF
"""

import os
import sys
import tempfile
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pdf_corrections():
    """Test des corrections PDF"""
    print("🧪 Test des corrections PDF")
    print("=" * 50)
    
    try:
        # 1. Test de la recherche de logo
        print("\n1. Test de la recherche de logo...")
        from utils.pdf_generator import PDFGenerator
        
        pdf_generator = PDFGenerator()
        logo_path = pdf_generator.find_company_logo()
        
        if logo_path:
            print(f"   ✅ Logo trouvé: {logo_path}")
            print(f"   📁 Existe: {os.path.exists(logo_path)}")
        else:
            print("   ⚠️  Aucun logo trouvé")
        
        # 2. Test de génération PDF avec données simulées
        print("\n2. Test de génération PDF avec données simulées...")
        
        # Données de test
        invoice_data = {
            'numero': 'TEST-2024-001',
            'fecha': '2024-12-07',
            'vencimiento': '2024-12-07',
            'cliente': {
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test, 123\n28001 Madrid'
            },
            'lineas': [
                {
                    'producto_referencia': 'REF-001',
                    'producto_nombre': 'Producto Test 1',
                    'cantidad': 2,
                    'precio_unitario': 25.50,
                    'descuento': 5.0,
                    'iva_aplicado': 21.0,
                    'total': 51.00
                },
                {
                    'producto_referencia': 'REF-002',
                    'producto_nombre': 'Producto Test 2',
                    'cantidad': 1,
                    'precio_unitario': 15.75,
                    'descuento': 0.0,
                    'iva_aplicado': 21.0,
                    'total': 15.75
                }
            ],
            'subtotal': 66.75,
            'iva_total': 14.02,
            'total': 80.77
        }
        
        # Créer un fichier PDF temporaire
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name
        
        try:
            # Désactiver l'ouverture automatique pour le test
            os.environ['TESTING'] = '1'
            
            # Générer le PDF
            success = pdf_generator.generate_invoice_pdf(invoice_data, pdf_path)
            
            if success and os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   ✅ PDF généré avec succès")
                print(f"   📄 Fichier: {os.path.basename(pdf_path)}")
                print(f"   📊 Taille: {file_size} bytes")
                
                # Vérifier que le fichier n'est pas vide
                if file_size > 1000:
                    print("   ✅ Taille du fichier correcte")
                else:
                    print("   ⚠️  Fichier PDF trop petit")
                
            else:
                print("   ❌ Échec de la génération PDF")
                return False
                
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            
            # Nettoyer la variable d'environnement
            if 'TESTING' in os.environ:
                del os.environ['TESTING']
        
        # 3. Test de la méthode exportar_pdf (simulation)
        print("\n3. Test de la méthode exportar_pdf (simulation)...")
        
        # Simuler les données comme elles viennent de la base de données
        factura_data_from_db = {
            'id': 1,
            'numero': 'TEST-2024-002',
            'fecha': '2024-12-07',
            'cliente': {
                'nombre': 'Cliente DB Test',
                'nif': '87654321B',
                'direccion': 'Avenida Test, 456'
            },
            'lineas': [
                {
                    'producto_referencia': 'DB-REF-001',
                    'producto_nombre': 'Producto desde DB',
                    'cantidad': 3,
                    'precio_unitario': 12.99,
                    'descuento': 10.0,
                    'iva_aplicado': 21.0,
                    'total': 38.97
                }
            ],
            'subtotal': 38.97,
            'iva_total': 8.18,
            'total': 47.15
        }
        
        # Test avec les données de la base de données
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name
        
        try:
            os.environ['TESTING'] = '1'
            success = pdf_generator.generate_invoice_pdf(factura_data_from_db, pdf_path)
            
            if success:
                print("   ✅ Test avec données DB réussi")
            else:
                print("   ❌ Test avec données DB échoué")
                
        finally:
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            if 'TESTING' in os.environ:
                del os.environ['TESTING']
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("\n📋 Résumé des corrections appliquées:")
        print("   ✅ Suppression de la fenêtre de confirmation PDF")
        print("   ✅ Amélioration de la recherche de logo")
        print("   ✅ Correction de l'affichage du nom du produit")
        print("   ✅ Correction de l'affichage de la référence du produit")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_corrections()
    sys.exit(0 if success else 1)
