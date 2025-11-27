# -*- coding: utf-8 -*-
"""
Fenêtre de gestion du stock - Version PyQt5 native
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox, QGroupBox, QSplitter, QFrame, QWidget
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtGui import QFont

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import db
from utils.logger import get_logger

class StockPyQt5Window(BasePyQt5Window):
    """Fenêtre de gestion du stock avec PyQt5"""
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Gestión de Stock", 1000, 700)
        
        # Variables
        self.productos = []
        self.selected_product_id = None
        
        # Charger les données
        self.load_stock_data()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Layout principal
        main_layout = QHBoxLayout(self)
        
        # Splitter pour diviser l'interface
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Configuration des sections
        self.setup_stock_list(splitter)
        self.setup_stock_form(splitter)
        
        # Boutons
        buttons_layout = QVBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.adjust_btn = QPushButton("📊 Ajustar Stock")
        
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addWidget(self.adjust_btn)
        buttons_layout.addStretch()
        
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        buttons_widget.setMaximumWidth(150)
        main_layout.addWidget(buttons_widget)
        
        # Connexions
        self.setup_connections()
        
        # Appliquer le style
        self.apply_style()
        
    def setup_stock_list(self, parent):
        """Configurer la liste des stocks"""
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Label
        list_label = QLabel("Stock de Productos")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        list_layout.addWidget(list_label)
        
        # Table des stocks
        self.stock_table = QTableWidget()
        headers = ["ID", "Producto", "Referencia", "Stock Actual", "Stock Mínimo", "Estado"]
        self.setup_table_widget(self.stock_table, headers)
        
        # Connecter la sélection
        self.stock_table.itemSelectionChanged.connect(self.on_product_selected)
        
        list_layout.addWidget(self.stock_table)
        parent.addWidget(list_widget)
        
    def setup_stock_form(self, parent):
        """Configurer le formulaire d'ajustement de stock"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # GroupBox pour le formulaire
        form_group = QGroupBox("Ajustar Stock")
        form_group_layout = QGridLayout(form_group)
        
        # Champs du formulaire
        self.producto_label = QLabel("Producto: -")
        self.stock_actual_label = QLabel("Stock Actual: -")
        
        self.nuevo_stock_edit = QSpinBox()
        self.nuevo_stock_edit.setMaximum(999999)
        self.nuevo_stock_edit.setMinimum(0)
        
        self.stock_minimo_edit = QSpinBox()
        self.stock_minimo_edit.setMaximum(999999)
        self.stock_minimo_edit.setMinimum(0)
        
        # Ajouter les champs au layout
        form_group_layout.addWidget(self.producto_label, 0, 0, 1, 2)
        form_group_layout.addWidget(self.stock_actual_label, 1, 0, 1, 2)
        
        form_group_layout.addWidget(QLabel("Nuevo Stock:"), 2, 0)
        form_group_layout.addWidget(self.nuevo_stock_edit, 2, 1)
        
        form_group_layout.addWidget(QLabel("Stock Mínimo:"), 3, 0)
        form_group_layout.addWidget(self.stock_minimo_edit, 3, 1)
        
        form_layout.addWidget(form_group)
        form_layout.addStretch()
        
        parent.addWidget(form_widget)
        
    def setup_connections(self):
        """Configurer les connexions de signaux"""
        self.refresh_btn.clicked.connect(self.load_stock_data)
        self.adjust_btn.clicked.connect(self.adjust_stock)
        
    def load_stock_data(self):
        """Charger les données de stock depuis la base de données"""
        try:
            self.productos = db.get_all_products()
            self.update_stock_table()
        except Exception as e:
            self.logger.error(f"Erreur chargement stock: {e}")
            self.show_error("Erreur", f"Impossible de charger le stock: {str(e)}")
            
    def update_stock_table(self):
        """Mettre à jour la table des stocks"""
        self.stock_table.setRowCount(len(self.productos))
        
        for row, producto in enumerate(self.productos):
            stock_actual = int(producto.get('stock_actual', 0))
            stock_minimo = int(producto.get('stock_minimo', 5))
            
            # Déterminer l'état du stock
            if stock_actual <= 0:
                estado = "❌ Agotado"
            elif stock_actual <= stock_minimo:
                estado = "⚠️ Bajo"
            else:
                estado = "✅ OK"
            
            self.stock_table.setItem(row, 0, QTableWidgetItem(str(producto.get('id', ''))))
            self.stock_table.setItem(row, 1, QTableWidgetItem(str(producto.get('nombre', ''))))
            self.stock_table.setItem(row, 2, QTableWidgetItem(str(producto.get('referencia', ''))))
            self.stock_table.setItem(row, 3, QTableWidgetItem(str(stock_actual)))
            self.stock_table.setItem(row, 4, QTableWidgetItem(str(stock_minimo)))
            self.stock_table.setItem(row, 5, QTableWidgetItem(estado))

    def on_product_selected(self):
        """Gérer la sélection d'un produit"""
        current_row = self.stock_table.currentRow()
        if current_row >= 0 and current_row < len(self.productos):
            producto = self.productos[current_row]
            self.selected_product_id = producto.get('id')
            self.load_product_data(producto)

    def load_product_data(self, producto):
        """Charger les données d'un produit dans le formulaire"""
        self.producto_label.setText(f"Producto: {producto.get('nombre', '')}")
        self.stock_actual_label.setText(f"Stock Actual: {int(producto.get('stock_actual', 0))}")
        self.nuevo_stock_edit.setValue(int(producto.get('stock_actual', 0)))
        self.stock_minimo_edit.setValue(int(producto.get('stock_minimo', 5)))

    def adjust_stock(self):
        """Ajuster le stock du produit sélectionné"""
        if not self.selected_product_id:
            self.show_warning("Selección", "Seleccione un producto para ajustar el stock")
            return

        try:
            nuevo_stock = self.nuevo_stock_edit.value()
            stock_minimo = self.stock_minimo_edit.value()

            # Mettre à jour le stock dans la table productos
            db.update_product_stock(self.selected_product_id, nuevo_stock)

            # Mettre à jour aussi le stock minimum
            self.update_stock_minimo(self.selected_product_id, stock_minimo)

            self.show_info("Éxito", f"Stock actualizado a {nuevo_stock} unidades\nStock mínimo: {stock_minimo}")

            # Recharger les données
            self.load_stock_data()

        except Exception as e:
            self.logger.error(f"Erreur ajustement stock: {e}")
            self.show_error("Error", f"Error al ajustar el stock: {str(e)}")

    def update_stock_minimo(self, product_id, stock_minimo):
        """Mettre à jour le stock minimum d'un produit"""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET stock_minimo = ? WHERE id = ?", (stock_minimo, product_id))
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Erreur mise à jour stock minimum: {e}")
            raise e
