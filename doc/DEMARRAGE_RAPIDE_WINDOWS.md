# ⚡ Démarrage Rapide - Windows 11

## 🎯 En 3 clics après `git clone`

### **1️⃣ Installation**
```bash
# Double-clic sur :
install.bat
```
*Installe Python, environnement virtuel et toutes les dépendances automatiquement*

### **2️⃣ Test**
```bash
# Double-clic sur :
test_windows.bat
```
*Vérifie que tout fonctionne correctement*

### **3️⃣ Lancement**
```bash
# Double-clic sur :
start.bat
```
*Lance l'application avec scroll activé !*

## 🖱️ Nouvelle fonctionnalité : Scroll avec molette

### **Où tester le scroll :**
1. **Productos** → Ouvrir et utiliser la molette
2. **Organización** → Scroller dans les formulaires longs
3. **Facturas** → Scroll dans l'interface complexe

### **Comment ça marche :**
- Molette vers le haut = Scroll vers le haut
- Molette vers le bas = Scroll vers le bas
- Fonctionne partout dans la fenêtre
- Scroll fluide et réactif

## 🔧 Si problème

### **Python pas trouvé**
1. Aller sur [python.org](https://python.org/downloads/windows/)
2. Télécharger Python 3.8+
3. ✅ **IMPORTANT :** Cocher "Add Python to PATH"
4. Installer et redémarrer
5. Relancer `install.bat`

### **Antivirus bloque**
1. Ajouter le dossier `facturacion_facil` aux exceptions
2. Ou désactiver temporairement l'antivirus
3. Relancer `install.bat`

### **Erreur permissions**
1. Clic droit sur `install.bat`
2. "Exécuter en tant qu'administrateur"

## 📁 Fichiers créés pour Windows

| Fichier | Description |
|---------|-------------|
| `install.bat` | Installation automatique complète |
| `start.bat` | Lancement rapide de l'app |
| `test_windows.bat` | Test de l'installation |
| `start.ps1` | Version PowerShell avancée |
| `README_WINDOWS.md` | Guide Windows complet |
| `INSTALLATION_WINDOWS11.md` | Installation détaillée |

## ✅ Checklist rapide

- [ ] `git clone` fait
- [ ] `install.bat` exécuté sans erreur
- [ ] `test_windows.bat` tous les tests passent
- [ ] `start.bat` lance l'application
- [ ] Scroll testé dans Productos/Organización/Facturas

## 🎉 C'est prêt !

Une fois ces étapes terminées, tu as :
- ✅ Application installée et fonctionnelle
- ✅ Scroll avec molette dans toutes les fenêtres
- ✅ Scripts de lancement automatiques
- ✅ Environnement Windows optimisé

## 💡 Utilisation quotidienne

### **Démarrage normal**
Double-clic sur `start.bat` (ou créer un raccourci sur le bureau)

### **Mise à jour**
```bash
git pull
install.bat  # Réinstalle si nouvelles dépendances
```

### **Dépannage**
```bash
test_windows.bat  # Diagnostique les problèmes
```

---

**🚀 Temps total d'installation : 2-5 minutes selon la connexion internet**
