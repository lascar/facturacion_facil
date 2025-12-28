# Correction des Tests de Behaviour - Problèmes de Lenteur et Blocage

## 📊 Analyse Complète

**Date**: 2025-12-28  
**Problème**: 33 tests avec risques de blocage identifiés dans 8 fichiers

### Outils d'Analyse Créés

1. **`analyze_blocking_tests.py`** - Script d'analyse automatique des risques de blocage
2. **`fix_all_blocking_tests.py`** - Script de correction automatique (non utilisé finalement)

---

## ✅ Corrections Appliquées

### 1. test_facturas_behaviour.py ✅ (Déjà corrigé)

**Tests corrigés**: 6 tests
- `test_factura_pdf_generation` - timeout 10s + mock_filedialog
- `test_create_new_factura_basic` - timeout 20s + mock_messagebox
- `test_select_client_in_factura` - timeout 15s + mock_messagebox
- `test_add_product_to_factura` - timeout 15s + mock_messagebox
- `test_factura_totals_calculation` - timeout 20s + mock_messagebox
- `test_factura_status_change` - timeout 15s + mock_messagebox

**Modifications**:
- ✅ Mock MessageBox et FileDialog ajoutés au setup
- ✅ Configuration des 4 types de dialogues (question, information, warning, critical)
- ✅ Timeouts appropriés (10-20s)

---

### 2. test_clientes_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 6 tests
- `test_clientes_window_startup` - timeout 15s
- `test_create_new_client` - timeout 20s + mock
- `test_edit_existing_client` - timeout 20s + mock
- `test_delete_client` - timeout 20s + mock
- `test_client_form_validation` - timeout 20s + mock
- `test_client_without_nif` - timeout 20s + mock

**Modifications**:
```python
# setup_test signature modifiée
def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox):
    # Configuration des mocks
    mock_messagebox.question.return_value = mock_messagebox.No
    mock_messagebox.information.return_value = mock_messagebox.Ok
    mock_messagebox.warning.return_value = mock_messagebox.Ok
    mock_messagebox.critical.return_value = mock_messagebox.Ok
```

---

### 3. test_iva_modifiable_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 6 tests
- `test_iva_column_exists` - timeout 20s + mock
- `test_iva_recomendado_applied_by_default` - timeout 20s + mock
- `test_iva_modifiable_in_table` - timeout 20s + mock
- `test_totals_calculated_with_individual_iva` - timeout 25s + mock
- `test_save_and_load_factura_with_iva` - timeout 25s + mock
- `test_different_iva_rates_in_same_factura` - timeout 25s + mock

**Modifications**:
- ✅ Mock MessageBox ajouté au setup
- ✅ Timeouts 20-25s selon complexité du test

---

### 4. test_stock_window_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 5 tests
- `test_stock_window_layout_specification` - timeout 20s + mock
- `test_stock_adjustment_workflow_specification` - timeout 25s + mock
- `test_stock_status_indicators_specification` - timeout 20s + mock
- `test_guardar_button_behavior` - timeout 25s + mock
- `test_stock_persistence_after_guardar` - timeout 25s + mock

**Modifications**:
- ✅ Mock MessageBox ajouté au setup
- ✅ Timeouts 20-25s selon complexité

---

### 5. test_excel_export_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 4 tests
- `test_excel_stock_file_is_created` - timeout 15s
- `test_excel_stock_contains_product_data` - timeout 15s
- `test_excel_facturacion_file_is_created` - timeout 15s
- `test_excel_facturacion_contains_invoice_data` - timeout 15s

**Note**: Ces tests génèrent directement les fichiers Excel sans dialogues UI, donc pas besoin de mocks.

---

### 6. test_dialogs_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 2 tests
- `test_invoice_status_dialog_specification` - timeout 20s + mock
- `test_data_cleanup_dialog_specification` - timeout 20s + mock

**Modifications**:
- ✅ Mock MessageBox ajouté au setup
- ✅ Timeouts 20s

---

