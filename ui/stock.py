import customtkinter as ctk
from utils.translations import get_text
from database.models import Stock

class StockWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(get_text("gestion_stock"))
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        # Crear interfaz básica
        label = ctk.CTkLabel(self.window, text=get_text("gestion_stock"), 
                           font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        
        info_label = ctk.CTkLabel(self.window, text="Ventana de stock - En desarrollo")
        info_label.pack(pady=20)
