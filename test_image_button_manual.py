#!/usr/bin/env python3
"""
Test manuel pour vérifier le problème du bouton de sélection d'image
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester tous les imports nécessaires"""
    print("🔍 Test des imports...")
    
    try:
        import customtkinter as ctk
        print("✅ customtkinter importé")
    except ImportError as e:
        print(f"❌ Erreur customtkinter: {e}")
        return False
    
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        print("✅ tkinter et filedialog importés")
    except ImportError as e:
        print(f"❌ Erreur tkinter: {e}")
        return False
    
    try:
        from utils.translations import get_text
        print("✅ translations importé")
    except ImportError as e:
        print(f"❌ Erreur translations: {e}")
        return False
    
    try:
        from database.models import Producto
        print("✅ models importé")
    except ImportError as e:
        print(f"❌ Erreur models: {e}")
        return False
    
    try:
        import shutil
        print("✅ shutil importé")
    except ImportError as e:
        print(f"❌ Erreur shutil: {e}")
        return False
    
    return True

def test_translations():
    """Tester les traductions nécessaires"""
    print("\n🔍 Test des traductions...")
    
    try:
        from utils.translations import get_text
        
        required_keys = [
            "seleccionar_imagen",
            "imagen", 
            "error"
        ]
        
        for key in required_keys:
            value = get_text(key)
            print(f"✅ {key}: '{value}'")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur traductions: {e}")
        return False

def test_method_definition():
    """Tester que la méthode seleccionar_imagen est bien définie"""
    print("\n🔍 Test de la définition de méthode...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Vérifier que la méthode existe
        if hasattr(ProductosWindow, 'seleccionar_imagen'):
            print("✅ Méthode seleccionar_imagen trouvée")
            
            # Vérifier que c'est une méthode callable
            if callable(getattr(ProductosWindow, 'seleccionar_imagen')):
                print("✅ Méthode seleccionar_imagen est callable")
                return True
            else:
                print("❌ seleccionar_imagen n'est pas callable")
                return False
        else:
            print("❌ Méthode seleccionar_imagen non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de méthode: {e}")
        return False

def test_filedialog_availability():
    """Tester la disponibilité du filedialog"""
    print("\n🔍 Test de disponibilité du filedialog...")
    
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Essayer de créer une root window temporaire
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        print("✅ Root window créée")
        
        # Tester que filedialog.askopenfilename existe
        if hasattr(filedialog, 'askopenfilename'):
            print("✅ filedialog.askopenfilename disponible")
            
            # Note: On ne peut pas tester l'ouverture réelle du dialog 
            # dans un environnement sans display
            print("ℹ️  Test d'ouverture du dialog ignoré (pas de display)")
            
            root.destroy()
            return True
        else:
            print("❌ filedialog.askopenfilename non disponible")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ Erreur filedialog: {e}")
        return False

def test_file_operations():
    """Tester les opérations de fichier"""
    print("\n🔍 Test des opérations de fichier...")
    
    try:
        import os
        import shutil
        import tempfile
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(b'fake_image_data')
            temp_path = temp_file.name
        
        print(f"✅ Fichier temporaire créé: {temp_path}")
        
        # Tester os.makedirs
        test_dir = "test_assets/images"
        os.makedirs(test_dir, exist_ok=True)
        print(f"✅ Répertoire créé: {test_dir}")
        
        # Tester shutil.copy2
        dest_path = os.path.join(test_dir, "test_image.png")
        shutil.copy2(temp_path, dest_path)
        print(f"✅ Fichier copié vers: {dest_path}")
        
        # Nettoyer
        os.unlink(temp_path)
        os.unlink(dest_path)
        os.rmdir(test_dir)
        os.rmdir("test_assets")
        print("✅ Nettoyage effectué")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur opérations fichier: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test manuel du bouton de sélection d'image")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Traductions", test_translations),
        ("Définition de méthode", test_method_definition),
        ("Disponibilité filedialog", test_filedialog_availability),
        ("Opérations de fichier", test_file_operations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TOUS LES TESTS PASSENT!")
        print("Le problème pourrait être lié à l'environnement d'exécution ou au display.")
    else:
        print("⚠️  CERTAINS TESTS ÉCHOUENT!")
        print("Vérifiez les erreurs ci-dessus pour identifier le problème.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
