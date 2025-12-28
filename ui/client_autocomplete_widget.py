# -*- coding: utf-8 -*-
"""
Widget d'autocomplétion intelligent pour les clients avec création inline
"""

from PyQt5.QtWidgets import (
    QLineEdit, QCompleter, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QDialog, QDialogButtonBox, QFormLayout, QTextEdit,
    QWidget, QGroupBox, QGridLayout, QStyle
)
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal as Signal, QTimer
from PyQt5.QtGui import QFont

from utils.logger import get_logger
from database.database import db
from services.cliente_service import ClienteService
from utils.exceptions import ClientNotFoundError, DatabaseError

class ClientAutoCompleteWidget(QLineEdit):
    """Widget d'autocomplétion pour les clients avec création automatique"""
    
    # Signaux émis quand un client est sélectionné ou créé
    client_selected = Signal(dict)  # Client existant sélectionné
    client_created = Signal(dict)   # Nouveau client créé
    client_changed = Signal()       # Client changé (pour mise à jour UI)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)

        # Service métier
        db_path = db.db_path if hasattr(db, 'db_path') else None
        self.cliente_service = ClienteService(db_path)

        # Variables
        self.clients_data = []
        self.current_client = None
        self.is_creating_new = False
        
        # Configuration de base
        self.setPlaceholderText("Escriba el nombre del cliente...")
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

        # Configuration pour améliorer la réactivité
        self.completer.setMaxVisibleItems(10)
        self.completer.setCompletionColumn(0)

        # Connecter la sélection
        self.completer.activated.connect(self.on_completion_selected)
        self.setCompleter(self.completer)
    
    def setup_connections(self):
        """Configure les connexions de signaux"""
        self.textChanged.connect(self.on_text_changed)
        self.editingFinished.connect(self.on_editing_finished)

    def keyPressEvent(self, event):
        """Gérer les événements clavier pour améliorer l'autocomplétion"""
        # Si le completer est visible et qu'on appuie sur Tab ou Entrée
        if (self.completer and self.completer.popup().isVisible() and
            event.key() in (Qt.Key_Tab, Qt.Key_Return, Qt.Key_Enter)):

            # Sélectionner la suggestion actuelle
            current_completion = self.completer.currentCompletion()
            if current_completion:
                self.setText(current_completion)
                self.completer.popup().hide()
                self.on_completion_selected(current_completion)
                event.accept()
                return

        # Comportement par défaut
        super().keyPressEvent(event)
    
    def apply_style(self):
        """Applique le style au widget"""
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                color: #2c3e50;
                min-height: 25px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
            QLineEdit[hasClient="true"] {
                border-color: #27ae60;
                background-color: #eafaf1;
            }
            QLineEdit[isNew="true"] {
                border-color: #f39c12;
                background-color: #fef9e7;
            }
        """)
    
    def load_clients(self, clients_data):
        """Charge la liste des clients"""
        self.clients_data = clients_data
        self.update_completer_model()
        self.logger.info(f"Cargados {len(clients_data)} clientes para autocompletado")
    
    def update_completer_model(self):
        """Met à jour le modèle de l'autocomplétion"""
        if not self.clients_data:
            return
        
        # Créer la liste des suggestions
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
        """Gérer le changement de texte"""
        # Arrêter le timer précédent
        self.search_timer.stop()

        # Si le texte est vide, effacer le client actuel
        if not text.strip():
            if self.current_client is not None:
                self.current_client = None
                self.setProperty("hasClient", False)
                self.setProperty("isNew", False)
                self.style().polish(self)
                self.client_changed.emit()  # Informer que le client a changé
            return

        # Si on a un client sélectionné et que le texte ne correspond plus au nom du client
        if self.current_client and self.current_client.get('nombre', '') != text.strip():
            # Le texte a changé, on n'a plus de client sélectionné
            self.current_client = None
            self.setProperty("hasClient", False)
            self.setProperty("isNew", False)
            self.style().polish(self)
            self.client_changed.emit()  # Informer que le client a changé

        # Démarrer le timer pour la recherche
        if text.strip():
            self.search_timer.start(200)  # Réduire à 200ms pour plus de réactivité
    
    def perform_search(self):
        """Effectue la recherche de clients"""
        text = self.text().strip()
        if not text:
            # Si pas de texte, afficher tous les clients
            self.update_completer_model()
            return

        # Chercher dans les clients existants
        matching_clients = []
        text_lower = text.lower()

        for client in self.clients_data:
            name = client.get('nombre', '').lower()
            nif = client.get('nif', '').lower()

            # Recherche plus flexible : début du nom ou contenu
            if (name.startswith(text_lower) or
                text_lower in name or
                (nif and (nif.startswith(text_lower) or text_lower in nif))):
                matching_clients.append(client)

        # Trier les résultats : ceux qui commencent par le texte en premier
        matching_clients.sort(key=lambda c: (
            not c.get('nombre', '').lower().startswith(text_lower),
            c.get('nombre', '').lower()
        ))

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

        # Forcer l'affichage du popup si on a des suggestions
        if suggestions and self.hasFocus():
            self.completer.complete()
    
    def on_completion_selected(self, text):
        """Gérer la sélection d'une suggestion"""
        # Extraire le nom du client (avant les parenthèses)
        client_name = text.split(' (')[0].strip()

        # Trouver le client correspondant dans les données d'autocomplétion
        for client in self.clients_data:
            if client.get('nombre', '') == client_name:
                # Récupérer les données complètes via le service
                self.logger.info(f"Intentando cargar datos completos para cliente ID: {client['id']}")
                try:
                    full_client_data = self.cliente_service.get_cliente_by_id(client['id'])
                except (ClientNotFoundError, DatabaseError) as e:
                    self.logger.error(f"Error cargando cliente: {e}")
                    full_client_data = None

                if full_client_data:
                    # Utiliser les données complètes
                    self.current_client = full_client_data
                    self.logger.info(f"Datos completos cargados para: {client_name}")
                    self.logger.info(f"  Telefono: '{full_client_data.get('telefono', '')}'")
                    self.logger.info(f"  Email: '{full_client_data.get('email', '')}'")
                    self.logger.info(f"  Direccion: '{full_client_data.get('direccion', '')}'")
                else:
                    # Fallback avec les données partielles
                    self.current_client = client
                    self.logger.warning(f"No se pudieron cargar datos completos para: {client_name}")

                self.setProperty("hasClient", True)
                self.setProperty("isNew", False)
                self.style().polish(self)
                self.client_selected.emit(self.current_client)
                self.client_changed.emit()
                self.logger.info(f"Cliente seleccionado: {client_name} (ID: {self.current_client['id']})")
                return
    
    def on_editing_finished(self):
        """Gérer la fin d'édition"""
        text = self.text().strip()
        if not text:
            self.current_client = None
            self.setProperty("hasClient", False)
            self.setProperty("isNew", False)
            self.style().polish(self)
            self.client_changed.emit()
            return

        # Vérifier si c'est un client existant exact (nom complet ou suggestion)
        client_found = False

        # Recherche exacte par nom
        for client in self.clients_data:
            client_name = client.get('nombre', '')
            if client_name.lower() == text.lower():
                # Récupérer les données complètes via le service
                try:
                    full_client_data = self.cliente_service.get_cliente_by_id(client['id'])
                except (ClientNotFoundError, DatabaseError) as e:
                    self.logger.error(f"Error cargando cliente: {e}")
                    full_client_data = None

                if full_client_data:
                    self.current_client = full_client_data
                    self.logger.info(f"Datos completos cargados para: {client_name}")
                else:
                    self.current_client = client
                    self.logger.warning(f"No se pudieron cargar datos completos para: {client_name}")

                self.setProperty("hasClient", True)
                self.setProperty("isNew", False)
                self.style().polish(self)
                self.client_selected.emit(self.current_client)
                self.client_changed.emit()
                self.logger.info(f"Cliente existente seleccionado: {client_name}")
                client_found = True
                break

        # Si pas trouvé exactement, chercher dans les suggestions affichées
        if not client_found and hasattr(self.completer, 'model') and self.completer.model():
            model = self.completer.model()
            for i in range(model.rowCount()):
                suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
                if suggestion and suggestion.lower() == text.lower():
                    # Extraire le nom du client de la suggestion
                    client_name = suggestion.split(' (')[0].strip()
                    for client in self.clients_data:
                        if client.get('nombre', '') == client_name:
                            # Récupérer les données complètes via le service
                            try:
                                full_client_data = self.cliente_service.get_cliente_by_id(client['id'])
                            except (ClientNotFoundError, DatabaseError) as e:
                                self.logger.error(f"Error cargando cliente: {e}")
                                full_client_data = None

                            if full_client_data:
                                self.current_client = full_client_data
                                self.logger.info(f"Datos completos cargados desde sugerencia: {client_name}")
                            else:
                                self.current_client = client
                                self.logger.warning(f"No se pudieron cargar datos completos desde sugerencia: {client_name}")

                            self.setProperty("hasClient", True)
                            self.setProperty("isNew", False)
                            self.style().polish(self)
                            self.client_selected.emit(self.current_client)
                            self.client_changed.emit()
                            self.logger.info(f"Cliente seleccionado desde sugerencia: {client_name}")
                            client_found = True
                            break
                    if client_found:
                        break

        # Si toujours pas trouvé, créer un nouveau client
        if not client_found and not self.is_creating_new:
            self.is_creating_new = True
            self.setProperty("hasClient", False)
            self.setProperty("isNew", True)
            self.style().polish(self)

            # Créer les données du nouveau client
            new_client_data = {
                'id': None,
                'nombre': text,
                'nif': '',
                'direccion': '',
                'telefono': '',
                'email': '',
                'is_new': True
            }

            self.current_client = new_client_data
            self.client_created.emit(new_client_data)
            self.client_changed.emit()
            self.logger.info(f"Nuevo cliente detectado: {text}")

            # Réinitialiser le flag
            QTimer.singleShot(1000, lambda: setattr(self, 'is_creating_new', False))
    
    def get_current_client(self):
        """Retourne le client actuel"""
        return self.current_client
    
    def set_client(self, client):
        """Définit le client actuel"""
        if client:
            self.current_client = client
            self.setText(client.get('nombre', ''))
            self.setProperty("hasClient", True)
            self.setProperty("isNew", client.get('is_new', False))
            self.style().polish(self)
            self.client_changed.emit()
    
    def clear_client(self):
        """Efface le client actuel"""
        self.current_client = None
        self.clear()
        self.setProperty("hasClient", False)
        self.setProperty("isNew", False)
        self.style().polish(self)
        self.client_changed.emit()


