#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogo copiable de emergencia usando PyQt5
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QTextEdit, QPushButton, QApplication, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def show_emergency_copyable_warning(parent, title, message):
    """Diálogo copiable de emergencia usando PyQt5"""
    print("🚨 EMERGENCY: Usando diálogo de emergencia PyQt5")

    try:
        # Crear aplicación si no existe
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Crear ventana de diálogo con PyQt5
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(450, 300)
        dialog.setModal(True)

        # Centrar en pantalla
        dialog.move(300, 200)

        print("✅ EMERGENCY: Ventana PyQt5 creada")

        # Layout principal
        layout = QVBoxLayout(dialog)

        # Título
        title_label = QLabel(title)
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Mensaje en TextEdit (copiable)
        text_widget = QTextEdit()
        text_widget.setPlainText(message)
        text_widget.setReadOnly(True)
        text_widget.setFont(QFont("Arial", 11))
        layout.addWidget(text_widget)

        # Frame de botones
        buttons_layout = QHBoxLayout()

        result = {"clicked": None}

        def copy_message():
            """Copiar mensaje al portapapeles"""
            try:
                clipboard = QApplication.clipboard()
                clipboard.setText(f"{title}\n\n{message}")
                print("✅ EMERGENCY: Mensaje copiado al portapapeles")

                # Cambiar texto del botón temporalmente
                copy_btn.setText("✅ COPIADO")
                from PyQt5.QtCore import QTimer
                timer = QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(lambda: copy_btn.setText("📋 COPIAR"))
                timer.start(1500)

            except Exception as e:
                print(f"❌ EMERGENCY: Error copiando: {e}")

        def ok_clicked():
            result["clicked"] = "ok"
            dialog.accept()

        # Botón COPIAR - ESTILO LLAMATIVO
        copy_btn = QPushButton("📋 COPIAR")
        copy_btn.clicked.connect(copy_message)
        copy_btn.setFont(QFont("Arial", 12, QFont.Bold))
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                border: 3px solid #FF4444;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
        """)
        buttons_layout.addWidget(copy_btn)

        # Botón OK
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(ok_clicked)
        ok_btn.setFont(QFont("Arial", 12))
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 3px solid #4CAF50;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        buttons_layout.addWidget(ok_btn)

        layout.addLayout(buttons_layout)

        print("✅ EMERGENCY: Botones PyQt5 creados - COPIAR debería ser MUY VISIBLE (rojo)")

        # Focus en OK
        ok_btn.setFocus()

        # Mostrar diálogo
        dialog.raise_()
        dialog.activateWindow()

        print("🔍 EMERGENCY: Mostrando diálogo PyQt5...")
        dialog.exec_()

        print("✅ EMERGENCY: Diálogo PyQt5 cerrado")
        return result["clicked"]

    except Exception as e:
        print(f"❌ EMERGENCY: Error en diálogo de emergencia PyQt5: {e}")
        import traceback
        print(f"❌ EMERGENCY: Traceback: {traceback.format_exc()}")

        # Último recurso: messagebox estándar PyQt5
        return QMessageBox.warning(parent, title, message)

if __name__ == "__main__":
    print("🧪 Test: Diálogo de Emergencia PyQt5")

    try:
        app = QApplication([])

        # Test del diálogo de emergencia
        result = show_emergency_copyable_warning(
            None,
            "Emergency Test",
            "Este es un diálogo de emergencia usando PyQt5.\n\nDebe tener un botón COPIAR rojo muy visible.\n\nEste es el último recurso si otros frameworks fallan."
        )

        print(f"Resultado: {result}")

    except Exception as e:
        print(f"Error en test: {e}")
        import traceback
        traceback.print_exc()
