#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test en direct de l'interface des produits
"""

import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt
from ui.productos_pyqt5 import ProductosPyQt5Window

class TestWindow(QWidget):
    """Fenêtre de test pour l'interface des produits"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Interface Produits - Catégories")
        self.setGeometry(100, 100, 800, 600)
        
        # Créer l'interface des produits
        self.productos_window = ProductosPyQt5Window()
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("🧪 TEST INTERFACE PRODUITS - CATÉGORIES")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Boutons de test
        buttons_layout = QHBoxLayout()
        
        # Bouton pour afficher l'état du combo
        btn_debug_combo = QPushButton("🔍 Debug Combo")
        btn_debug_combo.clicked.connect(self.debug_combo)
        buttons_layout.addWidget(btn_debug_combo)
        
        # Bouton pour recharger les catégories
        btn_reload_categories = QPushButton("🔄 Recharger Catégories")
        btn_reload_categories.clicked.connect(self.reload_categories)
        buttons_layout.addWidget(btn_reload_categories)
        
        # Bouton pour sélectionner le produit
        btn_select_product = QPushButton("📋 Sélectionner Produit")
        btn_select_product.clicked.connect(self.select_product)
        buttons_layout.addWidget(btn_select_product)
        
        # Bouton pour forcer la sélection de catégorie
        btn_force_category = QPushButton("🎯 Forcer Catégorie")
        btn_force_category.clicked.connect(self.force_category)
        buttons_layout.addWidget(btn_force_category)
        
        layout.addLayout(buttons_layout)
        
        # Zone d'information
        self.info_label = QLabel("Clique sur les boutons pour tester l'interface")
        self.info_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Ajouter l'interface des produits
        layout.addWidget(self.productos_window)
        
        self.setLayout(layout)
    
    def debug_combo(self):
        """Debug l'état du combo box"""
        combo = self.productos_window.categoria_combo
        
        info = f"🔍 ÉTAT DU COMBO BOX:\n"
        info += f"• Nombre d'options: {combo.count()}\n"
        info += f"• Texte actuel: '{combo.currentText()}'\n"
        info += f"• Index actuel: {combo.currentIndex()}\n"
        info += f"• Options disponibles:\n"
        
        for i in range(combo.count()):
            text = combo.itemText(i)
            marker = " ← SÉLECTIONNÉ" if i == combo.currentIndex() else ""
            info += f"  {i}: '{text}'{marker}\n"
        
        # Vérifier les produits
        if self.productos_window.productos:
            producto = self.productos_window.productos[0]
            info += f"\n📝 PRODUIT CHARGÉ:\n"
            info += f"• Nom: {producto.get('nombre')}\n"
            info += f"• Catégorie: '{producto.get('categoria')}'\n"
            info += f"• ID sélectionné: {self.productos_window.selected_producto_id}\n"
        
        self.info_label.setText(info)
    
    def reload_categories(self):
        """Recharger les catégories"""
        self.productos_window.load_categories()
        self.info_label.setText("🔄 Catégories rechargées !")
        self.debug_combo()
    
    def select_product(self):
        """Sélectionner le premier produit"""
        if self.productos_window.productos:
            producto = self.productos_window.productos[0]
            self.productos_window.selected_producto_id = producto.get('id')
            self.productos_window.load_product_data(producto)
            
            self.info_label.setText(f"📋 Produit sélectionné: {producto.get('nombre')}")
            self.debug_combo()
        else:
            self.info_label.setText("❌ Aucun produit disponible")
    
    def force_category(self):
        """Forcer la sélection de la catégorie"""
        if self.productos_window.productos:
            producto = self.productos_window.productos[0]
            categoria = producto.get('categoria')
            
            if categoria:
                combo = self.productos_window.categoria_combo
                
                # Méthode 1: setCurrentText
                combo.setCurrentText(categoria)
                
                # Méthode 2: findText + setCurrentIndex
                index = combo.findText(categoria)
                if index >= 0:
                    combo.setCurrentIndex(index)
                
                # Forcer le rafraîchissement
                combo.update()
                combo.repaint()
                
                self.info_label.setText(f"🎯 Catégorie forcée: '{categoria}'")
                self.debug_combo()
            else:
                self.info_label.setText("❌ Pas de catégorie à forcer")
        else:
            self.info_label.setText("❌ Aucun produit disponible")

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Créer la fenêtre de test
    window = TestWindow()
    window.show()
    
    # Lancer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
