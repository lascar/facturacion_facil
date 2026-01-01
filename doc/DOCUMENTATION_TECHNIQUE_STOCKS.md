# 📚 DOCUMENTATION TECHNIQUE - GESTION DES STOCKS

## 🎯 **ARCHITECTURE COMPLÈTE**

### **🔧 Composants Principaux**

#### **1. Base de Données (`database/database.py`)**
```python
# Méthodes clés pour les stocks
def adjust_product_stock(product_id, adjustment)     # Ajustement +/-
def update_product_stock(product_id, new_stock)      # Mise à jour directe
def add_invoice(invoice_data)                        # Création facture + stocks
def update_invoice(invoice_data)                     # Modification facture + stocks
def _process_invoice_stock_movement_with_connection() # Gestion stocks factures
```

#### **2. Interface Stock (`ui/stock_pyqt6.py`)**
```python
# Méthodes d'interface
def load_stock_data()           # Charge depuis la base
def refresh_stock_data()        # Rafraîchit avec notification (CORRIGÉ)
def update_stock()              # Édition manuelle d'un stock
def adjust_stock(id, adj)       # Boutons +/- 
def create_stock_buttons()      # Création boutons +/-
```

#### **3. Interface Factures (`ui/factura_editor_pyqt6.py`)**
```python
# Méthodes de sauvegarde
def save_invoice()              # Sauvegarde facture
def prepare_invoice_data()      # Prépare données avec lignes
def show_invoice_saved_summary() # Confirmation sauvegarde
```

---

## 🔄 **FLUX DE DONNÉES COMPLET**

### **📄 Création de Facture**
```
1. Interface Facture → prepare_invoice_data()
   ├─ Collecte client, produits, quantités
   └─ Structure: {cliente: {...}, lineas: [{producto_id, cantidad, ...}]}

2. save_invoice() → db.add_invoice(invoice_data)
   ├─ Sauvegarde facture en base
   └─ Appel automatique: _process_invoice_stock_movement_with_connection()

3. Traitement Stocks Automatique
   ├─ Pour chaque ligne: stock_actual -= cantidad
   ├─ Protection stock négatif (minimum 0)
   └─ Logs détaillés: "Stock actualizado - produit: X → Y (-Z)"

4. Confirmation
   ├─ Facture créée avec ID
   ├─ Stocks mis à jour en base
   └─ Interface: notification de succès
```

### **✏️ Modification de Facture**
```
1. Interface Facture → prepare_invoice_data() (données modifiées)

2. save_invoice() → db.update_invoice(invoice_data)
   ├─ REVERSION: Annule l'impact de l'ancienne facture
   │  └─ Pour chaque ancienne ligne: stock_actual += ancienne_cantidad
   ├─ NOUVEAU CALCUL: Applique l'impact de la nouvelle facture
   │  └─ Pour chaque nouvelle ligne: stock_actual -= nouvelle_cantidad
   └─ RÉSULTAT NET: Différence entre anciennes et nouvelles quantités

3. Logs Détaillés
   ├─ "Stock revertido para X productos"
   ├─ "Stock actualizado - produit: A → B (+reversion)"
   ├─ "Nuevo stock procesado para X productos"  
   └─ "Stock actualizado - produit: B → C (-nouveau)"
```

### **🔄 Rafraîchissement Interface**
```
1. Bouton "🔄 Actualizar" → refresh_stock_data()
   ├─ Appel: load_stock_data()
   ├─ Recharge TOUS les produits depuis la base
   ├─ Met à jour la table d'affichage
   └─ Notification: "Stocks actualizados correctamente"

2. Boutons +/- → adjust_stock(product_id, ±1)
   ├─ Appel: db.adjust_product_stock()
   ├─ Mise à jour immédiate en base
   ├─ Mise à jour ligne spécifique dans la table
   └─ Message temporaire: "📈/📉 Stock aumentado/reducido"
```

---

## 🎯 **CORRECTION MAJEURE APPORTÉE**

