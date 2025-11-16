#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de compatibilité CustomTkinter pour PyQt6
"""

from gui import set_gui_framework
set_gui_framework('pyqt6')

# Réexporter l'adaptateur comme customtkinter
from gui.customtkinter_to_pyqt6_adapter import create_customtkinter_adapter

# Créer le module adapté
_ctk_adapter = create_customtkinter_adapter()

# Exporter toutes les classes
CTkToplevel = _ctk_adapter.CTkToplevel
CTkFrame = _ctk_adapter.CTkFrame
CTkScrollableFrame = _ctk_adapter.CTkScrollableFrame
CTkLabel = _ctk_adapter.CTkLabel
CTkButton = _ctk_adapter.CTkButton

# Fonctions de configuration
set_appearance_mode = _ctk_adapter.set_appearance_mode
set_default_color_theme = _ctk_adapter.set_default_color_theme

# Alias pour compatibilité
CTk = CTkToplevel  # Pour les fenêtres principales
