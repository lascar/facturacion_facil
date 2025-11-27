# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des produits - Version PySide6 native
"""

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDoubleSpinBox, QTextEdit, QGroupBox, QSplitter,
    QFrame, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui.base_pyside6_window import BasePySide6Window
from database.database import db
from utils.logger import get_logger

class ProductosPySide6Window(BasePySide6Window):
    """Fenêtre de gestion des produits avec PySide6"""
    
    # Signaux
    producto_selected = Signal(dict)
    producto_updated = Signal(int)
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Gestión de Productos", 1000, 700)
        
        # Variables
        self.productos = []
        self.selected_producto_id = None
        
        # Charger les données
        self.load_productos()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        main_layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel("Gestión de Productos")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Partie gauche - Liste des produits
        self.setup_products_list(splitter)
        
        # Partie droite - Formulaire
        self.setup_product_form(splitter)
        
        # Boutons
        buttons_layout = self.create_button_layout([
            ("Nuevo", self.new_producto),
            ("Guardar", self.save_producto),
            ("Eliminar", self.delete_producto),
            ("Cerrar", self.close)
        ])
        main_layout.addLayout(buttons_layout)
        
        # Appliquer le style
        self.apply_style()
        
    def setup_products_list(self, parent):
        """Configurer la liste des produits"""
        # Widget conteneur
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Label
        list_label = QLabel("Lista de Productos")
        list_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        list_layout.addWidget(list_label)
        
        # Table des produits
        self.products_table = QTableWidget()
        headers = ["ID", "Nombre", "Precio", "Stock", "Categoría"]
        self.setup_table_widget(self.products_table, headers)
        
        # Connecter la sélection
        self.products_table.itemSelectionChanged.connect(self.on_product_selected)
        
        list_layout.addWidget(self.products_table)
        parent.addWidget(list_widget)
        
    def setup_product_form(self, parent):
        """Configurer le formulaire de produit"""
        # Widget conteneur
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # GroupBox pour le formulaire
        form_group = QGroupBox("Detalles del Producto")
        form_group_layout = QGridLayout(form_group)
        
        # Champs du formulaire
        self.nombre_edit = QLineEdit()
        self.precio_edit = QDoubleSpinBox()
        self.precio_edit.setMaximum(999999.99)
        self.precio_edit.setDecimals(2)
        
        self.stock_edit = QDoubleSpinBox()
        self.stock_edit.setMaximum(999999.99)
        self.stock_edit.setDecimals(2)
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Producto", "Servicio", "Material", "Otro"])
        
        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(100)
        
        # Ajouter les champs au layout
        form_group_layout.addWidget(QLabel("Nombre:"), 0, 0)
        form_group_layout.addWidget(self.nombre_edit, 0, 1)
        
        form_group_layout.addWidget(QLabel("Precio:"), 1, 0)
        form_group_layout.addWidget(self.precio_edit, 1, 1)
        
        form_group_layout.addWidget(QLabel("Stock:"), 2, 0)
        form_group_layout.addWidget(self.stock_edit, 2, 1)
        
        form_group_layout.addWidget(QLabel("Categoría:"), 3, 0)
        form_group_layout.addWidget(self.categoria_combo, 3, 1)
        
        form_group_layout.addWidget(QLabel("Descripción:"), 4, 0)
        form_group_layout.addWidget(self.descripcion_edit, 4, 1)
        
        form_layout.addWidget(form_group)
        form_layout.addStretch()
        
        parent.addWidget(form_widget)
        
    def setup_connections(self):
        """Configurer les connexions de signaux"""
        # Connecter les changements de données
        self.nombre_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.precio_edit.valueChanged.connect(lambda: self.set_data_modified(True))
        self.stock_edit.valueChanged.connect(lambda: self.set_data_modified(True))
        self.categoria_combo.currentTextChanged.connect(lambda: self.set_data_modified(True))
        self.descripcion_edit.textChanged.connect(lambda: self.set_data_modified(True))
        
    def load_productos(self):
        """Charger les produits depuis la base de données"""
        try:
            self.productos = db.get_all_productos()
            self.update_products_table()
        except Exception as e:
            self.logger.error(f"Erreur chargement produits: {e}")
            self.show_error("Erreur", f"Impossible de charger les produits: {str(e)}")
            
    def update_products_table(self):
        """Mettre à jour la table des produits"""
        self.products_table.setRowCount(len(self.productos))
        
        for row, producto in enumerate(self.productos):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(producto.get('id', ''))))
            self.products_table.setItem(row, 1, QTableWidgetItem(str(producto.get('nombre', ''))))
            self.products_table.setItem(row, 2, QTableWidgetItem(f"{producto.get('precio', 0):.2f}"))
            self.products_table.setItem(row, 3, QTableWidgetItem(f"{producto.get('stock', 0):.2f}"))
            self.products_table.setItem(row, 4, QTableWidgetItem(str(producto.get('categoria', ''))))
            
    def on_product_selected(self):
        """Gérer la sélection d'un produit"""
        current_row = self.products_table.currentRow()
        if current_row >= 0 and current_row < len(self.productos):
            producto = self.productos[current_row]
            self.selected_producto_id = producto.get('id')
            self.load_product_data(producto)
            self.producto_selected.emit(producto)
            
    def load_product_data(self, producto):
        """Charger les données d'un produit dans le formulaire"""
        self.nombre_edit.setText(str(producto.get('nombre', '')))
        self.precio_edit.setValue(float(producto.get('precio', 0)))
        self.stock_edit.setValue(float(producto.get('stock', 0)))
        
        categoria = str(producto.get('categoria', 'Producto'))
        index = self.categoria_combo.findText(categoria)
        if index >= 0:
            self.categoria_combo.setCurrentIndex(index)
            
        self.descripcion_edit.setPlainText(str(producto.get('descripcion', '')))
        self.set_data_modified(False)
        
    def new_producto(self):
        """Créer un nouveau produit"""
        self.selected_producto_id = None
        self.nombre_edit.clear()
        self.precio_edit.setValue(0.0)
        self.stock_edit.setValue(0.0)
        self.categoria_combo.setCurrentIndex(0)
        self.descripcion_edit.clear()
        self.set_data_modified(False)
        
    def save_producto(self):
        """Sauvegarder le produit"""
        try:
            # Validation basique
            if not self.nombre_edit.text().strip():
                self.show_warning("Validation", "Le nom du produit est requis")
                return
                
            # Préparer les données
            producto_data = {
                'nombre': self.nombre_edit.text().strip(),
                'precio': self.precio_edit.value(),
                'stock': self.stock_edit.value(),
                'categoria': self.categoria_combo.currentText(),
                'descripcion': self.descripcion_edit.toPlainText().strip()
            }
            
            # Sauvegarder
            if self.selected_producto_id:
                # Mise à jour
                producto_data['id'] = self.selected_producto_id
                db.update_producto(producto_data)
                self.show_info("Éxito", "Producto actualizado correctamente")
            else:
                # Nouveau produit
                new_id = db.add_producto(producto_data)
                self.selected_producto_id = new_id
                self.show_info("Éxito", "Producto creado correctamente")
            
            # Recharger les données
            self.load_productos()
            self.set_data_modified(False)
            self.producto_updated.emit(self.selected_producto_id or 0)
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde produit: {e}")
            self.show_error("Error", f"Error al guardar el producto: {str(e)}")
            
    def delete_producto(self):
        """Supprimer le produit sélectionné"""
        if not self.selected_producto_id:
            self.show_warning("Selección", "Seleccione un producto para eliminar")
            return
            
        if self.ask_confirmation("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                db.delete_producto(self.selected_producto_id)
                self.show_info("Éxito", "Producto eliminado correctamente")
                self.load_productos()
                self.new_producto()
            except Exception as e:
                self.logger.error(f"Erreur suppression produit: {e}")
                self.show_error("Error", f"Error al eliminar el producto: {str(e)}")
