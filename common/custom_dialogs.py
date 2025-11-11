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
        print(f"🔍 DEBUG: CopyableMessageDialog.__init__ - type: {dialog_type}, title: {title}")
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog_type = dialog_type  # info, error, warning, success
        self.result = None
        self.logger = get_logger("custom_dialog")

        print("🔍 DEBUG: Iniciando creación de diálogo...")
        
        # Créer la fenêtre de dialogue
        try:
            print("🔍 DEBUG: Creando CTkToplevel...")
            self.dialog = ctk.CTkToplevel(parent)
            print("🔍 DEBUG: CTkToplevel creado exitosamente")

            self.dialog.title(title)
            self.dialog.geometry("500x300")
            if parent:
                self.dialog.transient(parent)
            print("🔍 DEBUG: Configuración básica del diálogo completada")
        except Exception as e:
            print(f"❌ DEBUG: Error creando CTkToplevel: {e}")
            raise
        
        # Configurer l'apparence selon le type
        try:
            print("🔍 DEBUG: Configurando apariencia del diálogo...")
            self.setup_dialog_appearance()
            print("🔍 DEBUG: Apariencia configurada exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error configurando apariencia: {e}")
            raise

        # Créer l'interface
        try:
            print("🔍 DEBUG: Creando widgets del diálogo...")
            self.create_widgets()
            print("🔍 DEBUG: Widgets creados exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error creando widgets: {e}")
            raise

        # Configurer le focus
        try:
            print("🔍 DEBUG: Configurando focus...")
            self.setup_focus()
            print("🔍 DEBUG: Focus configurado exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error configurando focus: {e}")
            raise

        print("✅ DEBUG: CopyableMessageDialog creado completamente")
    
    def setup_dialog_appearance(self):
        """Configure l'apparence selon le type de dialogue"""
        # Couleurs selon le type
        self.colors = {
            "info": {"fg": "#1f538d", "hover": "#14375e"},
            "success": {"fg": "#2E8B57", "hover": "#228B22"},
            "warning": {"fg": "#FF8C00", "hover": "#FF7F00"},
            "error": {"fg": "#DC143C", "hover": "#B22222"}
        }
        
        self.color = self.colors.get(self.dialog_type, self.colors["info"])
        
        # Icônes selon le type
        self.icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        self.icon = self.icons.get(self.dialog_type, "ℹ️")
    
    def create_widgets(self):
        """Crée les widgets du dialogue"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame d'en-tête avec icône et titre
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 20))
        
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
        try:
            print("🔍 DEBUG: Creando buttons_frame...")
            buttons_frame = ctk.CTkFrame(main_frame)
            buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
            print("✅ DEBUG: buttons_frame creado y empaquetado exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error creando buttons_frame: {e}")
            raise
        
        # Bouton copier - VERSIÓN FORZADA VISIBLE
        try:
            print("🔍 DEBUG: Creando botón copiar...")
            copy_btn = ctk.CTkButton(
                buttons_frame,
                text="📋 COPIAR",  # Texto más visible
                command=self.copy_message,
                width=120,  # Más ancho
                height=35,  # Más alto
                fg_color="#FF6B6B",  # Color rojo llamativo
                hover_color="#FF5252",  # Color hover rojo
                font=ctk.CTkFont(size=14, weight="bold")  # Fuente más grande y bold
            )
            copy_btn.pack(side="left", padx=15, pady=15)  # Más padding
            print("✅ DEBUG: Botón copiar creado exitosamente")

            # FORZAR ACTUALIZACIÓN Y VISIBILIDAD
            copy_btn.update()
            buttons_frame.update()
            print("🔍 DEBUG: Forzando actualización de widgets...")

            # Verificar que el botón existe
            print(f"🔍 DEBUG: Botón copiar existe: {copy_btn.winfo_exists()}")
            print(f"🔍 DEBUG: Botón copiar visible: {copy_btn.winfo_viewable()}")
            print(f"🔍 DEBUG: Botón copiar geometría: {copy_btn.winfo_geometry()}")

        except Exception as e:
            print(f"❌ DEBUG: Error creando botón copiar: {e}")
            import traceback
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            raise
        
        # Bouton OK
        try:
            print("🔍 DEBUG: Creando botón OK...")
            ok_btn = ctk.CTkButton(
                buttons_frame,
                text="OK",
                command=self.ok_clicked,
                width=100,
                height=30,
                fg_color=self.color["fg"],
                hover_color=self.color["hover"]
            )
            ok_btn.pack(side="right", padx=10, pady=10)
            print("✅ DEBUG: Botón OK creado exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error creando botón OK: {e}")
            raise
        
        # Focus sur le bouton OK
        ok_btn.focus()

        # DEBUG FINAL: Verificar estado de todos los widgets
        try:
            print("🔍 DEBUG: Verificación final de widgets...")
            print(f"🔍 DEBUG: main_frame existe: {main_frame.winfo_exists()}")
            print(f"🔍 DEBUG: buttons_frame existe: {buttons_frame.winfo_exists()}")
            print(f"🔍 DEBUG: buttons_frame hijos: {buttons_frame.winfo_children()}")

            # Forzar actualización completa
            self.dialog.update_idletasks()
            self.dialog.update()
            print("✅ DEBUG: Actualización completa forzada")

        except Exception as e:
            print(f"❌ DEBUG: Error en verificación final: {e}")
        
        # Bind Enter pour OK
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.ok_clicked())
    
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
            print("🔍 DEBUG: ok_clicked() llamado")
            self.result = True
            self._close_dialog_safely()
        except Exception as e:
            print(f"⚠️  DEBUG: Error en ok_clicked(): {e}")
            self._close_dialog_safely()

    def _close_dialog_safely(self):
        """Cierra el diálogo de forma segura"""
        try:
            if hasattr(self, 'dialog'):
                # Usar el gestor de ventanas para cerrar de forma segura
                success = window_manager.close_window_safely(self.dialog)
                if success:
                    print("🔍 DEBUG: Diálogo cerrado exitosamente con window_manager")
                else:
                    print("⚠️  DEBUG: Error cerrando diálogo con window_manager")
        except Exception as e:
            print(f"⚠️  DEBUG: Error cerrando diálogo: {e}")
            # Forzar cierre si hay error
            try:
                if hasattr(self, 'dialog'):
                    self.dialog.quit()
            except:
                pass
    
    def show(self):
        """Muestra el diálogo y retorna el resultado"""
        try:
            print("🔍 DEBUG: show() iniciado")

            # Verificar que el dialog existe
            if not hasattr(self, 'dialog') or not self.dialog.winfo_exists():
                print("❌ DEBUG: Dialog no existe o fue destruido")
                return None

            print(f"🔍 DEBUG: dialog estado: {self.dialog.state()}")

            # Configurar el protocolo de cierre para evitar bloqueos
            self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)

            # Usar el gestor de ventanas para hacer visible de forma segura
            self.dialog.deiconify()
            window_manager.make_window_visible(self.dialog, temporary_topmost=True, duration_ms=100)

            print("🔍 DEBUG: Diálogo configurado para ser visible")

            # Centrar en pantalla si no tiene parent
            if not self.parent:
                self.dialog.geometry("+300+200")
                print("🔍 DEBUG: Diálogo centrado en pantalla")

            print("🔍 DEBUG: Iniciando wait_window()...")

            # Verificar si estamos en modo headless o test
            if os.environ.get('HEADLESS_MODE') == '1':
                print("🔍 DEBUG: Modo headless detectado, simulando interacción")
                # En modo headless, simular clic en OK después de un breve delay
                self.dialog.after(100, lambda: self.ok_clicked())

            # Usar wait_window con timeout implícito
            try:
                self.dialog.wait_window()
            except tk.TclError as tcl_error:
                print(f"⚠️  DEBUG: TclError en wait_window (normal si se cerró): {tcl_error}")

            print("🔍 DEBUG: wait_window() completado")

            print(f"🔍 DEBUG: Resultado final: {self.result}")
            return self.result

        except Exception as e:
            print(f"❌ DEBUG: Error en show(): {e}")
            import traceback
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")

            # Limpiar en caso de error
            try:
                if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                    self.dialog.attributes('-topmost', False)
                    self.dialog.destroy()
            except:
                pass

            return None

    def _remove_topmost_safely(self):
        """Quita el atributo topmost de forma segura"""
        try:
            if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                self.dialog.attributes('-topmost', False)
                print("🔍 DEBUG: Topmost removido exitosamente")
        except Exception as e:
            print(f"⚠️  DEBUG: Error removiendo topmost: {e}")

    def on_close(self):
        """Maneja el cierre del diálogo"""
        try:
            print("🔍 DEBUG: on_close() llamado")
            self.result = None
            self._close_dialog_safely()
        except Exception as e:
            print(f"⚠️  DEBUG: Error en on_close(): {e}")
            self._close_dialog_safely()

class CopyableConfirmDialog(CopyableMessageDialog):
    """Dialogue de confirmation avec texte copiable"""
    
    def __init__(self, parent, title, message):
        super().__init__(parent, title, message, "warning")
        self.result = None
    
    def create_widgets(self):
        """Crée les widgets du dialogue de confirmation"""
        # Utiliser la méthode parent mais modifier les boutons
        super().create_widgets()
        
        # Remplacer les boutons par Oui/Non
        buttons_frame = None
        for widget in self.dialog.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkFrame):
                                # Chercher le frame des boutons
                                buttons = [w for w in grandchild.winfo_children() if isinstance(w, ctk.CTkButton)]
                                if len(buttons) >= 2:
                                    buttons_frame = grandchild
                                    break
        
        if buttons_frame:
            # Supprimer les boutons existants
            for widget in buttons_frame.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.destroy()
            
            # Bouton copier
            copy_btn = ctk.CTkButton(
                buttons_frame,
                text="📋 Copiar",
                command=self.copy_message,
                width=100,
                height=30,
                fg_color="gray",
                hover_color="darkgray"
            )
            copy_btn.pack(side="left", padx=10, pady=10)
            
            # Bouton Cancelar
            no_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Cancelar",
                command=self.no_clicked,
                width=120,
                height=35,
                fg_color="#DC143C",
                hover_color="#B22222",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            no_btn.pack(side="right", padx=(5, 10), pady=10)

            # Bouton Confirmación
            yes_btn = ctk.CTkButton(
                buttons_frame,
                text="✅ Confirmación",
                command=self.yes_clicked,
                width=120,
                height=35,
                fg_color="#2E8B57",
                hover_color="#228B22",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            yes_btn.pack(side="right", padx=5, pady=10)
            
            # Focus sur Sí
            yes_btn.focus()
            
            # Bind teclas
            self.dialog.bind("<Return>", lambda e: self.yes_clicked())
            self.dialog.bind("<Escape>", lambda e: self.no_clicked())
    
    def yes_clicked(self):
        """Maneja el clic en Sí"""
        try:
            print("🔍 DEBUG: yes_clicked() llamado")
            self.result = True
            self._close_dialog_safely()
        except Exception as e:
            print(f"⚠️  DEBUG: Error en yes_clicked(): {e}")
            self._close_dialog_safely()

    def no_clicked(self):
        """Maneja el clic en No"""
        try:
            print("🔍 DEBUG: no_clicked() llamado")
            self.result = False
            self._close_dialog_safely()
        except Exception as e:
            print(f"⚠️  DEBUG: Error en no_clicked(): {e}")
            self._close_dialog_safely()

class StockConfirmationDialog(CopyableMessageDialog):
    """Dialogue spécifique pour confirmation de stock avec boutons très clairs"""

    def __init__(self, parent, title, message):
        super().__init__(parent, title, message, "warning")
        self.result = None

    def create_widgets(self):
        """Crée les widgets du dialogue de confirmation de stock"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icône et titre
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))

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
