#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilidad para forzar el uso de diálogos copiables
Reemplaza completamente las funciones de messagebox
"""

import tkinter.messagebox as original_messagebox
from utils.logger import get_logger

logger = get_logger("force_copyable")

def force_copyable_warning(title, message, **kwargs):
    """Forzar uso de diálogo copiable para advertencias"""
    logger.info(f"🔧 FORCE: Interceptando messagebox.showwarning - '{title}': '{message[:50]}...'")
    
    try:
        from common.custom_dialogs import show_copyable_warning
        parent = kwargs.get('parent', None)
        logger.info("🔧 FORCE: Usando show_copyable_warning")
        result = show_copyable_warning(parent, title, message)
        logger.info("✅ FORCE: show_copyable_warning exitoso")
        return result
    except Exception as e:
        logger.error(f"❌ FORCE: Error en show_copyable_warning: {e}")
        logger.warning("⚠️  FORCE: Fallback a messagebox original")
        return original_messagebox.showwarning(title, message, **kwargs)

def force_copyable_error(title, message, **kwargs):
    """Forzar uso de diálogo copiable para errores"""
    logger.info(f"🔧 FORCE: Interceptando messagebox.showerror - '{title}': '{message[:50]}...'")
    
    try:
        from common.custom_dialogs import show_copyable_error
        parent = kwargs.get('parent', None)
        logger.info("🔧 FORCE: Usando show_copyable_error")
        result = show_copyable_error(parent, title, message)
        logger.info("✅ FORCE: show_copyable_error exitoso")
        return result
    except Exception as e:
        logger.error(f"❌ FORCE: Error en show_copyable_error: {e}")
        logger.warning("⚠️  FORCE: Fallback a messagebox original")
        return original_messagebox.showerror(title, message, **kwargs)

def force_copyable_info(title, message, **kwargs):
    """Forzar uso de diálogo copiable para información"""
    logger.info(f"🔧 FORCE: Interceptando messagebox.showinfo - '{title}': '{message[:50]}...'")
    
    try:
        from common.custom_dialogs import show_copyable_info
        parent = kwargs.get('parent', None)
        logger.info("🔧 FORCE: Usando show_copyable_info")
        result = show_copyable_info(parent, title, message)
        logger.info("✅ FORCE: show_copyable_info exitoso")
        return result
    except Exception as e:
        logger.error(f"❌ FORCE: Error en show_copyable_info: {e}")
        logger.warning("⚠️  FORCE: Fallback a messagebox original")
        return original_messagebox.showinfo(title, message, **kwargs)

def force_copyable_confirm(title, message, **kwargs):
    """Forzar uso de diálogo copiable para confirmaciones"""
    logger.info(f"🔧 FORCE: Interceptando messagebox.askyesno - '{title}': '{message[:50]}...'")
    
    try:
        from common.custom_dialogs import show_copyable_confirm
        parent = kwargs.get('parent', None)
        logger.info("🔧 FORCE: Usando show_copyable_confirm")
        result = show_copyable_confirm(parent, title, message)
        logger.info("✅ FORCE: show_copyable_confirm exitoso")
        return result
    except Exception as e:
        logger.error(f"❌ FORCE: Error en show_copyable_confirm: {e}")
        logger.warning("⚠️  FORCE: Fallback a messagebox original")
        return original_messagebox.askyesno(title, message, **kwargs)

def apply_force_patch():
    """Aplicar parche forzado a messagebox"""
    try:
        import tkinter.messagebox as messagebox
        
        # Guardar originales si no están guardados
        if not hasattr(messagebox, '_force_original_showwarning'):
            messagebox._force_original_showwarning = messagebox.showwarning
            messagebox._force_original_showerror = messagebox.showerror
            messagebox._force_original_showinfo = messagebox.showinfo
            messagebox._force_original_askyesno = messagebox.askyesno
        
        # Aplicar parche forzado
        messagebox.showwarning = force_copyable_warning
        messagebox.showerror = force_copyable_error
        messagebox.showinfo = force_copyable_info
        messagebox.askyesno = force_copyable_confirm
        
        logger.info("🔧 FORCE: Parche forzado aplicado a messagebox")
        logger.info("🔧 FORCE: TODOS los messagebox ahora usan diálogos copiables")
        return True
        
    except Exception as e:
        logger.error(f"❌ FORCE: Error aplicando parche forzado: {e}")
        return False

def remove_force_patch():
    """Remover parche forzado"""
    try:
        import tkinter.messagebox as messagebox
        
        if hasattr(messagebox, '_force_original_showwarning'):
            messagebox.showwarning = messagebox._force_original_showwarning
            messagebox.showerror = messagebox._force_original_showerror
            messagebox.showinfo = messagebox._force_original_showinfo
            messagebox.askyesno = messagebox._force_original_askyesno
            
            # Limpiar referencias
            delattr(messagebox, '_force_original_showwarning')
            delattr(messagebox, '_force_original_showerror')
            delattr(messagebox, '_force_original_showinfo')
            delattr(messagebox, '_force_original_askyesno')
        
        logger.info("🔧 FORCE: Parche forzado removido")
        return True
        
    except Exception as e:
        logger.error(f"❌ FORCE: Error removiendo parche forzado: {e}")
        return False

# Aplicar automáticamente al importar
if __name__ != "__main__":
    try:
        apply_force_patch()
    except Exception as e:
        logger.error(f"❌ FORCE: Error en aplicación automática: {e}")

if __name__ == "__main__":
    print("🔧 Utilidad: Forzar Diálogos Copiables")
    print("=" * 40)
    print("💡 Esta utilidad FUERZA el uso de diálogos copiables")
    print("🔧 Intercepta TODAS las llamadas a messagebox")
    print()
    
    if apply_force_patch():
        print("✅ Parche forzado aplicado correctamente")
        print("🎯 Ahora TODOS los messagebox tendrán botón copiar")
        print()
        print("💡 Para usar en la aplicación:")
        print("   import utils.force_copyable_dialogs  # Se aplica automáticamente")
    else:
        print("❌ Error aplicando parche forzado")
        print("💡 Revisar logs para más detalles")
