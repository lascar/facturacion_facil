#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de mensajes de error copiables en el diálogo de productos
Ejecutar: python test/demo/demo_producto_dialog_copyable_errors.py
"""
import sys
import os
import customtkinter as ctk
import tkinter as tk

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ui.producto_factura_dialog import ProductoFacturaDialog
from database.models import Producto
from common.custom_dialogs import show_copyable_error

class ProductoDialogErrorDemo:
    """Demostración de errores copiables en el diálogo de productos"""
    
    def __init__(self):
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("Demo: Errores Copiables en Diálogo de Productos")
        self.root.geometry("600x500")
        
        self.create_sample_data()
        self.create_widgets()
    
    def create_sample_data(self):
        """Crea datos de ejemplo si no existen"""
        try:
            # Verificar si ya hay productos
            productos_existentes = Producto.get_all()
            if len(productos_existentes) >= 3:
                print(f"✅ Ya existen {len(productos_existentes)} productos en la base de datos")
                return
            
            print("🔄 Creando productos de ejemplo...")
            
            # Productos de ejemplo
            productos_ejemplo = [
                {
                    'nombre': 'Laptop Demo Error',
                    'referencia': 'DEMO001',
                    'precio': 899.99,
                    'categoria': 'Informática',
                    'descripcion': 'Laptop para demo de errores',
                    'iva_recomendado': 21.0
                },
                {
                    'nombre': 'Mouse Demo Error',
                    'referencia': 'DEMO002',
                    'precio': 25.50,
                    'categoria': 'Periféricos',
                    'descripcion': 'Mouse para demo de errores',
                    'iva_recomendado': 21.0
                },
                {
                    'nombre': 'Teclado Demo Error',
                    'referencia': 'DEMO003',
                    'precio': 75.00,
                    'categoria': 'Periféricos',
                    'descripcion': 'Teclado para demo de errores',
                    'iva_recomendado': 21.0
                }
            ]
            
            # Crear productos
            for producto_data in productos_ejemplo:
                producto = Producto(**producto_data)
                producto.save()
                print(f"✅ Creado: {producto.nombre}")
            
            print(f"🎉 Creados {len(productos_ejemplo)} productos de ejemplo")
            
        except Exception as e:
            print(f"❌ Error creando datos de ejemplo: {e}")
    
    def create_widgets(self):
        """Crea la interfaz de la demostración"""
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🚨 Demo: Mensajes de Error Copiables",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Descripción
        description = ctk.CTkLabel(
            self.root,
            text="Esta demo muestra cómo los mensajes de error en el diálogo\n"
                 "de productos ahora incluyen el botón '📋 Copiar' para facilitar\n"
                 "el reporte de errores y el soporte técnico.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        description.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sección de tests de error
        self.create_error_tests_section(main_frame)
        
        # Sección de información
        self.create_info_section(main_frame)
    
    def create_error_tests_section(self, parent):
        """Crea la sección de tests de error"""
        # Título de sección
        error_label = ctk.CTkLabel(
            parent,
            text="🧪 Tests de Errores Copiables",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        error_label.pack(pady=(10, 15))
        
        # Botón para test de validación
        validation_btn = ctk.CTkButton(
            parent,
            text="❌ Test Error de Validación",
            command=self.test_validation_error,
            fg_color="#dc3545",
            hover_color="#c82333",
            height=40,
            width=300
        )
        validation_btn.pack(pady=5)
        
        # Botón para test de error de procesamiento
        processing_btn = ctk.CTkButton(
            parent,
            text="⚠️ Test Error de Procesamiento",
            command=self.test_processing_error,
            fg_color="#fd7e14",
            hover_color="#e55a00",
            height=40,
            width=300
        )
        processing_btn.pack(pady=5)
        
        # Botón para test de diálogo normal
        normal_btn = ctk.CTkButton(
            parent,
            text="✅ Test Diálogo Normal",
            command=self.test_normal_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            height=40,
            width=300
        )
        normal_btn.pack(pady=5)
        
        # Botón para test de error directo
        direct_error_btn = ctk.CTkButton(
            parent,
            text="🔧 Test Error Directo",
            command=self.test_direct_error,
            fg_color="#6f42c1",
            hover_color="#5a2d91",
            height=40,
            width=300
        )
        direct_error_btn.pack(pady=5)
    
    def create_info_section(self, parent):
        """Crea la sección de información"""
        # Frame de información
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", pady=20)
        
        # Título de información
        info_title = ctk.CTkLabel(
            info_frame,
            text="📋 Características de los Mensajes Copiables",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        # Lista de características
        features_text = """
