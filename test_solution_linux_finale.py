#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de la solution Linux optimisée pour forcer les dialogs au premier plan
Spécialement conçu pour GNOME/X11
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog
from utils.dialog_foreground_linux import detect_linux_environment

class TestLinuxFinalWindow(QMainWindow):
    """Fenêtre de test pour la solution Linux finale"""
    
    def __init__(self):
        super().__init__()
        
        # Détecter l'environnement
        self.env = detect_linux_environment()
        
        self.setWindowTitle("🐧 TEST SOLUTION LINUX FINALE - Ventana Primer Plano")
        self.setGeometry(100, 100, 600, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre avec info environnement
        title = QLabel(f"🐧 TEST SOLUTION LINUX FINALE")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 15px; color: #2e7d32;")
        layout.addWidget(title)
        
        # Info environnement
        env_info = QLabel(f"""
🖥️ ENVIRONNEMENT DÉTECTÉ:
• Desktop: {self.env['desktop'].upper()}
• Session: {self.env['session'].upper()}
• GNOME: {'✅' if self.env['is_gnome'] else '❌'}
• X11: {'✅' if self.env['is_x11'] else '❌'}
• Wayland: {'✅' if self.env['is_wayland'] else '❌'}
        """)
        env_info.setStyleSheet("margin: 10px; padding: 15px; background-color: #e8f5e8; border-left: 4px solid #4caf50; font-family: monospace;")
        layout.addWidget(env_info)
        
        # Instructions
        instructions = QLabel("""
🎯 SOLUTION LINUX OPTIMISÉE IMPLÉMENTÉE:

✅ TECHNIQUES SPÉCIALISÉES:
• Détection automatique GNOME/X11
• Flags de fenêtre optimisés pour Linux
• WindowStaysOnTopHint avec durée prolongée (2s)
• Tentatives multiples avec délais croissants
• Forçage du focus système avec xprop
• Override de show() avec forçage automatique

🧪 TEST: Cliquez sur les boutons et vérifiez que CHAQUE fenêtre
apparaît INSTANTANÉMENT au premier plan sur votre système Linux.
        """)
        instructions.setStyleSheet("margin: 10px; padding: 15px; background-color: #fff3e0; border-left: 4px solid #ff9800;")
        layout.addWidget(instructions)
        
        # Boutons de test
        btn_crear = QPushButton("🆕 TEST LINUX: Crear Nueva Factura")
        btn_crear.clicked.connect(self.test_crear_linux)
        btn_crear.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #4caf50; color: white; font-weight: bold;")
        layout.addWidget(btn_crear)
        
        btn_editar = QPushButton("✏️ TEST LINUX: Editar Factura")
        btn_editar.clicked.connect(self.test_editar_linux)
        btn_editar.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #2196f3; color: white; font-weight: bold;")
        layout.addWidget(btn_editar)
        
        btn_stress = QPushButton("🚀 TEST STRESS: Ouvrir 5 fenêtres rapidement")
        btn_stress.clicked.connect(self.test_stress_linux)
        btn_stress.setStyleSheet("padding: 12px; margin: 8px; font-size: 13px; background-color: #ff5722; color: white; font-weight: bold;")
        layout.addWidget(btn_stress)
        
        # Status
        self.status_label = QLabel(f"🐧 Solution Linux optimisée prête pour {self.env['desktop'].upper()}/{self.env['session'].upper()}")
        self.status_label.setStyleSheet("margin: 15px; color: #2e7d32; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # Variables
        self.dialogs = []
    
    def test_crear_linux(self):
        """Test Linux optimisé de CrearFacturaDialog"""
        try:
            self.status_label.setText("🐧 OUVERTURE LINUX: CrearFacturaDialog...")
            
            # Créer le dialog avec solution Linux optimisée
            dialog = CrearFacturaDialog(None)  # Parent None pour éviter hiérarchie
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant LinuxDialogForegroundMixin
            dialog.show()
            
            self.status_label.setText("✅ CrearFacturaDialog ouvert - DOIT être au premier plan avec solution Linux!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur Linux: {e}")
    
    def test_editar_linux(self):
        """Test Linux optimisé de EditarFacturaDialog"""
        try:
            self.status_label.setText("🐧 OUVERTURE LINUX: EditarFacturaDialog...")
            
            # Données fictives
            factura_data = {
                'id': 1, 'numero': 'LINUX-TEST-001', 'cliente_id': 1,
                'cliente_nombre': 'Test Linux GNOME', 'fecha': '2025-12-07',
                'total': 1337.00, 'estado': 'Test Linux', 'lineas': []
            }
            
            # Créer le dialog avec solution Linux optimisée
            dialog = EditarFacturaDialog(factura_data, None)  # Parent None
            self.dialogs.append(dialog)
            
            # Le dialog utilise maintenant LinuxDialogForegroundMixin
            dialog.show()
            
            self.status_label.setText("✅ EditarFacturaDialog ouvert - DOIT être au premier plan avec solution Linux!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur Linux: {e}")
    
    def test_stress_linux(self):
        """Test de stress Linux - Ouverture multiple rapide"""
        try:
            self.status_label.setText("🚀 TEST STRESS LINUX: Ouverture de 5 fenêtres...")
            
            # Fermer les dialogs précédents
            for dialog in self.dialogs:
                if dialog:
                    dialog.close()
            self.dialogs.clear()
            
            # Ouvrir 5 fenêtres rapidement avec délais courts
            def ouvrir_crear1():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_editar1():
                factura_data = {'id': 1, 'numero': 'STRESS-1', 'cliente_id': 1,
                               'cliente_nombre': 'Stress Test 1', 'fecha': '2025-12-07',
                               'total': 100, 'estado': 'Test', 'lineas': []}
                dialog = EditarFacturaDialog(factura_data, None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_crear2():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_editar2():
                factura_data = {'id': 2, 'numero': 'STRESS-2', 'cliente_id': 2,
                               'cliente_nombre': 'Stress Test 2', 'fecha': '2025-12-07',
                               'total': 200, 'estado': 'Test', 'lineas': []}
                dialog = EditarFacturaDialog(factura_data, None)
                self.dialogs.append(dialog)
                dialog.show()
            
            def ouvrir_crear3():
                dialog = CrearFacturaDialog(None)
                self.dialogs.append(dialog)
                dialog.show()
            
            # Ouvrir avec délais très courts pour tester la robustesse
            ouvrir_crear1()
            QTimer.singleShot(100, ouvrir_editar1)
            QTimer.singleShot(200, ouvrir_crear2)
            QTimer.singleShot(300, ouvrir_editar2)
            QTimer.singleShot(400, ouvrir_crear3)
            
            QTimer.singleShot(800, lambda: self.status_label.setText(
                "✅ 5 fenêtres ouvertes - TOUTES doivent être au premier plan avec solution Linux!"
            ))
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur stress Linux: {e}")

def main():
    """Fonction principale"""
    print("🐧 TEST SOLUTION LINUX FINALE: Ventana Primer Plano")
    print("=" * 60)
    
    # Détecter l'environnement
    env = detect_linux_environment()
    print(f"🖥️ Environnement détecté: {env['desktop']} / {env['session']}")
    print(f"✅ GNOME: {env['is_gnome']}")
    print(f"✅ X11: {env['is_x11']}")
    print(f"✅ Wayland: {env['is_wayland']}")
    print()
    
    print("🎯 SOLUTION LINUX OPTIMISÉE:")
    print("   • LinuxDialogForegroundMixin avec détection automatique")
    print("   • Flags spécialisés pour GNOME/X11")
    print("   • WindowStaysOnTopHint prolongé (2 secondes)")
    print("   • Tentatives multiples avec délais croissants")
    print("   • Forçage système avec xprop")
    print("   • Override automatique de show()")
    print()
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre de test
    window = TestLinuxFinalWindow()
    window.show()
    
    print("🚀 Application de test Linux lancée!")
    print("📋 INSTRUCTIONS:")
    print("   1. Vérifiez l'environnement détecté dans l'interface")
    print("   2. Cliquez sur les boutons de test")
    print("   3. Vérifiez que CHAQUE fenêtre s'ouvre AU PREMIER PLAN")
    print("   4. Testez le stress test avec 5 fenêtres")
    print()
    print("🐧 RÉSULTAT ATTENDU: Toutes les fenêtres au premier plan sur Linux")
    
    # Lancer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
