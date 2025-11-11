#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que la boîte de dialogue de confirmation
a bien les boutons Confirmar et Cancelar
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_confirm_dialog_has_buttons():
    """Test que la boîte de dialogue de confirmation a les bons boutons"""
    try:
        import customtkinter as ctk
        from common.custom_dialogs import CopyableConfirmDialog
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer la boîte de dialogue
        dialog = CopyableConfirmDialog(
            root, 
            "Confirmar", 
            "¿Está seguro de que desea eliminar este producto?"
        )
        
        # Chercher les boutons
        buttons = []
        
        def find_buttons(widget):
            """Fonction récursive pour trouver tous les boutons"""
            if isinstance(widget, ctk.CTkButton):
                buttons.append(widget)
            
            try:
                for child in widget.winfo_children():
                    find_buttons(child)
            except:
                pass
        
        find_buttons(dialog.dialog)
        
        # Vérifier qu'on a au moins 3 boutons
        assert len(buttons) >= 3, f"Should have at least 3 buttons, found {len(buttons)}"
        
        # Vérifier les textes des boutons
        button_texts = [btn.cget("text") for btn in buttons]
        
        # Vérifier que les boutons essentiels sont présents
        has_copiar = any("Copiar" in text for text in button_texts)
        has_cancelar = any("Cancelar" in text for text in button_texts)
        has_confirmar = any("Confirmar" in text for text in button_texts)
        
        assert has_copiar, f"Should have 'Copiar' button. Found buttons: {button_texts}"
        assert has_cancelar, f"Should have 'Cancelar' button. Found buttons: {button_texts}"
        assert has_confirmar, f"Should have 'Confirmar' button. Found buttons: {button_texts}"
        
        # Nettoyer
        dialog.dialog.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_confirm_dialog_methods():
    """Test que la boîte de dialogue a les bonnes méthodes"""
    try:
        import customtkinter as ctk
        from common.custom_dialogs import CopyableConfirmDialog
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer la boîte de dialogue
        dialog = CopyableConfirmDialog(
            root, 
            "Confirmar", 
            "Test message"
        )
        
        # Vérifier que les méthodes existent
        assert hasattr(dialog, 'copy_message'), "Should have copy_message method"
        assert hasattr(dialog, 'yes_clicked'), "Should have yes_clicked method"
        assert hasattr(dialog, 'no_clicked'), "Should have no_clicked method"
        assert hasattr(dialog, 'show'), "Should have show method"
        
        # Vérifier que les méthodes sont appelables
        assert callable(dialog.copy_message), "copy_message should be callable"
        assert callable(dialog.yes_clicked), "yes_clicked should be callable"
        assert callable(dialog.no_clicked), "no_clicked should be callable"
        assert callable(dialog.show), "show should be callable"
        
        # Nettoyer
        dialog.dialog.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_eliminar_producto_uses_confirm_dialog():
    """Test que eliminar_producto utilise bien la boîte de dialogue de confirmation"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from database.models import Producto
        from unittest.mock import Mock
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer une instance de ProductosWindow
        productos_window = ProductosWindow(root)
        
        # Créer un produit mock
        mock_producto = Mock(spec=Producto)
        productos_window.selected_producto = mock_producto
        
        # Mock des méthodes pour éviter les effets de bord
        productos_window.load_productos = Mock()
        productos_window.limpiar_formulario = Mock()
        
        # Capturer l'appel à _show_message
        show_message_calls = []
        
        def mock_show_message(msg_type, title, message):
            show_message_calls.append((msg_type, title, message))
            if msg_type == "yesno":
                return True  # Simuler confirmation
            return None
        
        productos_window._show_message = mock_show_message
        
        # Appeler eliminar_producto
        productos_window.eliminar_producto()
        
        # Vérifier que la boîte de dialogue de confirmation a été appelée
        yesno_calls = [call for call in show_message_calls if call[0] == "yesno"]
        assert len(yesno_calls) > 0, "Should show confirmation dialog"
        
        # Vérifier le contenu de la boîte de dialogue
        call = yesno_calls[0]
        assert "Confirmar" in call[1], f"Title should contain 'Confirmar', got: {call[1]}"
        assert "eliminar" in call[2].lower(), f"Message should contain 'eliminar', got: {call[2]}"
        
        # Nettoyer
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Exécuter les tests
    tests = [
        test_confirm_dialog_has_buttons,
        test_confirm_dialog_methods,
        test_eliminar_producto_uses_confirm_dialog
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"Running {test.__name__}...")
        if test():
            print(f"✅ {test.__name__} PASSED")
            passed += 1
        else:
            print(f"❌ {test.__name__} FAILED")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
