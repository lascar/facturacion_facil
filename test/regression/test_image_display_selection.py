#!/usr/bin/env python3
"""
Test pour vérifier l'affichage d'image lors de la sélection de produit
"""

import sys
import os
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_image():
    """Crée une image de test"""
    try:
        from PIL import Image
        
        # Créer une image simple de test
        img = Image.new('RGB', (100, 100), color='red')
        
        # Sauvegarder dans un fichier temporaire
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file.name, 'PNG')
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        print(f"Erreur lors de la création de l'image de test: {e}")
        return None

def test_image_display_on_selection():
    """Test de l'affichage d'image lors de la sélection"""
    print("🔍 Test de l'affichage d'image lors de la sélection...")
    
    try:
        from ui.productos import ProductosWindow
        from database.models import Producto
        from unittest.mock import Mock, patch
        import tempfile
        
        # Créer une image de test
        test_image_path = create_test_image()
        if not test_image_path:
            print("   ❌ Impossible de créer l'image de test")
            return False
        
        try:
            # Créer un produit de test avec image
            test_producto = Mock(spec=Producto)
            test_producto.id = 1
            test_producto.nombre = "Producto Test"
            test_producto.referencia = "TEST-001"
            test_producto.precio = 10.50
            test_producto.categoria = "Test"
            test_producto.iva_recomendado = 21.0
            test_producto.descripcion = "Producto de test"
            test_producto.imagen_path = test_image_path
            
            # Créer instance mock de ProductosWindow
            window = Mock()
            window.window = Mock()
            window.window.winfo_exists.return_value = True
            window.logger = Mock()
            window.imagen_path = ""
            window.selected_producto = None
            
            # Mock des widgets
            window.nombre_entry = Mock()
            window.referencia_entry = Mock()
            window.precio_entry = Mock()
            window.categoria_entry = Mock()
            window.iva_entry = Mock()
            window.descripcion_text = Mock()
            window.imagen_label = Mock()
            window.imagen_display = Mock()
            window.quitar_imagen_btn = Mock()
            
            # Mock de update_image_display
            window.update_image_display = Mock()
            
            # Test de load_producto_to_form
            print("   🔧 Testando load_producto_to_form...")
            window.selected_producto = test_producto
            
            # Appeler la méthode réelle
            ProductosWindow.load_producto_to_form(window)
            
            # Vérifications
            assert window.imagen_path == test_image_path, f"Chemin d'image incorrect: {window.imagen_path}"
            window.imagen_label.configure.assert_called()
            window.update_image_display.assert_called_once()
            
            print("   ✅ load_producto_to_form appelle update_image_display")
            print(f"   ✅ Chemin d'image correctement assigné: {os.path.basename(test_image_path)}")
            
            # Test de update_image_display avec image existante
            print("   🔧 Testando update_image_display...")
            
            with patch('os.path.exists', return_value=True), \
                 patch('PIL.Image.open') as mock_image_open, \
                 patch('PIL.ImageTk.PhotoTk') as mock_photo:
                
                # Mock de l'image PIL
                mock_img = Mock()
                mock_img.size = (200, 200)
                mock_img.thumbnail = Mock()
                mock_image_open.return_value = mock_img
                
                # Mock de PhotoTk
                mock_photo_instance = Mock()
                mock_photo.return_value = mock_photo_instance
                
                # Appeler update_image_display
                ProductosWindow.update_image_display(window)
                
                # Vérifications
                mock_image_open.assert_called_once_with(test_image_path)
                mock_img.thumbnail.assert_called_once()
                window.imagen_display.configure.assert_called()
                
                print("   ✅ update_image_display charge et affiche l'image")
            
            return True
            
        finally:
            # Nettoyer l'image de test
            if test_image_path and os.path.exists(test_image_path):
                os.unlink(test_image_path)
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_path_validation():
    """Test de validation des chemins d'image"""
    print("\n🔍 Test de validation des chemins d'image...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Créer instance mock
        window = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.logger = Mock()
        window.imagen_display = Mock()
        window.quitar_imagen_btn = Mock()
        
        # Test avec chemin vide
        print("   🔧 Test avec chemin vide...")
        window.imagen_path = ""
        ProductosWindow.update_image_display(window)
        
        # Vérifier que le placeholder est affiché
        window.imagen_display.configure.assert_called_with(image="", text="Sin imagen\n📷")
        print("   ✅ Placeholder affiché pour chemin vide")
        
        # Test avec chemin inexistant
        print("   🔧 Test avec chemin inexistant...")
        window.imagen_path = "/chemin/inexistant/image.png"
        window.imagen_display.configure.reset_mock()
        
        ProductosWindow.update_image_display(window)
        
        # Vérifier que le placeholder est affiché
        window.imagen_display.configure.assert_called_with(image="", text="Sin imagen\n📷")
        print("   ✅ Placeholder affiché pour chemin inexistant")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_logging_integration():
    """Test de l'intégration du logging"""
    print("\n🔍 Test de l'intégration du logging...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Créer instance mock
        window = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.logger = Mock()
        window.imagen_path = "/test/image.png"
        window.imagen_display = Mock()
        window.quitar_imagen_btn = Mock()
        
        # Appeler update_image_display
        ProductosWindow.update_image_display(window)
        
        # Vérifier que le logging a été appelé
        window.logger.debug.assert_called()
        
        # Vérifier les messages de log
        log_calls = [call.args[0] for call in window.logger.debug.call_args_list]
        
        assert any("Actualizando display de imagen" in msg for msg in log_calls), "Log de début manquant"
        assert any("Archivo de imagen no existe" in msg for msg in log_calls), "Log d'erreur manquant"
        
        print("   ✅ Logging correctement intégré")
        print("   ✅ Messages de debug appropriés")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test d'Affichage d'Image lors de la Sélection")
    print("=" * 60)
    
    tests = [
        ("Affichage d'image lors de sélection", test_image_display_on_selection),
        ("Validation des chemins d'image", test_image_path_validation),
        ("Intégration du logging", test_logging_integration)
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
        print("🎉 ¡AFFICHAGE D'IMAGE LORS DE SÉLECTION CORRIGÉ!")
        print("\n📋 Corrections implémentées:")
        print("   1. ✅ load_producto_to_form appelle update_image_display")
        print("   2. ✅ Logging détaillé pour diagnostic")
        print("   3. ✅ Validation des chemins d'image")
        print("   4. ✅ Gestion des erreurs robuste")
        print("\n🎯 Maintenant quand vous sélectionnez un produit:")
        print("   - L'image du produit s'affiche automatiquement")
        print("   - Les logs montrent le processus de chargement")
        print("   - Les erreurs sont gérées gracieusement")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ!")
        print("Vérifiez les détails ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
