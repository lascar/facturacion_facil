# -*- coding: utf-8 -*-
"""
Widget d'autocomplétion pour les produits (lecture seule, pas de création)
"""

from PyQt5.QtWidgets import QLineEdit, QCompleter
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal as Signal, QTimer
from PyQt5.QtGui import QFont

from utils.logger import get_logger
from database.database import db

class ProductAutoCompleteWidget(QLineEdit):
    """Widget d'autocomplétion pour les produits (lecture seule)"""
    
    # Signal émis quand un produit est sélectionné
    product_selected = Signal(dict)  # Produit sélectionné
    product_changed = Signal()       # Produit changé (pour mise à jour UI)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        
        # Variables
        self.products_data = []
        self.current_product = None
        self.filtered_products = []
        
        # Configuration de base
        self.setPlaceholderText("Escriba el nombre del producto...")
        self.setup_completer()
        self.setup_connections()
        self.apply_style()
        
        # Timer pour éviter trop de requêtes
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
    
    def setup_completer(self):
        """Configure l'autocomplétion"""
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setMaxVisibleItems(10)
        
        # Modèle pour les suggestions
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.setCompleter(self.completer)
    
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Connexion pour la sélection depuis le completer
        self.completer.activated.connect(self.on_completion_selected)
        
        # Connexion pour la recherche en temps réel
        self.textChanged.connect(self.on_text_changed)
        
        # Connexion pour la validation quand on quitte le champ
        self.editingFinished.connect(self.on_editing_finished)
    
    def apply_style(self):
        """Applique le style au widget"""
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
                background-color: #f9f9f9;
            }
            QLineEdit:hover {
                border-color: #999;
            }
        """)
    
    def load_products(self, products):
        """Charge la liste des produits"""
        try:
            self.products_data = products or []
            self.update_completer_model()
            self.logger.info(f"Cargados {len(self.products_data)} productos en autocomplétion")
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            self.products_data = []
    
    def update_completer_model(self, filter_text=""):
        """Met à jour le modèle du completer avec filtrage"""
        try:
            if not filter_text:
                # Afficher tous les produits avec stock > 0 OU sin_stock=1
                self.filtered_products = [
                    p for p in self.products_data
                    if p.get('stock_actual', 0) > 0 or p.get('sin_stock', 0) == 1
                ]
            else:
                # Filtrer par nom et (stock > 0 OU sin_stock=1)
                filter_lower = filter_text.lower()
                self.filtered_products = [
                    p for p in self.products_data
                    if filter_lower in p.get('nombre', '').lower()
                    and (p.get('stock_actual', 0) > 0 or p.get('sin_stock', 0) == 1)
                ]

            # Créer les suggestions avec format: "Nom - Talla - Prix€ (Stock: X)" ou "Nom - Talla - Prix€ (Sin stock)"
            suggestions = []
            for product in self.filtered_products:
                stock = product.get('stock_actual', 0)
                sin_stock = product.get('sin_stock', 0)
                precio = product.get('precio_venta', 0.0)
                nombre = product['nombre']
                talla = product.get('talla', '')

                # Ajouter la taille si elle existe
                if talla and talla.strip():
                    nombre = f"{nombre} - {talla}"

                # Afficher "Sin stock" au lieu du stock si le produit est marqué sin_stock
                if sin_stock:
                    suggestion = f"{nombre} - {precio:.2f}€ (Sin stock)"
                else:
                    suggestion = f"{nombre} - {precio:.2f}€ (Stock: {stock})"
                suggestions.append(suggestion)

            self.model.setStringList(suggestions)
            
        except Exception as e:
            self.logger.error(f"Error actualizando modelo completer: {e}")
            self.model.setStringList([])
    
    def on_text_changed(self, text):
        """Gestiona les changements de texte"""
        # Arrêter le timer précédent
        self.search_timer.stop()
        
        # Réinitialiser le produit actuel si le texte change
        if self.current_product and text != self.format_product_display(self.current_product):
            self.current_product = None
            self.product_changed.emit()
        
        # Démarrer le timer pour la recherche
        if text.strip():
            self.search_timer.start(300)  # 300ms de délai
        else:
            self.update_completer_model()
    
    def perform_search(self):
        """Effectue la recherche avec le texte actuel"""
        text = self.text().strip()
        self.update_completer_model(text)
    
    def on_completion_selected(self, text):
        """Gestiona la sélection depuis l'autocomplétion"""
        try:
            # Trouver le produit correspondant au texte sélectionné
            for product in self.filtered_products:
                expected_text = self.format_product_display(product)
                if text == expected_text:
                    self.set_product(product)
                    break
        except Exception as e:
            self.logger.error(f"Error en selección de autocomplétion: {e}")
    
    def on_editing_finished(self):
        """Gestiona la fin d'édition"""
        text = self.text().strip()

        if not text:
            self.clear_product()
            return

        # Vérifier si le texte correspond exactement à un produit
        matching_product = None
        for product in self.products_data:
            if text.lower() == product.get('nombre', '').lower():
                # Accepter les produits avec stock > 0 OU sin_stock=1
                if product.get('stock_actual', 0) > 0 or product.get('sin_stock', 0) == 1:
                    matching_product = product
                    break

        if matching_product:
            self.set_product(matching_product)
        elif self.current_product is None:
            # Aucun produit trouvé, effacer le champ
            self.clear()
    
    def format_product_display(self, product):
        """Formate l'affichage d'un produit"""
        if not product:
            return ""

        stock = product.get('stock_actual', 0)
        sin_stock = product.get('sin_stock', 0)
        precio = product.get('precio_venta', 0.0)
        nombre = product['nombre']
        talla = product.get('talla', '')

        # Ajouter la taille si elle existe
        if talla and talla.strip():
            nombre = f"{nombre} - {talla}"

        # Afficher "Sin stock" au lieu du stock si le produit est marqué sin_stock
        if sin_stock:
            return f"{nombre} - {precio:.2f}€ (Sin stock)"
        else:
            return f"{nombre} - {precio:.2f}€ (Stock: {stock})"
    
    def set_product(self, product):
        """Définit le produit actuel"""
        try:
            self.current_product = product
            display_text = self.format_product_display(product)
            
            # Bloquer temporairement les signaux pour éviter la récursion
            self.blockSignals(True)
            self.setText(display_text)
            self.blockSignals(False)
            
            # Émettre le signal
            self.product_selected.emit(product)
            self.product_changed.emit()
            
            self.logger.info(f"Producto seleccionado: {product.get('nombre', '')}")
            
        except Exception as e:
            self.logger.error(f"Error estableciendo producto: {e}")
    
    def get_current_product(self):
        """Retourne le produit actuellement sélectionné"""
        return self.current_product
    
    def clear_product(self):
        """Efface le produit actuel"""
        self.current_product = None
        self.clear()
        self.product_changed.emit()
    
    def has_valid_product(self):
        """Vérifie si un produit valide est sélectionné"""
        return self.current_product is not None and self.current_product.get('stock_actual', 0) > 0
