# Correction des Tests Bloquants - Facturas

## 📋 Problèmes Identifiés

### Test 1: `test_factura_pdf_generation`
**Symptôme**: Le test bloque indéfiniment et nécessite Ctrl+C pour l'arrêter.

**Cause**: Le test clique sur le bouton "Generar PDF" qui ouvre une boîte de dialogue `QFileDialog` pour sauvegarder le fichier. Cette boîte de dialogue bloque l'exécution du test en attendant une interaction utilisateur qui ne vient jamais en mode automatisé.

### Test 2: `test_create_new_factura_basic`
**Symptôme**: Le test bloque indéfiniment

**Cause**: Le bouton "Nueva Factura" peut déclencher des dialogues de confirmation (via `ask_confirmation()` dans `cancel_edit()`) qui attendent une interaction utilisateur.

### Tests Dépendants
Les tests suivants appellent `test_create_new_factura_basic()` et héritent du même problème :
- `test_select_client_in_factura`
- `test_factura_totals_calculation`
- `test_factura_status_change`
- `test_add_product_to_factura` (appelle `test_select_client_in_factura`)

---

## ✅ Solutions Appliquées

### Solution 1: Mock du QFileDialog (test_factura_pdf_generation)

Le fixture `mock_filedialog` existe déjà dans `test/conftest.py` mais n'était pas utilisé par ce test.

**Modification**:
```python
@pytest.mark.timeout(10)
def test_factura_pdf_generation(self, mock_filedialog):
    # Mock du dialogue de sauvegarde de fichier pour éviter le blocage
    mock_filedialog.getSaveFileName.return_value = ('/tmp/test_factura.pdf', 'PDF Files (*.pdf)')
```

**Effet**: Simule la sélection d'un fichier par l'utilisateur, permettant au test de continuer sans interaction.

### Solution 2: Mock du QMessageBox (test_create_new_factura_basic et dépendants)

Tous les tests qui créent une nouvelle facture ont été modifiés pour utiliser le fixture `mock_messagebox` :

**Modification**:
```python
@pytest.mark.timeout(15)
def test_create_new_factura_basic(self, mock_messagebox):
    # Mock des dialogues pour éviter les blocages
    mock_messagebox.question.return_value = mock_messagebox.No
    mock_messagebox.information.return_value = mock_messagebox.Ok
```

**Effet**:
- `QMessageBox.question()` retourne automatiquement "No" (pas de confirmation)
- `QMessageBox.information()` retourne automatiquement "Ok"
- Aucune boîte de dialogue ne s'affiche

### Propagation du Mock

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

## 📊 Résumé des Tests Corrigés

| Test | Timeout | Mock | Statut |
|------|---------|------|--------|
| `test_factura_pdf_generation` | ✅ 10s | ✅ mock_filedialog | ✅ Corrigé |
| `test_create_new_factura_basic` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_select_client_in_factura` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_add_product_to_factura` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_factura_totals_calculation` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |
| `test_factura_status_change` | ✅ 15s | ✅ mock_messagebox | ✅ Corrigé |

---

## 📊 Résultat Global

| Avant | Après |
|-------|-------|
| ❌ 6 tests bloquent indéfiniment | ✅ 6 tests s'exécutent normalement |
| ❌ Nécessite Ctrl+C pour arrêter | ✅ Timeout de 10-15 secondes max |
| ❌ Empêche l'exécution des autres tests | ✅ Dialogues mockés |
| ❌ Aucune protection | ✅ Double protection (mock + timeout) |

---

## 🧪 Vérification

Pour vérifier la correction:

```bash
# Test spécifique
pytest test/behaviour/test_facturas_behaviour.py::TestFacturasBehaviour::test_factura_pdf_generation -v --headless

# Tous les tests de facturas
pytest test/behaviour/test_facturas_behaviour.py -v --headless

# Tous les tests de comportement
pytest test/behaviour/ -v --headless
```

---

## 📝 Fichiers Modifiés

1. ✅ **test/behaviour/test_facturas_behaviour.py**
   - `test_factura_pdf_generation` : Ajout mock_filedialog + timeout 10s
   - `test_create_new_factura_basic` : Ajout mock_messagebox + timeout 15s
   - `test_select_client_in_factura` : Ajout mock_messagebox + timeout 15s
   - `test_add_product_to_factura` : Ajout mock_messagebox + timeout 15s
   - `test_factura_totals_calculation` : Ajout mock_messagebox + timeout 15s
   - `test_factura_status_change` : Ajout mock_messagebox + timeout 15s

---

## 🔍 Analyse Technique

### Pourquoi les tests bloquaient ?

1. **QFileDialog** : Le bouton "Generar PDF" ouvre un dialogue de sauvegarde qui attend une interaction utilisateur

2. **QMessageBox** : Les méthodes `ask_confirmation()` et `show_error()` ouvrent des dialogues de confirmation/erreur

3. **Mode test headless** : En mode headless, les dialogues ne s'affichent pas mais bloquent quand même l'exécution

### Solution

Les mocks interceptent les appels à `QFileDialog` et `QMessageBox` avant qu'ils n'atteignent PyQt5, permettant aux tests de continuer sans interaction utilisateur.

---

## ✅ Conclusion

**6 tests de facturas** sont maintenant corrigés et ne bloquent plus. Les protections mises en place garantissent que les tests s'exécuteront rapidement et de manière fiable :

1. **Mock des dialogues** - Évite l'ouverture des boîtes de dialogue
2. **Timeout** - Limite le temps d'exécution à 10-15 secondes
3. **Propagation des mocks** - Les tests dépendants reçoivent les mocks nécessaires

Tous les tests peuvent maintenant être exécutés dans une suite de tests automatisée sans risque de blocage.

