#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de ventanas mejorado para evitar bloqueos y problemas de topmost
"""

import tkinter as tk
from utils.logger import get_logger

class WindowManager:
    """Gestiona ventanas de forma segura para evitar bloqueos"""
    
    def __init__(self):
        self.logger = get_logger("window_manager")
        self._topmost_windows = set()  # Ventanas que están en topmost
        
    def make_window_visible(self, window, temporary_topmost=True, duration_ms=100):
        """
        Hace que una ventana sea visible de forma segura
        
        Args:
            window: La ventana a hacer visible
            temporary_topmost: Si usar topmost temporal
            duration_ms: Duración del topmost en milisegundos
        """
        try:
            if not window or not window.winfo_exists():
                return False
                
            # Traer al frente
            window.lift()
            window.focus_force()
            
            if temporary_topmost:
                # Configurar topmost temporal
                window.attributes('-topmost', True)
                self._topmost_windows.add(window)
                
                # Programar remoción del topmost
                window.after(duration_ms, lambda: self._remove_topmost_safely(window))
                
            self.logger.debug(f"Ventana hecha visible: {window}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error haciendo ventana visible: {e}")
            return False
    
    def _remove_topmost_safely(self, window):
        """Remueve topmost de forma segura"""
        try:
            if window in self._topmost_windows:
                self._topmost_windows.remove(window)
                
            if window and window.winfo_exists():
                window.attributes('-topmost', False)
                self.logger.debug(f"Topmost removido de ventana: {window}")
                
        except Exception as e:
            self.logger.debug(f"Error removiendo topmost: {e}")
    
    def close_window_safely(self, window):
        """Cierra una ventana de forma segura"""
        try:
            if not window:
                return True
                
            # Remover topmost si está activo
            if window in self._topmost_windows:
                self._remove_topmost_safely(window)
            
            # Verificar si existe antes de cerrar
            if window.winfo_exists():
                # Quitar topmost por si acaso
                try:
                    window.attributes('-topmost', False)
                except:
                    pass
                
                # Cerrar la ventana
                window.destroy()
                self.logger.debug(f"Ventana cerrada exitosamente: {window}")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error cerrando ventana: {e}")
            # Intentar forzar cierre
            try:
                if window:
                    window.quit()
            except:
                pass
            return False
    
    def cleanup_all_topmost(self):
        """Limpia todas las ventanas topmost"""
        windows_to_clean = list(self._topmost_windows)
        for window in windows_to_clean:
            self._remove_topmost_safely(window)
        
        self.logger.info(f"Limpiadas {len(windows_to_clean)} ventanas topmost")
    
    def show_dialog_safely(self, dialog_func, *args, **kwargs):
        """
        Muestra un diálogo de forma segura con timeout
        
        Args:
            dialog_func: Función que crea y muestra el diálogo
            *args, **kwargs: Argumentos para la función
            
        Returns:
            Resultado del diálogo o None si hay error
        """
        try:
            # Ejecutar la función del diálogo
            result = dialog_func(*args, **kwargs)
            return result
            
        except Exception as e:
            self.logger.error(f"Error mostrando diálogo: {e}")
            return None
        finally:
            # Limpiar cualquier topmost que pueda haber quedado
            self.cleanup_all_topmost()

# Instancia global del gestor de ventanas
window_manager = WindowManager()

def make_window_visible(window, temporary_topmost=True, duration_ms=100):
    """Función de conveniencia para hacer ventana visible"""
    return window_manager.make_window_visible(window, temporary_topmost, duration_ms)

def close_window_safely(window):
    """Función de conveniencia para cerrar ventana de forma segura"""
    return window_manager.close_window_safely(window)

def show_dialog_safely(dialog_func, *args, **kwargs):
    """Función de conveniencia para mostrar diálogo de forma segura"""
    return window_manager.show_dialog_safely(dialog_func, *args, **kwargs)

def cleanup_all_topmost():
    """Función de conveniencia para limpiar todas las ventanas topmost"""
    return window_manager.cleanup_all_topmost()
