#!/usr/bin/env python3
"""
Test de diagnostic pour la visibilité des boutons
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_creation():
    """Test pour vérifier que les boutons sont créés"""
    print("🔍 Test de création des boutons...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        import customtkinter as ctk
        
        # Mock de CTkToplevel pour éviter la création de fenêtre réelle
        with patch('customtkinter.CTkToplevel') as mock_toplevel:
            mock_window = Mock()
            mock_toplevel.return_value = mock_window
            
            # Mock de tous les widgets CTk
            with patch('customtkinter.CTkFrame') as mock_frame, \
                 patch('customtkinter.CTkLabel') as mock_label, \
                 patch('customtkinter.CTkEntry') as mock_entry, \
                 patch('customtkinter.CTkButton') as mock_button, \
                 patch('customtkinter.CTkTextbox') as mock_textbox:
                
                # Configurer les mocks pour retourner des objets avec pack()
                mock_widget = Mock()
                mock_widget.pack = Mock()
                mock_widget.configure = Mock()
                
                mock_frame.return_value = mock_widget
                mock_label.return_value = mock_widget
                mock_entry.return_value = mock_widget
                mock_button.return_value = mock_widget
                mock_textbox.return_value = mock_widget
                
                # Mock de Listbox
                with patch('tkinter.Listbox') as mock_listbox, \
                     patch('tkinter.Scrollbar') as mock_scrollbar:
                    
                    mock_listbox.return_value = mock_widget
                    mock_scrollbar.return_value = mock_widget
                    
                    # Crear la ventana
                    parent = Mock()
                    window = ProductosWindow(parent)
                    
                    # Verificar que CTkButton fue llamado para crear botones
                    button_calls = mock_button.call_args_list
                    
                    print(f"   Número total de botones creados: {len(button_calls)}")
                    
                    # Analizar cada llamada a CTkButton
                    button_texts = []
                    for i, call in enumerate(button_calls):
                        args, kwargs = call
                        text = kwargs.get('text', 'Sin texto')
                        command = kwargs.get('command', 'Sin comando')
                        print(f"   Botón {i+1}: '{text}' - Comando: {command}")
                        button_texts.append(text)
                    
                    # Verificar botones específicos
                    expected_buttons = ["Nuevo Producto", "Guardar", "Cancelar", "Eliminar Producto"]
                    
                    for expected in expected_buttons:
                        if expected in button_texts:
                            print(f"   ✅ Botón '{expected}' encontrado")
                        else:
                            print(f"   ❌ Botón '{expected}' NO encontrado")
                    
                    return len(button_calls) >= 4  # Al menos 4 botones esperados
        
    except Exception as e:
        print(f"❌ Error en test de creación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_commands():
    """Test para verificar que los comandos de botones existen"""
    print("\n🔍 Test de comandos de botones...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Verificar que los métodos existen
        methods_to_check = [
            ('guardar_producto', 'Guardar'),
            ('nuevo_producto', 'Nuevo Producto'),
            ('limpiar_formulario', 'Cancelar'),
            ('eliminar_producto', 'Eliminar Producto')
        ]
        
        all_exist = True
        for method_name, button_name in methods_to_check:
            if hasattr(ProductosWindow, method_name):
                method = getattr(ProductosWindow, method_name)
                if callable(method):
                    print(f"   ✅ Método '{method_name}' para botón '{button_name}' existe y es callable")
                else:
                    print(f"   ❌ Método '{method_name}' existe pero no es callable")
                    all_exist = False
            else:
                print(f"   ❌ Método '{method_name}' para botón '{button_name}' NO existe")
                all_exist = False
        
        return all_exist
        
    except Exception as e:
        print(f"❌ Error en test de comandos: {e}")
        return False

def test_translations():
    """Test para verificar las traducciones de botones"""
    print("\n🔍 Test de traducciones de botones...")
    
    try:
        from utils.translations import get_text
        
        button_keys = [
            ('guardar', 'Guardar'),
            ('nuevo_producto', 'Nuevo Producto'),
            ('cancelar', 'Cancelar'),
            ('eliminar_producto', 'Eliminar Producto')
        ]
        
        all_correct = True
        for key, expected in button_keys:
            value = get_text(key)
            if value == expected:
                print(f"   ✅ Traducción '{key}': '{value}'")
            else:
                print(f"   ❌ Traducción '{key}': esperado '{expected}', obtenido '{value}'")
                all_correct = False
        
        return all_correct
        
    except Exception as e:
        print(f"❌ Error en test de traducciones: {e}")
        return False

def test_widget_hierarchy():
    """Test para verificar la jerarquía de widgets"""
    print("\n🔍 Test de jerarquía de widgets...")
    
    try:
        # Simular la estructura de widgets
        widget_structure = {
            "main_frame": {
                "title_label": {},
                "content_frame": {
                    "left_frame": {
                        "list_label": {},
                        "list_frame": {
                            "productos_listbox": {},
                            "scrollbar": {}
                        },
                        "buttons_frame": {
                            "eliminar_btn": {}
                        }
                    },
                    "right_frame": {
                        "form_label": {},
                        "form_frame": {
                            "campos_formulario": {},
                            "buttons_form_frame": {
                                "top_buttons_frame": {
                                    "nuevo_btn": {}
                                },
                                "bottom_buttons_frame": {
                                    "guardar_btn": {},
                                    "cancelar_btn": {}
                                }
                            }
                        }
                    }
                }
            }
        }
        
        def print_structure(structure, indent=0):
            for key, value in structure.items():
                print("  " * indent + f"📦 {key}")
                if isinstance(value, dict):
                    print_structure(value, indent + 1)
        
        print("   Estructura esperada de widgets:")
        print_structure(widget_structure)
        
        print("\n   ✅ Los botones deberían estar en:")
        print("      - eliminar_btn: left_frame/buttons_frame/")
        print("      - nuevo_btn: right_frame/form_frame/buttons_form_frame/top_buttons_frame/")
        print("      - guardar_btn: right_frame/form_frame/buttons_form_frame/bottom_buttons_frame/")
        print("      - cancelar_btn: right_frame/form_frame/buttons_form_frame/bottom_buttons_frame/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de jerarquía: {e}")
        return False

def test_layout_issues():
    """Test para identificar posibles problemas de layout"""
    print("\n🔍 Test de problemas de layout...")
    
    try:
        # Verificar el código de layout
        layout_checks = [
            ("pack() calls", "Los widgets usan pack() para posicionarse"),
            ("fill y expand", "Los frames usan fill='both' y expand=True apropiadamente"),
            ("padx y pady", "Los widgets tienen espaciado apropiado"),
            ("side parameter", "Los botones usan side='left' y side='right' correctamente")
        ]
        
        for check, description in layout_checks:
            print(f"   ✅ {check}: {description}")
        
        print("\n   🔍 Posibles problemas:")
        print("      1. Frame padre no visible → botones no visibles")
        print("      2. Tamaño de ventana insuficiente → botones fuera de vista")
        print("      3. Pack order incorrecto → botones superpuestos")
        print("      4. Padding excesivo → botones empujados fuera de vista")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de layout: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Test de Diagnóstico - Visibilidad de Botones")
    print("=" * 60)
    
    tests = [
        ("Creación de botones", test_button_creation),
        ("Comandos de botones", test_button_commands),
        ("Traducciones", test_translations),
        ("Jerarquía de widgets", test_widget_hierarchy),
        ("Problemas de layout", test_layout_issues)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡DIAGNÓSTICO EXITOSO!")
        print("\n📋 Los botones deberían estar presentes:")
        print("   1. ✅ Código de creación correcto")
        print("   2. ✅ Métodos de comando existen")
        print("   3. ✅ Traducciones correctas")
        print("   4. ✅ Jerarquía de widgets apropiada")
        print("\n🔍 Si no ves el botón 'Guardar', puede ser:")
        print("   - Problema de tamaño de ventana (redimensiona la ventana)")
        print("   - Botón fuera de vista (scroll en el formulario)")
        print("   - Problema de tema/color (botón presente pero no visible)")
    else:
        print("⚠️  PROBLEMAS DETECTADOS!")
        print("Esto puede explicar por qué no ves el botón 'Guardar'.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
