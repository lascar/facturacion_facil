import customtkinter as ctk
from utils.translations import get_text
from ui.productos import ProductosWindow
from ui.organizacion import OrganizacionWindow
from ui.stock import StockWindow
from ui.facturas import FacturasWindow

class MainWindow:
    def __init__(self):
        # Configuración de CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Ventana principal
        self.root = ctk.CTk()
        self.root.title(get_text("app_title"))
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Centrar la ventana
        self.center_window()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Variables para ventanas secundarias
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Crea los widgets de la interfaz principal"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=get_text("app_title"),
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(30, 50))
        
        # Frame para los botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Configurar grid
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Botón Productos
        productos_btn = ctk.CTkButton(
            buttons_frame,
            text=get_text("productos"),
            font=ctk.CTkFont(size=18, weight="bold"),
            height=80,
            command=self.open_productos
        )
        productos_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Botón Organización
        organizacion_btn = ctk.CTkButton(
            buttons_frame,
            text=get_text("organizacion"),
            font=ctk.CTkFont(size=18, weight="bold"),
            height=80,
            command=self.open_organizacion
        )
        organizacion_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Botón Stock
        stock_btn = ctk.CTkButton(
            buttons_frame,
            text=get_text("stock"),
            font=ctk.CTkFont(size=18, weight="bold"),
            height=80,
            command=self.open_stock
        )
        stock_btn.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        
        # Botón Facturas
        facturas_btn = ctk.CTkButton(
            buttons_frame,
            text=get_text("facturas"),
            font=ctk.CTkFont(size=18, weight="bold"),
            height=80,
            command=self.open_facturas
        )
        facturas_btn.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        
        # Botón Nueva Factura (destacado)
        nueva_factura_btn = ctk.CTkButton(
            buttons_frame,
            text=get_text("nueva_factura"),
            font=ctk.CTkFont(size=20, weight="bold"),
            height=80,
            fg_color="#2E8B57",
            hover_color="#228B22",
            command=self.open_nueva_factura
        )
        nueva_factura_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Frame inferior para botón salir
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Botón Salir
        salir_btn = ctk.CTkButton(
            bottom_frame,
            text=get_text("salir"),
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="#DC143C",
            hover_color="#B22222",
            command=self.root.quit
        )
        salir_btn.pack(pady=10)
    
    def open_productos(self):
        """Abre la ventana de gestión de productos"""
        if self.productos_window is None or not self.productos_window.window.winfo_exists():
            self.productos_window = ProductosWindow(self.root)
        else:
            # Traer la ventana al frente y darle foco
            self.productos_window.window.lift()
            self.productos_window.window.focus_force()
            self.productos_window.window.attributes('-topmost', True)
            self.productos_window.window.attributes('-topmost', False)
    
    def open_organizacion(self):
        """Abre la ventana de configuración de organización"""
        if self.organizacion_window is None or not self.organizacion_window.window.winfo_exists():
            self.organizacion_window = OrganizacionWindow(self.root)
        else:
            # Traer la ventana al frente y darle foco
            self.organizacion_window.window.lift()
            self.organizacion_window.window.focus_force()
            self.organizacion_window.window.attributes('-topmost', True)
            self.organizacion_window.window.attributes('-topmost', False)
    
    def open_stock(self):
        """Abre la ventana de gestión de stock"""
        if self.stock_window is None or not self.stock_window.window.winfo_exists():
            self.stock_window = StockWindow(self.root)
        else:
            # Traer la ventana al frente y darle foco
            self.stock_window.window.lift()
            self.stock_window.window.focus_force()
            self.stock_window.window.attributes('-topmost', True)
            self.stock_window.window.attributes('-topmost', False)
    
    def open_facturas(self):
        """Abre la ventana de gestión de facturas"""
        if self.facturas_window is None or not self.facturas_window.window.winfo_exists():
            self.facturas_window = FacturasWindow(self.root)
        else:
            # Traer la ventana al frente y darle foco
            self.facturas_window.window.lift()
            self.facturas_window.window.focus_force()
            self.facturas_window.window.attributes('-topmost', True)
            self.facturas_window.window.attributes('-topmost', False)
    
    def open_nueva_factura(self):
        """Abre la ventana para crear una nueva factura"""
        if self.facturas_window is None or not self.facturas_window.window.winfo_exists():
            self.facturas_window = FacturasWindow(self.root, nueva_factura=True)
        else:
            self.facturas_window.window.lift()
            self.facturas_window.nueva_factura()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()
