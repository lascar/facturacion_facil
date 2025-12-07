# -*- coding: utf-8 -*-
"""
Diálogo para limpieza selectiva de datos
Permite eliminar datos de forma controlada y segura
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QGroupBox, QTextEdit, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

from database.database import db
from utils.logger import get_logger
from auto_backup_system import AutoBackupSystem
import sqlite3

class DataCleanupWorker(QThread):
    """Worker thread para realizar la limpieza de datos"""
    
    progress_updated = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, cleanup_options, create_backup=True):
        super().__init__()
        self.cleanup_options = cleanup_options
        self.create_backup = create_backup
        self.logger = get_logger("data_cleanup_worker")
        
    def run(self):
        """Ejecuta la limpieza de datos"""
        try:
            total_steps = len([opt for opt in self.cleanup_options.values() if opt]) + (1 if self.create_backup else 0)
            current_step = 0
            
            # Crear backup si se solicita
            if self.create_backup:
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Creando backup de seguridad...")
                backup_system = AutoBackupSystem()
                backup_path = backup_system.create_backup("before_cleanup")
                if not backup_path:
                    self.finished_signal.emit(False, "Error creando backup de seguridad")
                    return
                current_step += 1
            
            conn = db.get_connection()
            cursor = conn.cursor()
            
            # Eliminar facturas y sus items
            if self.cleanup_options.get('facturas', False):
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Eliminando facturas...")
                cursor.execute("DELETE FROM factura_items")
                cursor.execute("DELETE FROM facturas")
                current_step += 1
            
            # Eliminar productos y stocks
            if self.cleanup_options.get('productos', False):
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Eliminando productos y stocks...")
                cursor.execute("DELETE FROM stock_movements")
                cursor.execute("DELETE FROM stock")
                cursor.execute("DELETE FROM productos")
                current_step += 1
            
            # Eliminar clientes sin facturas
            if self.cleanup_options.get('clientes_sin_facturas', False):
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Eliminando clientes sin facturas...")
                cursor.execute("""
                    DELETE FROM clientes 
                    WHERE id NOT IN (SELECT DISTINCT cliente_id FROM facturas WHERE cliente_id IS NOT NULL)
                """)
                current_step += 1
            
            # Eliminar todos los clientes
            if self.cleanup_options.get('todos_clientes', False):
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Eliminando todos los clientes...")
                cursor.execute("DELETE FROM clientes")
                current_step += 1
            
            # Eliminar TODO
            if self.cleanup_options.get('todo', False):
                self.progress_updated.emit(int((current_step / total_steps) * 100), "Eliminando todos los datos...")
                cursor.execute("DELETE FROM factura_items")
                cursor.execute("DELETE FROM facturas")
                cursor.execute("DELETE FROM stock_movements")
                cursor.execute("DELETE FROM stock")
                cursor.execute("DELETE FROM productos")
                cursor.execute("DELETE FROM clientes")
                current_step += 1
            
            conn.commit()
            conn.close()
            
            # Optimizar base de datos
            self.progress_updated.emit(95, "Optimizando base de datos...")
            conn = sqlite3.connect(db.db_path)
            conn.execute("VACUUM")
            conn.close()
            
            self.progress_updated.emit(100, "Limpieza completada")
            self.finished_signal.emit(True, "Limpieza de datos completada exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error durante la limpieza: {e}")
            self.finished_signal.emit(False, f"Error durante la limpieza: {str(e)}")

class DataCleanupDialog(QDialog):
    """Diálogo para limpieza selectiva de datos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger("data_cleanup_dialog")
        self.worker = None
        
        self.setWindowTitle("🗑️ Limpieza de Datos")
        self.setModal(True)
        self.setFixedSize(500, 600)
        
        # Centrar en la pantalla
        if parent:
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        
        self.setup_ui()
        self.load_database_stats()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout(self)
        
        # Título y advertencia
        title_label = QLabel("🗑️ Limpieza Selectiva de Datos")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        warning_label = QLabel("⚠️ ATENCIÓN: Esta operación eliminará datos permanentemente")
        warning_label.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)
        
        # Estadísticas actuales
        self.stats_group = QGroupBox("📊 Estado Actual de la Base de Datos")
        stats_layout = QVBoxLayout(self.stats_group)
        self.stats_label = QLabel("Cargando estadísticas...")
        stats_layout.addWidget(self.stats_label)
        layout.addWidget(self.stats_group)
        
        # Opciones de limpieza
        options_group = QGroupBox("🎯 Opciones de Limpieza")
        options_layout = QVBoxLayout(options_group)
        
        self.facturas_cb = QCheckBox("🧾 Eliminar todas las facturas y sus items")
        self.productos_cb = QCheckBox("📦 Eliminar todos los productos y stocks")
        self.clientes_sin_facturas_cb = QCheckBox("👤 Eliminar clientes sin facturas")
        self.todos_clientes_cb = QCheckBox("👥 Eliminar TODOS los clientes")
        self.todo_cb = QCheckBox("💥 ELIMINAR TODO (facturas, productos, clientes)")
        
        # Estilo para la opción más peligrosa
        self.todo_cb.setStyleSheet("QCheckBox { color: red; font-weight: bold; }")
        
        options_layout.addWidget(self.facturas_cb)
        options_layout.addWidget(self.productos_cb)
        options_layout.addWidget(self.clientes_sin_facturas_cb)
        options_layout.addWidget(self.todos_clientes_cb)
        options_layout.addWidget(QLabel(""))  # Separador
        options_layout.addWidget(self.todo_cb)
        
        layout.addWidget(options_group)
        
        # Opción de backup
        backup_group = QGroupBox("💾 Seguridad")
        backup_layout = QVBoxLayout(backup_group)
        self.backup_cb = QCheckBox("✅ Crear backup automático antes de eliminar")
        self.backup_cb.setChecked(True)  # Activado por defecto
        backup_layout.addWidget(self.backup_cb)
        layout.addWidget(backup_group)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.execute_btn = QPushButton("🗑️ Ejecutar Limpieza")
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        buttons_layout.addWidget(self.execute_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Conexiones
        self.execute_btn.clicked.connect(self.execute_cleanup)
        self.cancel_btn.clicked.connect(self.reject)
        self.todo_cb.toggled.connect(self.on_todo_toggled)
        
    def load_database_stats(self):
        """Carga las estadísticas de la base de datos"""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM facturas")
            facturas_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM productos")
            productos_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM clientes")
            clientes_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM stock")
            stock_count = cursor.fetchone()[0]
            
            # Clientes sin facturas
            cursor.execute("""
                SELECT COUNT(*) FROM clientes 
                WHERE id NOT IN (SELECT DISTINCT cliente_id FROM facturas WHERE cliente_id IS NOT NULL)
            """)
            clientes_sin_facturas = cursor.fetchone()[0]
            
            conn.close()
            
            stats_text = f"""
📊 Registros actuales:
• Facturas: {facturas_count}
• Productos: {productos_count}
• Clientes: {clientes_count}
• Entradas de stock: {stock_count}
• Clientes sin facturas: {clientes_sin_facturas}
            """.strip()
            
            self.stats_label.setText(stats_text)
            
        except Exception as e:
            self.logger.error(f"Error cargando estadísticas: {e}")
            self.stats_label.setText("Error cargando estadísticas de la base de datos")
    
    def on_todo_toggled(self, checked):
        """Maneja el cambio en la opción 'eliminar todo'"""
        if checked:
            # Desactivar otras opciones si se selecciona "todo"
            self.facturas_cb.setChecked(False)
            self.productos_cb.setChecked(False)
            self.clientes_sin_facturas_cb.setChecked(False)
            self.todos_clientes_cb.setChecked(False)
            
            self.facturas_cb.setEnabled(False)
            self.productos_cb.setEnabled(False)
            self.clientes_sin_facturas_cb.setEnabled(False)
            self.todos_clientes_cb.setEnabled(False)
        else:
            # Reactivar otras opciones
            self.facturas_cb.setEnabled(True)
            self.productos_cb.setEnabled(True)
            self.clientes_sin_facturas_cb.setEnabled(True)
            self.todos_clientes_cb.setEnabled(True)

    def execute_cleanup(self):
        """Ejecuta la limpieza de datos"""
        # Verificar que al menos una opción esté seleccionada
        cleanup_options = {
            'facturas': self.facturas_cb.isChecked(),
            'productos': self.productos_cb.isChecked(),
            'clientes_sin_facturas': self.clientes_sin_facturas_cb.isChecked(),
            'todos_clientes': self.todos_clientes_cb.isChecked(),
            'todo': self.todo_cb.isChecked()
        }

        if not any(cleanup_options.values()):
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar al menos una opción de limpieza.")
            return

        # Confirmar la operación
        selected_options = []
        if cleanup_options['facturas']:
            selected_options.append("• Facturas y sus items")
        if cleanup_options['productos']:
            selected_options.append("• Productos y stocks")
        if cleanup_options['clientes_sin_facturas']:
            selected_options.append("• Clientes sin facturas")
        if cleanup_options['todos_clientes']:
            selected_options.append("• TODOS los clientes")
        if cleanup_options['todo']:
            selected_options.append("• TODO (facturas, productos, clientes)")

        confirmation_text = f"""
⚠️ CONFIRMACIÓN DE ELIMINACIÓN ⚠️

Estás a punto de eliminar:
{chr(10).join(selected_options)}

{'✅ Se creará un backup automático antes de la eliminación.' if self.backup_cb.isChecked() else '❌ NO se creará backup automático.'}

Esta operación NO se puede deshacer.

¿Estás seguro de que quieres continuar?
        """.strip()

        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            confirmation_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Deshabilitar botones y mostrar progreso
        self.execute_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)

        # Crear y ejecutar worker
        self.worker = DataCleanupWorker(cleanup_options, self.backup_cb.isChecked())
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.finished_signal.connect(self.on_cleanup_finished)
        self.worker.start()

    def on_progress_updated(self, progress, message):
        """Actualiza la barra de progreso"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)

    def on_cleanup_finished(self, success, message):
        """Maneja la finalización de la limpieza"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

        if success:
            QMessageBox.information(self, "Éxito", message)
            # Recargar estadísticas
            self.load_database_stats()
            self.accept()  # Cerrar el diálogo
        else:
            QMessageBox.critical(self, "Error", message)

        # Reactivar botones
        self.execute_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)

        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker = None

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Operación en curso",
                "Hay una operación de limpieza en curso. ¿Quieres cancelarla?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.worker.terminate()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
