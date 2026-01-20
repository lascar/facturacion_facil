> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔧 Guide de Debug - Problèmes Identifiés

## 🚨 Problèmes Rapportés

### 1. **Confusion de Stock entre Fenêtres**
- **Fenêtre gauche** (création) : Stock 0
- **Fenêtre droite** (édition) : Stock 5
- **Suspicion** : Les valeurs sont inversées

### 2. **Ouverture Automatique de Nouvelle Facture**
- Après édition et fermeture → Popup de succès ✅
- Après clic "OK" sur popup → **Nouvelle fenêtre de création s'ouvre** ❌

## 🔍 Analyse Technique

### **Problème 1 : Affichage du Stock**

#### **Logique Actuelle**
```python
# CrearFacturaDialog (fenêtre gauche)
stock = producto.get('stock_actual', 0)  # Stock direct de la base

# EditarFacturaDialog (fenêtre droite)  
stock_disponible = stock_actual + cantidad_original  # Stock + quantité libérée
```

#### **Explication**
- **Fenêtre création** : Affiche le stock réel en base de données
- **Fenêtre édition** : Affiche le stock disponible pour modification (incluant les quantités qui seront libérées)

#### **C'est Normal !**
Si vous avez :
- Stock en base : 5 unités
- Facture avec : 7 unités
- **Création** affiche : 5 (stock réel)
- **Édition** affiche : 12 (5 + 7 libérées)

### **Problème 2 : Ouverture Automatique**

#### **Flux Normal Attendu**
```
edit_factura() → EditarFacturaDialog → guardar_factura() → 
Message succès → self.accept() → Retour fenêtre principale
```

#### **Flux Problématique Observé**
```
... → Message succès → self.accept() → Retour fenêtre principale → 
❌ CrearFacturaDialog s'ouvre automatiquement
```

#### **Causes Possibles**
1. **Signal accidentel** émis après `self.accept()`
2. **Connexion incorrecte** de bouton
3. **Événement clavier** mal géré (ex: Entrée)
4. **Timer ou callback** qui déclenche `new_factura()`

## 🛠️ Debug Ajouté

### **Logs de Diagnostic**
```python
# Dans new_factura()
self.logger.debug("new_factura() appelée - Ouverture dialogue création")

# Dans edit_factura()
self.logger.debug(f"edit_factura() - Editando factura ID: {self.selected_factura_id}")
self.logger.debug(f"edit_factura() - Resultado del diálogo: {result}")

# Dans les combos de produits
self.logger.debug(f"CrearFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}")
self.logger.debug(f"EditarFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}")
```

## 📋 Instructions de Debug

### **Étape 1 : Reproduire le Problème**
1. Lancez l'application
2. Sélectionnez une facture
3. Cliquez "✏️ Editar"
4. Modifiez quelque chose
5. Cliquez "OK"
6. Cliquez "OK" sur le message de succès
7. **Observez** si une nouvelle fenêtre s'ouvre

### **Étape 2 : Analyser les Logs**
Recherchez dans les logs :
```
edit_factura() - Editando factura ID: X
edit_factura() - Resultado del diálogo: 1
edit_factura() - Recargando facturas...
edit_factura() - Facturas recargadas, terminado
new_factura() appelée - Ouverture dialogue création  ← PROBLÈME ICI
```

### **Étape 3 : Identifier la Cause**
Si `new_factura()` apparaît dans les logs après `edit_factura()`, cherchez :
- **Événements clavier** (Entrée, Espace)
- **Clics accidentels** sur le bouton "Nueva Factura"
- **Signaux Qt** mal connectés
- **Focus** sur le bouton "Nueva Factura"

## 🔧 Solutions Potentielles

### **Pour le Problème de Stock**
```python
# Si vous voulez que l'édition affiche le stock réel :
# Dans EditarFacturaDialog, remplacez :
stock_disponible = self.get_available_stock_for_product(producto_id)
# Par :
stock_actual = producto.get('stock_actual', 0)
```

### **Pour l'Ouverture Automatique**

#### **Solution A : Désactiver temporairement le bouton**
```python
def edit_factura(self):
    self.new_btn.setEnabled(False)  # Désactiver
    # ... code d'édition ...
    self.new_btn.setEnabled(True)   # Réactiver
```

#### **Solution B : Vérifier les événements clavier**
```python
def keyPressEvent(self, event):
    # Ignorer Entrée sur le bouton Nueva Factura
    if event.key() == Qt.Key_Return and self.new_btn.hasFocus():
        return
    super().keyPressEvent(event)
```

#### **Solution C : Déconnecter/reconnecter le signal**
```python
def edit_factura(self):
    self.new_btn.clicked.disconnect()  # Déconnecter
    # ... code d'édition ...
    self.new_btn.clicked.connect(self.new_factura)  # Reconnecter
```

## 🎯 Prochaines Étapes

### **Immédiat**
1. **Testez** avec les logs debug activés
2. **Identifiez** quand `new_factura()` est appelée
3. **Localisez** la source du signal/événement

### **Correction**
1. **Appliquez** la solution appropriée selon la cause
2. **Testez** que le problème est résolu
3. **Supprimez** les logs debug si souhaité

### **Validation**
1. **Éditez** plusieurs factures
2. **Vérifiez** qu'aucune fenêtre ne s'ouvre automatiquement
3. **Confirmez** que les stocks s'affichent correctement

---

## 💡 Notes Importantes

### **Stock Normal**
- **Création** : Stock réel en base
- **Édition** : Stock disponible (réel + libéré)
- **C'est logique** et correct !

### **Debug Efficace**
- Les logs ajoutés vous diront **exactement** quand le problème survient
- Suivez l'ordre chronologique des événements
- La cause sera évidente dans les logs

**Avec ces outils de debug, vous devriez pouvoir identifier et résoudre rapidement le problème ! 🚀**

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
