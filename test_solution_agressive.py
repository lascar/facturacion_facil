#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la solution agressive pour forcer les dialogs au premier plan
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog

class TestAggressiveWindow(QMainWindow):
    """Fenêtre de test pour la solution agressive"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔥 Test Solution AGRESSIVE - Ventana Primer Plano")
        self.setGeometry(100, 100, 500, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🔥 TEST SOLUTION AGRESSIVE")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 15px; color: #d32f2f;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
🎯 OBJECTIF: Vérifier que les fenêtres s'ouvrent IMMÉDIATEMENT au premier plan

✅ SOLUTION AGRESSIVE IMPLÉMENTÉE:
• Override de show() avec forçage automatique
• Techniques multiples: WindowStaysOnTopHint, setActiveWindow, etc.
• Tentatives répétées avec délais (10ms, 50ms, 100ms)
• Forçage du focus système

🧪 TEST: Cliquez sur les boutons et vérifiez que CHAQUE fenêtre
apparaît INSTANTANÉMENT au premier plan, PAS en arrière-plan.
        """)
        instructions.setStyleSheet("margin: 10px; padding: 15px; background-color: #fff3e0; border-left: 4px solid #ff9800;")
        layout.addWidget(instructions)
        
        # Boutons de test
        btn_crear = QPushButton("🆕 TEST AGGRESSIF: Crear Nueva Factura")
        btn_crear.clicked.connect(self.test_crear_aggressif)
        btn_crear.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #4caf50; color: white; font-weight: bold;")
        layout.addWidget(btn_crear)
        
        btn_editar = QPushButton("✏️ TEST AGGRESSIF: Editar Factura")
        btn_editar.clicked.connect(self.test_editar_aggressif)
        btn_editar.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #2196f3; color: white; font-weight: bold;")
        layout.addWidget(btn_editar)
        
        btn_multiple = QPushButton("🚀 TEST MULTIPLE: Ouvrir 3 fenêtres rapidement")
        btn_multiple.clicked.connect(self.test_multiple_aggressif)
        btn_multiple.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #ff5722; color: white; font-weight: bold;")
        layout.addWidget(btn_multiple)
        
        # Status
        self.status_label = QLabel("🔥 Solution agressive prête - Testez maintenant!")
        self.status_label.setStyleSheet("margin: 15px; color: #d32f2f; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # Variables
        self.dialogs = []
    
    def test_crear_aggressif(self):
        """Test agressif de CrearFacturaDialog"""
        try:
            self.status_label.setText("🔥 OUVERTURE AGRESSIVE: CrearFacturaDialog...")
            
            # Créer le dialog - la solution agressive est dans le mixin
            dialog = CrearFacturaDialog(None)  # Parent None pour éviter hiérarchie
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant show() overridé avec forçage automatique
            dialog.show()
            
            self.status_label.setText("✅ CrearFacturaDialog ouvert - DOIT être au premier plan IMMÉDIATEMENT!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur: {e}")
    
    def test_editar_aggressif(self):
        """Test agressif de EditarFacturaDialog"""
        try:
            self.status_label.setText("🔥 OUVERTURE AGRESSIVE: EditarFacturaDialog...")
            
            # Données fictives
            factura_data = {
                'id': 1, 'numero': 'TEST-AGGRESSIF-001', 'cliente_id': 1,
                'cliente_nombre': 'Test Aggressif', 'fecha': '2025-12-07',
                'total': 999.99, 'estado': 'Test', 'lineas': []
            }
            
            # Créer le dialog - la solution agressive est dans le mixin
            dialog = EditarFacturaDialog(factura_data, None)  # Parent None
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant show() overridé avec forçage automatique
            dialog.show()
            
            self.status_label.setText("✅ EditarFacturaDialog ouvert - DOIT être au premier plan IMMÉDIATEMENT!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur: {e}")
    
    def test_multiple_aggressif(self):
        """Test d'ouverture multiple rapide"""
        try:
            self.status_label.setText("🚀 TEST MULTIPLE: Ouverture de 3 fenêtres...")
            
            # Fermer les dialogs précédents
            for dialog in self.dialogs:
                if dialog:
                    dialog.close()
            self.dialogs.clear()
            
            # Ouvrir 3 fenêtres rapidement
            def ouvrir_crear():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_editar1():
                factura_data = {'id': 1, 'numero': 'MULTI-1', 'cliente_id': 1,
                               'cliente_nombre': 'Multi Test 1', 'fecha': '2025-12-07',
                               'total': 100, 'estado': 'Test', 'lineas': []}
                dialog = EditarFacturaDialog(factura_data, None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_editar2():
                factura_data = {'id': 2, 'numero': 'MULTI-2', 'cliente_id': 2,
                               'cliente_nombre': 'Multi Test 2', 'fecha': '2025-12-07',
                               'total': 200, 'estado': 'Test', 'lineas': []}
                dialog = EditarFacturaDialog(factura_data, None)
                self.dialogs.append(dialog)
                dialog.show()
            
            # Ouvrir avec délais courts
            ouvrir_crear()
            QTimer.singleShot(200, ouvrir_editar1)
            QTimer.singleShot(400, ouvrir_editar2)
            
            QTimer.singleShot(600, lambda: self.status_label.setText(
                "✅ 3 fenêtres ouvertes - TOUTES doivent être au premier plan!"
            ))
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur multiple: {e}")

def main():
    """Fonction principale"""
    print("🔥 TEST SOLUTION AGRESSIVE: Ventana Primer Plano")
    print("=" * 60)
    print("🎯 OBJECTIF: Vérifier que la solution agressive fonctionne")
    print("✅ TECHNIQUES IMPLÉMENTÉES:")
    print("   • Override de show() avec forçage automatique")
    print("   • WindowStaysOnTopHint temporaire")
    print("   • setActiveWindow() système")
    print("   • Tentatives multiples avec délais")
    print("   • Forçage du focus et de l'état actif")
    print()
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre de test
    window = TestAggressiveWindow()
    window.show()
    
    print("🚀 Application de test lancée!")
    print("📋 INSTRUCTIONS:")
    print("   1. Cliquez sur les boutons de test")
    print("   2. Vérifiez que CHAQUE fenêtre s'ouvre AU PREMIER PLAN")
    print("   3. Si une fenêtre s'ouvre en arrière-plan = ÉCHEC")
    print("   4. Si toutes s'ouvrent au premier plan = SUCCÈS")
    print()
    print("🔥 RÉSULTAT ATTENDU: Toutes les fenêtres au premier plan IMMÉDIATEMENT")
    
    # Lancer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
