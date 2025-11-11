#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation de la couche d'abstraction GUI
"""

try:
    from .abstract_components import AbstractForm, AbstractListWindow
    from .gui_manager import get_gui_manager, set_gui_framework
except ImportError:
    # Import absolu si exécuté directement
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from gui.abstract_components import AbstractForm, AbstractListWindow
    from gui.gui_manager import get_gui_manager, set_gui_framework
from typing import List

class ExampleClientForm(AbstractForm):
    """Exemple de formulaire client utilisant l'abstraction"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Formulaire Client", "500x400")
        self.show()
    
    def create_widgets(self):
        """Crée les widgets du formulaire"""
        # Ajouter les champs
        self.add_field("nombre", "Nom *:", "entry", placeholder_text="Nom complet")
        self.add_field("email", "Email:", "entry", placeholder_text="email@exemple.com")
        self.add_field("telefono", "Téléphone:", "entry", placeholder_text="123456789")
        self.add_field("direccion", "Adresse:", "text", height=80)
        
        # Ajouter les boutons
        self.add_button("guardar", "Guardar", command=self.save_client)
        self.add_button("limpiar", "Limpiar", command=self.clear_form)
        self.add_button("cancelar", "Cancelar", command=self.destroy)
    
    def save_client(self):
        """Sauvegarde le client"""
        # Valider
        errors = self.validate_form()
        if errors:
            self.gui_factory.show_message("error", "Erreurs", "\n".join(errors))
            return
        
        # Récupérer les valeurs
        nombre = self.get_field_value("nombre")
        email = self.get_field_value("email")
        telefono = self.get_field_value("telefono")
        direccion = self.get_field_value("direccion")
        
        # Simuler la sauvegarde
        print(f"Client sauvegardé: {nombre}, {email}, {telefono}")
        
        self.gui_factory.show_message("info", "Succès", f"Client '{nombre}' sauvegardé avec succès")
        self.clear_form()
    
    def validate_form(self) -> List[str]:
        """Valide le formulaire"""
        errors = []
        
        nombre = self.get_field_value("nombre").strip()
        if not nombre:
            errors.append("Le nom est obligatoire")
        
        email = self.get_field_value("email").strip()
        if email and "@" not in email:
            errors.append("Format d'email invalide")
        
        return errors

class ExampleClientList(AbstractListWindow):
    """Exemple de liste de clients utilisant l'abstraction"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Liste des Clients", "800x600")
        self.set_columns(["Nom", "Email", "Téléphone"])
        self.show()
    
    def create_widgets(self):
        """Crée les widgets de la fenêtre"""
        # Créer les widgets de liste
        self.create_list_widgets()
        
        # Ajouter des boutons d'action
        actions_frame = self.gui_factory.create_frame(self.window)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        new_btn = self.gui_factory.create_button(
            actions_frame, text="Nouveau Client", command=self.new_client
        )
        new_btn.pack(side="left", padx=5)
        
        edit_btn = self.gui_factory.create_button(
            actions_frame, text="Modifier", command=self.edit_client
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = self.gui_factory.create_button(
            actions_frame, text="Supprimer", command=self.delete_client
        )
        delete_btn.pack(side="left", padx=5)
        
        # Charger les données
        self.load_data()
        
        # Bind événements
        native_tree = self.treeview.get_native_widget()
        native_tree.bind("<<TreeviewSelect>>", self.on_item_selected)
    
    def load_data(self):
        """Charge les données de test"""
        # Données de test
        test_clients = [
            ("Juan Pérez", "juan@example.com", "123456789"),
            ("María García", "maria@example.com", "987654321"),
            ("Carlos López", "carlos@example.com", "555666777"),
        ]
        
        self.clear_list()
        for client in test_clients:
            self.add_item(list(client))
    
    def on_item_selected(self, event=None):
        """Gère la sélection d'un élément"""
        selected = self.get_selected_item()
        if selected:
            values = selected['values']
            print(f"Client sélectionné: {values[0]}")
    
    def new_client(self):
        """Crée un nouveau client"""
        form = ExampleClientForm(self.window)
    
    def edit_client(self):
        """Modifie le client sélectionné"""
        selected = self.get_selected_item()
        if selected:
            values = selected['values']
            self.gui_factory.show_message("info", "Modifier", f"Modification de {values[0]}")
        else:
            self.gui_factory.show_message("warning", "Attention", "Sélectionnez un client à modifier")
    
    def delete_client(self):
        """Supprime le client sélectionné"""
        selected = self.get_selected_item()
        if selected:
            values = selected['values']
            if self.gui_factory.show_message("question", "Confirmer", 
                                            f"Supprimer le client '{values[0]}' ?"):
                # Simuler la suppression
                native_tree = self.treeview.get_native_widget()
                for item in native_tree.selection():
                    native_tree.delete(item)
                self.gui_factory.show_message("info", "Supprimé", "Client supprimé avec succès")
        else:
            self.gui_factory.show_message("warning", "Attention", "Sélectionnez un client à supprimer")

def demo_customtkinter():
    """Démonstration avec CustomTkinter"""
    print("🎨 Démonstration avec CustomTkinter")
    
    # Définir le framework
    set_gui_framework('customtkinter')
    
    # Créer l'application
    manager = get_gui_manager()
    app = manager.create_application()
    app.initialize()
    
    # Créer la liste de clients
    client_list = ExampleClientList()
    
    # Lancer l'application
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application interrompue")

def demo_tkinter():
    """Démonstration avec Tkinter standard"""
    print("🖼️ Démonstration avec Tkinter standard")
    
    # Définir le framework
    set_gui_framework('tkinter')
    
    # Créer l'application
    manager = get_gui_manager()
    app = manager.create_application()
    app.initialize()
    
    # Créer la liste de clients
    client_list = ExampleClientList()
    
    # Lancer l'application
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application interrompue")

def demo_framework_switching():
    """Démonstration du changement de framework"""
    print("🔄 Démonstration du changement de framework")
    
    frameworks = ['customtkinter', 'tkinter']
    
    for framework in frameworks:
        print(f"\n--- Test avec {framework} ---")
        
        try:
            set_gui_framework(framework)
            manager = get_gui_manager()
            
            print(f"Framework actuel: {manager.get_current_framework()}")
            print(f"Factory: {type(manager.get_factory()).__name__}")
            
            # Créer une fenêtre de test simple
            factory = manager.get_factory()
            window = factory.create_window(f"Test {framework}", "400x300")
            
            frame = factory.create_frame(window)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            label = factory.create_label(frame, text=f"Interface avec {framework}")
            label.pack(pady=10)
            
            button = factory.create_button(
                frame, 
                text="Fermer", 
                command=lambda: window.get_native_widget().quit()
            )
            button.pack(pady=10)
            
            print(f"✅ Interface créée avec {framework}")
            
            # Ne pas lancer mainloop pour les tests automatiques
            # window.get_native_widget().mainloop()
            
        except Exception as e:
            print(f"❌ Erreur avec {framework}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "customtkinter":
            demo_customtkinter()
        elif sys.argv[1] == "tkinter":
            demo_tkinter()
        elif sys.argv[1] == "switch":
            demo_framework_switching()
        else:
            print("Usage: python example_usage.py [customtkinter|tkinter|switch]")
    else:
        demo_framework_switching()
