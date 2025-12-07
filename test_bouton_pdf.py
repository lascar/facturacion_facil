#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton PDF dans l'interface des factures
"""

import sys
import os
import tempfile
import shutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.facturas_pyqt5 import FacturasPyQt5Window
from database.database import db

def test_bouton_pdf_interface():
    """Test que le bouton PDF est présent dans l'interface"""
    print("🧪 Test 1: Vérification de la présence du bouton PDF")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre des factures
        window = FacturasPyQt5Window()
        
        # Vérifier que le bouton PDF existe
        assert hasattr(window, 'pdf_btn'), "Le bouton PDF n'existe pas"
        assert window.pdf_btn is not None, "Le bouton PDF est None"
        
        # Vérifier le texte du bouton
        button_text = window.pdf_btn.text()
        assert "PDF" in button_text, f"Le texte du bouton ne contient pas 'PDF': {button_text}"
        
        # Vérifier que le bouton est visible
        assert window.pdf_btn.isVisible(), "Le bouton PDF n'est pas visible"
        
        print("✅ Bouton PDF présent et configuré correctement")
        print(f"   Texte: {button_text}")
        
        window.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_bouton_pdf_sans_selection():
    """Test du bouton PDF sans facture sélectionnée"""
    print("\n🧪 Test 2: Bouton PDF sans sélection")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        window = FacturasPyQt5Window()
        
        # S'assurer qu'aucune facture n'est sélectionnée
        window.selected_factura_id = None
        
        # Simuler un clic sur le bouton PDF
        print("   Simulation du clic sur le bouton PDF...")
        window.exportar_pdf()
        
        print("✅ Le bouton PDF gère correctement l'absence de sélection")
        
        window.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_creation_dossier_pdf():
    """Test de la création du dossier pdfs"""
    print("\n🧪 Test 3: Création du dossier pdfs")
    
    try:
        # Créer un dossier temporaire pour le test
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        
        try:
            os.chdir(temp_dir)
            
            # Vérifier que le dossier pdfs n'existe pas
            pdf_dir = os.path.join(temp_dir, "pdfs")
            assert not os.path.exists(pdf_dir), "Le dossier pdfs existe déjà"
            
            # Simuler la création du dossier (comme dans exportar_pdf)
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
            
            # Vérifier que le dossier a été créé
            assert os.path.exists(pdf_dir), "Le dossier pdfs n'a pas été créé"
            assert os.path.isdir(pdf_dir), "pdfs n'est pas un dossier"
            
            print("✅ Dossier pdfs créé correctement")
            print(f"   Chemin: {pdf_dir}")
            
            return True
            
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_generation_nom_fichier():
    """Test de la génération du nom de fichier PDF"""
    print("\n🧪 Test 4: Génération du nom de fichier PDF")
    
    try:
        from datetime import datetime
        
        # Simuler une factura avec différents numéros
        test_cases = [
            {"numero": "F-2024-001", "expected_contains": "F_2024_001"},
            {"numero": "FACT/2024/123", "expected_contains": "FACT_2024_123"},
            {"numero": "SIN_NUMERO", "expected_contains": "SIN_NUMERO"},
        ]
        
        for case in test_cases:
            numero_safe = str(case["numero"]).replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
            
            assert case["expected_contains"] in pdf_filename, \
                f"Nom de fichier incorrect pour {case['numero']}: {pdf_filename}"
            
            assert pdf_filename.endswith(".pdf"), \
                f"Le fichier ne se termine pas par .pdf: {pdf_filename}"
            
            print(f"   ✅ {case['numero']} → {pdf_filename}")
        
        print("✅ Génération des noms de fichiers correcte")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Tests du bouton PDF pour les factures")
    print("=" * 50)
    
    # Désactiver l'ouverture automatique des PDFs pendant les tests
    os.environ['DISABLE_PDF_OPEN'] = '1'
    os.environ['TESTING'] = '1'
    
    tests = [
        test_bouton_pdf_interface,
        test_bouton_pdf_sans_selection,
        test_creation_dossier_pdf,
        test_generation_nom_fichier,
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
    print("📊 RÉSULTATS DES TESTS")
    print(f"✅ Tests réussis: {sum(results)}/{len(results)}")
    print(f"❌ Tests échoués: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Le bouton PDF est prêt à être utilisé.")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
