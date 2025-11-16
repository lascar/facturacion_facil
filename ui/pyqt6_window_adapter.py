#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptateur pour les fenêtres secondaires avec PyQt6
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QMainWindow

class PyQt6WindowAdapter:
    """Adaptateur pour faire fonctionner les fenêtres CustomTkinter avec un parent PyQt6"""

    def __init__(self, pyqt6_parent):
        """
        Crée un adaptateur pour un parent PyQt6

        Args:
            pyqt6_parent: Instance de QMainWindow (notre MainWindow PyQt6)
        """
        self.pyqt6_parent = pyqt6_parent

        # Créer un widget Tkinter racine caché pour la compatibilité
        self._create_hidden_tkinter_root()

        # Créer un objet tk factice pour la compatibilité
        self.tk = self._create_tk_mock()

        # Ajouter les attributs internes Tkinter nécessaires
        self._setup_tkinter_attributes()

    def _create_hidden_tkinter_root(self):
        """Crée un widget Tkinter racine caché pour la compatibilité"""
        try:
            import tkinter as tk

            # Créer une fenêtre Tkinter cachée
            self._hidden_root = tk.Tk()
            self._hidden_root.withdraw()  # Cacher la fenêtre
            self._hidden_root.title("Hidden Root for PyQt6 Adapter")

            # Utiliser cette racine comme master
            self.master = self._hidden_root

        except Exception as e:
            print(f"Avertissement: Impossible de créer la racine Tkinter cachée: {e}")
            self.master = None
            self._hidden_root = None

    def _setup_tkinter_attributes(self):
        """Configure les attributs internes Tkinter nécessaires"""
        # Attributs pour la gestion des widgets enfants
        self._last_child_ids = None
        self.children = {}

        # Attributs pour la gestion des noms de widgets
        self._name = "pyqt6_adapter"
        self._w = f".{self._name}"

        # Attributs pour la gestion des options (ne pas écraser master s'il existe)
        if not hasattr(self, 'master'):
            self.master = None
        self._tclCommands = []

        # Attributs pour la compatibilité avec CustomTkinter
        self._appearance_mode = "system"
        self._fg_color = None
        self._corner_radius = 0

        # Attributs pour les événements
        self._bindings = {}

        # Attributs pour la géométrie
        self._geometry_manager = None
        self._grid_info = {}
        self._pack_info = {}
        self._place_info = {}

    def _create_tk_mock(self):
        """Crée un objet tk factice pour la compatibilité"""
        class TkMock:
            def __init__(self, parent):
                self.parent = parent
                self._commands = {}
                self._command_counter = 0

            def call(self, *args):
                """Mock de la méthode call de Tkinter"""
                pass

            def createcommand(self, name, func):
                """Crée une commande Tcl"""
                if name is None:
                    name = f"pyqt6_cmd_{self._command_counter}"
                    self._command_counter += 1
                self._commands[name] = func
                return name

            def deletecommand(self, name):
                """Supprime une commande Tcl"""
                if name in self._commands:
                    del self._commands[name]

            def eval(self, script):
                """Évalue un script Tcl (mock)"""
                return ""

            def evalfile(self, filename):
                """Évalue un fichier Tcl (mock)"""
                return ""

            def split(self, string):
                """Divise une chaîne Tcl"""
                return string.split()

            def splitlist(self, string):
                """Divise une liste Tcl"""
                if string is None:
                    return []
                if isinstance(string, (list, tuple)):
                    return list(string)
                if hasattr(string, 'split'):
                    return string.split()
                return [str(string)]

            def winfo_x(self):
                """Position X de la fenêtre"""
                return self.parent.x()

            def winfo_y(self):
                """Position Y de la fenêtre"""
                return self.parent.y()

            def winfo_width(self):
                """Largeur de la fenêtre"""
                return self.parent.width()

            def winfo_height(self):
                """Hauteur de la fenêtre"""
                return self.parent.height()

            def getvar(self, name):
                """Obtient une variable Tcl"""
                return ""

            def setvar(self, name, value):
                """Définit une variable Tcl"""
                pass

            def unsetvar(self, name):
                """Supprime une variable Tcl"""
                pass

            def getint(self, value):
                """Convertit une valeur en entier"""
                try:
                    return int(float(str(value)))
                except (ValueError, TypeError):
                    return 0

            def getdouble(self, value):
                """Convertit une valeur en float"""
                try:
                    return float(str(value))
                except (ValueError, TypeError):
                    return 0.0

            def getboolean(self, value):
                """Convertit une valeur en booléen"""
                if isinstance(value, bool):
                    return value
                if isinstance(value, (int, float)):
                    return bool(value)
                if isinstance(value, str):
                    return value.lower() in ('1', 'true', 'yes', 'on')
                return False

        return TkMock(self.pyqt6_parent)
    
    def winfo_x(self):
        """Position X de la fenêtre"""
        return self.pyqt6_parent.x()
    
    def winfo_y(self):
        """Position Y de la fenêtre"""
        return self.pyqt6_parent.y()
    
    def winfo_width(self):
        """Largeur de la fenêtre"""
        return self.pyqt6_parent.width()
    
    def winfo_height(self):
        """Hauteur de la fenêtre"""
        return self.pyqt6_parent.height()
    
    def geometry(self, geom_string=None):
        """Gestion de la géométrie de la fenêtre"""
        if geom_string:
            # Parser la chaîne de géométrie (ex: "800x600+100+100")
            if '+' in geom_string:
                size_part, pos_part = geom_string.split('+', 1)
                if 'x' in size_part:
                    width, height = map(int, size_part.split('x'))
                    self.pyqt6_parent.resize(width, height)
                
                if '+' in pos_part:
                    x, y = map(int, pos_part.split('+'))
                    self.pyqt6_parent.move(x, y)
            elif 'x' in geom_string:
                width, height = map(int, geom_string.split('x'))
                self.pyqt6_parent.resize(width, height)
        else:
            # Retourner la géométrie actuelle
            return f"{self.pyqt6_parent.width()}x{self.pyqt6_parent.height()}+{self.pyqt6_parent.x()}+{self.pyqt6_parent.y()}"
    
    def title(self, title=None):
        """Gestion du titre de la fenêtre"""
        if title:
            self.pyqt6_parent.setWindowTitle(title)
        else:
            return self.pyqt6_parent.windowTitle()
    
    def transient(self, parent=None):
        """Rendre la fenêtre transiente (modal)"""
        # En PyQt6, ceci est géré différemment
        pass
    
    def lift(self):
        """Amener la fenêtre au premier plan"""
        self.pyqt6_parent.raise_()
        self.pyqt6_parent.activateWindow()
    
    def focus_force(self):
        """Forcer le focus sur la fenêtre"""
        self.pyqt6_parent.activateWindow()
    
    def destroy(self):
        """Détruire la fenêtre"""
        self.pyqt6_parent.close()
    
    def withdraw(self):
        """Cacher la fenêtre"""
        self.pyqt6_parent.hide()
    
    def deiconify(self):
        """Afficher la fenêtre"""
        self.pyqt6_parent.show()
    
    def state(self, new_state=None):
        """Gestion de l'état de la fenêtre"""
        if new_state:
            if new_state == 'normal':
                self.pyqt6_parent.showNormal()
            elif new_state == 'iconic':
                self.pyqt6_parent.showMinimized()
            elif new_state == 'zoomed':
                self.pyqt6_parent.showMaximized()
        else:
            if self.pyqt6_parent.isMinimized():
                return 'iconic'
            elif self.pyqt6_parent.isMaximized():
                return 'zoomed'
            else:
                return 'normal'
    
    def protocol(self, protocol, callback):
        """Gestion des protocoles de fenêtre"""
        if protocol == "WM_DELETE_WINDOW":
            # En PyQt6, on utilise closeEvent
            def closeEvent(event):
                callback()
                event.accept()
            self.pyqt6_parent.closeEvent = closeEvent
    
    def bind(self, event, callback):
        """Liaison d'événements (mock)"""
        pass
    
    def after(self, delay, callback):
        """Exécution différée (mock)"""
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(delay, callback)

    def nametowidget(self, name):
        """Retourne un widget par son nom (mock)"""
        return self.children.get(name, self)

    def winfo_children(self):
        """Retourne la liste des widgets enfants"""
        return list(self.children.values())

    def winfo_parent(self):
        """Retourne le parent du widget"""
        return ""

    def winfo_toplevel(self):
        """Retourne le widget toplevel"""
        return self

    def winfo_class(self):
        """Retourne la classe du widget"""
        return "PyQt6Adapter"

    def winfo_name(self):
        """Retourne le nom du widget"""
        return self._name

    def winfo_pathname(self, winid):
        """Retourne le chemin d'un widget par son ID"""
        return self._w

    def register(self, func, subst=None, needcleanup=1):
        """Enregistre une fonction Tcl (mock)"""
        return f"PY_VAR{id(func)}"

    def call(self, *args):
        """Appel Tcl (mock)"""
        pass

    def _register(self, func, subst=None):
        """Enregistrement interne (mock)"""
        return self.register(func, subst)

    def _substitute(self, *args):
        """Substitution interne (mock)"""
        pass

    def _report_exception(self):
        """Rapport d'exception (mock)"""
        import traceback
        traceback.print_exc()

    def iconname(self, newName=None):
        """Gestion du nom d'icône"""
        if newName is not None:
            self._icon_name = newName
        return getattr(self, '_icon_name', 'PyQt6App')

    def wm_iconname(self, newName=None):
        """Alias pour iconname"""
        return self.iconname(newName)

    def winfo_screen(self):
        """Retourne l'écran"""
        return ":0.0"

    def winfo_screendepth(self):
        """Retourne la profondeur de l'écran"""
        return 24

    def winfo_screenheight(self):
        """Retourne la hauteur de l'écran"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        return screen.geometry().height() if screen else 1080

    def winfo_screenwidth(self):
        """Retourne la largeur de l'écran"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        return screen.geometry().width() if screen else 1920

    def winfo_screenmmheight(self):
        """Retourne la hauteur de l'écran en mm"""
        return int(self.winfo_screenheight() * 25.4 / 96)  # Approximation

    def winfo_screenmmwidth(self):
        """Retourne la largeur de l'écran en mm"""
        return int(self.winfo_screenwidth() * 25.4 / 96)  # Approximation

    def winfo_pixels(self, number):
        """Convertit une distance en pixels"""
        return int(float(number))

    def winfo_fpixels(self, number):
        """Convertit une distance en pixels (float)"""
        return float(number)

    def winfo_rgb(self, color):
        """Retourne les composantes RGB d'une couleur"""
        # Retourner une valeur par défaut
        return (65535, 65535, 65535)  # Blanc

    def winfo_atom(self, name):
        """Retourne l'ID d'un atome"""
        return hash(name) % 65536

    def winfo_atomname(self, id):
        """Retourne le nom d'un atome"""
        return f"atom_{id}"

    def cleanup(self):
        """Nettoie les ressources de l'adaptateur"""
        if hasattr(self, '_hidden_root') and self._hidden_root:
            try:
                self._hidden_root.destroy()
            except:
                pass
            self._hidden_root = None

def create_adapter_for_pyqt6_parent(pyqt6_parent):
    """
    Crée un adaptateur pour un parent PyQt6
    
    Args:
        pyqt6_parent: Instance de QMainWindow
        
    Returns:
        PyQt6WindowAdapter: Adaptateur compatible avec les fenêtres CustomTkinter
    """
    return PyQt6WindowAdapter(pyqt6_parent)
