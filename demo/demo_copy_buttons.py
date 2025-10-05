#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo visual de los botones de copiar en ventanas de error
"""

import os
import sys
import tkinter as tk
import customtkinter as ctk

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.custom_dialogs import (
    show_copyable_error, show_copyable_warning, 
    show_copyable_info, show_copyable_confirm
)

class CopyButtonDemo:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Demo: Botones de Copiar en Ventanas de Error")
        self.root.geometry("600x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crear la interfaz del demo"""
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🔧 Demo: Botones de Copiar en Ventanas de Error",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Descripción
        desc_label = ctk.CTkLabel(
            self.root,
            text="Haz clic en los botones para ver las ventanas de error con botones de copiar:",
            font=ctk.CTkFont(size=14)
        )
        desc_label.pack(pady=10)
        
        # Frame para botones
        buttons_frame = ctk.CTkFrame(self.root)
        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Botón de error
        error_btn = ctk.CTkButton(
            buttons_frame,
            text="🚨 Mostrar Error Copiable",
            command=self.show_error_demo,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#dc3545"
        )
        error_btn.pack(pady=10, padx=20, fill="x")
        
        # Botón de advertencia
        warning_btn = ctk.CTkButton(
            buttons_frame,
            text="⚠️ Mostrar Advertencia Copiable",
            command=self.show_warning_demo,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ffc107"
        )
        warning_btn.pack(pady=10, padx=20, fill="x")
        
        # Botón de información
        info_btn = ctk.CTkButton(
            buttons_frame,
            text="ℹ️ Mostrar Información Copiable",
            command=self.show_info_demo,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#17a2b8"
        )
        info_btn.pack(pady=10, padx=20, fill="x")
        
        # Botón de confirmación
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="❓ Mostrar Confirmación Copiable",
            command=self.show_confirm_demo,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745"
        )
        confirm_btn.pack(pady=10, padx=20, fill="x")
        
        # Instrucciones
        instructions_label = ctk.CTkLabel(
            self.root,
            text="💡 En cada ventana, busca el botón '📋 Copiar' para copiar el mensaje al portapapeles",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        instructions_label.pack(pady=10)
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            self.root,
            text="Cerrar Demo",
            command=self.root.quit,
            height=30
        )
        close_btn.pack(pady=10)
    
    def show_error_demo(self):
        """Mostrar demo de error copiable"""
        error_message = """❌ Error de Conexión a la Base de Datos

🔍 Detalles técnicos:
- Error: sqlite3.OperationalError: database is locked
- Archivo: /home/user/app/data/facturacion.db
- Línea: 245 en database/connection.py

💡 Soluciones sugeridas:
1. Cerrar otras instancias de la aplicación
2. Verificar permisos del archivo de base de datos
3. Reiniciar la aplicación
4. Contactar soporte técnico con este mensaje

🕒 Timestamp: 2025-10-05 14:30:25
📧 Para soporte: soporte@empresa.com"""
        
        show_copyable_error(self.root, "Error de Base de Datos", error_message)
    
    def show_warning_demo(self):
        """Mostrar demo de advertencia copiable"""
        warning_message = """⚠️ Stock Bajo Detectado

📦 Productos con stock crítico:
- Producto A: 2 unidades (mínimo: 10)
- Producto B: 0 unidades (mínimo: 5)
- Producto C: 1 unidad (mínimo: 15)

📊 Estadísticas:
- Total productos: 150
- Productos con stock bajo: 3
- Porcentaje crítico: 2%

🔄 Acciones recomendadas:
1. Revisar proveedores
2. Generar órdenes de compra
3. Actualizar stock mínimo
4. Notificar al departamento de compras

🕒 Última actualización: 2025-10-05 14:25:00"""
        
        show_copyable_warning(self.root, "Advertencia de Stock", warning_message)
    
    def show_info_demo(self):
        """Mostrar demo de información copiable"""
        info_message = """ℹ️ Proceso Completado Exitosamente

✅ Resumen de la operación:
- Facturas procesadas: 25
- Total facturado: €12,450.75
- Tiempo de procesamiento: 2.3 segundos
- Errores encontrados: 0

📈 Estadísticas:
- Factura más alta: €2,100.00 (Factura #2025-001)
- Factura más baja: €45.50 (Factura #2025-025)
- Promedio por factura: €498.03

📁 Archivos generados:
- reporte_facturas_2025-10-05.pdf
- resumen_diario.xlsx
- backup_facturas.db

🕒 Proceso finalizado: 2025-10-05 14:35:12"""
        
        show_copyable_info(self.root, "Proceso Completado", info_message)
    
    def show_confirm_demo(self):
        """Mostrar demo de confirmación copiable"""
        confirm_message = """❓ Confirmar Eliminación de Datos

⚠️ ACCIÓN IRREVERSIBLE ⚠️

📋 Datos a eliminar:
- 15 facturas del mes anterior
- 3 productos descontinuados
- 8 clientes inactivos
- Archivos de respaldo antiguos

💾 Espacio a liberar: 245 MB

🔒 Medidas de seguridad:
- Se creará un respaldo completo antes de eliminar
- Los datos se moverán a la papelera de reciclaje
- Se mantendrá un log de la operación

⏰ Esta operación tomará aproximadamente 5 minutos

¿Estás seguro de que deseas continuar?"""
        
        result = show_copyable_confirm(self.root, "Confirmar Eliminación", confirm_message)
        
        # Mostrar resultado
        if result:
            show_copyable_info(self.root, "Confirmado", "✅ Operación confirmada por el usuario")
        else:
            show_copyable_info(self.root, "Cancelado", "❌ Operación cancelada por el usuario")
    
    def run(self):
        """Ejecutar el demo"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🔧 Iniciando Demo de Botones de Copiar...")
    print("=" * 50)
    print("💡 Este demo muestra las ventanas de error con botones de copiar")
    print("📋 En cada ventana, busca el botón '📋 Copiar' para copiar el mensaje")
    print("🖱️  Haz clic en los botones para ver diferentes tipos de mensajes")
    print()
    
    try:
        demo = CopyButtonDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Error ejecutando demo: {e}")
        print("💡 Asegúrate de tener un entorno gráfico disponible")
        sys.exit(1)
