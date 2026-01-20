> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🧪 TESTS GUI NON-BLOQUANTS

## 📋 **Problème Résolu**

**Problème :** Les tests d'interface graphique se bloquaient à cause des boîtes de dialogue (`messagebox.showinfo`, `messagebox.showerror`, etc.) qui attendent une interaction utilisateur.

**Solution :** Techniques pour créer des tests GUI non-bloquants et automatisés.

---

## 🔧 **Techniques de Test Non-Bloquant**

### **1. Mocking des Boîtes de Dialogue**

#### **Problème**
```python
# ❌ Code qui bloque les tests
def guardar_cliente(self):
    # ... logique de sauvegarde ...
    messagebox.showinfo("Succès", "Client sauvegardé")  # BLOQUE LE TEST
```

#### **Solution**
```python
def test_cliente_interface_simulation(self, temp_db):
    import tkinter.messagebox as messagebox
    
    # Sauvegarder la fonction originale
    original_showinfo = messagebox.showinfo
    
    try:
        # Remplacer par un mock non-bloquant
        messagebox.showinfo = lambda title, message: print(f"📝 {title}: {message}")
        
        # Exécuter le test
        clientes_window.guardar_cliente()  # Ne bloque plus
        
    finally:
        # Restaurer la fonction originale
        messagebox.showinfo = original_showinfo
```

### **2. Tests Sans Interface Graphique**

#### **Approche Directe**
```python
def test_cliente_logic_only(self):
    """Test de la logique métier sans GUI"""
    # Tester directement les modèles
    cliente = Cliente(nombre="Test", email="test@example.com")
    cliente_id = cliente.save()
    
    # Vérifier sans interface
    cliente_leido = Cliente.get_by_id(cliente_id)
    assert cliente_leido.nombre == "Test"
```

#### **Simulation de Saisie**
```python
def test_form_validation_only(self):
    """Test de validation sans affichage"""
    clientes_window = ClientesWindow(root)
    
    # Simuler la saisie
    clientes_window.nombre_entry.insert(0, "Test Client")
    clientes_window.email_entry.insert(0, "invalid-email")
    
    # Tester la validation (sans sauvegarder)
    errors = clientes_window.validate_form()
    assert "email" in str(errors).lower()
```

### **3. Fenêtres Cachées**

#### **Technique**
```python
def test_with_hidden_window(self):
    """Test avec fenêtre cachée"""
    root = ctk.CTk()
    root.withdraw()  # Cacher la fenêtre principale
    
    try:
        # Créer la fenêtre de test
        window = ClientesWindow(root)
        window.window.get_native_widget().withdraw()  # Cacher aussi cette fenêtre
        
        # Exécuter les tests
        # ...
        
    finally:
        root.destroy()
```

### **4. Tests avec Timeout**

#### **Protection Contre le Blocage**
```python
import signal
import pytest

def timeout_handler(signum, frame):
    raise TimeoutError("Test bloqué trop longtemps")

def test_with_timeout(self):
    """Test avec timeout de sécurité"""
    # Définir un timeout de 5 secondes
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)
    
    try:
        # Code de test potentiellement bloquant
        clientes_window.guardar_cliente()
        
    except TimeoutError:
        pytest.fail("Test bloqué par une boîte de dialogue")
    finally:
        signal.alarm(0)  # Annuler le timeout
```

---

## 🛠️ **Patterns de Test Recommandés**

### **1. Pattern Mock-Restore**
```python
class TestClientesNonBlocking:
    def setup_method(self):
        """Configuration avant chaque test"""
        import tkinter.messagebox as messagebox
        self.original_showinfo = messagebox.showinfo
        self.original_showerror = messagebox.showerror
        self.original_askyesno = messagebox.askyesno
        
        # Remplacer par des mocks
        messagebox.showinfo = self.mock_showinfo
        messagebox.showerror = self.mock_showerror
        messagebox.askyesno = self.mock_askyesno
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo = self.original_showinfo
        messagebox.showerror = self.original_showerror
        messagebox.askyesno = self.original_askyesno
    
    def mock_showinfo(self, title, message):
        print(f"INFO: {title} - {message}")
        return None
    
    def mock_showerror(self, title, message):
        print(f"ERROR: {title} - {message}")
        return None
    
    def mock_askyesno(self, title, message):
        print(f"QUESTION: {title} - {message}")
        return True  # Simuler "Oui"
```

