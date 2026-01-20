> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# Guide d'utilisation du bouton PDF

## 🎯 Fonctionnalité

Le bouton PDF permet de convertir et sauvegarder les factures en format PDF dans le dossier `pdfs/`.

## 📍 Localisation

Le bouton **📄 Exportar PDF** se trouve dans l'interface de gestion des factures, positionné entre les boutons "Editar" et "Eliminar".

## 🚀 Utilisation

### Étapes pour exporter une facture en PDF :

1. **Lancer l'application**
   ```bash
   python3 main.py
   ```

2. **Accéder aux factures**
   - Cliquer sur le bouton "Facturas" dans le menu principal

3. **Sélectionner une facture**
   - Cliquer sur une ligne dans la table des factures pour la sélectionner

4. **Exporter en PDF**
   - Cliquer sur le bouton "📄 Exportar PDF"

5. **Confirmation**
   - Un message de confirmation s'affiche avec les détails du fichier généré

## 📁 Sauvegarde

### Dossier de destination
- **Dossier** : `pdfs/` (créé automatiquement si nécessaire)
- **Localisation** : Dans le répertoire racine de l'application

### Format du nom de fichier
```
Factura_[NUMERO]_[TIMESTAMP].pdf
```

**Exemples :**
- `Factura_F-2024-001_20241207_130500.pdf`
- `Factura_FACT_2024_123_20241207_130501.pdf`

### Caractéristiques du nom
- **Préfixe** : `Factura_`
- **Numéro** : Numéro de la facture (caractères `/` remplacés par `_`)
- **Timestamp** : Date et heure de génération (YYYYMMDD_HHMMSS)
- **Extension** : `.pdf`

## ⚠️ Gestion des erreurs

### Aucune facture sélectionnée
- **Message** : "Seleccione una factura para exportar a PDF"
- **Action** : Sélectionner une facture avant de cliquer sur le bouton

### Erreur de génération
- **Message** : Détails de l'erreur rencontrée
- **Vérifications** :
  - Permissions d'écriture dans le dossier
  - Espace disque disponible
  - Facture valide dans la base de données

## ✅ Fonctionnalités

### Automatiques
- ✅ Création du dossier `pdfs/` si nécessaire
- ✅ Génération automatique du nom de fichier unique
- ✅ Utilisation du générateur PDF existant
- ✅ Gestion des erreurs avec messages informatifs

### Contenu du PDF
- ✅ Informations complètes de la facture
- ✅ Données du client
- ✅ Liste détaillée des produits
- ✅ Calculs d'IVA
- ✅ Totaux
- ✅ Design professionnel

## 🔧 Technique

### Implémentation
- **Fichier** : `ui/facturas_pyqt5.py`
- **Méthode** : `exportar_pdf()`
- **Générateur** : `utils/pdf_generator.py`

### Code principal
```python
def exportar_pdf(self):
    """Exportar la factura seleccionada a PDF"""
    if not self.selected_factura_id:
        self.show_warning("Selección", "Seleccione una factura para exportar a PDF")
        return
    
    # Obtenir la facture
    factura = db.get_invoice_by_id(self.selected_factura_id)
    
    # Générer le PDF
    pdf_generator = PDFGenerator()
    success = pdf_generator.generar_factura_pdf(factura, pdf_path, auto_open=False)
```

## 📊 Tests

### Tests disponibles
- `test_bouton_pdf_simple.py` - Tests de base
- `test_bouton_pdf_final.py` - Tests complets
- `test_bouton_pdf_real.py` - Test avec interface

### Exécution des tests
```bash
python3 test_bouton_pdf_final.py
```

## 🎉 Résultat

Après avoir cliqué sur le bouton PDF :
1. Le fichier PDF est généré dans le dossier `pdfs/`
2. Un message de confirmation s'affiche
3. Le PDF contient toutes les informations de la facture
4. Le fichier est prêt pour impression ou envoi

## 📞 Support

En cas de problème :
1. Vérifier que la facture est bien sélectionnée
2. Vérifier les permissions du dossier `pdfs/`
3. Consulter les logs pour plus de détails
4. Exécuter les tests pour diagnostiquer

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
