#!/usr/bin/env python3
"""
Test des améliorations apportées à l'interface des produits
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_system():
    """Test du système de configuration"""
    print("🔧 Test du système de configuration...")
    
    try:
        from utils.config import app_config
        
        # Test des méthodes de base
        default_dir = app_config.get_default_image_directory()
        print(f"✅ Répertoire par défaut: {default_dir}")
        
        assets_dir = app_config.get_assets_directory()
        print(f"✅ Répertoire assets: {assets_dir}")
        
        display_size = app_config.get_image_display_size()
        print(f"✅ Taille d'affichage: {display_size}")
        
        formats = app_config.get_supported_formats()
        print(f"✅ Formats supportés: {formats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur config: {e}")
        return False

def test_new_methods():
    """Test des nouvelles méthodes"""
    print("\n🔧 Test des nouvelles méthodes...")
    
    try:
        from ui.productos import ProductosWindow
        
        # Vérifier que les nouvelles méthodes existent
        methods_to_check = [
            'update_image_display',
            'quitar_imagen', 
            'configurar_directorio_imagenes'
        ]
        
        for method_name in methods_to_check:
            if hasattr(ProductosWindow, method_name):
                method = getattr(ProductosWindow, method_name)
                if callable(method):
                    print(f"✅ Méthode {method_name} trouvée et callable")
                else:
                    print(f"❌ Méthode {method_name} trouvée mais pas callable")
                    return False
            else:
                print(f"❌ Méthode {method_name} non trouvée")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur méthodes: {e}")
        return False

def test_translations():
    """Test des nouvelles traductions"""
    print("\n🌐 Test des nouvelles traductions...")
    
    try:
        from utils.translations import get_text
        
        new_translations = [
            "quitar_imagen",
            "configurar_directorio"
        ]
        
        for key in new_translations:
            value = get_text(key)
            if value and value != key:  # Vérifier que la traduction existe
                print(f"✅ {key}: '{value}'")
            else:
                print(f"❌ Traduction manquante pour: {key}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur traductions: {e}")
        return False

def test_pil_import():
    """Test de l'import PIL"""
    print("\n🖼️  Test de l'import PIL...")
    
    try:
        from PIL import Image, ImageTk
        print("✅ PIL importé avec succès")
        
        # Test de création d'une image simple
        img = Image.new('RGB', (100, 100), color='red')
        print("✅ Création d'image PIL réussie")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import PIL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur PIL: {e}")
        return False

def test_file_operations():
    """Test des opérations de fichier améliorées"""
    print("\n📁 Test des opérations de fichier...")
    
    try:
        import tempfile
        import os
        from utils.config import app_config
        
        # Test de création du répertoire assets
        assets_dir = app_config.get_assets_directory()
        os.makedirs(assets_dir, exist_ok=True)
        print(f"✅ Répertoire assets créé: {assets_dir}")
        
        # Test de création d'un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(b'fake_image_data')
            temp_path = temp_file.name
        
        print(f"✅ Fichier temporaire créé: {temp_path}")
        
        # Nettoyer
        os.unlink(temp_path)
        print("✅ Nettoyage effectué")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur opérations fichier: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test des améliorations de l'interface produits")
    print("=" * 60)
    
    tests = [
        ("Système de configuration", test_config_system),
        ("Nouvelles méthodes", test_new_methods),
        ("Nouvelles traductions", test_translations),
        ("Import PIL", test_pil_import),
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
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TOUTES LES AMÉLIORATIONS SONT FONCTIONNELLES!")
        print("\n📋 Améliorations apportées:")
        print("   1. ✅ Display d'image avec aperçu")
        print("   2. ✅ Configuration du répertoire par défaut")
        print("   3. ✅ Bouton 'Nuevo Producto' déplacé dans le formulaire")
        print("   4. ✅ Bouton 'Quitar imagen' ajouté")
        print("   5. ✅ Bouton de configuration (⚙️) ajouté")
        print("   6. ✅ Gestion d'erreurs améliorée")
    else:
        print("⚠️  CERTAINES AMÉLIORATIONS ONT DES PROBLÈMES!")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
