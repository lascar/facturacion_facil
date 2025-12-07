#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la solution SIMPLE et MULTIPLATEFORME pour forcer les dialogs au premier plan
Fonctionne sur Windows, Linux, macOS sans détection d'environnement
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog

class TestSimpleMultiplateformeWindow(QMainWindow):
    """Fenêtre de test pour la solution simple multiplateforme"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("🌍 TEST SOLUTION SIMPLE MULTIPLATEFORME - Ventana Primer Plano")
        self.setGeometry(100, 100, 600, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🌍 TEST SOLUTION SIMPLE MULTIPLATEFORME")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 15px; color: #2e7d32;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("""
🎯 SOLUTION SIMPLE DÉPLOYÉE:

✅ TECHNIQUES UNIVERSELLES:
• Pas de détection d'environnement complexe
• Flags PyQt5 universels (WindowStaysOnTopHint)
• Forçage simple avec show(), raise_(), activateWindow()
• WindowStaysOnTopHint temporaire (3 secondes)
• Override simple de show() avec forçage automatique
• Compatible Windows, Linux, macOS

🧪 TEST: Cliquez sur les boutons et vérifiez que CHAQUE fenêtre
apparaît INSTANTANÉMENT au premier plan sur votre système.
        """)
        description.setStyleSheet("margin: 10px; padding: 15px; background-color: #fff3e0; border-left: 4px solid #ff9800;")
        layout.addWidget(description)
        
        # Boutons de test
        btn_crear = QPushButton("🆕 TEST SIMPLE: Crear Nueva Factura")
        btn_crear.clicked.connect(self.test_crear_simple)
        btn_crear.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #4caf50; color: white; font-weight: bold;")
        layout.addWidget(btn_crear)
        
        btn_editar = QPushButton("✏️ TEST SIMPLE: Editar Factura")
        btn_editar.clicked.connect(self.test_editar_simple)
        btn_editar.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #2196f3; color: white; font-weight: bold;")
        layout.addWidget(btn_editar)
        
        btn_stress = QPushButton("🚀 TEST STRESS: Ouvrir 3 fenêtres rapidement")
        btn_stress.clicked.connect(self.test_stress_simple)
        btn_stress.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #ff5722; color: white; font-weight: bold;")
        layout.addWidget(btn_stress)
        
        btn_fermer_tout = QPushButton("🗑️ Fermer tous les dialogs")
        btn_fermer_tout.clicked.connect(self.fermer_tous_dialogs)
        btn_fermer_tout.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #9e9e9e; color: white; font-weight: bold;")
        layout.addWidget(btn_fermer_tout)
        
        # Status
        self.status_label = QLabel("🌍 Solution simple multiplateforme prête")
        self.status_label.setStyleSheet("margin: 15px; color: #2e7d32; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # Variables
        self.dialogs = []
    
    def test_crear_simple(self):
        """Test simple de CrearFacturaDialog"""
        try:
            self.status_label.setText("🌍 OUVERTURE SIMPLE: CrearFacturaDialog...")
            
            # Créer le dialog avec solution simple
            dialog = CrearFacturaDialog(None)  # Parent None pour éviter hiérarchie
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant SimpleDialogForegroundMixin
            # Le forçage est automatique grâce à l'override de show()
            dialog.show()
            
            self.status_label.setText("✅ CrearFacturaDialog ouvert - DOIT être au premier plan avec solution simple!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur simple: {e}")
    
    def test_editar_simple(self):
        """Test simple de EditarFacturaDialog"""
        try:
            self.status_label.setText("🌍 OUVERTURE SIMPLE: EditarFacturaDialog...")
            
            # Données fictives
            factura_data = {
                'id': 1, 'numero': 'SIMPLE-TEST-001', 'cliente_id': 1,
                'cliente_nombre': 'Test Simple Multiplateforme', 'fecha': '2025-12-07',
                'total': 999.00, 'estado': 'Test Simple', 'lineas': []
            }
            
            # Créer le dialog avec solution simple
            dialog = EditarFacturaDialog(factura_data, None)  # Parent None
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant SimpleDialogForegroundMixin
            # Le forçage est automatique grâce à l'override de show()
            dialog.show()
            
            self.status_label.setText("✅ EditarFacturaDialog ouvert - DOIT être au premier plan avec solution simple!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur simple: {e}")
    
    def test_stress_simple(self):
        """Test de stress simple - Ouverture multiple rapide"""
        try:
            self.status_label.setText("🚀 TEST STRESS SIMPLE: Ouverture de 3 fenêtres...")
            
            # Fermer les dialogs précédents
            self.fermer_tous_dialogs()
            
            # Ouvrir 3 fenêtres rapidement avec délais courts
            def ouvrir_crear():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_editar():
                factura_data = {'id': 1, 'numero': 'STRESS-SIMPLE', 'cliente_id': 1,
                               'cliente_nombre': 'Stress Test Simple', 'fecha': '2025-12-07',
                               'total': 100, 'estado': 'Test', 'lineas': []}
                dialog = EditarFacturaDialog(factura_data, None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_crear2():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            # Ouvrir avec délais très courts pour tester la robustesse
            ouvrir_crear()
            QTimer.singleShot(200, ouvrir_editar)
            QTimer.singleShot(400, ouvrir_crear2)
            
            QTimer.singleShot(800, lambda: self.status_label.setText(
                "✅ 3 fenêtres ouvertes - TOUTES doivent être au premier plan avec solution simple!"
            ))
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur stress simple: {e}")
    
    def fermer_tous_dialogs(self):
        """Ferme tous les dialogs ouverts"""
        try:
            count = 0
            for dialog in self.dialogs:
                if dialog and dialog.isVisible():
                    dialog.close()
                    count += 1
            self.dialogs.clear()
            self.status_label.setText(f"🗑️ {count} dialogs fermés")
        except Exception as e:
            self.status_label.setText(f"❌ Erreur fermeture: {e}")

def main():
    """Fonction principale"""
    print("🌍 TEST SOLUTION SIMPLE MULTIPLATEFORME: Ventana Primer Plano")
    print("=" * 70)
    
    print("🎯 SOLUTION SIMPLE DÉPLOYÉE:")
    print("   • SimpleDialogForegroundMixin universel")
    print("   • Flags PyQt5 standards (WindowStaysOnTopHint)")
    print("   • WindowStaysOnTopHint temporaire (3 secondes)")
    print("   • Forçage simple: show(), raise_(), activateWindow()")
    print("   • Override automatique de show()")
    print("   • Compatible Windows/Linux/macOS")
    print()
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre de test
    window = TestSimpleMultiplateformeWindow()
    window.show()
    
    print("🚀 Application de test simple lancée!")
    print("📋 INSTRUCTIONS:")
    print("   1. Cliquez sur les boutons de test")
    print("   2. Vérifiez que CHAQUE fenêtre s'ouvre AU PREMIER PLAN")
    print("   3. Testez le stress test avec 3 fenêtres")
    print("   4. Utilisez 'Fermer tous les dialogs' pour nettoyer")
    print()
    print("🌍 RÉSULTAT ATTENDU: Toutes les fenêtres au premier plan (multiplateforme)")
    
    # Lancer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
