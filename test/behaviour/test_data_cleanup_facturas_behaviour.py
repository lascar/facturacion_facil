#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de comportement pour vérifier que 'Eliminar todas las facturas' fonctionne correctement.
Ce test reproduit le problème signalé : la suppression des factures ne fonctionne pas.

⚠️ PROTECTION PRODUCTION: Ce test utilise exclusivement isolated_test_database
pour garantir l'isolation complète de la base de données de production.

✅ CONFORME BDD: Utilise les fixtures standardisées (3 produits, 3 clients, 3 factures)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from unittest.mock import patch

from ui.data_cleanup_dialog import DataCleanupDialog, DataCleanupWorker


@pytest.mark.behaviour
class TestDataCleanupFacturasBehaviour:
    """Test de comportement pour la suppression des factures"""
    
    @pytest.fixture
    def app(self):
        """Fixture pour l'application Qt"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        yield app
    
    def get_counts(self, database):
        """Obtient le nombre de factures et items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM facturas")
        facturas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM factura_items")
        items = cursor.fetchone()[0]
        
        conn.close()
        
        return {'facturas': facturas, 'items': items}
    
    def test_eliminar_todas_las_facturas_fonctionne(self, app, isolated_test_database, monkeypatch):
        """
        Test que le bouton 'Eliminar todas las facturas' supprime réellement les factures.
        Ce test reproduit le problème signalé par l'utilisateur.
        
        ⚠️ PRODUCTION SAFETY: Utilise exclusivement isolated_test_database
        ✅ BDD: Utilise les 3 factures des fixtures standardisées
        """
        test_data = isolated_test_database
        
        # Patcher l'instance globale db dans le module
        monkeypatch.setattr('ui.data_cleanup_dialog.db', test_data)
        
        # Vérifier les données initiales (3 factures des fixtures)
        counts_before = self.get_counts(test_data)
        print(f"\n📊 Avant suppression: {counts_before}")
        assert counts_before['facturas'] == 3, f"Devrait y avoir 3 factures avant suppression (fixtures), a: {counts_before['facturas']}"
        assert counts_before['items'] > 0, "Devrait y avoir des items avant suppression"
        
        # Créer le dialogue
        dialog = DataCleanupDialog()
        
        # Cocher "Eliminar todas las facturas"
        dialog.facturas_cb.setChecked(True)
        assert dialog.facturas_cb.isChecked(), "La checkbox devrait être cochée"
        
        # Désactiver le backup pour accélérer le test
        dialog.backup_cb.setChecked(False)
        
        # Simuler le clic sur "Ejecutar Limpieza"
        # Mais d'abord, on mock le QMessageBox.question pour retourner Yes
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            # Exécuter la méthode
            dialog.execute_cleanup()
            
            # Attendre que le worker termine (avec timeout)
            if dialog.worker:
                dialog.worker.wait(5000)  # Attendre max 5 secondes
        
        # Vérifier les données après suppression
        counts_after = self.get_counts(test_data)
        print(f"📊 Après suppression: {counts_after}")
        
        # VÉRIFICATION CRITIQUE : Les factures doivent être supprimées
        assert counts_after['facturas'] == 0, f"❌ ERREUR: Les factures n'ont pas été supprimées! (reste: {counts_after['facturas']})"
        assert counts_after['items'] == 0, f"❌ ERREUR: Les items n'ont pas été supprimés! (reste: {counts_after['items']})"
        
        print("✅ SUCCÈS: Toutes les factures et items ont été supprimés")
        
        dialog.close()
    
    def test_worker_elimina_facturas_correctamente(self, app, isolated_test_database, monkeypatch):
        """
        Test que le DataCleanupWorker supprime correctement les factures.
        Test direct du worker sans l'interface.
        
        ⚠️ PRODUCTION SAFETY: Utilise exclusivement isolated_test_database
        ✅ BDD: Utilise les fixtures standardisées
        """
        test_data = isolated_test_database
        
        # Patcher l'instance globale db dans le module
        monkeypatch.setattr('ui.data_cleanup_dialog.db', test_data)
        
        # Vérifier les données initiales (3 factures des fixtures)
        counts_before = self.get_counts(test_data)
        print(f"\n📊 Worker test - Avant: {counts_before}")
        assert counts_before['facturas'] == 3, f"Devrait y avoir 3 factures (fixtures), a: {counts_before['facturas']}"
        
        # Créer et exécuter le worker
        cleanup_options = {
            'facturas': True,
            'productos': False,
            'clientes_sin_facturas': False,
            'todos_clientes': False,
            'todo': False
        }
        
        worker = DataCleanupWorker(cleanup_options, create_backup=False)
        
        # Capturer les signaux
        finished_result = {'success': None, 'message': None}
        
        def on_finished(success, message):
            finished_result['success'] = success
            finished_result['message'] = message
        
        worker.finished_signal.connect(on_finished)
        
        # Exécuter le worker
        worker.run()
        
        # Vérifier le résultat
        assert finished_result['success'] is True, f"Le worker a échoué: {finished_result['message']}"
        
        # Vérifier les données après
        counts_after = self.get_counts(test_data)
        print(f"📊 Worker test - Après: {counts_after}")
        
        assert counts_after['facturas'] == 0, f"❌ ERREUR: Les factures n'ont pas été supprimées par le worker!"
        assert counts_after['items'] == 0, f"❌ ERREUR: Les items n'ont pas été supprimés par le worker!"
        
        print("✅ SUCCÈS: Le worker supprime correctement les factures")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
