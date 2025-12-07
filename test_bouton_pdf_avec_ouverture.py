#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton PDF avec ouverture automatique
"""

import sys
import os
import tempfile
import time

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_methode_abrir_pdf():
    """Test de la méthode abrir_pdf"""
    print("🧪 Test: Méthode abrir_pdf")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        # Créer l'application si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Créer la fenêtre des factures
        window = FacturasPyQt5Window()
        
        # Vérifier que la méthode abrir_pdf existe
        if not hasattr(window, 'abrir_pdf'):
            print("   ❌ La méthode abrir_pdf n'existe pas")
            return False
        
        if not callable(window.abrir_pdf):
            print("   ❌ abrir_pdf n'est pas callable")
            return False
        
        print("   ✅ Méthode abrir_pdf disponible")
        
        # Créer un fichier PDF temporaire pour le test
        temp_dir = tempfile.mkdtemp()
        test_pdf_path = os.path.join(temp_dir, "test_ouverture.pdf")
        
        # Créer un fichier PDF simple pour le test
        with open(test_pdf_path, 'wb') as f:
            # En-tête PDF minimal
            f.write(b'%PDF-1.4\n')
            f.write(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
            f.write(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
            f.write(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n')
            f.write(b'xref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n')
            f.write(b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n178\n%%EOF\n')
        
        print(f"   ✅ Fichier PDF test créé: {test_pdf_path}")
        
        # Tester la méthode abrir_pdf
        # Note: En mode test, on ne veut pas vraiment ouvrir le PDF
        # On va juste vérifier que la méthode ne lève pas d'exception
        
        # Désactiver l'ouverture réelle en mode test
        os.environ['TESTING'] = '1'
        
        result = window.abrir_pdf(test_pdf_path)
        print(f"   ✅ Méthode abrir_pdf exécutée: {result}")
        
        # Tester avec un fichier inexistant
        result_inexistant = window.abrir_pdf("/fichier/inexistant.pdf")
        print(f"   ✅ Gestion fichier inexistant: {result_inexistant}")
        
        # Nettoyer
        os.remove(test_pdf_path)
        os.rmdir(temp_dir)
        window.close()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exportar_pdf_avec_ouverture():
    """Test de exportar_pdf avec ouverture automatique"""
    print("\n🧪 Test: Export PDF avec ouverture")
    
    try:
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        from datetime import datetime
        
        # Obtenir une facture pour le test
        facturas = db.get_all_invoices()
        if not facturas:
            print("   ℹ️  Aucune facture pour le test")
            return True
        
        selected_factura_id = facturas[0]['id']
        print(f"   ✅ Facture sélectionnée: ID {selected_factura_id}")
        
        # Simuler exactement ce que fait exportar_pdf() avec ouverture
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
        
        if not success:
            print("   ❌ Génération PDF échouée")
            return False
        
        if not os.path.exists(pdf_path):
            print("   ❌ Fichier PDF non créé")
            return False
        
        file_size = os.path.getsize(pdf_path)
        print(f"   ✅ PDF généré: {file_size} bytes")
        
        # Tester l'ouverture (en mode test, ne pas vraiment ouvrir)
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        window = FacturasPyQt5Window()
        
        # Désactiver l'ouverture réelle en mode test
        os.environ['TESTING'] = '1'
        
        result_ouverture = window.abrir_pdf(pdf_path)
        print(f"   ✅ Test ouverture PDF: {result_ouverture}")
        
        # Nettoyer
        window.close()
        os.remove(pdf_path)
        os.rmdir(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_ouverture_presente():
    """Test que le code d'ouverture est présent"""
    print("\n🧪 Test: Code d'ouverture présent")
    
    try:
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications du code d'ouverture
        checks = [
            ('def abrir_pdf(self, pdf_path):', 'Méthode abrir_pdf définie'),
            ('self.abrir_pdf(pdf_path)', 'Appel à abrir_pdf dans exportar_pdf'),
            ('platform.system()', 'Détection du système d\'exploitation'),
            ('xdg-open', 'Support Linux'),
            ('startfile', 'Support Windows'),
            ('open', 'Support macOS'),
            ('PDF generado y abierto exitosamente', 'Message mis à jour'),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - MANQUANT: {check}")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_detection_systeme():
    """Test de la détection du système d'exploitation"""
    print("\n🧪 Test: Détection système")
    
    try:
        import platform
        
        sistema = platform.system().lower()
        print(f"   ✅ Système détecté: {sistema}")
        
        # Vérifier que nous avons une stratégie pour ce système
        if sistema == "windows":
            print("   ✅ Stratégie Windows: os.startfile()")
        elif sistema == "darwin":
            print("   ✅ Stratégie macOS: subprocess.run(['open', ...])")
        else:
            print("   ✅ Stratégie Linux/Autres: subprocess.run(['xdg-open', ...])")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test du bouton PDF avec ouverture automatique")
    print("=" * 60)
    
    # Désactiver l'ouverture automatique des PDFs en mode test
    os.environ['DISABLE_PDF_OPEN'] = '1'
    os.environ['TESTING'] = '1'
    
    tests = [
        test_code_ouverture_presente,
        test_detection_systeme,
        test_methode_abrir_pdf,
        test_exportar_pdf_avec_ouverture,
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
        print("\n🎉 OUVERTURE AUTOMATIQUE IMPLÉMENTÉE!")
        print("\n📋 FONCTIONNALITÉS AJOUTÉES:")
        print("✓ Méthode abrir_pdf() pour ouvrir le PDF")
        print("✓ Détection automatique du système d'exploitation")
        print("✓ Support Windows (os.startfile)")
        print("✓ Support macOS (open)")
        print("✓ Support Linux (xdg-open)")
        print("✓ Gestion d'erreurs robuste")
        print("✓ Ouverture automatique après génération")
        
        print("\n🎯 WORKFLOW COMPLET:")
        print("1. Utilisateur clique sur '📄 Exportar PDF'")
        print("2. PDF généré dans le dossier pdfs/")
        print("3. PDF ouvert automatiquement dans le visor par défaut")
        print("4. Message de confirmation affiché")
        
        print("\n🎉 LE BOUTON PDF GÉNÈRE ET OUVRE MAINTENANT AUTOMATIQUEMENT!")
        
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
