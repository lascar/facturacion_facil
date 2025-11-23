#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de liste de produits avec mini-images - Version PyQt6
"""

try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QScrollArea, QFrame, QPushButton)
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QPixmap, QFont
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

import os
from PIL import Image

class ProductoListWidget(QWidget):
    """Widget de liste de produits avec mini-images pour PyQt6"""
    
    # Signal émis quand un produit est sélectionné
    product_selected = pyqtSignal(dict)
    
    def __init__(self, parent=None, height=300):
        """Initialise le widget de liste"""
        if GUI_AVAILABLE:
            super().__init__(parent)
        
        self.parent = parent
        self.height = height
        self.items = []
        self.selected_index = -1
        
        if GUI_AVAILABLE:
            self.create_widgets()
        else:
            # Mock pour tests sans GUI
            self.frame = MockWidget()
            self.scroll_area = MockWidget()
            self.content_widget = MockWidget()
        
        print("ProductoListWidget inicializado")
    
    def create_widgets(self):
        """Crée les widgets PyQt6"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Zone de défilement
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(self.height)
        layout.addWidget(self.scroll_area)
        
        # Widget de contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(2)
        
        self.scroll_area.setWidget(self.content_widget)
        
        # Frame principal pour compatibilité
        self.frame = self
    
    def add_item(self, item_data, image_path=None):
        """Ajoute un item à la liste"""
        self.items.append({
            'data': item_data,
            'image_path': image_path
        })
        
        if GUI_AVAILABLE:
            self.refresh_display()
    
    def add_producto(self, producto, image_path=None):
        """Ajoute un produit (méthode de compatibilité)"""
        item_data = {
            'id': getattr(producto, 'id', None),
            'nombre': getattr(producto, 'nombre', ''),
            'precio': getattr(producto, 'precio', 0.0),
            'referencia': getattr(producto, 'referencia', '')
        }
        self.add_item(item_data, image_path)
    
    def clear_items(self):
        """Vide la liste"""
        self.items = []
        self.selected_index = -1
        
        if GUI_AVAILABLE:
            self.refresh_display()
    
    def refresh_display(self):
        """Actualise l'affichage de la liste"""
        if not GUI_AVAILABLE:
            return
        
        # Supprimer tous les widgets existants
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Ajouter les nouveaux items
        for index, item in enumerate(self.items):
            item_widget = self.create_item_widget(item, index)
            self.content_layout.addWidget(item_widget)
        
        # Spacer pour pousser les items vers le haut
        self.content_layout.addStretch()
    
    def create_item_widget(self, item, index):
        """Crée un widget pour un item"""
        item_frame = QFrame()
        item_frame.setFrameStyle(QFrame.Shape.Box)
        item_frame.setLineWidth(1)
        
        # Style de sélection
        if index == self.selected_index:
            item_frame.setStyleSheet("QFrame { background-color: #e3f2fd; border: 2px solid #2196f3; }")
        else:
            item_frame.setStyleSheet("QFrame { background-color: white; border: 1px solid #ddd; }")
        
        layout = QHBoxLayout(item_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image (si disponible)
        if item.get('image_path') and os.path.exists(item['image_path']):
            try:
                pixmap = QPixmap(item['image_path'])
                if not pixmap.isNull():
                    # Redimensionner à 32x32
                    scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
                    image_label = QLabel()
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setFixedSize(32, 32)
                    layout.addWidget(image_label)
            except Exception as e:
                print(f"Error cargando imagen: {e}")
        
        # Texte
        data = item['data']
        text = f"{data.get('nombre', '')} - {data.get('precio', 0):.2f}€"
        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 10))
        layout.addWidget(text_label)
        
        # Rendre cliquable
        item_frame.mousePressEvent = lambda event, idx=index: self.select_item(idx)
        
        return item_frame
    
    def select_item(self, index):
        """Sélectionne un item par index"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self.refresh_display()
            
            # Émettre le signal
            if GUI_AVAILABLE:
                self.product_selected.emit(self.items[index]['data'])
            
            return True
        return False
    
    def get_selected_item(self):
        """Obtient l'item sélectionné"""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]['data']
        return None
    
    def get_selected_index(self):
        """Obtient l'index sélectionné"""
        return self.selected_index if self.selected_index >= 0 else None
    
    def set_selected_index(self, index):
        """Établit l'index sélectionné"""
        return self.select_item(index)


class MockWidget:
    """Widget mock pour tests sans GUI"""
    
    def __init__(self):
        self.value = ""
        self.visible = True
    
    def setVisible(self, visible):
        self.visible = visible
    
    def setParent(self, parent):
        pass
