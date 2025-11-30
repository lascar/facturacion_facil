# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des produits - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDoubleSpinBox, QTextEdit, QGroupBox, QSplitter,
    QFrame, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from utils.logger import get_logger
from utils.event_manager import event_manager

class ProductosPyQt6Window(BasePyQt6Window):
    """Fenêtre de gestion des produits en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Productos", 1000, 700)
        self.logger = get_logger("productos_pyqt6")
        self.current_product = None
        self.editing_mode = False

        # Connecter aux signaux d'événements
        self.connect_event_signals()

        self.logger.info("Inicializando ventana de gestión de productos PyQt6")

    def connect_event_signals(self):
        """Connecte aux signaux d'événements pour la synchronisation"""
        # Écouter les modifications de stock
        event_manager.stock_updated.connect(self.on_stock_updated)
        event_manager.stock_adjusted.connect(self.on_stock_adjusted)

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(splitter)
        
        # Panneau gauche - Formulaire
        self.create_form_panel(splitter)
        
        # Panneau droit - Liste des produits
        self.create_products_panel(splitter)
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_products()
    
    def create_form_panel(self, parent):
        """Crée le panneau de formulaire"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Groupe d'informations de base
        basic_group = QGroupBox("Información Básica")
        basic_layout = QGridLayout(basic_group)
        
        # Référence
        basic_layout.addWidget(QLabel("Referencia:"), 0, 0)
        self.ref_edit = QLineEdit()
        self.ref_edit.setPlaceholderText("Código único del producto")
        basic_layout.addWidget(self.ref_edit, 0, 1)
        
        # Nom
        basic_layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nombre del producto")
        basic_layout.addWidget(self.name_edit, 1, 1)
        
        # Catégorie
        basic_layout.addWidget(QLabel("Categoría:"), 2, 0)
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.load_categories()
        basic_layout.addWidget(self.category_combo, 2, 1)
        
        form_layout.addWidget(basic_group)
        
        # Groupe de prix
        price_group = QGroupBox("Precios")
        price_layout = QGridLayout(price_group)
        
        # Prix d'achat
        price_layout.addWidget(QLabel("Precio Compra:"), 0, 0)
        self.buy_price_spin = QDoubleSpinBox()
        self.buy_price_spin.setRange(0, 999999.99)
        self.buy_price_spin.setDecimals(2)
        self.buy_price_spin.setSuffix(" €")
        price_layout.addWidget(self.buy_price_spin, 0, 1)
        
        # Prix de vente
        price_layout.addWidget(QLabel("Precio Venta:"), 1, 0)
        self.sell_price_spin = QDoubleSpinBox()
        self.sell_price_spin.setRange(0, 999999.99)
        self.sell_price_spin.setDecimals(2)
        self.sell_price_spin.setSuffix(" €")
        price_layout.addWidget(self.sell_price_spin, 1, 1)
        
        form_layout.addWidget(price_group)
        
        # Groupe de description
        desc_group = QGroupBox("Descripción")
        desc_layout = QVBoxLayout(desc_group)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Descripción detallada del producto...")
        desc_layout.addWidget(self.description_edit)
        
        form_layout.addWidget(desc_group)
        
        # Stretch pour pousser vers le haut
        form_layout.addStretch()
        
        parent.addWidget(form_widget)
    
    def create_products_panel(self, parent):
        """Crée le panneau de liste des produits"""
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        
        # Titre
        title_label = QLabel("Lista de Productos")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        products_layout.addWidget(title_label)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar por referencia o nombre...")
        self.search_edit.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_edit)
        products_layout.addLayout(search_layout)
        
        # Table des produits
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "Referencia", "Nombre", "Categoría", "Precio Compra", "Precio Venta", "Stock"
        ])
        
        # Configuration de la table
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Referencia
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Nombre
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Categoría
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Precio Compra
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Precio Venta
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Stock
        
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.itemSelectionChanged.connect(self.on_product_selected)
        self.products_table.itemDoubleClicked.connect(self.on_product_double_clicked)
        
        products_layout.addWidget(self.products_table)
        
        parent.addWidget(products_widget)
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        self.logger.info("Creando botones de acción...")

        buttons_config = [
            ("Actualizar", self.refresh_products, "info"),
            ("Nuevo", self.new_product, "success"),
            ("Editar", self.edit_product, "info"),
            ("Guardar", self.save_product, "primary"),
            ("Eliminar", self.delete_product, "danger"),
            ("Cerrar", self.close, "secondary")
        ]

        self.logger.info(f"Configuración de botones: {[btn[0] for btn in buttons_config]}")

        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)

        self.logger.info("Botones añadidos al layout principal")

        # Désactiver certains boutons au démarrage
        self.update_button_states()
    
    def load_categories(self):
        """Charge les catégories disponibles"""
        try:
            categories = db.get_product_categories()
            self.category_combo.clear()
            self.category_combo.addItems(categories)
        except Exception as e:
            self.logger.error(f"Error cargando categorías: {e}")
    
    def load_products(self):
        """Charge la liste des produits"""
        try:
            products = db.get_all_products()
            
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product.get('referencia', ''))))
                self.products_table.setItem(row, 1, QTableWidgetItem(str(product.get('nombre', ''))))
                self.products_table.setItem(row, 2, QTableWidgetItem(str(product.get('categoria', ''))))
                self.products_table.setItem(row, 3, QTableWidgetItem(f"{product.get('precio_compra', 0):.2f} €"))
                self.products_table.setItem(row, 4, QTableWidgetItem(f"{product.get('precio_venta', 0):.2f} €"))

                # Colonne Stock avec couleur selon le niveau
                stock_actual = product.get('stock_actual', 0)
                stock_minimo = product.get('stock_minimo', 5)
                stock_item = QTableWidgetItem(str(stock_actual))
                stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Couleur selon le niveau de stock
                if stock_actual <= 0:
                    stock_item.setForeground(QColor("#dc3545"))  # Rouge pour stock épuisé
                elif stock_actual <= stock_minimo:
                    stock_item.setForeground(QColor("#fd7e14"))  # Orange pour stock bas
                else:
                    stock_item.setForeground(QColor("#28a745"))  # Vert pour stock OK

                self.products_table.setItem(row, 5, stock_item)

                # Stocker l'ID du produit
                self.products_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, product.get('id'))
            
            self.logger.info(f"Cargados {len(products)} productos")
            
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            self.show_error("Error", f"Error al cargar productos: {e}")

    def refresh_products(self):
        """Actualiza la lista de productos desde la base de datos"""
        try:
            # Compter les produits avant actualisation
            old_count = self.products_table.rowCount()

            # Recharger toutes les données depuis la base de données
            self.load_products()
            self.load_categories()

            # Compter les produits après actualisation
            new_count = self.products_table.rowCount()

            # Message de confirmation détaillé
            message = f"🔄 {new_count} productos actualizados desde la base de datos"
            self.show_temporary_status(message, 4000)

            # Log détaillé
            self.logger.info(f"Productos actualizados: {new_count} productos cargados desde la base de datos")

            # Afficher une notification plus visible
            self.show_info("Actualización Completa",
                          f"✅ Productos actualizados correctamente\n\n"
                          f"📦 Productos cargados: {new_count}\n"
                          f"🔄 Datos sincronizados con la base de datos\n\n"
                          f"Todos los cambios realizados en otras ventanas\n"
                          f"están ahora visibles en la lista.")

        except Exception as e:
            self.logger.error(f"Error actualizando productos: {e}")
            self.show_temporary_status("❌ Error al actualizar productos", 3000)
            self.show_error("Error de Actualización",
                           f"No se pudieron actualizar los productos:\n{str(e)}")
    
    def filter_products(self):
        """Filtre les produits selon le texte de recherche"""
        search_text = self.search_edit.text().lower()
        
        for row in range(self.products_table.rowCount()):
            show_row = False
            
            # Vérifier dans référence et nom
            for col in [0, 1]:  # Référence et nom
                item = self.products_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            self.products_table.setRowHidden(row, not show_row)
    
    def on_product_selected(self):
        """Gère la sélection d'un produit"""
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            # Charger les données du produit dans le formulaire
            ref_item = self.products_table.item(current_row, 0)
            if ref_item:
                product_id = ref_item.data(Qt.ItemDataRole.UserRole)
                self.load_product_data(product_id)
                self.editing_mode = False  # Sortir du mode édition
                self.update_button_states()
                self.update_form_style()

    def on_product_double_clicked(self, item):
        """Gère le double-clic sur un produit (lance l'édition)"""
        if self.current_product:
            self.edit_product()
    
    def load_product_data(self, product_id):
        """Charge les données d'un produit dans le formulaire"""
        try:
            product = db.get_product_by_id(product_id)
            if product:
                self.current_product = product
                
                self.ref_edit.setText(str(product.get('referencia', '')))
                self.name_edit.setText(str(product.get('nombre', '')))
                self.category_combo.setCurrentText(str(product.get('categoria', '')))
                self.buy_price_spin.setValue(float(product.get('precio_compra', 0)))
                self.sell_price_spin.setValue(float(product.get('precio_venta', 0)))
                self.description_edit.setPlainText(str(product.get('descripcion', '')))
                
        except Exception as e:
            self.logger.error(f"Error cargando producto {product_id}: {e}")
            self.show_error("Error", f"Error al cargar producto: {e}")
    
    def new_product(self):
        """Prépare un nouveau produit"""
        self.current_product = None
        self.editing_mode = True  # Mode création = mode édition
        self.clear_form()
        self.ref_edit.setFocus()
        self.update_button_states()
        self.update_form_style()

    def edit_product(self):
        """Active le mode édition pour le produit sélectionné"""
        if not self.current_product:
            self.show_warning("Selección", "Selecciona un producto para editar")
            return

        self.editing_mode = True
        self.ref_edit.setFocus()
        self.update_button_states()
        self.update_form_style()
        self.show_info("Edición", f"Editando producto: {self.current_product.get('nombre', '')}")

    def update_form_style(self):
        """Met à jour le style du formulaire selon le mode"""
        if self.editing_mode:
            # Style pour mode édition
            style = "QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit { border: 2px solid #3498db; background-color: #f8f9fa; }"
        else:
            # Style normal
            style = "QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit { border: 1px solid #ddd; background-color: white; }"

        # Appliquer le style au groupe de formulaire
        if hasattr(self, 'form_group'):
            self.form_group.setStyleSheet(style)

    def update_button_states(self):
        """Met à jour l'état des boutons selon le contexte"""
        # Vérifier que les attributs existent
        if not hasattr(self, 'current_product') or not hasattr(self, 'main_layout'):
            return

        # Récupérer les boutons depuis le layout
        buttons = {}
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and hasattr(item, 'layout') and item.layout():
                layout = item.layout()
                for j in range(layout.count()):
                    widget = layout.itemAt(j).widget()
                    if isinstance(widget, QPushButton):
                        buttons[widget.text()] = widget

        # État des boutons selon le contexte
        has_selection = self.current_product is not None
        is_editing = getattr(self, 'editing_mode', False)

        # Le bouton Actualizar est toujours actif
        if 'Actualizar' in buttons:
            buttons['Actualizar'].setEnabled(True)
        if 'Editar' in buttons:
            buttons['Editar'].setEnabled(has_selection and not is_editing)
        if 'Eliminar' in buttons:
            buttons['Eliminar'].setEnabled(has_selection and not is_editing)
        if 'Guardar' in buttons:
            buttons['Guardar'].setEnabled(is_editing or not has_selection)
    
    def clear_form(self):
        """Vide le formulaire"""
        self.ref_edit.clear()
        self.name_edit.clear()
        self.category_combo.setCurrentText("")
        self.buy_price_spin.setValue(0)
        self.sell_price_spin.setValue(0)
        self.description_edit.clear()
    
    def save_product(self):
        """Sauvegarde le produit"""
        try:
            # Validation
            if not self.ref_edit.text().strip():
                self.show_warning("Validación", "La referencia es obligatoria")
                return
            
            if not self.name_edit.text().strip():
                self.show_warning("Validación", "El nombre es obligatorio")
                return
            
            # Préparer les données
            product_data = {
                'referencia': self.ref_edit.text().strip(),
                'nombre': self.name_edit.text().strip(),
                'categoria': self.category_combo.currentText().strip(),
                'precio_compra': self.buy_price_spin.value(),
                'precio_venta': self.sell_price_spin.value(),
                'descripcion': self.description_edit.toPlainText().strip()
            }
            
            # Sauvegarder
            if self.current_product and self.editing_mode:
                # Mise à jour
                product_data['id'] = self.current_product['id']
                db.update_product(product_data)
                self.show_info("Éxito", "Producto actualizado correctamente")
                self.editing_mode = False

                # Émettre signal de modification
                event_manager.emit_product_updated(product_data)
            else:
                # Nouveau produit
                product_id = db.add_product(product_data)
                if product_id:
                    product_data['id'] = product_id
                self.show_info("Éxito", "Producto creado correctamente")
                self.current_product = None
                self.editing_mode = False

                # Émettre signal de création
                event_manager.emit_product_created(product_data)

            # Recharger la liste
            self.load_products()
            self.load_categories()
            self.update_button_states()
            self.update_form_style()
            
        except Exception as e:
            self.logger.error(f"Error guardando producto: {e}")
            self.show_error("Error", f"Error al guardar producto: {e}")
    
    def delete_product(self):
        """Supprime le produit sélectionné"""
        if not self.current_product:
            self.show_warning("Selección", "Selecciona un producto para eliminar")
            return
        
        if self.ask_question("Confirmar",
                           f"¿Estás seguro de eliminar el producto '{self.current_product.get('nombre', '')}'?"):
            try:
                product_id = self.current_product['id']
                db.delete_product(product_id)
                self.show_info("Éxito", "Producto eliminado correctamente")

                # Émettre signal de suppression
                event_manager.emit_product_deleted(product_id)

                self.clear_form()
                self.current_product = None
                self.load_products()
                
            except Exception as e:
                self.logger.error(f"Error eliminando producto: {e}")
                self.show_error("Error", f"Error al eliminar producto: {e}")

    # Méthodes de gestion des événements
    def on_stock_updated(self, product_id, new_stock):
        """Gère la mise à jour de stock d'un produit"""
        self.logger.debug(f"Stock mis à jour: produit {product_id}, nouveau stock {new_stock}")
        # Mettre à jour la colonne stock dans la table
        self.update_product_stock_in_table(product_id, new_stock)

    def on_stock_adjusted(self, product_id, old_stock, new_stock):
        """Gère l'ajustement de stock d'un produit"""
        self.logger.debug(f"Stock ajusté: produit {product_id}, {old_stock} -> {new_stock}")
        # Mettre à jour la colonne stock dans la table
        self.update_product_stock_in_table(product_id, new_stock)

        # Afficher une notification temporaire si le produit est actuellement sélectionné
        if (self.current_product and
            self.current_product.get('id') == product_id):
            self.show_temporary_status(f"📦 Stock actualizado: {old_stock} → {new_stock}", 3000)

    def update_product_stock_in_table(self, product_id, new_stock):
        """Met à jour la colonne stock d'un produit spécifique dans la table"""
        try:
            # Chercher la ligne correspondant au produit
            for row in range(self.products_table.rowCount()):
                ref_item = self.products_table.item(row, 0)  # Colonne référence
                if ref_item and ref_item.data(Qt.ItemDataRole.UserRole) == product_id:
                    # Mettre à jour la colonne stock (colonne 5)
                    stock_item = self.products_table.item(row, 5)
                    if stock_item:
                        stock_item.setText(str(new_stock))

                        # Mettre à jour la couleur selon le nouveau stock
                        # Obtenir le stock minimum (par défaut 5)
                        stock_minimo = 5  # Valeur par défaut, pourrait être récupérée de la BD

                        if new_stock <= 0:
                            stock_item.setForeground(QColor("#dc3545"))  # Rouge
                        elif new_stock <= stock_minimo:
                            stock_item.setForeground(QColor("#fd7e14"))  # Orange
                        else:
                            stock_item.setForeground(QColor("#28a745"))  # Vert
                    break

        except Exception as e:
            self.logger.error(f"Error actualizando stock en tabla: {e}")