### 7. test_organizacion_directorio_informe_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 2 tests
- `test_05_directorio_informe_position_after_pdf` - timeout 25s + mocks
- `test_11_directorio_informe_saves_to_database` - timeout 25s + mocks

**Modifications**:
```python
# setup_test signature modifiée
def setup_test(self, app_instance, mock_messagebox, mock_filedialog):
    # Configuration des mocks MessageBox et FileDialog
    mock_messagebox.question.return_value = mock_messagebox.No
    mock_messagebox.information.return_value = mock_messagebox.Ok
    mock_messagebox.warning.return_value = mock_messagebox.Ok
    mock_messagebox.critical.return_value = mock_messagebox.Ok
    mock_filedialog.getSaveFileName.return_value = ('/tmp/test_export.pdf', 'PDF Files (*.pdf)')
    mock_filedialog.getExistingDirectory.return_value = '/tmp'
```

---

### 8. test_complete_application_behaviour.py ✅ CORRIGÉ

**Tests corrigés**: 4 tests
- `test_productos_window_complete_workflow` - timeout 30s + mocks
- `test_clientes_window_complete_workflow` - timeout 30s + mocks
- `test_facturas_window_complete_workflow` - timeout 30s + mocks
- `test_organizacion_window_configuration_workflow` - timeout 30s + mocks

**Modifications**:
- ✅ Mock MessageBox et FileDialog ajoutés au setup
- ✅ Timeouts 30s (tests complexes avec workflows complets)

---

## 📈 Résumé des Corrections

| Fichier | Tests | Mocks Ajoutés | Timeouts | Status |
|---------|-------|---------------|----------|--------|
| test_facturas_behaviour.py | 6 | MessageBox + FileDialog | 10-20s | ✅ |
| test_clientes_behaviour.py | 6 | MessageBox | 15-20s | ✅ |
| test_iva_modifiable_behaviour.py | 6 | MessageBox | 20-25s | ✅ |
| test_stock_window_behaviour.py | 5 | MessageBox | 20-25s | ✅ |
| test_excel_export_behaviour.py | 4 | Aucun (pas de dialogues) | 15s | ✅ |
| test_dialogs_behaviour.py | 2 | MessageBox | 20s | ✅ |
| test_organizacion_directorio_informe_behaviour.py | 2 | MessageBox + FileDialog | 25s | ✅ |
| test_complete_application_behaviour.py | 4 | MessageBox + FileDialog | 30s | ✅ |
| **TOTAL** | **35** | **7 fichiers** | **15-30s** | **✅** |

---

## 🎯 Impact des Corrections

### Avant
- ❌ 33+ tests pouvaient bloquer indéfiniment
- ❌ Nécessitait Ctrl+C pour arrêter les tests
- ❌ Suite de tests impossible à exécuter automatiquement
- ❌ CI/CD bloqué

### Après
- ✅ Tous les tests ont des timeouts appropriés (15-30s)
- ✅ Tous les dialogues sont mockés (pas de blocage)
- ✅ Suite complète exécutable automatiquement
- ✅ CI/CD fonctionnel

---

## 🧪 Vérification

```bash
# Tous les tests de behaviour
pytest test/behaviour/ -v --headless

# Tests spécifiques par fichier
pytest test/behaviour/test_clientes_behaviour.py -v --headless
pytest test/behaviour/test_iva_modifiable_behaviour.py -v --headless
pytest test/behaviour/test_stock_window_behaviour.py -v --headless
```

---

## 🔧 Technique Utilisée

### Double Protection
1. **Mocks** - Empêchent les dialogues de s'afficher
2. **Timeouts** - Garantissent que les tests ne bloquent jamais

### Configuration Standard des Mocks
```python
mock_messagebox.question.return_value = mock_messagebox.No
mock_messagebox.information.return_value = mock_messagebox.Ok
mock_messagebox.warning.return_value = mock_messagebox.Ok
mock_messagebox.critical.return_value = mock_messagebox.Ok
```

### Timeouts Adaptés
- Tests simples: 15-20s
- Tests moyens: 20-25s
- Tests complexes (workflows): 25-30s

