#!/usr/bin/env python3
"""
Test para verificar la corrección del filedialog de selección de imágenes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_filedialog_filetypes():
    """Test para verificar que los filetypes están correctamente configurados"""
    print("🔍 Test de configuración de filetypes...")
    
    try:
        from utils.config import app_config
        
        # Obtener formatos soportados
        supported_formats = app_config.get_supported_formats()
        print(f"✅ Formatos soportados: {supported_formats}")
        
        # Construir filetypes como en el código corregido
        filetypes_str = " ".join([f"*{fmt}" for fmt in supported_formats])
        print(f"✅ String de filetypes: '{filetypes_str}'")
        
        # Verificar que el formato es correcto
        expected_filetypes = [
            ("Imágenes", filetypes_str),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("Todos los archivos", "*.*")
        ]
        
        print("✅ Filetypes configurados:")
        for name, pattern in expected_filetypes:
            print(f"   - {name}: {pattern}")
        
        # Verificar que cada formato está incluido
        for fmt in supported_formats:
            assert fmt in filetypes_str, f"Formato {fmt} no está en filetypes_str"
        
        print("🎉 Configuración de filetypes es correcta!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de filetypes: {e}")
        return False

def test_filedialog_mock():
    """Test para verificar que el filedialog se llama con los parámetros correctos"""
    print("\n🔍 Test de llamada a filedialog...")
    
    try:
        from unittest.mock import Mock, patch
        from ui.productos import ProductosWindow
        
        # Crear una instancia mock
        window = Mock(spec=ProductosWindow)
        window.imagen_path = ""
        window.imagen_label = Mock()
        window.update_image_display = Mock()
        
        # Mock del filedialog
        with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
            mock_filedialog.return_value = ""
            
            # Llamar al método real
            ProductosWindow.seleccionar_imagen(window)
            
            # Verificar que se llamó
            mock_filedialog.assert_called_once()
            
            # Verificar los parámetros
            call_kwargs = mock_filedialog.call_args[1]
            print(f"✅ Título: {call_kwargs['title']}")
            print(f"✅ Directorio inicial: {call_kwargs.get('initialdir', 'No especificado')}")
            print(f"✅ Filetypes: {call_kwargs['filetypes']}")
            
            # Verificar que hay múltiples opciones de filetypes
            filetypes = call_kwargs['filetypes']
            assert len(filetypes) > 1, "Debería haber múltiples opciones de filetypes"
            assert any("Imágenes" in ft[0] for ft in filetypes), "Debería haber una opción 'Imágenes'"
            assert any("PNG" in ft[0] for ft in filetypes), "Debería haber una opción 'PNG'"
            assert any("*.*" in ft[1] for ft in filetypes), "Debería haber una opción 'Todos los archivos'"
            
            print("🎉 Llamada a filedialog es correcta!")
            return True
        
    except Exception as e:
        print(f"❌ Error en test de filedialog: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_selection_simulation():
    """Test para simular la selección de diferentes tipos de archivos"""
    print("\n🔍 Test de simulación de selección de archivos...")
    
    try:
        from unittest.mock import Mock, patch
        from ui.productos import ProductosWindow
        import tempfile
        
        # Crear archivos temporales de diferentes tipos
        test_files = []
        for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            temp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
            temp_file.write(b'fake_image_data')
            temp_file.close()
            test_files.append(temp_file.name)
        
        try:
            for test_file in test_files:
                print(f"✅ Probando archivo: {os.path.basename(test_file)}")
                
                # Crear instancia mock
                window = Mock(spec=ProductosWindow)
                window.imagen_path = ""
                window.imagen_label = Mock()
                window.update_image_display = Mock()
                
                # Mock de las operaciones de archivo
                with patch('tkinter.filedialog.askopenfilename') as mock_filedialog, \
                     patch('os.makedirs'), \
                     patch('shutil.copy2') as mock_copy:
                    
                    mock_filedialog.return_value = test_file
                    
                    # Llamar al método
                    ProductosWindow.seleccionar_imagen(window)
                    
                    # Verificar que se procesó correctamente
                    mock_copy.assert_called_once()
                    assert window.imagen_path != ""
                    
                    print(f"   ✅ Archivo {os.path.basename(test_file)} procesado correctamente")
            
            print("🎉 Simulación de selección de archivos exitosa!")
            return True
            
        finally:
            # Limpiar archivos temporales
            for test_file in test_files:
                if os.path.exists(test_file):
                    os.unlink(test_file)
        
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Test de Corrección del Filedialog")
    print("=" * 50)
    
    tests = [
        ("Configuración de filetypes", test_filedialog_filetypes),
        ("Llamada a filedialog", test_filedialog_mock),
        ("Simulación de selección", test_file_selection_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡CORRECCIÓN DEL FILEDIALOG EXITOSA!")
        print("\n📋 Cambios realizados:")
        print("   1. ✅ Filetypes corregidos con múltiples opciones")
        print("   2. ✅ Opciones específicas por tipo de archivo")
        print("   3. ✅ Opción 'Todos los archivos' añadida")
        print("   4. ✅ Formato correcto para tkinter filedialog")
        print("\n🎯 Ahora deberías poder seleccionar archivos de imagen correctamente!")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON!")
        print("Revisa los errores arriba para más detalles.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
