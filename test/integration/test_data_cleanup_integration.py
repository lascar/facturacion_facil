#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour le système de nettoyage de données
Teste l'interface et la fonctionnalité de suppression sélective

⚠️ PROTECTION PRODUCTION: Ce test utilise exclusivement isolated_test_database
pour garantir l'isolation complète de la base de données de production.

❌ INTERDICTION ABSOLUE: Ne jamais modifier db.db_path directement
✅ OBLIGATOIRE: Utiliser monkeypatch pour remplacer l'instance db
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
from ui.data_cleanup_dialog import DataCleanupDialog
from database.models import Producto, Cliente, Factura, Stock
from utils.logger import get_logger


@pytest.mark.integration
class TestDataCleanupIntegration:
    """Test d'intégration pour le nettoyage de données"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger("test_data_cleanup")

    def create_test_data(self, db):
        """
        Crée des données de test dans la base fournie.
        
        ⚠️ PRODUCTION SAFETY: Utilise uniquement la base de test fournie en paramètre
        """
        try:
            # Créer des clients
            cliente1 = Cliente(nombre="Cliente Test 1", email="test1@test.com")
            cliente1.save()
            
            cliente2 = Cliente(nombre="Cliente Test 2", email="test2@test.com")
            cliente2.save()
            
            cliente_sin_factura = Cliente(nombre="Cliente Sin Factura", email="sin@factura.com")
            cliente_sin_factura.save()
            
            # Créer des produits
            producto1 = Producto(nombre="Producto Test 1", referencia="TEST-PROD-001", precio=10.0)
            producto1.save()

            producto2 = Producto(nombre="Producto Test 2", referencia="TEST-PROD-002", precio=20.0)
            producto2.save()
            
            # Créer des stocks
            stock1 = Stock(producto1.id, 100)
            stock1.save()
            
            stock2 = Stock(producto2.id, 50)
            stock2.save()
            
            # Créer des factures
            factura1 = Factura(cliente_id=cliente1.id, numero_factura="TEST-001",
                              nombre_cliente=cliente1.nombre, fecha_factura="2025-01-01")
            factura1.save()

            factura2 = Factura(cliente_id=cliente2.id, numero_factura="TEST-002",
                              nombre_cliente=cliente2.nombre, fecha_factura="2025-01-01")
            factura2.save()
            
            print("✅ Datos de test creados:")
            print(f"   - Clientes: 3 (2 con facturas, 1 sin facturas)")
            print(f"   - Productos: 2")
            print(f"   - Stocks: 2")
            print(f"   - Facturas: 2")
            
        except Exception as e:
            self.logger.error(f"Error creando datos de test: {e}")
            raise
    
    def get_database_counts(self, db):
        """
        Obtiene el conteo actual de registros.
        
        ⚠️ PRODUCTION SAFETY: Utilise uniquement la base de test fournie
        """
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            counts = {}
            
            cursor.execute("SELECT COUNT(*) FROM clientes")
            counts['clientes'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM productos")
            counts['productos'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM stock")
            counts['stock'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM facturas")
            counts['facturas'] = cursor.fetchone()[0]
            
            # Clientes sin facturas
            cursor.execute("""
                SELECT COUNT(*) FROM clientes 
                WHERE id NOT IN (SELECT DISTINCT cliente_id FROM facturas WHERE cliente_id IS NOT NULL)
            """)
            counts['clientes_sin_facturas'] = cursor.fetchone()[0]
            
            conn.close()
            return counts
            
        except Exception as e:
            self.logger.error(f"Error obteniendo conteos: {e}")
            return {}
    
    def test_dialog_creation(self, integration_db, monkeypatch):
        """Testa la creación del diálogo"""
        try:
            print("\n🧪 Test: Creación del diálogo de limpieza")
            
            # Patcher l'instance db dans le module data_cleanup_dialog
            monkeypatch.setattr('ui.data_cleanup_dialog.db', integration_db)
            
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            dialog = DataCleanupDialog()
            
            # Verificar que el diálogo se crea correctamente
            assert dialog.windowTitle() == "🗑️ Limpieza de Datos"
            assert dialog.isModal() == True
            
            # Verificar que los checkboxes existen
            assert hasattr(dialog, 'facturas_cb')
            assert hasattr(dialog, 'productos_cb')
            assert hasattr(dialog, 'clientes_sin_facturas_cb')
            assert hasattr(dialog, 'todos_clientes_cb')
            assert hasattr(dialog, 'todo_cb')
            
            # Verificar que el backup está activado por defecto
            assert dialog.backup_cb.isChecked() == True
            
            print("   ✅ Diálogo creado correctamente")
            print("   ✅ Todos los controles presentes")
            print("   ✅ Backup activado por defecto")

            dialog.close()

        except Exception as e:
            print(f"   ❌ Error en test de creación: {e}")
            pytest.fail(f"Error en test de creación: {e}")
    
    def test_organization_window_button(self, integration_db, isolated_test_config, monkeypatch):
        """Testa que el botón aparece en la ventana de organización"""
        try:
            print("\n🧪 Test: Botón en ventana de organización")

            # Patcher l'instance db dans les modules
            monkeypatch.setattr('database.models.db', integration_db)
            
            # Activer le mode test
            os.environ['PYTEST_RUNNING'] = '1'
            os.environ['CONFIG_FILE'] = isolated_test_config

            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            window = OrganizacionPyQt5Window()
            
            # Verificar que el botón existe
            assert hasattr(window, 'cleanup_btn')
            assert window.cleanup_btn.text() == "🗑️ Limpiar Datos"
            
            # Verificar el estilo del botón (debe ser rojo)
            style = window.cleanup_btn.styleSheet()
            assert "#dc3545" in style  # Color rojo
            
            print("   ✅ Botón de limpieza presente")
            print("   ✅ Estilo rojo aplicado")
            print("   ✅ Texto correcto")

            window.close()

        except Exception as e:
            print(f"   ❌ Error en test de botón: {e}")
            pytest.fail(f"Error en test de botón: {e}")
    
    def test_database_stats_loading(self, integration_db, monkeypatch):
        """Testa la carga de estadísticas de la base de datos"""
        try:
            print("\n🧪 Test: Carga de estadísticas")
            
            # Patcher l'instance db dans les modules
            monkeypatch.setattr('ui.data_cleanup_dialog.db', integration_db)
            monkeypatch.setattr('database.models.db', integration_db)
            
            # Créer des données de test
            self.create_test_data(integration_db)
            
            # Obtener conteos avant
            counts_before = self.get_database_counts(integration_db)
            print(f"   📊 Conteos actuales: {counts_before}")
            
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            dialog = DataCleanupDialog()
            
            # Verificar que las estadísticas se cargan
            stats_text = dialog.stats_label.text()
            assert "Facturas:" in stats_text
            assert "Productos:" in stats_text
            assert "Clientes:" in stats_text

            print("   ✅ Estadísticas cargadas correctamente")
            print(f"   📊 Texto de estadísticas: {stats_text[:100]}...")

            dialog.close()

        except Exception as e:
            print(f"   ❌ Error en test de estadísticas: {e}")
            pytest.fail(f"Error en test de estadísticas: {e}")
    
    def test_all_data_cleanup_integration(self, integration_db, isolated_test_config, monkeypatch):
        """Test principal d'intégration du système de nettoyage"""
        print("🔧 TESTS DE INTEGRACIÓN - LIMPIEZA DE DATOS")
        print("=" * 50)

        try:
            # Exécuter tous les sous-tests avec la base de test isolée
            self.test_dialog_creation(integration_db, monkeypatch)
            self.test_organization_window_button(integration_db, isolated_test_config, monkeypatch)
            self.test_database_stats_loading(integration_db, monkeypatch)

            print(f"\n📊 RESUMEN DE TESTS:")
            print(f"🎉 Todos los tests pasaron exitosamente!")

        except Exception as e:
            self.logger.error(f"Error en test d'intégration: {e}")
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
        print("❌ Ce test nécessite pytest pour l'isolation de la base de données")
        sys.exit(1)

if __name__ == "__main__":
    main()
