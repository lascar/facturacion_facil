# Guide Utilisateur - Export PDF Corrigé

## 🎯 Nouvelles fonctionnalités

L'export PDF des factures a été amélioré pour une meilleure expérience utilisateur.

## ✨ Améliorations apportées

### 1. **Ouverture automatique sans confirmation**
- ✅ **AVANT** : Une fenêtre "PDF generado con éxito" apparaissait
- ✅ **MAINTENANT** : Le PDF s'ouvre directement sans message

### 2. **Logo d'entreprise affiché**
- ✅ **AVANT** : Seul le texte "LOGO" apparaissait
- ✅ **MAINTENANT** : Le logo de votre entreprise s'affiche correctement

### 3. **Noms des produits corrects**
- ✅ **AVANT** : "N/A" apparaissait à la place du nom
- ✅ **MAINTENANT** : Les vrais noms des produits sont affichés

### 4. **Références des produits visibles**
- ✅ **AVANT** : Les références n'apparaissaient pas
- ✅ **MAINTENANT** : Les références sont clairement visibles

## 📋 Comment utiliser l'export PDF

### Étapes simples :

1. **Ouvrir l'application**
   ```bash
   python3 main.py
   ```

2. **Aller dans Facturas**
   - Cliquez sur le bouton "Facturas" dans le menu principal

3. **Sélectionner une facture**
   - Cliquez sur une ligne dans la liste des factures

4. **Exporter en PDF**
   - Cliquez sur le bouton "📄 Exportar PDF"

5. **Résultat**
   - Le PDF s'ouvre automatiquement dans votre lecteur PDF par défaut
   - Aucune fenêtre de confirmation n'apparaît

## 📁 Où sont sauvegardés les PDF ?

🎯 **Répertoire configurable :** Les fichiers PDF sont sauvegardés dans le répertoire que vous avez configuré dans la fenêtre "Organización".

### Configuration du répertoire :
1. Allez dans **"Organización"**
2. Trouvez **"Directorio por defecto para descargas de PDF"**
3. Cliquez sur **"📁 Seleccionar"** pour choisir votre répertoire
4. Cliquez sur **"💾 Guardar Configuración"**

### Répertoire par défaut :
Si aucun répertoire n'est configuré ou si le répertoire configuré n'existe plus :
```
facturacion_facil/pdfs/
```

ℹ️ **Note :** Le répertoire est créé automatiquement s'il n'existe pas.

### Format du nom de fichier :
```
Factura_[NUMERO]_[DATE_HEURE].pdf
```

**Exemples :**
- `Factura_2024-001_20241207_143022.pdf`
- `Factura_F-2024-123_20241207_143045.pdf`

## 🔍 Contenu du PDF généré

Votre PDF contiendra maintenant :

### En-tête
- ✅ **Logo de votre entreprise** (si configuré)
- ✅ Informations de l'entreprise
- ✅ Numéro et date de facture

### Informations client
- ✅ Nom du client
- ✅ NIF/CIF
- ✅ Adresse complète

### Détail des produits
- ✅ **Référence du produit** (visible)
- ✅ **Nom du produit** (correct)
- ✅ Quantité
- ✅ Prix unitaire
- ✅ Remise (%)
- ✅ TVA (%)
- ✅ Total par ligne

### Totaux
- ✅ Sous-total
- ✅ Total TVA
- ✅ **Total général**

## 🖼️ Configuration du logo

Pour que votre logo apparaisse dans les PDF :

### Emplacements supportés :
- `assets/logo.png`
- `assets/icon.png`
- `data/logos/logo.png`
- `data/logos/logo.jpg`
- `logo/logo.png`
- `logo/logo.jpg`

### Formats supportés :
- PNG (recommandé)
- JPG/JPEG
- GIF
- BMP

### Taille recommandée :
- Largeur : 200-400 pixels
- Hauteur : 100-200 pixels
- Ratio : 2:1 ou 3:2

## ⚠️ Résolution de problèmes

### Si "Producto eliminado" apparaît :
- Le produit a été supprimé de la base de données
- La facture fait encore référence à ce produit
- **Solution** : Restaurer le produit ou créer une nouvelle facture

### Si "N/A" apparaît pour la référence :
- Le produit n'a pas de référence définie
- **Solution** : Ajouter une référence au produit dans la gestion des produits

### Si le logo n'apparaît pas :
- Vérifiez qu'un fichier logo existe dans un des emplacements supportés
- Vérifiez que le fichier n'est pas corrompu
- **Solution** : Placez un logo valide dans `assets/logo.png`

## 🎉 Avantages de la nouvelle version

### Pour l'utilisateur :
- ✅ **Plus rapide** : Pas de clic supplémentaire
- ✅ **Plus fluide** : Ouverture directe du PDF
- ✅ **Plus professionnel** : Logo et données complètes

### Pour l'entreprise :
- ✅ **Image de marque** : Logo visible sur tous les PDF
- ✅ **Informations complètes** : Tous les détails produits visibles
- ✅ **Traçabilité** : Références produits clairement identifiées

## 📞 Support

Si vous rencontrez des problèmes :

1. **Vérifiez les logs** dans le dossier `logs/`
2. **Testez avec une nouvelle facture** contenant des produits existants
3. **Vérifiez la configuration du logo**

Les fichiers de test sont disponibles :
- `test_corrections_pdf.py` - Test des corrections
- `demo_corrections_pdf.py` - Démonstration complète

---

**Version :** Décembre 2024  
**Statut :** ✅ Corrections appliquées et testées
