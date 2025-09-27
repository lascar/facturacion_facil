#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de stock optimisée pour de meilleures performances
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from database.optimized_models import OptimizedStock, BatchOperations
from utils.performance_optimizer import performance_monitor, performance_optimizer
from utils.translations import get_text
from utils.logger import get_logger
from common.ui_components import BaseWindow
import time


class OptimizedStockWindow(BaseWindow):
    """Fenêtre de stock optimisée avec virtualisation et cache"""
    
    def __init__(self, parent):
        super().__init__(parent, get_text("gestion_stock"), "1200x800")
        
        # Variables de performance
        self.stock_data = []
        self.filtered_data = []
        self.displayed_items = {}  # Cache des widgets affichés
        self.visible_range = (0, 50)  # Plage visible (virtualisation)
        self.item_height = 60
        self.search_var = tk.StringVar()
        self.last_search_time = 0
        self.search_delay = 300  # ms
        
        # Variables de tri
        self.sort_column = "nombre"
        self.sort_reverse = False
        
        self.create_optimized_widgets()
        self.load_stock_data_optimized()
        
        self.logger.info("Ventana de stock optimizada inicializada")
    
    def create_optimized_widgets(self):
        """Créer l'interface optimisée"""
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame de contrôles optimisé
        self.create_optimized_controls(main_frame)
        
        # Frame de la table avec virtualisation
        self.create_virtualized_table(main_frame)
        
        # Statistiques en temps réel
        self.create_stats_panel(main_frame)
    
    def create_optimized_controls(self, parent):
        """Créer les contrôles optimisés"""
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Frame de recherche avec debouncing
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(side="left", fill="x", expand=True, padx=(10, 20), pady=20)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍 Búsqueda rápida:")
        search_label.pack(side="left", padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Nombre o referencia...",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)
        
        # Búsqueda con debouncing (evita búsquedas excesivas)
        self.search_var.trace_add("write", self.on_search_change)
        
        # Botón de limpieza
        clear_btn = ctk.CTkButton(
            search_frame,
            text="✖",
            command=self.clear_search,
            width=30
        )
        clear_btn.pack(side="left", padx=5)
        
        # Indicador de resultados
        self.results_label = ctk.CTkLabel(
            search_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.results_label.pack(side="left", padx=(10, 0))
        
        # Botones de acción optimizados
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=(10, 20), pady=20)
        
        refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualizar",
            command=self.refresh_data,
            width=120
        )
        refresh_btn.pack(side="left", padx=5)
        
        low_stock_btn = ctk.CTkButton(
            buttons_frame,
            text="⚠️ Stock Bajo",
            command=self.show_low_stock_optimized,
            width=120,
            fg_color="orange",
            hover_color="darkorange"
        )
        low_stock_btn.pack(side="left", padx=5)
        
        # Botón de optimización
        optimize_btn = ctk.CTkButton(
            buttons_frame,
            text="⚡ Optimizar",
            command=self.optimize_performance,
            width=120,
            fg_color="purple",
            hover_color="darkviolet"
        )
        optimize_btn.pack(side="left", padx=5)
    
    def create_virtualized_table(self, parent):
        """Créer une table virtualisée pour de meilleures performances"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # En-têtes avec tri
        headers_frame = ctk.CTkFrame(table_frame)
        headers_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        headers = [
            ("nombre", "Producto", 0.3),
            ("referencia", "Referencia", 0.15),
            ("cantidad", "Stock", 0.1),
            ("precio", "Precio", 0.15),
            ("categoria", "Categoría", 0.15),
            ("fecha_actualizacion", "Actualizado", 0.15)
        ]
        
        self.header_buttons = {}
        for col_key, col_name, width_ratio in headers:
            btn = ctk.CTkButton(
                headers_frame,
                text=f"{col_name} ↕",
                command=lambda k=col_key: self.sort_by_column(k),
                height=30,
                fg_color="gray30",
                hover_color="gray40"
            )
            btn.pack(side="left", fill="x", expand=True, padx=2)
            self.header_buttons[col_key] = btn
        
        # Frame scrollable optimisé
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_frame,
            height=400
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind pour le scroll virtualisé
        self.scrollable_frame.bind("<Configure>", self.on_scroll_configure)
        self.scrollable_frame.bind("<MouseWheel>", self.on_mouse_wheel)
    
    def create_stats_panel(self, parent):
        """Créer un panneau de statistiques en temps réel"""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Cargando estadísticas...",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack(pady=10)
    
    @performance_monitor.time_function("load_stock_data_optimized")
    def load_stock_data_optimized(self):
        """Charger les données de stock de manière optimisée"""
        try:
            # Utiliser la requête optimisée
            self.stock_data = OptimizedStock.get_all_optimized()
            self.filtered_data = self.stock_data.copy()
            
            # Mettre à jour l'affichage
            self.update_display_optimized()
            self.update_stats()
            
            self.logger.info(f"Stock cargado optimizado: {len(self.stock_data)} productos")
            
        except Exception as e:
            self.logger.error(f"Error cargando stock optimizado: {e}")
            self.show_error_message("Error", f"Error cargando datos: {e}")
    
    def update_display_optimized(self):
        """Mettre à jour l'affichage de manière optimisée (virtualisation)"""
        try:
            # Nettoyer seulement si nécessaire
            if not hasattr(self, '_last_data_hash') or self._last_data_hash != hash(str(self.filtered_data)):
                self.clear_display()
                self._last_data_hash = hash(str(self.filtered_data))
            
            if not self.filtered_data:
                self.show_no_data_message()
                return
            
            # Afficher seulement les éléments visibles (virtualisation)
            start_idx, end_idx = self.visible_range
            end_idx = min(end_idx, len(self.filtered_data))
            
            for i in range(start_idx, end_idx):
                if i not in self.displayed_items:
                    item = self.filtered_data[i]
                    widget = self.create_optimized_stock_row(item, i)
                    self.displayed_items[i] = widget
            
            # Supprimer les éléments non visibles
            for idx in list(self.displayed_items.keys()):
                if idx < start_idx or idx >= end_idx:
                    widget = self.displayed_items.pop(idx)
                    widget.destroy()
            
            self.update_results_indicator()
            
        except Exception as e:
            self.logger.error(f"Error actualizando display optimizado: {e}")
    
    def create_optimized_stock_row(self, item, index):
        """Créer une ligne de stock optimisée"""
        # Frame principal avec couleur alternée
        bg_color = "gray20" if index % 2 == 0 else "gray25"
        row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color)
        row_frame.pack(fill="x", padx=2, pady=1)
        
        # Conteneur pour les colonnes
        content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=5)
        
        # Colonnes avec largeurs fixes
        columns = [
            (item['nombre'], 0.3),
            (item['referencia'], 0.15),
            (f"{item['cantidad']}", 0.1),
            (f"€{item['precio']:.2f}", 0.15),
            (item['categoria'], 0.15),
            (str(item['fecha_actualizacion'])[:10], 0.15)
        ]
        
        for i, (text, width_ratio) in enumerate(columns):
            # Couleur spéciale pour stock bas
            text_color = "red" if i == 2 and item['cantidad'] <= 5 else "white"
            
            label = ctk.CTkLabel(
                content_frame,
                text=str(text)[:20] + "..." if len(str(text)) > 20 else str(text),
                text_color=text_color,
                font=ctk.CTkFont(size=11)
            )
            label.pack(side="left", fill="x", expand=True, padx=2)
        
        # Boutons d'action (seulement si nécessaire)
        if item['cantidad'] <= 5:
            action_btn = ctk.CTkButton(
                content_frame,
                text="+ Stock",
                command=lambda: self.quick_add_stock(item),
                width=80,
                height=25,
                fg_color="green",
                hover_color="darkgreen"
            )
            action_btn.pack(side="right", padx=5)
        
        return row_frame
    
    def on_search_change(self, *args):
        """Gérer les changements de recherche avec debouncing"""
        current_time = time.time() * 1000  # en millisecondes
        self.last_search_time = current_time
        
        # Programmer la recherche avec délai
        self.window.after(self.search_delay, lambda: self.delayed_search(current_time))
    
    def delayed_search(self, search_time):
        """Exécuter la recherche avec délai (debouncing)"""
        if search_time == self.last_search_time:  # Seulement si c'est la dernière recherche
            self.perform_search_optimized()
    
    @performance_monitor.time_function("perform_search_optimized")
    def perform_search_optimized(self):
        """Effectuer une recherche optimisée"""
        try:
            search_text = self.search_var.get().lower().strip()
            
            if not search_text:
                self.filtered_data = self.stock_data.copy()
            else:
                # Recherche optimisée avec compréhension de liste
                self.filtered_data = [
                    item for item in self.stock_data
                    if (search_text in item.get('nombre', '').lower() or
                        search_text in item.get('referencia', '').lower() or
                        search_text in item.get('categoria', '').lower())
                ]
            
            # Réinitialiser la plage visible
            self.visible_range = (0, min(50, len(self.filtered_data)))
            
            self.update_display_optimized()
            self.update_stats()
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda optimizada: {e}")
    
    def sort_by_column(self, column):
        """Trier par colonne"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Trier les données
        try:
            self.filtered_data.sort(
                key=lambda x: x.get(column, ''),
                reverse=self.sort_reverse
            )
            
            # Mettre à jour l'indicateur de tri dans l'en-tête
            for col, btn in self.header_buttons.items():
                if col == column:
                    arrow = "↓" if self.sort_reverse else "↑"
                    btn.configure(text=f"{btn.cget('text').split(' ')[0]} {arrow}")
                else:
                    btn.configure(text=f"{btn.cget('text').split(' ')[0]} ↕")
            
            self.update_display_optimized()
            
        except Exception as e:
            self.logger.error(f"Error ordenando por {column}: {e}")
    
    @performance_optimizer.cache_result("low_stock_display", ttl=60)
    def show_low_stock_optimized(self):
        """Afficher le stock bas de manière optimisée"""
        try:
            low_stock_data = OptimizedStock.get_low_stock_optimized()
            
            self.search_var.set("")
            self.filtered_data = low_stock_data
            self.visible_range = (0, min(50, len(self.filtered_data)))
            
            self.update_display_optimized()
            self.update_stats()
            
            if not self.filtered_data:
                self.show_info_message("Stock Bajo", "No hay productos con stock bajo.")
            
        except Exception as e:
            self.logger.error(f"Error mostrando stock bajo: {e}")
    
    def quick_add_stock(self, item):
        """Ajouter rapidement du stock"""
        try:
            # Dialog simple pour ajouter stock
            dialog = ctk.CTkInputDialog(
                text=f"Agregar stock para {item['nombre']}:",
                title="Agregar Stock"
            )
            cantidad_str = dialog.get_input()
            
            if cantidad_str:
                cantidad = int(cantidad_str)
                if cantidad > 0:
                    # Mettre à jour en lot pour de meilleures performances
                    updates = [{
                        'producto_id': item['producto_id'],
                        'cantidad': item['cantidad'] + cantidad
                    }]
                    
                    BatchOperations.update_multiple_stock(updates)
                    
                    # Mettre à jour localement
                    item['cantidad'] += cantidad
                    
                    # Rafraîchir l'affichage
                    self.update_display_optimized()
                    self.update_stats()
                    
                    self.show_success_message(
                        "Éxito", 
                        f"Stock agregado: +{cantidad}\nNuevo total: {item['cantidad']}"
                    )
        
        except ValueError:
            self.show_error_message("Error", "Cantidad inválida")
        except Exception as e:
            self.logger.error(f"Error agregando stock rápido: {e}")
            self.show_error_message("Error", f"Error agregando stock: {e}")
    
    def update_stats(self):
        """Mettre à jour les statistiques en temps réel"""
        try:
            total_productos = len(self.stock_data)
            productos_mostrados = len(self.filtered_data)
            stock_bajo = len([item for item in self.filtered_data if item['cantidad'] <= 5])
            valor_total = sum(item['cantidad'] * item['precio'] for item in self.filtered_data)
            
            stats_text = (
                f"📊 Total: {total_productos} productos | "
                f"Mostrados: {productos_mostrados} | "
                f"Stock bajo: {stock_bajo} | "
                f"Valor total: €{valor_total:.2f}"
            )
            
            self.stats_label.configure(text=stats_text)
            
        except Exception as e:
            self.logger.error(f"Error actualizando estadísticas: {e}")
    
    def update_results_indicator(self):
        """Mettre à jour l'indicateur de résultats"""
        search_text = self.search_var.get().strip()
        if search_text:
            self.results_label.configure(
                text=f"{len(self.filtered_data)} resultados para '{search_text}'"
            )
        else:
            self.results_label.configure(text=f"{len(self.filtered_data)} productos")
    
    def clear_display(self):
        """Nettoyer l'affichage"""
        for widget in self.displayed_items.values():
            widget.destroy()
        self.displayed_items.clear()
    
    def show_no_data_message(self):
        """Afficher un message quand il n'y a pas de données"""
        no_data_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="No hay productos en stock",
            font=ctk.CTkFont(size=16)
        )
        no_data_label.pack(pady=50)
    
    def clear_search(self):
        """Nettoyer la recherche"""
        self.search_var.set("")
        self.filtered_data = self.stock_data.copy()
        self.visible_range = (0, min(50, len(self.filtered_data)))
        self.update_display_optimized()
        self.update_stats()
    
    def refresh_data(self):
        """Actualiser les données"""
        # Vider le cache
        performance_optimizer.clear_cache("stock")
        performance_optimizer.clear_cache("low_stock")
        
        # Recharger
        self.load_stock_data_optimized()
    
    def optimize_performance(self):
        """Optimiser les performances"""
        try:
            # Vider tous les caches
            performance_optimizer.clear_cache()
            
            # Préchauffer les caches
            OptimizedStock.get_all_optimized()
            OptimizedStock.get_low_stock_optimized()
            
            # Optimiser la base de données
            from utils.performance_optimizer import optimize_database_queries
            optimize_database_queries()
            
            self.show_success_message(
                "Optimización", 
                "Rendimiento optimizado correctamente"
            )
            
        except Exception as e:
            self.logger.error(f"Error optimizando rendimiento: {e}")
            self.show_error_message("Error", f"Error en optimización: {e}")
    
    def on_scroll_configure(self, event):
        """Gérer la configuration du scroll"""
        # Implémenter la virtualisation si nécessaire
        pass
    
    def on_mouse_wheel(self, event):
        """Gérer le scroll de la souris"""
        # Implémenter le scroll virtualisé si nécessaire
        pass


if __name__ == "__main__":
    # Test de la fenêtre optimisée
    root = ctk.CTk()
    app = OptimizedStockWindow(root)
    root.mainloop()