class ClientDetailsWidget(QWidget):
    """Widget pour afficher et éditer les détails du client"""

    client_updated = Signal(dict)  # Client mis à jour
    client_saved = Signal(dict)    # Client sauvegardé
    client_changes_discarded = Signal(dict)  # Changements annulés

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.current_client = None
        self.original_client_data = None  # Données originales pour annuler
        self.has_changes = False
        self.setup_ui()
        self.hide()  # Caché par défaut

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # GroupBox pour les détails
        self.details_group = QGroupBox("Detalles del Cliente")
        details_layout = QGridLayout(self.details_group)

        # Champs d'édition
        self.nif_edit = QLineEdit()
        self.nif_edit.setPlaceholderText("NIF/CIF/DNI")

        self.telefono_edit = QLineEdit()
        self.telefono_edit.setPlaceholderText("Teléfono")

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")

        self.direccion_edit = QTextEdit()
        self.direccion_edit.setPlaceholderText("Dirección")
        self.direccion_edit.setMaximumHeight(80)

        # Ajouter au layout (2 lignes compactes)
        # Ligne 0: NIF + Teléfono + Email
        details_layout.addWidget(QLabel("NIF/CIF (opcional):"), 0, 0)
        details_layout.addWidget(self.nif_edit, 0, 1)

        details_layout.addWidget(QLabel("Teléfono (opcional):"), 0, 2)
        details_layout.addWidget(self.telefono_edit, 0, 3)

        details_layout.addWidget(QLabel("Email (opcional):"), 0, 4)
        details_layout.addWidget(self.email_edit, 0, 5)

        # Ligne 1: Dirección (toute la largeur)
        details_layout.addWidget(QLabel("Dirección (opcional):"), 1, 0)
        details_layout.addWidget(self.direccion_edit, 1, 1, 1, 5)

        layout.addWidget(self.details_group)

        # Boutons d'action
        self.buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(self.buttons_widget)
        buttons_layout.setContentsMargins(0, 5, 0, 0)

        # Bouton Guardar
        self.save_btn = QPushButton("Guardar")
        self.save_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.save_btn.clicked.connect(self.save_client)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)

        # Bouton Deshacer cambios
        self.discard_btn = QPushButton("Deshacer cambios")
        self.discard_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.discard_btn.clicked.connect(self.discard_changes)
        self.discard_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)

        # Ajouter les boutons au layout
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.discard_btn)
        buttons_layout.addStretch()

        layout.addWidget(self.buttons_widget)

        # Variable pour éviter les mises à jour pendant le chargement
        self.loading_data = False

        # Connecter les signaux pour détecter les changements
        self.nif_edit.textChanged.connect(self.on_data_changed)
        self.telefono_edit.textChanged.connect(self.on_data_changed)
        self.email_edit.textChanged.connect(self.on_data_changed)
        self.direccion_edit.textChanged.connect(self.on_data_changed)

        # Désactiver les boutons par défaut
        self.update_buttons_state()

    def show_client_details(self, client):
        """Affiche les détails du client"""
        self.current_client = client

        # Sauvegarder les données originales pour pouvoir annuler
        if client:
            self.original_client_data = {
                'nif': client.get('nif', ''),
                'telefono': client.get('telefono', ''),
                'email': client.get('email', ''),
                'direccion': client.get('direccion', '')
            }
        else:
            self.original_client_data = None

        if client:
            # Marquer qu'on est en train de charger pour éviter les mises à jour
            self.loading_data = True

            # Remplir les champs
            self.nif_edit.setText(client.get('nif', ''))
            self.telefono_edit.setText(client.get('telefono', ''))
            self.email_edit.setText(client.get('email', ''))
            self.direccion_edit.setPlainText(client.get('direccion', ''))

            # Réinitialiser l'état des changements
            # Pour un nouveau client, activer le bouton Guardar immédiatement
            self.has_changes = client.get('is_new', False)
            self.update_buttons_state()

            # Fin du chargement
            self.loading_data = False

            # Mettre à jour le titre
            if client.get('is_new', False):
                self.details_group.setTitle(f"Nuevo Cliente: {client.get('nombre', '')}")
                self.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #f39c12;
                        border: 2px solid #f39c12;
                        border-radius: 5px;
                        margin-top: 10px;
                        padding-top: 10px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px 0 5px;
                    }
                """)
            else:
                self.details_group.setTitle(f"Cliente: {client.get('nombre', '')}")
                self.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #27ae60;
                        border: 2px solid #27ae60;
                        border-radius: 5px;
                        margin-top: 10px;
                        padding-top: 10px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px 0 5px;
                    }
                """)

            self.show()
        else:
            self.hide()

    def on_data_changed(self):
        """Gérer les changements de données"""
        # Ne pas traiter les changements pendant le chargement des données
        if self.loading_data:
            return

        if self.current_client and self.original_client_data:
            # Vérifier s'il y a des changements
            current_data = {
                'nif': self.nif_edit.text().strip(),
                'telefono': self.telefono_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'direccion': self.direccion_edit.toPlainText().strip()
            }

            # Pour un nouveau client, toujours considérer qu'il y a des changements
            # pour garder le bouton Guardar activé
            if self.current_client.get('is_new', False):
                has_changes = True
            else:
                # Comparer avec les données originales pour un client existant
                has_changes = (
                    current_data['nif'] != self.original_client_data['nif'] or
                    current_data['telefono'] != self.original_client_data['telefono'] or
                    current_data['email'] != self.original_client_data['email'] or
                    current_data['direccion'] != self.original_client_data['direccion']
                )

            if has_changes != self.has_changes:
                self.has_changes = has_changes
                self.update_buttons_state()

            # Mettre à jour les données du client temporairement
            self.current_client['nif'] = current_data['nif']
            self.current_client['telefono'] = current_data['telefono']
            self.current_client['email'] = current_data['email']
            self.current_client['direccion'] = current_data['direccion']

            # Émettre le signal de mise à jour
            self.client_updated.emit(self.current_client)

    def get_client_data(self):
        """Retourne les données du client"""
        if self.current_client:
            return {
                'id': self.current_client.get('id'),
                'nombre': self.current_client.get('nombre', ''),
                'nif': self.nif_edit.text().strip(),
                'telefono': self.telefono_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'direccion': self.direccion_edit.toPlainText().strip(),
                'is_new': self.current_client.get('is_new', False)
            }
        return None

    def update_buttons_state(self):
        """Met à jour l'état des boutons selon les changements"""
        # Activer/désactiver les boutons selon s'il y a des changements
        self.save_btn.setEnabled(self.has_changes)
        self.discard_btn.setEnabled(self.has_changes)

        # Mettre à jour le style du groupe selon l'état
        if self.current_client:
            if self.has_changes:
                # Style pour indiquer des changements non sauvegardés
                border_color = "#f39c12"  # Orange pour changements
                title_prefix = "* "  # Astérisque pour indiquer des changements
            else:
                # Style normal
                if self.current_client.get('is_new', False):
                    border_color = "#f39c12"  # Orange pour nouveau
                    title_prefix = ""
                else:
                    border_color = "#27ae60"  # Vert pour existant
                    title_prefix = ""

            client_name = self.current_client.get('nombre', '')
            if self.current_client.get('is_new', False):
                title = f"{title_prefix}Nuevo Cliente: {client_name}"
            else:
                title = f"{title_prefix}Cliente: {client_name}"

            self.details_group.setTitle(title)
            self.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: {border_color};
                    border: 2px solid {border_color};
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)

    def save_client(self):
        """Sauvegarder les changements du client"""
        if not self.current_client or not self.has_changes:
            return

        try:
            # Récupérer les données actuelles
            client_data = self.get_client_data()

            if client_data:
                # Mettre à jour les données originales
                self.original_client_data = {
                    'nif': client_data['nif'],
                    'telefono': client_data['telefono'],
                    'email': client_data['email'],
                    'direccion': client_data['direccion']
                }

                # Réinitialiser l'état des changements
                self.has_changes = False
                self.update_buttons_state()

                # Émettre le signal de sauvegarde
                self.client_saved.emit(client_data)
                self.logger.info(f"Cliente guardado: {client_data.get('nombre', '')}")

        except Exception as e:
            self.logger.error(f"Error al guardar cliente: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

    def discard_changes(self):
        """Annuler les changements et revenir aux données originales"""
        if not self.current_client or not self.has_changes or not self.original_client_data:
            return

        try:
            # Restaurer les données originales
            self.nif_edit.setText(self.original_client_data['nif'])
            self.telefono_edit.setText(self.original_client_data['telefono'])
            self.email_edit.setText(self.original_client_data['email'])
            self.direccion_edit.setPlainText(self.original_client_data['direccion'])

            # Mettre à jour les données du client
            self.current_client['nif'] = self.original_client_data['nif']
            self.current_client['telefono'] = self.original_client_data['telefono']
            self.current_client['email'] = self.original_client_data['email']
            self.current_client['direccion'] = self.original_client_data['direccion']

            # Réinitialiser l'état des changements
            self.has_changes = False
            self.update_buttons_state()

            # Émettre le signal d'annulation
            self.client_changes_discarded.emit(self.current_client)
            self.logger.info(f"Cambios descartados para cliente: {self.current_client.get('nombre', '')}")

        except Exception as e:
            self.logger.error(f"Error al descartar cambios: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

    def clear(self):
        """Efface les détails"""
        self.current_client = None
        self.original_client_data = None
        self.has_changes = False
        self.nif_edit.clear()
        self.telefono_edit.clear()
        self.email_edit.clear()
        self.direccion_edit.clear()
        self.update_buttons_state()
        self.hide()
