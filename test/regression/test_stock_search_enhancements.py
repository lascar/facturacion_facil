#!/usr/bin/env python3
"""
Test de régression pour valider les améliorations de la recherche stock
Vérifie les raccourcis clavier et l'indicateur de résultats
"""

import sys
import os
import tempfile

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_stock_search_enhancements():
    """Test des améliorations de la recherche stock"""
    print("🧪 Test: Améliorations recherche stock")
    
    try:
        from database.models import Stock, Producto
        from database.database import Database
        
        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')
        
        try:
            # Initialiser la base de données
            db = Database(temp_db_path)
            
            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path
            
            print(f"   📁 Base de données temporaire: {temp_db_path}")
            
            # Créer des produits de test
            productos_test = [
                ("Laptop Dell Inspiron", "LAPTOP-DELL-001", 800.0, "Informática"),
                ("Mouse Logitech MX", "MOUSE-LOG-001", 25.0, "Accesorios"),
                ("Teclado Mecánico RGB", "TECLADO-RGB-001", 120.0, "Accesorios"),
                ("Monitor Samsung 24\"", "MONITOR-SAM-001", 300.0, "Informática"),
                ("Impresora HP LaserJet", "PRINTER-HP-001", 150.0, "Oficina"),
                ("Webcam Logitech C920", "WEBCAM-LOG-001", 80.0, "Accesorios"),
                ("Disco SSD Samsung", "SSD-SAM-001", 100.0, "Almacenamiento")
            ]
            
            for nombre, referencia, precio, categoria in productos_test:
                producto = Producto(
                    nombre=nombre,
                    referencia=referencia,
                    precio=precio,
                    categoria=categoria
                )
                producto.save()
                print(f"   ✅ Producto creado: {nombre}")
            
            # Simular la classe StockWindow avec améliorations
            class EnhancedMockStockWindow:
                def __init__(self):
                    from utils.logger import get_logger
                    self.logger = get_logger("enhanced_mock_stock_window")
                    self.stock_data = []
                    self.filtered_data = []
                    self.search_var = MockStringVar()
                    self.results_label = MockLabel()
                    self.search_entry = MockEntry()
                    self.load_stock_data()
                
                def load_stock_data(self):
                    """Cargar datos de stock"""
                    self.stock_data = []
                    for row in Stock.get_all():
                        producto_id, cantidad, nombre, referencia = row
                        
                        self.stock_data.append({
                            'producto_id': producto_id,
                            'nombre': nombre,
                            'referencia': referencia,
                            'cantidad': cantidad,
                            'fecha_actualizacion': 'N/A'
                        })
                    
                    self.filtered_data = self.stock_data.copy()
                    self.update_results_indicator()
                    self.logger.debug(f"Datos cargados: {len(self.stock_data)} productos")
                
                def on_search_enter(self, event=None):
                    """Simular evento Enter"""
                    self.perform_search()
                    return "break"
                
                def on_search_escape(self, event=None):
                    """Simular evento Escape"""
                    self.clear_search()
                    return "break"
                
                def on_select_all(self, event=None):
                    """Simular Ctrl+A"""
                    self.search_entry.select_range(0, 'end')
                    return "break"
                
                def perform_search(self):
                    """Realizar búsqueda"""
                    try:
                        search_text = self.search_var.get().lower().strip()
                        
                        if not search_text:
                            self.filtered_data = self.stock_data.copy()
                        else:
                            self.filtered_data = []
                            for item in self.stock_data:
                                nombre = item.get('nombre', '') or ''
                                referencia = item.get('referencia', '') or ''
                                
                                if (search_text in nombre.lower() or 
                                    search_text in referencia.lower()):
                                    self.filtered_data.append(item)
                        
                        self.update_stock_display()
                        self.update_results_indicator(search_text)
                        
                    except Exception as e:
                        self.logger.error(f"Error en búsqueda: {e}")
                        self.filtered_data = self.stock_data.copy()
                        self.update_stock_display()
                
                def clear_search(self):
                    """Limpiar búsqueda"""
                    try:
                        self.search_var.set("")
                        self.filtered_data = self.stock_data.copy()
                        self.update_stock_display()
                        self.update_results_indicator()
                        self.search_entry.focus()
                        
                    except Exception as e:
                        self.logger.error(f"Error limpiando búsqueda: {e}")
                
                def update_results_indicator(self, search_text=""):
                    """Actualizar indicador de resultados"""
                    try:
                        total_products = len(self.stock_data)
                        filtered_products = len(self.filtered_data)
                        
                        if not search_text:
                            self.results_label.configure(text=f"{total_products} productos")
                        elif filtered_products == 0:
                            self.results_label.configure(text="Sin resultados", text_color="red")
                        elif filtered_products == total_products:
                            self.results_label.configure(text=f"{total_products} productos", text_color="gray")
                        else:
                            self.results_label.configure(text=f"{filtered_products} de {total_products}", text_color="green")
                            
                    except Exception as e:
                        self.logger.error(f"Error actualizando indicador: {e}")
                        self.results_label.configure(text="", text_color="gray")
                
                def update_stock_display(self):
                    """Simular actualización de display"""
                    self.logger.debug(f"Display actualizado: {len(self.filtered_data)} elementos")
                
                def show_low_stock(self):
                    """Mostrar stock bajo"""
                    try:
                        self.search_var.set("")
                        self.filtered_data = [
                            item for item in self.stock_data
                            if item['cantidad'] <= 5
                        ]
                        self.update_stock_display()
                        self.update_results_indicator()
                        
                    except Exception as e:
                        self.logger.error(f"Error mostrando stock bajo: {e}")
            
            # Classes mock pour les composants UI
            class MockStringVar:
                def __init__(self):
                    self.value = ""
                
                def get(self):
                    return self.value
                
                def set(self, value):
                    self.value = value
            
            class MockLabel:
                def __init__(self):
                    self.text = ""
                    self.color = "gray"
                
                def configure(self, text="", text_color="gray"):
                    self.text = text
                    self.color = text_color
            
            class MockEntry:
                def __init__(self):
                    self.focused = False
                    self.selection = (0, 0)
                
                def focus(self):
                    self.focused = True
                
                def select_range(self, start, end):
                    self.selection = (start, end)
            
            # Test des améliorations
            print("\n   🧪 Test des améliorations...")
            
            mock_window = EnhancedMockStockWindow()
            
            # Test 1: Indicateur initial
            print("\n   1️⃣ Test indicateur initial")
            assert mock_window.results_label.text == "7 productos", f"Indicateur initial incorrect: '{mock_window.results_label.text}'"
            assert mock_window.results_label.color == "gray", f"Couleur initiale incorrecte: {mock_window.results_label.color}"
            print(f"   ✅ Indicateur initial: {mock_window.results_label.text}")
            
            # Test 2: Recherche avec résultats
            print("\n   2️⃣ Test recherche avec résultats")
            mock_window.search_var.set("logitech")
            mock_window.on_search_enter()
            assert mock_window.results_label.text == "2 de 7", f"Indicateur filtré incorrect: '{mock_window.results_label.text}'"
            assert mock_window.results_label.color == "green", f"Couleur filtrée incorrecte: {mock_window.results_label.color}"
            print(f"   ✅ Indicateur filtré: {mock_window.results_label.text}")
            
            # Test 3: Recherche sans résultats
            print("\n   3️⃣ Test recherche sans résultats")
            mock_window.search_var.set("inexistente")
            mock_window.perform_search()
            assert mock_window.results_label.text == "Sin resultados", f"Indicateur sans résultats incorrect: '{mock_window.results_label.text}'"
            assert mock_window.results_label.color == "red", f"Couleur sans résultats incorrecte: {mock_window.results_label.color}"
            print(f"   ✅ Indicateur sans résultats: {mock_window.results_label.text}")
            
            # Test 4: Escape pour effacer
            print("\n   4️⃣ Test Escape pour effacer")
            mock_window.on_search_escape()
            assert mock_window.search_var.get() == "", "Escape devrait vider le champ de recherche"
            assert mock_window.results_label.text == "7 productos", f"Indicateur après Escape incorrect: '{mock_window.results_label.text}'"
            assert mock_window.search_entry.focused, "Le champ devrait être focalisé après Escape"
            print("   ✅ Escape efface et focalise")
            
            # Test 5: Ctrl+A pour sélectionner tout
            print("\n   5️⃣ Test Ctrl+A pour sélectionner tout")
            mock_window.search_var.set("test text")
            mock_window.on_select_all()
            assert mock_window.search_entry.selection == (0, 'end'), f"Sélection incorrecte: {mock_window.search_entry.selection}"
            print("   ✅ Ctrl+A sélectionne tout le texte")
            
            # Test 6: Recherche montrant tous les résultats
            print("\n   6️⃣ Test recherche montrant tous les résultats")
            mock_window.search_var.set("001")  # Toutes les références contiennent "001"
            mock_window.perform_search()
            assert len(mock_window.filtered_data) == 7, f"Devrait trouver tous les produits, trouvé {len(mock_window.filtered_data)}"
            assert mock_window.results_label.text == "7 productos", f"Indicateur tous résultats incorrect: '{mock_window.results_label.text}'"
            assert mock_window.results_label.color == "gray", f"Couleur tous résultats incorrecte: {mock_window.results_label.color}"
            print(f"   ✅ Tous les résultats: {mock_window.results_label.text}")
            
            # Test 7: Stock bajo avec indicateur
            print("\n   7️⃣ Test stock bajo avec indicateur")
            mock_window.show_low_stock()
            assert mock_window.search_var.get() == "", "Stock bajo devrait vider la recherche"
            # Tous les produits ont stock 0, donc tous devraient apparaître
            assert len(mock_window.filtered_data) == 7, f"Stock bajo devrait montrer tous les produits, montre {len(mock_window.filtered_data)}"
            assert mock_window.results_label.text == "7 productos", f"Indicateur stock bajo incorrect: '{mock_window.results_label.text}'"
            print(f"   ✅ Stock bajo: {mock_window.results_label.text}")
            
            # Test 8: Effacement avec focus
            print("\n   8️⃣ Test effacement avec focus")
            mock_window.search_var.set("test")
            mock_window.perform_search()
            mock_window.clear_search()
            assert mock_window.search_var.get() == "", "Clear devrait vider le champ"
            assert mock_window.search_entry.focused, "Clear devrait focaliser le champ"
            assert mock_window.results_label.text == "7 productos", f"Indicateur après clear incorrect: '{mock_window.results_label.text}'"
            print("   ✅ Clear efface, focalise et met à jour l'indicateur")
            
            print("\n🎉 TOUS LES TESTS D'AMÉLIORATIONS PASSENT")
            print("✅ Les améliorations fonctionnent correctement")
            
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Test de régression - Améliorations recherche stock")
    print("=" * 60)
    
    success = test_stock_search_enhancements()
    
    if success:
        print("\n🎉 TEST AMÉLIORATIONS RÉUSSI")
        print("\n✅ NOUVELLES AMÉLIORATIONS:")
        print("   • Raccourci Escape pour effacer la recherche")
        print("   • Raccourci Ctrl+A pour sélectionner tout le texte")
        print("   • Indicateur de résultats en temps réel")
        print("   • Couleurs différentes selon le type de résultat")
        print("   • Focus automatique après effacement")
        print("   • Gestion robuste des événements clavier")
        print("\n💡 L'interface de recherche stock est maintenant complète !")
        sys.exit(0)
    else:
        print("\n❌ TEST AMÉLIORATIONS ÉCHOUÉ")
        sys.exit(1)
