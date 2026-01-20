> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📊 **SCHÉMA COMPLET DE LA BASE DE DONNÉES**

## 🏢 **1. TABLE `organizacion`** (Configuration entreprise)
```sql
CREATE TABLE organizacion (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,                    -- Nom de l'entreprise
    direccion TEXT,                          -- Adresse complète
    telefono TEXT,                           -- Téléphone
    email TEXT,                              -- Email
    cif TEXT,                                -- CIF/NIF
    logo_path TEXT,                          -- Chemin du logo
    directorio_imagenes_defecto TEXT,        -- Répertoire images par défaut
    numero_factura_inicial TEXT DEFAULT '1', -- Numéro initial factures
    directorio_descargas_pdf TEXT,           -- Répertoire PDFs
    visor_pdf_personalizado TEXT,            -- Visionneuse PDF personnalisée
    logo_orientation TEXT DEFAULT 'landscape', -- Orientation logo
    directorio_logos_storage TEXT,           -- Stockage logos
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛍️ **2. TABLE `productos`** (Catalogue produits)
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,                    -- Nom du produit
    referencia TEXT UNIQUE,                  -- Référence unique
    precio REAL NOT NULL,                    -- Prix de vente
    categoria TEXT,                          -- Catégorie
    descripcion TEXT,                        -- Description
    imagen_path TEXT,                        -- Chemin image
    iva_recomendado REAL DEFAULT 21.0,       -- TVA recommandée
    stock_actual INTEGER DEFAULT 0,          -- Stock actuel
    stock_minimo INTEGER DEFAULT 5,          -- Stock minimum
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 👥 **3. TABLE `clientes`** (Clients)
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,                    -- Nom du client
    dni_nie TEXT,                            -- DNI/NIE
    direccion TEXT,                          -- Adresse
    email TEXT,                              -- Email
    telefono TEXT,                           -- Téléphone
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📄 **4. TABLE `facturas`** (Factures)
```sql
CREATE TABLE facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_factura TEXT UNIQUE NOT NULL,    -- Numéro facture
    fecha_factura DATE NOT NULL,             -- Date facture
    cliente_id INTEGER,                      -- ID client (FK)
    nombre_cliente TEXT NOT NULL,            -- Nom client (dénormalisé)
    dni_nie_cliente TEXT,                    -- DNI client (dénormalisé)
    direccion_cliente TEXT,                  -- Adresse client (dénormalisé)
    email_cliente TEXT,                      -- Email client (dénormalisé)
    telefono_cliente TEXT,                   -- Téléphone client (dénormalisé)
    subtotal REAL NOT NULL,                  -- Sous-total HT
    total_iva REAL NOT NULL,                 -- Total TVA
    total_factura REAL NOT NULL,             -- Total TTC
    modo_pago TEXT,                          -- Mode de paiement
    estado TEXT DEFAULT 'Borrador',          -- État facture
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);
```

## 📋 **5. TABLE `factura_items`** (Lignes de facture)
```sql
CREATE TABLE factura_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,            -- ID facture (FK)
    producto_id INTEGER NOT NULL,           -- ID produit (FK)
    cantidad INTEGER NOT NULL,              -- Quantité
    precio_unitario REAL NOT NULL,          -- Prix unitaire
    iva_aplicado REAL NOT NULL,             -- TVA appliquée
    descuento REAL DEFAULT 0,               -- Remise %
    subtotal REAL NOT NULL,                 -- Sous-total ligne
    descuento_amount REAL DEFAULT 0,        -- Montant remise
    iva_amount REAL NOT NULL,               -- Montant TVA
    total REAL NOT NULL,                    -- Total ligne
    FOREIGN KEY (factura_id) REFERENCES facturas (id),
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);
```

## 🏷️ **6. TABLE `factura_estados`** (États des factures)
```sql
CREATE TABLE factura_estados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,            -- Nom de l'état
    descripcion TEXT,                       -- Description
    permite_modificacion BOOLEAN DEFAULT 1, -- Permet modification
    color TEXT DEFAULT '#007bff',           -- Couleur d'affichage
    orden INTEGER DEFAULT 0,                -- Ordre d'affichage
    activo BOOLEAN DEFAULT 1,               -- État actif
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📦 **7. TABLE `stock`** (Stock des produits)
```sql
CREATE TABLE stock (
    producto_id INTEGER PRIMARY KEY,        -- ID produit (FK)
    cantidad_disponible INTEGER DEFAULT 0,  -- Quantité disponible
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);
```

## 📈 **8. TABLE `stock_movements`** (Mouvements de stock)
```sql
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,           -- ID produit (FK)
    cantidad INTEGER NOT NULL,              -- Quantité (+ entrée, - sortie)
    tipo TEXT NOT NULL,                     -- Type: MANUAL, VENTA, AJUSTE, INICIAL
    descripcion TEXT,                       -- Description du mouvement
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);
```

## 🔗 **RELATIONS ET CONTRAINTES**

### **Clés étrangères** :
- `facturas.cliente_id` → `clientes.id`
- `factura_items.factura_id` → `facturas.id`
- `factura_items.producto_id` → `productos.id`
- `stock.producto_id` → `productos.id`
- `stock_movements.producto_id` → `productos.id`

### **Index uniques** :
- `productos.referencia` (UNIQUE)
- `facturas.numero_factura` (UNIQUE)
- `factura_estados.nombre` (UNIQUE)

### **États par défaut des factures** :
1. **Borrador** - Facture en création (modifiable)
2. **Pendiente** - Envoyée, en attente de paiement
3. **Pagada** - Payée complètement
4. **Vencida** - Échue sans paiement
5. **Cancelada** - Annulée
6. **Anulada** - Annulée administrativement

## 📊 **STATISTIQUES**

- **8 tables principales**
- **Dénormalisation** : Données client copiées dans facturas pour historique
- **Gestion stock** : Table dédiée + historique des mouvements
- **États configurables** : Système flexible d'états de factures
- **Audit trail** : Timestamps sur toutes les tables principales

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
