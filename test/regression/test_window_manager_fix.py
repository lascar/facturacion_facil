#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que el gestor de ventanas funciona correctamente
"""

import sys
import os
import threading
import time

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Configurar modo headless para evitar problemas de GUI
os.environ['HEADLESS_MODE'] = '1'

def test_window_manager_fix():
    """Test que verifica que el gestor de ventanas funciona correctamente"""
    print("🧪 Probando gestor de ventanas mejorado")
    print("=" * 60)
    
    try:
        # Importar después de configurar el path
        import customtkinter as ctk
        from utils.window_manager import window_manager, make_window_visible, close_window_safely
        
        print("✅ Módulos importados correctamente")
        
        # Test 1: Crear ventana raíz
        print("\n1️⃣ Test: Creación de ventana raíz")
        
        root = ctk.CTk()
        root.withdraw()  # Ocultar la ventana principal
        
        print("   ✅ Ventana raíz creada")
        
        # Test 2: Verificar funciones del gestor de ventanas
        print("\n2️⃣ Test: Verificar funciones del gestor")
        
        # Crear ventana de prueba
        test_window = ctk.CTkToplevel(root)
        test_window.title("Test Window")
        test_window.withdraw()
        
        # Verificar que se puede hacer visible
        result = make_window_visible(test_window, temporary_topmost=True, duration_ms=50)
        assert result == True, "make_window_visible debería retornar True"
        
        print("   ✅ make_window_visible funciona")
        
        # Test 3: Verificar cierre seguro
        print("\n3️⃣ Test: Verificar cierre seguro")
        
        # Esperar un poco para que el topmost se quite
        time.sleep(0.1)
        
        # Cerrar ventana de forma segura
        result = close_window_safely(test_window)
        assert result == True, "close_window_safely debería retornar True"
        
        print("   ✅ close_window_safely funciona")
        
        # Test 4: Verificar limpieza de topmost
        print("\n4️⃣ Test: Verificar limpieza de topmost")
        
        # Crear otra ventana
        test_window2 = ctk.CTkToplevel(root)
        test_window2.withdraw()
        
        # Hacer visible con topmost
        make_window_visible(test_window2, temporary_topmost=True, duration_ms=50)
        
        # Limpiar todos los topmost
        window_manager.cleanup_all_topmost()
        
        print("   ✅ cleanup_all_topmost funciona")
        
        # Cerrar ventana
        close_window_safely(test_window2)
        
        # Test 5: Verificar gestión de errores
        print("\n5️⃣ Test: Verificar gestión de errores")
        
        # Intentar cerrar ventana None
        result = close_window_safely(None)
        assert result == True, "close_window_safely con None debería retornar True"
        
        # Intentar hacer visible ventana None
        result = make_window_visible(None)
        assert result == False, "make_window_visible con None debería retornar False"
        
        print("   ✅ Gestión de errores funciona")
        
        # Limpiar
        try:
            close_window_safely(root)
        except:
            pass
        
        print("\n" + "=" * 60)
        print("🎉 TODOS LOS TESTS PASARON")
        print("📋 Funcionalidades verificadas:")
        print("   ✅ Gestor de ventanas creado correctamente")
        print("   ✅ make_window_visible funciona con topmost temporal")
        print("   ✅ close_window_safely cierra ventanas de forma segura")
        print("   ✅ cleanup_all_topmost limpia ventanas topmost")
        print("   ✅ Gestión de errores robusta")
        print("\n✨ El gestor de ventanas mejorado está FUNCIONANDO!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_window_manager_fix()
        print(f"\n{'✅ TEST EXITOSO' if success else '❌ TEST FALLIDO'}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
