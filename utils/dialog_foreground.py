#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaire pour forcer les dialogs au premier plan de manière robuste
Solution au problème: "la ventana de editar o nueva factura se abre en segundo plano"
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication
import os
import subprocess


def detect_linux_environment():
    """Détecte l'environnement Linux pour optimiser les techniques de forçage"""
    try:
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        session = os.environ.get('XDG_SESSION_TYPE', '').lower()

        return {
            'desktop': desktop,
            'session': session,
            'is_gnome': 'gnome' in desktop,
            'is_kde': 'kde' in desktop or 'plasma' in desktop,
            'is_wayland': 'wayland' in session,
            'is_x11': 'x11' in session
        }
    except:
        return {'desktop': 'unknown', 'session': 'unknown', 'is_gnome': False, 'is_kde': False, 'is_wayland': False, 'is_x11': False}

class DialogForegroundMixin:
    """Mixin pour forcer les dialogs au premier plan - Version Linux GNOME/X11 optimisée"""
    
    def setup_foreground_display(self, always_on_top_duration=1000):
        """
        Configure le dialog pour s'afficher au premier plan de manière garantie

        Args:
            always_on_top_duration (int): Durée en ms pour garder le flag "always on top"
        """
        # Étape 1: Configuration des flags de fenêtre pour priorité maximale
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowStaysOnTopHint |  # Temporaire pour forcer au premier plan
            Qt.WindowTitleHint
        )

        # Étape 2: Configuration non-modale pour permettre l'accès aux autres fenêtres
        self.setModal(False)

        # Étape 3: Centrer sur l'écran pour visibilité maximale
        self._center_on_screen()

        # Étape 4: Forçage immédiat au premier plan
        self._force_to_foreground_immediate()

        # Étape 5: Forçage retardé avec multiple tentatives
        self._schedule_delayed_foreground_forcing()

        # Étape 6: Retirer le flag "always on top" après la durée spécifiée
        QTimer.singleShot(always_on_top_duration, self._remove_always_on_top_flag)

    def force_to_foreground_now(self):
        """Force immédiatement le dialog au premier plan - Méthode publique"""
        self._force_to_foreground_immediate()
        self._schedule_delayed_foreground_forcing()

    def show(self):
        """Override de show() pour forcer automatiquement au premier plan"""
        # Appeler la méthode show() originale
        super().show()

        # Forcer immédiatement au premier plan après show()
        self._force_to_foreground_immediate()

        # Programmer des tentatives supplémentaires
        QTimer.singleShot(10, self._force_to_foreground_immediate)
        QTimer.singleShot(50, self._force_to_foreground_immediate)
        QTimer.singleShot(100, self._force_to_foreground_immediate)
    
    def _center_on_screen(self):
        """Centrer le dialog sur l'écran"""
        try:
            screen = QApplication.desktop().screenGeometry()
            self.move(
                (screen.width() - self.width()) // 2,
                (screen.height() - self.height()) // 2
            )
        except Exception:
            # Si le centrage échoue, continuer sans erreur
            pass
    
    def _force_to_foreground_immediate(self):
        """Forçage immédiat au premier plan avec toutes les techniques - Version agressive"""
        try:
            # Technique 1: Forcer l'état actif
            self.setWindowState(Qt.WindowActive)

            # Technique 2: Forçage agressif avec flags temporaires
            current_flags = self.windowFlags()
            self.setWindowFlags(current_flags | Qt.WindowStaysOnTopHint)

            # Technique 3: Afficher et forcer au premier plan
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()

            # Technique 4: Forcer l'état de fenêtre active (retire minimized si présent)
            self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

            # Technique 5: Forçage du focus système
            QApplication.setActiveWindow(self)

            # Technique 6: Restaurer les flags après un court délai
            QTimer.singleShot(50, lambda: self.setWindowFlags(current_flags) or self.show())

        except Exception as e:
            print(f"Erreur lors du forçage immédiat: {e}")
    
    def _schedule_delayed_foreground_forcing(self):
        """Programmer des tentatives de forçage au premier plan avec délais"""
        # Multiple tentatives avec délais croissants pour s'assurer du succès
        delays = [25, 50, 100, 150, 200, 300, 500]
        
        for delay in delays:
            QTimer.singleShot(delay, self._force_to_foreground_delayed)
    
    def _force_to_foreground_delayed(self):
        """Forcer au premier plan avec vérification de visibilité"""
        if self.isVisible():
            self.raise_()
            self.activateWindow()
            self.setFocus()
            self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    
    def _remove_always_on_top_flag(self):
        """Retirer le flag 'always on top' tout en gardant le dialog au premier plan"""
        if self.isVisible():
            # Retirer le flag WindowStaysOnTopHint
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowCloseButtonHint |
                Qt.WindowMinimizeButtonHint |
                Qt.WindowTitleHint
            )
            
            # Réafficher avec les nouveaux flags
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()


def force_dialog_to_foreground(dialog, always_on_top_duration=1000):
    """
    Fonction utilitaire pour forcer un dialog existant au premier plan
    
    Args:
        dialog: Le dialog à forcer au premier plan
        always_on_top_duration (int): Durée en ms pour garder le flag "always on top"
    """
    if not dialog or not hasattr(dialog, 'setWindowFlags'):
        return
    
    # Appliquer la même logique que le mixin
    dialog.setWindowFlags(
        Qt.Window |
        Qt.WindowCloseButtonHint |
        Qt.WindowMinimizeButtonHint |
        Qt.WindowStaysOnTopHint |
        Qt.WindowTitleHint
    )
    
    dialog.setModal(False)
    
    # Centrer sur l'écran
    try:
        screen = QApplication.desktop().screenGeometry()
        dialog.move(
            (screen.width() - dialog.width()) // 2,
            (screen.height() - dialog.height()) // 2
        )
    except Exception:
        pass
    
    # Forçage immédiat
    dialog.setWindowState(Qt.WindowActive)
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    dialog.setFocus()
    dialog.setWindowState(dialog.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    
    # Forçage retardé
    delays = [25, 50, 100, 150, 200, 300, 500]
    for delay in delays:
        QTimer.singleShot(delay, lambda: _delayed_force(dialog))
    
    # Retirer le flag "always on top" après la durée spécifiée
    QTimer.singleShot(always_on_top_duration, lambda: _remove_always_on_top(dialog))


def _delayed_force(dialog):
    """Fonction helper pour le forçage retardé"""
    if dialog and dialog.isVisible():
        dialog.raise_()
        dialog.activateWindow()
        dialog.setFocus()
        dialog.setWindowState(dialog.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)


def _remove_always_on_top(dialog):
    """Fonction helper pour retirer le flag always on top"""
    if dialog and dialog.isVisible():
        dialog.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowTitleHint
        )
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        dialog.setFocus()


# Exemple d'utilisation:
"""
# Méthode 1: Utiliser le mixin dans une classe
class MonDialog(QDialog, DialogForegroundMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mon Dialog")
        self.resize(400, 300)
        
        # Configurer l'affichage au premier plan
        self.setup_foreground_display()

# Méthode 2: Utiliser la fonction utilitaire
dialog = QDialog()
dialog.setWindowTitle("Mon Dialog")
dialog.resize(400, 300)
force_dialog_to_foreground(dialog)
"""
