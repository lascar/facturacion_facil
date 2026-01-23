> **[⬆️ Volver al índice](../INDEX.md)** | **[📦 Features](README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📄 Contrôles de Visibilité PDF - Conditions de Paiement et Informations Légales

> **Date** : 2026-01-23  
> **Statut** : ✅ Implémenté et testé  
> **Version** : 1.0

---

## 📋 Vue d'ensemble

Cette fonctionnalité permet de contrôler la visibilité des sections "Condiciones de Pago" et "Información Legal" dans les PDFs de factures générés par l'application.

### Objectif

Donner à l'utilisateur la possibilité de masquer certaines sections du footer des PDFs sans avoir à supprimer le contenu de ces champs.

---

## ✨ Fonctionnalités

### Interface Utilisateur

**Localisation** : Fenêtre "Configuración de la Organización"

Deux nouvelles cases à cocher ont été ajoutées :
- ✅ **"Visible en los PDF"** sous le champ "Condiciones de Pago"
- ✅ **"Visible en los PDF"** sous le champ "Información Legal"

**Comportement par défaut** : Les deux cases sont cochées (sections visibles)

### Configuration

**Fichier** : `config/config.json`

Deux nouveaux champs dans `organizacion_defaults` :
```json
{
  "organizacion_defaults": {
    "condiciones_pago": "...",
    "informacion_legal": "...",
    "condiciones_pago_visible": 1,
    "informacion_legal_visible": 1
  }
}
```

**Valeurs** :
- `1` = Section visible dans les PDFs
- `0` = Section masquée dans les PDFs

### Génération PDF

Le générateur PDF vérifie les flags de visibilité avant d'inclure les sections dans le footer.

**Logique** :
- Si `condiciones_pago_visible == 0` → Section "CONDICIONES DE PAGO" non affichée
- Si `informacion_legal_visible == 0` → Section "INFORMACIÓN LEGAL" non affichée

---

## 🔧 Implémentation Technique

### Fichiers Modifiés

#### 1. **Interface** (`ui/organizacion_pyqt5.py`)

**Ajouts** :
- Lignes 166-168 : QCheckBox pour condiciones_pago_visible
- Lignes 182-184 : QCheckBox pour informacion_legal_visible
- Lignes 403-404 : Valeurs par défaut dans get_default_config()
- Lignes 553-556 : Chargement des états dans load_organization_data()
- Lignes 869-870 : Sauvegarde des états dans save_organizacion()

#### 2. **Générateur PDF** (`utils/pdf_generator.py`)

**Modifications** :
- Lignes 337-344 : Ajout des flags dans get_default_config()
- Lignes 385-438 : Logique conditionnelle dans create_footer()

**Logique de construction du footer** :
```python
footer_parts = []

# Ajouter les conditions de paiement si visibles
if condiciones_pago_visible:
    if condiciones_pago.strip():
        footer_parts.append(f"<b>CONDICIONES DE PAGO:</b><br/>{condiciones_pago_html}")

# Ajouter les informations légales si visibles
if informacion_legal_visible:
    if informacion_legal.strip():
        footer_parts.append(f"<b>INFORMACIÓN LEGAL:</b><br/>{informacion_legal_html}")

# Joindre les parties avec double saut de ligne
footer_text = "<br/><br/>".join(footer_parts)
```

---

## 🧪 Tests

### Fichier de Tests

**Localisation** : `test/behaviour/test_organizacion_visibility_checkboxes_behaviour.py`

### Tests Implémentés

**4 tests de comportement** :

1. **test_01_checkboxes_exist_in_organizacion_window**
   - Vérifie que les cases à cocher existent dans l'interface

2. **test_02_checkboxes_default_checked**
   - Vérifie que les cases sont cochées par défaut

3. **test_03_checkboxes_save_to_config_json**
   - Vérifie que les états sont sauvegardés dans config.json

4. **test_04_checkboxes_load_from_config_json**
   - Vérifie que les états sont chargés depuis config.json

### Protection des Fichiers de Production

**Conformité** : ✅ Respecte `docs/dev/testing/PROTECTION_FICHIERS_PRODUCTION.md`

**Méthode** :
- Utilisation de `tmp_path` (fixture pytest) pour créer un fichier config temporaire
- Patch de `organizacion_window.config_file` après ouverture de la fenêtre
- Rechargement des données avec `organizacion_window.load_organizacion()`
- Aucun accès direct à `config/config.json` en production

**Vérification** :
```bash
python3 test/scripts/verify_no_production_db_usage.py
# ✅ Aucun problème détecté dans test_organizacion_visibility_checkboxes_behaviour.py
```

### Exécution des Tests

```bash
# Tous les tests
pytest test/behaviour/test_organizacion_visibility_checkboxes_behaviour.py -v

# Test spécifique
pytest test/behaviour/test_organizacion_visibility_checkboxes_behaviour.py::TestOrganizacionVisibilityCheckboxesBehaviour::test_01_checkboxes_exist_in_organizacion_window -v
```

**Résultat** : ✅ 4/4 tests passent

---

## 📝 Utilisation

### Pour l'Utilisateur Final

1. Ouvrir **"Configuración de la Organización"**
2. Remplir les champs "Condiciones de Pago" et/ou "Información Legal"
3. Cocher/décocher les cases **"✓ Visible en los PDF"** selon les besoins
4. Cliquer sur **"💾 Guardar Configuración"**
5. Les PDFs générés respecteront les choix de visibilité

### Cas d'Usage

**Exemple 1** : Masquer temporairement les conditions de paiement
- Décocher "Visible en los PDF" sous "Condiciones de Pago"
- Le contenu est conservé mais n'apparaît pas dans les PDFs

**Exemple 2** : Afficher uniquement les informations légales
- Décocher "Visible en los PDF" sous "Condiciones de Pago"
- Laisser cochée "Visible en los PDF" sous "Información Legal"

---

## 🔗 Voir Aussi

- **[PDF_FEATURES_SUMMARY.md](PDF_FEATURES_SUMMARY.md)** - Vue d'ensemble des fonctionnalités PDF
- **[PROTECTION_FICHIERS_PRODUCTION.md](../testing/PROTECTION_FICHIERS_PRODUCTION.md)** - Protection des fichiers de production dans les tests
- **[GUIDE_TESTS_BEHAVIOUR_AUTO_CLOSE.md](../testing/GUIDE_TESTS_BEHAVIOUR_AUTO_CLOSE.md)** - Guide des tests comportementaux

---

**Dernière mise à jour** : 2026-01-23  
**Auteur** : Équipe de développement

