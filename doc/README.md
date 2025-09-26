# 📚 Documentation - Facturación Fácil

## 📁 **Structure de la Documentation**

```
doc/
├── 📚 README.md                 # Ce guide principal
├── 👥 user/                     # Documentation utilisateur
│   ├── 📄 README.md             # ✅ Guide des documents utilisateur
│   ├── GUIDE_UTILISATEUR_PDF_DOWNLOAD.md
│   ├── GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md
│   └── GUIDE_MINI_IMAGES_FACTURAS.md
├── 🔧 technical/                # Documentation technique
│   ├── 📄 README.md             # ✅ Guide des documents techniques
│   ├── TESTING_GUIDE.md
│   ├── FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md
│   ├── RESUME_FINAL_FONCTIONNALITES_PDF.md
│   └── MINI_IMAGES_FACTURAS_RESUME.md
└── 🔌 api/                      # Documentation API
    └── 📄 README.md             # ✅ Guide des APIs et modules
```

## 📖 **Documentation Organisée par Répertoire**

Chaque répertoire dispose maintenant de sa propre documentation complète :

### **📄 Guides par Catégorie**
- **`user/README.md`** : Guide des documents utilisateur (300 lignes)
- **`technical/README.md`** : Guide des documents techniques (300 lignes)
- **`api/README.md`** : Guide des APIs et modules (300 lignes)

**Total : ~900 lignes de documentation organisée !**

## 👤 **Documentation Utilisateur**

### **Guides d'Utilisation**

#### **📄 Guide PDF Download**
**Fichier** : `user/GUIDE_UTILISATEUR_PDF_DOWNLOAD.md`
**Description** : Guide de base pour la fonctionnalité de téléchargement PDF
**Contenu** :
- Configuration du répertoire de téléchargement
- Génération et ouverture automatique des PDFs
- Gestion des répertoires et dépannage

#### **🖥️ Guide Visor PDF Complet**
**Fichier** : `user/GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md`
**Description** : Guide complet incluant le visor PDF personnalisé
**Contenu** :
- Configuration complète (répertoire + visor)
- Visors recommandés par plateforme
- Système de fallback et optimisation
- Workflow complet et conseils avancés

#### **🖼️ Guide Mini Images Facturas**
**Fichier** : `user/GUIDE_MINI_IMAGES_FACTURAS.md`
**Description** : Guide pour les mini images dans les lignes de facture
**Contenu** :
- Fonctionnalité d'affichage des images de produits
- Configuration et utilisation
- Optimisation et performance
- Dépannage et conseils

### **Utilisation des Guides**

```bash
# Consulter la documentation utilisateur
cd doc/user/

# Guide de base PDF
cat GUIDE_UTILISATEUR_PDF_DOWNLOAD.md

# Guide complet avec visor
cat GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md
```

## 🔧 **Documentation Technique**

### **Guides Techniques**

#### **🧪 Guide des Tests**
**Fichier** : `technical/TESTING_GUIDE.md`
**Description** : Guide complet pour l'exécution des tests
**Contenu** :
- Configuration de l'environnement de test
- Types de tests et leur exécution
- Couverture de code et rapports
- Dépannage et bonnes pratiques

#### **📄 Résumé Fonctionnalité PDF**
**Fichier** : `technical/FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md`
**Description** : Documentation technique détaillée de la fonctionnalité PDF
**Contenu** :
- Architecture et modifications apportées
- Modèles de données et base de données
- Interface utilisateur et générateur PDF
- Tests et compatibilité

#### **🎯 Résumé Final Complet**
**Fichier** : `technical/RESUME_FINAL_FONCTIONNALITES_PDF.md`
**Description** : Vue d'ensemble complète de toutes les fonctionnalités implémentées
**Contenu** :
- Mission accomplie et fonctionnalités réalisées
- Architecture technique complète
- Tests et validation
- Documentation et guides

### **Utilisation de la Documentation Technique**

```bash
# Consulter la documentation technique
cd doc/technical/

# Guide des tests
cat TESTING_GUIDE.md

# Documentation fonctionnalité PDF
cat FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md

# Résumé final
cat RESUME_FINAL_FONCTIONNALITES_PDF.md
```