✨ Botón "📋 Copiar" para copiar el mensaje completo
🖱️ Texto seleccionable con el ratón
⌨️ Atajos de teclado (Ctrl+A, Ctrl+C)
🕒 Timestamp incluido en errores técnicos
💡 Sugerencias de solución en errores detallados
✅ Feedback visual al copiar ("✅ Copiado")
🛡️ Fallback a messagebox estándar si hay problemas
        """
        
        features_label = ctk.CTkLabel(
            info_frame,
            text=features_text.strip(),
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        features_label.pack(padx=10, pady=(5, 10))
        
        # Botón salir
        exit_btn = ctk.CTkButton(
            parent,
            text="❌ Salir",
            command=self.root.quit,
            fg_color="#6c757d",
            hover_color="#5a6268",
            width=150
        )
        exit_btn.pack(pady=10)
    
    def demo_validation_error(self):
        """Test de error de validación"""
        try:
            print("🧪 Iniciando test de error de validación...")
            
            # Crear diálogo sin productos (para forzar error)
            dialog = ProductoFacturaDialog(self.root, [])
            
            # Simular intento de aceptar sin seleccionar producto
            # Esto debería mostrar un error de validación copiable
            dialog.accept()
            
            # Limpiar
            if hasattr(dialog, 'dialog') and dialog.dialog.winfo_exists():
                dialog.dialog.destroy()
            
        except Exception as e:
            print(f"❌ Error en test de validación: {e}")
            # Mostrar error copiable como ejemplo
            show_copyable_error(
                self.root,
                "Error en Test de Validación",
                f"Error durante el test de validación:\n\n{str(e)}\n\nEste es un ejemplo de mensaje de error copiable."
            )
    
    def demo_processing_error(self):
        """Test de error de procesamiento"""
        try:
            print("🧪 Iniciando test de error de procesamiento...")
            
            # Mostrar directamente un error de procesamiento simulado
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            error_message = f"""Error al procesar datos del producto:

🔍 Detalles técnicos:
ValueError: Precio inválido - se esperaba un número positivo

💡 Posibles soluciones:
1. Verificar que todos los campos estén correctamente completados
2. Asegurar que el producto seleccionado sea válido
3. Comprobar que los valores numéricos sean correctos
4. Intentar cerrar y reabrir el diálogo

🕒 Timestamp: {timestamp}

📋 Este mensaje es completamente copiable usando el botón 'Copiar'"""
            
            show_copyable_error(
                self.root,
                "Error al Procesar Datos",
                error_message
            )
            
        except Exception as e:
            print(f"❌ Error en test de procesamiento: {e}")
    
    def demo_normal_dialog(self):
        """Test de diálogo normal"""
        try:
            print("🧪 Iniciando test de diálogo normal...")
            
            # Obtener productos disponibles
            productos = Producto.get_all()
            
            if not productos:
                show_copyable_error(
                    self.root,
                    "Sin Productos",
                    "No hay productos disponibles en la base de datos.\n\nPor favor, cree algunos productos primero."
                )
                return
            
            # Crear diálogo normal
            dialog = ProductoFacturaDialog(self.root, productos)
            result = dialog.show()
            
            if result:
                print(f"✅ Producto agregado: {result}")
            else:
                print("❌ Diálogo cancelado")
            
        except Exception as e:
            print(f"❌ Error en test de diálogo normal: {e}")
            show_copyable_error(
                self.root,
                "Error en Test Normal",
                f"Error durante el test del diálogo normal:\n\n{str(e)}"
            )
    
    def demo_direct_error(self):
        """Test de error directo"""
        try:
            print("🧪 Iniciando test de error directo...")
            
            # Mostrar un error copiable directamente
            error_message = """🚨 Error de Demostración

Este es un mensaje de error de ejemplo que muestra todas las características de los mensajes copiables:

🔍 Información técnica:
- Código de error: DEMO_ERROR_001
- Módulo: demo_producto_dialog_copyable_errors.py
- Función: demo_direct_error()

📊 Datos del contexto:
- Usuario: Demo User
- Sesión: Demo Session
- Timestamp: """ + self.get_current_timestamp() + """

💡 Instrucciones para el usuario:
1. Haga clic en el botón "📋 Copiar" para copiar este mensaje
2. Pegue el mensaje en un email o ticket de soporte
3. Incluya cualquier información adicional relevante

🛠️ Información para soporte técnico:
- Este error es solo para demostración
- No requiere acción correctiva
- Puede cerrar este mensaje de forma segura

✨ Características del mensaje copiable:
- Texto completamente seleccionable
- Botón de copia con feedback visual
- Formato estructurado para fácil lectura
- Información técnica detallada incluida"""
            
            show_copyable_error(
                self.root,
                "Error de Demostración Completa",
                error_message
            )
            
        except Exception as e:
            print(f"❌ Error en test directo: {e}")
    
    def get_current_timestamp(self):
        """Obtiene timestamp actual"""
        try:
            from datetime import datetime
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "N/A"
    
    def run(self):
        """Ejecuta la demostración"""
        print("🚀 Iniciando demo de mensajes de error copiables...")
        print("💡 Instrucciones:")
        print("   - Haga clic en los botones para probar diferentes tipos de error")
        print("   - Observe el botón '📋 Copiar' en cada mensaje de error")
        print("   - Pruebe copiar y pegar los mensajes")
        print("   - Note el feedback visual al copiar")
        
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        demo = ProductoDialogErrorDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Error iniciando demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
