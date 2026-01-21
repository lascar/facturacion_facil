# -*- coding: utf-8 -*-
"""
Tests de comportement pour vérifier que les fenêtres sont scrollables
"""

import pytest
from PyQt5.QtWidgets import QScrollArea
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from ui.facturas_pyqt5 import FacturasPyQt5Window
from ui.factura_edit_window import FacturaEditWindow


class TestScrollableWindowsBehaviour(BaseBehaviourTest):
    """Tests pour vérifier que les fenêtres sont scrollables"""

    def test_factura_edit_window_is_scrollable(self, temp_db, app_instance):
        """
        GIVEN: Une fenêtre FacturaEditWindow
        WHEN: La fenêtre est créée
        THEN: Elle doit contenir un QScrollArea pour le contenu
        """
        self.logger.info("🧪 Test: FacturaEditWindow doit être scrollable")

        # GIVEN: Créer la fenêtre
        edit_window = FacturaEditWindow(database_instance=temp_db)
        self.wait_and_process_events(200)
        
        # WHEN: Vérifier la présence d'un QScrollArea
        scroll_areas = []
        for child in edit_window.findChildren(QScrollArea):
            scroll_areas.append(child)
        
        # THEN: Il doit y avoir au moins un QScrollArea
        assert len(scroll_areas) > 0, "FacturaEditWindow doit contenir un QScrollArea"
        
        # Vérifier que le QScrollArea est configuré correctement
        scroll_area = scroll_areas[0]
        assert scroll_area.widgetResizable(), "Le QScrollArea doit avoir widgetResizable=True"
        assert scroll_area.widget() is not None, "Le QScrollArea doit contenir un widget"
        
        self.logger.info(f"✅ FacturaEditWindow contient {len(scroll_areas)} QScrollArea(s)")
        
        # Nettoyer
        edit_window.close()

    def test_facturas_pyqt5_window_is_scrollable(self, temp_db, app_instance):
        """
        GIVEN: Une fenêtre FacturasPyQt5Window
        WHEN: La fenêtre est créée
        THEN: Elle doit avoir le scroll activé via BasePyQt5Window
        """
        self.logger.info("🧪 Test: FacturasPyQt5Window doit être scrollable")

        # GIVEN: Créer la fenêtre
        facturas_window = FacturasPyQt5Window()
        self.wait_and_process_events(200)
        
        # WHEN: Vérifier la présence du scrollable_widget (de BasePyQt5Window)
        has_scrollable_widget = hasattr(facturas_window, 'scrollable_widget')
        
        # THEN: Le scrollable_widget doit exister
        assert has_scrollable_widget, "FacturasPyQt5Window doit avoir un scrollable_widget"
        
        if has_scrollable_widget:
            assert facturas_window.scrollable_widget is not None, "scrollable_widget ne doit pas être None"
            self.logger.info("✅ FacturasPyQt5Window a le scroll activé via BasePyQt5Window")
        
        # Vérifier aussi la présence de QScrollArea
        scroll_areas = facturas_window.findChildren(QScrollArea)
        if len(scroll_areas) > 0:
            self.logger.info(f"✅ FacturasPyQt5Window contient {len(scroll_areas)} QScrollArea(s)")
        
        # Nettoyer
        facturas_window.close()

    def test_factura_edit_window_buttons_outside_scroll(self, temp_db, app_instance):
        """
        GIVEN: Une fenêtre FacturaEditWindow
        WHEN: La fenêtre est créée
        THEN: Les boutons doivent être en dehors du QScrollArea (toujours visibles)
        """
        self.logger.info("🧪 Test: Les boutons de FacturaEditWindow doivent être hors du scroll")

        # GIVEN: Créer la fenêtre
        edit_window = FacturaEditWindow(database_instance=temp_db)
        self.wait_and_process_events(200)
        
        # WHEN: Récupérer le QScrollArea et les boutons
        scroll_areas = edit_window.findChildren(QScrollArea)
        assert len(scroll_areas) > 0, "FacturaEditWindow doit contenir un QScrollArea"
        
        scroll_area = scroll_areas[0]
        scroll_widget = scroll_area.widget()
        
        # Chercher le bouton "Guardar"
        guardar_btn = None
        for child in edit_window.findChildren(type(edit_window).__bases__[0]):
            # Chercher dans les enfants directs de edit_window, pas dans scroll_widget
            pass
        
        # Vérifier que les boutons ne sont pas dans le scroll_widget
        buttons_in_main = []
        from PyQt5.QtWidgets import QPushButton
        for btn in edit_window.findChildren(QPushButton):
            # Vérifier si le bouton est un descendant du scroll_widget
            parent = btn.parent()
            is_in_scroll = False
            while parent is not None:
                if parent == scroll_widget:
                    is_in_scroll = True
                    break
                parent = parent.parent()
            
            if not is_in_scroll:
                buttons_in_main.append(btn.text())
        
        # THEN: Il doit y avoir des boutons en dehors du scroll
        self.logger.info(f"Boutons hors du scroll: {buttons_in_main}")
        assert len(buttons_in_main) > 0, "Il doit y avoir des boutons en dehors du QScrollArea"
        assert "Guardar" in buttons_in_main or "Cancelar" in buttons_in_main, \
            "Les boutons Guardar/Cancelar doivent être hors du scroll"
        
        self.logger.info(f"✅ {len(buttons_in_main)} boutons sont hors du scroll (toujours visibles)")
        
        # Nettoyer
        edit_window.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