### **❌ AVANT (Incorrect)**
```python
buttons_config = [
    ("Actualizar Stock", self.update_stock, "primary"),  # ← Ouvrait dialog
    # ...
]

def update_stock(self):
    # Ouvrait QInputDialog pour modifier UN stock
    # Comportement confus pour un bouton "Actualizar"
```

### **✅ APRÈS (Correct)**
```python
buttons_config = [
    ("🔄 Actualizar", self.refresh_stock_data, "primary"),     # ← Rafraîchit TOUS
    ("📝 Editar Stock", self.update_stock, "secondary"),       # ← Modifie UN
    # ...
]

def refresh_stock_data(self):
    # Recharge TOUS les stocks depuis la base de données
    # Affiche notification de confirmation
    # Comportement logique pour "Actualizar"
```

---

## 🧪 **TESTS DISPONIBLES**

### **📋 Tests Unitaires**
```bash
# Test relation complète
python test_relation_stocks_factures_complet.py

# Test bouton Actualizar corrigé  
python test_bouton_actualizar.py

# Test boutons +/-
python test_symboles_boutons.py

# Démonstration fonctionnelle
python demo_relation_stocks_factures.py
```

### **📊 Tests Manuels**
```bash
# Test workflow complet
1. python main.py → Stock (noter stocks)
2. Facturas → Nueva → Ajouter produits → Guardar
3. Stock → "🔄 Actualizar" → Voir changements
4. Logs: tail -f logs/facturacion_facil.log
```

---

## 🔍 **DÉBOGAGE ET LOGS**

### **📋 Logs Clés à Surveiller**
```bash
# Création facture
"Stock actualizado - produit: X → Y (-Z)"
"Factura añadida con ID: N"
"Movimientos de stock procesados: N productos"

# Modification facture  
"Stock revertido para N productos"
"Nuevo stock procesado para N productos"
"Factura N actualizada con N líneas"

# Rafraîchissement interface
"Stocks rafraîchis: N produits chargés depuis la base de données"
"Status: 🔄 N produits actualisés depuis la base de données"
```

### **🔧 Points de Vérification**
```python
# 1. Vérifier stock en base directement
sqlite3 facturacion.db "SELECT id, nombre, stock_actual FROM productos;"

# 2. Vérifier factures récentes
sqlite3 facturacion.db "SELECT id, numero_factura, fecha_factura FROM facturas ORDER BY id DESC LIMIT 5;"

# 3. Vérifier lignes de facture
sqlite3 facturacion.db "SELECT factura_id, producto_id, cantidad FROM factura_items WHERE factura_id = X;"
```

---

## ✅ **GARANTIES SYSTÈME**

### **🛡️ Protections Intégrées**
- **Stock minimum 0** : Pas de stock négatif possible
- **Transactions atomiques** : Cohérence base de données garantie
- **Logs détaillés** : Traçabilité complète des mouvements
- **Validation données** : Vérification avant traitement

### **🎯 Cohérence Garantie**
- **Création facture** → Stock diminue automatiquement
- **Modification facture** → Ajustement précis des stocks
- **Suppression facture** → Reversion des stocks (si implémentée)
- **Interface** → Rafraîchissement sur demande

---

## 🚀 **UTILISATION OPTIMALE**

### **👤 Pour l'Utilisateur Final**
```bash
# Workflow recommandé
1. Créer/modifier factures normalement
2. Aller dans Stock → "🔄 Actualizar"  
3. ✅ Voir tous les changements immédiatement
4. Utiliser "📝 Editar Stock" pour corrections manuelles
5. Utiliser +/- pour ajustements rapides
```

### **🔧 Pour le Développeur**
```python
# Points d'extension
- Ajouter auto-refresh périodique
- Implémenter suppression factures avec reversion stocks
- Ajouter alertes stock bas
- Créer rapports de mouvements
- Intégrer avec système de commandes
```

**🎉 SYSTÈME COMPLET ET OPÉRATIONNEL À 100% !**
