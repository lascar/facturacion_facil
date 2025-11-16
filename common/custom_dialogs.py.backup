# -*- coding: utf-8 -*-
"""
Dialogues personnalisés avec texte sélectionnable et copiable
"""
import customtkinter as ctk
import tkinter as tk
import os
from tkinter import messagebox
from utils.logger import get_logger
from utils.window_manager import window_manager

class CopyableMessageDialog:
    """Dialogue de message avec texte sélectionnable et copiable"""
    
    def __init__(self, parent, title, message, dialog_type="info"):
        # DEBUG désactivé
        
        # Icône
        icon_label = ctk.CTkLabel(
            header_frame,
            text=self.icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(10, 5))
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.color["fg"]
        )
        title_label.pack(side="left", padx=(5, 10))
        
        # Frame pour le message
        message_frame = ctk.CTkFrame(main_frame)
        message_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Label d'instruction
        instruction_label = ctk.CTkLabel(
            message_frame,
            text="📋 Mensaje (seleccionable y copiable):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        instruction_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Textbox pour le message (sélectionnable et copiable)
        self.message_textbox = ctk.CTkTextbox(
            message_frame,
            height=120,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        self.message_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Insérer le message
        self.message_textbox.insert("1.0", self.message)
        
        # Rendre le texte en lecture seule mais sélectionnable
        self.message_textbox.configure(state="disabled")
        
        # Frame pour les boutons
        self.create_buttons()

    def setup_focus(self):
        """Configure le focus du dialogue"""
        try:
            self.dialog.lift()
            self.dialog.focus_force()
            self.dialog.attributes('-topmost', True)
            self.dialog.grab_set()  # Modal
            
            # Centrer le dialogue
            self.center_dialog()
            
            # Retirer topmost après un moment
            self.dialog.after(500, lambda: self.dialog.attributes('-topmost', False))
            
        except Exception as e:
            self.logger.error(f"Error configurando focus: {e}")
    
    def center_dialog(self):
        """Centre le dialogue par rapport au parent"""
        try:
            self.dialog.update_idletasks()
            
            # Dimensions du dialogue
            dialog_width = self.dialog.winfo_width()
            dialog_height = self.dialog.winfo_height()
            
            if self.parent:
                # Position relative au parent
                parent_x = self.parent.winfo_x()
                parent_y = self.parent.winfo_y()
                parent_width = self.parent.winfo_width()
                parent_height = self.parent.winfo_height()
                
                x = parent_x + (parent_width // 2) - (dialog_width // 2)
                y = parent_y + (parent_height // 2) - (dialog_height // 2)
            else:
                # Centrer sur l'écran
                screen_width = self.dialog.winfo_screenwidth()
                screen_height = self.dialog.winfo_screenheight()
                
                x = (screen_width // 2) - (dialog_width // 2)
                y = (screen_height // 2) - (dialog_height // 2)
            
            # Assurer que le dialogue reste dans l'écran
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            
            x = max(0, min(x, screen_width - dialog_width))
            y = max(0, min(y, screen_height - dialog_height))
            
            self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
        except Exception as e:
            self.logger.error(f"Error centrando diálogo: {e}")
    
    def copy_message(self):
        """Copie le message dans le presse-papiers"""
        try:
            # Copier dans le presse-papiers
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(self.message)
            self.dialog.update()  # Assurer que la copie est effective
            
            # Feedback visuel temporaire
            self.show_copy_feedback()
            
            self.logger.info("Mensaje copiado al portapapeles")
            
        except Exception as e:
            self.logger.error(f"Error copiando mensaje: {e}")
            # Fallback avec messagebox standard
            messagebox.showinfo("Copiar", "Mensaje copiado al portapapeles", parent=self.dialog)
    
    def show_copy_feedback(self):
        """Muestra feedback visual de que se copió el mensaje"""
        # Cambiar temporalmente el texto del botón
        copy_btn = None
        for widget in self.dialog.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkButton) and "Copiar" in grandchild.cget("text"):
                                copy_btn = grandchild
                                break
        
        if copy_btn:
            original_text = copy_btn.cget("text")
            copy_btn.configure(text="✅ Copiado")
            self.dialog.after(1500, lambda: copy_btn.configure(text=original_text))
    
    def ok_clicked(self):
        """Maneja el clic en OK"""
        try:
            # DEBUG désactivé

            # Usar wait_window con timeout implícito
            try:
                self.dialog.wait_window()
            except tk.TclError as tcl_error:
                print(f"⚠️  DEBUG: TclError en wait_window (normal si se cerró): {tcl_error}")

            # DEBUG désactivé
            self.dialog.bind("<Escape>", lambda e: self.no_clicked())
    
    def yes_clicked(self):
        """Maneja el clic en Sí"""
        try:
            # DEBUG désactivé

        icon_label = ctk.CTkLabel(
            header_frame,
            text="📦",
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(10, 5))

        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.color["text"]
        )
        title_label.pack(side="left", padx=5)

        # Área de texto scrollable y seleccionable
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.text_widget = ctk.CTkTextbox(
            text_frame,
            height=200,
            font=ctk.CTkFont(size=11, family="Consolas"),
            wrap="word"
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Insertar el mensaje
        self.text_widget.insert("1.0", self.message)
        self.text_widget.configure(state="disabled")  # Solo lectura pero seleccionable

        # Frame de botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))

        # Botón Copiar (izquierda)
        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copiar",
            command=self.copy_message,
            width=100,
            height=35,
            fg_color="gray",
            hover_color="darkgray",
            font=ctk.CTkFont(size=11)
        )
        copy_btn.pack(side="left", padx=15, pady=10)

        # Botón CANCELAR (derecha)
        cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ CANCELAR",
            command=self.cancelar_clicked,
            width=140,
            height=40,
            fg_color="#DC143C",
            hover_color="#B22222",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        cancelar_btn.pack(side="right", padx=(5, 15), pady=10)

        # Botón CONFIRMAR (derecha)
        confirmar_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ CONFIRMAR",
            command=self.confirmar_clicked,
            width=140,
            height=40,
            fg_color="#2E8B57",
            hover_color="#228B22",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        confirmar_btn.pack(side="right", padx=5, pady=10)

        # Focus en CONFIRMAR por defecto
        confirmar_btn.focus()

        # Bind teclas
        self.dialog.bind("<Return>", lambda e: self.confirmar_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancelar_clicked())

    def confirmar_clicked(self):
        """Maneja el clic en CONFIRMAR"""
        self.result = True
        self.dialog.destroy()

    def cancelar_clicked(self):
        """Maneja el clic en CANCELAR"""
        self.result = False
        self.dialog.destroy()

    def copy_message(self):
        """Copie le message dans le presse-papiers"""
        try:
            # Copier dans le presse-papiers
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(self.message)
            self.dialog.update()

            # Feedback visuel
            self.logger.info("Mensaje de stock copiado al portapapeles")

        except Exception as e:
            self.logger.error(f"Error copiando mensaje de stock: {e}")

# Funciones de conveniencia
def show_copyable_info(parent, title, message):
    """Muestra un diálogo de información con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "info")
    return dialog.show()

def show_copyable_success(parent, title, message):
    """Muestra un diálogo de éxito con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "success")
    return dialog.show()

def show_copyable_warning(parent, title, message):
    """Muestra un diálogo de advertencia con texto copiable"""
    try:
        print(f"🔍 DEBUG: show_copyable_warning llamada - parent: {parent}, title: {title}")
        dialog = CopyableMessageDialog(parent, title, message, "warning")
        print("🔍 DEBUG: CopyableMessageDialog creado exitosamente")
        print("🔍 DEBUG: Llamando a dialog.show()...")
        result = dialog.show()
        print(f"🔍 DEBUG: dialog.show() completado - resultado: {result}")
        print("✅ DEBUG: show_copyable_warning terminado exitosamente")
        return result
    except Exception as e:
        print(f"❌ DEBUG: Error en show_copyable_warning: {e}")
        import traceback
        print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
        # Fallback a messagebox estándar
        import tkinter.messagebox as messagebox
        print("⚠️  DEBUG: Usando fallback messagebox")
        return messagebox.showwarning(title, message, parent=parent)

def show_copyable_error(parent, title, message):
    """Muestra un diálogo de error con texto copiable"""
    dialog = CopyableMessageDialog(parent, title, message, "error")
    return dialog.show()

def show_copyable_confirm(parent, title, message):
    """Muestra un diálogo de confirmación con texto copiable"""
    dialog = CopyableConfirmDialog(parent, title, message)
    return dialog.show()

def show_stock_confirmation_dialog(parent, title, message):
    """Muestra un diálogo específico para confirmación de stock con botones claros"""
    dialog = StockConfirmationDialog(parent, title, message)
    return dialog.show()
