# 📄 Guide Utilisateur - Visor PDF Personnalisé

## 🎯 **Nouvelle Fonctionnalité Avancée**

Votre application de facturation dispose maintenant d'une fonctionnalité complète pour la gestion des PDFs :
- **Répertoire configurable** pour sauvegarder vos factures PDF
- **Visor PDF personnalisé** pour choisir votre logiciel préféré
- **Ouverture automatique** des PDFs générés
- **Conservation de toutes vos préférences**

## 🔧 **Configuration Complète**

### **Étape 1 : Accéder à la Configuration**
1. Ouvrez l'application de facturation
2. Cliquez sur **"Organización"** dans le menu principal
3. La fenêtre de configuration de l'organisation s'ouvre

### **Étape 2 : Configurer les Répertoires et Visor**
Dans la section **"⚙️ Configuración Adicional"**, vous trouverez :

```
Directorio por defecto para imágenes de productos: [________________] [📁 Seleccionar]
Directorio por defecto para descargas de PDF:      [________________] [📁 Seleccionar]
Visor PDF personalizado (opcional):                [________________] [📁 Seleccionar]
Número inicial para serie de facturas:             [____]
```

#### **Configuration du Répertoire PDF**
1. Cliquez sur **"📁 Seleccionar"** à côté de "Directorio por defecto para descargas de PDF"
2. Choisissez le dossier où vous voulez sauvegarder vos factures PDF
3. Exemple : `C:\Users\VotreNom\Documents\Facturas_PDF`

#### **Configuration du Visor PDF (Nouveau !)**
1. Cliquez sur **"📁 Seleccionar"** à côté de "Visor PDF personalizado"
2. Naviguez vers votre logiciel PDF préféré
3. Sélectionnez l'exécutable du programme

### **Étape 3 : Sauvegarder**
1. Cliquez sur **"💾 Guardar Configuración"**
2. Vos préférences sont sauvegardées automatiquement
3. Elles seront conservées pour toutes les futures utilisations

## 🖥️ **Visors PDF Recommandés par Système**

### **Windows 📱**
| Logiciel | Chemin Typique | Avantages |
|----------|----------------|-----------|
| **Adobe Acrobat Reader DC** | `C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe` | Standard industrie, annotations |
| **Foxit Reader** | `C:\Program Files\Foxit Software\Foxit Reader\FoxitReader.exe` | Rapide, léger |
| **Sumatra PDF** | `C:\Program Files\SumatraPDF\SumatraPDF.exe` | Ultra-léger, rapide |
| **PDF-XChange Viewer** | `C:\Program Files\Tracker Software\PDF Viewer\PDFXCview.exe` | Annotations avancées |

### **macOS 🍎**
| Logiciel | Chemin Typique | Avantages |
|----------|----------------|-----------|
| **Preview** | `/Applications/Preview.app` | Intégré, rapide |
| **Adobe Acrobat Reader DC** | `/Applications/Adobe Acrobat Reader DC.app` | Fonctionnalités complètes |
| **PDF Expert** | `/Applications/PDF Expert.app` | Interface moderne |
| **Skim** | `/Applications/Skim.app` | Recherche académique |

### **Linux 🐧**
| Logiciel | Chemin Typique | Avantages |
|----------|----------------|-----------|
| **Evince** | `/usr/bin/evince` | GNOME par défaut |
| **Okular** | `/usr/bin/okular` | KDE, annotations |
| **Zathura** | `/usr/bin/zathura` | Minimaliste, clavier |
| **MuPDF** | `/usr/bin/mupdf` | Très rapide |

## 📄 **Utilisation**

### **Générer une Facture PDF**
1. **Depuis la liste des factures** :
   - Sélectionnez une facture
   - Cliquez sur **"📄 Exportar PDF"**

2. **Depuis l'éditeur de facture** :
   - Créez ou modifiez une facture
   - Cliquez sur **"📄 Generar PDF"**

### **Ce qui se passe automatiquement** :
1. ✅ **Génération** : Le PDF est créé avec toutes les informations
2. 📁 **Sauvegarde** : Il est sauvegardé dans votre répertoire configuré
3. 🚀 **Ouverture** : Il s'ouvre avec votre visor PDF choisi
4. 👀 **Utilisation** : Vous pouvez immédiatement voir, imprimer, partager

## 🔄 **Système de Fallback Intelligent**

