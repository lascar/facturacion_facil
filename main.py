#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Facturación Fácil
Aplicación de facturación simple con gestión de productos, stock y clientes.
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from database.database import db
from utils.logger import app_logger, log_info, log_error, log_exception

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar logging
        app_logger.log_startup_info()
        log_info("=== Iniciando aplicación Facturación Fácil ===")

        # Inicializar la base de datos
        log_info("Inicializando base de datos...")
        db.init_database()
        log_info("Base de datos inicializada correctamente")

        # Crear y ejecutar la aplicación
        log_info("Creando ventana principal")
        app = MainWindow()

        log_info("Iniciando bucle principal de la aplicación")
        app.run()

        log_info("Aplicación cerrada normalmente")

    except Exception as e:
        log_exception(e, "main")
        log_error(f"Error crítico al iniciar la aplicación: {str(e)}")

        # Mostrar error al usuario si es posible
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror(
                "Error Crítico",
                f"Error inesperado en la aplicación:\n{str(e)}\n\nRevisa los logs en el directorio 'logs' para más detalles."
            )
        except:
            print(f"Error crítico: {str(e)}")

        sys.exit(1)

if __name__ == "__main__":
    main()
