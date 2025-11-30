# -*- coding: utf-8 -*-
"""
Fenêtre de gestion du stock - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QSpinBox, QGroupBox, QSplitter, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from utils.logger import get_logger
from utils.event_manager import event_manager

class StockPyQt6Window(BasePyQt6Window):
    """Fenêtre de gestion du stock en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Stock", 1000, 700)
        self.logger = get_logger("stock_pyqt6")

        # Connecter aux signaux d'événements
        self.connect_event_signals()

        self.logger.info("Inicializando ventana de gestión de stock PyQt6")

    def connect_event_signals(self):
        """Connecte aux signaux d'événements pour la synchronisation"""
        # Écouter les modifications de produits
        event_manager.product_created.connect(self.on_product_created)
        event_manager.product_updated.connect(self.on_product_updated)
        event_manager.product_deleted.connect(self.on_product_deleted)

        # Écouter les modifications de factures (qui peuvent affecter le stock)
        event_manager.invoice_created.connect(self.on_invoice_created)

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title_label = QLabel("Gestión de Stock")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Barre de recherche et filtres
        self.create_search_panel()
        
        # Table de stock
        self.create_stock_table()
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_stock_data()
    
    def create_search_panel(self):
        """Crée le panneau de recherche et filtres"""
        search_group = QGroupBox("Filtros y Búsqueda")
        search_layout = QGridLayout(search_group)
        
        # Recherche par nom/référence
        search_layout.addWidget(QLabel("Buscar:"), 0, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar por referencia o nombre...")
        self.search_edit.textChanged.connect(self.filter_stock)
        search_layout.addWidget(self.search_edit, 0, 1, 1, 2)
        
        # Filtre par catégorie
        search_layout.addWidget(QLabel("Categoría:"), 1, 0)
        self.category_filter = QComboBox()
        self.category_filter.addItem("Todas las categorías", "")
        self.load_categories()
        self.category_filter.currentTextChanged.connect(self.filter_stock)
        search_layout.addWidget(self.category_filter, 1, 1)
        
        # Filtre par stock bas
        self.low_stock_check = QPushButton("Solo Stock Bajo")
        self.low_stock_check.setCheckable(True)
        self.low_stock_check.toggled.connect(self.filter_stock)
        search_layout.addWidget(self.low_stock_check, 1, 2)
        
        self.main_layout.addWidget(search_group)
    
    def create_stock_table(self):
        """Crée la table de stock"""
        # Groupe pour la table
        table_group = QGroupBox("Inventario de Stock")
        table_layout = QVBoxLayout(table_group)
        
        # Table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(8)
        self.stock_table.setHorizontalHeaderLabels([
            "Referencia", "Nombre", "Categoría", "Stock Actual", "Acciones", "Stock Mínimo", "Estado", "ID"
        ])
        
        # Configuration de la table
        header = self.stock_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Referencia
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Nombre
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Categoría
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Stock Actual
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Acciones (+/-)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Stock Mínimo
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Estado
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # ID (caché)
        
        self.stock_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stock_table.setAlternatingRowColors(True)

        # Cacher la colonne ID
        self.stock_table.setColumnHidden(7, True)

        table_layout.addWidget(self.stock_table)
        self.main_layout.addWidget(table_group)
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("🔄 Actualizar", self.refresh_stock_data, "primary"),
            ("📝 Editar Stock", self.update_stock, "secondary"),
            ("📊 Ver Historial", self.view_history, "secondary"),
            ("💾 Exportar", self.export_stock, "secondary"),
            ("❌ Cerrar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def load_categories(self):
        """Charge les catégories pour le filtre"""
        try:
            categories = db.get_product_categories()
            for category in categories:
                self.category_filter.addItem(category, category)
        except Exception as e:
            self.logger.error(f"Error cargando categorías: {e}")
    
    def load_stock_data(self):
        """Charge les données de stock"""
        try:
            # Obtenir les produits avec informations de stock
            products = db.get_all_products()

            self.stock_table.setRowCount(len(products))

            for row, product in enumerate(products):
                # Référence
                self.stock_table.setItem(row, 0, QTableWidgetItem(str(product.get('referencia', ''))))

                # Nom
                self.stock_table.setItem(row, 1, QTableWidgetItem(str(product.get('nombre', ''))))

                # Catégorie
                self.stock_table.setItem(row, 2, QTableWidgetItem(str(product.get('categoria', ''))))

                # Stock actuel
                current_stock = product.get('stock_actual', 0)
                stock_item = QTableWidgetItem(str(current_stock))
                stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stock_table.setItem(row, 3, stock_item)

                # Boutons d'action (+/-)
                self.create_stock_buttons(row, product.get('id'))

                # Stock minimum
                min_stock = product.get('stock_minimo', 5)
                min_item = QTableWidgetItem(str(min_stock))
                min_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stock_table.setItem(row, 5, min_item)
                
                # État
                if current_stock <= min_stock:
                    status = "⚠️ BAJO"
                    status_color = QColor("#dc3545")
                elif current_stock <= min_stock * 2:
                    status = "⚡ MEDIO"
                    status_color = QColor("#ffc107")
                else:
                    status = "✅ OK"
                    status_color = QColor("#28a745")

                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                status_item.setForeground(status_color)
                self.stock_table.setItem(row, 6, status_item)  # Colonne 6 pour État

                # ID du produit (colonne cachée)
                id_item = QTableWidgetItem(str(product.get('id', '')))
                self.stock_table.setItem(row, 7, id_item)
            
            self.logger.info(f"Cargados {len(products)} productos en stock")

        except Exception as e:
            self.logger.error(f"Error cargando datos de stock: {e}")
            self.show_error("Error", f"Error al cargar datos de stock: {e}")

    def create_stock_buttons(self, row, product_id):
        """Crée les boutons +/- pour ajuster le stock"""
        # Widget conteneur pour les boutons
        buttons_widget = QFrame()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(2, 2, 2, 2)
        buttons_layout.setSpacing(2)

        # Bouton - (diminuer stock)
        minus_btn = QPushButton("-")  # Caractère minus simple
        minus_btn.setFixedSize(30, 30)  # Boutons plus grands
        minus_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 20px;
                font-family: 'Arial Black', 'Arial', 'Helvetica', sans-serif;
                text-align: center;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #a71e2a;
            }
        """)
        minus_btn.setToolTip("Diminuer le stock de 1")
        minus_btn.clicked.connect(lambda: self.adjust_stock(product_id, -1))

        # Bouton + (augmenter stock)
        plus_btn = QPushButton("+")  # Caractère plus simple
        plus_btn.setFixedSize(30, 30)  # Boutons plus grands
        plus_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 20px;
                font-family: 'Arial Black', 'Arial', 'Helvetica', sans-serif;
                text-align: center;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        plus_btn.setToolTip("Augmenter le stock de 1")
        plus_btn.clicked.connect(lambda: self.adjust_stock(product_id, +1))

        # Ajouter les boutons au layout
        buttons_layout.addWidget(minus_btn)
        buttons_layout.addWidget(plus_btn)

        # Ajouter le widget à la table
        self.stock_table.setCellWidget(row, 4, buttons_widget)

    def adjust_stock(self, product_id, adjustment):
        """Ajuste le stock d'un produit de manière fluide"""
        try:
            # Obtenir l'ancien stock pour le signal
            old_stock = self.get_current_stock_from_table(product_id)

            # Ajuster le stock en base de données
            new_stock = db.adjust_product_stock(product_id, adjustment)

            if new_stock is not False:
                # Mettre à jour seulement la ligne concernée (plus rapide)
                self.update_single_product_row(product_id, new_stock)

                # Émettre un signal pour notifier les autres fenêtres
                event_manager.emit_stock_adjusted(product_id, old_stock, new_stock)

                # Indicateur visuel temporaire dans la barre de statut
                action_symbol = "📈" if adjustment > 0 else "📉"
                action_text = "aumentado" if adjustment > 0 else "reducido"
                self.show_temporary_status(f"{action_symbol} Stock {action_text}: {new_stock}")

                # Log silencieux pour traçabilité
                self.logger.info(f"Stock {action_text}: producto {product_id}, nuevo stock: {new_stock}")
            else:
                # Erreur silencieuse dans les logs, pas de popup
                self.logger.error(f"No se pudo ajustar el stock del producto {product_id}")

        except Exception as e:
            self.logger.error(f"Error ajustando stock: {e}")
            # Seulement afficher l'erreur si c'est critique
            if "database" in str(e).lower():
                self.show_error("Error de Base de Datos", "Error al conectar con la base de datos")

    def get_current_stock_from_table(self, product_id):
        """Obtient le stock actuel d'un produit depuis la table"""
        try:
            for row in range(self.stock_table.rowCount()):
                id_item = self.stock_table.item(row, 7)  # Colonne ID cachée
                if id_item and int(id_item.text()) == product_id:
                    stock_item = self.stock_table.item(row, 3)  # Colonne stock actuel
                    if stock_item:
                        return int(stock_item.text())
            return 0
        except Exception as e:
            self.logger.error(f"Error obteniendo stock actual: {e}")
            return 0

    def update_single_product_row(self, product_id, new_stock):
        """Met à jour une seule ligne de produit dans la table"""
        try:
            # Chercher la ligne correspondant au produit
            for row in range(self.stock_table.rowCount()):
                id_item = self.stock_table.item(row, 7)  # Colonne ID cachée
                if id_item and int(id_item.text()) == product_id:
                    # Mettre à jour le stock actuel (colonne 3)
                    stock_item = self.stock_table.item(row, 3)
                    if stock_item:
                        stock_item.setText(str(new_stock))

                    # Mettre à jour l'état (colonne 6)
                    status_item = self.stock_table.item(row, 6)
                    min_item = self.stock_table.item(row, 5)

                    if status_item and min_item:
                        min_stock = int(min_item.text())

                        # Calculer le nouvel état
                        if new_stock <= min_stock:
                            status = "⚠️ BAJO"
                            status_color = QColor("#dc3545")
                        elif new_stock <= min_stock * 2:
                            status = "⚡ MEDIO"
                            status_color = QColor("#ffc107")
                        else:
                            status = "✅ OK"
                            status_color = QColor("#28a745")

                        status_item.setText(status)
                        status_item.setForeground(status_color)

                    break

        except Exception as e:
            self.logger.error(f"Error actualizando fila de producto {product_id}: {e}")

    def show_temporary_status(self, message, duration=2000):
        """Affiche un message temporaire dans la barre de statut"""
        try:
            # Créer une barre de statut si elle n'existe pas
            if not hasattr(self, 'status_bar'):
                self.status_bar = self.statusBar()

            # Afficher le message temporairement
            self.status_bar.showMessage(message, duration)

        except Exception as e:
            # Si pas de barre de statut, afficher dans les logs
            self.logger.info(f"Status: {message}")

    def refresh_stock_data(self):
        """Rafraîchit tous les stocks depuis la base de données"""
        try:
            # Compter les produits avant rafraîchissement
            old_count = self.stock_table.rowCount()

            # Recharger toutes les données depuis la base de données
            self.load_stock_data()

            # Compter les produits après rafraîchissement
            new_count = self.stock_table.rowCount()

            # Message de confirmation détaillé
            message = f"🔄 {new_count} produits actualisés depuis la base de données"
            self.show_temporary_status(message, 4000)

            # Log détaillé
            self.logger.info(f"Stocks rafraîchis: {new_count} produits chargés depuis la base de données")

            # Afficher une notification plus visible
            self.show_info("Actualización Completa",
                          f"✅ Stocks actualizados correctamente\n\n"
                          f"📦 Productos cargados: {new_count}\n"
                          f"🔄 Datos sincronizados con la base de datos\n\n"
                          f"Todos los cambios de stock por facturas\n"
                          f"están ahora visibles en la tabla.")

        except Exception as e:
            self.logger.error(f"Error rafraîchissant les stocks: {e}")
            self.show_temporary_status("❌ Error al actualizar stocks", 3000)
            self.show_error("Error de Actualización",
                           f"No se pudieron actualizar los stocks:\n{str(e)}")
    
    def filter_stock(self):
        """Filtre les données de stock"""
        search_text = self.search_edit.text().lower()
        category_filter = self.category_filter.currentData()
        low_stock_only = self.low_stock_check.isChecked()
        
        for row in range(self.stock_table.rowCount()):
            show_row = True
            
            # Filtre par texte de recherche
            if search_text:
                ref_item = self.stock_table.item(row, 0)
                name_item = self.stock_table.item(row, 1)
                
                if not ((ref_item and search_text in ref_item.text().lower()) or
                        (name_item and search_text in name_item.text().lower())):
                    show_row = False
            
            # Filtre par catégorie
            if show_row and category_filter:
                cat_item = self.stock_table.item(row, 2)
                if not (cat_item and cat_item.text() == category_filter):
                    show_row = False
            
            # Filtre stock bas
            if show_row and low_stock_only:
                status_item = self.stock_table.item(row, 5)
                if not (status_item and "BAJO" in status_item.text()):
                    show_row = False
            
            self.stock_table.setRowHidden(row, not show_row)
    
    def update_stock(self):
        """Édite manuellement le stock du produit sélectionné"""
        current_row = self.stock_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Selecciona un producto para editar su stock manualmente")
            return

        # Pour la démo, on affiche juste un message
        # Récupérer l'ID du produit
        id_item = self.stock_table.item(current_row, 7)  # Colonne ID cachée
        if not id_item:
            self.show_error("Error", "No se pudo obtener el ID del producto")
            return

        product_id = int(id_item.text())

        # Récupérer les informations actuelles
        ref_item = self.stock_table.item(current_row, 0)
        name_item = self.stock_table.item(current_row, 1)
        stock_item = self.stock_table.item(current_row, 3)

        product_ref = ref_item.text() if ref_item else "N/A"
        product_name = name_item.text() if name_item else "N/A"
        current_stock = int(stock_item.text()) if stock_item else 0

        # Demander le nouveau stock
        from PyQt6.QtWidgets import QInputDialog

        new_stock, ok = QInputDialog.getInt(
            self,
            "Actualizar Stock",
            f"Producto: {product_name} ({product_ref})\n"
            f"Stock actual: {current_stock}\n\n"
            f"Nuevo stock:",
            current_stock,  # Valeur par défaut
            0,  # Minimum
            9999  # Maximum
        )

        if ok and new_stock != current_stock:
            try:
                # Mettre à jour le stock
                success = db.update_product_stock(product_id, new_stock)
                if success:
                    # Mettre à jour l'affichage
                    self.update_single_product_row(product_id, new_stock)

                    # Message de confirmation
                    self.show_temporary_status(f"📊 Stock actualizado: {product_name} → {new_stock}")
                    self.logger.info(f"Stock actualizado manualmente: {product_name} ({current_stock} → {new_stock})")
                else:
                    self.show_error("Error", "No se pudo actualizar el stock")
            except Exception as e:
                self.logger.error(f"Error actualizando stock manualmente: {e}")
                self.show_error("Error", f"Error al actualizar stock:\n{str(e)}")
    
    def view_history(self):
        """Affiche l'historique du produit sélectionné"""
        current_row = self.stock_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Selecciona un producto para ver su historial")
            return
        
        # Récupérer les informations du produit
        ref_item = self.stock_table.item(current_row, 0)
        name_item = self.stock_table.item(current_row, 1)
        stock_item = self.stock_table.item(current_row, 3)

        product_ref = ref_item.text() if ref_item else "N/A"
        product_name = name_item.text() if name_item else "N/A"
        current_stock = stock_item.text() if stock_item else "0"

        # Afficher un historique informatif
        history_text = f"""HISTORIAL DE STOCK - {product_name} ({product_ref})

Stock Actual: {current_stock} unidades

📊 MOVIMIENTOS AUTOMÁTICOS:
• Las ventas reducen el stock automáticamente
• Los ajustes manuales (+/-) se registran
• Cada factura actualiza el inventario

💡 INFORMACIÓN:
• Stock mínimo recomendado: 5 unidades
• Estado actual: {"✅ OK" if int(current_stock) > 5 else "⚠️ BAJO" if int(current_stock) > 0 else "❌ AGOTADO"}

🔍 Historial detallado disponible en logs/facturacion_facil.log"""

        self.show_info("Historial de Stock", history_text)
    
    def export_stock(self):
        """Exporte les données de stock vers un fichier CSV"""
        try:
            from PyQt6.QtWidgets import QFileDialog
            import csv
            from datetime import datetime

            # Demander où sauvegarder le fichier
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Stock",
                f"stock_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV files (*.csv);;All files (*.*)"
            )

            if filename:
                # Récupérer les données de stock
                products = db.get_all_products()

                # Écrire le fichier CSV
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # En-têtes
                    writer.writerow([
                        'Referencia', 'Nombre', 'Categoria', 'Stock_Actual',
                        'Stock_Minimo', 'Precio', 'Estado', 'Fecha_Export'
                    ])

                    # Données
                    export_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for product in products:
                        stock_actual = product.get('stock_actual', 0)
                        stock_minimo = product.get('stock_minimo', 5)

                        # Déterminer l'état
                        if stock_actual <= 0:
                            estado = "AGOTADO"
                        elif stock_actual <= stock_minimo:
                            estado = "BAJO"
                        elif stock_actual <= stock_minimo * 2:
                            estado = "MEDIO"
                        else:
                            estado = "OK"

                        writer.writerow([
                            product.get('referencia', ''),
                            product.get('nombre', ''),
                            product.get('categoria', ''),
                            stock_actual,
                            stock_minimo,
                            product.get('precio', 0),
                            estado,
                            export_date
                        ])

                self.show_info("Exportación Exitosa",
                              f"Stock exportado correctamente a:\n{filename}\n\n"
                              f"Productos exportados: {len(products)}")

                self.logger.info(f"Stock exportado a: {filename} ({len(products)} productos)")

        except Exception as e:
            self.logger.error(f"Error exportando stock: {e}")
            self.show_error("Error de Exportación", f"No se pudo exportar el stock:\n{str(e)}")

    # Méthodes de gestion des événements
    def on_product_created(self, product_data):
        """Gère la création d'un nouveau produit"""
        self.logger.debug(f"Nouveau produit créé: {product_data.get('nombre', 'N/A')}")
        # Recharger les données pour inclure le nouveau produit
        self.load_stock_data()

    def on_product_updated(self, product_data):
        """Gère la modification d'un produit"""
        self.logger.debug(f"Produit modifié: {product_data.get('nombre', 'N/A')}")
        # Recharger les données pour refléter les modifications
        self.load_stock_data()

    def on_product_deleted(self, product_id):
        """Gère la suppression d'un produit"""
        self.logger.debug(f"Produit supprimé: {product_id}")
        # Recharger les données pour supprimer le produit de la liste
        self.load_stock_data()

    def on_invoice_created(self, invoice_data):
        """Gère la création d'une facture (peut affecter le stock)"""
        self.logger.debug(f"Facture créée: {invoice_data.get('numero', 'N/A')}")
        # Recharger les données car les stocks peuvent avoir changé
        self.load_stock_data()
