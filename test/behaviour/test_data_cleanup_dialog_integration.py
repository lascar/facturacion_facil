#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration pour vérifier que le dialogue de nettoyage fonctionne correctement
avec des données réelles dans la base de données de test.

⚠️ PROTECTION PRODUCTION: Ce test utilise exclusivement clean_db
pour garantir l'isolation complète de la base de données de production.
"""

import pytest
import sys
import os

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtTest import QTest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from ui.data_cleanup_dialog import DataCleanupDialog


@pytest.mark.behaviour
class TestDataCleanupDialogIntegration:
    """Test d'intégration avec la base de données de test isolée"""
    
    @pytest.fixture
    def app(self):
        """Fixture pour l'application Qt"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        yield app
    
    def get_facturas_count(self, db):
        """Obtient le nombre de factures dans la base de données fournie"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_items_count(self, db):
        """Obtient le nombre d'items dans la base de données fournie"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factura_items")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def test_dialog_eliminar_facturas_real_db(self, app, clean_db, monkeypatch):
        """
        Test que le dialogue supprime réellement les factures de la base de données.
        Utilise la fixture clean_db qui fournit une base de test propre.
        
        ⚠️ PRODUCTION SAFETY: Utilise exclusivement clean_db
        """
        # Patcher l'instance db dans tous les modules utilisés
        monkeypatch.setattr('ui.data_cleanup_dialog.db', clean_db)
        monkeypatch.setattr('database.models.db', clean_db)
        
        from database.models import Factura, Cliente
        
        # Créer des données de test dans la base clean_db
        cliente = Cliente(nombre="Test Cliente", email="test@test.com")
        cliente.save()
        
        # Créer quelques factures
        factura1 = Factura(
            numero_factura="TEST-001",
            fecha_factura="2025-01-01",
            cliente_id=cliente.id,
            nombre_cliente=cliente.nombre,
            subtotal=100.0,
            total_iva=21.0,
            total_factura=121.0
        )
        factura1.save()
        
        factura2 = Factura(
            numero_factura="TEST-002",
            fecha_factura="2025-01-02",
            cliente_id=cliente.id,
            nombre_cliente=cliente.nombre,
            subtotal=200.0,
            total_iva=42.0,
            total_factura=242.0
        )
        factura2.save()
        
        # Ajouter des items via SQL direct
        conn = clean_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, subtotal, iva_amount, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (factura1.id, 1, 2, 50.0, 21.0, 100.0, 21.0, 121.0))
        cursor.execute("""
            INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, subtotal, iva_amount, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (factura2.id, 1, 4, 50.0, 21.0, 200.0, 42.0, 242.0))
        conn.commit()
        conn.close()
        
        # Vérifier les données initiales
        facturas_before = self.get_facturas_count(clean_db)
        items_before = self.get_items_count(clean_db)
        print(f"\n📊 Avant suppression: {facturas_before} facturas, {items_before} items")
        assert facturas_before >= 2, f"Devrait y avoir au moins 2 factures, trouvé: {facturas_before}"
        
        # Créer le dialogue
        dialog = DataCleanupDialog()
        
        # Cocher "Eliminar todas las facturas"
        dialog.facturas_cb.setChecked(True)
        assert dialog.facturas_cb.isChecked()
        
        # Désactiver le backup pour accélérer
        dialog.backup_cb.setChecked(False)
        
        # Capturer le signal finished pour attendre la fin
        cleanup_finished = {'finished': False, 'success': False}
        
        def on_finished(success, message):
            cleanup_finished['finished'] = True
            cleanup_finished['success'] = success
            cleanup_finished['message'] = message
        
        # Connecter le signal
        dialog.worker = None
        
        # Exécuter avec mock du QMessageBox de confirmation
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            dialog.execute_cleanup()
            
            # Connecter le signal après la création du worker
            if dialog.worker:
                dialog.worker.finished_signal.connect(on_finished)
                
                # Attendre que le worker termine
                timeout = 0
                while not cleanup_finished['finished'] and timeout < 50:  # Max 5 secondes
                    QTest.qWait(100)
                    timeout += 1
        
        # Vérifier le résultat
        print(f"Cleanup finished: {cleanup_finished}")
        assert cleanup_finished['finished'], "Le cleanup n'a pas terminé"
        assert cleanup_finished['success'], f"Le cleanup a échoué: {cleanup_finished.get('message', '')}"
        
        # Vérifier que les factures ont été supprimées
        facturas_after = self.get_facturas_count(clean_db)
        items_after = self.get_items_count(clean_db)
        print(f"📊 Après suppression: {facturas_after} facturas, {items_after} items")
        
        assert facturas_after == 0, f"❌ ERREUR: Il reste encore {facturas_after} factures!"
        assert items_after == 0, f"❌ ERREUR: Il reste encore {items_after} items!"
        
        print("✅ SUCCÈS: Toutes les factures ont été supprimées correctement")
        
        dialog.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
