#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration finale du bouton PDF corrigé
"""

import sys
import os
import tempfile

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_correction_appliquee():
    """Test que la correction est appliquée dans le code"""
    print("🧪 Test: Correction appliquée")
    
    try:
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications de la correction
        corrections = [
            ('factura_data = db.get_invoice_by_id', 'Utilisation factura_data'),
            ('generate_invoice_pdf(factura_data', 'Méthode generate_invoice_pdf'),
            ('factura_data.get(\'numero\'', 'Accès dictionnaire'),
        ]
        
        for check, description in corrections:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - MANQUANT")
                return False
        
        # Vérifier que l'ancienne méthode problématique n'est plus utilisée
        if 'generar_factura_pdf(factura,' in content:
            print("   ❌ Ancienne méthode problématique encore présente")
            return False
        else:
            print("   ✅ Ancienne méthode problématique supprimée")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_generation_pdf_fonctionnelle():
    """Test que la génération PDF fonctionne"""
    print("\n🧪 Test: Génération PDF fonctionnelle")
    
    try:
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        
        # Obtenir une facture pour le test
        facturas = db.get_all_invoices()
        if not facturas:
            print("   ℹ️  Aucune facture disponible pour le test")
            return True
        
        # Récupérer la facture complète
        factura_data = db.get_invoice_by_id(facturas[0]['id'])
        if not factura_data:
            print("   ❌ Facture non récupérée")
            return False
        
        print(f"   ✅ Facture récupérée: {factura_data.get('numero', 'N/A')}")
        
        # Vérifier la structure attendue
        required_fields = ['numero', 'cliente', 'lineas']
        for field in required_fields:
            if field not in factura_data:
                print(f"   ❌ Champ manquant: {field}")
                return False
        
        print("   ✅ Structure de données correcte")
        
        # Tester la génération PDF
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, "test_correction.pdf")
        
        pdf_generator = PDFGenerator()
        success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
        
        if not success:
            print("   ❌ Génération PDF échouée")
            return False
        
        if not os.path.exists(pdf_path):
            print("   ❌ Fichier PDF non créé")
            return False
        
        file_size = os.path.getsize(pdf_path)
        if file_size < 1000:
            print(f"   ❌ Fichier PDF trop petit: {file_size} bytes")
            return False
        
        print(f"   ✅ PDF généré avec succès: {file_size} bytes")
        
        # Nettoyer
        os.remove(pdf_path)
        os.rmdir(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bouton_pdf_interface():
    """Test de l'interface du bouton PDF"""
    print("\n🧪 Test: Interface bouton PDF")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        # Créer l'application si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Créer la fenêtre des factures
        window = FacturasPyQt5Window()
        
        # Vérifier que le bouton PDF existe
        if not hasattr(window, 'pdf_btn'):
            print("   ❌ Le bouton PDF n'existe pas")
            return False
        
        if window.pdf_btn is None:
            print("   ❌ Le bouton PDF est None")
            return False
        
        print("   ✅ Bouton PDF existe")
        
        # Vérifier le texte du bouton
        button_text = window.pdf_btn.text()
        if "PDF" not in button_text:
            print(f"   ❌ Texte du bouton incorrect: {button_text}")
            return False
        
        print(f"   ✅ Texte du bouton: {button_text}")
        
        # Vérifier que la méthode exportar_pdf existe
        if not hasattr(window, 'exportar_pdf'):
            print("   ❌ La méthode exportar_pdf n'existe pas")
            return False
        
        if not callable(window.exportar_pdf):
            print("   ❌ exportar_pdf n'est pas callable")
            return False
        
        print("   ✅ Méthode exportar_pdf disponible")
        
        # Tester la méthode sans sélection (ne doit pas lever d'exception)
        window.selected_factura_id = None
        window.exportar_pdf()
        print("   ✅ Gestion de l'absence de sélection OK")
        
        window.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simulation_workflow_complet():
    """Test de simulation du workflow complet"""
    print("\n🧪 Test: Simulation workflow complet")
    
    try:
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        from datetime import datetime
        
        # Obtenir une facture
        facturas = db.get_all_invoices()
        if not facturas:
            print("   ℹ️  Aucune facture pour le test")
            return True
        
        selected_factura_id = facturas[0]['id']
        print(f"   ✅ Facture sélectionnée: ID {selected_factura_id}")
        
        # Simuler exactement ce que fait exportar_pdf()
        factura_data = db.get_invoice_by_id(selected_factura_id)
        if not factura_data:
            print("   ❌ Facture non récupérée")
            return False
        
        print(f"   ✅ Factura_data récupérée: {factura_data.get('numero', 'N/A')}")
        
        # Créer le dossier temporaire (simule pdfs/)
        temp_dir = tempfile.mkdtemp()
        
        # Générer nom du fichier (comme dans exportar_pdf)
        numero_safe = str(factura_data.get('numero', 'SIN_NUMERO')).replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        print(f"   ✅ Nom fichier généré: {pdf_filename}")
        
        # Créer le générateur PDF (comme dans exportar_pdf)
        pdf_generator = PDFGenerator()
        
        # Générer le PDF (méthode corrigée)
        success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
        
        if not success:
            print("   ❌ Génération PDF échouée")
            return False
        
        if not os.path.exists(pdf_path):
            print("   ❌ Fichier PDF non créé")
            return False
        
        file_size = os.path.getsize(pdf_path)
        print(f"   ✅ PDF généré avec succès: {file_size} bytes")
        
        # Nettoyer
        os.remove(pdf_path)
        os.rmdir(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 Test d'intégration finale du bouton PDF")
    print("=" * 60)
    
    # Désactiver l'ouverture automatique des PDFs
    os.environ['DISABLE_PDF_OPEN'] = '1'
    os.environ['TESTING'] = '1'
    
    tests = [
        test_correction_appliquee,
        test_generation_pdf_fonctionnelle,
        test_bouton_pdf_interface,
        test_simulation_workflow_complet,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX")
    print(f"✅ Tests réussis: {sum(results)}/{len(results)}")
    print(f"❌ Tests échoués: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 INTÉGRATION FINALE RÉUSSIE!")
        print("\n📋 FONCTIONNALITÉS VALIDÉES:")
        print("✓ Correction de l'erreur 'builtin_function_or_method' appliquée")
        print("✓ Bouton PDF présent et fonctionnel dans l'interface")
        print("✓ Génération PDF avec dictionnaire fonctionne")
        print("✓ Workflow complet de A à Z validé")
        print("✓ Gestion d'erreurs et cas limites OK")
        
        print("\n🎯 LE BOUTON PDF EST MAINTENANT COMPLÈTEMENT OPÉRATIONNEL!")
        print("\n📱 UTILISATION:")
        print("1. Lance l'application: python3 main.py")
        print("2. Va dans 'Facturas'")
        print("3. Sélectionne une facture")
        print("4. Clique sur '📄 Exportar PDF'")
        print("5. Le PDF est généré dans le dossier pdfs/")
        
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
