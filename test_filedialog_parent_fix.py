#!/usr/bin/env python3
"""
Test pour vérifier la correction du parent dans les filedialog
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_filedialog_askopenfilename_has_parent():
    """Test que filedialog.askopenfilename a un parent spécifié"""
    print("🔍 Test que filedialog.askopenfilename a un parent...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        
        # Créer instance mock
        window = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.window.lift = Mock()
        window.window.focus_force = Mock()
        window.logger = Mock()
        window.imagen_path = ""
        window.imagen_label = Mock()
        window.update_image_display = Mock()
        
        # Mock de app_config
        with patch('ui.productos.app_config') as mock_config:
            mock_config.get_default_image_directory.return_value = "/test/dir"
            mock_config.get_supported_formats.return_value = ['.png', '.jpg']
            mock_config.get_assets_directory.return_value = "/test/assets"
            
            # Mock de filedialog
            with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
                mock_filedialog.return_value = ""
                
                # Appeler seleccionar_imagen
                ProductosWindow.seleccionar_imagen(window)
                
                # Vérifications
                mock_filedialog.assert_called_once()
                
                # Vérifier que parent est spécifié
                call_kwargs = mock_filedialog.call_args[1]
                assert 'parent' in call_kwargs, "Paramètre 'parent' manquant dans filedialog.askopenfilename"
                assert call_kwargs['parent'] == window.window, "Parent incorrect dans filedialog.askopenfilename"
                
                # Vérifier que la fenêtre est mise au premier plan
                window.window.lift.assert_called()
                window.window.focus_force.assert_called()
                
                print("   ✅ filedialog.askopenfilename a parent=self.window")
                print("   ✅ Fenêtre mise au premier plan avant le dialog")
                
                return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_filedialog_askdirectory_has_parent():
    """Test que filedialog.askdirectory a un parent spécifié"""
    print("\n🔍 Test que filedialog.askdirectory a un parent...")
    
    try:
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        
        # Créer instance mock
        window = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.window.lift = Mock()
        window.window.focus_force = Mock()
        window.logger = Mock()
        
        # Mock de app_config
        with patch('ui.productos.app_config') as mock_config:
            mock_config.get_default_image_directory.return_value = "/test/dir"
            mock_config.set_default_image_directory.return_value = True
            
            # Mock de filedialog
            with patch('tkinter.filedialog.askdirectory') as mock_filedialog:
                mock_filedialog.return_value = "/new/test/dir"
                
                # Mock de _show_message
                window._show_message = Mock()
                
                # Appeler configurar_directorio
                ProductosWindow.configurar_directorio(window)
                
                # Vérifications
                mock_filedialog.assert_called_once()
                
                # Vérifier que parent est spécifié
                call_kwargs = mock_filedialog.call_args[1]
                assert 'parent' in call_kwargs, "Paramètre 'parent' manquant dans filedialog.askdirectory"
                assert call_kwargs['parent'] == window.window, "Parent incorrect dans filedialog.askdirectory"
                
                # Vérifier que la fenêtre est mise au premier plan
                window.window.lift.assert_called()
                window.window.focus_force.assert_called()
                
                print("   ✅ filedialog.askdirectory a parent=self.window")
                print("   ✅ Fenêtre mise au premier plan avant le dialog")
                
                return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_analysis():
    """Analyse du code pour vérifier les corrections"""
    print("\n🔍 Analyse du code pour vérifier les corrections...")
    
    try:
        # Lire le fichier productos.py
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les corrections
        corrections = [
            ('parent=self.window', 'Parent spécifié dans filedialog'),
            ('self.window.lift()', 'Fenêtre mise au premier plan'),
            ('self.window.focus_force()', 'Focus forcé sur la fenêtre'),
            ('filedialog.askopenfilename(', 'filedialog.askopenfilename présent'),
            ('filedialog.askdirectory(', 'filedialog.askdirectory présent')
        ]
        
        corrections_found = 0
        for pattern, description in corrections:
            count = content.count(pattern)
            if count > 0:
                corrections_found += 1
                print(f"   ✅ {description} ({count} occurrences)")
            else:
                print(f"   ❌ {description} - NON TROUVÉ")
        
        # Vérifier spécifiquement les parents dans filedialog
        askopenfilename_lines = [line for line in content.split('\n') if 'filedialog.askopenfilename(' in line]
        askdirectory_lines = [line for line in content.split('\n') if 'filedialog.askdirectory(' in line]
        
        print(f"\n   📊 filedialog.askopenfilename trouvés: {len(askopenfilename_lines)}")
        print(f"   📊 filedialog.askdirectory trouvés: {len(askdirectory_lines)}")
        
        # Vérifier que parent= apparaît après chaque filedialog
        parent_count = content.count('parent=self.window')
        expected_dialogs = len(askopenfilename_lines) + len(askdirectory_lines)
        
        print(f"   📊 parent=self.window trouvés: {parent_count}")
        print(f"   📊 Dialogs attendus: {expected_dialogs}")
        
        if parent_count >= expected_dialogs and corrections_found >= 4:
            print("   ✅ Toutes les corrections principales implémentées")
            return True
        else:
            print("   ❌ Corrections insuffisantes")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_window_focus_before_dialog():
    """Test que la fenêtre est mise au premier plan avant les dialogs"""
    print("\n🔍 Test de focus avant dialogs...")
    
    try:
        # Lire le fichier productos.py
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Chercher les patterns de focus avant filedialog
        focus_patterns_found = 0
        
        for i, line in enumerate(lines):
            if 'filedialog.' in line:
                # Vérifier les lignes précédentes pour lift() et focus_force()
                preceding_lines = lines[max(0, i-5):i]
                preceding_text = ''.join(preceding_lines)
                
                if 'self.window.lift()' in preceding_text and 'self.window.focus_force()' in preceding_text:
                    focus_patterns_found += 1
                    print(f"   ✅ Focus avant filedialog à la ligne {i+1}")
                else:
                    print(f"   ❌ Focus manquant avant filedialog à la ligne {i+1}")
        
        if focus_patterns_found >= 2:  # Au moins 2 dialogs avec focus
            print("   ✅ Focus implémenté avant les dialogs")
            return True
        else:
            print("   ❌ Focus insuffisant avant les dialogs")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test de Correction du Parent dans Filedialog")
    print("=" * 60)
    
    tests = [
        ("filedialog.askopenfilename a parent", test_filedialog_askopenfilename_has_parent),
        ("filedialog.askdirectory a parent", test_filedialog_askdirectory_has_parent),
        ("Focus avant dialogs", test_window_focus_before_dialog),
        ("Analyse du code", test_code_analysis)
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
        print("🎉 ¡CORRECTION DU FILEDIALOG RÉUSSIE!")
        print("\n📋 Corrections implémentées:")
        print("   1. ✅ filedialog.askopenfilename avec parent=self.window")
        print("   2. ✅ filedialog.askdirectory avec parent=self.window")
        print("   3. ✅ Fenêtre mise au premier plan avant dialogs")
        print("   4. ✅ Focus forcé sur la fenêtre")
        print("\n🎯 Maintenant les dialogs de sélection:")
        print("   - Apparaissent DEVANT la fenêtre de produits")
        print("   - Sont modaux par rapport à la fenêtre parent")
        print("   - Ne restent plus cachés derrière")
        print("\n📋 Pour tester:")
        print("   1. Ouvrir 'Gestión de Productos'")
        print("   2. Cliquer 'Seleccionar Imagen'")
        print("   3. ✅ Le dialog apparaît DEVANT la fenêtre")
    else:
        print("⚠️  CERTAINES CORRECTIONS ONT ÉCHOUÉ!")
        print("Vérifiez les détails ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
