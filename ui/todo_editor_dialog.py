# -*- coding: utf-8 -*-
"""
Diálogo para editar el archivo TODO.md
Permite editar y guardar el contenido del archivo TODO
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.logger import get_logger


class TodoEditorDialog(QDialog):
    """Diálogo para editar el archivo TODO.md"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger("todo_editor_dialog")
        self.todo_file_path = "TODO.md"
        self.original_content = ""
        
        self.setWindowTitle("📝 Editor de TODO")
        self.setModal(False)  # Permettre l'accès aux autres fenêtres
        self.setFixedSize(600, 500)
        
        # Centrar en la pantalla
        if parent:
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        
        self.setup_ui()
        self.load_todo_content()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("📝 Editor de TODO")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instrucciones
        instructions_label = QLabel("Edita el contenido del archivo TODO.md:")
        instructions_label.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(instructions_label)
        
        # Editor de texto
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 11))
        self.text_edit.setPlaceholderText("Escribe aquí el contenido del TODO...")
        layout.addWidget(self.text_edit)
        
        # Información sobre formato
        format_info = QLabel("💡 El contenido se guardará en formato Markdown")
        format_info.setStyleSheet("color: #007acc; font-style: italic; margin: 5px 0;")
        layout.addWidget(format_info)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Guardar")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Conexiones
        self.save_btn.clicked.connect(self.save_todo)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        
    def load_todo_content(self):
        """Carga el contenido del archivo TODO.md"""
        try:
            if os.path.exists(self.todo_file_path):
                with open(self.todo_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.original_content = content
                    self.text_edit.setPlainText(content)
                    self.logger.info(f"Contenido TODO cargado desde {self.todo_file_path}")
            else:
                # Crear archivo TODO.md con contenido por defecto
                default_content = "# TODO\n\n- clientes\n- preparar para cado trimeste facturas pdf + resumen\n- historico de facturas pdf trimestre a trimetre"
                self.original_content = default_content
                self.text_edit.setPlainText(default_content)
                self.logger.info("Archivo TODO.md no existe, usando contenido por defecto")
                
        except Exception as e:
            self.logger.error(f"Error cargando TODO: {e}")
            QMessageBox.warning(self, "Error", f"Error al cargar el archivo TODO: {str(e)}")
            
    def save_todo(self):
        """Guarda el contenido editado en el archivo TODO.md"""
        try:
            content = self.text_edit.toPlainText()
            
            # Verificar si hay cambios
            if content == self.original_content:
                self.logger.info("No hay cambios en el TODO")
                self.accept()
                return
            
            # Asegurar que el contenido tenga formato Markdown
            if not content.strip().startswith("# TODO"):
                if content.strip():
                    content = "# TODO\n\n" + content
                else:
                    content = "# TODO\n\n"
            
            # Guardar el archivo
            with open(self.todo_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"TODO guardado exitosamente en {self.todo_file_path}")

            # Pas de message de confirmation ici - sera géré par la fenêtre parent
            self.accept()
            
        except Exception as e:
            self.logger.error(f"Error guardando TODO: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al guardar el archivo TODO: {str(e)}"
            )
            
    def cancel_edit(self):
        """Cancela la edición y cierra el diálogo"""
        current_content = self.text_edit.toPlainText()
        
        # Verificar si hay cambios no guardados
        if current_content != self.original_content:
            reply = QMessageBox.question(
                self,
                "Cambios no guardados",
                "Hay cambios no guardados. ¿Estás seguro de que quieres cancelar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        self.logger.info("Edición de TODO cancelada")
        self.reject()
