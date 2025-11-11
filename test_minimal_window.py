#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test minimal pour identifier le problème fondamental
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_minimal_window():
    """Test minimal d'une fenêtre avec boutons"""
    try:
        print("🧪 TEST MINIMAL FENÊTRE")
        print("=" * 40)
        
        import customtkinter as ctk
        import tkinter as tk
        
        print("📝 Création fenêtre principale...")
        root = ctk.CTk()
        root.title("Test Principal")
        root.geometry("400x300")
        
        print("📝 Création fenêtre secondaire...")
        test_window = ctk.CTkToplevel(root)
        test_window.title("📊 Test Movimiento")
        test_window.geometry("600x500")
        
        print("📝 Ajout d'éléments...")
        
        # Label de test
        label = ctk.CTkLabel(test_window, text="FENÊTRE DE TEST", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)
        
        # Entry de test
        entry = ctk.CTkEntry(test_window, placeholder_text="Tapez quelque chose et appuyez Enter")
        entry.pack(pady=10)
        
        # Fonction de test
        def test_function():
            print("🎯 BOUTON CLIQUÉ !")
            entry_value = entry.get()
            print(f"📝 Valeur entry: '{entry_value}'")
        
        def test_enter(event):
            print("⌨️ ENTER PRESSÉ !")
            test_function()
        
        # Boutons de test - APPROCHE ULTRA SIMPLE
        print("📝 Création boutons...")
        
        button1 = ctk.CTkButton(
            test_window,
            text="🔴 BOUTON ROUGE",
            command=test_function,
            fg_color="red",
            width=200,
            height=50
        )
        button1.pack(pady=10)
        print("✅ Bouton rouge créé")
        
        button2 = ctk.CTkButton(
            test_window,
            text="🟢 BOUTON VERT", 
            command=test_function,
            fg_color="green",
            width=200,
            height=50
        )
        button2.pack(pady=10)
        print("✅ Bouton vert créé")
        
        # Binding Enter
        entry.bind("<Return>", test_enter)
        print("✅ Binding Enter configuré")
        
        # Forcer la mise à jour
        test_window.update_idletasks()
        test_window.update()
        print("✅ Mise à jour forcée")
        
        # Rendre visible
        test_window.lift()
        test_window.focus_force()
        print("✅ Fenêtre mise au premier plan")
        
        print("\n" + "=" * 40)
        print("🎯 INSTRUCTIONS:")
        print("1. Vous devriez voir une fenêtre 'Test Movimiento'")
        print("2. Avec un label 'FENÊTRE DE TEST'")
        print("3. Un champ de saisie")
        print("4. DEUX BOUTONS: rouge et vert")
        print("5. Tapez dans le champ et appuyez Enter")
        print("6. Ou cliquez sur les boutons")
        print("7. Regardez la console pour les messages")
        print("\n⏳ Fenêtre ouverte pour 30 secondes...")
        print("❌ Fermez la fenêtre ou attendez 30s")
        
        # Attendre 30 secondes ou fermeture
        root.after(30000, lambda: root.quit())
        
        # Démarrer la boucle
        root.mainloop()
        
        print("✅ Test terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_minimal_window()
    print(f"\nRésultat: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
    sys.exit(0 if success else 1)
