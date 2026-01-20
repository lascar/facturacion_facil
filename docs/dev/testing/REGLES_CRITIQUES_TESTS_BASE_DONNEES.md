# 🚨 RÈGLES CRITIQUES : Tests et Base de Données

## ⚠️ AVERTISSEMENT CRITIQUE

**TOUTE VIOLATION DE CES RÈGLES EST CONSIDÉRÉE COMME UN INCIDENT GRAVE**

Ces règles ont été établies suite à une violation des standards de sécurité de la base de données lors du développement de tests. Elles sont **NON NÉGOCIABLES** et s'appliquent à **TOUS** les développements, y compris les tests "temporaires" ou "de développement".

## ❌ INTERDICTIONS ABSOLUES

### 1. **Bases de données temporaires**
```python
# ❌ INTERDIT - Ne JAMAIS faire cela
import tempfile
temp_dir = tempfile.mkdtemp()
test_db_path = os.path.join(temp_dir, 'test_facturacion.db')
db = DatabaseImproved(test_db_path)  # VIOLATION GRAVE
```

### 2. **Modification du chemin de base de données**
```python
# ❌ INTERDIT - Ne JAMAIS faire cela
original_db_path = DatabaseImproved.DB_PATH
DatabaseImproved.DB_PATH = test_db_path  # VIOLATION GRAVE
```

### 3. **Création/modification de données dans les tests**
```python
# ❌ INTERDIT - Ne JAMAIS faire cela
db.add_product(test_data)  # VIOLATION GRAVE
db.execute_query("INSERT INTO...")  # VIOLATION GRAVE
db.execute_query("DELETE FROM...")  # VIOLATION GRAVE
db.execute_query("UPDATE...")  # VIOLATION GRAVE
```

### 4. **Modification de structure même temporaire**
```python
# ❌ INTERDIT - Ne JAMAIS faire cela
db.execute_query("ALTER TABLE...")  # VIOLATION GRAVE
db.execute_query("DROP TABLE...")  # VIOLATION GRAVE
db.execute_query("CREATE TABLE...")  # VIOLATION GRAVE
```

## ✅ PRATIQUES AUTORISÉES

### 1. **Tests en lecture seule**
```python
# ✅ AUTORISÉ - Lecture des données existantes
window = ProductosPyQt5Window()
window.load_productos()
row_count = window.products_table.rowCount()
```

### 2. **Validation d'interface**
```python
# ✅ AUTORISÉ - Tests de structure d'interface
headers = []
for col in range(window.products_table.columnCount()):
    header = window.products_table.horizontalHeaderItem(col)
    if header:
        headers.append(header.text())
assert "Categoría" in headers
```

### 3. **Tests de logique métier sans modification**
```python
# ✅ AUTORISÉ - Tests de comportement d'interface
window.categoria_combo.setCurrentText('Test Category')
current_text = window.categoria_combo.currentText()
assert current_text == 'Test Category'
```

## 🛡️ PROTECTION DE LA BASE DE DONNÉES

### **Principe fondamental**
La base de données de production `facturacion.db` est **SACRÉE**. Elle contient les données critiques de l'entreprise et ne doit **JAMAIS** être mise en danger, même par des tests.

### **Conséquences des violations**
- **Perte de données** : Incident grave avec impact business
- **Corruption de base** : Arrêt complet du système
- **Perte de confiance** : Impact sur la fiabilité du système

## 📋 CHECKLIST AVANT TOUT TEST

Avant de créer un test, vérifier :

- [ ] ❌ Le test ne crée PAS de base de données temporaire
- [ ] ❌ Le test ne modifie PAS le chemin de base de données
- [ ] ❌ Le test ne crée PAS de données
- [ ] ❌ Le test ne modifie PAS de données existantes
- [ ] ❌ Le test ne supprime PAS de données
- [ ] ❌ Le test ne modifie PAS la structure de base
- [ ] ✅ Le test utilise UNIQUEMENT la base existante
- [ ] ✅ Le test fonctionne en lecture seule
- [ ] ✅ Le test valide l'interface utilisateur
- [ ] ✅ Le test respecte le système de migration officiel

## 🚀 EXEMPLES DE TESTS CONFORMES

### **Test de régression d'interface**
```python
def test_categoria_column_exists(self):
    """Test: Vérifier que la colonne 'Categoría' existe."""
    window = ProductosPyQt5Window()
    
    headers = []
    for col in range(window.products_table.columnCount()):
        header = window.products_table.horizontalHeaderItem(col)
        if header:
            headers.append(header.text())
    
    assert "Categoría" in headers
```

### **Test d'intégration lecture seule**
```python
def test_categoria_display_with_real_data(self):
    """Test: Affichage des catégories avec données réelles."""
    window = ProductosPyQt5Window()
    window.load_productos()
    
    row_count = window.products_table.rowCount()
    if row_count > 0:
        # Validation de l'affichage des données existantes
        categoria_col = 5
        for row in range(min(3, row_count)):
            item = window.products_table.item(row, categoria_col)
            assert item is not None
```

## 📝 DOCUMENTATION OBLIGATOIRE

Chaque test doit inclure un commentaire expliquant :
- **Objectif** : Ce que le test valide
- **Méthode** : Comment il procède (lecture seule)
- **Données** : Quelles données il utilise (existantes)
- **Sécurité** : Confirmation qu'il ne modifie rien

## 🔄 RÉVISION ET CONTRÔLE

- **Code review** : Tout test doit être revu avant intégration
- **Validation** : Confirmer le respect des règles avant exécution
- **Documentation** : Mettre à jour ce document si nécessaire

---

**Date de création** : 2025-12-07  
**Raison** : Violation des règles de sécurité base de données  
**Statut** : **RÈGLES ACTIVES ET OBLIGATOIRES**  
**Révision** : Annuelle ou après incident
