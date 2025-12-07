#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaire spécialisé pour forcer les dialogs au premier plan sur Linux
Solution optimisée pour GNOME/X11 sans outils externes
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

def get_window_id(widget):
    """Obtient l'ID de fenêtre native pour les outils système"""
    try:
        if hasattr(widget, 'winId'):
            return widget.winId()
        elif hasattr(widget, 'windowHandle'):
            handle = widget.windowHandle()
            if handle:
                return handle.winId()
    except:
        pass
    return None

def try_system_focus(widget):
    """Essaie d'utiliser les outils système pour forcer le focus"""
    window_id = get_window_id(widget)
    if not window_id:
        return False
    
    try:
        # Essayer xprop (généralement disponible)
        subprocess.run(['xprop', '-id', str(window_id), '-f', '_NET_ACTIVE_WINDOW', '32a', '-set', '_NET_ACTIVE_WINDOW', '1'], 
                     timeout=0.5, capture_output=True, check=False)
        return True
    except:
        pass
    
    try:
        # Essayer wmctrl si disponible
        subprocess.run(['wmctrl', '-i', '-a', str(window_id)], timeout=0.5, capture_output=True, check=False)
        return True
    except:
        pass
    
    try:
        # Essayer xdotool si disponible
        subprocess.run(['xdotool', 'windowactivate', str(window_id)], timeout=0.5, capture_output=True, check=False)
        return True
    except:
        pass
    
    return False

class LinuxDialogForegroundMixin:
    """Mixin spécialisé pour forcer les dialogs au premier plan sur Linux"""
    
    def setup_linux_foreground_display(self, always_on_top_duration=2000):
        """
        Configure le dialog pour s'afficher au premier plan - Version Linux optimisée
        
        Args:
            always_on_top_duration (int): Durée en ms pour garder le flag "always on top"
        """
        # Détecter l'environnement Linux
        env = detect_linux_environment()
        print(f"🐧 Environnement Linux: {env['desktop']} / {env['session']}")
        
        # Configuration des flags selon l'environnement
        if env['is_gnome'] and env['is_x11']:
            # GNOME/X11 - Configuration spécialisée avec flags agressifs
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowCloseButtonHint |
                Qt.WindowStaysOnTopHint |  # Essentiel pour GNOME
                Qt.WindowTitleHint |
                Qt.WindowSystemMenuHint |
                Qt.WindowMaximizeButtonHint
            )
        elif env['is_wayland']:
            # Wayland - Flags limités
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowCloseButtonHint |
                Qt.WindowTitleHint
            )
        else:
            # Configuration générique pour autres environnements
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowCloseButtonHint |
                Qt.WindowStaysOnTopHint |
                Qt.WindowTitleHint
            )
        
        # Configuration non-modale
        self.setModal(False)
        
        # Centrage sur l'écran
        self._center_on_screen()
        
        # Forçage immédiat avec techniques Linux
        self._linux_force_immediate(env)
        
        # Programmer des tentatives multiples avec délais croissants
        delays = [25, 50, 100, 200, 300, 500, 750, 1000]
        for i, delay in enumerate(delays):
            QTimer.singleShot(delay, lambda env=env: self._linux_force_immediate(env))
        
        # Retirer le flag "always on top" après délai
        if always_on_top_duration > 0:
            QTimer.singleShot(always_on_top_duration, self._remove_always_on_top_flag)
    
    def _center_on_screen(self):
        """Centre le dialog sur l'écran"""
        try:
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
        except Exception as e:
            print(f"Erreur centrage: {e}")
    
    def _linux_force_immediate(self, env):
        """Forçage immédiat avec techniques Linux optimisées"""
        try:
            # Technique 1: États de fenêtre PyQt5
            self.setWindowState(Qt.WindowActive)
            self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
            
            # Technique 2: Séquence de forçage standard
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()
            
            # Technique 3: Forçage du focus système PyQt5
            QApplication.setActiveWindow(self)
            
            # Technique 4: Forcer le traitement des événements
            QApplication.processEvents()
            
            # Technique 5: Essayer les outils système si disponibles
            if env['is_x11']:  # Seulement sur X11
                try_system_focus(self)
            
        except Exception as e:
            print(f"Erreur forçage Linux: {e}")
    
    def _remove_always_on_top_flag(self):
        """Retire le flag WindowStaysOnTopHint après forçage"""
        try:
            current_flags = self.windowFlags()
            new_flags = current_flags & ~Qt.WindowStaysOnTopHint
            self.setWindowFlags(new_flags)
            self.show()  # Réafficher avec les nouveaux flags
        except Exception as e:
            print(f"Erreur suppression flag: {e}")
    
    def show(self):
        """Override de show() avec forçage Linux automatique"""
        # Appeler la méthode show() originale
        super().show()
        
        # Forçage Linux immédiat
        env = detect_linux_environment()
        self._linux_force_immediate(env)
        
        # Forçage supplémentaire retardé
        QTimer.singleShot(50, lambda: self._linux_force_immediate(env))
        QTimer.singleShot(150, lambda: self._linux_force_immediate(env))
    
    def force_to_foreground_now(self):
        """Force immédiatement le dialog au premier plan - Méthode publique Linux"""
        env = detect_linux_environment()
        self._linux_force_immediate(env)
        
        # Tentatives supplémentaires
        QTimer.singleShot(25, lambda: self._linux_force_immediate(env))
        QTimer.singleShot(75, lambda: self._linux_force_immediate(env))

# Fonction utilitaire pour compatibilité
def force_dialog_to_foreground_linux(dialog):
    """Force un dialog au premier plan avec techniques Linux"""
    if hasattr(dialog, 'force_to_foreground_now'):
        dialog.force_to_foreground_now()
    else:
        # Fallback pour dialogs sans mixin
        env = detect_linux_environment()
        try:
            dialog.setWindowState(Qt.WindowActive)
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()
            dialog.setFocus()
            QApplication.setActiveWindow(dialog)
            QApplication.processEvents()
            
            if env['is_x11']:
                try_system_focus(dialog)
        except Exception as e:
            print(f"Erreur forçage fallback: {e}")

if __name__ == "__main__":
    # Test de l'environnement
    env = detect_linux_environment()
    print("🐧 TEST ENVIRONNEMENT LINUX")
    print("=" * 40)
    print(f"Desktop: {env['desktop']}")
    print(f"Session: {env['session']}")
    print(f"GNOME: {env['is_gnome']}")
    print(f"KDE: {env['is_kde']}")
    print(f"Wayland: {env['is_wayland']}")
    print(f"X11: {env['is_x11']}")
