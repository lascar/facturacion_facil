"""
Widget personnalisé pour afficher les produits avec images dans les factures
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from utils.image_utils import ImageUtils
from common.validators import CalculationHelper
from utils.logger import get_logger

class ProductoListWidget(ctk.CTkScrollableFrame):
    """Widget personnalisé pour afficher une liste de produits avec images"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.logger = get_logger("producto_list_widget")
        
        # Variables
        self.items = []
        self.selected_index = None
        self.selection_callback = None
        
        # Configuration du style
        self.configure(fg_color=("gray95", "gray10"))
        
        # Header
        self.create_header()
        
        # Container pour les items
        self.items_frame = ctk.CTkFrame(self)
        self.items_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_header(self):
        """Crée l'en-tête avec les colonnes"""
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        # Colonnes de l'en-tête
        headers = [
            ("", 50),  # Image
            ("Producto", 180),
            ("Cantidad", 80),
            ("Precio Unit.", 100),
            ("IVA %", 80),
            ("Descuento %", 100),
            ("Total", 100)
        ]
        
        for i, (text, width) in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=text,
                font=ctk.CTkFont(weight="bold"),
                width=width
            )
            label.grid(row=0, column=i, padx=2, pady=5, sticky="ew")
        
        # Configurer les poids des colonnes
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=0)
    
    def add_item(self, factura_item):
        """Ajoute un item à la liste"""
        try:
            producto = factura_item.get_producto()
            if not producto:
                return
            
            # Frame pour cet item
            item_frame = ctk.CTkFrame(self.items_frame)
            item_frame.pack(fill="x", padx=2, pady=1)
            
            # Configurer le clic pour sélection
            item_index = len(self.items)
            item_frame.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Image du produit
            image_label = ctk.CTkLabel(item_frame, text="", width=50, height=40)
            image_label.grid(row=0, column=0, padx=2, pady=2)
            
            # Charger l'image
            mini_image = None
            if producto.imagen_path:
                mini_image = ImageUtils.create_mini_image(
                    producto.imagen_path, 
                    (40, 40)  # Taille légèrement plus grande pour meilleure visibilité
                )
            
            if mini_image:
                image_label.configure(image=mini_image, text="")
                image_label.image = mini_image  # Garder référence
            else:
                image_label.configure(text="📷", font=ctk.CTkFont(size=16))
            
            # Bind clic sur image aussi
            image_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Nom du produit
            producto_label = ctk.CTkLabel(
                item_frame,
                text=f"{producto.nombre}\n({producto.referencia})",
                width=180,
                anchor="w",
                justify="left"
            )
            producto_label.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
            producto_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Cantidad
            cantidad_label = ctk.CTkLabel(
                item_frame,
                text=str(factura_item.cantidad),
                width=80
            )
            cantidad_label.grid(row=0, column=2, padx=2, pady=2)
            cantidad_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Precio unitario
            precio_label = ctk.CTkLabel(
                item_frame,
                text=CalculationHelper.format_currency(factura_item.precio_unitario),
                width=100
            )
            precio_label.grid(row=0, column=3, padx=2, pady=2)
            precio_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # IVA
            iva_label = ctk.CTkLabel(
                item_frame,
                text=CalculationHelper.format_percentage(factura_item.iva_aplicado),
                width=80
            )
            iva_label.grid(row=0, column=4, padx=2, pady=2)
            iva_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Descuento
            descuento_label = ctk.CTkLabel(
                item_frame,
                text=CalculationHelper.format_percentage(factura_item.descuento),
                width=100
            )
            descuento_label.grid(row=0, column=5, padx=2, pady=2)
            descuento_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Total
            total_label = ctk.CTkLabel(
                item_frame,
                text=CalculationHelper.format_currency(factura_item.total),
                width=100,
                font=ctk.CTkFont(weight="bold")
            )
            total_label.grid(row=0, column=6, padx=2, pady=2)
            total_label.bind("<Button-1>", lambda e, idx=item_index: self.select_item(idx))
            
            # Configurer les poids des colonnes
            for i in range(7):
                item_frame.grid_columnconfigure(i, weight=0)
            
            # Stocker les références
            item_data = {
                'frame': item_frame,
                'factura_item': factura_item,
                'labels': [image_label, producto_label, cantidad_label, precio_label, iva_label, descuento_label, total_label]
            }
            self.items.append(item_data)
            
            self.logger.debug(f"Item ajouté: {producto.nombre}")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout d'item: {e}")
    
    def clear_items(self):
        """Supprime tous les items"""
        try:
            for item_data in self.items:
                item_data['frame'].destroy()
            self.items.clear()
            self.selected_index = None
            self.logger.debug("Tous les items supprimés")
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression des items: {e}")
    
    def select_item(self, index):
        """Sélectionne un item"""
        try:
            if 0 <= index < len(self.items):
                # Désélectionner l'item précédent
                if self.selected_index is not None and self.selected_index < len(self.items):
                    self.items[self.selected_index]['frame'].configure(fg_color=("gray90", "gray20"))
                
                # Sélectionner le nouveau item
                self.selected_index = index
                self.items[index]['frame'].configure(fg_color=("lightblue", "darkblue"))
                
                # Appeler le callback si défini
                if self.selection_callback:
                    self.selection_callback(index)
                
                self.logger.debug(f"Item sélectionné: {index}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection: {e}")
    
    def get_selected_item(self):
        """Retourne l'item sélectionné"""
        if self.selected_index is not None and self.selected_index < len(self.items):
            return self.items[self.selected_index]['factura_item']
        return None
    
    def get_selected_index(self):
        """Retourne l'index de l'item sélectionné"""
        return self.selected_index
    
    def set_selection_callback(self, callback):
        """Définit le callback appelé lors de la sélection"""
        self.selection_callback = callback
    
    def update_items(self, factura_items):
        """Met à jour la liste avec de nouveaux items"""
        try:
            self.clear_items()
            for item in factura_items:
                self.add_item(item)
            self.logger.debug(f"Liste mise à jour avec {len(factura_items)} items")
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour: {e}")
