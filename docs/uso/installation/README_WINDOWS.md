> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🪟 Facturación Fácil - Installation Windows 11

## 🚀 Installation rapide (3 étapes)

### **1. Cloner le projet**
```bash
git clone https://github.com/ton-username/facturacion_facil.git
cd facturacion_facil
```

### **2. Installation automatique**
```bash
# Double-clic sur le fichier :
install.bat
```

### **3. Lancement**
```bash
# Double-clic sur le fichier :
start.bat
```

## ✨ Nouvelles fonctionnalités

### **🖱️ Scroll avec la molette de souris**
- **Productos** - Scroll dans la liste et formulaires
- **Organización** - Scroll dans les longs formulaires de configuration
- **Facturas** - Scroll dans l'interface complexe de facturation

### **🎯 Test du scroll**
1. Lancer l'application avec `start.bat`
2. Ouvrir **Productos**, **Organización** ou **Facturas**
3. Utiliser la molette de souris pour scroller
4. Le scroll fonctionne partout dans la fenêtre !

## 📋 Prérequis

- **Windows 11** (ou Windows 10)
- **Python 3.8+** avec PATH configuré
- **Git** (optionnel, pour les mises à jour)

## 🔧 Si ça ne marche pas

### **Python pas trouvé**
1. Télécharger depuis [python.org](https://python.org/downloads/windows/)
2. ✅ Cocher "Add Python to PATH" pendant l'installation
3. Redémarrer l'ordinateur
4. Relancer `install.bat`

### **Erreur PowerShell**
```powershell
# Exécuter en tant qu'administrateur :
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Antivirus bloque**
1. Ajouter le dossier aux exceptions de l'antivirus
2. Ou désactiver temporairement la protection

### **Erreur de permissions**
1. Clic droit sur `install.bat` → "Exécuter en tant qu'administrateur"
2. Ou déplacer le projet vers `C:\facturacion_facil`

## 📁 Fichiers importants

- **`install.bat`** - Installation automatique complète
- **`start.bat`** - Lancement rapide de l'application
- **`start.ps1`** - Version PowerShell (plus d'infos)
- **[INSTALLATION_WINDOWS11.md](INSTALLATION_WINDOWS11.md)** - Guide détaillé

## 🆘 Support

### **Logs d'erreur**
Vérifier le dossier `logs/` :
- `app.log` - Log complet
- `error.log` - Erreurs uniquement

### **Test rapide**
```bash
# Dans PowerShell/CMD :
python --version
python -c "import PyQt5; print('OK')"
```

## 🎮 Utilisation quotidienne

### **Démarrage normal**
Double-clic sur `start.bat`

### **Mise à jour**
```bash
git pull
install.bat
```

### **Raccourci bureau**
Créer un raccourci vers `start.bat` sur le bureau

## ✅ Installation réussie si...

- [ ] `install.bat` se termine sans erreur
- [ ] `start.bat` lance l'application
- [ ] Fenêtre principale s'affiche
- [ ] Scroll fonctionne avec la molette dans Productos/Organización/Facturas

## 🎉 Prêt à utiliser !

Une fois installé, l'application est prête à utiliser avec toutes les nouvelles fonctionnalités de scroll !

---

**💡 Astuce :** Garde `start.bat` sur ton bureau pour un accès rapide à l'application.
