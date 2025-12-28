# Correction des Tests Bloquants - Facturas

## 📋 Problèmes Identifiés

### Test 1: `test_create_new_factura_basic`
**Symptôme**: Le test bloque indéfiniment

**Cause**: Le bouton "Nueva Factura" peut déclencher des dialogues de confirmation (via `ask_confirmation()` dans `cancel_edit()`) qui attendent une interaction utilisateur.

### Tests Dépendants
Les tests suivants appellent `test_create_new_factura_basic()` et héritent du même problème :
- `test_select_client_in_factura`
- `test_factura_totals_calculation`
- `test_factura_status_change`

---

## ✅ Solutions Appliquées

### 1. Mock des Dialogues QMessageBox

Tous les tests ont été modifiés pour utiliser le fixture `mock_messagebox` :

```python
@pytest.mark.timeout(15)
def test_create_new_factura_basic(self, mock_messagebox):
    """Test de création d'une nouvelle facture basique"""
    self.logger.info("🧪 Test: Création nouvelle facture basique")
    
    # Mock des dialogues pour éviter les blocages
    mock_messagebox.question.return_value = mock_messagebox.No
    mock_messagebox.information.return_value = mock_messagebox.Ok
    
    # ... reste du test
```

**Effet**: 
- `QMessageBox.question()` retourne automatiquement "No" (pas de confirmation)
- `QMessageBox.information()` retourne automatiquement "Ok"
- Aucune boîte de dialogue ne s'affiche

### 2. Timeout de Sécurité

Tous les tests ont un timeout de 15 secondes :

```python
@pytest.mark.timeout(15)
```

**Effet**: Si un test bloque malgré les mocks, il échouera après 15 secondes au lieu de bloquer indéfiniment.

### 3. Propagation du Mock

Les tests qui appellent `test_create_new_factura_basic()` passent maintenant le mock :

```python
def test_select_client_in_factura(self, mock_messagebox):
    # Mock des dialogues
    mock_messagebox.question.return_value = mock_messagebox.No
    mock_messagebox.information.return_value = mock_messagebox.Ok
    
    # Créer une nouvelle facture avec le mock
    self.test_create_new_factura_basic(mock_messagebox)
```

---

## 📊 Tests Corrigés

| Test | Timeout | Mock | Statut |
|------|---------|------|--------|
| `test_create_new_factura_basic` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_select_client_in_factura` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_factura_totals_calculation` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_factura_status_change` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_factura_pdf_generation` | ✅ 10s | ✅ mock_filedialog | ✅ Corrigé (précédemment) |

---

## 🧪 Vérification

Pour vérifier les corrections :

```bash
# Test spécifique
pytest test/behaviour/test_facturas_behaviour.py::TestFacturasBehaviour::test_create_new_factura_basic -v --headless

# Tous les tests de facturas
pytest test/behaviour/test_facturas_behaviour.py -v --headless

# Tous les tests de comportement
pytest test/behaviour/ -v --headless
```

---

## 📝 Fichiers Modifiés

1. ✅ **test/behaviour/test_facturas_behaviour.py**
   - `test_create_new_factura_basic` : Ajout mock_messagebox + timeout
   - `test_select_client_in_factura` : Ajout mock_messagebox + timeout
   - `test_factura_totals_calculation` : Ajout mock_messagebox + timeout
   - `test_factura_status_change` : Ajout mock_messagebox + timeout
   - `test_factura_pdf_generation` : Ajout mock_filedialog + timeout (précédemment)

---

## 🔍 Analyse Technique

### Pourquoi les tests bloquaient ?

1. **Dialogues de confirmation** : La méthode `cancel_edit()` dans `facturas_pyqt5.py` appelle `ask_confirmation()` qui ouvre un `QMessageBox.question()`

2. **Génération de numéro** : La méthode `new_factura_inline()` génère un numéro de facture et peut afficher des erreurs via `show_error()`

3. **Mode test headless** : En mode headless, les dialogues ne s'affichent pas mais bloquent quand même l'exécution

### Solution

Les mocks interceptent les appels à `QMessageBox` avant qu'ils n'atteignent PyQt5, permettant aux tests de continuer sans interaction utilisateur.

---

## ✅ Résultat

| Avant | Après |
|-------|-------|
| ❌ 5 tests bloquent | ✅ 5 tests s'exécutent normalement |
| ❌ Nécessite Ctrl+C | ✅ Timeout de 10-15 secondes max |
| ❌ Empêche les autres tests | ✅ Dialogues mockés |
| ❌ Aucune protection | ✅ Double protection (mock + timeout) |

**Tous les tests de facturas peuvent maintenant s'exécuter automatiquement sans blocage.**

