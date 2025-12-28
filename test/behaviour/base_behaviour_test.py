# -*- coding: utf-8 -*-
"""
Classe de base pour tous les tests de comportement
"""

import pytest
import time
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from utils.logger import get_logger
from test.behaviour.utils.pyqt5_automation import PyQt5Automation

class BaseBehaviourTest:
    """Classe de base pour tous les tests de comportement"""

    def init_base_attributes(self):
        """Initialiser les attributs de base (appelé depuis setup_test)"""
        if not hasattr(self, 'logger'):
            self.logger = get_logger(self.__class__.__name__)
        if not hasattr(self, 'app'):
            self.app = None
        if not hasattr(self, 'main_window'):
            self.main_window = None
        if not hasattr(self, 'database'):
            self.database = None
        if not hasattr(self, 'config'):
            self.config = None
        if not hasattr(self, 'screenshots_dir'):
            self.screenshots_dir = None
        if not hasattr(self, 'automation'):
            self.automation = None
        
    def setup_method(self, method):
        """Configuration avant chaque test"""
        # S'assurer que les attributs de base sont initialisés
        self.init_base_attributes()

        if hasattr(self, 'logger'):
            self.logger.info(f"🧪 Début du test: {method.__name__}")

        # Initialiser l'automation si l'app est disponible
        if hasattr(self, 'app') and self.app and not self.automation:
            self.automation = PyQt5Automation(self.app)

        # Attendre que l'interface soit prête
        if hasattr(self, 'app') and self.app:
            self.app.processEvents()
            time.sleep(0.05)  # Réduit de 0.1 à 0.05
    
    def teardown_method(self, method):
        """Nettoyage après chaque test"""
        self.logger.info(f"✅ Fin du test: {method.__name__}")

        # Fermer toutes les fenêtres ouvertes
        self.close_all_windows()

        # Traiter les événements en attente plusieurs fois pour s'assurer de la fermeture
        if self.app:
            for _ in range(3):
                self.app.processEvents()
                time.sleep(0.05)
    
    def close_all_windows(self):
        """Fermer toutes les fenêtres ouvertes de manière robuste"""
        try:
            if self.app:
                # 1. Désactiver les boîtes de dialogue de confirmation pendant les tests
                self.disable_confirmation_dialogs()

                # 2. Fermer toutes les fenêtres top-level
                for widget in self.app.allWidgets():
                    if widget and hasattr(widget, 'close') and widget.isWindow():
                        try:
                            if widget.isVisible():
                                # Forcer la fermeture sans confirmation
                                self.force_close_widget(widget)
                                self.logger.debug(f"Fenêtre fermée: {widget.__class__.__name__}")
                        except Exception as e:
                            self.logger.warning(f"Erreur fermeture widget: {e}")

                # 3. Traiter les événements pour finaliser les fermetures
                self.app.processEvents()
                time.sleep(0.05)  # Réduit de 0.1 à 0.05

                # 4. Forcer la fermeture des fenêtres restantes
                remaining_windows = [w for w in self.app.allWidgets() if w and w.isWindow() and w.isVisible()]
                for window in remaining_windows:
                    try:
                        window.hide()
                        window.deleteLater()
                        self.logger.debug(f"Fenêtre forcée à fermer: {window.__class__.__name__}")
                    except Exception as e:
                        self.logger.warning(f"Erreur fermeture forcée: {e}")

                # 5. Traitement final des événements
                self.app.processEvents()
                time.sleep(0.05)  # Réduit de 0.1 à 0.05

            # 6. Fermer les fenêtres spécifiques du main_window si disponible
            if self.main_window:
                for attr_name in dir(self.main_window):
                    if attr_name.endswith('_window'):
                        window = getattr(self.main_window, attr_name, None)
                        if window and hasattr(window, 'close'):
                            try:
                                if window.isVisible():
                                    self.force_close_widget(window)
                                    self.logger.debug(f"Fenêtre spécifique fermée: {attr_name}")
                            except Exception as e:
                                self.logger.warning(f"Erreur fermeture {attr_name}: {e}")

        except Exception as e:
            self.logger.warning(f"Erreur lors de la fermeture des fenêtres: {e}")

    def disable_confirmation_dialogs(self):
        """Désactiver les boîtes de dialogue de confirmation pendant les tests"""
        try:
            # Marquer le mode test pour éviter les confirmations
            import os
            os.environ['PYTEST_RUNNING'] = '1'

            # Patcher QMessageBox.question pour retourner automatiquement Yes
            from PyQt5.QtWidgets import QMessageBox

            if not hasattr(self, '_original_question'):
                self._original_question = QMessageBox.question

                def mock_question(*args, **kwargs):
                    self.logger.debug("🔄 Dialog de confirmation intercepté - Réponse automatique: Yes")
                    return QMessageBox.Yes

                QMessageBox.question = mock_question

        except Exception as e:
            self.logger.warning(f"Erreur désactivation dialogs: {e}")

    def force_close_widget(self, widget):
        """Forcer la fermeture d'un widget sans confirmation"""
        try:
            # Méthode 1: Essayer la fermeture normale
            if hasattr(widget, 'close'):
                widget.close()
                return

            # Méthode 2: Cacher et supprimer
            if hasattr(widget, 'hide'):
                widget.hide()
            if hasattr(widget, 'deleteLater'):
                widget.deleteLater()

        except Exception as e:
            self.logger.warning(f"Erreur fermeture forcée widget: {e}")
    
    def wait_for_window(self, window, timeout=2):
        """Attendre qu'une fenêtre soit visible et prête"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if window and window.isVisible():
                self.app.processEvents()
                time.sleep(0.05)  # Délai réduit de 0.1 à 0.05
                return True
            self.app.processEvents()
            time.sleep(0.05)  # Délai réduit de 0.1 à 0.05
        return False

    def open_window_with_auto_close(self, window_opener_func, test_duration=2.0, *args, **kwargs):
        """
        Ouvrir une fenêtre avec fermeture automatique après un délai

        Args:
            window_opener_func: Fonction qui ouvre la fenêtre
            test_duration: Durée en secondes avant fermeture automatique
            *args, **kwargs: Arguments pour window_opener_func

        Returns:
            La fenêtre ouverte
        """
        # Ouvrir la fenêtre
        window = window_opener_func(*args, **kwargs)

        if window and self.app:
            # Attendre que la fenêtre soit visible
            self.wait_for_window(window, timeout=2)

            # Programmer la fermeture automatique
            def auto_close():
                try:
                    if window and window.isVisible():
                        self.logger.info(f"🔄 Fermeture automatique de {window.__class__.__name__}")
                        window.close()
                        self.app.processEvents()
                except Exception as e:
                    self.logger.warning(f"Erreur fermeture automatique: {e}")

            # Créer un timer pour la fermeture automatique
            timer = QTimer()
            timer.timeout.connect(auto_close)
            timer.setSingleShot(True)
            timer.start(int(test_duration * 1000))  # Convertir en millisecondes

            # Traiter les événements pendant la durée du test
            start_time = time.time()
            while time.time() - start_time < test_duration and window.isVisible():
                self.app.processEvents()
                time.sleep(0.05)  # Réduit de 0.1 à 0.05

            # S'assurer que la fenêtre est fermée
            if window.isVisible():
                window.close()
                self.app.processEvents()

        return window
    
    def click_button(self, button, wait_after=0.1):
        """Cliquer sur un bouton avec gestion d'erreur"""
        try:
            if button and button.isEnabled():
                button.click()
                self.app.processEvents()
                if wait_after > 0:
                    time.sleep(wait_after)
                return True
            else:
                self.logger.warning("Bouton non disponible ou désactivé")
                return False
        except Exception as e:
            self.logger.error(f"Erreur lors du clic sur le bouton: {e}")
            return False
    
    def set_text_field(self, field, text, wait_after=0.05):
        """Définir le texte d'un champ avec gestion d'erreur"""
        try:
            if field and hasattr(field, 'setText'):
                field.clear()
                field.setText(text)
                self.app.processEvents()
                if wait_after > 0:
                    time.sleep(wait_after)
                return True
            else:
                self.logger.warning("Champ de texte non disponible")
                return False
        except Exception as e:
            self.logger.error(f"Erreur lors de la saisie de texte: {e}")
            return False
    
    def take_screenshot(self, name="screenshot"):
        """Prendre une capture d'écran"""
        if not self.config or not self.config.get('screenshots', False):
            return
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            if self.main_window:
                pixmap = self.main_window.grab()
                pixmap.save(filepath)
                self.logger.info(f"📸 Capture d'écran sauvée: {filepath}")
                
        except Exception as e:
            self.logger.warning(f"Erreur lors de la capture d'écran: {e}")
    
    def slow_mode_wait(self):
        """Attendre en mode lent pour le débogage"""
        if self.config and self.config.get('slow', False):
            time.sleep(0.5)  # Réduit de 1.0 à 0.5
        else:
            time.sleep(0.05)  # Réduit de 0.1 à 0.05

    def wait_and_process_events(self, milliseconds):
        """Attendre un certain temps en millisecondes tout en traitant les événements"""
        if self.app:
            self.app.processEvents()
            QTest.qWait(milliseconds)
            self.app.processEvents()

    def assert_window_visible(self, window, window_name=""):
        """Vérifier qu'une fenêtre est visible"""
        assert window is not None, f"Fenêtre {window_name} n'existe pas"
        assert window.isVisible(), f"Fenêtre {window_name} n'est pas visible"
        self.logger.info(f"✅ Fenêtre {window_name} visible")
    
    def assert_button_enabled(self, button, button_name=""):
        """Vérifier qu'un bouton est activé"""
        assert button is not None, f"Bouton {button_name} n'existe pas"
        assert button.isEnabled(), f"Bouton {button_name} n'est pas activé"
        self.logger.info(f"✅ Bouton {button_name} activé")
    
    def assert_text_field_value(self, field, expected_value, field_name=""):
        """Vérifier la valeur d'un champ de texte"""
        assert field is not None, f"Champ {field_name} n'existe pas"
        actual_value = field.text() if hasattr(field, 'text') else str(field.value())
        assert actual_value == expected_value, f"Champ {field_name}: attendu '{expected_value}', obtenu '{actual_value}'"
        self.logger.info(f"✅ Champ {field_name} a la valeur correcte: {expected_value}")
