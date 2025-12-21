# -*- coding: utf-8 -*-
"""
Exemple de test avec fermeture automatique des fenêtres
"""

import pytest
import sys
import os
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTimer

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from utils.logger import get_logger


class TestAutoCloseExample(BaseBehaviourTest):
    """Exemple de test avec fermeture automatique des fenêtres"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir):
        """Configuration automatique pour chaque test"""
        self.init_base_attributes()
        
        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir
        self.logger = get_logger(self.__class__.__name__)
        
        if self.app:
            self.automation = PyQt5Automation(self.app)
    
    def test_stock_window_auto_close(self):
        """Test d'ouverture de la fenêtre stock avec fermeture automatique"""
        self.logger.info("🧪 Test fenêtre stock avec fermeture automatique")
        
        def open_stock_window():
            """Fonction pour ouvrir la fenêtre stock"""
            try:
                # Simuler l'ouverture de la fenêtre stock
                if hasattr(self.main_window, 'open_stock_window'):
                    return self.main_window.open_stock_window()
                elif hasattr(self.main_window, 'stock_window'):
                    stock_window = self.main_window.stock_window
                    if stock_window:
                        stock_window.show()
                        return stock_window
                else:
                    self.logger.warning("Méthode d'ouverture stock non trouvée")
                    return None
            except Exception as e:
                self.logger.error(f"Erreur ouverture stock: {e}")
                return None
        
        # Ouvrir la fenêtre avec fermeture automatique après 3 secondes
        stock_window = self.open_window_with_auto_close(
            open_stock_window,
            test_duration=3.0
        )
        
        if stock_window:
            self.logger.info("✅ Fenêtre stock ouverte et fermée automatiquement")
        else:
            self.logger.warning("⚠️ Impossible d'ouvrir la fenêtre stock")
    
    def test_productos_window_auto_close(self):
        """Test d'ouverture de la fenêtre productos avec fermeture automatique"""
        self.logger.info("🧪 Test fenêtre productos avec fermeture automatique")
        
        def open_productos_window():
            """Fonction pour ouvrir la fenêtre productos"""
            try:
                if hasattr(self.main_window, 'open_productos_window'):
                    return self.main_window.open_productos_window()
                elif hasattr(self.main_window, 'productos_window'):
                    productos_window = self.main_window.productos_window
                    if productos_window:
                        productos_window.show()
                        return productos_window
                else:
                    self.logger.warning("Méthode d'ouverture productos non trouvée")
                    return None
            except Exception as e:
                self.logger.error(f"Erreur ouverture productos: {e}")
                return None
        
        # Ouvrir la fenêtre avec fermeture automatique après 2 secondes
        productos_window = self.open_window_with_auto_close(
            open_productos_window,
            test_duration=2.0
        )
        
        if productos_window:
            self.logger.info("✅ Fenêtre productos ouverte et fermée automatiquement")
        else:
            self.logger.warning("⚠️ Impossible d'ouvrir la fenêtre productos")
    
    def test_multiple_windows_auto_close(self):
        """Test d'ouverture de plusieurs fenêtres avec fermeture automatique"""
        self.logger.info("🧪 Test ouverture multiple avec fermeture automatique")
        
        windows_opened = []
        
        # Ouvrir plusieurs fenêtres rapidement
        for window_name in ['stock', 'productos']:
            def open_window(name=window_name):
                try:
                    if name == 'stock' and hasattr(self.main_window, 'open_stock_window'):
                        return self.main_window.open_stock_window()
                    elif name == 'productos' and hasattr(self.main_window, 'open_productos_window'):
                        return self.main_window.open_productos_window()
                    else:
                        self.logger.warning(f"Méthode d'ouverture {name} non trouvée")
                        return None
                except Exception as e:
                    self.logger.error(f"Erreur ouverture {name}: {e}")
                    return None
            
            # Ouvrir avec fermeture automatique courte
            window = self.open_window_with_auto_close(
                open_window,
                test_duration=1.5
            )
            
            if window:
                windows_opened.append(window_name)
        
        self.logger.info(f"✅ {len(windows_opened)} fenêtres ouvertes et fermées automatiquement")
        
        # Vérifier qu'aucune fenêtre n'est restée ouverte
        remaining_windows = [w for w in self.app.allWidgets() if w and w.isWindow() and w.isVisible()]
        if remaining_windows:
            self.logger.warning(f"⚠️ {len(remaining_windows)} fenêtres encore ouvertes")
            # Forcer la fermeture
            self.close_all_windows()
        else:
            self.logger.info("✅ Toutes les fenêtres ont été fermées correctement")


if __name__ == '__main__':
    # Test direct sans pytest
    print("🧪 Test direct de fermeture automatique")
    
    app = QApplication([])
    
    # Simuler une fenêtre simple
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
    
    def create_test_window():
        window = QWidget()
        window.setWindowTitle("Test Auto Close")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Cette fenêtre se fermera automatiquement"))
        window.setLayout(layout)
        window.show()
        return window
    
    # Créer et fermer automatiquement
    window = create_test_window()
    
    def auto_close():
        print("🔄 Fermeture automatique...")
        window.close()
        app.quit()
    
    timer = QTimer()
    timer.timeout.connect(auto_close)
    timer.setSingleShot(True)
    timer.start(2000)  # 2 secondes
    
    print("✅ Fenêtre ouverte, fermeture dans 2 secondes...")
    app.exec_()
    print("✅ Test terminé")
