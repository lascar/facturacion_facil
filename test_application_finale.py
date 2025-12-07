#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'application pour vérifier que les fenêtres s'ouvrent au premier plan
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog, VerFacturaDialog

class TestMainWindow(QMainWindow):
    """Fenêtre principale de test"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Application - Ventana Primer Plano")
        self.setGeometry(100, 100, 400, 300)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🧪 Test Final: Ventana Primer Plano")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
Cliquez sur les boutons ci-dessous pour tester que les fenêtres
s'ouvrent IMMÉDIATEMENT au premier plan (pas en arrière-plan).

✅ Attendu: Chaque fenêtre apparaît instantanément au premier plan
❌ Problème: Si une fenêtre s'ouvre en arrière-plan
        """)
        instructions.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(instructions)
        
        # Boutons de test
        btn_crear = QPushButton("🆕 Test: Crear Nueva Factura")
        btn_crear.clicked.connect(self.test_crear_factura)
        btn_crear.setStyleSheet("padding: 10px; margin: 5px; font-size: 12px;")
        layout.addWidget(btn_crear)
        
        btn_editar = QPushButton("✏️ Test: Editar Factura")
        btn_editar.clicked.connect(self.test_editar_factura)
        btn_editar.setStyleSheet("padding: 10px; margin: 5px; font-size: 12px;")
        layout.addWidget(btn_editar)
        
        btn_ver = QPushButton("👁️ Test: Ver Factura")
        btn_ver.clicked.connect(self.test_ver_factura)
        btn_ver.setStyleSheet("padding: 10px; margin: 5px; font-size: 12px;")
        layout.addWidget(btn_ver)
        
        # Status
        self.status_label = QLabel("Prêt pour les tests...")
        self.status_label.setStyleSheet("margin: 10px; color: #666;")
        layout.addWidget(self.status_label)
        
        # Variables pour les dialogs
        self.crear_dialog = None
        self.editar_dialog = None
        self.ver_dialog = None
    
    def test_crear_factura(self):
        """Tester CrearFacturaDialog"""
        try:
            self.status_label.setText("🧪 Ouverture CrearFacturaDialog...")
            
            # Fermer le dialog précédent s'il existe
            if self.crear_dialog:
                self.crear_dialog.close()
            
            # Créer et afficher le dialog
            self.crear_dialog = CrearFacturaDialog(self)
            self.crear_dialog.show()
            
            self.status_label.setText("✅ CrearFacturaDialog ouvert - Vérifiez qu'il est au premier plan!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur CrearFacturaDialog: {e}")
    
    def test_editar_factura(self):
        """Tester EditarFacturaDialog"""
        try:
            self.status_label.setText("🧪 Ouverture EditarFacturaDialog...")
            
            # Fermer le dialog précédent s'il existe
            if self.editar_dialog:
                self.editar_dialog.close()
            
            # Données de facture fictives
            factura_data = {
                'id': 1,
                'numero': 'TEST-001',
                'cliente_id': 1,
                'cliente_nombre': 'Cliente Test',
                'fecha': '2025-12-07',
                'total': 100.0,
                'estado': 'Pendiente',
                'lineas': []
            }
            
            # Créer et afficher le dialog
            self.editar_dialog = EditarFacturaDialog(factura_data, self)
            self.editar_dialog.show()
            
            self.status_label.setText("✅ EditarFacturaDialog ouvert - Vérifiez qu'il est au premier plan!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur EditarFacturaDialog: {e}")
    
    def test_ver_factura(self):
        """Tester VerFacturaDialog"""
        try:
            self.status_label.setText("🧪 Ouverture VerFacturaDialog...")
            
            # Fermer le dialog précédent s'il existe
            if self.ver_dialog:
                self.ver_dialog.close()
            
            # Données de facture fictives
            factura_data = {
                'id': 1,
                'numero': 'TEST-001',
                'cliente_id': 1,
                'cliente_nombre': 'Cliente Test',
                'fecha': '2025-12-07',
                'total': 100.0,
                'estado': 'Pendiente',
                'lineas': []
            }
            
            # Créer et afficher le dialog
            self.ver_dialog = VerFacturaDialog(factura_data, self)
            self.ver_dialog.show()
            
            self.status_label.setText("✅ VerFacturaDialog ouvert - Vérifiez qu'il est au premier plan!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur VerFacturaDialog: {e}")

def main():
    """Fonction principale"""
    print("🚀 TEST FINAL: Application Ventana Primer Plano")
    print("=" * 50)
    print("Lancement de l'application de test...")
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre principale
    window = TestMainWindow()
    window.show()
    
    print("✅ Application lancée!")
    print("📋 Instructions:")
    print("   1. Cliquez sur les boutons pour ouvrir les dialogs")
    print("   2. Vérifiez que chaque dialog s'ouvre AU PREMIER PLAN")
    print("   3. Fermez l'application quand terminé")
    print()
    print("🎯 Résultat attendu: Tous les dialogs s'ouvrent immédiatement au premier plan")
    
    # Lancer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
