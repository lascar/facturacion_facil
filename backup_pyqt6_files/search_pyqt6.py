# -*- coding: utf-8 -*-
"""
Fenêtre de recherche globale - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDateEdit, QGroupBox, QTabWidget, QWidget, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from utils.logger import get_logger

class SearchPyQt6Window(BasePyQt6Window):
    """Fenêtre de recherche globale en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Búsqueda Global", 1000, 700)
        self.logger = get_logger("search_pyqt6")
        
        self.logger.info("Inicializando ventana de búsqueda global PyQt6")
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title_label = QLabel("Búsqueda Global")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Panneau de recherche
        self.create_search_panel()
        
        # Onglets de résultats
        self.create_results_tabs()
        
        # Boutons d'action
        self.create_action_buttons()
    
    def create_search_panel(self):
        """Crée le panneau de recherche"""
        search_group = QGroupBox("Criterios de Búsqueda")
        search_layout = QGridLayout(search_group)
        
        # Terme de recherche
        search_layout.addWidget(QLabel("Buscar:"), 0, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Introduce términos de búsqueda...")
        search_layout.addWidget(self.search_edit, 0, 1, 1, 2)
        
        # Type de recherche
        search_layout.addWidget(QLabel("Buscar en:"), 1, 0)
        self.search_type = QComboBox()
        self.search_type.addItems(["Todo", "Productos", "Clientes", "Facturas"])
        search_layout.addWidget(self.search_type, 1, 1)
        
        # Bouton de recherche
        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(search_btn, 1, 2)
        
        # Filtres de date
        search_layout.addWidget(QLabel("Desde:"), 2, 0)
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-3))
        self.date_from.setCalendarPopup(True)
        search_layout.addWidget(self.date_from, 2, 1)
        
        search_layout.addWidget(QLabel("Hasta:"), 2, 2)
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        search_layout.addWidget(self.date_to, 2, 3)
        
        self.main_layout.addWidget(search_group)
    
    def create_results_tabs(self):
        """Crée les onglets de résultats"""
        self.results_tabs = QTabWidget()
        
        # Onglet Productos
        self.products_tab = self.create_products_tab()
        self.results_tabs.addTab(self.products_tab, "Productos")
        
        # Onglet Clientes
        self.clients_tab = self.create_clients_tab()
        self.results_tabs.addTab(self.clients_tab, "Clientes")
        
        # Onglet Facturas
        self.invoices_tab = self.create_invoices_tab()
        self.results_tabs.addTab(self.invoices_tab, "Facturas")
        
        self.main_layout.addWidget(self.results_tabs)
    
    def create_products_tab(self):
        """Crée l'onglet des produits"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels([
            "Referencia", "Nombre", "Categoría", "Precio"
        ])
        
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.products_table.setAlternatingRowColors(True)
        layout.addWidget(self.products_table)
        
        return tab
    
    def create_clients_tab(self):
        """Crée l'onglet des clients"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(4)
        self.clients_table.setHorizontalHeaderLabels([
            "Nombre", "NIF/CIF", "Teléfono", "Email"
        ])
        
        header = self.clients_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.clients_table.setAlternatingRowColors(True)
        layout.addWidget(self.clients_table)
        
        return tab
    
    def create_invoices_tab(self):
        """Crée l'onglet des factures"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(5)
        self.invoices_table.setHorizontalHeaderLabels([
            "Número", "Fecha", "Cliente", "Total", "Estado"
        ])
        
        header = self.invoices_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.invoices_table.setAlternatingRowColors(True)
        layout.addWidget(self.invoices_table)
        
        return tab
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("Limpiar", self.clear_results, "secondary"),
            ("Exportar", self.export_results, "secondary"),
            ("Cerrar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def perform_search(self):
        """Effectue la recherche"""
        search_term = self.search_edit.text().strip()
        search_type = self.search_type.currentText()
        
        if not search_term:
            self.show_warning("Búsqueda", "Introduce un término de búsqueda")
            return
        
        try:
            self.logger.info(f"Realizando búsqueda: '{search_term}' en '{search_type}'")
            
            # Effacer les résultats précédents
            self.clear_results()
            
            # Effectuer la recherche selon le type
            if search_type in ["Todo", "Productos"]:
                self.search_products(search_term)
            
            if search_type in ["Todo", "Clientes"]:
                self.search_clients(search_term)
            
            if search_type in ["Todo", "Facturas"]:
                self.search_invoices(search_term)
            
            self.show_info("Búsqueda", f"Búsqueda completada para '{search_term}'")
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
            self.show_error("Error", f"Error realizando búsqueda: {e}")
    
    def search_products(self, term):
        """Recherche dans les produits"""
        # Données de démonstration
        demo_products = [
            {"referencia": "P001", "nombre": "Producto A", "categoria": "Categoría 1", "precio": "25.00 €"},
            {"referencia": "P002", "nombre": "Producto B", "categoria": "Categoría 2", "precio": "35.50 €"},
        ]
        
        # Filtrer selon le terme de recherche
        filtered_products = [p for p in demo_products 
                           if term.lower() in p["nombre"].lower() or term.lower() in p["referencia"].lower()]
        
        self.products_table.setRowCount(len(filtered_products))
        
        for row, product in enumerate(filtered_products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product["referencia"]))
            self.products_table.setItem(row, 1, QTableWidgetItem(product["nombre"]))
            self.products_table.setItem(row, 2, QTableWidgetItem(product["categoria"]))
            self.products_table.setItem(row, 3, QTableWidgetItem(product["precio"]))
    
    def search_clients(self, term):
        """Recherche dans les clients"""
        # Données de démonstration
        demo_clients = [
            {"nombre": "Juan Pérez", "nif": "12345678A", "telefono": "91-123-4567", "email": "juan@email.com"},
            {"nombre": "María García", "nif": "87654321B", "telefono": "91-765-4321", "email": "maria@email.com"},
        ]
        
        # Filtrer selon le terme de recherche
        filtered_clients = [c for c in demo_clients 
                          if term.lower() in c["nombre"].lower() or term.lower() in c["nif"].lower()]
        
        self.clients_table.setRowCount(len(filtered_clients))
        
        for row, client in enumerate(filtered_clients):
            self.clients_table.setItem(row, 0, QTableWidgetItem(client["nombre"]))
            self.clients_table.setItem(row, 1, QTableWidgetItem(client["nif"]))
            self.clients_table.setItem(row, 2, QTableWidgetItem(client["telefono"]))
            self.clients_table.setItem(row, 3, QTableWidgetItem(client["email"]))
    
    def search_invoices(self, term):
        """Recherche dans les factures"""
        # Données de démonstration
        demo_invoices = [
            {"numero": "F-2024-001", "fecha": "2024-01-15", "cliente": "Juan Pérez", "total": "1250.00 €", "estado": "Pagada"},
            {"numero": "F-2024-002", "fecha": "2024-01-20", "cliente": "María García", "total": "850.50 €", "estado": "Pendiente"},
        ]
        
        # Filtrer selon le terme de recherche
        filtered_invoices = [i for i in demo_invoices 
                           if term.lower() in i["numero"].lower() or term.lower() in i["cliente"].lower()]
        
        self.invoices_table.setRowCount(len(filtered_invoices))
        
        for row, invoice in enumerate(filtered_invoices):
            self.invoices_table.setItem(row, 0, QTableWidgetItem(invoice["numero"]))
            self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice["fecha"]))
            self.invoices_table.setItem(row, 2, QTableWidgetItem(invoice["cliente"]))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(invoice["total"]))
            self.invoices_table.setItem(row, 4, QTableWidgetItem(invoice["estado"]))
    
    def clear_results(self):
        """Efface tous les résultats"""
        self.products_table.setRowCount(0)
        self.clients_table.setRowCount(0)
        self.invoices_table.setRowCount(0)
        self.search_edit.clear()
    
    def export_results(self):
        """Exporte les résultats"""
        self.show_info("Exportar", "Funcionalidad de exportación\n(Por implementar)")
