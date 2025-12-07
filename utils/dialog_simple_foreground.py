#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solution SIMPLE et MULTIPLATEFORME pour forcer les dialogs au premier plan
Fonctionne sur Windows, Linux, macOS sans détection d'environnement
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication

class SimpleDialogForegroundMixin:
    """
    Mixin SIMPLE pour forcer les dialogs au premier plan
    Solution multiplateforme sans complexité
    """
    
    def setup_simple_foreground_display(self):
        """
        Configuration SIMPLE pour affichage au premier plan
        Fonctionne sur toutes les plateformes
        """
        # Configuration des flags SIMPLES et universels
        self.setWindowFlags(
            Qt.Window |                    # Fenêtre indépendante
            Qt.WindowCloseButtonHint |     # Bouton fermer
            Qt.WindowTitleHint |           # Barre de titre
            Qt.WindowStaysOnTopHint        # TOUJOURS au premier plan
        )
        
        # Non-modal pour permettre l'accès aux autres fenêtres
        self.setModal(False)
        
        # Centrer sur l'écran
        self._simple_center_on_screen()
        
        # Forçage SIMPLE et immédiat
        self._simple_force_foreground()
        
        # Programmer la suppression du flag "always on top" après 3 secondes
        QTimer.singleShot(3000, self._remove_always_on_top)
    
    def _simple_center_on_screen(self):
        """Centre le dialog sur l'écran - Version simple"""
        try:
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
        except:
            pass  # Ignore les erreurs de centrage
    
    def _simple_force_foreground(self):
        """Forçage SIMPLE au premier plan - Multiplateforme"""
        try:
            # Technique 1: État actif
            self.setWindowState(Qt.WindowActive)
            
            # Technique 2: Séquence standard
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()
            
            # Technique 3: Focus application
            QApplication.setActiveWindow(self)
            
            # Technique 4: Traitement des événements
            QApplication.processEvents()
            
        except:
            pass  # Ignore les erreurs
    
    def _remove_always_on_top(self):
        """Retire le flag WindowStaysOnTopHint après affichage"""
        try:
            if self.isVisible():
                # Nouveaux flags sans WindowStaysOnTopHint
                self.setWindowFlags(
                    Qt.Window |
                    Qt.WindowCloseButtonHint |
                    Qt.WindowTitleHint
                )
                # Réafficher avec les nouveaux flags
                self.show()
                self.raise_()
                self.activateWindow()
        except:
            pass  # Ignore les erreurs
    
    def show(self):
        """Override SIMPLE de show() avec forçage automatique"""
        # Appeler la méthode show() originale
        super().show()
        
        # Forçage simple immédiat
        self._simple_force_foreground()
    
    def force_simple_foreground_now(self):
        """Force immédiatement au premier plan - Méthode publique simple"""
        self._simple_force_foreground()

def force_dialog_simple_foreground(dialog):
    """Fonction utilitaire SIMPLE pour forcer un dialog au premier plan"""
    try:
        # Forçage simple sans complexité
        dialog.setWindowState(Qt.WindowActive)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        dialog.setFocus()
        QApplication.setActiveWindow(dialog)
        QApplication.processEvents()
        
        # Si le dialog a la méthode du mixin, l'utiliser
        if hasattr(dialog, 'force_simple_foreground_now'):
            dialog.force_simple_foreground_now()
            
    except Exception as e:
        print(f"Erreur forçage simple: {e}")

if __name__ == "__main__":
    print("🔧 SOLUTION SIMPLE MULTIPLATEFORME")
    print("=" * 40)
    print("✅ Pas de détection d'environnement")
    print("✅ Flags PyQt5 universels")
    print("✅ WindowStaysOnTopHint temporaire (3s)")
    print("✅ Forçage simple et robuste")
    print("✅ Compatible Windows/Linux/macOS")
