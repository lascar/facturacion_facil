# -*- coding: utf-8 -*-
"""
Dialogues personnalisés avec PyQt6
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QTextEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from utils.logger import get_logger

class CopyableMessageDialog:
    """Dialogue de message avec texte sélectionnable et copiable"""
    
    def __init__(self, parent, title, message, dialog_type="info"):
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog_type = dialog_type
        self.result = None
        self.logger = get_logger("custom_dialog")
        
        self.create_dialog()
        self.create_widgets()
        self.setup_focus()
    
    def create_dialog(self):
        """Crée la fenêtre de dialogue"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("500x300")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrer sur le parent
        if self.parent:
            self.dialog.geometry(f"+{self.parent.winfo_rootx() + 50}+{self.parent.winfo_rooty() + 50}")
    
    def create_widgets(self):
        """Crée les widgets du dialogue"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Zone de texte sélectionnable
        self.message_textbox = ctk.CTkTextbox(
            main_frame,
            height=150,
            font=ctk.CTkFont(size=11, family="Consolas")
        )
        self.message_textbox.pack(fill="both", expand=True, pady=(0, 15))
        self.message_textbox.insert("1.0", self.message)
        self.message_textbox.configure(state="disabled")
        
        # Frame pour les boutons
        self.create_buttons()
    
    def create_buttons(self):
        """Crée les boutons du dialogue"""
        buttons_frame = ctk.CTkFrame(self.dialog)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Bouton Copier
        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copier",
            command=self.copy_message,
            width=100,
            height=35,
            fg_color="#FF4444",
            hover_color="#FF6666"
        )
        copy_btn.pack(side="left", padx=10, pady=10)
        
        # Bouton OK
        ok_btn = ctk.CTkButton(
            buttons_frame,
            text="OK",
            command=self.ok_clicked,
            width=80,
            height=35
        )
        ok_btn.pack(side="right", padx=10, pady=10)
    
    def setup_focus(self):
        """Configure le focus du dialogue"""
        self.dialog.lift()
        self.dialog.focus()
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def copy_message(self):
        """Copie le message dans le presse-papiers"""
        try:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(self.message)
            self.dialog.update()
            self.logger.info("Mensaje copiado al portapapeles")
        except Exception as e:
            self.logger.error(f"Error copiando mensaje: {e}")
    
    def ok_clicked(self):
        """Gère le clic sur OK"""
        self.result = "ok"
        self.dialog.destroy()
    
    def on_close(self):
        """Gère la fermeture du dialogue"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Affiche le dialogue et attend la réponse"""
        try:
            self.dialog.wait_window()
        except tk.TclError:
            pass  # Normal si la fenêtre est fermée
        return self.result

class CopyableConfirmDialog(CopyableMessageDialog):
    """Dialogue de confirmation avec texte copiable"""
    
    def __init__(self, parent, title, message):
        super().__init__(parent, title, message, "warning")
        self.result = None
    
    def create_buttons(self):
        """Crée les boutons de confirmation"""
        buttons_frame = ctk.CTkFrame(self.dialog)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Bouton Copier
        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copier",
            command=self.copy_message,
            width=100,
            height=35,
            fg_color="#FF4444",
            hover_color="#FF6666"
        )
        copy_btn.pack(side="left", padx=10, pady=10)
        
        # Bouton Non
        no_btn = ctk.CTkButton(
            buttons_frame,
            text="No",
            command=self.no_clicked,
            width=80,
            height=35,
            fg_color="#666666",
            hover_color="#888888"
        )
        no_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # Bouton Sí
        yes_btn = ctk.CTkButton(
            buttons_frame,
            text="Sí",
            command=self.yes_clicked,
            width=80,
            height=35
        )
        yes_btn.pack(side="right", padx=5, pady=10)
    
    def yes_clicked(self):
        """Gère le clic sur Sí"""
        self.result = True
        self.dialog.destroy()
    
    def no_clicked(self):
        """Gère le clic sur No"""
        self.result = False
        self.dialog.destroy()

# Fonctions de conveniencia
def show_copyable_info(parent, title, message):
    """Muestra un diálogo de información con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "info")
    return dialog.show()

def show_copyable_error(parent, title, message):
    """Muestra un diálogo de error con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "error")
    return dialog.show()

def show_copyable_warning(parent, title, message):
    """Muestra un diálogo de advertencia con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "warning")
    return dialog.show()

def show_copyable_success(parent, title, message):
    """Muestra un diálogo de éxito con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "success")
    return dialog.show()

def show_copyable_confirm(parent, title, message):
    """Muestra un diálogo de confirmación con texto copiable"""
    dialog = CopyableConfirmDialog(parent, title, message)
    return dialog.show()

def show_stock_confirmation_dialog(parent, title, message):
    """Muestra un diálogo específico para confirmación de stock con botones claros"""
    dialog = CopyableConfirmDialog(parent, title, message)
    return dialog.show()
