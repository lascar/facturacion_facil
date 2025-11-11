#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify image handling fixes
"""

import sys
import os
import tempfile
import warnings
from PIL import Image

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_image_validation():
    """Test image path validation"""
    print("🧪 Testing image path validation...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Create a mock productos window for testing
        class MockProductosWindow:
            def __init__(self):
                from utils.logger import get_logger
                self.logger = get_logger("test")
                
            def _validate_image_path(self, image_path):
                """Copy of the validation method"""
                if not image_path:
                    return ""
                
                # Verificar que el archivo existe
                if not os.path.exists(image_path):
                    self.logger.debug(f"Imagen no existe: {image_path}")
                    return ""
                
                # Verificar que es un archivo de imagen válido
                try:
                    with Image.open(image_path) as test_image:
                        test_image.verify()
                    return image_path
                except Exception as e:
                    self.logger.warning(f"Archivo no es una imagen válida: {image_path} - {e}")
                    return ""
        
        mock_window = MockProductosWindow()
        
        # Test 1: Empty path
        result = mock_window._validate_image_path("")
        assert result == "", "Empty path should return empty string"
        print("  ✅ Empty path test passed")
        
        # Test 2: Non-existent file
        result = mock_window._validate_image_path("/tmp/non_existent_image.png")
        assert result == "", "Non-existent file should return empty string"
        print("  ✅ Non-existent file test passed")
        
        # Test 3: Create a valid test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Create a simple test image
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image.save(tmp_file.name, 'PNG')
            
            result = mock_window._validate_image_path(tmp_file.name)
            assert result == tmp_file.name, "Valid image should return the same path"
            print("  ✅ Valid image test passed")
            
            # Clean up
            os.unlink(tmp_file.name)
        
        # Test 4: Invalid file (not an image)
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b"This is not an image")
            tmp_file.flush()
            
            result = mock_window._validate_image_path(tmp_file.name)
            assert result == "", "Invalid image file should return empty string"
            print("  ✅ Invalid image file test passed")
            
            # Clean up
            os.unlink(tmp_file.name)
        
        print("✅ All image validation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Image validation test failed: {e}")
        return False

def test_ctk_image_usage():
    """Test that CTkImage is used instead of ImageTk.PhotoImage"""
    print("🧪 Testing CTkImage usage...")
    
    try:
        # Check productos.py
        with open('ui/productos.py', 'r') as f:
            content = f.read()
            
        # Should not contain ImageTk.PhotoImage
        assert 'ImageTk.PhotoImage' not in content, "productos.py should not use ImageTk.PhotoImage"
        print("  ✅ productos.py doesn't use ImageTk.PhotoImage")
        
        # Should contain CTkImage
        assert 'ctk.CTkImage' in content, "productos.py should use ctk.CTkImage"
        print("  ✅ productos.py uses ctk.CTkImage")
        
        # Check common/ui_components.py
        with open('common/ui_components.py', 'r') as f:
            content = f.read()
            
        # Should contain CTkImage
        assert 'ctk.CTkImage' in content, "ui_components.py should use ctk.CTkImage"
        print("  ✅ ui_components.py uses ctk.CTkImage")
        
        print("✅ All CTkImage usage tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CTkImage usage test failed: {e}")
        return False

def test_debug_cleanup():
    """Test that debug print statements were removed"""
    print("🧪 Testing debug cleanup...")
    
    try:
        with open('common/custom_dialogs.py', 'r') as f:
            content = f.read()
            
        # Count debug print statements
        debug_prints = content.count('print(f"🔍 DEBUG:')
        debug_prints += content.count('print("🔍 DEBUG:')
        debug_prints += content.count('print(f"❌ DEBUG:')
        debug_prints += content.count('print("❌ DEBUG:')
        debug_prints += content.count('print(f"✅ DEBUG:')
        debug_prints += content.count('print("✅ DEBUG:')
        
        assert debug_prints == 0, f"Found {debug_prints} debug print statements"
        print("  ✅ No debug print statements found")
        
        print("✅ Debug cleanup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Debug cleanup test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running image handling fixes tests...\n")
    
    # Capture warnings to check if CustomTkinter warnings are gone
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        tests = [
            test_image_validation,
            test_ctk_image_usage,
            test_debug_cleanup
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()
        
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        # Check for warnings
        ctk_warnings = [warning for warning in w if 'CTkLabel Warning' in str(warning.message)]
        if ctk_warnings:
            print(f"⚠️  Found {len(ctk_warnings)} CustomTkinter warnings")
            for warning in ctk_warnings:
                print(f"   {warning.message}")
        else:
            print("✅ No CustomTkinter warnings detected")
        
        if passed == total and not ctk_warnings:
            print("🎉 All tests passed successfully!")
            return True
        else:
            print("❌ Some tests failed or warnings detected")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
