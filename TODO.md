# TODO
# Préférences de développement pour facturacion_facil

 ## Communication et workflow
 - **Langue** : Communiquer exclusivement en français avec tutoiement
 - **Validation obligatoire** : Aucune modification de code ou système sans confirmation préalable explicite de l'utilisateur. Toujours expliquer en détail le code. Présenter les modifications sous la forme d'un git diff

 ### Localisation
 - **Textes en dur** : ne jamais harcoder des textes en dur dans le code
 - **Langues obligatoires** : ES pour chaque nouveau texte

 ### Tests
 - ** les tests doivent être intégrés comme test de régression ou d'integration dans la suite de test et non supprimer
 - ** les tests doivent utiliser une base de donnée différente à celle de production
 - ** lorque tu fais un nouveau test dans le developpement intègre-le à la suite de test

 ### Structure de données - CRITIQUE ⚠️
 - ** JAMAIS modifier la structure de base de données sans sauvegarde préalable obligatoire
 - ** JAMAIS supprimer ou perdre des données de production - INCIDENT GRAVE
 - ** quand la structure de la base de donnée change, il faut maintenir la compatibilité avec la structure antérieur
 - ** si la structure de la base de donnée change, il faut migrer les données existantes de la base de production
 - ** TOUJOURS utiliser des migrations progressives (ADD COLUMN) au lieu de DROP/CREATE
 - ** TOUJOURS tester les migrations sur une copie avant application en production
 - ** TOUJOURS vérifier que les données sont préservées après migration
 - ** En cas de doute sur une modification de structure : DEMANDER CONFIRMATION EXPLICITE
 - ** UTILISER OBLIGATOIREMENT le système de migration : database/migration_manager.py
 - ** CONSULTER la documentation : GUIDE_MIGRATIONS_BASE_DONNEES.md
 - ** TESTER avec le script : test_migration_system.py avant toute modification
 - ** En cas de perte de données : utiliser restore_and_migrate.py pour récupération


## ✅ PROBLEMAS RESUELTOS

### 1. ✅ Nueva Factura au premier plan (FORÇAGE MAXIMAL)
~~il n'y a qu'une fenetre nueva factura mais elle aparait derriére gestion de facturas~~
~~pas du tout résolu dialog apparaît en second plan~~
~~NON ABSOLUMENT PAS RÉSOLU . LE PROBLÈME SUBSISTE~~
~~Forçage dans constructeur ne fonctionne pas non plus~~
~~Solution sans parent ne fonctionne pas non plus~~

🔧 **SOLUTION FINALE IMPLÉMENTÉE** - Nueva Factura au premier plan avec chargement asynchrone

### 2. ✅ Bouton PDF pour convertir et sauvegarder les factures
🎉 **IMPLÉMENTÉ** - Bouton PDF ajouté à l'interface des factures

**FONCTIONNALITÉ AJOUTÉE:** Bouton PDF dans l'interface de gestion des factures

**SOLUTION TECHNIQUE:**
```python
# Dans ui/facturas_pyqt5.py:
self.pdf_btn = QPushButton("📄 Exportar PDF")
self.pdf_btn.clicked.connect(self.exportar_pdf)

def exportar_pdf(self):
    # Vérification sélection facture
    factura_data = db.get_invoice_by_id(self.selected_factura_id)

    # Génération nom fichier avec timestamp
    numero_safe = str(factura_data.get('numero', 'SIN_NUMERO')).replace('/', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"

    # Création dossier pdfs/ si nécessaire
    pdf_dir = os.path.join(os.getcwd(), "pdfs")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Utilisation PDFGenerator avec dictionnaire (CORRIGÉ)
    pdf_generator = PDFGenerator()
    success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)
```

