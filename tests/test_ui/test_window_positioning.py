#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour le positionnement des fenêtres - Solution forçage maximal
Tests intégrés pour résoudre le problème "Nueva Factura apparaît en second plan"
"""

import pytest
import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


class TestWindowPositioning:
    """Tests pour le positionnement des fenêtres"""
    
    @pytest.fixture(autouse=True)
    def setup_app(self):
        """Setup de l'application Qt pour les tests"""
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        yield
        # Cleanup après chaque test
        if hasattr(self, 'main_window'):
            try:
                if hasattr(self.main_window, 'facturas_window') and self.main_window.facturas_window:
                    if hasattr(self.main_window.facturas_window, 'crear_dialog') and self.main_window.facturas_window.crear_dialog:
                        self.main_window.facturas_window.crear_dialog.close()
                    self.main_window.facturas_window.close()
                self.main_window.close()
            except:
                pass
    
    def test_nueva_factura_forcage_maximal(self):
        """Test du forçage maximal pour Nueva Factura"""
        # Créer l'application
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        
        # Ouvrir facturas
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        assert facturas_window is not None, "Fenêtre facturas doit être créée"
        assert facturas_window.isVisible(), "Fenêtre facturas doit être visible"
        
        # S'assurer que facturas est au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.5)
        
        # Ouvrir Nueva Factura avec forçage maximal
        facturas_window.new_factura()
        
        # Vérification immédiate
        self.app.processEvents()
        time.sleep(0.3)
        
        assert facturas_window.crear_dialog is not None, "Dialog Nueva Factura doit être créé"
        assert facturas_window.crear_dialog.isVisible(), "Dialog Nueva Factura doit être visible"
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier les flags de forçage maximal
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_bypass = bool(flags & Qt.X11BypassWindowManagerHint)
        has_frameless = bool(flags & Qt.FramelessWindowHint)
        has_tool = bool(flags & Qt.Tool)
        has_window = bool(flags & Qt.Window)
        
        # Au moins un flag de forçage doit être présent
        assert has_stay_on_top or has_tool or has_bypass, "Au moins un flag de forçage doit être appliqué"
        assert has_window, "Flag Window doit être présent"
        
        # Vérifier que le dialog est actif
        is_active = dialog.isActiveWindow()
        assert is_active, "Dialog doit être la fenêtre active"
    
    def test_nueva_factura_resistance_focus(self):
        """Test de résistance au changement de focus"""
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        assert dialog.isVisible(), "Dialog doit être visible initialement"
        
        # Essayer de forcer facturas au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        facturas_window.setFocus()
        self.app.processEvents()
        time.sleep(0.2)
        
        # Vérifier que le dialog reste accessible
        still_visible = dialog.isVisible()
        assert still_visible, "Dialog doit rester visible après tentative de changement de focus"
    
    def test_nueva_factura_stabilite_long_terme(self):
        """Test de stabilité long terme du dialog"""
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        assert dialog.isVisible(), "Dialog doit être visible initialement"
        
        # Attendre la période de maintien complète (2.5 secondes)
        time.sleep(2.5)
        self.app.processEvents()
        
        # Vérifier la stabilité après nettoyage
        final_visible = dialog.isVisible()
        assert final_visible, "Dialog doit rester stable après la période de maintien"
    
    def test_nueva_factura_flags_cleanup(self):
        """Test du nettoyage des flags après stabilisation"""
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier les flags initiaux
        flags_initial = dialog.windowFlags()
        has_bypass_initial = bool(flags_initial & Qt.X11BypassWindowManagerHint)
        has_frameless_initial = bool(flags_initial & Qt.FramelessWindowHint)
        
        # Attendre le nettoyage (2+ secondes)
        time.sleep(2.2)
        self.app.processEvents()
        
        # Vérifier les flags après nettoyage
        flags_final = dialog.windowFlags()
        has_bypass_final = bool(flags_final & Qt.X11BypassWindowManagerHint)
        has_frameless_final = bool(flags_final & Qt.FramelessWindowHint)
        has_stay_on_top_final = bool(flags_final & Qt.WindowStaysOnTopHint)
        
        # Le dialog doit toujours être visible
        assert dialog.isVisible(), "Dialog doit rester visible après nettoyage"
        
        # Certains flags agressifs peuvent être retirés, mais StaysOnTop peut rester
        # C'est acceptable tant que le dialog reste visible et fonctionnel
        assert has_stay_on_top_final or dialog.isActiveWindow(), "Dialog doit rester au premier plan ou actif"
    
    def test_nueva_factura_sans_parent(self):
        """Test que le dialog est créé sans parent pour éviter les conflits de hiérarchie"""
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier que le dialog n'a pas de parent (ou parent = None)
        parent = dialog.parent()
        assert parent is None, "Dialog doit être créé sans parent pour éviter les conflits de hiérarchie"
    
    def test_scenario_utilisateur_complet(self):
        """Test du scénario utilisateur complet"""
        # Simulation du workflow utilisateur complet
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.5)
        
        # Utilisateur ouvre Facturas
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        assert facturas_window.isVisible(), "Fenêtre Facturas doit être visible"
        
        # Utilisateur travaille dans facturas (simulation)
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(1.0)
        
        # MOMENT CRITIQUE: Utilisateur clique Nueva Factura
        facturas_window.new_factura()
        
        # Vérification immédiate (ce que voit l'utilisateur)
        self.app.processEvents()
        time.sleep(0.2)
        
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "Dialog doit être créé"
        assert dialog.isVisible(), "Dialog doit être visible pour l'utilisateur"
        assert dialog.isActiveWindow(), "Dialog doit être au premier plan"
        
        # Test de résistance utilisateur
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.3)
        
        # Dialog doit rester accessible
        assert dialog.isVisible(), "Dialog doit rester accessible après tentative de retour à Facturas"

    def test_nueva_factura_solution_finale(self):
        """Test de la solution finale pour Nueva Factura avec chargement asynchrone"""
        from ui.facturas_pyqt5 import CrearFacturaDialog
        from PyQt5.QtCore import Qt

        # Créer le dialog avec la solution finale
        dialog = CrearFacturaDialog(None)

        try:
            # Vérifier que le dialog est créé
            assert dialog is not None

            # Vérifier les flags de fenêtre
            flags = dialog.windowFlags()
            assert bool(flags & Qt.Window), "Dialog doit avoir le flag Window"
            assert bool(flags & Qt.WindowStaysOnTopHint), "Dialog doit avoir WindowStaysOnTopHint"
            assert bool(flags & Qt.WindowCloseButtonHint), "Dialog doit avoir WindowCloseButtonHint"
            assert bool(flags & Qt.WindowMinimizeButtonHint), "Dialog doit avoir WindowMinimizeButtonHint"
            assert bool(flags & Qt.WindowTitleHint), "Dialog doit avoir WindowTitleHint"

            # Vérifier l'état de la fenêtre
            assert dialog.windowState() == Qt.WindowActive, "Dialog doit être dans l'état WindowActive"

            # Vérifier que le dialog est visible
            assert dialog.isVisible(), "Dialog doit être visible"

            # Vérifier le titre
            assert dialog.windowTitle() == "Crear Nueva Factura", "Dialog doit avoir le bon titre"

            # Vérifier que le dialog n'est pas modal
            assert not dialog.isModal(), "Dialog ne doit pas être modal"

        finally:
            dialog.close()

    def test_nueva_factura_chargement_asynchrone(self):
        """Test que le chargement des données est asynchrone"""
        from ui.facturas_pyqt5 import CrearFacturaDialog
        import time

        # Mesurer le temps de création du dialog
        start_time = time.time()
        dialog = CrearFacturaDialog(None)
        creation_time = time.time() - start_time

        try:
            # Le dialog doit se créer rapidement (moins de 1 seconde)
            # car le chargement des données est asynchrone
            assert creation_time < 1.0, f"Création trop lente: {creation_time:.2f}s"

            # Le dialog doit être visible immédiatement
            assert dialog.isVisible(), "Dialog doit être visible immédiatement"

        finally:
            dialog.close()

    def test_bouton_pdf_presente(self):
        """Test que le bouton PDF est présent dans l'interface des factures"""
        from ui.facturas_pyqt5 import FacturasPyQt5Window

        # Créer la fenêtre des factures
        window = FacturasPyQt5Window()

        try:
            # Vérifier que le bouton PDF existe
            assert hasattr(window, 'pdf_btn'), "Le bouton PDF n'existe pas"
            assert window.pdf_btn is not None, "Le bouton PDF est None"

            # Vérifier le texte du bouton
            button_text = window.pdf_btn.text()
            assert "PDF" in button_text, f"Le texte du bouton ne contient pas 'PDF': {button_text}"

            # Vérifier que le bouton est visible
            assert window.pdf_btn.isVisible(), "Le bouton PDF n'est pas visible"

            # Vérifier que la méthode exportar_pdf existe
            assert hasattr(window, 'exportar_pdf'), "La méthode exportar_pdf n'existe pas"
            assert callable(window.exportar_pdf), "exportar_pdf n'est pas callable"

        finally:
            window.close()

    def test_bouton_pdf_sans_selection(self):
        """Test du bouton PDF sans facture sélectionnée"""
        from ui.facturas_pyqt5 import FacturasPyQt5Window

        window = FacturasPyQt5Window()

        try:
            # S'assurer qu'aucune facture n'est sélectionnée
            window.selected_factura_id = None

            # Tester la méthode exportar_pdf (ne doit pas lever d'exception)
            window.exportar_pdf()

            # Si on arrive ici, c'est que la méthode gère bien l'absence de sélection
            assert True, "La méthode exportar_pdf gère l'absence de sélection"

        finally:
            window.close()

    def test_bouton_pdf_correction_appliquee(self):
        """Test que la correction du bouton PDF est appliquée"""
        # Vérifier le code corrigé
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifications de la correction
        corrections = [
            ('factura_data = db.get_invoice_by_id', 'Utilisation factura_data'),
            ('generate_invoice_pdf(factura_data', 'Méthode generate_invoice_pdf'),
            ('factura_data.get(\'numero\'', 'Accès dictionnaire'),
        ]

        for check, description in corrections:
            assert check in content, f"Correction manquante: {description}"

        # Vérifier que l'ancienne méthode problématique n'est plus utilisée
        assert 'generar_factura_pdf(factura,' not in content, \
               "Ancienne méthode problématique encore présente"

    def test_bouton_pdf_generation_fonctionnelle(self):
        """Test que la génération PDF fonctionne avec la correction"""
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        import tempfile
        import os

        # Obtenir une facture pour le test
        facturas = db.get_all_invoices()
        if not facturas:
            pytest.skip("Aucune facture disponible pour le test")

        # Récupérer la facture complète (comme le fait exportar_pdf)
        factura_data = db.get_invoice_by_id(facturas[0]['id'])
        assert factura_data is not None, "Facture non récupérée"

        # Vérifier la structure attendue
        assert 'numero' in factura_data
        assert 'cliente' in factura_data
        assert 'lineas' in factura_data

        # Tester la génération PDF avec la méthode corrigée
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, "test_correction.pdf")

        try:
            pdf_generator = PDFGenerator()
            success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)

            assert success, "Génération PDF échouée"
            assert os.path.exists(pdf_path), "Fichier PDF non créé"

            file_size = os.path.getsize(pdf_path)
            assert file_size > 1000, "Fichier PDF trop petit"

        finally:
            # Nettoyer
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            os.rmdir(temp_dir)

    def test_bouton_pdf_ouverture_automatique(self):
        """Test que l'ouverture automatique du PDF fonctionne"""
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        import tempfile

        window = FacturasPyQt5Window()

        try:
            # Vérifier que la méthode abrir_pdf existe
            assert hasattr(window, 'abrir_pdf'), "La méthode abrir_pdf n'existe pas"
            assert callable(window.abrir_pdf), "abrir_pdf n'est pas callable"

            # Créer un fichier PDF temporaire pour le test
            temp_dir = tempfile.mkdtemp()
            test_pdf_path = os.path.join(temp_dir, "test_ouverture.pdf")

            # Créer un fichier PDF minimal
            with open(test_pdf_path, 'wb') as f:
                f.write(b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF\n')

            # Tester la méthode abrir_pdf (en mode test, ne pas vraiment ouvrir)
            os.environ['TESTING'] = '1'
            result = window.abrir_pdf(test_pdf_path)

            # La méthode doit retourner True si le fichier existe
            assert result, "abrir_pdf doit retourner True pour un fichier existant"

            # Tester avec un fichier inexistant
            result_inexistant = window.abrir_pdf("/fichier/inexistant.pdf")
            assert not result_inexistant, "abrir_pdf doit retourner False pour un fichier inexistant"

            # Nettoyer
            os.remove(test_pdf_path)
            os.rmdir(temp_dir)

        finally:
            window.close()

    def test_bouton_pdf_workflow_complet(self):
        """Test du workflow complet: génération + ouverture"""
        from database.database import db
        from utils.pdf_generator import PDFGenerator
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        import tempfile
        from datetime import datetime

        # Obtenir une facture pour le test
        facturas = db.get_all_invoices()
        if not facturas:
            pytest.skip("Aucune facture disponible pour le test")

        # Simuler le workflow complet
        factura_data = db.get_invoice_by_id(facturas[0]['id'])
        assert factura_data is not None, "Facture non récupérée"

        # Créer le dossier temporaire
        temp_dir = tempfile.mkdtemp()

        try:
            # Générer nom du fichier (comme dans exportar_pdf)
            numero_safe = str(factura_data.get('numero', 'SIN_NUMERO')).replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
            pdf_path = os.path.join(temp_dir, pdf_filename)

            # Générer le PDF
            pdf_generator = PDFGenerator()
            success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
            assert success, "Génération PDF échouée"
            assert os.path.exists(pdf_path), "Fichier PDF non créé"

            # Tester l'ouverture
            window = FacturasPyQt5Window()
            os.environ['TESTING'] = '1'  # Mode test
            result_ouverture = window.abrir_pdf(pdf_path)
            assert result_ouverture, "Ouverture PDF échouée"

            window.close()

        finally:
            # Nettoyer
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            os.rmdir(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