### **Si le visor personnalisé n'est pas disponible** :
- 🔄 L'application utilise automatiquement le visor système par défaut
- 📝 Un message informatif est enregistré dans les logs
- ✅ Le PDF s'ouvre quand même sans interruption

### **Si le répertoire configuré n'existe plus** :
- 📁 L'application utilise le dossier `pdfs/` par défaut
- 🔄 Le PDF est quand même généré et ouvert
- ⚠️ Vous pouvez reconfigurer le répertoire quand vous voulez

## 🎨 **Interface Utilisateur Améliorée**

### **Nouveaux Éléments dans Organisation** :
```
⚙️ Configuración Adicional
├── Directorio por defecto para imágenes de productos: [____] [📁]
├── Directorio por defecto para descargas de PDF:      [____] [📁]
├── Visor PDF personalizado (opcional):                [____] [📁] ← NOUVEAU
└── Número inicial para serie de facturas:             [____]
```

### **Informations Contextuelles** :
```
💡 Información:
• El directorio de imágenes se usará como ubicación por defecto al agregar imágenes a productos
• El directorio de PDF se usará para guardar y abrir automáticamente las facturas generadas
• El visor PDF personalizado permite elegir qué programa usar para abrir PDFs (Adobe Reader, Foxit, etc.)
• Si no se especifica visor personalizado, se usará el predeterminado del sistema
• El número inicial de facturas se aplicará cuando se configure una nueva serie de numeración
• Estos ajustes se pueden cambiar en cualquier momento
```

## 🔧 **Dépannage Avancé**

### **Le visor personnalisé ne fonctionne pas**
**Vérifications** :
1. ✅ Le chemin vers l'exécutable est correct
2. ✅ Le logiciel est installé et fonctionnel
3. ✅ Vous avez les permissions d'exécution

**Solutions** :
- Testez le logiciel manuellement
- Reconfigurez avec le bon chemin
- Laissez vide pour utiliser le système

### **PDF généré mais ne s'ouvre pas**
**Causes possibles** :
- Visor configuré inexistant
- Permissions insuffisantes
- Logiciel PDF corrompu

**Solutions** :
1. Reconfigurez le visor PDF
2. Testez avec le visor système (laissez vide)
3. Réinstallez votre logiciel PDF

### **Erreur de génération PDF**
**Si le PDF ne se génère pas** :
1. Vérifiez l'espace disque disponible
2. Vérifiez les permissions du répertoire
3. Consultez les logs de l'application

## 💡 **Conseils d'Optimisation**

### **Choix du Visor** :
- **Rapidité** : Sumatra PDF (Windows), Preview (macOS), Zathura (Linux)
- **Fonctionnalités** : Adobe Acrobat Reader DC (toutes plateformes)
- **Annotations** : PDF Expert (macOS), Okular (Linux)
- **Légèreté** : Evince (Linux), Foxit Reader (Windows)

### **Organisation des Fichiers** :
- 📅 Créez des sous-dossiers par période (2024-01, 2024-02...)
- 🏷️ Les noms de fichiers sont automatiques : `Factura_2024-001.pdf`
- 💾 Sauvegardez régulièrement votre dossier de factures
- ☁️ Utilisez un service cloud pour la synchronisation

### **Workflow Optimisé** :
1. **Configuration unique** : Définissez vos préférences une fois
2. **Génération rapide** : Un clic pour créer et ouvrir
3. **Partage immédiat** : Le PDF est prêt à être envoyé
4. **Archivage automatique** : Tout est organisé automatiquement

## 🎉 **Avantages de la Solution Complète**

### **Flexibilité Totale** :
- 🎯 **Votre choix** : Répertoire ET visor personnalisés
- 🔄 **Adaptabilité** : Changez quand vous voulez
- 💾 **Persistance** : Toutes vos préférences conservées

### **Fiabilité** :
- 🔒 **Système de fallback** : Toujours fonctionnel
- ✅ **Compatibilité** : Tous systèmes et logiciels
- 🛡️ **Robustesse** : Gestion d'erreurs complète

### **Productivité** :
- ⚡ **Rapidité** : Génération et ouverture instantanées
- 🎯 **Précision** : Exactement comme vous le voulez
- 🔄 **Efficacité** : Workflow optimisé

---

## 📞 **Support**

**Cette fonctionnalité avancée vous donne un contrôle total sur la gestion de vos PDFs de facturation !**

Profitez de cette flexibilité pour adapter l'application exactement à vos besoins et préférences ! 🎯
