# Corrections des Segmentation Faults dans les Tests Manuels

## 🐛 Problème Initial

Les tests dans `test/manual/` causaient des **segmentation faults** lors de l'exécution avec pytest :

```
Fatal Python error: Segmentation fault
test/manual/test_iva_modifiable.py::test_iva_modifiable
```

## 🔍 Cause du Problème

Les tests manuels créaient des instances de `QApplication` directement sans utiliser les fixtures pytest appropriées, ce qui causait des problèmes lors du nettoyage automatique de pytest.

### Code Problématique (Avant)

```python
def test_iva_modifiable():
    app = QApplication(sys.argv)  # ❌ Création manuelle
    window = FacturasPyQt5Window()
    # ... tests ...
    # ❌ Pas de nettoyage propre
    return True

if __name__ == '__main__':
    success = test_iva_modifiable()
    sys.exit(0 if success else 1)
```

## ✅ Solution Appliquée

### 1. Transformation en Classes de Test Pytest

Tous les tests ont été transformés pour utiliser :
- La classe de base `BaseBehaviourTest`
- Les fixtures pytest (`app_instance`)
- Un nettoyage automatique et propre

### Code Corrigé (Après)

```python
class TestIVAModifiable(BaseBehaviourTest):
    """Tests pour vérifier que l'IVA est modifiable dans les factures"""

    def setup_test(self, app_instance):
        """Configuration du test avec l'instance de l'application"""
        self.app = app_instance['app']
        self.database = app_instance['database']
        self.main_window = app_instance['main_window']
        self.init_base_attributes()

    def test_iva_modifiable(self, app_instance):
        """Test de l'IVA modifiable dans factura"""
        self.setup_test(app_instance)
        
        window = FacturasPyQt5Window()
        window.show()
        self.app.processEvents()
        
        try:
            # ... tests ...
        finally:
            # ✅ Fermeture propre
            window.close()
            self.app.processEvents()
```

### 2. Création du conftest.py

Un fichier `test/manual/conftest.py` a été créé pour importer les fixtures du module `test/behaviour/` :

```python
from test.behaviour.conftest import (
    app_instance,
    isolated_test_database,
    test_database_path,
    # ... autres fixtures
)
```

## 📋 Tests Corrigés

1. ✅ `test_iva_modifiable.py` - Test de l'IVA modifiable
2. ✅ `test_dni_opcional_ui.py` - Test du DNI optionnel
3. ✅ `test_nuevo_cliente_guardar_button.py` - Test du bouton Guardar

## 🧪 Résultats

### Avant
```
test/manual/test_iva_modifiable.py::test_iva_modifiable 
Fatal Python error: Segmentation fault
```

### Après
```
test/manual/test_iva_modifiable.py::TestIVAModifiable::test_iva_modifiable PASSED
test/manual/test_dni_opcional_ui.py::TestDNIOpcionalUI::test_dni_opcional_validation PASSED
test/manual/test_dni_opcional_ui.py::TestDNIOpcionalUI::test_cliente_creation_without_dni PASSED
test/manual/test_dni_opcional_ui.py::TestDNIOpcionalUI::test_factura_creation_with_client_without_dni PASSED
test/manual/test_nuevo_cliente_guardar_button.py::TestNuevoClienteGuardarButton::test_nuevo_cliente_guardar_button PASSED

========================= 5 passed, 1 warning in 4.61s =========================
```

## 🎯 Avantages de la Solution

1. **Plus de segfaults** - Nettoyage automatique et propre des ressources PyQt5
2. **Isolation des tests** - Chaque test utilise une base de données de test isolée
3. **Meilleure intégration** - Les tests suivent maintenant les conventions pytest
4. **Réutilisabilité** - Utilisation de la classe de base `BaseBehaviourTest`
5. **Maintenabilité** - Code plus structuré et facile à maintenir

## 📚 Références

- `test/behaviour/base_behaviour_test.py` - Classe de base pour les tests
- `test/behaviour/conftest.py` - Configuration des fixtures pytest
- `INSTRUCTIONS_TESTS_BEHAVIOUR_SANS_BLOCAGE.md` - Guide des tests de comportement

## 🚀 Exécution

```bash
# Exécuter tous les tests manuels
pytest test/manual/ -v

# Exécuter un test spécifique
pytest test/manual/test_iva_modifiable.py -v -s

# Exécuter avec pytest direct
/home/pascal/.pyenv/versions/3.13.7/bin/pytest test/manual/ -v
```

---

**Date de correction** : 2024-12-31  
**Statut** : ✅ Résolu