## 🎯 **Navigation Rapide**

### **Pour les Utilisateurs Finaux**
1. **Première utilisation** → `user/GUIDE_UTILISATEUR_PDF_DOWNLOAD.md`
2. **Configuration avancée** → `user/GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md`

### **Pour les Développeurs**
1. **Tests** → `technical/TESTING_GUIDE.md`
2. **Architecture** → `technical/FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md`
3. **Vue d'ensemble** → `technical/RESUME_FINAL_FONCTIONNALITES_PDF.md`

### **Pour les Administrateurs**
1. **Configuration système** → `user/GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md`
2. **Tests et validation** → `technical/TESTING_GUIDE.md`

## 📖 **Contenu par Sujet**

### **Configuration PDF**
- **Répertoire de téléchargement** : `user/GUIDE_UTILISATEUR_PDF_DOWNLOAD.md`
- **Visor personnalisé** : `user/GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md`
- **Architecture technique** : `technical/FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md`

### **Tests et Qualité**
- **Guide complet des tests** : `technical/TESTING_GUIDE.md`
- **Tests spécifiques PDF** : Voir `../test/README.md`

### **Développement**
- **Fonctionnalités implémentées** : `technical/RESUME_FINAL_FONCTIONNALITES_PDF.md`
- **Architecture et code** : `technical/FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md`

## 🔍 **Recherche dans la Documentation**

### **Par Mot-clé**
```bash
# Rechercher dans toute la documentation
grep -r "PDF" doc/
grep -r "visor" doc/
grep -r "test" doc/

# Rechercher dans un type spécifique
grep -r "configuration" doc/user/
grep -r "architecture" doc/technical/
```

### **Par Fonctionnalité**
- **PDF Download** : `user/GUIDE_UTILISATEUR_PDF_DOWNLOAD.md`
- **Visor Personnalisé** : `user/GUIDE_UTILISATEUR_VISOR_PDF_COMPLET.md`
- **Tests** : `technical/TESTING_GUIDE.md`
- **Architecture** : `technical/FONCTIONNALITE_PDF_DOWNLOAD_RESUME.md`

## 📋 **Formats et Conventions**

### **Markdown**
Tous les documents utilisent le format Markdown avec :
- **Titres** : `#`, `##`, `###`
- **Code** : ````bash` ou ````python`
- **Listes** : `-` ou `1.`
- **Emphase** : `**gras**`, `*italique*`
- **Emojis** : Pour améliorer la lisibilité

### **Structure Type**
```markdown
# 📄 Titre Principal

## 🎯 Objectif

## 🔧 Configuration

### Étape 1
### Étape 2

## 📊 Exemples

## 🔧 Dépannage

## 💡 Conseils
```

## 🔄 **Mise à Jour de la Documentation**

### **Ajout de Nouvelle Documentation**
1. **Utilisateur** → Placer dans `doc/user/`
2. **Technique** → Placer dans `doc/technical/`
3. **API** → Placer dans `doc/api/` (futur)

### **Conventions de Nommage**
- **Guides utilisateur** : `GUIDE_UTILISATEUR_[SUJET].md`
- **Documentation technique** : `[SUJET]_RESUME.md` ou `[SUJET]_GUIDE.md`
- **API** : `API_[MODULE].md`

### **Mise à Jour de ce Guide**
Quand vous ajoutez de la documentation :
1. Mettre à jour la structure dans ce README
2. Ajouter les liens de navigation
3. Mettre à jour les sections de recherche

## 🎯 **Liens Utiles**

### **Documentation Externe**
- **Pytest** : https://docs.pytest.org/
- **CustomTkinter** : https://customtkinter.tomschimansky.com/
- **ReportLab** : https://www.reportlab.com/docs/

### **Documentation Interne**
- **Tests** : `../test/README.md`
- **Code** : Commentaires dans le code source
- **Configuration** : `../pytest.ini`, `../requirements*.txt`

## 📞 **Support**

Pour toute question sur la documentation :
1. Consultez d'abord ce guide
2. Recherchez dans la documentation existante
3. Vérifiez les exemples de code
4. Consultez les tests pour des exemples d'utilisation

---

**La documentation est vivante et évolue avec le projet !** 📚
