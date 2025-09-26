#!/usr/bin/env python3
"""
Démonstration du scroll de la rueda del ratón dans la fenêtre des produits
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from ui.productos import ProductosWindow
from utils.logger import get_logger

def demo_mousewheel_scroll():
    """Démonstration du scroll de la souris"""
    print("🎯 Démonstration du scroll de la rueda del ratón")
    print("=" * 50)
    
    # Configurer CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Créer la fenêtre principale
    root = ctk.CTk()
    root.title("Demo Scroll - Facturación Fácil")
    root.geometry("400x300")
    
    # Logger
    logger = get_logger("demo_scroll")
    logger.info("Iniciando demo de scroll de rueda del ratón")
    
    # Créer un label d'instructions
    instructions = ctk.CTkLabel(
        root,
        text="Demo Scroll de la Rueda del Ratón\n\n" +
             "1. Cliquez sur 'Abrir Productos'\n" +
             "2. Dans la fenêtre qui s'ouvre:\n" +
             "   • Utilisez la rueda del ratón\n" +
             "   • Le contenu devrait défiler\n" +
             "   • Testez sur différentes zones\n\n" +
             "3. Redimensionnez la fenêtre\n" +
             "4. Testez le scroll à nouveau",
        font=ctk.CTkFont(size=14),
        justify="left"
    )
    instructions.pack(pady=20, padx=20)
    
    def open_productos():
        """Ouvre la fenêtre des produits"""
        try:
            logger.info("Abriendo ventana de productos para demo")
            productos_window = ProductosWindow(root)
            logger.info("Ventana de productos abierta - Pruebe el scroll con la rueda del ratón")
        except Exception as e:
            logger.error(f"Error al abrir ventana de productos: {e}")
            print(f"❌ Error: {e}")
    
    # Bouton pour ouvrir la fenêtre des produits
    open_btn = ctk.CTkButton(
        root,
        text="🖱️ Abrir Productos (Test Scroll)",
        command=open_productos,
        font=ctk.CTkFont(size=16, weight="bold"),
        height=40
    )
    open_btn.pack(pady=20)
    
    # Instructions de fermeture
    close_label = ctk.CTkLabel(
        root,
        text="Fermez cette fenêtre pour terminer la démo",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    )
    close_label.pack(pady=10)
    
    print("✅ Fenêtre de démo créée")
    print("💡 Utilisez la rueda del ratón dans la fenêtre des produits")
    print("🔄 Le scroll devrait fonctionner sur toute la fenêtre")
    
    # Démarrer la boucle principale
    try:
        root.mainloop()
        logger.info("Demo terminada")
        print("✅ Démo terminée")
    except KeyboardInterrupt:
        print("\n🛑 Démo interrompue par l'utilisateur")
    except Exception as e:
        logger.error(f"Error en demo: {e}")
        print(f"❌ Erreur dans la démo: {e}")

if __name__ == "__main__":
    demo_mousewheel_scroll()
