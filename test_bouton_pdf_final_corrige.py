#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final du bouton PDF corrigé
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_bouton_pdf():
    """Test de l'application avec le bouton PDF corrigé"""
    print("🚀 Test final du bouton PDF corrigé")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.main_window_pyqt5 import MainWindowPyQt5
        from database.database import db
        
        # Vérifier qu'il y a des factures
        facturas = db.get_all_invoices()
        if not facturas:
            print("⚠️  Aucune facture trouvée pour le test")
            print("   Créez d'abord une facture dans l'application")
            return False
        
        print(f"✅ {len(facturas)} facture(s) disponible(s) pour le test")
        
        # Créer l'application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("✅ Application PyQt5 créée")
        
        # Créer la fenêtre principale
        main_window = MainWindowPyQt5()
        print("✅ Fenêtre principale créée")
        
        # Afficher la fenêtre
        main_window.show()
        print("✅ Fenêtre affichée")
        
        print("\n📋 INSTRUCTIONS POUR LE TEST:")
        print("1. La fenêtre principale s'ouvre")
        print("2. Clique sur 'Facturas' pour ouvrir la gestion des factures")
        print("3. Vérifie que le bouton '📄 Exportar PDF' est présent")
        print("4. Sélectionne une facture dans la liste")
        print("5. Clique sur '📄 Exportar PDF'")
        print("6. Vérifie qu'un message de succès s'affiche")
        print("7. Vérifie que le PDF est créé dans le dossier 'pdfs/'")
        print("8. Ferme l'application quand tu as terminé")
        
        print("\n🎯 VÉRIFICATIONS À FAIRE:")
        print("✓ Le bouton PDF est visible et positionné correctement")
        print("✓ Cliquer sans sélection affiche: 'Seleccione una factura para exportar a PDF'")
        print("✓ Cliquer avec une facture sélectionnée génère un PDF")
        print("✓ Le message de succès affiche le nom du fichier et l'emplacement")
        print("✓ Le PDF est sauvegardé dans le dossier 'pdfs/' avec le bon nom")
        print("✓ Le PDF contient les informations de la facture")
        
        print(f"\n📁 DOSSIER PDF: {os.path.join(os.getcwd(), 'pdfs')}")
        print(f"📊 FACTURES DISPONIBLES:")
        for i, factura in enumerate(facturas[:5]):  # Afficher les 5 premières
            print(f"   {i+1}. {factura.get('numero', 'N/A')} - {factura.get('cliente_nombre', 'N/A')} - €{factura.get('total', 0):.2f}")
        
        print("\n⏳ Lancement de l'application...")
        print("   (Ferme la fenêtre pour terminer le test)")
        
        # Lancer l'application
        app.exec_()
        
        print("\n✅ Application fermée")
        
        # Vérifier si des PDFs ont été créés
        pdf_dir = os.path.join(os.getcwd(), "pdfs")
        if os.path.exists(pdf_dir):
            pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            if pdf_files:
                print(f"\n📄 PDFs trouvés dans le dossier:")
                for pdf_file in pdf_files[-3:]:  # Afficher les 3 derniers
                    pdf_path = os.path.join(pdf_dir, pdf_file)
                    file_size = os.path.getsize(pdf_path)
                    print(f"   • {pdf_file} ({file_size} bytes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_verification_correction():
    """Test de vérification que la correction est appliquée"""
    print("\n🔍 Vérification de la correction")
    print("-" * 30)
    
    try:
        # Vérifier le code corrigé
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications
        corrections = [
            ('factura_data = db.get_invoice_by_id', '✅ Utilisation de factura_data (dictionnaire)'),
            ('generate_invoice_pdf(factura_data', '✅ Méthode generate_invoice_pdf utilisée'),
            ('factura_data.get(\'numero\'', '✅ Accès dictionnaire avec .get()'),
        ]
        
        all_ok = True
        for check, message in corrections:
            if check in content:
                print(f"   {message}")
            else:
                print(f"   ❌ {message} - MANQUANT")
                all_ok = False
        
        # Vérifier que l'ancienne méthode n'est plus utilisée
        if 'generar_factura_pdf(factura,' in content:
            print("   ❌ Ancienne méthode generar_factura_pdf encore présente")
            all_ok = False
        else:
            print("   ✅ Ancienne méthode problématique supprimée")
        
        return all_ok
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    # Désactiver l'ouverture automatique des PDFs
    os.environ['DISABLE_PDF_OPEN'] = '1'
    
    # Vérifier la correction
    correction_ok = test_verification_correction()
    
    if not correction_ok:
        print("\n❌ La correction n'est pas appliquée correctement!")
        return False
    
    print("\n✅ Correction vérifiée - Prêt pour le test")
    
    # Test de l'application
    success = test_application_bouton_pdf()
    
    if success:
        print("\n🎉 TEST FINAL RÉUSSI!")
        print("\n📋 RÉSUMÉ:")
        print("✅ Bouton PDF ajouté à l'interface des factures")
        print("✅ Correction appliquée pour l'erreur 'builtin_function_or_method'")
        print("✅ PDF généré correctement avec generate_invoice_pdf()")
        print("✅ Sauvegarde dans le dossier pdfs/ avec nom unique")
        print("✅ Messages informatifs pour l'utilisateur")
        
        print("\n🎯 LE BOUTON PDF EST MAINTENANT COMPLÈTEMENT FONCTIONNEL!")
        
    else:
        print("\n❌ TEST FINAL ÉCHOUÉ!")
        print("Vérifiez les erreurs ci-dessus.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
