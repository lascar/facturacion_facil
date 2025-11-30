# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des clients - Version PyQt5 native
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QSplitter, QFrame, QWidget, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtGui import QFont

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import db
from utils.logger import get_logger

class ClientesPyQt5Window(BasePyQt5Window):
    """Fenêtre de gestion des clients avec PyQt5"""
    
    # Signaux
    cliente_selected = Signal(dict)
    cliente_updated = Signal(int)
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Gestión de Clientes", 1000, 700)
        
        # Variables
        self.clientes = []
        self.selected_cliente_id = None
        
        # Charger les données
        self.load_clientes()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Layout principal
        main_layout = QHBoxLayout(self)
        
        # Splitter pour diviser l'interface
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Configuration des sections
        self.setup_clients_list(splitter)
        self.setup_client_form(splitter)
        
        # Boutons
        buttons_layout = QVBoxLayout()
        
        self.new_btn = QPushButton("➕ Nuevo")
        self.save_btn = QPushButton("💾 Guardar")
        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.refresh_btn = QPushButton("🔄 Actualizar")
        
        buttons_layout.addWidget(self.new_btn)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addStretch()
        
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        buttons_widget.setMaximumWidth(150)
        main_layout.addWidget(buttons_widget)
        
        # Connexions
        self.setup_connections()
        
        # Appliquer le style
        self.apply_style()
        
    def setup_clients_list(self, parent):
        """Configurer la liste des clients"""
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Label
        list_label = QLabel("Lista de Clientes")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        list_layout.addWidget(list_label)
        
        # Table des clients
        self.clients_table = QTableWidget()
        headers = ["ID", "Nombre", "NIF/DNI", "Email", "Teléfono"]
        self.setup_table_widget(self.clients_table, headers)
        
        # Connecter la sélection
        self.clients_table.itemSelectionChanged.connect(self.on_client_selected)
        
        list_layout.addWidget(self.clients_table)
        parent.addWidget(list_widget)
        
    def setup_client_form(self, parent):
        """Configurer le formulaire de client"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # GroupBox pour le formulaire
        form_group = QGroupBox("Detalles del Cliente")
        form_group_layout = QGridLayout(form_group)
        
        # Champs du formulaire
        self.nombre_edit = QLineEdit()
        self.nif_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.direccion_edit = QTextEdit()
        self.direccion_edit.setMaximumHeight(100)
        
        # Ajouter les champs au layout
        form_group_layout.addWidget(QLabel("Nombre:"), 0, 0)
        form_group_layout.addWidget(self.nombre_edit, 0, 1)
        
        form_group_layout.addWidget(QLabel("NIF/DNI:"), 1, 0)
        form_group_layout.addWidget(self.nif_edit, 1, 1)
        
        form_group_layout.addWidget(QLabel("Email:"), 2, 0)
        form_group_layout.addWidget(self.email_edit, 2, 1)
        
        form_group_layout.addWidget(QLabel("Teléfono:"), 3, 0)
        form_group_layout.addWidget(self.telefono_edit, 3, 1)
        
        form_group_layout.addWidget(QLabel("Dirección:"), 4, 0)
        form_group_layout.addWidget(self.direccion_edit, 4, 1)
        
        form_layout.addWidget(form_group)
        form_layout.addStretch()
        
        parent.addWidget(form_widget)
        
    def setup_connections(self):
        """Configurer les connexions de signaux"""
        self.new_btn.clicked.connect(self.new_cliente)
        self.save_btn.clicked.connect(self.save_cliente)
        self.delete_btn.clicked.connect(self.delete_cliente)
        self.refresh_btn.clicked.connect(self.load_clientes)
        
        # Connecter les changements de données
        self.nombre_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.nif_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.email_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.telefono_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.direccion_edit.textChanged.connect(lambda: self.set_data_modified(True))
        
    def load_clientes(self):
        """Charger les clients depuis la base de données"""
        try:
            self.clientes = db.get_all_clients()
            self.update_clients_table()
        except Exception as e:
            self.logger.error(f"Erreur chargement clients: {e}")
            self.show_error("Erreur", f"Impossible de charger les clients: {str(e)}")
            
    def update_clients_table(self):
        """Mettre à jour la table des clients"""
        self.clients_table.setRowCount(len(self.clientes))
        
        for row, cliente in enumerate(self.clientes):
            self.clients_table.setItem(row, 0, QTableWidgetItem(str(cliente.get('id', ''))))
            self.clients_table.setItem(row, 1, QTableWidgetItem(str(cliente.get('nombre', ''))))
            self.clients_table.setItem(row, 2, QTableWidgetItem(str(cliente.get('nif', ''))))
            self.clients_table.setItem(row, 3, QTableWidgetItem(str(cliente.get('email', ''))))
            self.clients_table.setItem(row, 4, QTableWidgetItem(str(cliente.get('telefono', ''))))

    def on_client_selected(self):
        """Gérer la sélection d'un client"""
        current_row = self.clients_table.currentRow()
        if current_row >= 0 and current_row < len(self.clientes):
            cliente = self.clientes[current_row]
            self.selected_cliente_id = cliente.get('id')
            self.load_client_data(cliente)
            self.cliente_selected.emit(cliente)

    def load_client_data(self, cliente):
        """Charger les données d'un client dans le formulaire"""
        self.nombre_edit.setText(str(cliente.get('nombre', '')))
        self.nif_edit.setText(str(cliente.get('nif', '')))
        self.email_edit.setText(str(cliente.get('email', '')))
        self.telefono_edit.setText(str(cliente.get('telefono', '')))
        self.direccion_edit.setPlainText(str(cliente.get('direccion', '')))
        self.set_data_modified(False)

    def new_cliente(self):
        """Créer un nouveau client"""
        self.selected_cliente_id = None
        self.nombre_edit.clear()
        self.nif_edit.clear()
        self.email_edit.clear()
        self.telefono_edit.clear()
        self.direccion_edit.clear()
        self.set_data_modified(False)

    def save_cliente(self):
        """Sauvegarder le client"""
        try:
            # Validation basique
            if not self.nombre_edit.text().strip():
                self.show_warning("Validation", "Le nom du client est requis")
                return

            # Préparer les données
            cliente_data = {
                'nombre': self.nombre_edit.text().strip(),
                'nif': self.nif_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'telefono': self.telefono_edit.text().strip(),
                'direccion': self.direccion_edit.toPlainText().strip()
            }

            # Sauvegarder
            if self.selected_cliente_id:
                # Mise à jour
                cliente_data['id'] = self.selected_cliente_id
                db.update_client(cliente_data)
                self.show_info("Éxito", "Cliente actualizado correctamente")
            else:
                # Nouveau client
                new_id = db.add_client(cliente_data)
                self.selected_cliente_id = new_id
                self.show_info("Éxito", "Cliente creado correctamente")

            # Recharger les données
            self.load_clientes()
            self.set_data_modified(False)
            self.cliente_updated.emit(self.selected_cliente_id or 0)

        except Exception as e:
            self.logger.error(f"Erreur sauvegarde client: {e}")
            self.show_error("Error", f"Error al guardar el cliente: {str(e)}")

    def delete_cliente(self):
        """Supprimer le client sélectionné"""
        if not self.selected_cliente_id:
            self.show_warning("Selección", "Seleccione un cliente para eliminar")
            return

        # Vérifier d'abord si le client a des factures
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM facturas WHERE cliente_id = ?", (self.selected_cliente_id,))
            invoice_count = cursor.fetchone()[0]

            # Obtenir les informations du client
            cursor.execute("SELECT nombre FROM clientes WHERE id = ?", (self.selected_cliente_id,))
            client_result = cursor.fetchone()
            client_name = client_result[0] if client_result else "Cliente"
            conn.close()

            if invoice_count > 0:
                # Le client a des factures, proposer des options
                self.show_client_with_invoices_dialog(client_name, invoice_count)
                return

        except Exception as e:
            self.logger.error(f"Error verificando facturas del cliente: {e}")
            self.show_error("Error", f"Error al verificar las facturas del cliente: {str(e)}")
            return

        # Le client n'a pas de factures, procéder à la suppression normale
        if self.ask_confirmation("Confirmar", f"¿Está seguro de eliminar el cliente '{client_name}'?"):
            try:
                db.delete_client(self.selected_cliente_id)
                self.show_info("Éxito", "Cliente eliminado correctamente")
                self.load_clientes()
                self.new_cliente()
            except Exception as e:
                self.logger.error(f"Error suppression client: {e}")
                self.show_error("Error", f"Error al eliminar el cliente: {str(e)}")

    def show_client_with_invoices_dialog(self, client_name, invoice_count):
        """Afficher un dialogue avec options quand le client a des factures"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Cliente con Facturas")
        dialog.setModal(True)
        dialog.resize(500, 300)

        layout = QVBoxLayout(dialog)

        # Message principal
        title_label = QLabel(f"<h3>No se puede eliminar el cliente '{client_name}'</h3>")
        layout.addWidget(title_label)

        info_label = QLabel(f"Este cliente tiene <b>{invoice_count} factura(s)</b> asociada(s).")
        layout.addWidget(info_label)

        explanation_label = QLabel(
            "Para mantener la integridad de los datos, no se puede eliminar un cliente "
            "que tiene facturas asociadas."
        )
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        # Opciones disponibles
        options_label = QLabel("<h4>Opciones disponibles:</h4>")
        layout.addWidget(options_label)

        option1_label = QLabel("• <b>Ver facturas:</b> Consultar las facturas de este cliente")
        layout.addWidget(option1_label)

        option2_label = QLabel("• <b>Eliminar facturas:</b> Eliminar primero todas las facturas del cliente")
        layout.addWidget(option2_label)

        option3_label = QLabel("• <b>Cancelar:</b> Mantener el cliente y sus facturas")
        layout.addWidget(option3_label)

        # Botones
        buttons_layout = QHBoxLayout()

        view_invoices_btn = QPushButton("Ver Facturas")
        view_invoices_btn.clicked.connect(lambda: self.view_client_invoices(dialog))
        buttons_layout.addWidget(view_invoices_btn)

        delete_invoices_btn = QPushButton("Eliminar Facturas")
        delete_invoices_btn.setStyleSheet("background-color: #dc3545; color: white;")
        delete_invoices_btn.clicked.connect(lambda: self.delete_client_invoices(dialog, client_name, invoice_count))
        buttons_layout.addWidget(delete_invoices_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(dialog.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        dialog.exec_()

    def view_client_invoices(self, dialog):
        """Ouvrir la fenêtre des factures avec filtre sur le client"""
        dialog.accept()

        # Obtenir le nom du client
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM clientes WHERE id = ?", (self.selected_cliente_id,))
            client_result = cursor.fetchone()
            client_name = client_result[0] if client_result else "Cliente"
            conn.close()

            self.show_info("Información",
                          f"Abre la ventana de Facturas para ver las facturas del cliente '{client_name}'.\n\n"
                          f"Puedes filtrar por cliente o eliminar las facturas individualmente.")

        except Exception as e:
            self.logger.error(f"Error obteniendo nombre del cliente: {e}")

    def delete_client_invoices(self, dialog, client_name, invoice_count):
        """Eliminar todas las facturas del cliente y luego el cliente"""
        # Confirmar la eliminación de las facturas
        reply = QMessageBox.question(
            dialog,
            "Confirmar Eliminación de Facturas",
            f"¿Está seguro de eliminar las {invoice_count} factura(s) del cliente '{client_name}'?\n\n"
            f"Esta acción eliminará:\n"
            f"• Todas las facturas del cliente\n"
            f"• El cliente '{client_name}'\n\n"
            f"Esta acción NO se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Obtener los IDs de las facturas del cliente
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM facturas WHERE cliente_id = ?", (self.selected_cliente_id,))
                invoice_ids = [row[0] for row in cursor.fetchall()]
                conn.close()

                # Eliminar las facturas
                if invoice_ids:
                    deleted_invoices = db.delete_multiple_invoices(invoice_ids)
                    self.logger.info(f"Eliminadas {deleted_invoices} facturas del cliente {self.selected_cliente_id}")

                # Ahora eliminar el cliente
                db.delete_client(self.selected_cliente_id)

                dialog.accept()
                self.show_info("Éxito",
                              f"Cliente '{client_name}' y sus {invoice_count} factura(s) eliminados correctamente")
                self.load_clientes()
                self.new_cliente()

            except Exception as e:
                self.logger.error(f"Error eliminando cliente y facturas: {e}")
                self.show_error("Error", f"Error al eliminar el cliente y sus facturas: {str(e)}")
