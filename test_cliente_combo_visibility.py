#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour diagnostiquer et corriger le problème de visibilité du client sélectionné
"""

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.database import db

class TestClienteComboDialog(QDialog):
    """Dialog de test pour le combo box des clients"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Visibilité Cliente Combo")
        self.setGeometry(300, 300, 500, 400)
        self.setup_ui()
        self.load_clientes()
    
    def setup_ui(self):
        """Configurer l'interface de test"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Test de Visibilité du Combo Box Cliente")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Combo box original (problématique)
        layout.addWidget(QLabel("Combo Box Original (problématique):"))
        self.combo_original = QComboBox()
        layout.addWidget(self.combo_original)
        
        # Combo box avec style amélioré
        layout.addWidget(QLabel("Combo Box avec Style Amélioré:"))
        self.combo_improved = QComboBox()
        self.combo_improved.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                color: #333333;
                min-height: 20px;
            }
            QComboBox:hover {
                border-color: #0078d4;
            }
            QComboBox:focus {
                border-color: #0078d4;
                background-color: #f0f8ff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #cccccc;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #cccccc;
                selection-background-color: #0078d4;
                selection-color: white;
                color: #333333;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.combo_improved)
        
        # Combo box avec format de texte amélioré
        layout.addWidget(QLabel("Combo Box avec Format de Texte Amélioré:"))
        self.combo_formatted = QComboBox()
        self.combo_formatted.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #bdc3c7;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #ecf0f1;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #34495e;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #3498db;
                selection-background-color: #3498db;
                selection-color: white;
                color: #2c3e50;
                font-size: 13px;
                font-weight: normal;
                padding: 5px;
            }
        """)
        layout.addWidget(self.combo_formatted)
        
        # Informations de sélection
        layout.addWidget(QLabel("Cliente sélectionné:"))
        self.selection_label = QLabel("Aucun client sélectionné")
        self.selection_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        layout.addWidget(self.selection_label)
        
        # Connecter les signaux
        self.combo_original.currentTextChanged.connect(self.on_selection_changed)
        self.combo_improved.currentTextChanged.connect(self.on_selection_changed)
        self.combo_formatted.currentTextChanged.connect(self.on_selection_changed)
        
        # Bouton de fermeture
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def load_clientes(self):
        """Charger les clients dans tous les combo boxes"""
        try:
            clientes = db.get_all_clients()
            
            # Vider tous les combos
            self.combo_original.clear()
            self.combo_improved.clear()
            self.combo_formatted.clear()
            
            # Ajouter l'option par défaut
            self.combo_original.addItem("Seleccionar cliente...", None)
            self.combo_improved.addItem("Seleccionar cliente...", None)
            self.combo_formatted.addItem("📋 Seleccionar cliente...", None)
            
            # Ajouter les clients
            for cliente in clientes:
                # Format original
                texto_original = f"{cliente['nombre']} - {cliente['nif']}"
                
                # Format amélioré avec icônes
                texto_mejorado = f"👤 {cliente['nombre']} • NIF: {cliente['nif']}"
                
                self.combo_original.addItem(texto_original, cliente)
                self.combo_improved.addItem(texto_original, cliente)
                self.combo_formatted.addItem(texto_mejorado, cliente)
            
            print(f"✅ Cargados {len(clientes)} clientes en los combo boxes")
            
        except Exception as e:
            print(f"❌ Error cargando clientes: {e}")
    
    def on_selection_changed(self, text):
        """Gérer le changement de sélection"""
        sender = self.sender()
        if sender:
            data = sender.currentData()
            if data:
                self.selection_label.setText(f"Cliente: {data['nombre']} (NIF: {data['nif']})")
            else:
                self.selection_label.setText("Aucun client sélectionné")

def main():
    """Fonction principale"""
    print("🧪 TEST VISIBILITÉ COMBO BOX CLIENTE")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    
    try:
        dialog = TestClienteComboDialog()
        dialog.show()
        
        print("\n📋 INSTRUCTIONS:")
        print("1. Sélectionne un client dans chaque combo box")
        print("2. Compare la lisibilité du texte sélectionné")
        print("3. Identifie quel style fonctionne le mieux")
        print("4. Ferme la fenêtre quand terminé")
        
        result = app.exec_()
        
        print("\n🎯 RÉSULTAT:")
        print("Le test permet de comparer 3 styles différents")
        print("Le style qui offre la meilleure lisibilité sera appliqué")
        
        return result == 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
