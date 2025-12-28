# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des produits - Version PyQt5 native
Refactorisée pour utiliser ProductoService (Phase 5)
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit, QGroupBox, QSplitter,
    QFrame, QScrollArea, QWidget, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtGui import QFont

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import db, Database
from services.producto_service import ProductoService
from utils.logger import get_logger
from utils.event_manager_pyqt5 import event_manager
from utils.exceptions import (
    ProductValidationError, ProductNotFoundError, DatabaseError
)

class ProductosPyQt5Window(BasePyQt5Window):
    """Fenêtre de gestion des produits avec PyQt5 - Refactorisée avec ProductoService"""

    # Signaux
    producto_selected = Signal(dict)
    producto_updated = Signal(int)

    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)

        # Service métier - utiliser le même chemin DB que l'ancienne instance
        # IMPORTANT: Initialiser AVANT super().__init__() car setup_ui() en a besoin
        db_path = db.db_path if hasattr(db, 'db_path') else None
        self.producto_service = ProductoService(db_path)

        # Référence à l'ancienne DB pour get_product_categories (temporaire)
        self.db = Database(db_path)

        # Variables
        self.productos = []
        self.selected_producto_id = None

        # Maintenant appeler super().__init__() qui va appeler setup_ui()
        super().__init__(parent, "Gestión de Productos", 1200, 700)

        # Charger les données
        self.load_productos()

        # Connecter aux signaux d'événements
        self.connect_event_signals()

    def load_categories(self):
        """Charger les catégories depuis la base de données"""
        try:
            # Utiliser l'ancienne DB pour get_product_categories (pas encore dans le service)
            categories = self.db.get_product_categories()

            # Ne pas ajouter de catégories par défaut - laisser vide si aucune catégorie n'existe

            # Vider et remplir le combo
            self.categoria_combo.clear()
            self.categoria_combo.addItem("")  # Option vide
            self.categoria_combo.addItems(categories)

        except Exception as e:
            self.logger.error(f"Erreur chargement catégories: {e}")
            # En cas d'erreur, laisser seulement l'option vide
            self.categoria_combo.clear()
            self.categoria_combo.addItem("")  # Option vide seulement
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Activer le scroll pour cette fenêtre
        self.enable_window_scroll(enable_horizontal=False, enable_vertical=True)

        # Obtenir le layout de contenu (scrollable ou normal)
        main_layout = self.get_content_layout()

        # Titre
        title_label = QLabel("Gestión de Productos")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Splitter principal (vertical pour plus de lisibilité)
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Partie gauche - Liste des produits
        self.setup_products_list(splitter)
        
        # Partie droite - Formulaire
        self.setup_product_form(splitter)
        
        # Boutons
        buttons_layout = self.create_button_layout([
            ("Actualizar", self.refresh_productos),
            ("Nuevo", self.new_producto),
            ("Guardar", self.save_producto),
            ("Eliminar", self.delete_producto),
            ("Cerrar", self.close)
        ])
        main_layout.addLayout(buttons_layout)
        
        # Appliquer le style
        self.apply_style()

        # Connecter les changements du formulaire pour synchronisation temps réel
        self.setup_form_connections()
        
    def setup_products_list(self, parent):
        """Configurer la liste des produits"""
        # Widget conteneur
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Label
        list_label = QLabel("Lista de Productos")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        list_layout.addWidget(list_label)
        
        # Table des produits
        self.products_table = QTableWidget()
        headers = ["ID", "Nombre", "Referencia", "Precio", "Talla", "Stock", "Categoría"]
        self.setup_table_widget(self.products_table, headers)

        # Configuration spécifique des largeurs de colonnes
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Nombre
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Referencia
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Precio
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Talla
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Stock
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Categoría

        # Connecter la sélection
        self.products_table.itemSelectionChanged.connect(self.on_product_selected)
        
        list_layout.addWidget(self.products_table)
        parent.addWidget(list_widget)
        
    def setup_product_form(self, parent):
        """Configurer le formulaire de produit"""
        # Widget conteneur scrollable
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)

        # GroupBox pour le formulaire
        form_group = QGroupBox("Detalles del Producto")
        form_group_layout = QGridLayout(form_group)

        # Champs du formulaire
        self.nombre_edit = QLineEdit()
        self.referencia_edit = QLineEdit()
        self.referencia_edit.setPlaceholderText("Ej: REF001 (opcional)")
        self.precio_edit = QDoubleSpinBox()
        self.precio_edit.setMaximum(999999.99)
        self.precio_edit.setDecimals(2)

        self.iva_edit = QDoubleSpinBox()
        self.iva_edit.setMaximum(100.0)
        self.iva_edit.setMinimum(0.0)
        self.iva_edit.setDecimals(2)
        self.iva_edit.setValue(21.0)  # IVA par défaut en Espagne
        self.iva_edit.setSuffix(" %")

        self.stock_edit = QSpinBox()
        self.stock_edit.setMaximum(999999)
        self.stock_edit.setMinimum(0)

        # Checkbox "Sin stock"
        self.sin_stock_checkbox = QCheckBox("Sin stock")
        self.sin_stock_checkbox.setToolTip("Si está marcado, este producto no gestiona stock")
        self.sin_stock_checkbox.stateChanged.connect(self.on_sin_stock_changed)

        self.categoria_combo = QComboBox()
        self.categoria_combo.setEditable(True)  # Permet d'ajouter de nouvelles catégories
        self.categoria_combo.lineEdit().setPlaceholderText("Escribir categoría o dejar vacío")
        self.load_categories()

        self.talla_edit = QLineEdit()
        self.talla_edit.setPlaceholderText("Ej: M, L, XL (opcional)")

        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(100)

        # Ajouter les champs au layout - Nouvelle disposition
        row = 0

        # Ligne 0: Nombre (sur toute la largeur)
        form_group_layout.addWidget(QLabel("Nombre:"), row, 0)
        form_group_layout.addWidget(self.nombre_edit, row, 1, 1, 3)
        row += 1

        # Ligne 1: Referencia (2/3) et Categoría + Talla (1/3 chacun, moitié-moitié)
        ref_cat_layout = QHBoxLayout()
        ref_cat_layout.addWidget(QLabel("Referencia:"))
        ref_cat_layout.addWidget(self.referencia_edit, 2)  # stretch factor 2 = 2/3
        ref_cat_layout.addWidget(QLabel("Categoría:"))
        ref_cat_layout.addWidget(self.categoria_combo, 1)  # stretch factor 1 = 1/6
        ref_cat_layout.addWidget(QLabel("Talla:"))
        ref_cat_layout.addWidget(self.talla_edit, 1)  # stretch factor 1 = 1/6
        form_group_layout.addLayout(ref_cat_layout, row, 0, 1, 4)
        row += 1

        # Ligne 2: Precio et IVA sur la même ligne
        form_group_layout.addWidget(QLabel("Precio:"), row, 0)
        form_group_layout.addWidget(self.precio_edit, row, 1)
        form_group_layout.addWidget(QLabel("IVA:"), row, 2)
        form_group_layout.addWidget(self.iva_edit, row, 3)
        row += 1

        # Ligne 3: Stock et checkbox "Sin stock"
        stock_layout = QHBoxLayout()
        stock_layout.addWidget(QLabel("Stock:"))
        stock_layout.addWidget(self.stock_edit, 1)
        stock_layout.addWidget(self.sin_stock_checkbox)
        stock_layout.addStretch()
        form_group_layout.addLayout(stock_layout, row, 0, 1, 4)
        row += 1

        # Ligne 4: Descripción (sur toute la largeur)
        form_group_layout.addWidget(QLabel("Descripción:"), row, 0)
        form_group_layout.addWidget(self.descripcion_edit, row, 1, 1, 3)

        form_layout.addWidget(form_group)
        form_layout.addStretch()

        form_scroll.setWidget(form_widget)
        parent.addWidget(form_scroll)

    def setup_connections(self):
        """Configurer les connexions de signaux"""
        # Connecter les changements de données
        self.nombre_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.referencia_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.precio_edit.valueChanged.connect(lambda: self.set_data_modified(True))
        self.iva_edit.valueChanged.connect(lambda: self.set_data_modified(True))
        self.stock_edit.valueChanged.connect(lambda: self.set_data_modified(True))
        self.categoria_combo.currentTextChanged.connect(lambda: self.set_data_modified(True))
        self.talla_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.descripcion_edit.textChanged.connect(lambda: self.set_data_modified(True))
        
    def load_productos(self):
        """Charger les produits depuis la base de données via ProductoService"""
        try:
            self.productos = self.producto_service.get_all_productos()
            self.update_products_table()
        except DatabaseError as e:
            self.logger.error(f"Erreur base de données: {e}")
            self.show_error("Error de Base de Datos", f"Impossible de charger les produits: {str(e)}")
        except Exception as e:
            self.logger.error(f"Erreur chargement produits: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")
            
    def update_products_table(self):
        """Mettre à jour la table des produits"""
        self.products_table.setRowCount(len(self.productos))

        for row, producto in enumerate(self.productos):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(producto.get('id', ''))))
            self.products_table.setItem(row, 1, QTableWidgetItem(str(producto.get('nombre', ''))))
            self.products_table.setItem(row, 2, QTableWidgetItem(str(producto.get('referencia', ''))))
            self.products_table.setItem(row, 3, QTableWidgetItem(f"{producto.get('precio_venta', 0):.2f}"))
            talla = producto.get('talla', '') or ''  # Convertir None en chaîne vide
            self.products_table.setItem(row, 4, QTableWidgetItem(str(talla)))
            self.products_table.setItem(row, 5, QTableWidgetItem(str(int(producto.get('stock_actual', 0)))))
            categoria = producto.get('categoria', '') or ''  # Convertir None en chaîne vide
            self.products_table.setItem(row, 6, QTableWidgetItem(str(categoria)))
            
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
        # Bloquer temporairement les signaux pour éviter les boucles
        self.nombre_edit.blockSignals(True)
        self.referencia_edit.blockSignals(True)
        self.precio_edit.blockSignals(True)
        self.iva_edit.blockSignals(True)
        self.stock_edit.blockSignals(True)
        self.categoria_combo.blockSignals(True)
        self.talla_edit.blockSignals(True)
        self.sin_stock_checkbox.blockSignals(True)

        try:
            self.nombre_edit.setText(str(producto.get('nombre', '')))

            # Gérer la référence NULL/None
            referencia = producto.get('referencia')
            self.referencia_edit.setText(str(referencia) if referencia else '')

            self.precio_edit.setValue(float(producto.get('precio_venta', 0)))
            self.iva_edit.setValue(float(producto.get('iva_recomendado', 21.0)))
            self.stock_edit.setValue(int(producto.get('stock_actual', 0)))

            # Gérer sin_stock
            sin_stock = producto.get('sin_stock', 0)
            self.sin_stock_checkbox.setChecked(bool(sin_stock))
            self.stock_edit.setEnabled(not bool(sin_stock))

            # Gérer la catégorie NULL/None
            categoria = producto.get('categoria')
            if categoria and categoria.strip():
                # S'assurer que les catégories sont chargées
                current_categories = [self.categoria_combo.itemText(i) for i in range(self.categoria_combo.count())]
                if categoria not in current_categories:
                    # Recharger les catégories si la catégorie n'est pas présente
                    self.load_categories()

                # Chercher et sélectionner la catégorie
                index = self.categoria_combo.findText(categoria)
                if index >= 0:
                    self.categoria_combo.setCurrentIndex(index)
                else:
                    # Si la catégorie n'existe toujours pas, l'ajouter
                    self.categoria_combo.addItem(categoria)
                    new_index = self.categoria_combo.findText(categoria)
                    if new_index >= 0:
                        self.categoria_combo.setCurrentIndex(new_index)

                # Vérification finale
                if self.categoria_combo.currentText() != categoria:
                    # Forcer la sélection avec setCurrentText en dernier recours
                    self.categoria_combo.setCurrentText(categoria)

                # Log pour debug
                self.logger.debug(f"Catégorie sélectionnée: '{categoria}' → Résultat: '{self.categoria_combo.currentText()}' (index: {self.categoria_combo.currentIndex()})")
            else:
                # Pas de catégorie, sélectionner l'option vide
                self.categoria_combo.setCurrentText("")

            # Gérer la talla NULL/None
            talla = producto.get('talla')
            self.talla_edit.setText(str(talla) if talla else '')

            self.descripcion_edit.setPlainText(str(producto.get('descripcion', '')))
            self.set_data_modified(False)
        finally:
            # Réactiver les signaux
            self.nombre_edit.blockSignals(False)
            self.referencia_edit.blockSignals(False)
            self.precio_edit.blockSignals(False)
            self.iva_edit.blockSignals(False)
            self.stock_edit.blockSignals(False)
            self.categoria_combo.blockSignals(False)
            self.talla_edit.blockSignals(False)
            self.sin_stock_checkbox.blockSignals(False)

    def new_producto(self):
        """Créer un nouveau produit"""
        self.clear_form()

    def clear_form(self):
        """Vider le formulaire"""
        self.selected_producto_id = None
        self.nombre_edit.clear()
        self.referencia_edit.clear()
        self.precio_edit.setValue(0.0)
        self.iva_edit.setValue(21.0)  # IVA par défaut
        self.stock_edit.setValue(0)
        self.categoria_combo.setCurrentText("")  # Commencer vide
        self.talla_edit.clear()
        self.descripcion_edit.clear()
        self.sin_stock_checkbox.setChecked(False)
        self.stock_edit.setEnabled(True)
        self.set_data_modified(False)

    def on_sin_stock_changed(self, state):
        """Gérer le changement du checkbox 'Sin stock'"""
        is_checked = bool(state)
        self.stock_edit.setEnabled(not is_checked)
        if is_checked:
            # Si "sin stock" est coché, mettre le stock à 0
            self.stock_edit.setValue(0)
        self.set_data_modified(True)
        
    def save_producto(self):
        """Sauvegarder le produit"""
        try:
            # Validation basique
            if not self.nombre_edit.text().strip():
                self.show_warning("Validation", "Le nom du produit est requis")
                return
                
            # Préparer les données
            # Gérer la référence vide (NULL au lieu de chaîne vide pour éviter UNIQUE constraint)
            referencia = self.referencia_edit.text().strip()
            referencia = referencia if referencia else None

            # Gérer la catégorie vide
            categoria = self.categoria_combo.currentText().strip()
            if categoria == "-- Sin categoría --" or not categoria:
                categoria = None

            # Gérer la talla vide
            talla = self.talla_edit.text().strip()
            talla = talla if talla else None

            producto_data = {
                'nombre': self.nombre_edit.text().strip(),
                'referencia': referencia,
                'precio_venta': self.precio_edit.value(),
                'iva_recomendado': self.iva_edit.value(),
                'stock': self.stock_edit.value() if not self.sin_stock_checkbox.isChecked() else 0,
                'categoria': categoria,
                'talla': talla,
                'sin_stock': self.sin_stock_checkbox.isChecked(),
                'descripcion': self.descripcion_edit.toPlainText().strip()
            }
            
            # Sauvegarder via ProductoService
            is_new_product = not bool(self.selected_producto_id)

            if self.selected_producto_id:
                # Mise à jour
                producto_data['id'] = self.selected_producto_id
                self.producto_service.update_producto(producto_data)
                self.show_info("Éxito", "Producto actualizado correctamente")
            else:
                # Nouveau produit
                new_id = self.producto_service.create_producto(producto_data)
                self.selected_producto_id = new_id
                self.show_info("Éxito", "Producto creado correctamente")

            # Recharger les données
            self.load_productos()
            self.load_categories()  # Recharger les catégories pour inclure les nouvelles
            self.set_data_modified(False)

            # Émettre des signaux pour notifier les autres fenêtres
            if self.selected_producto_id:
                # Obtenir les données du produit sauvegardé
                producto_data = None
                for p in self.productos:
                    if p.get('id') == self.selected_producto_id:
                        producto_data = p
                        break

                if producto_data:
                    if is_new_product:
                        event_manager.emit_product_created(producto_data)
                    else:
                        event_manager.emit_product_updated(producto_data)

            self.producto_updated.emit(self.selected_producto_id or 0)

        except ProductValidationError as e:
            self.logger.error(f"Erreur validation produit: {e}")
            self.show_error("Error de Validación", str(e))
        except ProductNotFoundError as e:
            self.logger.error(f"Produit non trouvé: {e}")
            self.show_error("Producto No Encontrado", str(e))
        except DatabaseError as e:
            self.logger.error(f"Erreur base de données: {e}")
            self.show_error("Error de Base de Datos", str(e))
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde produit: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")
            
    def delete_producto(self):
        """Supprimer le produit sélectionné via ProductoService"""
        if not self.selected_producto_id:
            self.show_warning("Selección", "Seleccione un producto para eliminar")
            return

        if self.ask_confirmation("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                self.producto_service.delete_producto(self.selected_producto_id)
                self.show_info("Éxito", "Producto eliminado correctamente")
                self.load_productos()
                self.new_producto()
            except ProductNotFoundError as e:
                self.logger.error(f"Produit non trouvé: {e}")
                self.show_error("Producto No Encontrado", str(e))
            except DatabaseError as e:
                self.logger.error(f"Erreur base de données: {e}")
                self.show_error("Error de Base de Datos", str(e))
            except Exception as e:
                self.logger.error(f"Erreur suppression produit: {e}")
                self.show_error("Error", f"Error inesperado: {str(e)}")

    def refresh_productos(self):
        """Actualiza la lista de productos desde la base de datos"""
        try:
            # Compter les produits avant actualisation
            old_count = len(self.productos)

            # Recharger toutes les données depuis la base de données
            self.load_productos()
            self.load_categories()

            # Compter les produits après actualisation
            new_count = len(self.productos)

            # Message de confirmation détaillé
            self.show_info("Actualización Completa",
                          f"✅ Productos actualizados correctamente\n\n"
                          f"📦 Productos cargados: {new_count}\n"
                          f"🔄 Datos sincronizados con la base de datos\n\n"
                          f"Todos los cambios realizados en otras ventanas\n"
                          f"están ahora visibles en la lista.")

            # Log détaillé
            self.logger.info(f"Productos actualizados: {new_count} productos cargados desde la base de datos")

        except Exception as e:
            self.logger.error(f"Error actualizando productos: {e}")
            self.show_error("Error de Actualización",
                           f"No se pudieron actualizar los productos:\n{str(e)}")

    def connect_event_signals(self):
        """Connecte aux signaux d'événements pour la synchronisation"""
        try:
            self.logger.debug("Connexion aux signaux d'événements...")
            # Écouter les modifications de stock
            event_manager.stock_updated.connect(self.on_stock_updated)
            event_manager.stock_adjusted.connect(self.on_stock_adjusted)
            self.logger.debug("✅ Signaux connectés avec succès")
        except Exception as e:
            self.logger.error(f"❌ Erreur connexion signaux: {e}")

    def on_stock_updated(self, product_id, new_stock):
        """Gère la mise à jour de stock d'un produit"""
        self.logger.debug(f"Stock mis à jour: produit {product_id}, nouveau stock {new_stock}")
        # Mettre à jour la colonne stock dans la table
        self.update_product_stock_in_table(product_id, new_stock)

        # Si le produit est actuellement sélectionné, mettre à jour le formulaire
        if self.selected_producto_id == product_id:
            self.stock_edit.setValue(new_stock)

    def on_stock_adjusted(self, product_id, old_stock, new_stock):
        """Gère l'ajustement de stock d'un produit"""
        self.logger.info(f"🔄 SIGNAL REÇU - Stock ajusté: produit {product_id}, {old_stock} -> {new_stock}")
        # Mettre à jour la colonne stock dans la table
        self.update_product_stock_in_table(product_id, new_stock)

        # Si le produit est actuellement sélectionné, mettre à jour le formulaire et afficher notification
        if self.selected_producto_id == product_id:
            self.stock_edit.setValue(new_stock)
            self.show_temporary_status(f"📦 Stock actualizado: {old_stock} → {new_stock}", 3000)

        # Afficher une notification dans les logs pour confirmer la réception
        self.logger.info(f"✅ Synchronisation terminée pour produit {product_id}")

    def update_product_stock_in_table(self, product_id, new_stock):
        """Met à jour le stock d'un produit dans la table"""
        try:
            # Trouver la ligne du produit dans la table
            for row in range(self.products_table.rowCount()):
                item = self.products_table.item(row, 0)  # Colonne ID
                if item and int(item.text()) == product_id:
                    # Mettre à jour la colonne Stock (colonne 4)
                    stock_item = QTableWidgetItem(str(int(new_stock)))
                    self.products_table.setItem(row, 4, stock_item)

                    # Mettre à jour aussi les données en mémoire
                    if row < len(self.productos):
                        self.productos[row]['stock_actual'] = new_stock
                    break
        except Exception as e:
            self.logger.error(f"Erreur mise à jour stock dans table: {e}")

    def show_temporary_status(self, message, duration=2000):
        """Affiche un message temporaire dans la barre de statut"""
        try:
            # Si la fenêtre parent a une barre de statut
            if hasattr(self.parent(), 'statusBar'):
                self.parent().statusBar().showMessage(message, duration)
            else:
                # Sinon, log le message
                self.logger.info(f"Status: {message}")
        except:
            self.logger.info(f"Status: {message}")

    def setup_form_connections(self):
        """Configure les connexions pour la synchronisation temps réel du formulaire"""
        # Connecter les changements de texte
        self.nombre_edit.textChanged.connect(self.on_form_data_changed)
        self.referencia_edit.textChanged.connect(self.on_form_data_changed)
        self.talla_edit.textChanged.connect(self.on_form_data_changed)

        # Connecter les changements de valeurs numériques
        self.precio_edit.valueChanged.connect(self.on_form_data_changed)
        self.stock_edit.valueChanged.connect(self.on_form_data_changed)

        # Connecter les changements de combo box
        self.categoria_combo.currentTextChanged.connect(self.on_form_data_changed)

    def on_form_data_changed(self):
        """Gère les changements dans le formulaire pour synchronisation temps réel"""
        # Debug: vérifier les conditions
        has_selected_id = bool(self.selected_producto_id)
        signals_blocked = self.nombre_edit.signalsBlocked()

        self.logger.debug(f"🔄 Changement formulaire - ID sélectionné: {has_selected_id}, Signaux bloqués: {signals_blocked}")

        if self.selected_producto_id and not self.nombre_edit.signalsBlocked():
            self.logger.debug("✅ Mise à jour de la table depuis le formulaire")
            # Mettre à jour la ligne correspondante dans la table
            self.update_table_row_from_form()
            self.set_data_modified(True)
        else:
            self.logger.debug(f"❌ Pas de mise à jour - ID: {self.selected_producto_id}, Bloqué: {signals_blocked}")

    def update_table_row_from_form(self):
        """Met à jour la ligne de la table avec les données du formulaire"""
        if not self.selected_producto_id:
            return

        try:
            # Trouver la ligne du produit dans la table
            for row in range(self.products_table.rowCount()):
                item = self.products_table.item(row, 0)  # Colonne ID
                if item and int(item.text()) == self.selected_producto_id:
                    # Mettre à jour les colonnes avec les données du formulaire
                    self.products_table.setItem(row, 1, QTableWidgetItem(self.nombre_edit.text()))
                    self.products_table.setItem(row, 2, QTableWidgetItem(self.referencia_edit.text()))
                    self.products_table.setItem(row, 3, QTableWidgetItem(f"{self.precio_edit.value():.2f}"))
                    self.products_table.setItem(row, 4, QTableWidgetItem(str(int(self.stock_edit.value()))))
                    self.products_table.setItem(row, 5, QTableWidgetItem(self.categoria_combo.currentText()))

                    # Mettre à jour aussi les données en mémoire
                    if row < len(self.productos):
                        self.productos[row]['nombre'] = self.nombre_edit.text()
                        self.productos[row]['referencia'] = self.referencia_edit.text() or None
                        self.productos[row]['precio_venta'] = self.precio_edit.value()
                        self.productos[row]['stock_actual'] = int(self.stock_edit.value())
                        self.productos[row]['categoria'] = self.categoria_combo.currentText() or None
                        self.productos[row]['talla'] = self.talla_edit.text() or None
                    break
        except Exception as e:
            self.logger.error(f"Erreur mise à jour ligne table: {e}")
