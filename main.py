#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Facturación Fácil
Aplicación de facturación simple con gestión de productos, stock y clientes.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework

# Définir PyQt6 comme framework GUI
set_gui_framework('pyqt6')

from ui.main_window import MainWindow
from database.database import db
from utils.logger import app_logger, log_info, log_error, log_exception

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar logging
        app_logger.log_startup_info()
        log_info("=== Iniciando aplicación Facturación Fácil ===")

        # Aplicar parche FORZADO para asegurar que todos los mensajes tengan botón copiar
        try:
            import utils.force_copyable_dialogs  # Se aplica automáticamente
            log_info("🔧 Parche FORZADO de mensajes copiables aplicado correctamente")
            log_info("🎯 GARANTÍA: Todos los messagebox tendrán botón copiar")
        except Exception as e:
            log_error(f"❌ Error aplicando parche forzado: {e}")
            # Fallback al parche normal
            try:
                from utils.ensure_copyable_messages import patch_messagebox
                patch_messagebox()
                log_info("✅ Parche normal de mensajes copiables aplicado como fallback")
            except Exception as e2:
                log_error(f"⚠️  Advertencia: No se pudo aplicar ningún parche de mensajes: {e2}")

        # Inicializar la base de datos
        log_info("Inicializando base de datos...")
        db.init_database()
        log_info("Base de datos inicializada correctamente")

        # Crear y ejecutar la aplicación PyQt6
        log_info("Creando ventana principal")

        # Créer l'application PyQt6 si elle n'existe pas
        from PyQt6.QtWidgets import QApplication
        if not QApplication.instance():
            qt_app = QApplication(sys.argv)
        else:
            qt_app = QApplication.instance()

        # Créer la fenêtre principale
        main_window = MainWindow()
        main_window.show()

        log_info("Iniciando bucle principal de la aplicación")
        qt_app.exec()

        log_info("Aplicación cerrada normalmente")

    except Exception as e:
        log_exception(e, "main")
        log_error(f"Error crítico al iniciar la aplicación: {str(e)}")

        # Mostrar error al usuario si es posible
        try:
            # Intentar usar diálogo copiable
            from common.custom_dialogs import show_copyable_error
            show_copyable_error(
                None,
                "Error Crítico de Aplicación",
                f"❌ Error inesperado en la aplicación:\n\n"
                f"🔍 Detalles técnicos:\n{str(e)}\n\n"
                f"📁 Logs: Revisa los logs en el directorio 'logs' para más detalles.\n\n"
                f"💡 Soluciones sugeridas:\n"
                f"1. Reiniciar la aplicación\n"
                f"2. Verificar permisos de archivos\n"
                f"3. Contactar soporte técnico con este mensaje\n\n"
                f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        except Exception:
            # Fallback con messagebox estándar
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
