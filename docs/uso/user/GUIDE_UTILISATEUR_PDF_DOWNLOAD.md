> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📄 Guide Utilisateur - Téléchargement PDF Configurable

## 🎯 **Nouvelle Fonctionnalité**

Votre application de facturation dispose maintenant d'une fonctionnalité avancée pour la gestion des PDFs :
- **Répertoire configurable** pour sauvegarder vos factures PDF
- **Ouverture automatique** des PDFs générés
- **Conservation de vos préférences** de répertoire

## 🔧 **Configuration**

### **Étape 1 : Accéder à la Configuration**
1. Ouvrez l'application de facturation
2. Cliquez sur **"Organización"** dans le menu principal
3. La fenêtre de configuration de l'organisation s'ouvre

### **Étape 2 : Configurer le Répertoire PDF**
Dans la section **"⚙️ Configuración Adicional"**, vous trouverez :

```
Directorio por defecto para descargas de PDF: [________________] [📁 Seleccionar]
```

1. Cliquez sur le bouton **"📁 Seleccionar"**
2. Choisissez le répertoire où vous souhaitez sauvegarder vos PDFs
   - Exemple : `C:\Users\VotreNom\Documents\Facturas`
   - Exemple : `/home/utilisateur/Documents/Facturas`
3. Cliquez sur **"💾 Guardar Configuración"**

### **Étape 3 : Vérification**
- Le répertoire choisi apparaît dans le champ de texte
- Votre choix est automatiquement sauvegardé
- Il sera conservé pour toutes les futures générations de PDF

## 📄 **Utilisation**

### **Générer une Facture PDF**
1. **Depuis la liste des factures** :
   - Sélectionnez une facture dans la liste
   - Cliquez sur **"📄 Exportar PDF"**

2. **Depuis l'éditeur de facture** :
   - Ouvrez ou créez une facture
   - Cliquez sur **"📄 Generar PDF"**

### **Ce qui se passe automatiquement** :
1. ✅ Le PDF est généré avec toutes les informations de la facture
2. 📁 Il est sauvegardé dans votre répertoire configuré
3. 🚀 Le PDF s'ouvre automatiquement dans votre lecteur PDF par défaut
4. 👀 Vous pouvez immédiatement visualiser, imprimer ou partager le PDF

## 📁 **Gestion des Répertoires**

### **Répertoires Recommandés**
- **Windows** : `C:\Users\[VotreNom]\Documents\Facturas`
- **macOS** : `/Users/[VotreNom]/Documents/Facturas`
- **Linux** : `/home/[utilisateur]/Documents/Facturas`

### **Conseils d'Organisation**
- Créez un dossier dédié aux factures (ex: "Facturas_2024")
- Utilisez un répertoire facilement accessible
- Évitez les répertoires système ou temporaires

### **Système de Sécurité**
Si le répertoire configuré n'est plus accessible :
- 🔄 L'application utilise automatiquement un répertoire par défaut
- 📁 Les PDFs sont sauvegardés dans le dossier `pdfs/` de l'application
- ⚠️ Vous recevrez une notification pour reconfigurer le répertoire

## 🎨 **Interface Utilisateur**

### **Nouveaux Éléments**
Dans la configuration de l'organisation :

```
⚙️ Configuración Adicional
├── Directorio por defecto para imágenes de productos: [____] [📁]
├── Directorio por defecto para descargas de PDF:      [____] [📁] ← NOUVEAU
└── Número inicial para serie de facturas:             [____]
```

### **Messages d'Information**
L'application affiche des messages informatifs :
- ✅ **"PDF generado exitosamente"** : Confirmation de génération
- 📁 **Emplacement du fichier** : Chemin complet du PDF créé
- 🚀 **"PDF abierto automáticamente"** : Confirmation d'ouverture

## 🔧 **Dépannage**

### **Le PDF ne s'ouvre pas automatiquement**
**Causes possibles** :
- Aucun lecteur PDF installé sur votre système
- Permissions insuffisantes

**Solutions** :
- Installez un lecteur PDF (Adobe Reader, Foxit, etc.)
- Le PDF est quand même sauvegardé dans votre répertoire configuré

### **Erreur de répertoire**
**Message** : "Error al seleccionar directorio"

**Solutions** :
1. Vérifiez que le répertoire existe
2. Vérifiez vos permissions d'écriture
3. Choisissez un autre répertoire

### **PDF non trouvé**
**Si vous ne trouvez pas votre PDF** :
1. Vérifiez le répertoire configuré
2. Regardez dans le dossier `pdfs/` de l'application
3. Recherchez par nom de facture (ex: "Factura_2024-001.pdf")

## 💡 **Conseils d'Utilisation**

### **Bonnes Pratiques**
- 📅 **Organisation par date** : Créez des sous-dossiers par mois/année
- 🏷️ **Nommage cohérent** : Les PDFs sont nommés automatiquement
- 💾 **Sauvegarde** : Sauvegardez régulièrement votre répertoire de factures
- 🔄 **Synchronisation** : Utilisez un service cloud pour accéder partout

### **Workflow Recommandé**
1. **Configuration initiale** : Définissez votre répertoire une fois
2. **Génération** : Créez vos factures normalement
3. **Export PDF** : Un clic pour générer et ouvrir
4. **Partage** : Le PDF est prêt à être envoyé par email
5. **Archivage** : Tous vos PDFs sont organisés au même endroit

## 🎉 **Avantages**

### **Gain de Temps**
- ⚡ **Ouverture instantanée** : Plus besoin de chercher le fichier
- 📁 **Organisation automatique** : Tous les PDFs au même endroit
- 🔄 **Workflow fluide** : De la facture au PDF en un clic

### **Contrôle Total**
- 🎯 **Votre choix** : Vous décidez où sauvegarder
- 💾 **Persistance** : Vos préférences sont conservées
- 🔒 **Sécurité** : Système de fallback robuste

### **Compatibilité**
- 🖥️ **Multi-plateforme** : Windows, macOS, Linux
- 📱 **Lecteurs PDF** : Compatible avec tous les lecteurs
- 🔄 **Intégration** : S'intègre parfaitement à votre workflow existant

---

## 📞 **Support**

Si vous rencontrez des difficultés :
1. Consultez la section **Dépannage** ci-dessus
2. Vérifiez que votre répertoire est accessible
3. Redémarrez l'application si nécessaire

**Profitez de cette nouvelle fonctionnalité pour une gestion encore plus efficace de vos factures !** 🎯

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
