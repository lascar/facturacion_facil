#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires spécifiques pour gestionnaires de fenêtres Linux
Résolution du problème de fenêtres en arrière-plan
"""

import os
import subprocess
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QWindow

def detect_window_manager():
    """Détecte le gestionnaire de fenêtres Linux"""
    try:
        # Vérifier les variables d'environnement
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        session = os.environ.get('XDG_SESSION_TYPE', '').lower()
        
        # Détection spécifique
        if 'kde' in desktop or 'plasma' in desktop:
            return 'kde'
        elif 'gnome' in desktop:
            return 'gnome'
        elif 'xfce' in desktop:
            return 'xfce'
        elif 'wayland' in session:
            return 'wayland'
        elif 'x11' in session:
            return 'x11'
        else:
            # Essayer de détecter via processus
            try:
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                if 'kwin' in result.stdout:
                    return 'kde'
                elif 'gnome-shell' in result.stdout:
                    return 'gnome'
                elif 'xfwm4' in result.stdout:
                    return 'xfce'
            except:
                pass
                
        return 'unknown'
    except:
        return 'unknown'

def get_window_id(widget):
    """Obtient l'ID de fenêtre native"""
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

def force_window_foreground_linux(widget):
    """Force une fenêtre au premier plan sur Linux avec techniques spécifiques"""
    wm = detect_window_manager()
    window_id = get_window_id(widget)
    
    print(f"🐧 Gestionnaire de fenêtres détecté: {wm}")
    print(f"🪟 ID de fenêtre: {window_id}")
    
    # Techniques PyQt5 standard
    try:
        widget.setWindowState(Qt.WindowActive)
        widget.show()
        widget.raise_()
        widget.activateWindow()
        widget.setFocus()
        QApplication.setActiveWindow(widget)
    except Exception as e:
        print(f"Erreur techniques PyQt5: {e}")
    
    # Techniques spécifiques au gestionnaire de fenêtres
    if window_id:
        try:
            if wm == 'kde':
                # KDE/KWin - Utiliser kwin_x11
                subprocess.run(['kwin_x11', '--replace'], timeout=1, capture_output=True)
                subprocess.run(['wmctrl', '-i', '-a', str(window_id)], timeout=1, capture_output=True)
            elif wm == 'gnome':
                # GNOME - Utiliser wmctrl et xdotool
                subprocess.run(['wmctrl', '-i', '-a', str(window_id)], timeout=1, capture_output=True)
                subprocess.run(['xdotool', 'windowactivate', str(window_id)], timeout=1, capture_output=True)
            elif wm == 'xfce':
                # XFCE - Utiliser wmctrl
                subprocess.run(['wmctrl', '-i', '-a', str(window_id)], timeout=1, capture_output=True)
            else:
                # Techniques génériques
                subprocess.run(['wmctrl', '-i', '-a', str(window_id)], timeout=1, capture_output=True)
                subprocess.run(['xdotool', 'windowactivate', str(window_id)], timeout=1, capture_output=True)
        except Exception as e:
            print(f"Erreur techniques système: {e}")
    
    # Forçage avec xprop si disponible
    if window_id:
        try:
            subprocess.run(['xprop', '-id', str(window_id), '-f', '_NET_ACTIVE_WINDOW', '32a', '-set', '_NET_ACTIVE_WINDOW', '1'], 
                         timeout=1, capture_output=True)
        except:
            pass

def install_window_tools():
    """Installe les outils nécessaires pour la gestion des fenêtres"""
    tools = ['wmctrl', 'xdotool', 'xprop']
    
    print("🔧 Vérification des outils de gestion de fenêtres...")
    
    missing_tools = []
    for tool in tools:
        try:
            subprocess.run(['which', tool], check=True, capture_output=True)
            print(f"✅ {tool} disponible")
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
            print(f"❌ {tool} manquant")
    
    if missing_tools:
        print(f"\n💡 Pour installer les outils manquants:")
        print(f"sudo apt install {' '.join(missing_tools)}")
        print(f"ou")
        print(f"sudo yum install {' '.join(missing_tools)}")
        return False
    
    return True

class LinuxWindowForegroundMixin:
    """Mixin spécialisé pour Linux avec techniques avancées"""
    
    def setup_linux_foreground_display(self):
        """Configuration spécialisée pour Linux"""
        # Détecter l'environnement
        wm = detect_window_manager()
        print(f"🐧 Configuration pour gestionnaire: {wm}")
        
        # Configuration des flags selon l'environnement
        if wm == 'wayland':
            # Wayland - Techniques limitées
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        else:
            # X11 - Techniques complètes
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)
        
        # Forçage immédiat
        self._linux_force_immediate()
        
        # Forçage retardé avec techniques système
        QTimer.singleShot(50, self._linux_force_system)
        QTimer.singleShot(100, self._linux_force_system)
        QTimer.singleShot(200, self._linux_force_system)
    
    def _linux_force_immediate(self):
        """Forçage immédiat avec techniques Linux"""
        try:
            # Techniques PyQt5
            self.setWindowState(Qt.WindowActive)
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()
            QApplication.setActiveWindow(self)
            
            # Forçage du processus des événements
            QApplication.processEvents()
            
        except Exception as e:
            print(f"Erreur forçage immédiat Linux: {e}")
    
    def _linux_force_system(self):
        """Forçage avec outils système Linux"""
        try:
            force_window_foreground_linux(self)
        except Exception as e:
            print(f"Erreur forçage système Linux: {e}")
    
    def show(self):
        """Override de show() avec forçage Linux automatique"""
        # Appeler la méthode show() originale
        super().show()
        
        # Forçage Linux immédiat
        self._linux_force_immediate()
        
        # Forçage système retardé
        QTimer.singleShot(25, self._linux_force_system)
        QTimer.singleShot(75, self._linux_force_system)

def test_linux_window_manager():
    """Test du gestionnaire de fenêtres Linux"""
    print("🐧 TEST GESTIONNAIRE DE FENÊTRES LINUX")
    print("=" * 50)
    
    wm = detect_window_manager()
    print(f"Gestionnaire détecté: {wm}")
    
    # Variables d'environnement
    print(f"XDG_CURRENT_DESKTOP: {os.environ.get('XDG_CURRENT_DESKTOP', 'Non défini')}")
    print(f"XDG_SESSION_TYPE: {os.environ.get('XDG_SESSION_TYPE', 'Non défini')}")
    print(f"DISPLAY: {os.environ.get('DISPLAY', 'Non défini')}")
    print(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'Non défini')}")
    
    # Test des outils
    tools_available = install_window_tools()
    print(f"Outils disponibles: {tools_available}")
    
    return wm, tools_available

if __name__ == "__main__":
    test_linux_window_manager()
