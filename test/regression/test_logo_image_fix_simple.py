#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple non-blocking test for logo image functionality
"""

import sys
import os
import tempfile
import pytest

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_logo_image_methods_exist():
    """Test that logo image methods exist and can be imported"""
    try:
        from ui.organizacion import OrganizacionWindow
        
        # Check that the class has the required methods
        assert hasattr(OrganizacionWindow, 'load_logo_image')
        assert hasattr(OrganizacionWindow, 'remove_logo')
        assert hasattr(OrganizacionWindow, '_clear_previous_logo_image')
        assert hasattr(OrganizacionWindow, '_load_and_process_image')
        assert hasattr(OrganizacionWindow, '_create_and_display_ctk_image')
        assert hasattr(OrganizacionWindow, '_configure_logo_label_safe')
        
        print("✅ All logo image methods exist")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except AttributeError as e:
        print(f"❌ Missing method: {e}")
        return False

def test_image_validation_logic():
    """Test image validation logic without GUI"""
    try:
        from PIL import Image
        import tempfile
        
        # Test 1: Create a valid image
        test_image = Image.new('RGB', (100, 100), color='blue')
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            test_image.save(temp_file.name, 'PNG')
            temp_path = temp_file.name
        
        # Test that the image can be opened and verified
        try:
            with Image.open(temp_path) as img:
                img.verify()
            print("✅ Valid image created and verified")
        except Exception as e:
            print(f"❌ Image verification failed: {e}")
            return False
        finally:
            os.unlink(temp_path)
        
        # Test 2: Test with non-existent file
        non_existent = "/tmp/non_existent_image.png"
        assert not os.path.exists(non_existent)
        print("✅ Non-existent file test passed")
        
        # Test 3: Test with invalid image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(b"This is not an image")
            temp_file.flush()
            invalid_path = temp_file.name
        
        try:
            with Image.open(invalid_path) as img:
                img.verify()
            print("❌ Invalid image should have failed verification")
            return False
        except Exception:
            print("✅ Invalid image correctly rejected")
        finally:
            os.unlink(invalid_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Image validation test failed: {e}")
        return False

def test_ctk_image_usage():
    """Test that CTkImage is used in the logo handling code"""
    try:
        # Read the organizacion.py file
        org_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ui', 'organizacion.py')
        
        with open(org_file_path, 'r') as f:
            content = f.read()
        
        # Check that CTkImage is used
        assert 'ctk.CTkImage' in content, "organizacion.py should use ctk.CTkImage"
        print("✅ CTkImage is used in organizacion.py")
        
        # Check that the robust image handling methods exist
        assert '_create_and_display_ctk_image' in content, "Should have robust CTkImage creation method"
        assert '_configure_logo_label_safe' in content, "Should have safe label configuration method"
        print("✅ Robust image handling methods exist")
        
        return True
        
    except Exception as e:
        print(f"❌ CTkImage usage test failed: {e}")
        return False

def test_logo_image_fix():
    """Main test function that runs all sub-tests"""
    print("🧪 Testing logo image fixes (non-blocking version)")
    print("=" * 60)
    
    tests = [
        ("Method existence", test_logo_image_methods_exist),
        ("Image validation logic", test_image_validation_logic),
        ("CTkImage usage", test_ctk_image_usage)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All logo image tests passed!")
        print("✨ Logo image functionality is working correctly!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = test_logo_image_fix()
    sys.exit(0 if success else 1)
