# -*- coding: utf-8 -*-
"""
Widget d'autocomplétion intelligent pour les clients
"""

from PyQt6.QtWidgets import (
    QLineEdit, QCompleter, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QDialog, QDialogButtonBox, QFormLayout, QTextEdit
)
from PyQt6.QtCore import Qt, QStringListModel, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from utils.logger import get_logger

class ClientAutoCompleteWidget(QLineEdit):
    """Widget d'autocomplétion pour les clients avec création automatique"""
    
    # Signaux émis quand un client est sélectionné ou créé
    client_selected = pyqtSignal(dict)  # Client existant sélectionné
    client_created = pyqtSignal(dict)   # Nouveau client créé
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger("client_autocomplete")
        
        # Données des clients
        self.clients_data = []
        self.current_client = None
        
        # Configuration du widget
        self.setup_widget()
        self.setup_completer()
        
        # Timer pour éviter trop de requêtes
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.update_suggestions)
        
        # Connecter les signaux
        self.textChanged.connect(self.on_text_changed)
        self.editingFinished.connect(self.on_editing_finished)
        
        self.logger.info("Widget d'autocomplétion client initialisé")
    
    def setup_widget(self):
        """Configure le widget"""
        self.setPlaceholderText("Escriba el nombre del cliente...")
        self.setMinimumHeight(35)

        # S'assurer que le widget est éditable
        self.setReadOnly(False)
        self.setEnabled(True)

        # Style pour indiquer l'autocomplétion
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            QLineEdit[hasClient="true"] {
                border-color: #27ae60;
                background-color: #d5f4e6;
            }
            QLineEdit[isNew="true"] {
                border-color: #f39c12;
                background-color: #fef9e7;
            }
        """)
    
    def setup_completer(self):
        """Configure l'autocomplétion"""
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        # Configuration pour permettre la saisie libre
        self.completer.setCompletionRole(Qt.ItemDataRole.DisplayRole)

        # Connecter la sélection
        self.completer.activated.connect(self.on_completion_selected)

        self.setCompleter(self.completer)
    
    def load_clients(self, clients_data):
        """Charge la liste des clients"""
        self.clients_data = clients_data
        self.update_completer_model()
        
        self.logger.info(f"Cargados {len(clients_data)} clientes para autocompletado")
    
    def update_completer_model(self):
        """Met à jour le modèle de l'autocomplétion"""
        if not self.clients_data:
            return
        
        # Créer la liste des suggestions (nom + informations supplémentaires)
        suggestions = []
        for client in self.clients_data:
            name = client.get('nombre', '')
            nif = client.get('nif', '')
            
            # Format: "Nom (NIF)" pour l'affichage
            if nif:
                suggestion = f"{name} ({nif})"
            else:
                suggestion = name
            
            suggestions.append(suggestion)
        
        # Mettre à jour le modèle
        model = QStringListModel(suggestions)
        self.completer.setModel(model)
    
    def on_text_changed(self, text):
        """Gère le changement de texte"""
        # Réinitialiser l'état
        self.current_client = None
        self.setProperty("hasClient", False)
        self.setProperty("isNew", False)
        self.style().polish(self)
        
        # Démarrer le timer pour la recherche
        if text.strip():
            self.search_timer.start(300)  # 300ms de délai
    
    def update_suggestions(self):
        """Met à jour les suggestions basées sur le texte actuel"""
        text = self.text().strip().lower()
        if not text:
            return
        
        # Filtrer les clients correspondants
        matching_clients = []
        for client in self.clients_data:
            name = client.get('nombre', '').lower()
            nif = client.get('nif', '').lower()
            
            if text in name or text in nif:
                matching_clients.append(client)
        
        # Mettre à jour les suggestions
        suggestions = []
        for client in matching_clients:
            name = client.get('nombre', '')
            nif = client.get('nif', '')
            
            if nif:
                suggestion = f"{name} ({nif})"
            else:
                suggestion = name
            
            suggestions.append(suggestion)
        
        # Mettre à jour le modèle du completer
        model = QStringListModel(suggestions)
        self.completer.setModel(model)
    
    def on_completion_selected(self, text):
        """Gère la sélection d'une suggestion"""
        # Extraire le nom du client de la suggestion
        client_name = text.split(' (')[0] if ' (' in text else text
        
        # Trouver le client correspondant
        for client in self.clients_data:
            if client.get('nombre', '') == client_name:
                self.current_client = client
                self.setProperty("hasClient", True)
                self.setProperty("isNew", False)
                self.style().polish(self)
                
                # Émettre le signal
                self.client_selected.emit(client)
                self.logger.info(f"Cliente seleccionado: {client_name}")
                break
    
    def on_editing_finished(self):
        """Gère la fin de l'édition"""
        text = self.text().strip()
        if not text:
            return

        # Vérifier si un client existant est sélectionné
        if self.current_client and self.current_client.get('nombre', '').lower() == text.lower():
            # Client déjà sélectionné et nom identique, ne rien faire
            return

        # Recharger les clients depuis la base pour avoir les données les plus récentes
        from database.database import db
        fresh_clients = db.get_all_clients()
        self.load_clients(fresh_clients)

        # Vérifier directement dans la base de données (priorité aux données complètes)
        from database.database import db
        existing_client = db.get_client_by_name(text)
        if existing_client:
            self.current_client = existing_client
            self.setProperty("hasClient", True)
            self.setProperty("isNew", False)
            self.style().polish(self)
            self.client_selected.emit(existing_client)
            self.logger.info(f"Cliente existente encontrado en base: {text} (ID: {existing_client['id']})")
            # Recharger les données pour inclure ce client
            fresh_clients = db.get_all_clients()
            self.load_clients(fresh_clients)
            return

        # Vérifier aussi dans la liste locale (fallback)
        for client in self.clients_data:
            if client.get('nombre', '').lower() == text.lower():
                self.current_client = client
                self.setProperty("hasClient", True)
                self.setProperty("isNew", False)
                self.style().polish(self)
                self.client_selected.emit(client)
                self.logger.info(f"Cliente existente seleccionado desde lista local: {text}")
                return

        # Aucun client existant trouvé - marquer comme nouveau
        self.setProperty("hasClient", False)
        self.setProperty("isNew", True)
        self.style().polish(self)

        # Créer automatiquement les données du nouveau client (une seule fois)
        if not hasattr(self, '_creating_client') or not self._creating_client:
            self._creating_client = True

            new_client_data = {
                'id': None,
                'nombre': text,
                'nif': '',
                'direccion': '',
                'telefono': '',
                'email': '',
                'is_new': True
            }

            # Émettre le signal de création de client
            self.client_created.emit(new_client_data)
            self.logger.info(f"Nuevo cliente detectado y creado: {text}")

            # Réinitialiser le flag après un délai
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, lambda: setattr(self, '_creating_client', False))
    
    def get_current_client(self):
        """Retourne le client actuel ou None"""
        return self.current_client
    
    def get_client_data_for_invoice(self):
        """Retourne les données client pour la facture"""
        text = self.text().strip()
        if not text:
            return None
        
        if self.current_client:
            # Client existant
            return self.current_client
        else:
            # Nouveau client - créer les données de base
            new_client_data = {
                'id': None,  # Sera assigné lors de la sauvegarde
                'nombre': text,
                'nif': '',
                'direccion': '',
                'telefono': '',
                'email': '',
                'is_new': True  # Marquer comme nouveau
            }
            return new_client_data
    
    def create_new_client_dialog(self):
        """Ouvre un dialogue pour créer un nouveau client"""
        text = self.text().strip()
        if not text:
            return None
        
        dialog = NewClientDialog(text, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            client_data = dialog.get_client_data()
            
            # Ajouter à la liste des clients
            self.clients_data.append(client_data)
            self.update_completer_model()
            
            # Sélectionner le nouveau client
            self.current_client = client_data
            self.setProperty("hasClient", True)
            self.setProperty("isNew", False)
            self.style().polish(self)
            
            # Émettre le signal
            self.client_created.emit(client_data)
            self.logger.info(f"Nuevo cliente creado: {client_data['nombre']}")
            
            return client_data
        
        return None
    
    def clear_selection(self):
        """Efface la sélection actuelle"""
        self.current_client = None
        self.clear()
        self.setProperty("hasClient", False)
        self.setProperty("isNew", False)
        self.style().polish(self)


class NewClientDialog(QDialog):
    """Dialogue pour créer un nouveau client"""
    
    def __init__(self, client_name, parent=None):
        super().__init__(parent)
        self.client_name = client_name
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue"""
        self.setWindowTitle("Nuevo Cliente")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel(f"Crear nuevo cliente: {self.client_name}")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Formulaire
        form_layout = QFormLayout()
        
        self.nombre_edit = QLineEdit(self.client_name)
        form_layout.addRow("Nombre:", self.nombre_edit)
        
        self.nif_edit = QLineEdit()
        self.nif_edit.setPlaceholderText("NIF/CIF (opcional)")
        form_layout.addRow("NIF/CIF:", self.nif_edit)
        
        self.direccion_edit = QTextEdit()
        self.direccion_edit.setMaximumHeight(80)
        self.direccion_edit.setPlaceholderText("Dirección (opcional)")
        form_layout.addRow("Dirección:", self.direccion_edit)
        
        self.telefono_edit = QLineEdit()
        self.telefono_edit.setPlaceholderText("Teléfono (opcional)")
        form_layout.addRow("Teléfono:", self.telefono_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email (opcional)")
        form_layout.addRow("Email:", self.email_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_client_data(self):
        """Retourne les données du client"""
        return {
            'id': None,  # Sera assigné lors de la sauvegarde en base
            'nombre': self.nombre_edit.text().strip(),
            'nif': self.nif_edit.text().strip(),
            'direccion': self.direccion_edit.toPlainText().strip(),
            'telefono': self.telefono_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'is_new': True
        }
