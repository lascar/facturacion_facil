#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la correction du bouton PDF
"""

import sys
import os
import tempfile

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_structure_factura_data():
    """Test de la structure des données de facture"""
    print("🧪 Test: Structure des données de facture")
    
    try:
        from database.database import db
        
        # Obtenir toutes les factures pour tester
        facturas = db.get_all_invoices()
        
        if not facturas:
            print("   ℹ️  Aucune facture trouvée pour le test")
            return True
        
        # Prendre la première facture
        factura_simple = facturas[0]
        print(f"   ✅ Facture simple trouvée: {factura_simple.get('numero', 'N/A')}")
        
        # Obtenir la facture complète
        factura_complete = db.get_invoice_by_id(factura_simple['id'])
        
        if not factura_complete:
            print("   ❌ Impossible de récupérer la facture complète")
            return False
        
        print(f"   ✅ Facture complète récupérée: {factura_complete.get('numero', 'N/A')}")
        
        # Vérifier la structure
        required_fields = ['numero', 'fecha', 'cliente', 'subtotal', 'iva_total', 'total', 'lineas']
        for field in required_fields:
            if field in factura_complete:
                print(f"   ✅ Champ {field}: {type(factura_complete[field])}")
            else:
                print(f"   ❌ Champ manquant: {field}")
                return False
        
        # Vérifier la structure du client
        cliente = factura_complete.get('cliente', {})
        if isinstance(cliente, dict):
            print(f"   ✅ Client: {cliente.get('nombre', 'N/A')}")
        else:
            print(f"   ❌ Structure client incorrecte: {type(cliente)}")
            return False
        
        # Vérifier les lignes
        lineas = factura_complete.get('lineas', [])
        print(f"   ✅ Lignes: {len(lineas)} items")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_pdf_generator_avec_dictionnaire():
    """Test du générateur PDF avec un dictionnaire"""
    print("\n🧪 Test: Générateur PDF avec dictionnaire")
    
    try:
        from utils.pdf_generator import PDFGenerator
        from database.database import db
        
        # Obtenir une facture
        facturas = db.get_all_invoices()
        if not facturas:
            print("   ℹ️  Aucune facture pour le test")
            return True
        
        factura_data = db.get_invoice_by_id(facturas[0]['id'])
        if not factura_data:
            print("   ❌ Impossible de récupérer la facture")
            return False
        
        print(f"   ✅ Facture récupérée: {factura_data.get('numero', 'N/A')}")
        
        # Créer un fichier temporaire
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, "test_factura.pdf")
        
        # Créer le générateur PDF
        pdf_generator = PDFGenerator()
        
        # Tester la méthode generate_invoice_pdf (qui accepte un dictionnaire)
        success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
        
        if success:
            print("   ✅ PDF généré avec succès")
            
            # Vérifier que le fichier existe
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   ✅ Fichier PDF créé: {file_size} bytes")
                
                # Nettoyer
                os.remove(pdf_path)
                os.rmdir(temp_dir)
                
                return True
            else:
                print("   ❌ Fichier PDF non créé")
                return False
        else:
            print("   ❌ Échec de génération PDF")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_methode_exportar_pdf_corrigee():
    """Test de la méthode exportar_pdf corrigée"""
    print("\n🧪 Test: Méthode exportar_pdf corrigée")
    
    try:
        # Vérifier le code de la méthode
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications du code corrigé
        checks = [
            ('factura_data = db.get_invoice_by_id', 'Récupération factura_data'),
            ('generate_invoice_pdf(factura_data', 'Utilisation generate_invoice_pdf'),
            ('factura_data.get(\'numero\'', 'Accès dictionnaire factura_data'),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - MANQUANT: {check}")
                return False
        
        # Vérifier que l'ancienne méthode n'est plus utilisée
        if 'generar_factura_pdf(factura,' in content:
            print("   ❌ Ancienne méthode generar_factura_pdf encore présente")
            return False
        else:
            print("   ✅ Ancienne méthode generar_factura_pdf supprimée")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_simulation_exportar_pdf():
    """Test de simulation de la méthode exportar_pdf"""
    print("\n🧪 Test: Simulation exportar_pdf")
    
    try:
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        import tempfile
        from datetime import datetime
        
        # Obtenir une facture
        facturas = db.get_all_invoices()
        if not facturas:
            print("   ℹ️  Aucune facture pour le test")
            return True
        
        selected_factura_id = facturas[0]['id']
        print(f"   ✅ Facture sélectionnée: ID {selected_factura_id}")
        
        # Simuler la méthode exportar_pdf
        factura_data = db.get_invoice_by_id(selected_factura_id)
        if not factura_data:
            print("   ❌ Facture non récupérée")
            return False
        
        print(f"   ✅ Factura_data récupérée: {factura_data.get('numero', 'N/A')}")
        
        # Créer le dossier temporaire
        temp_dir = tempfile.mkdtemp()
        
        # Générer nom du fichier
        numero_safe = str(factura_data.get('numero', 'SIN_NUMERO')).replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        print(f"   ✅ Nom fichier: {pdf_filename}")
        
        # Créer le générateur PDF
        pdf_generator = PDFGenerator()
        
        # Générer le PDF
        success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
        
        if success:
            print("   ✅ PDF généré avec succès")
            
            # Vérifier le fichier
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   ✅ Fichier créé: {file_size} bytes")
                
                # Nettoyer
                os.remove(pdf_path)
                os.rmdir(temp_dir)
                
                return True
            else:
                print("   ❌ Fichier non créé")
                return False
        else:
            print("   ❌ Échec génération PDF")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de la correction du bouton PDF")
    print("=" * 50)
    
    # Désactiver l'ouverture automatique des PDFs
    os.environ['DISABLE_PDF_OPEN'] = '1'
    os.environ['TESTING'] = '1'
    
    tests = [
        test_structure_factura_data,
        test_pdf_generator_avec_dictionnaire,
        test_methode_exportar_pdf_corrigee,
        test_simulation_exportar_pdf,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DE LA CORRECTION")
    print(f"✅ Tests réussis: {sum(results)}/{len(results)}")
    print(f"❌ Tests échoués: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("Le bouton PDF devrait maintenant fonctionner correctement.")
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("1. Lance l'application: python3 main.py")
        print("2. Va dans 'Facturas'")
        print("3. Sélectionne une facture")
        print("4. Clique sur '📄 Exportar PDF'")
        print("5. Vérifie que le PDF est généré sans erreur")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
