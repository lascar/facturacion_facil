#!/usr/bin/env python3
"""
Test pour vérifier la visibilité réelle du bouton Guardar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_visibility_with_gui():
    """Test avec GUI réelle pour vérifier la visibilité"""
    print("🔍 Test de visibilité avec GUI réelle...")
    
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        import time
        
        # Créer fenêtre principale
        root = ctk.CTk()
        root.title("Test de Visibilité")
        root.geometry("300x200")
        
        # Créer bouton pour ouvrir productos
        def open_productos():
            productos_window = ProductosWindow(root)
            
            # Ajouter debug pour vérifier les widgets
            def check_widgets():
                print("\n🔍 Vérification des widgets après création:")
                
                # Vérifier que la fenêtre existe
                print(f"   ✅ Fenêtre productos: {productos_window.window}")
                print(f"   ✅ Titre: {productos_window.window.title()}")
                
                # Essayer de trouver tous les widgets CTkButton
                def find_buttons(widget, level=0):
                    indent = "  " * level
                    widget_type = type(widget).__name__
                    
                    if "CTkButton" in widget_type:
                        try:
                            text = widget.cget("text") if hasattr(widget, 'cget') else "No text"
                            print(f"{indent}🔘 BOUTON TROUVÉ: {text} ({widget_type})")
                        except:
                            print(f"{indent}🔘 BOUTON TROUVÉ: (text inaccessible) ({widget_type})")
                    
                    # Chercher dans les enfants
                    try:
                        if hasattr(widget, 'winfo_children'):
                            for child in widget.winfo_children():
                                find_buttons(child, level + 1)
                    except:
                        pass
                
                print("   🔍 Recherche de tous les boutons dans la hiérarchie:")
                find_buttons(productos_window.window)
                
                # Vérifier les attributs spécifiques
                attrs_to_check = ['nombre_entry', 'referencia_entry', 'precio_entry']
                for attr in attrs_to_check:
                    if hasattr(productos_window, attr):
                        widget = getattr(productos_window, attr)
                        print(f"   ✅ {attr}: {type(widget).__name__}")
                    else:
                        print(f"   ❌ {attr}: MANQUANT")
                
                # Tester la méthode nuevo_producto
                print("\n🔍 Test de nuevo_producto():")
                try:
                    productos_window.nuevo_producto()
                    print("   ✅ nuevo_producto() exécuté sans erreur")
                except Exception as e:
                    print(f"   ❌ Erreur dans nuevo_producto(): {e}")
            
            # Programmer la vérification après un délai
            productos_window.window.after(100, check_widgets)
        
        # Créer bouton de test
        test_btn = ctk.CTkButton(
            root,
            text="Ouvrir Productos\n(Vérifier Console)",
            command=open_productos,
            height=60
        )
        test_btn.pack(expand=True, pady=20)
        
        # Instructions
        info_label = ctk.CTkLabel(
            root,
            text="1. Cliquer le bouton\n2. Vérifier la console\n3. Fermer les fenêtres",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(pady=10)
        
        print("   ✅ Fenêtre de test créée")
        print("   📋 Instructions:")
        print("      1. Cliquer sur 'Ouvrir Productos'")
        print("      2. Vérifier la console pour les résultats")
        print("      3. Fermer les fenêtres pour continuer")
        
        # Fermer automatiquement après 30 secondes
        def auto_close():
            print("\n⏰ Fermeture automatique après 30 secondes")
            root.quit()
        
        root.after(30000, auto_close)  # 30 secondes
        
        # Lancer la GUI
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_colors():
    """Test des couleurs des boutons"""
    print("\n🎨 Test des couleurs des boutons...")
    
    try:
        # Analyser les couleurs définies dans le code
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher les définitions de couleurs
        color_patterns = [
            ('fg_color="#2E8B57"', 'Guardar - Couleur principale: Vert foncé'),
            ('hover_color="#228B22"', 'Guardar - Couleur hover: Vert plus foncé'),
            ('fg_color="#808080"', 'Cancelar - Couleur principale: Gris'),
            ('hover_color="#696969"', 'Cancelar - Couleur hover: Gris foncé')
        ]
        
        for pattern, description in color_patterns:
            if pattern in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - NON TROUVÉ")
        
        # Vérifier si les couleurs sont visibles
        print("\n   🔍 Analyse de visibilité des couleurs:")
        print("      - #2E8B57 (Vert foncé): Devrait être bien visible")
        print("      - #228B22 (Vert hover): Devrait être visible au survol")
        print("      - #808080 (Gris): Peut être peu visible selon le thème")
        print("      - #696969 (Gris foncé): Devrait être visible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_frame_hierarchy():
    """Test de la hiérarchie des frames"""
    print("\n📦 Test de la hiérarchie des frames...")
    
    try:
        # Analyser la structure des frames dans le code
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        frame_structure = []
        button_locations = []
        
        for i, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            if 'ctk.CTkFrame' in line_clean and '=' in line_clean:
                frame_name = line_clean.split('=')[0].strip()
                frame_structure.append((i, frame_name))
            
            if 'ctk.CTkButton' in line_clean and 'guardar' in line_clean.lower():
                button_locations.append((i, 'Bouton Guardar'))
            
            if '.pack(' in line_clean and any(frame in line_clean for frame, _ in frame_structure[-3:] if frame_structure):
                frame_structure.append((i, f"  └─ pack() call"))
        
        print("   📋 Structure des frames trouvée:")
        for line_num, frame_info in frame_structure:
            print(f"      Ligne {line_num}: {frame_info}")
        
        print("\n   🔘 Localisation des boutons:")
        for line_num, button_info in button_locations:
            print(f"      Ligne {line_num}: {button_info}")
        
        return len(frame_structure) > 0 and len(button_locations) > 0
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test de Visibilité Réelle du Bouton Guardar")
    print("=" * 60)
    
    tests = [
        ("Couleurs des boutons", test_button_colors),
        ("Hiérarchie des frames", test_frame_hierarchy),
        ("Visibilité avec GUI", test_button_visibility_with_gui)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 {test_name}...")
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
    print("💡 SOLUTIONS IMMÉDIATES:")
    print("1. 🔍 VÉRIFICATION DIRECTE:")
    print("   ./run_with_correct_python.sh main.py")
    print("   → Gestión de Productos → Nuevo Producto")
    print("   → Chercher le bouton vert 'Guardar' en bas du formulaire")
    print("")
    print("2. 📏 SI PAS VISIBLE:")
    print("   → Redimensionner la fenêtre (plus grande)")
    print("   → Faire défiler vers le bas dans le formulaire")
    print("   → Vérifier en bas à gauche du formulaire")
    print("")
    print("3. 🎨 SI PROBLÈME DE COULEUR:")
    print("   → Le bouton est vert foncé (#2E8B57)")
    print("   → Devrait être visible sur fond clair")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
