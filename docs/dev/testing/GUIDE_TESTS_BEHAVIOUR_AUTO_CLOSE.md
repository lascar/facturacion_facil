> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔄 Guide des Tests de Comportement avec Fermeture Automatique

## 🎯 Problème Résolu

**Avant** : Les fenêtres PyQt5 restaient ouvertes pendant les tests de comportement, bloquant l'exécution des tests automatisés.

**Maintenant** : Fermeture automatique et robuste de toutes les fenêtres après chaque test.

## 🏗️ Architecture de la Solution

### 1. **Classe de Base Améliorée** (`base_behaviour_test.py`)

```python
class BaseBehaviourTest:
    def teardown_method(self, method):
        """Nettoyage automatique après chaque test"""
        self.close_all_windows()  # Fermeture robuste
        
    def close_all_windows(self):
        """Fermeture robuste de toutes les fenêtres"""
        # 1. Fermer toutes les fenêtres top-level
        # 2. Forcer la fermeture des fenêtres restantes
        # 3. Traitement des événements pour finaliser
```

### 2. **Méthode de Fermeture Automatique**

```python
def open_window_with_auto_close(self, window_opener_func, test_duration=2.0):
    """Ouvrir une fenêtre avec fermeture automatique programmée"""
    window = window_opener_func()
    
    # Timer pour fermeture automatique
    timer = QTimer()
    timer.timeout.connect(lambda: window.close())
    timer.start(int(test_duration * 1000))
    
    return window
```

## 🚀 Utilisation dans les Tests

### ✅ **Nouvelle Approche (Recommandée)**

```python
class TestMonComportement(BaseBehaviourTest):
    
    def test_fenetre_stock(self):
        """Test avec fermeture automatique"""
        # Note: Les fenêtres se ferment automatiquement via teardown_method()
        
        def open_stock():
            return self.main_window.open_stock_window()
        
        # Ouverture avec fermeture automatique après 3 secondes
        stock_window = self.open_window_with_auto_close(
            open_stock, 
            test_duration=3.0
        )
        
        # Faire les tests...
        assert stock_window.isVisible()
        
        # Pas besoin de fermer manuellement !
        # teardown_method() s'en charge automatiquement
```

### ❌ **Ancienne Approche (À Éviter)**

```python
def test_fenetre_stock_old(self):
    """Ancienne approche qui bloque"""
    stock_window = self.main_window.open_stock_window()
    
    # Tests...
    
    stock_window.close()  # ❌ Peut ne pas fonctionner
    self.wait_and_process_events(5000)  # ❌ Attente trop longue
```

## 🔧 Correction des Tests Existants

### Script de Correction Automatique

```bash
# Corriger automatiquement tous les tests
python fix_behaviour_tests_auto_close.py
```

### Corrections Manuelles

1. **Supprimer les appels manuels** :
   ```python
   # ❌ Avant
   stock_window.close()
   self.wait_and_process_events(5000)
   
   # ✅ Après
   # Fermeture automatique gérée par teardown_method()
   self.wait_and_process_events(1000)
   ```

2. **Hériter de la classe de base** :
   ```python
   from test.behaviour.base_behaviour_test import BaseBehaviourTest
   
   class MonTest(BaseBehaviourTest):  # ✅ Hérite de la classe de base
   ```

3. **Utiliser les fixtures pytest** :
   ```python
   @pytest.fixture(autouse=True)
   def setup_test(self, app_instance, test_config, screenshots_dir):
       """Configuration automatique"""
       self.init_base_attributes()  # ✅ Initialise les attributs de base
   ```

## 📊 Mécanismes de Fermeture

### 1. **Fermeture Immédiate** (teardown_method)
- Appelée automatiquement après chaque test
- Ferme toutes les fenêtres top-level
- Force la fermeture des fenêtres récalcitrantes

### 2. **Fermeture Programmée** (QTimer)
- Timer automatique pour les tests longs
- Fermeture après durée spécifiée
- Évite les blocages

### 3. **Fermeture Forcée** (deleteLater)
- Pour les fenêtres qui résistent
- Suppression complète du widget
- Dernier recours

## 🧪 Tests de Validation

### Test Simple
```bash
# Test de l'exemple de fermeture automatique
python test/behaviour/test_auto_close_example.py
```

### Test Complet
```bash
# Tous les tests de comportement
pytest test/behaviour/ -v -s
```

### Vérification
```bash
# Vérifier qu'aucune fenêtre ne reste ouverte
ps aux | grep python  # Aucun processus PyQt5 en attente
```

## 📋 Bonnes Pratiques

### ✅ **À Faire**
- Hériter de `BaseBehaviourTest`
- Utiliser `open_window_with_auto_close()` pour les tests longs
- Laisser `teardown_method()` gérer la fermeture
- Utiliser des durées de test courtes (1-3 secondes)

### ❌ **À Éviter**
- Appeler manuellement `window.close()`
- Utiliser des attentes longues (>2 secondes)
- Oublier d'hériter de la classe de base
- Créer des timers manuels

## 🔍 Débogage

### Fenêtres qui ne se ferment pas
```python
# Ajouter des logs pour diagnostiquer
self.logger.debug(f"Fenêtres ouvertes: {len(self.app.allWidgets())}")

# Forcer la fermeture en cas de problème
self.close_all_windows()
```

### Tests qui traînent
```python
# Réduire la durée des tests
self.open_window_with_auto_close(open_func, test_duration=1.0)  # 1 seconde max
```

## 🎯 Résultat

**Avant** : Tests bloqués, fenêtres ouvertes indéfiniment
**Maintenant** : Tests fluides, fermeture automatique garantie

Les tests de comportement peuvent maintenant s'exécuter en série sans intervention manuelle ! 🚀

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
