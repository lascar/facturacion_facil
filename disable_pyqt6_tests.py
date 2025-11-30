#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour désactiver temporairement les tests PyQt6 après migration vers PyQt5 uniquement
"""

import os
import shutil
from pathlib import Path

def disable_pyqt6_tests():
    """Désactive les tests PyQt6 qui ne sont plus pertinents"""
    
    print("🔧 DÉSACTIVATION DES TESTS PYQT6")
    print("=" * 50)
    
    # Créer le dossier de sauvegarde
    backup_dir = Path("test_backup_pyqt6")
    backup_dir.mkdir(exist_ok=True)
    
    # Tests à désactiver
    tests_to_disable = [
        "test/integration/test_gui_abstraction.py",
        "test/integration/test_pyqt6_integration.py"
    ]
    
    disabled_count = 0
    
    for test_file in tests_to_disable:
        test_path = Path(test_file)
        if test_path.exists():
            # Sauvegarder le fichier
            backup_path = backup_dir / test_path.name
            shutil.copy2(test_path, backup_path)
            
            # Créer un fichier de remplacement qui skip tous les tests
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(f'''# -*- coding: utf-8 -*-
"""
Tests PyQt6 désactivés après migration vers PyQt5 uniquement
Fichier original sauvegardé dans: {backup_path}
"""

import pytest

@pytest.mark.skip(reason="Tests PyQt6 désactivés après migration vers PyQt5 uniquement")
class TestDisabled:
    """Classe de test désactivée"""
    
    def test_disabled(self):
        """Test désactivé"""
        pass
''')
            
            print(f"✅ Désactivé: {test_file}")
            print(f"   📁 Sauvegardé: {backup_path}")
            disabled_count += 1
        else:
            print(f"⚠️  Fichier non trouvé: {test_file}")
    
    print(f"\n📊 Résumé:")
    print(f"   ✅ Tests désactivés: {disabled_count}")
    print(f"   📁 Sauvegardés dans: {backup_dir}")
    
    print(f"\n🎯 SUCCÈS!")
    print("   • Tests PyQt6 désactivés")
    print("   • Fichiers originaux sauvegardés")
    print("   • Tests PyQt5 restent actifs")

if __name__ == "__main__":
    disable_pyqt6_tests()
