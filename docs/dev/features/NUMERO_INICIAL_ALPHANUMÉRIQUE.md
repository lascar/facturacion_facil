> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔢 NUMÉRO INITIAL ALPHANUMÉRIQUE

## 📋 **Vue d'ensemble**

Amélioration du champ "Número inicial" dans la configuration de l'organisation pour supporter les formats alphanumériques comme "2025-FACT-001", "INV-123", etc.

**Avant :** Seulement des nombres entiers (1, 100, 2025)
**Après :** Formats alphanumériques complets (2025-FACT-001, INV-123, SÉRIE-A-001)

---

## 🎯 **Problème Résolu**

### **Erreur Précédente**
```
Por favor, corrija los siguientes errores:
• El número inicial debe ser un número válido
```

### **Cause**
- Le code tentait de convertir le numéro initial en entier avec `int()`
- Les formats comme "2025-FACT-001" échouaient à la conversion
- La base de données stockait le champ comme `INTEGER`

---

## ✅ **Solution Implémentée**

### **1. Migration de Base de Données**
- **Changement de type** : `INTEGER` → `TEXT`
- **Migration automatique** : Conversion des données existantes
- **Compatibilité** : Préservation des données existantes

### **2. Validation Améliorée**
```python
# Nouvelle validation alphanumérique
numero_inicial_str = self.numero_inicial_entry.get().strip()

if len(numero_inicial_str) > 50:
    errors.append("El número inicial es demasiado largo (máximo 50 caracteres)")
elif not any(c.isalnum() for c in numero_inicial_str):
    errors.append("El número inicial debe contener al menos un número o letra")
```

### **3. Formats Supportés**
- ✅ **Nombres simples** : `1`, `100`, `2025`
- ✅ **Avec tirets** : `2025-FACT-001`, `INV-123`
- ✅ **Avec underscores** : `FACTURA_123`, `DOC_2025`
- ✅ **Avec slashes** : `2025/01/001`, `FACT/2025`
- ✅ **Mixtes** : `F001`, `123ABC`, `SÉRIE-A-001`
- ✅ **Maximum 50 caractères**
- ✅ **Au moins un caractère alphanumérique**

---

## 🔧 **Modifications Techniques**

### **Base de Données (`database/database.py`)**
```python
# Avant
numero_factura_inicial INTEGER DEFAULT 1

# Après
numero_factura_inicial TEXT DEFAULT '1'

# Migration automatique
CREATE TABLE organizacion_temp (
    ...
    numero_factura_inicial TEXT DEFAULT '1',
    ...
)
```

### **Modèle (`database/models.py`)**
```python
# Avant
def __init__(self, ..., numero_factura_inicial=1, ...):

# Après
def __init__(self, ..., numero_factura_inicial="1", ...):

# Correction de l'ordre des colonnes après migration
numero_inicial = row[8] if len(row) > 8 and row[8] is not None else "1"
```

### **Interface (`ui/organizacion.py`)**
```python
# Validation améliorée
if not any(c.isalnum() for c in numero_inicial_str):
    errors.append("El número inicial debe contener al menos un número o letra")

# Sauvegarde sans conversion
numero_factura_inicial=self.numero_inicial_entry.get().strip() or "1"

# Chargement robuste
if isinstance(numero_inicial, int):
    numero_inicial = str(numero_inicial)
```

---

## 🧪 **Tests Intégrés**

### **Tests de Régression**
**Fichier :** `test/regression/test_organizacion_numero_inicial_alphanum.py`

#### **Formats Testés :**
- ✅ Nombres simples : `1`, `100`
- ✅ Formats avec tirets : `2025-FACT-001`
- ✅ Formats avec lettres : `FACT-2025`, `INV-001`
- ✅ Formats avec slashes : `2025/01/001`
- ✅ Formats mixtes : `F001`, `123ABC`
- ✅ Validation des erreurs : trop long, seulement symboles

### **Tests d'Intégration**
**Fichier :** `test/integration/test_organizacion_alphanum_integration.py`

#### **Scénarios Testés :**
1. **Sauvegarde** avec format alphanumérique
2. **Rechargement** des données depuis la base
3. **Interface** de rechargement
4. **Différents formats** supportés

#### **Résultats :**
```bash
pytest test/regression/test_organizacion_numero_inicial_alphanum.py -v
pytest test/integration/test_organizacion_alphanum_integration.py -v
# ✅ Tous les tests passent
```

---

## 📊 **Exemples d'Utilisation**

### **Formats Valides**
```
✅ 1                    (Simple)
✅ 2025                 (Année)
✅ 2025-FACT-001        (Format complet)
✅ INV-2025-001         (Avec préfixe)
✅ FACTURA_123          (Avec underscore)
✅ 2025/01/001          (Avec slashes)
✅ F001                 (Court)
✅ 123ABC               (Mixte)
✅ SÉRIE-A-001          (Avec accents)
```

### **Formats Invalides**
```
❌ ---                  (Seulement symboles)
❌ "   "                (Seulement espaces)
❌ [50+ caractères]     (Trop long)
```

---

## 🎉 **Avantages**

### **Pour l'Utilisateur**
- ✅ **Flexibilité totale** : Formats personnalisés
- ✅ **Plus d'erreurs** : Validation intelligente
- ✅ **Compatibilité** : Anciens formats préservés
- ✅ **Intuitivité** : Formats naturels comme "2025-FACT-001"

### **Pour le Système**
- ✅ **Migration automatique** : Pas d'intervention manuelle
- ✅ **Rétrocompatibilité** : Anciens numéros fonctionnent
- ✅ **Validation robuste** : Gestion d'erreurs complète
- ✅ **Tests complets** : Couverture de régression et d'intégration

### **Pour la Maintenance**
- ✅ **Code plus flexible** : Gestion de différents formats
- ✅ **Documentation complète** : Formats supportés documentés
- ✅ **Tests automatisés** : Détection de régressions
- ✅ **Migration sûre** : Préservation des données existantes

---

## 🔄 **Migration Automatique**

La migration s'effectue automatiquement au démarrage de l'application :

1. **Détection** : Vérification du type de colonne
2. **Sauvegarde** : Création d'une table temporaire
3. **Conversion** : `CAST(numero_factura_inicial AS TEXT)`
4. **Remplacement** : Suppression ancienne table, renommage
5. **Validation** : Vérification de l'intégrité des données

**État :** ✅ **IMPLÉMENTÉ ET TESTÉ**

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
