# -*- coding: utf-8 -*-
"""
Mixin simple pour affichage des dialogues au premier plan SANS GLITCH
Version simplifiée qui évite les changements de flags de fenêtre
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


class NoGlitchDialogForegroundMixin:
    """
    Mixin SIMPLE pour forcer les dialogues au premier plan sans glitch
    
    Évite les problèmes visuels causés par les changements de WindowFlags
    et les QTimer qui modifient l'apparence de la fenêtre après ouverture.
    """
    
    def setup_no_glitch_foreground_display(self):
        """
        Configuration SIMPLE pour affichage au premier plan sans glitch
        Fonctionne sur toutes les plateformes sans effets visuels indésirables
        """
        # Configuration des flags FIXES (pas de changement après ouverture)
        self.setWindowFlags(
            Qt.Window |                    # Fenêtre indépendante
            Qt.WindowCloseButtonHint |     # Bouton fermer
            Qt.WindowTitleHint             # Barre de titre
            # PAS de WindowStaysOnTopHint pour éviter le glitch
        )
        
        # Non-modal pour permettre l'accès aux autres fenêtres
        self.setModal(False)
        
        # Centrer sur l'écran
        self._no_glitch_center_on_screen()
    
    def _no_glitch_center_on_screen(self):
        """Centre la fenêtre sur l'écran"""
        try:
            screen = QApplication.desktop().screenGeometry()
            size = self.geometry()
            x = (screen.width() - size.width()) // 2
            y = (screen.height() - size.height()) // 2
            self.move(x, y)
        except:
            pass  # Ignore les erreurs de centrage
    
    def _no_glitch_force_foreground(self):
        """Forçage simple au premier plan sans modification de flags"""
        try:
            # Séquence de forçage standard SANS changement de flags
            self.setWindowState(Qt.WindowActive)
            self.raise_()
            self.activateWindow()
            self.setFocus()
            
            # Forçage du focus système
            QApplication.setActiveWindow(self)
            QApplication.processEvents()
        except:
            pass  # Ignore les erreurs
    
    def show(self):
        """Override SIMPLE de show() avec forçage automatique SANS GLITCH"""
        # Appeler la méthode show() originale
        super().show()
        
        # Forçage simple immédiat (sans modification de flags)
        self._no_glitch_force_foreground()
    
    def force_no_glitch_foreground_now(self):
        """Force immédiatement au premier plan - Méthode publique simple"""
        self._no_glitch_force_foreground()


def force_dialog_no_glitch_foreground(dialog):
    """Fonction utilitaire SIMPLE pour forcer un dialog au premier plan SANS GLITCH"""
    try:
        # Forçage simple sans modification de flags de fenêtre
        dialog.setWindowState(Qt.WindowActive)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        dialog.setFocus()
        QApplication.setActiveWindow(dialog)
        QApplication.processEvents()
        
        # Si le dialog a la méthode du mixin, l'utiliser
        if hasattr(dialog, 'force_no_glitch_foreground_now'):
            dialog.force_no_glitch_foreground_now()
            
    except Exception as e:
        print(f"Erreur forçage sans glitch: {e}")


# Exemple d'utilisation:
"""
# Méthode 1: Utiliser le mixin dans une classe
class MonDialog(QDialog, NoGlitchDialogForegroundMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mon Dialog")
        self.resize(400, 300)
        
        # Configurer l'affichage au premier plan SANS GLITCH
        self.setup_no_glitch_foreground_display()

# Méthode 2: Utiliser la fonction utilitaire
dialog = QDialog()
dialog.show()
force_dialog_no_glitch_foreground(dialog)
"""
