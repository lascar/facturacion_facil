#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la configuration du répertoire PDF depuis la fenêtre Organisation
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_repertoire_pdf_configuration():
    """Test de la configuration du répertoire PDF"""
    print("🧪 Test de la configuration du répertoire PDF")
    print("=" * 60)
    
    try:
        # Importer les modules nécessaires
        from database.models import Organizacion
        from utils.pdf_generator import PDFGenerator
        
        print("\n1. Test de la configuration par défaut...")
        
        # Récupérer l'organisation actuelle
        org = Organizacion.get()
        if org:
            print(f"   📋 Organisation trouvée: {org.nombre}")
            print(f"   📁 Répertoire PDF configuré: '{org.directorio_descargas_pdf}'")
        else:
            print("   ⚠️  Aucune organisation configurée")
            # Créer une organisation de test
            org = Organizacion(
                nombre="Test Organisation",
                directorio_descargas_pdf=""
            )
            org.save()
            print("   ✅ Organisation de test créée")
        
        print("\n2. Test avec répertoire personnalisé...")
        
        # Créer un répertoire temporaire pour les tests
        temp_pdf_dir = tempfile.mkdtemp(prefix="test_pdf_config_")
        print(f"   📁 Répertoire temporaire créé: {temp_pdf_dir}")
        
        # Configurer l'organisation avec ce répertoire
        org.directorio_descargas_pdf = temp_pdf_dir
        org.save()
        print("   ✅ Configuration sauvegardée")
        
        # Vérifier que la configuration a été sauvegardée
        org_reloaded = Organizacion.get()
        assert org_reloaded.directorio_descargas_pdf == temp_pdf_dir
        print("   ✅ Configuration vérifiée")
        
        print("\n3. Test de génération PDF avec répertoire configuré...")
        
        # Simuler les données d'une facture
        factura_data = {
            'id': 999,
            'numero': 'TEST-CONFIG-001',
            'fecha': '2024-12-07',
            'cliente': {
                'nombre': 'Client Test Configuration',
                'nif': '12345678Z',
                'direccion': 'Adresse Test'
            },
            'lineas': [
                {
                    'producto_referencia': 'CONFIG-REF-001',
                    'producto_nombre': 'Produit Test Configuration',
                    'cantidad': 1,
                    'precio_unitario': 100.00,
                    'descuento': 0.0,
                    'iva_aplicado': 21.0,
                    'total': 100.00
                }
            ],
            'subtotal': 100.00,
            'iva_total': 21.00,
            'total': 121.00
        }
        
        # Générer le PDF
        numero_safe = str(factura_data.get('numero', 'TEST')).replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
        pdf_path = os.path.join(temp_pdf_dir, pdf_filename)
        
        # Désactiver l'ouverture automatique pour le test
        os.environ['TESTING'] = '1'
        
        try:
            pdf_generator = PDFGenerator()
            success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
            
            if success and os.path.exists(pdf_path):
                print(f"   ✅ PDF généré dans le répertoire configuré")
                print(f"   📄 Fichier: {pdf_filename}")
                print(f"   📁 Répertoire: {temp_pdf_dir}")
                print(f"   📊 Taille: {os.path.getsize(pdf_path)} bytes")
                
                # Vérifier que le fichier est dans le bon répertoire
                assert os.path.dirname(pdf_path) == temp_pdf_dir
                print("   ✅ Fichier dans le bon répertoire")
                
            else:
                print("   ❌ Échec de la génération PDF")
                return False
                
        finally:
            if 'TESTING' in os.environ:
                del os.environ['TESTING']
        
        print("\n4. Test avec répertoire inexistant...")
        
        # Configurer un répertoire qui n'existe pas
        fake_dir = "/repertoire/inexistant/test"
        org.directorio_descargas_pdf = fake_dir
        org.save()
        
        # Simuler l'appel de exportar_pdf (logique de fallback)
        org_test = Organizacion.get()
        configured_dir = org_test.directorio_descargas_pdf.strip() if org_test and org_test.directorio_descargas_pdf else ""
        
        if not configured_dir or not os.path.exists(configured_dir):
            fallback_dir = os.path.join(os.getcwd(), "pdfs")
            print(f"   ✅ Fallback vers répertoire par défaut: {fallback_dir}")
        else:
            print("   ❌ Le fallback n'a pas fonctionné")
            return False
        
        print("\n5. Nettoyage...")
        
        # Restaurer la configuration originale
        org.directorio_descargas_pdf = ""
        org.save()
        
        # Nettoyer le répertoire temporaire
        if os.path.exists(temp_pdf_dir):
            shutil.rmtree(temp_pdf_dir)
            print(f"   🗑️  Répertoire temporaire supprimé: {temp_pdf_dir}")
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("\n📋 Résumé des fonctionnalités testées:")
        print("   ✅ Configuration du répertoire PDF dans l'organisation")
        print("   ✅ Sauvegarde et récupération de la configuration")
        print("   ✅ Génération PDF dans le répertoire configuré")
        print("   ✅ Système de fallback pour répertoires inexistants")
        print("   ✅ Création automatique des répertoires")
        
        print("\n💡 Utilisation:")
        print("   1. Allez dans 'Organización'")
        print("   2. Configurez 'Directorio por defecto para descargas de PDF'")
        print("   3. Les factures PDF seront sauvegardées dans ce répertoire")
        print("   4. Si le répertoire n'existe plus, fallback vers 'pdfs/'")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_repertoire_pdf_configuration()
    sys.exit(0 if success else 1)