### **2. Pattern Test Factory**
```python
class GUITestFactory:
    """Factory pour créer des composants GUI de test"""
    
    @staticmethod
    def create_hidden_window():
        """Crée une fenêtre cachée pour les tests"""
        root = ctk.CTk()
        root.withdraw()
        return root
    
    @staticmethod
    def mock_all_dialogs():
        """Mock toutes les boîtes de dialogue"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo = lambda t, m: print(f"INFO: {t}")
        messagebox.showerror = lambda t, m: print(f"ERROR: {t}")
        messagebox.askyesno = lambda t, m: True
    
    @staticmethod
    def create_test_client_window(parent=None):
        """Crée une fenêtre client pour les tests"""
        if parent is None:
            parent = GUITestFactory.create_hidden_window()
        
        GUITestFactory.mock_all_dialogs()
        return ClientesWindow(parent)
```

### **3. Pattern Assertion Helper**
```python
class GUIAssertions:
    """Helpers pour les assertions GUI"""
    
    @staticmethod
    def assert_field_value(widget, expected_value):
        """Vérifie la valeur d'un champ"""
        actual = widget.get() if hasattr(widget, 'get') else widget.get("1.0", "end-1c")
        assert actual.strip() == expected_value.strip()
    
    @staticmethod
    def assert_form_valid(form_window):
        """Vérifie qu'un formulaire est valide"""
        errors = form_window.validate_form()
        assert len(errors) == 0, f"Formulaire invalide: {errors}"
    
    @staticmethod
    def simulate_user_input(widget, value):
        """Simule une saisie utilisateur"""
        if hasattr(widget, 'delete'):
            widget.delete(0, 'end')
            widget.insert(0, value)
        elif hasattr(widget, 'set'):
            widget.set(value)
```

---

## ✅ **Exemple Complet de Test Non-Bloquant**

```python
def test_complete_client_workflow(self, temp_db):
    """Test complet du workflow client sans blocage"""
    
    # 1. Setup non-bloquant
    root = ctk.CTk()
    root.withdraw()
    
    # Mock des dialogues
    import tkinter.messagebox as messagebox
    original_showinfo = messagebox.showinfo
    messages_received = []
    
    def mock_showinfo(title, message):
        messages_received.append((title, message))
        return None
    
    messagebox.showinfo = mock_showinfo
    
    try:
        # 2. Créer l'interface
        clientes_window = ClientesWindow(root)
        
        # 3. Simuler la saisie utilisateur
        test_data = {
            "nombre": "Client Test Complet",
            "email": "test@complet.com",
            "telefono": "123456789"
        }
        
        for field, value in test_data.items():
            widget = getattr(clientes_window, f"{field}_entry")
            widget.delete(0, 'end')
            widget.insert(0, value)
        
        # 4. Tester la validation
        errors = clientes_window.validate_form()
        assert len(errors) == 0, f"Erreurs de validation: {errors}"
        
        # 5. Tester la sauvegarde (sans blocage)
        clientes_window.guardar_cliente()
        
        # 6. Vérifier que le message a été affiché
        assert len(messages_received) > 0, "Aucun message de confirmation"
        assert "sauvegardé" in messages_received[0][1].lower()
        
        # 7. Vérifier en base de données
        cliente = Cliente.get_by_nombre("Client Test Complet")
        assert cliente is not None
        assert cliente.email == "test@complet.com"
        
        # 8. Nettoyer
        cliente.delete()
        clientes_window.window.destroy()
        
    finally:
        # 9. Restaurer les fonctions originales
        messagebox.showinfo = original_showinfo
        root.destroy()
```

---

## 🎯 **Bonnes Pratiques**

### **À Faire ✅**
- ✅ **Toujours mocker** les boîtes de dialogue dans les tests
- ✅ **Cacher les fenêtres** avec `withdraw()`
- ✅ **Tester la logique** séparément de l'interface
- ✅ **Utiliser des timeouts** pour éviter les blocages
- ✅ **Nettoyer les ressources** dans `finally`

### **À Éviter ❌**
- ❌ **Afficher des fenêtres** pendant les tests automatisés
- ❌ **Laisser des dialogues** non mockés
- ❌ **Oublier de nettoyer** les ressources GUI
- ❌ **Tests dépendants** de l'interaction utilisateur
- ❌ **Timeouts trop longs** qui ralentissent les tests

---

## 🚀 **Résultat**

**Avec ces techniques, tous les tests GUI sont :**
- ✅ **Non-bloquants** : Pas d'attente d'interaction utilisateur
- ✅ **Automatisés** : Exécution complètement automatique
- ✅ **Rapides** : Pas de délais d'affichage
- ✅ **Fiables** : Résultats reproductibles
- ✅ **Maintenables** : Code de test propre et structuré

**État :** ✅ **IMPLÉMENTÉ ET TESTÉ**

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