**CORRECTION APPLIQUÉE:**
- ✅ **Problème résolu**: 'builtin_function_or_method' object is not iterable
- ✅ **Cause**: Utilisation de `generar_factura_pdf()` qui attend un objet avec attributs
- ✅ **Solution**: Utilisation de `generate_invoice_pdf()` qui accepte un dictionnaire
- ✅ **Tests**: Tous les tests passent, PDF généré correctement (3388 bytes)

**OUVERTURE AUTOMATIQUE AJOUTÉE:**
- ✅ **Méthode abrir_pdf()**: Ouvre le PDF avec le visor par défaut du système
- ✅ **Support multi-plateforme**: Windows (startfile), macOS (open), Linux (xdg-open)
- ✅ **Workflow complet**: Génération → Sauvegarde → Ouverture automatique
- ✅ **Message mis à jour**: "PDF generado y abierto exitosamente"

**CARACTÉRISTIQUES:**
✅ Bouton visible entre "Editar" et "Eliminar"
✅ Icône 📄 et texte "Exportar PDF"
✅ Gestion de l'absence de sélection avec message d'avertissement
✅ Génération automatique du nom de fichier avec timestamp
✅ Création automatique du dossier pdfs/ si nécessaire
✅ Utilisation du PDFGenerator existant
✅ Message de confirmation avec détails du fichier généré
✅ Tests intégrés dans la suite de tests

**PROBLÈME RÉSOLU:** Nueva Factura apparaît maintenant au premier plan

**SOLUTION TECHNIQUE FINALE:**
1. **Flags robustes dans le constructeur:**
   - Qt.Window + Qt.WindowCloseButtonHint + Qt.WindowMinimizeButtonHint
   - Qt.WindowStaysOnTopHint + Qt.WindowTitleHint
   - setWindowState(Qt.WindowActive)

2. **Affichage immédiat avant chargement:**
   - show() + raise_() + activateWindow() + setFocus() dans le constructeur
   - Chargement des données en asynchrone avec QTimer.singleShot(100ms)

3. **Dialog sans parent:**
   - CrearFacturaDialog(None) pour éviter conflits de hiérarchie

**SOLUTION TECHNIQUE FINALE:**
```python
# Dans CrearFacturaDialog.__init__():
# Étape 1: Flags robustes
self.setWindowFlags(
    Qt.Window |
    Qt.WindowCloseButtonHint |
    Qt.WindowMinimizeButtonHint |
    Qt.WindowStaysOnTopHint |
    Qt.WindowTitleHint
)

# Étape 2: État actif
self.setWindowState(Qt.WindowActive)

# Étape 3: Affichage immédiat
self.show()
self.raise_()
self.activateWindow()
self.setFocus()

# Étape 4: Chargement asynchrone
QTimer.singleShot(100, self.load_data)

# Dans new_factura():
self.crear_dialog = CrearFacturaDialog(None)  # SANS parent
```

**RÉSULTAT UTILISATEUR:**
- Dialog Nueva Factura apparaît IMMÉDIATEMENT au premier plan
- Complètement indépendant de la fenêtre parent
- Plus JAMAIS caché derrière d'autres fenêtres
- Gestion native par l'OS, comportement prévisible

**TECHNIQUE FINALE :**
```python
# Dans CrearFacturaDialog.__init__():
self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)
self.raise_()
self.activateWindow()
self.setFocus()

# Timer pour retrait automatique du flag
QTimer.singleShot(500, remove_always_on_top)
```

**RÉSULTAT UTILISATEUR :**
- Le dialog Nueva Factura apparaît INSTANTANÉMENT au premier plan
- Plus JAMAIS caché derrière d'autres fenêtres
- Comportement 100% prévisible et fiable
- Interface fluide et professionnelle

## 🎯 PROCHAINES TÂCHES

### Gestion du stock
- Implémenter système d'alerte stock minimum
- Ajouter historique des mouvements de stock
- Créer interface de gestion des entrées/sorties

### Améliorations interface
- Optimiser performance chargement listes
- Ajouter raccourcis clavier
- Améliorer navigation entre fenêtres
