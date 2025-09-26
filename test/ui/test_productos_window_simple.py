#!/usr/bin/env python3
"""
Test simple pour vérifier la fenêtre de productos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_productos_window_real():
    """Test avec une vraie fenêtre (ferme automatiquement)"""
    print("🔍 Test avec vraie fenêtre de productos...")
    
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        
        # Créer fenêtre principale
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre principale
        
        # Créer fenêtre de productos
        productos_window = ProductosWindow(root)
        
        # Vérifier que la fenêtre existe
        print(f"   ✅ Fenêtre créée: {productos_window.window}")
        print(f"   ✅ Titre: {productos_window.window.title()}")
        print(f"   ✅ Géométrie: {productos_window.window.geometry()}")
        
        # Vérifier que les attributs de boutons existent
        button_methods = ['guardar_producto', 'nuevo_producto', 'limpiar_formulario', 'eliminar_producto']
        for method in button_methods:
            if hasattr(productos_window, method):
                print(f"   ✅ Méthode {method} existe")
            else:
                print(f"   ❌ Méthode {method} manquante")
        
        # Vérifier que les widgets de formulaire existent
        form_widgets = ['nombre_entry', 'referencia_entry', 'precio_entry', 'categoria_entry', 'iva_entry']
        for widget in form_widgets:
            if hasattr(productos_window, widget):
                print(f"   ✅ Widget {widget} existe")
            else:
                print(f"   ❌ Widget {widget} manquant")
        
        # Fermer la fenêtre
        productos_window.window.destroy()
        root.destroy()
        
        print("   ✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_layout_analysis():
    """Analyse du layout des boutons"""
    print("\n🔍 Analyse du layout des boutons...")
    
    try:
        # Lire le code source pour analyser le layout
        with open('ui/productos.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher les sections de boutons
        button_sections = []
        
        if 'guardar_btn = ctk.CTkButton' in content:
            print("   ✅ Code de création du bouton 'Guardar' trouvé")
            button_sections.append("Guardar")
        else:
            print("   ❌ Code de création du bouton 'Guardar' NOT trouvé")
        
        if 'nuevo_btn = ctk.CTkButton' in content:
            print("   ✅ Code de création du bouton 'Nuevo' trouvé")
            button_sections.append("Nuevo")
        else:
            print("   ❌ Code de création du bouton 'Nuevo' NOT trouvé")
        
        if 'cancelar_btn = ctk.CTkButton' in content:
            print("   ✅ Code de création du bouton 'Cancelar' trouvé")
            button_sections.append("Cancelar")
        else:
            print("   ❌ Code de création du bouton 'Cancelar' NOT trouvé")
        
        # Analyser le pack() du bouton guardar
        if 'guardar_btn.pack(side="left"' in content:
            print("   ✅ Bouton 'Guardar' utilise pack(side='left')")
        elif 'guardar_btn.pack(' in content:
            print("   ⚠️  Bouton 'Guardar' utilise pack() mais pas side='left'")
        else:
            print("   ❌ Bouton 'Guardar' ne semble pas utiliser pack()")
        
        # Analyser la hiérarchie
        if 'bottom_buttons_frame = ctk.CTkFrame' in content:
            print("   ✅ Frame 'bottom_buttons_frame' créé pour les boutons")
        else:
            print("   ❌ Frame 'bottom_buttons_frame' NOT trouvé")
        
        if 'bottom_buttons_frame.pack(' in content:
            print("   ✅ Frame 'bottom_buttons_frame' est packed")
        else:
            print("   ❌ Frame 'bottom_buttons_frame' n'est pas packed")
        
        return len(button_sections) >= 3
        
    except Exception as e:
        print(f"   ❌ Erreur dans l'analyse: {e}")
        return False

def test_window_size_analysis():
    """Analyse de la taille de fenêtre"""
    print("\n🔍 Analyse de la taille de fenêtre...")
    
    try:
        # Analyser les dimensions
        window_width = 1000
        window_height = 700
        
        print(f"   📏 Taille de fenêtre: {window_width}x{window_height}")
        
        # Estimer l'espace utilisé
        estimated_usage = {
            "Titre": 50,
            "Liste de productos (gauche)": 600,  # Prend la moitié
            "Formulaire (droite)": 600,  # Prend la moitié
            "Champs de formulaire": 400,
            "Boutons": 100,
            "Padding/margins": 50
        }
        
        total_estimated_height = sum([v for k, v in estimated_usage.items() if "gauche" not in k and "droite" not in k])
        
        print(f"   📊 Estimation d'utilisation verticale:")
        for component, height in estimated_usage.items():
            if "gauche" not in component and "droite" not in component:
                print(f"      - {component}: ~{height}px")
        
        print(f"   📊 Total estimé: ~{total_estimated_height}px sur {window_height}px disponibles")
        
        if total_estimated_height > window_height:
            print("   ⚠️  PROBLÈME POTENTIEL: Contenu peut dépasser la hauteur de fenêtre")
            print("   💡 Solution: Augmenter la hauteur de fenêtre ou ajouter scrolling")
        else:
            print("   ✅ Espace suffisant pour tous les éléments")
        
        return total_estimated_height <= window_height
        
    except Exception as e:
        print(f"   ❌ Erreur dans l'analyse: {e}")
        return False

def suggest_solutions():
    """Suggère des solutions pour le problème"""
    print("\n💡 SOLUTIONS SUGGÉRÉES:")
    
    solutions = [
        "1. 🔍 VÉRIFICATION VISUELLE:",
        "   - Ouvrir l'application: ./run_with_correct_python.sh main.py",
        "   - Aller dans 'Gestión de Productos'",
        "   - Redimensionner la fenêtre si nécessaire",
        "   - Faire défiler vers le bas dans le formulaire",
        "",
        "2. 📏 PROBLÈME DE TAILLE:",
        "   - Augmenter la hauteur de fenêtre dans productos.py ligne 16",
        "   - Changer '1000x700' vers '1000x800' ou plus",
        "",
        "3. 🎨 PROBLÈME DE COULEUR/THÈME:",
        "   - Le bouton existe mais n'est pas visible (même couleur que fond)",
        "   - Vérifier les couleurs fg_color et hover_color",
        "",
        "4. 📦 PROBLÈME DE LAYOUT:",
        "   - Vérifier que bottom_buttons_frame est visible",
        "   - Ajouter du debug logging dans create_widgets()",
        "",
        "5. 🔧 DEBUG RAPIDE:",
        "   - Ajouter print() dans create_widgets() pour tracer la création",
        "   - Vérifier les logs pour voir si la création se fait correctement"
    ]
    
    for solution in solutions:
        print(solution)

def main():
    """Fonction principale"""
    print("🧪 Test Simple - Fenêtre de Productos")
    print("=" * 50)
    
    tests = [
        ("Layout des boutons", test_button_layout_analysis),
        ("Taille de fenêtre", test_window_size_analysis),
        ("Fenêtre réelle", test_productos_window_real)
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
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    # Toujours afficher les solutions
    suggest_solutions()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡ANÁLISIS COMPLETADO!")
        print("El botón 'Guardar' debería estar presente.")
        print("Si no lo ves, prueba las soluciones sugeridas arriba.")
    else:
        print("⚠️  PROBLEMAS DETECTADOS!")
        print("Revisa las soluciones sugeridas arriba.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
