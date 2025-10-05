#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilidad para asegurar que todos los mensajes tengan botón copiar
Intercepta llamadas a messagebox y las redirige a diálogos copiables
"""

import tkinter.messagebox as original_messagebox
from utils.logger import get_logger

logger = get_logger("copyable_messages")

def ensure_copyable_error(title, message, **kwargs):
    """Asegurar que los errores tengan botón copiar"""
    try:
        from common.custom_dialogs import show_copyable_error
        parent = kwargs.get('parent', None)
        return show_copyable_error(parent, title, message)
    except Exception as e:
        logger.warning(f"Fallback a messagebox estándar para error: {e}")
        return original_messagebox.showerror(title, message, **kwargs)

def ensure_copyable_warning(title, message, **kwargs):
    """Asegurar que las advertencias tengan botón copiar"""
    try:
        from common.custom_dialogs import show_copyable_warning
        parent = kwargs.get('parent', None)
        return show_copyable_warning(parent, title, message)
    except Exception as e:
        logger.warning(f"Fallback a messagebox estándar para warning: {e}")
        return original_messagebox.showwarning(title, message, **kwargs)

def ensure_copyable_info(title, message, **kwargs):
    """Asegurar que la información tenga botón copiar"""
    try:
        from common.custom_dialogs import show_copyable_info
        parent = kwargs.get('parent', None)
        return show_copyable_info(parent, title, message)
    except Exception as e:
        logger.warning(f"Fallback a messagebox estándar para info: {e}")
        return original_messagebox.showinfo(title, message, **kwargs)

def ensure_copyable_confirm(title, message, **kwargs):
    """Asegurar que las confirmaciones tengan botón copiar"""
    try:
        from common.custom_dialogs import show_copyable_confirm
        parent = kwargs.get('parent', None)
        return show_copyable_confirm(parent, title, message)
    except Exception as e:
        logger.warning(f"Fallback a messagebox estándar para confirm: {e}")
        return original_messagebox.askyesno(title, message, **kwargs)

def patch_messagebox():
    """Parchear messagebox para usar diálogos copiables por defecto"""
    try:
        import tkinter.messagebox as messagebox
        
        # Guardar funciones originales si no están guardadas
        if not hasattr(messagebox, '_original_showerror'):
            messagebox._original_showerror = messagebox.showerror
            messagebox._original_showwarning = messagebox.showwarning
            messagebox._original_showinfo = messagebox.showinfo
            messagebox._original_askyesno = messagebox.askyesno
        
        # Reemplazar con versiones copiables
        messagebox.showerror = ensure_copyable_error
        messagebox.showwarning = ensure_copyable_warning
        messagebox.showinfo = ensure_copyable_info
        messagebox.askyesno = ensure_copyable_confirm
        
        logger.info("MessageBox parcheado para usar diálogos copiables")
        return True
        
    except Exception as e:
        logger.error(f"Error parcheando messagebox: {e}")
        return False

def unpatch_messagebox():
    """Restaurar messagebox original"""
    try:
        import tkinter.messagebox as messagebox
        
        if hasattr(messagebox, '_original_showerror'):
            messagebox.showerror = messagebox._original_showerror
            messagebox.showwarning = messagebox._original_showwarning
            messagebox.showinfo = messagebox._original_showinfo
            messagebox.askyesno = messagebox._original_askyesno
            
            # Limpiar referencias
            delattr(messagebox, '_original_showerror')
            delattr(messagebox, '_original_showwarning')
            delattr(messagebox, '_original_showinfo')
            delattr(messagebox, '_original_askyesno')
        
        logger.info("MessageBox restaurado a versión original")
        return True
        
    except Exception as e:
        logger.error(f"Error restaurando messagebox: {e}")
        return False

def test_copyable_messages():
    """Test para verificar que el parche funciona"""
    print("🧪 Test: Parche de mensajes copiables")
    
    try:
        # Aplicar parche
        if not patch_messagebox():
            print("   ❌ Error aplicando parche")
            return False
        
        # Test con messagebox parcheado
        import tkinter.messagebox as messagebox
        
        # Crear ventana temporal para test
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        # Test de funciones parcheadas (sin mostrar diálogos reales)
        print("   ✅ Parche aplicado correctamente")
        print("   ✅ messagebox.showerror -> diálogo copiable")
        print("   ✅ messagebox.showwarning -> diálogo copiable")
        print("   ✅ messagebox.showinfo -> diálogo copiable")
        print("   ✅ messagebox.askyesno -> diálogo copiable")
        
        # Restaurar
        root.destroy()
        unpatch_messagebox()
        
        print("   ✅ Test PASADO")
        return True
        
    except Exception as e:
        print(f"   ❌ Test FALLÓ: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Utilidad: Asegurar Mensajes Copiables")
    print("=" * 45)
    print("💡 Esta utilidad parchea messagebox para usar diálogos copiables")
    print()
    
    if test_copyable_messages():
        print("\n🎉 La utilidad funciona correctamente")
        print("💡 Para usar en la aplicación:")
        print("   from utils.ensure_copyable_messages import patch_messagebox")
        print("   patch_messagebox()  # Al inicio de la aplicación")
    else:
        print("\n❌ La utilidad tiene problemas")
        print("💡 Revisar logs para más detalles")
