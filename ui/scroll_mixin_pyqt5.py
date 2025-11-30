# -*- coding: utf-8 -*-
"""
Mixin pour ajouter le support du scroll avec la molette de souris aux fenêtres PyQt5
"""

from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QWheelEvent
from utils.logger import get_logger


class ScrollableMixin:
    """
    Mixin qui ajoute le support du scroll avec la molette de souris aux fenêtres PyQt5.
    
    Usage:
    1. Hériter de cette classe en plus de la classe de base
    2. Appeler setup_scrollable_content() dans setup_ui()
    3. Ajouter le contenu au self.scrollable_widget au lieu du widget principal
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_logger = get_logger(f"{self.__class__.__name__}_Scroll")
        self.scroll_area = None
        self.scrollable_widget = None
        self.original_layout = None
        
    def setup_scrollable_content(self, enable_horizontal=False, enable_vertical=True):
        """
        Configure le contenu scrollable pour la fenêtre.
        
        Args:
            enable_horizontal (bool): Activer le scroll horizontal
            enable_vertical (bool): Activer le scroll vertical
        """
        try:
            # Créer la zone de scroll
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            
            # Configuration du scroll
            if enable_horizontal and enable_vertical:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            elif enable_vertical:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            elif enable_horizontal:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            # Créer le widget scrollable
            self.scrollable_widget = QWidget()
            self.scrollable_widget.setObjectName("scrollable_content")
            
            # Installer le filtre d'événements pour capturer les événements de scroll
            self.installEventFilter(self)
            self.scroll_area.installEventFilter(self)
            self.scrollable_widget.installEventFilter(self)
            
            # Configurer la zone de scroll
            self.scroll_area.setWidget(self.scrollable_widget)
            
            # Remplacer le layout principal par la zone de scroll
            if self.layout():
                # Sauvegarder le layout original s'il existe
                self.original_layout = self.layout()
                
            # Créer un nouveau layout principal qui contient la zone de scroll
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self.scroll_area)
            
            self.scroll_logger.debug("Zone de scroll configurée avec succès")
            
        except Exception as e:
            self.scroll_logger.error(f"Erreur lors de la configuration du scroll: {e}")
            
    def get_scrollable_layout(self):
        """
        Retourne le layout du widget scrollable où ajouter le contenu.
        Crée un layout vertical par défaut si aucun n'existe.
        """
        if not self.scrollable_widget:
            self.scroll_logger.warning("Widget scrollable non initialisé")
            return None
            
        if not self.scrollable_widget.layout():
            layout = QVBoxLayout(self.scrollable_widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            
        return self.scrollable_widget.layout()
        
    def eventFilter(self, obj, event):
        """
        Filtre les événements pour capturer les événements de scroll de la molette.
        """
        if event.type() == QEvent.Wheel and isinstance(event, QWheelEvent):
            # Vérifier si l'événement provient de notre fenêtre ou de ses enfants
            if (obj == self or 
                obj == self.scroll_area or 
                obj == self.scrollable_widget or
                self.is_child_of_scrollable(obj)):
                
                return self.handle_wheel_event(event)
                
        # Laisser passer les autres événements
        return super().eventFilter(obj, event) if hasattr(super(), 'eventFilter') else False
        
    def is_child_of_scrollable(self, widget):
        """Vérifie si un widget est un enfant du widget scrollable."""
        if not self.scrollable_widget:
            return False
            
        parent = widget.parent()
        while parent:
            if parent == self.scrollable_widget:
                return True
            parent = parent.parent()
        return False
        
    def handle_wheel_event(self, event):
        """
        Gère les événements de la molette de souris pour le scroll.
        """
        if not self.scroll_area:
            return False
            
        try:
            # Obtenir la direction du scroll
            delta = event.angleDelta().y()
            
            # Calculer le pas de scroll (plus fluide)
            scroll_step = -delta // 8  # Diviser par 8 pour un scroll plus fluide
            
            # Appliquer le scroll vertical
            vertical_bar = self.scroll_area.verticalScrollBar()
            if vertical_bar and vertical_bar.isVisible():
                new_value = vertical_bar.value() + scroll_step
                new_value = max(vertical_bar.minimum(), min(vertical_bar.maximum(), new_value))
                vertical_bar.setValue(new_value)
                
                # Accepter l'événement pour éviter qu'il soit propagé
                event.accept()
                return True
                
        except Exception as e:
            self.scroll_logger.error(f"Erreur lors du traitement de l'événement de scroll: {e}")
            
        return False
        
    def scroll_to_top(self):
        """Fait défiler vers le haut."""
        if self.scroll_area:
            self.scroll_area.verticalScrollBar().setValue(0)
            
    def scroll_to_bottom(self):
        """Fait défiler vers le bas."""
        if self.scroll_area:
            vertical_bar = self.scroll_area.verticalScrollBar()
            vertical_bar.setValue(vertical_bar.maximum())
