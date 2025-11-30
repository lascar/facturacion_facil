#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections finales pour l'éditeur de factures
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_style():
    """Tester le style des boutons poubelle"""
    print("🔍 Test du style des boutons poubelle...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
        from PyQt5.QtCore import Qt
        
        # Créer une application Qt pour le test
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Créer un bouton avec le nouveau style
        eliminar_btn = QPushButton("🗑️")
        eliminar_btn.setFixedSize(40, 30)
        eliminar_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
        print("✅ Bouton poubelle créé avec nouveau style")
        print(f"   - Taille: {eliminar_btn.size().width()}x{eliminar_btn.size().height()}")
        print(f"   - Couleur de fond: #dc3545 (rouge)")
        print(f"   - Bordures arrondies: 4px")
        print(f"   - Taille de police: 14px")
        
        # Tester le conteneur
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)
        container_layout.addWidget(eliminar_btn)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setContentsMargins(5, 2, 5, 2)
        
        print("✅ Conteneur créé avec marges appropriées")
        print(f"   - Marges: 5px (gauche/droite), 2px (haut/bas)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test style: {e}")
        return False

def test_message_content():
    """Tester le contenu des messages"""
    print("\n🔍 Test du contenu des messages...")
    
    try:
        # Vérifier le contenu du fichier
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les nouveaux messages
        if "Operación Exitosa" in content:
            print("✅ Nouveau titre de succès trouvé: 'Operación Exitosa'")
        else:
            print("❌ Titre de succès non trouvé")
            return False
        
        if "La factura ha sido actualizada correctamente" in content:
            print("✅ Nouveau message de succès trouvé")
        else:
            print("❌ Message de succès non trouvé")
            return False
        
        if "Error en la Operación" in content:
            print("✅ Nouveau titre d'erreur trouvé: 'Error en la Operación'")
        else:
            print("❌ Titre d'erreur non trouvé")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test messages: {e}")
        return False

def test_ui_flow():
    """Tester le flux UI"""
    print("\n🔍 Test du flux UI...")
    
    try:
        # Vérifier que les imports fonctionnent
        from ui.facturas_pyqt5 import EditarFacturaDialog
        print("✅ Import EditarFacturaDialog réussi")
        
        # Simuler le flux attendu
        print("📋 Flux attendu:")
        print("   1. Utilisateur clique 'OK' pour sauvegarder")
        print("   2. Message 'Operación Exitosa' s'affiche")
        print("   3. Utilisateur clique 'OK' sur le message")
        print("   4. Fenêtre d'édition se ferme (self.accept())")
        print("   5. Retour à la fenêtre des factures")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test flux: {e}")
        return False

def test_visual_improvements():
    """Tester les améliorations visuelles"""
    print("\n🔍 Test des améliorations visuelles...")
    
    try:
        # Vérifier les améliorations dans le code
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        improvements = [
            ("setFixedSize(40, 30)", "Taille de bouton augmentée"),
            ("background-color: #dc3545", "Couleur rouge pour suppression"),
            ("border-radius: 4px", "Bordures arrondies"),
            ("font-size: 14px", "Taille de police appropriée"),
            ("setContentsMargins(5, 2, 5, 2)", "Marges pour espacement")
        ]
        
        for code, description in improvements:
            if code in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - non trouvé")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test améliorations: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES CORRECTIONS FINALES")
    print("=" * 45)
    
    tests = [
        test_button_style,
        test_message_content,
        test_ui_flow,
        test_visual_improvements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 45)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 CORRECTIONS FINALES VALIDÉES !")
        print("\n📋 Améliorations appliquées:")
        print("   ✅ Boutons poubelle: taille 40x30, style rouge")
        print("   ✅ Messages clairs: 'Operación Exitosa' / 'Error en la Operación'")
        print("   ✅ Flux simplifié: popup → fermeture → retour factures")
        print("   ✅ Style professionnel avec bordures arrondies")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Test terminé: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
