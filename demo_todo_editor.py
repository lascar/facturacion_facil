#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de l'éditeur de TODO
Lance l'interface d'organisation avec le bouton d'édition TODO
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from utils.logger import get_logger


def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION - ÉDITEUR TODO")
    print("=" * 35)
    print()
    print("Cette démonstration lance l'interface d'organisation")
    print("avec le nouveau bouton d'édition TODO.")
    print()
    print("📝 FONCTIONNALITÉS:")
    print("   • Bouton bleu '📝 Editar TODO' dans l'interface d'organisation")
    print("   • Éditeur de texte pour modifier le contenu TODO.md")
    print("   • Sauvegarde automatique en format Markdown")
    print("   • Boutons Guardar et Cancelar")
    print("   • Confirmation des changements non sauvegardés")
    print()
    print("🔒 SÉCURITÉ:")
    print("   • Confirmation avant annulation si changements non sauvegardés")
    print("   • Format Markdown automatiquement appliqué")
    print("   • Sauvegarde sécurisée avec gestion d'erreurs")
    print()
    print("📍 INSTRUCTIONS:")
    print("   1. La fenêtre d'organisation va s'ouvrir")
    print("   2. Cherchez le bouton bleu '📝 Editar TODO' en bas à droite")
    print("   3. Cliquez dessus pour ouvrir l'éditeur")
    print("   4. Modifiez le contenu et cliquez 'Guardar'")
    print("   5. Le fichier TODO.md sera mis à jour")
    print()
    
    try:
        # Créer l'application
        app = QApplication(sys.argv)
        
        # Créer et afficher la fenêtre d'organisation
        logger = get_logger("demo_todo_editor")
        logger.info("Iniciando demostración del editor TODO")
        
        org_window = OrganizacionPyQt5Window()
        org_window.show()
        
        # Message d'information
        QMessageBox.information(
            org_window,
            "🚀 Démonstration TODO Editor",
            "La fenêtre d'organisation est maintenant ouverte.\n\n"
            "Cherchez le bouton bleu '📝 Editar TODO' en bas à droite\n"
            "et cliquez dessus pour tester l'éditeur de TODO.\n\n"
            "Le fichier TODO.md sera créé/modifié dans le répertoire racine."
        )
        
        print("✅ Fenêtre d'organisation ouverte")
        print("   Cherchez le bouton '📝 Editar TODO' en bas à droite")
        print()
        print("🎯 TESTEZ MAINTENANT:")
        print("   • Cliquez sur le bouton bleu '📝 Editar TODO'")
        print("   • Modifiez le contenu dans l'éditeur")
        print("   • Cliquez 'Guardar' pour sauvegarder")
        print("   • Vérifiez que TODO.md a été mis à jour")
        print()
        
        # Lancer l'application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    main()
