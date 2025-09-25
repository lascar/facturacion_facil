# -*- coding: utf-8 -*-
"""
Ventana de configuración para numeración de facturas
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from utils.translations import get_text
from utils.logger import get_logger

logger = get_logger(__name__)
from utils.factura_numbering import factura_numbering_service
from common.ui_components import FormHelper

class ConfiguracionFacturasDialog:
    """Diálogo para configurar la numeración de facturas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        # Crear ventana modal
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Configuración de Numeración de Facturas")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.resizable(False, False)
        
        # Variables
        self.numero_inicial_var = tk.StringVar()
        self.prefijo_var = tk.StringVar()
        self.sufijo_var = tk.StringVar()
        self.serie_personalizada_var = tk.StringVar()
        
        self.create_widgets()
        self.load_current_config()
        
        # Hacer modal
        self.dialog.update_idletasks()
        self.dialog.grab_set()
        self.dialog.lift()
        self.dialog.focus_force()
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Configuración de Numeración de Facturas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de configuración
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Número inicial
        numero_frame = ctk.CTkFrame(config_frame)
        numero_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(numero_frame, text="Número inicial:").pack(anchor="w")
        self.numero_inicial_entry = ctk.CTkEntry(
            numero_frame, 
            textvariable=self.numero_inicial_var,
            placeholder_text="Ej: 1, 100, 1000"
        )
        self.numero_inicial_entry.pack(fill="x", pady=(5, 0))
        
        # Prefijo
        prefijo_frame = ctk.CTkFrame(config_frame)
        prefijo_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(prefijo_frame, text="Prefijo (opcional):").pack(anchor="w")
        self.prefijo_entry = ctk.CTkEntry(
            prefijo_frame, 
            textvariable=self.prefijo_var,
            placeholder_text="Ej: FAC-, FACT"
        )
        self.prefijo_entry.pack(fill="x", pady=(5, 0))
        
        # Sufijo
        sufijo_frame = ctk.CTkFrame(config_frame)
        sufijo_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(sufijo_frame, text="Sufijo (opcional):").pack(anchor="w")
        self.sufijo_entry = ctk.CTkEntry(
            sufijo_frame,
            textvariable=self.sufijo_var,
            placeholder_text="Ej: -2024, /ES"
        )
        self.sufijo_entry.pack(fill="x", pady=(5, 0))

        # Separador
        separator = ctk.CTkLabel(main_frame, text="─" * 50, text_color="gray")
        separator.pack(pady=10)

        # Sección de serie personalizada
        serie_label = ctk.CTkLabel(
            main_frame,
            text="O establecer una nueva serie personalizada:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        serie_label.pack(pady=(10, 5))

        serie_frame = ctk.CTkFrame(main_frame)
        serie_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(serie_frame, text="Número inicial de nueva serie:").pack(anchor="w")
        self.serie_personalizada_entry = ctk.CTkEntry(
            serie_frame,
            textvariable=self.serie_personalizada_var,
            placeholder_text="Ej: FAC-100, FACT-001, 500"
        )
        self.serie_personalizada_entry.pack(fill="x", pady=(5, 10))

        # Botón para establecer nueva serie
        establecer_serie_btn = ctk.CTkButton(
            serie_frame,
            text="Establecer Nueva Serie",
            command=self.establecer_nueva_serie,
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        establecer_serie_btn.pack(pady=5)
        
        # Vista previa
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(preview_frame, text="Vista previa:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.preview_label = ctk.CTkLabel(
            preview_frame, 
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("gray10", "gray90")
        )
        self.preview_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Información adicional
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_text = """Información:
• El número inicial se usa solo para nuevas facturas
• Si introduces un número personalizado, el siguiente se basará en ese número
• Los prefijos y sufijos son opcionales
• Ejemplo: Con prefijo "FAC-" y número 123 → "FAC-0123" """
        
        info_label = ctk.CTkLabel(
            info_frame, 
            text=info_text,
            justify="left",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(anchor="w", padx=20, pady=10)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x")
        
        ctk.CTkButton(
            button_frame, 
            text="Cancelar",
            command=self.cancel,
            width=100
        ).pack(side="right", padx=(10, 20), pady=20)
        
        ctk.CTkButton(
            button_frame, 
            text="Guardar",
            command=self.save_config,
            width=100
        ).pack(side="right", pady=20)
        
        # Vincular eventos para vista previa
        self.numero_inicial_var.trace('w', self.update_preview)
        self.prefijo_var.trace('w', self.update_preview)
        self.sufijo_var.trace('w', self.update_preview)
    
    def load_current_config(self):
        """Cargar la configuración actual"""
        try:
            config = factura_numbering_service.get_configuracion_numeracion()
            
            self.numero_inicial_var.set(str(config.get("numero_inicial", 1)))
            self.prefijo_var.set(config.get("prefijo", ""))
            self.sufijo_var.set(config.get("sufijo", ""))
            
            self.update_preview()
            
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
    
    def update_preview(self, *args):
        """Actualizar la vista previa del formato con año al final"""
        try:
            from datetime import datetime

            numero_inicial = self.numero_inicial_var.get() or "1"
            prefijo = self.prefijo_var.get()
            year = datetime.now().year

            # Formatear número con ceros a la izquierda (3 dígitos para el nuevo formato)
            try:
                numero = int(numero_inicial)
                numero_formateado = str(numero).zfill(3)
            except ValueError:
                numero_formateado = "001"

            # Construir vista previa con año al final
            if prefijo:
                preview = f"{prefijo}-{numero_formateado}-{year}"
            else:
                preview = f"{numero_formateado}-{year}"

            self.preview_label.configure(text=f"Próxima factura: {preview}")

        except Exception as e:
            logger.debug(f"Error actualizando vista previa: {e}")
            self.preview_label.configure(text="Vista previa no disponible")
    
    def save_config(self):
        """Guardar la configuración"""
        try:
            # Validar número inicial
            numero_inicial_str = self.numero_inicial_var.get().strip()
            if not numero_inicial_str:
                messagebox.showerror("Error", "El número inicial es obligatorio")
                return
            
            try:
                numero_inicial = int(numero_inicial_str)
                if numero_inicial <= 0:
                    messagebox.showerror("Error", "El número inicial debe ser mayor que 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "El número inicial debe ser un número válido")
                return
            
            # Obtener valores
            prefijo = self.prefijo_var.get().strip()
            sufijo = self.sufijo_var.get().strip()
            
            # Guardar configuración
            success = factura_numbering_service.set_configuracion_numeracion(
                numero_inicial=numero_inicial,
                prefijo=prefijo,
                sufijo=sufijo
            )
            
            if success:
                self.result = True
                messagebox.showinfo("Éxito", "Configuración guardada correctamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Error al guardar la configuración")
                
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def establecer_nueva_serie(self):
        """Establecer una nueva serie de numeración personalizada"""
        try:
            numero_serie = self.serie_personalizada_var.get().strip()

            if not numero_serie:
                messagebox.showerror("Error", "Debe ingresar un número para la nueva serie")
                return

            # Usar el servicio de numeración para establecer la nueva serie
            success, message = factura_numbering_service.set_nueva_serie_numeracion(numero_serie)

            if success:
                messagebox.showinfo("Éxito", message)
                # Limpiar el campo de serie personalizada
                self.serie_personalizada_var.set("")
                # Actualizar la configuración mostrada
                self.load_current_config()
            else:
                messagebox.showerror("Error", message)

        except Exception as e:
            logger.error(f"Error estableciendo nueva serie: {e}")
            messagebox.showerror("Error", f"Error al establecer nueva serie: {str(e)}")

    def cancel(self):
        """Cancelar el diálogo"""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Mostrar el diálogo y esperar resultado"""
        self.dialog.wait_window()
        return self.result
