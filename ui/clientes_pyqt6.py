# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des clients - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QGroupBox, QSplitter, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from utils.logger import get_logger

class ClientesPyQt6Window(BasePyQt6Window):
    """Fenêtre de gestion des clients en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Clientes", 1000, 700)
        self.logger = get_logger("clientes_pyqt6")
        self.current_client = None
        
        self.logger.info("Inicializando ventana de gestión de clientes PyQt6")
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(splitter)
        
        # Panneau gauche - Formulaire
        self.create_form_panel(splitter)
        
        # Panneau droit - Liste des clients
        self.create_clients_panel(splitter)
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_clients()
    
    def create_form_panel(self, parent):
        """Crée le panneau de formulaire"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Titre
        title_label = QLabel("Datos del Cliente")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        form_layout.addWidget(title_label)
        
        # Informations de base
        basic_group = QGroupBox("Información Básica")
        basic_layout = QGridLayout(basic_group)
        
        # Nom
        basic_layout.addWidget(QLabel("Nombre:"), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nombre completo o razón social")
        basic_layout.addWidget(self.name_edit, 0, 1)
        
        # NIF/CIF
        basic_layout.addWidget(QLabel("NIF/CIF:"), 1, 0)
        self.nif_edit = QLineEdit()
        self.nif_edit.setPlaceholderText("Número de identificación")
        basic_layout.addWidget(self.nif_edit, 1, 1)
        
        # Adresse
        basic_layout.addWidget(QLabel("Dirección:"), 2, 0)
        self.address_edit = QTextEdit()
        self.address_edit.setMaximumHeight(80)
        self.address_edit.setPlaceholderText("Dirección completa")
        basic_layout.addWidget(self.address_edit, 2, 1)
        
        form_layout.addWidget(basic_group)
        
        # Informations de contact
        contact_group = QGroupBox("Contacto")
        contact_layout = QGridLayout(contact_group)
        
        # Téléphone
        contact_layout.addWidget(QLabel("Teléfono:"), 0, 0)
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Número de teléfono")
        contact_layout.addWidget(self.phone_edit, 0, 1)
        
        # Email
        contact_layout.addWidget(QLabel("Email:"), 1, 0)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Dirección de correo")
        contact_layout.addWidget(self.email_edit, 1, 1)
        
        form_layout.addWidget(contact_group)
        
        # Notes
        notes_group = QGroupBox("Notas")
        notes_layout = QVBoxLayout(notes_group)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("Notas adicionales sobre el cliente...")
        notes_layout.addWidget(self.notes_edit)
        
        form_layout.addWidget(notes_group)
        
        # Stretch
        form_layout.addStretch()
        
        parent.addWidget(form_widget)
    
    def create_clients_panel(self, parent):
        """Crée le panneau de liste des clients"""
        clients_widget = QWidget()
        clients_layout = QVBoxLayout(clients_widget)
        
        # Titre
        title_label = QLabel("Lista de Clientes")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        clients_layout.addWidget(title_label)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar por nombre o NIF...")
        self.search_edit.textChanged.connect(self.filter_clients)
        search_layout.addWidget(self.search_edit)
        clients_layout.addLayout(search_layout)
        
        # Table des clients
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(4)
        self.clients_table.setHorizontalHeaderLabels([
            "Nombre", "NIF/CIF", "Teléfono", "Email"
        ])
        
        # Configuration de la table
        header = self.clients_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.clients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.clients_table.setAlternatingRowColors(True)

        # Permettre la sélection multiple (Ctrl pour sélection discrète, Shift pour plage)
        self.clients_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

        # Connecter le signal de changement de sélection
        self.clients_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.clients_table.itemSelectionChanged.connect(self.on_client_selected)
        
        clients_layout.addWidget(self.clients_table)

        # Label d'information sur la sélection
        self.selection_info_label = QLabel("Selecciona clientes con Ctrl+clic (discreto) o Shift+clic (rango)")
        self.selection_info_label.setStyleSheet("color: #6c757d; font-size: 10pt; padding: 5px;")
        clients_layout.addWidget(self.selection_info_label)

        parent.addWidget(clients_widget)
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("Nuevo", self.new_client, "success"),
            ("Guardar", self.save_client, "primary"),
            ("Eliminar", self.delete_clients, "danger"),  # Renommé pour gérer multiple
            ("Cerrar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def load_clients(self):
        """Charge la liste des clients depuis la base de données"""
        try:
            # Charger les clients depuis la base de données
            db_clients = db.get_all_clients()

            if db_clients:
                self.clients_table.setRowCount(len(db_clients))

                for row, client in enumerate(db_clients):
                    self.clients_table.setItem(row, 0, QTableWidgetItem(client["nombre"]))
                    self.clients_table.setItem(row, 1, QTableWidgetItem(client.get("nif", "")))
                    self.clients_table.setItem(row, 2, QTableWidgetItem(client.get("telefono", "")))
                    self.clients_table.setItem(row, 3, QTableWidgetItem(client.get("email", "")))

                    # Stocker les données complètes
                    self.clients_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, client)

                self.logger.info(f"Cargados {len(db_clients)} clientes de la base de datos")
            else:
                # Si pas de clients, créer quelques clients de démo
                self.logger.info("No hay clientes en la base de datos, creando clientes de demo")
                demo_clients = [
                    {"nombre": "Juan Pérez", "nif": "12345678A", "telefono": "91-123-4567", "email": "juan@email.com", "direccion": "Calle Mayor, 1"},
                    {"nombre": "María García", "nif": "87654321B", "telefono": "91-765-4321", "email": "maria@email.com", "direccion": "Avenida Principal, 25"},
                    {"nombre": "Empresa ABC S.L.", "nif": "A12345678", "telefono": "91-555-0123", "email": "info@abc.com", "direccion": "Polígono Industrial, 15"},
                ]

                # Créer les clients de démo en base
                created_clients = []
                for demo_client in demo_clients:
                    try:
                        client_id = db.add_client(demo_client)
                        demo_client['id'] = client_id
                        created_clients.append(demo_client)
                        self.logger.info(f"Cliente de demo creado: {demo_client['nombre']} (ID: {client_id})")
                    except Exception as e:
                        self.logger.error(f"Error creando cliente de demo: {e}")

                # Afficher les clients créés
                if created_clients:
                    self.clients_table.setRowCount(len(created_clients))
                    for row, client in enumerate(created_clients):
                        self.clients_table.setItem(row, 0, QTableWidgetItem(client["nombre"]))
                        self.clients_table.setItem(row, 1, QTableWidgetItem(client.get("nif", "")))
                        self.clients_table.setItem(row, 2, QTableWidgetItem(client.get("telefono", "")))
                        self.clients_table.setItem(row, 3, QTableWidgetItem(client.get("email", "")))
                        self.clients_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, client)

        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")
            self.show_error("Error", f"Error al cargar clientes: {e}")
    
    def filter_clients(self):
        """Filtre les clients"""
        search_text = self.search_edit.text().lower()
        
        for row in range(self.clients_table.rowCount()):
            show_row = True
            
            if search_text:
                name_item = self.clients_table.item(row, 0)
                nif_item = self.clients_table.item(row, 1)
                
                if not ((name_item and search_text in name_item.text().lower()) or
                        (nif_item and search_text in nif_item.text().lower())):
                    show_row = False
            
            self.clients_table.setRowHidden(row, not show_row)
    
    def on_client_selected(self):
        """Gère la sélection d'un client"""
        current_row = self.clients_table.currentRow()
        if current_row >= 0:
            name_item = self.clients_table.item(current_row, 0)
            if name_item:
                client_data = name_item.data(Qt.ItemDataRole.UserRole)
                self.load_client_data(client_data)
    
    def load_client_data(self, client_data):
        """Charge les données d'un client dans le formulaire"""
        if client_data:
            self.current_client = client_data
            
            self.name_edit.setText(client_data.get("nombre", ""))
            self.nif_edit.setText(client_data.get("nif", ""))
            self.address_edit.setPlainText(client_data.get("direccion", ""))
            self.phone_edit.setText(client_data.get("telefono", ""))
            self.email_edit.setText(client_data.get("email", ""))
            self.notes_edit.setPlainText(client_data.get("notas", ""))
    
    def new_client(self):
        """Prépare un nouveau client"""
        self.current_client = None
        self.clear_form()
        self.name_edit.setFocus()
    
    def clear_form(self):
        """Vide le formulaire"""
        self.name_edit.clear()
        self.nif_edit.clear()
        self.address_edit.clear()
        self.phone_edit.clear()
        self.email_edit.clear()
        self.notes_edit.clear()
    
    def save_client(self):
        """Sauvegarde le client"""
        try:
            # Validation
            if not self.name_edit.text().strip():
                self.show_warning("Validación", "El nombre es obligatorio")
                return
            
            # Préparer les données
            client_data = {
                'nombre': self.name_edit.text().strip(),
                'nif': self.nif_edit.text().strip(),
                'direccion': self.address_edit.toPlainText().strip(),
                'telefono': self.phone_edit.text().strip(),
                'email': self.email_edit.text().strip()
                # Note: 'notas' n'est pas dans le schéma de base de données
            }

            if self.current_client:
                # Mise à jour d'un client existant
                client_data['id'] = self.current_client['id']
                success = db.update_client(client_data)
                if success:
                    self.show_info("Éxito", f"Cliente '{client_data['nombre']}' actualizado correctamente")
                    self.logger.info(f"Cliente actualizado: {client_data['nombre']} (ID: {client_data['id']})")
                else:
                    self.show_error("Error", "No se pudo actualizar el cliente")
                    return
            else:
                # Création d'un nouveau client
                client_id = db.add_client(client_data)
                if client_id:
                    self.show_info("Éxito", f"Cliente '{client_data['nombre']}' creado con ID: {client_id}")
                    self.logger.info(f"Nuevo cliente creado: {client_data['nombre']} (ID: {client_id})")

                    # Mettre à jour current_client avec l'ID assigné
                    client_data['id'] = client_id
                    self.current_client = client_data
                else:
                    self.show_error("Error", "No se pudo crear el cliente")
                    return

            # Recharger la liste
            self.load_clients()

            # Vider le formulaire après sauvegarde réussie
            self.clear_form()
            self.current_client = None
            
        except Exception as e:
            self.logger.error(f"Error guardando cliente: {e}")
            self.show_error("Error", f"Error al guardar cliente: {e}")
    
    def delete_clients(self):
        """Supprime les clients sélectionnés (simple ou multiple)"""
        selected_rows = self.get_selected_rows()

        if not selected_rows:
            self.show_warning("Selección", "Selecciona uno o más clientes para eliminar")
            return

        try:
            # Préparer les informations des clients à supprimer
            clients_to_delete = []
            client_names = []

            for row in selected_rows:
                # Récupérer les données du client depuis la table
                client_data = self.clients_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                if client_data and client_data.get('id'):
                    clients_to_delete.append(client_data['id'])
                    client_names.append(client_data['nombre'])

            if not clients_to_delete:
                self.show_error("Error", "No se pudieron obtener los IDs de los clientes")
                return

            # Demander confirmation
            count = len(clients_to_delete)
            if count == 1:
                message = f"¿Eliminar el cliente '{client_names[0]}'?"
                title = "Confirmar Eliminación"
            else:
                names_text = ", ".join(client_names[:3])
                if count > 3:
                    names_text += f" y {count - 3} más"
                message = f"¿Eliminar {count} clientes?\n\nClientes: {names_text}"
                title = "Confirmar Eliminación Múltiple"

            if not self.ask_question(title, message):
                return

            # Eliminar de la base de datos
            if count == 1:
                success = db.delete_client(clients_to_delete[0])
                if success:
                    deleted_count = 1
                else:
                    deleted_count = 0
            else:
                deleted_count = db.delete_multiple_clients(clients_to_delete)

            if deleted_count > 0:
                # Recargar la lista de clients
                self.load_clients()

                # Mostrar mensaje de éxito
                if deleted_count == 1:
                    self.show_info("Éxito", "Cliente eliminado correctamente")
                else:
                    self.show_info("Éxito", f"{deleted_count} clientes eliminados correctamente")

                self.logger.info(f"{deleted_count} clientes eliminados")
            else:
                self.show_error("Error", "No se pudieron eliminar los clientes")

        except Exception as e:
            self.logger.error(f"Error eliminando clientes: {e}")
            self.show_error("Error", f"Error al eliminar clientes:\n{str(e)}")

    def get_selected_rows(self):
        """Obtiene las filas seleccionadas"""
        selected_items = self.clients_table.selectedItems()
        if not selected_items:
            return []

        # Obtener las filas únicas (éviter les doublons car plusieurs colonnes par ligne)
        selected_rows = list(set(item.row() for item in selected_items))
        selected_rows.sort()  # Trier pour un ordre cohérent

        return selected_rows

    def on_selection_changed(self):
        """Gère le changement de sélection"""
        try:
            selected_rows = self.get_selected_rows()
            count = len(selected_rows)

            if count == 0:
                self.selection_info_label.setText("Selecciona clientes con Ctrl+clic (discreto) o Shift+clic (rango)")
            elif count == 1:
                # Récupérer le nom du client
                client_data = self.clients_table.item(selected_rows[0], 0).data(Qt.ItemDataRole.UserRole)
                client_name = client_data['nombre'] if client_data else "N/A"
                self.selection_info_label.setText(f"1 cliente seleccionado: {client_name}")
            else:
                self.selection_info_label.setText(f"{count} clientes seleccionados")

        except Exception as e:
            self.logger.error(f"Error actualizando información de selección: {e}")
