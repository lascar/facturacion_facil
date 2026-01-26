#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour l'éditeur de TODO
Teste l'interface et la fonctionnalité d'édition du TODO.md

Conforme aux préférences de développement :
- Tests intégrés comme tests de régression/intégration
- Utilise des fichiers temporaires séparés de la production
- Maintient la compatibilité avec la structure existante
"""

import sys
import os
import tempfile
import shutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Import pytest si disponible, sinon utiliser des décorateurs vides
try:
    import pytest
except ImportError:
    # Créer des décorateurs vides si pytest n'est pas disponible
    class pytest:
        class mark:
            @staticmethod
            def integration(func):
                return func

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from ui.todo_editor_dialog import TodoEditorDialog
from utils.logger import get_logger


@pytest.mark.integration
class TestTodoEditorIntegration:
    """Test d'intégration pour l'éditeur de TODO"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger("test_todo_editor")
        self.test_todo_path = None
        self.original_todo_path = None
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        self.cleanup_test_files()
        
    def setup_test_todo_file(self):
        """Crée un fichier TODO de test"""
        try:
            # Créer un fichier temporaire
            temp_dir = tempfile.mkdtemp()
            self.test_todo_path = os.path.join(temp_dir, "TODO.md")
            
            # Contenu de test
            test_content = """# TODO

- tâche de test 1
- tâche de test 2
- preparar para cado trimeste facturas pdf + resumen"""
            
            with open(self.test_todo_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Sauvegarder le chemin original et configurer le test
            from ui.todo_editor_dialog import TodoEditorDialog
            self.original_todo_path = TodoEditorDialog.__dict__.get('todo_file_path', 'TODO.md')
            
            self.logger.info(f"Fichier TODO de test créé: {self.test_todo_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando archivo TODO de test: {e}")
            return False
    
    def cleanup_test_files(self):
        """Nettoie les fichiers de test"""
        try:
            if self.test_todo_path and os.path.exists(self.test_todo_path):
                # Supprimer le répertoire temporaire
                temp_dir = os.path.dirname(self.test_todo_path)
                shutil.rmtree(temp_dir)
                self.logger.info("Fichiers de test TODO supprimés")
        except Exception as e:
            self.logger.error(f"Error limpiando archivos de test: {e}")
    
    def test_todo_dialog_creation(self):
        """Test de création du dialogue d'édition TODO"""
        print("\n🧪 Test: Creación del diálogo de edición TODO")
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        try:
            # Créer le dialogue
            dialog = TodoEditorDialog()
            
            # Vérifications de base
            assert dialog.windowTitle() == "📝 Editor de TODO"
            assert hasattr(dialog, 'text_edit')
            assert hasattr(dialog, 'save_btn')
            assert hasattr(dialog, 'cancel_btn')
            
            print("   ✅ Diálogo creado correctamente")
            print("   ✅ Todos los controles presentes")
            print("   ✅ Título configurado correctamente")
            
        except Exception as e:
            print(f"   ❌ Error en test de creación: {e}")
            raise
    
    def test_organization_window_todo_button(self, isolated_test_config):
        """Test du bouton TODO dans la fenêtre d'organisation"""
        print("\n🧪 Test: Botón TODO en ventana de organización")

        # Activer le mode test
        os.environ['PYTEST_RUNNING'] = '1'
        os.environ['CONFIG_FILE'] = isolated_test_config

        app = QApplication.instance() or QApplication(sys.argv)

        try:
            # Créer la fenêtre d'organisation
            org_window = OrganizacionPyQt5Window()
            
            # Vérifier que le bouton TODO existe
            assert hasattr(org_window, 'todo_btn')
            assert org_window.todo_btn.text() == "📝 Editar TODO"
            
            # Vérifier le style (couleur bleue)
            style = org_window.todo_btn.styleSheet()
            assert "#007bff" in style  # Couleur bleue
            
            print("   ✅ Botón TODO presente")
            print("   ✅ Texto correcto")
            print("   ✅ Estilo azul aplicado")
            
        except Exception as e:
            print(f"   ❌ Error en test de botón: {e}")
            raise
    
    def test_todo_content_loading(self):
        """Test du chargement du contenu TODO"""
        print("\n🧪 Test: Carga de contenido TODO")
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        try:
            # Créer le dialogue
            dialog = TodoEditorDialog()
            
            # Vérifier que le contenu est chargé
            content = dialog.text_edit.toPlainText()
            assert content.strip() != ""
            assert "TODO" in content
            
            print(f"   📄 Contenido cargado: {len(content)} caracteres")
            print("   ✅ Contenido TODO presente")
            
        except Exception as e:
            print(f"   ❌ Error en test de carga: {e}")
            raise
    
    def test_all_todo_editor_integration(self, isolated_test_config):
        """Test principal d'intégration de l'éditeur TODO"""
        print("🔧 TESTS DE INTEGRACIÓN - EDITOR TODO")
        print("=" * 45)

        try:
            # Exécuter tous les sous-tests
            self.test_todo_dialog_creation()
            self.test_organization_window_todo_button(isolated_test_config)
            self.test_todo_content_loading()

            print(f"\n📊 RESUMEN DE TESTS:")
            print(f"🎉 Todos los tests pasaron exitosamente!")

        except Exception as e:
            print(f"\n❌ Error en tests: {e}")
            raise


# Fonction pour exécution directe (compatibilité)
def main():
    """Fonction principale pour exécution directe"""
    try:
        # Essayer d'utiliser pytest si disponible
        import pytest as real_pytest
        real_pytest.main([__file__, "-v"])
    except ImportError:
        # Fallback : exécution directe
        print("🔧 Exécution directe (pytest non disponible)")
        tester = TestTodoEditorIntegration()
        tester.setup_method()
        try:
            tester.test_all_todo_editor_integration()
            print("✅ Test réussi")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Test échoué: {e}")
            sys.exit(1)
        finally:
            tester.teardown_method()

if __name__ == "__main__":
    main()
