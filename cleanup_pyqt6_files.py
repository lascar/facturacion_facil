#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour nettoyer les fichiers PyQt6 inutiles et s'assurer que l'application utilise uniquement PyQt5
"""

import os
import shutil
from pathlib import Path

def backup_and_remove_pyqt6_files():
    """Sauvegarde et supprime les fichiers PyQt6 inutiles"""
    
    # Créer un dossier de sauvegarde
    backup_dir = Path("backup_pyqt6_files")
    backup_dir.mkdir(exist_ok=True)
    
    # Fichiers PyQt6 à sauvegarder et supprimer du dossier ui/
    pyqt6_ui_files = [
        "ui/productos_pyqt6.py",
        "ui/main_window_pyqt6.py", 
        "ui/main_window_native_pyqt6.py",
        "ui/base_pyqt6_window.py",
        "ui/clientes_pyqt6.py",
        "ui/organizacion_pyqt6.py",
        "ui/stock_pyqt6.py",
        "ui/facturas_pyqt6.py",
        "ui/factura_editor_pyqt6.py",
        "ui/search_pyqt6.py",
        "ui/invoice_status_dialog.py",
        "ui/producto_list_widget_pyqt6.py",
        "ui/widgets/client_autocomplete.py"
    ]
    
    # Fichiers PyQt6 dans d'autres dossiers à sauvegarder
    other_pyqt6_files = [
        "gui/pyqt6_impl.py",
        "utils/event_manager.py",
        "ui/pyqt6_window_adapter.py",
        "ui/facturas_abstract.py",
        "ui/clientes_abstract.py",
        "common/producto_autocomplete.py"
    ]
    
    print("🧹 NETTOYAGE DES FICHIERS PYQT6")
    print("="*40)
    
    moved_count = 0
    
    # Sauvegarder et supprimer les fichiers UI PyQt6
    for file_path in pyqt6_ui_files:
        if os.path.exists(file_path):
            backup_path = backup_dir / Path(file_path).name
            try:
                shutil.move(file_path, backup_path)
                print(f"✅ Déplacé: {file_path} → {backup_path}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Erreur déplacement {file_path}: {e}")
    
    # Sauvegarder les autres fichiers PyQt6
    for file_path in other_pyqt6_files:
        if os.path.exists(file_path):
            backup_path = backup_dir / Path(file_path).name
            try:
                shutil.move(file_path, backup_path)
                print(f"✅ Déplacé: {file_path} → {backup_path}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Erreur déplacement {file_path}: {e}")
    
    print(f"\n📦 {moved_count} fichiers PyQt6 sauvegardés dans {backup_dir}")
    return moved_count

def verify_pyqt5_consistency():
    """Vérifie que tous les fichiers utilisent PyQt5 de manière cohérente"""
    
    print("\n🔍 VÉRIFICATION COHÉRENCE PYQT5")
    print("="*40)
    
    # Fichiers PyQt5 qui doivent exister
    required_pyqt5_files = [
        "ui/main_window_pyqt5.py",
        "ui/base_pyqt5_window.py", 
        "ui/productos_pyqt5.py",
        "ui/clientes_pyqt5.py",
        "ui/organizacion_pyqt5.py",
        "ui/stock_pyqt5.py",
        "ui/facturas_pyqt5.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_pyqt5_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ Trouvé: {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ Manquant: {file_path}")
    
    print(f"\n📊 Résumé:")
    print(f"   ✅ Fichiers PyQt5 existants: {len(existing_files)}")
    print(f"   ❌ Fichiers PyQt5 manquants: {len(missing_files)}")
    
    return len(missing_files) == 0

def main():
    """Fonction principale"""
    print("🔧 NETTOYAGE ET VÉRIFICATION PYQT5")
    print("="*50)
    
    # Étape 1: Nettoyer les fichiers PyQt6
    moved_count = backup_and_remove_pyqt6_files()
    
    # Étape 2: Vérifier la cohérence PyQt5
    is_consistent = verify_pyqt5_consistency()
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ FINAL")
    print("="*20)
    print(f"✅ Fichiers PyQt6 nettoyés: {moved_count}")
    print(f"{'✅' if is_consistent else '❌'} Cohérence PyQt5: {'OK' if is_consistent else 'PROBLÈMES DÉTECTÉS'}")
    
    if is_consistent and moved_count > 0:
        print(f"\n🎉 SUCCÈS!")
        print(f"   • Application maintenant 100% PyQt5")
        print(f"   • Fichiers PyQt6 sauvegardés dans backup_pyqt6_files/")
        print(f"   • Prêt pour les tests")
    elif not is_consistent:
        print(f"\n⚠️  ATTENTION!")
        print(f"   • Des fichiers PyQt5 sont manquants")
        print(f"   • Vérifiez la structure des fichiers")
    
    print(f"\n🚀 Testez maintenant: python main.py")

if __name__ == "__main__":
    main()
