#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier que le numéro de facture alphanumérique fonctionne
Lance l'application et permet de tester la sauvegarde de "fact-2005-1"
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Lancer l'application pour test manuel"""
    print("=" * 80)
    print("🧪 TEST MANUEL: Numéro de facture alphanumérique")
    print("=" * 80)
    print()
    print("Instructions:")
    print("1. Clique sur le bouton 'Organización'")
    print("2. Dans le champ 'Número Inicial de Factura', entre: fact-2005-1")
    print("3. Clique sur 'Guardar'")
    print("4. Vérifie qu'il n'y a PAS d'erreur de validation")
    print("5. Ferme et rouvre la fenêtre Organización")
    print("6. Vérifie que 'fact-2005-1' est bien affiché")
    print()
    print("Formats acceptés:")
    print("  ✅ 1")
    print("  ✅ 100")
    print("  ✅ fact-2005-1")
    print("  ✅ FAC-2025-001")
    print()
    print("Formats rejetés:")
    print("  ❌ (vide)")
    print("  ❌ ---  (pas de caractères alphanumériques)")
    print("  ❌ " + "a" * 51 + " (trop long)")
    print()
    print("=" * 80)
    print()
    
    app = QApplication(sys.argv)
    window = MainWindowPyQt5()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

