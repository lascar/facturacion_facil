#!/usr/bin/env python3
"""
Test des dialogues avec texte copiable
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from common.custom_dialogs import (
    show_copyable_info, show_copyable_success, 
    show_copyable_warning, show_copyable_error,
    show_copyable_confirm
)

def test_copyable_dialogs():
    """Test des dialogues avec texte copiable"""
    
    print("=== Test des dialogues copiables ===\n")
    
    # Configurar CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Crear ventana principal
    root = ctk.CTk()
    root.title("Test Dialogues Copiables")
    root.geometry("700x500")
    
    # Centrer la ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Titre principal
    title_label = ctk.CTkLabel(
        root,
        text="Test de Dialogues avec Texte Copiable",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=30)
    
    # Description
    desc_label = ctk.CTkLabel(
        root,
        text="Teste les différents types de dialogues avec texte sélectionnable et copiable",
        font=ctk.CTkFont(size=12)
    )
    desc_label.pack(pady=10)
    
    # Frame pour les boutons
    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(pady=30, padx=50, fill="both", expand=True)
    
    # Messages de test
    messages = {
        "info": """ℹ️ Message d'information
        
Ceci est un message d'information avec du texte que tu peux sélectionner et copier.

Détails techniques :
- Version: 1.0.0
- Module: Gestion des stocks
- Timestamp: 2025-01-25 09:15:21

Tu peux sélectionner ce texte avec la souris et le copier avec Ctrl+C ou en cliquant sur le bouton 'Copiar'.""",
        
        "success": """✅ Opération réussie !
        
L'opération s'est terminée avec succès.

Résumé :
- Stock mis à jour : Produit ABC123
- Quantité ajoutée : +25 unités
- Nouveau total : 75 unités
- Heure : 09:15:21

Ce message peut être copié pour documentation ou support.""",
        
        "warning": """⚠️ Attention - Stock bas détecté
        
Les produits suivants ont un stock critique :

• Produit A (REF001) : 3 unités restantes
• Produit B (REF002) : 1 unité restante  
• Produit C (REF003) : 0 unités (rupture)

Action recommandée : Réapprovisionnement urgent

Erreur technique : STOCK_LOW_WARNING_001
Date : 2025-01-25 09:15:21""",
        
        "error": """❌ Erreur lors de la mise à jour du stock
        
Une erreur s'est produite pendant l'opération.

Détails de l'erreur :
- Code d'erreur : STOCK_UPDATE_FAILED_500
- Module : database.models.Stock
- Méthode : update_stock()
- Ligne : 245
- Message : Connection timeout to database
- Timestamp : 2025-01-25 09:15:21.123

Stack trace :
  File "stock.py", line 245, in update_stock
    stock_obj.save()
  File "models.py", line 156, in save
    db.execute_query(query, params)
  DatabaseError: Connection timeout

Copie ce message pour le support technique.""",
        
        "confirm": """🤔 Confirmer l'impact sur le stock
        
Cette opération va affecter le stock des produits suivants :

📦 IMPACT SUR LE STOCK :

• Produit Premium A :
  Stock actuel : 50 → Après : 45 unités
  État : 🟢 STOCK OK (45)

• Produit Standard B :
  Stock actuel : 8 → Après : 5 unités  
  État : 🟠 STOCK BAS (5)

• Produit Économique C :
  Stock actuel : 3 → Après : 0 unités
  État : 🔴 SIN STOCK

⚠️ Attention : Le produit C sera en rupture de stock !

Veux-tu continuer avec cette opération ?"""
    }
    
    def show_info_dialog():
        result = show_copyable_info(root, "Information", messages["info"])
        print(f"Dialogue info fermé, résultat : {result}")
    
    def show_success_dialog():
        result = show_copyable_success(root, "Succès", messages["success"])
        print(f"Dialogue succès fermé, résultat : {result}")
    
    def show_warning_dialog():
        result = show_copyable_warning(root, "Avertissement", messages["warning"])
        print(f"Dialogue avertissement fermé, résultat : {result}")
    
    def show_error_dialog():
        result = show_copyable_error(root, "Erreur", messages["error"])
        print(f"Dialogue erreur fermé, résultat : {result}")
    
    def show_confirm_dialog():
        result = show_copyable_confirm(root, "Confirmation", messages["confirm"])
        print(f"Dialogue confirmation fermé, résultat : {result}")
    
    # Boutons de test
    info_btn = ctk.CTkButton(
        buttons_frame,
        text="ℹ️ Test Message Info",
        command=show_info_dialog,
        height=40,
        font=ctk.CTkFont(size=14)
    )
    info_btn.pack(pady=10, padx=20, fill="x")
    
    success_btn = ctk.CTkButton(
        buttons_frame,
        text="✅ Test Message Succès",
        command=show_success_dialog,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="green",
        hover_color="darkgreen"
    )
    success_btn.pack(pady=10, padx=20, fill="x")
    
    warning_btn = ctk.CTkButton(
        buttons_frame,
        text="⚠️ Test Message Avertissement",
        command=show_warning_dialog,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="orange",
        hover_color="darkorange"
    )
    warning_btn.pack(pady=10, padx=20, fill="x")
    
    error_btn = ctk.CTkButton(
        buttons_frame,
        text="❌ Test Message Erreur",
        command=show_error_dialog,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="red",
        hover_color="darkred"
    )
    error_btn.pack(pady=10, padx=20, fill="x")
    
    confirm_btn = ctk.CTkButton(
        buttons_frame,
        text="🤔 Test Dialogue Confirmation",
        command=show_confirm_dialog,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="purple",
        hover_color="darkviolet"
    )
    confirm_btn.pack(pady=10, padx=20, fill="x")
    
    # Instructions
    instructions_frame = ctk.CTkFrame(root)
    instructions_frame.pack(fill="x", padx=20, pady=20)
    
    instructions_text = """
📋 INSTRUCTIONS DE TEST :

1. Clique sur chaque bouton pour tester les différents types de dialogues
2. Dans chaque dialogue :
   ✅ Vérifie que le texte est sélectionnable avec la souris
   ✅ Teste le bouton "📋 Copiar" pour copier le message
   ✅ Vérifie que le dialogue s'affiche au premier plan
   ✅ Teste les raccourcis clavier (Enter, Escape)
3. Pour les confirmations, teste les boutons "Sí" et "No"
4. Vérifie que le texte copié peut être collé ailleurs (Ctrl+V)
    """
    
    instructions_label = ctk.CTkLabel(
        instructions_frame,
        text=instructions_text,
        font=ctk.CTkFont(size=10),
        justify="left"
    )
    instructions_label.pack(padx=10, pady=10)
    
    print("Interface de test des dialogues copiables lancée.")
    print("Teste chaque type de dialogue et vérifie la fonctionnalité de copie.")
    
    root.mainloop()

if __name__ == "__main__":
    test_copyable_dialogs()
