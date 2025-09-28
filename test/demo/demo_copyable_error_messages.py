#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration des messages d'erreur copiables dans l'interface de produits
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from ui.productos import ProductosWindow
from database.database import db
from utils.logger import get_logger

def demo_copyable_error_messages():
    """Démonstration des messages d'erreur copiables"""
    
    print("🧪 DÉMONSTRATION - Messages d'erreur copiables")
    print("=" * 60)
    
    # Initialiser la base de données
    db.initialize()
    
    # Créer l'application principale
    app = ctk.CTk()
    app.title("Demo - Messages Copiables")
    app.geometry("400x300")
    
    # Logger
    logger = get_logger("demo_copyable")
    
    def test_error_message():
        """Test d'un message d'erreur copiable"""
        try:
            # Ouvrir la fenêtre de produits
            productos_window = ProductosWindow(app)
            
            # Simuler une erreur de validation en essayant de sauvegarder un produit vide
            print("\n1️⃣ Test de validation avec champs vides...")
            print("   - Ouvrir la fenêtre de produits")
            print("   - Cliquer sur 'Guardar' sans remplir les champs")
            print("   - Le message d'erreur devrait être copiable")
            
            # Forcer une erreur de validation
            productos_window.nombre_entry.delete(0, 'end')  # Vider le nom
            productos_window.referencia_entry.delete(0, 'end')  # Vider la référence
            productos_window.precio_entry.delete(0, 'end')  # Vider le prix
            productos_window.precio_entry.insert(0, "prix_invalide")  # Prix invalide
            
            # Déclencher la validation (cela devrait montrer un message d'erreur copiable)
            productos_window.guardar_producto()
            
            logger.info("✅ Test de message d'erreur copiable déclenché")
            
        except Exception as e:
            logger.error(f"❌ Erreur dans le test: {e}")
    
    def test_success_message():
        """Test d'un message de succès copiable"""
        try:
            # Ouvrir la fenêtre de produits
            productos_window = ProductosWindow(app)
            
            print("\n2️⃣ Test de message de succès...")
            print("   - Remplir un produit valide")
            print("   - Sauvegarder")
            print("   - Le message de succès devrait être copiable")
            
            # Remplir avec des données valides
            productos_window.nombre_entry.delete(0, 'end')
            productos_window.nombre_entry.insert(0, "Producto Demo Copiable")
            
            productos_window.referencia_entry.delete(0, 'end')
            productos_window.referencia_entry.insert(0, "DEMO-COPY-001")
            
            productos_window.precio_entry.delete(0, 'end')
            productos_window.precio_entry.insert(0, "19.99")
            
            productos_window.categoria_entry.delete(0, 'end')
            productos_window.categoria_entry.insert(0, "Demo")
            
            # Sauvegarder (cela devrait montrer un message de succès copiable)
            productos_window.guardar_producto()
            
            logger.info("✅ Test de message de succès copiable déclenché")
            
        except Exception as e:
            logger.error(f"❌ Erreur dans le test de succès: {e}")
    
    # Créer l'interface de test
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    title_label = ctk.CTkLabel(
        main_frame,
        text="🧪 Demo Messages Copiables",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=20)
    
    info_label = ctk.CTkLabel(
        main_frame,
        text="Haz clic en los botones para probar los mensajes copiables.\n"
             "Los mensajes tendrán un botón '📋 Copiar' para copiar el texto.",
        font=ctk.CTkFont(size=12),
        wraplength=350
    )
    info_label.pack(pady=10)
    
    # Botón para test de error
    error_btn = ctk.CTkButton(
        main_frame,
        text="🚨 Probar Mensaje de Error Copiable",
        command=test_error_message,
        fg_color="#dc3545",
        hover_color="#c82333",
        height=40
    )
    error_btn.pack(pady=10, fill="x")
    
    # Botón para test de éxito
    success_btn = ctk.CTkButton(
        main_frame,
        text="✅ Probar Mensaje de Éxito Copiable",
        command=test_success_message,
        fg_color="#28a745",
        hover_color="#218838",
        height=40
    )
    success_btn.pack(pady=10, fill="x")
    
    # Instrucciones
    instructions_frame = ctk.CTkFrame(main_frame)
    instructions_frame.pack(fill="x", pady=20)
    
    instructions_label = ctk.CTkLabel(
        instructions_frame,
        text="📋 Instrucciones:\n\n"
             "1. Haz clic en cualquier botón de prueba\n"
             "2. Se abrirá la ventana de productos\n"
             "3. Aparecerá un mensaje con botón 'Copiar'\n"
             "4. Haz clic en 'Copiar' para copiar el mensaje\n"
             "5. Pega el mensaje donde necesites (Ctrl+V)",
        font=ctk.CTkFont(size=11),
        justify="left"
    )
    instructions_label.pack(padx=10, pady=10)
    
    # Botón salir
    exit_btn = ctk.CTkButton(
        main_frame,
        text="❌ Salir",
        command=app.quit,
        fg_color="#6c757d",
        hover_color="#5a6268"
    )
    exit_btn.pack(pady=10)
    
    print("\n📋 Instrucciones:")
    print("1. Haz clic en los botones para probar los mensajes copiables")
    print("2. Los mensajes de error/éxito tendrán un botón '📋 Copiar'")
    print("3. Usa el botón para copiar el mensaje al portapapeles")
    print("4. Pega donde necesites con Ctrl+V")
    print("\n🎯 Objetivo: Verificar que todos los mensajes son copiables")
    
    # Ejecutar la aplicación
    app.mainloop()

if __name__ == "__main__":
    demo_copyable_error_messages()
