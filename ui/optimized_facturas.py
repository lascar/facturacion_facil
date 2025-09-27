#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de facturas optimisée pour de meilleures performances
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from database.optimized_models import OptimizedFactura, OptimizedProducto
from utils.performance_optimizer import performance_monitor, performance_optimizer
from utils.translations import get_text
from utils.logger import get_logger
from common.ui_components import BaseWindow
import time


class OptimizedFacturasWindow(BaseWindow):
    """Fenêtre de facturas optimisée avec chargement paresseux et cache"""
    
    def __init__(self, parent, nueva_factura=False):
        super().__init__(parent, get_text("facturas"), "1400x900")
        
        # Variables de performance
        self.facturas_summary = []  # Résumé pour l'affichage rapide
        self.facturas_full = {}     # Cache des facturas complètes
        self.selected_factura_id = None
        self.current_factura = None
        self.productos_cache = {}   # Cache des productos
        
        # Variables de recherche optimisée
        self.search_var = tk.StringVar()
        self.last_search_time = 0
        self.search_delay = 200  # ms
        
        # Variables de pagination
        self.page_size = 50
        self.current_page = 0
        self.total_pages = 0
        
        self.create_optimized_widgets()
        self.load_facturas_optimized()
        self.load_productos_cache()
        
        if nueva_factura:
            self.nueva_factura()
        
        self.logger.info("Ventana de facturas optimizada inicializada")
    
    def create_optimized_widgets(self):
        """Créer l'interface optimisée"""
        # Frame principal avec splitter
        main_paned = ctk.CTkFrame(self.window)
        main_paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Lista de facturas optimizada
        left_panel = ctk.CTkFrame(main_paned)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.create_facturas_list_optimized(left_panel)
        
        # Panel derecho - Detalles de factura
        right_panel = ctk.CTkFrame(main_paned)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.create_factura_details_optimized(right_panel)
    
    def create_facturas_list_optimized(self, parent):
        """Créer la liste de facturas optimisée"""
        # Título y controles
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📄 Lista de Facturas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Controles de búsqueda y paginación
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Búsqueda optimizada
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍")
        search_label.pack(side="left", padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por número, cliente...",
            width=250
        )
        self.search_entry.pack(side="left", padx=5)
        
        # Búsqueda con debouncing
        self.search_var.trace_add("write", self.on_search_change)
        
        clear_search_btn = ctk.CTkButton(
            search_frame,
            text="✖",
            command=self.clear_search,
            width=30
        )
        clear_search_btn.pack(side="left", padx=5)
        
        # Controles de paginación
        pagination_frame = ctk.CTkFrame(controls_frame)
        pagination_frame.pack(side="right", padx=(5, 10), pady=10)
        
        self.prev_btn = ctk.CTkButton(
            pagination_frame,
            text="◀",
            command=self.prev_page,
            width=40
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.page_label = ctk.CTkLabel(
            pagination_frame,
            text="Página 1 de 1",
            width=100
        )
        self.page_label.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(
            pagination_frame,
            text="▶",
            command=self.next_page,
            width=40
        )
        self.next_btn.pack(side="left", padx=2)
        
        # TreeView optimizado para facturas
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear TreeView con scrollbar
        tree_container = tk.Frame(tree_frame, bg="#212121")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.facturas_tree = ttk.Treeview(
            tree_container,
            columns=("numero", "fecha", "cliente", "total"),
            show="headings",
            height=15
        )
        
        # Configurar columnas
        self.facturas_tree.heading("numero", text="Número", command=lambda: self.sort_facturas("numero"))
        self.facturas_tree.heading("fecha", text="Fecha", command=lambda: self.sort_facturas("fecha"))
        self.facturas_tree.heading("cliente", text="Cliente", command=lambda: self.sort_facturas("cliente"))
        self.facturas_tree.heading("total", text="Total", command=lambda: self.sort_facturas("total"))
        
        self.facturas_tree.column("numero", width=120, anchor="center")
        self.facturas_tree.column("fecha", width=100, anchor="center")
        self.facturas_tree.column("cliente", width=200, anchor="w")
        self.facturas_tree.column("total", width=100, anchor="e")
        
        # Scrollbar
        scrollbar_facturas = ttk.Scrollbar(tree_container, orient="vertical", command=self.facturas_tree.yview)
        self.facturas_tree.configure(yscrollcommand=scrollbar_facturas.set)
        
        self.facturas_tree.pack(side="left", fill="both", expand=True)
        scrollbar_facturas.pack(side="right", fill="y")
        
        # Bind para selección optimizada
        self.facturas_tree.bind("<<TreeviewSelect>>", self.on_factura_select_optimized)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        nueva_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Nueva Factura",
            command=self.nueva_factura,
            fg_color="green",
            hover_color="darkgreen"
        )
        nueva_btn.pack(side="left", padx=5, pady=5)
        
        eliminar_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_factura,
            fg_color="red",
            hover_color="darkred"
        )
        eliminar_btn.pack(side="left", padx=5, pady=5)
        
        pdf_btn = ctk.CTkButton(
            actions_frame,
            text="📄 Exportar PDF",
            command=self.exportar_pdf,
            fg_color="blue",
            hover_color="darkblue"
        )
        pdf_btn.pack(side="right", padx=5, pady=5)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Actualizar",
            command=self.refresh_facturas,
            width=100
        )
        refresh_btn.pack(side="right", padx=5, pady=5)
    
    def create_factura_details_optimized(self, parent):
        """Créer le panel de détails de factura optimisé"""
        # Título
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.details_title = ctk.CTkLabel(
            header_frame,
            text="📋 Detalles de Factura",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.details_title.pack(side="left", padx=10, pady=10)
        
        # Indicador de carga
        self.loading_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        )
        self.loading_label.pack(side="right", padx=10, pady=10)
        
        # Frame scrollable para detalles
        self.details_frame = ctk.CTkScrollableFrame(parent)
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Mensaje inicial
        self.show_no_selection_message()
    
    @performance_monitor.time_function("load_facturas_optimized")
    def load_facturas_optimized(self):
        """Charger les facturas de manière optimisée (résumé seulement)"""
        try:
            self.loading_label.configure(text="⏳ Cargando...")
            self.window.update()
            
            # Charger seulement le résumé pour l'affichage rapide
            self.facturas_summary = OptimizedFactura.get_summary_optimized()
            
            # Calculer la pagination
            self.total_pages = max(1, (len(self.facturas_summary) + self.page_size - 1) // self.page_size)
            self.current_page = 0
            
            self.update_facturas_display()
            self.update_pagination_controls()
            
            self.loading_label.configure(text="")
            self.logger.info(f"Facturas cargadas (resumen): {len(self.facturas_summary)}")
            
        except Exception as e:
            self.loading_label.configure(text="❌ Error")
            self.logger.error(f"Error cargando facturas optimizado: {e}")
            self.show_error_message("Error", f"Error cargando facturas: {e}")
    
    def update_facturas_display(self):
        """Mettre à jour l'affichage des facturas (pagination)"""
        try:
            # Nettoyer la liste
            for item in self.facturas_tree.get_children():
                self.facturas_tree.delete(item)
            
            # Calculer la plage de la page actuelle
            start_idx = self.current_page * self.page_size
            end_idx = min(start_idx + self.page_size, len(self.facturas_summary))
            
            # Ajouter les facturas de la page actuelle
            for i in range(start_idx, end_idx):
                factura = self.facturas_summary[i]
                self.facturas_tree.insert("", "end", values=(
                    factura['numero_factura'],
                    factura['fecha_factura'],
                    factura['nombre_cliente'],
                    f"€{factura['total_factura']:.2f}"
                ), tags=(str(factura['id']),))
            
        except Exception as e:
            self.logger.error(f"Error actualizando display facturas: {e}")
    
    def on_factura_select_optimized(self, event):
        """Gérer la sélection de factura de manière optimisée (chargement paresseux)"""
        try:
            selection = self.facturas_tree.selection()
            if not selection:
                return
            
            # Obtenir l'ID de la factura sélectionnée
            item = self.facturas_tree.item(selection[0])
            factura_id = int(item['tags'][0])
            
            if factura_id == self.selected_factura_id:
                return  # Déjà sélectionnée
            
            self.selected_factura_id = factura_id
            
            # Charger les détails de manière asynchrone
            self.load_factura_details_async(factura_id)
            
        except Exception as e:
            self.logger.error(f"Error en selección de factura: {e}")
    
    def load_factura_details_async(self, factura_id):
        """Charger les détails de factura de manière asynchrone"""
        try:
            self.loading_label.configure(text="⏳ Cargando detalles...")
            self.window.update()
            
            # Vérifier le cache
            if factura_id in self.facturas_full:
                factura = self.facturas_full[factura_id]
            else:
                # Charger depuis la base de données
                from database.models import Factura
                factura = Factura.get_by_id(factura_id)
                if factura:
                    self.facturas_full[factura_id] = factura
            
            if factura:
                self.current_factura = factura
                self.display_factura_details(factura)
            
            self.loading_label.configure(text="")
            
        except Exception as e:
            self.loading_label.configure(text="❌ Error")
            self.logger.error(f"Error cargando detalles de factura {factura_id}: {e}")
    
    def display_factura_details(self, factura):
        """Afficher les détails de la factura"""
        try:
            # Nettoyer le frame de détails
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            
            # Información básica
            basic_frame = ctk.CTkFrame(self.details_frame)
            basic_frame.pack(fill="x", padx=10, pady=5)
            
            basic_title = ctk.CTkLabel(
                basic_frame,
                text="📋 Información Básica",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            basic_title.pack(anchor="w", padx=10, pady=(10, 5))
            
            # Grid para información básica
            info_grid = ctk.CTkFrame(basic_frame)
            info_grid.pack(fill="x", padx=10, pady=(0, 10))
            
            info_data = [
                ("Número:", factura.numero_factura),
                ("Fecha:", factura.fecha_factura),
                ("Cliente:", factura.nombre_cliente),
                ("Email:", factura.email_cliente or "N/A"),
                ("Teléfono:", factura.telefono_cliente or "N/A"),
                ("Modo de Pago:", factura.modo_pago or "Efectivo")
            ]
            
            for i, (label, value) in enumerate(info_data):
                row = i // 2
                col = i % 2
                
                label_widget = ctk.CTkLabel(
                    info_grid,
                    text=label,
                    font=ctk.CTkFont(weight="bold")
                )
                label_widget.grid(row=row, column=col*2, sticky="w", padx=(10, 5), pady=2)
                
                value_widget = ctk.CTkLabel(info_grid, text=str(value))
                value_widget.grid(row=row, column=col*2+1, sticky="w", padx=(0, 20), pady=2)
            
            # Items de la factura
            items_frame = ctk.CTkFrame(self.details_frame)
            items_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            items_title = ctk.CTkLabel(
                items_frame,
                text="🛒 Productos",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            items_title.pack(anchor="w", padx=10, pady=(10, 5))
            
            # TreeView para items
            items_tree_frame = tk.Frame(items_frame, bg="#212121")
            items_tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            items_tree = ttk.Treeview(
                items_tree_frame,
                columns=("producto", "cantidad", "precio", "iva", "total"),
                show="headings",
                height=8
            )
            
            # Configurar columnas de items
            items_tree.heading("producto", text="Producto")
            items_tree.heading("cantidad", text="Cant.")
            items_tree.heading("precio", text="Precio Unit.")
            items_tree.heading("iva", text="IVA")
            items_tree.heading("total", text="Total")
            
            items_tree.column("producto", width=200, anchor="w")
            items_tree.column("cantidad", width=80, anchor="center")
            items_tree.column("precio", width=100, anchor="e")
            items_tree.column("iva", width=80, anchor="e")
            items_tree.column("total", width=100, anchor="e")
            
            # Scrollbar para items
            items_scrollbar = ttk.Scrollbar(items_tree_frame, orient="vertical", command=items_tree.yview)
            items_tree.configure(yscrollcommand=items_scrollbar.set)
            
            items_tree.pack(side="left", fill="both", expand=True)
            items_scrollbar.pack(side="right", fill="y")
            
            # Cargar items
            for item in factura.items:
                producto_nombre = "Producto desconocido"
                if item.producto:
                    producto_nombre = item.producto.nombre
                elif item.producto_id in self.productos_cache:
                    producto_nombre = self.productos_cache[item.producto_id]['nombre']
                
                items_tree.insert("", "end", values=(
                    producto_nombre,
                    f"{item.cantidad}",
                    f"€{item.precio_unitario:.2f}",
                    f"{item.iva_aplicado}%",
                    f"€{item.total:.2f}"
                ))
            
            # Totales
            totals_frame = ctk.CTkFrame(self.details_frame)
            totals_frame.pack(fill="x", padx=10, pady=5)
            
            totals_title = ctk.CTkLabel(
                totals_frame,
                text="💰 Totales",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            totals_title.pack(anchor="w", padx=10, pady=(10, 5))
            
            totals_grid = ctk.CTkFrame(totals_frame)
            totals_grid.pack(fill="x", padx=10, pady=(0, 10))
            
            totals_data = [
                ("Subtotal:", f"€{factura.subtotal:.2f}"),
                ("IVA:", f"€{factura.total_iva:.2f}"),
                ("TOTAL:", f"€{factura.total_factura:.2f}")
            ]
            
            for i, (label, value) in enumerate(totals_data):
                label_widget = ctk.CTkLabel(
                    totals_grid,
                    text=label,
                    font=ctk.CTkFont(weight="bold")
                )
                label_widget.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=2)
                
                color = "green" if "TOTAL" in label else "white"
                value_widget = ctk.CTkLabel(
                    totals_grid,
                    text=value,
                    text_color=color,
                    font=ctk.CTkFont(weight="bold" if "TOTAL" in label else "normal")
                )
                value_widget.grid(row=i, column=1, sticky="e", padx=(0, 10), pady=2)
            
        except Exception as e:
            self.logger.error(f"Error mostrando detalles de factura: {e}")
    
    def load_productos_cache(self):
        """Charger le cache des productos pour éviter les requêtes répétées"""
        try:
            productos_summary = OptimizedProducto.get_summary_optimized()
            self.productos_cache = {p['id']: p for p in productos_summary}
            self.logger.info(f"Cache de productos cargado: {len(self.productos_cache)} productos")
        except Exception as e:
            self.logger.error(f"Error cargando cache de productos: {e}")
    
    def on_search_change(self, *args):
        """Gérer les changements de recherche avec debouncing"""
        current_time = time.time() * 1000
        self.last_search_time = current_time
        self.window.after(self.search_delay, lambda: self.delayed_search(current_time))
    
    def delayed_search(self, search_time):
        """Exécuter la recherche avec délai"""
        if search_time == self.last_search_time:
            self.perform_search()
    
    def perform_search(self):
        """Effectuer la recherche"""
        try:
            search_text = self.search_var.get().lower().strip()
            
            if not search_text:
                # Restaurer toutes les facturas
                self.facturas_summary = OptimizedFactura.get_summary_optimized()
            else:
                # Filtrer les facturas
                all_facturas = OptimizedFactura.get_summary_optimized()
                self.facturas_summary = [
                    f for f in all_facturas
                    if (search_text in f['numero_factura'].lower() or
                        search_text in f['nombre_cliente'].lower())
                ]
            
            # Réinitialiser la pagination
            self.total_pages = max(1, (len(self.facturas_summary) + self.page_size - 1) // self.page_size)
            self.current_page = 0
            
            self.update_facturas_display()
            self.update_pagination_controls()
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
    
    def clear_search(self):
        """Nettoyer la recherche"""
        self.search_var.set("")
        self.perform_search()
    
    def prev_page(self):
        """Page précédente"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_facturas_display()
            self.update_pagination_controls()
    
    def next_page(self):
        """Page suivante"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_facturas_display()
            self.update_pagination_controls()
    
    def update_pagination_controls(self):
        """Mettre à jour les contrôles de pagination"""
        self.page_label.configure(text=f"Página {self.current_page + 1} de {self.total_pages}")
        
        self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")
    
    def sort_facturas(self, column):
        """Trier les facturas par colonne"""
        try:
            reverse = getattr(self, f'_sort_{column}_reverse', False)
            
            if column == "numero":
                self.facturas_summary.sort(key=lambda x: x['numero_factura'], reverse=reverse)
            elif column == "fecha":
                self.facturas_summary.sort(key=lambda x: x['fecha_factura'], reverse=reverse)
            elif column == "cliente":
                self.facturas_summary.sort(key=lambda x: x['nombre_cliente'], reverse=reverse)
            elif column == "total":
                self.facturas_summary.sort(key=lambda x: x['total_factura'], reverse=reverse)
            
            setattr(self, f'_sort_{column}_reverse', not reverse)
            
            self.update_facturas_display()
            
        except Exception as e:
            self.logger.error(f"Error ordenando por {column}: {e}")
    
    def show_no_selection_message(self):
        """Afficher un message quand aucune factura n'est sélectionnée"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        message_label = ctk.CTkLabel(
            self.details_frame,
            text="👈 Selecciona una factura para ver sus detalles",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        message_label.pack(expand=True)
    
    def refresh_facturas(self):
        """Actualiser les facturas"""
        # Vider les caches
        performance_optimizer.clear_cache("facturas")
        self.facturas_full.clear()
        
        # Recharger
        self.load_facturas_optimized()
        self.show_no_selection_message()
    
    def nueva_factura(self):
        """Créer une nouvelle factura"""
        # Implémenter la création de nouvelle factura
        self.show_info_message("Nueva Factura", "Funcionalidad en desarrollo")
    
    def eliminar_factura(self):
        """Supprimer la factura sélectionnée"""
        if not self.current_factura:
            self.show_warning_message("Advertencia", "Selecciona una factura para eliminar")
            return
        
        # Implémenter la suppression
        self.show_info_message("Eliminar Factura", "Funcionalidad en desarrollo")
    
    def exportar_pdf(self):
        """Exporter la factura en PDF"""
        if not self.current_factura:
            self.show_warning_message("Advertencia", "Selecciona una factura para exportar")
            return
        
        # Implémenter l'export PDF
        self.show_info_message("Exportar PDF", "Funcionalidad en desarrollo")


if __name__ == "__main__":
    # Test de la fenêtre optimisée
    root = ctk.CTk()
    app = OptimizedFacturasWindow(root)
    root.mainloop()
