#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo de configuración de Verifacti.

Permite configurar los datos necesarios para la integración con Verifacti API.
"""

import logging
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout, QGroupBox,
    QCheckBox
)
from PyQt5.QtCore import Qt

from services.verifacti_service import (
    ConfigVerifacti, cargar_configuracion, guardar_configuracion,
    inicializar_directorios, verificar_conectividad
)

logger = logging.getLogger(__name__)


class VerifactiConfigDialog(QDialog):
    """Diálogo para configurar la integración con Verifacti."""
    
    def __init__(self, parent: Optional[QDialog] = None) -> None:
        super().__init__(parent)
        self.config = cargar_configuracion()
        self._setup_ui()
        self._cargar_datos_existentes()
    
    def _setup_ui(self) -> None:
        """Configura la interfaz del diálogo."""
        self.setWindowTitle("Configuración de Verifacti")
        self.setMinimumWidth(450)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Grupo de información de la empresa
        grupo_empresa = QGroupBox("Datos de la empresa")
        form_layout = QFormLayout()
        
        self.txt_nif = QLineEdit()
        self.txt_nif.setPlaceholderText("Ej: 12345678A")
        form_layout.addRow("NIF/CIF:*", self.txt_nif)
        
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre completo de la empresa")
        form_layout.addRow("Nombre empresa:*", self.txt_nombre)
        
        self.txt_serie = QLineEdit()
        self.txt_serie.setPlaceholderText("A")
        form_layout.addRow("Serie facturas:", self.txt_serie)
        
        grupo_empresa.setLayout(form_layout)
        layout.addWidget(grupo_empresa)
        
        # Grupo de API
        grupo_api = QGroupBox("Credenciales API")
        api_layout = QFormLayout()
        
        self.txt_api_key = QLineEdit()
        self.txt_api_key.setEchoMode(QLineEdit.Password)
        self.txt_api_key.setPlaceholderText("API Key de Verifacti")
        api_layout.addRow("API Key:*", self.txt_api_key)
        
        self.chk_mostrar_key = QCheckBox("Mostrar API Key")
        self.chk_mostrar_key.stateChanged.connect(self._toggle_mostrar_key)
        api_layout.addRow("", self.chk_mostrar_key)
        
        # Botón de prueba
        btn_test = QPushButton("Probar conexión")
        btn_test.clicked.connect(self._probar_conexion)
        api_layout.addRow("", btn_test)
        
        grupo_api.setLayout(api_layout)
        layout.addWidget(grupo_api)
        
        # Información
        lbl_info = QLabel(
            "<i>* Campos obligatorios</i><br>"
            "<small>Los datos se guardarán en config/config.json</small>"
        )
        lbl_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_info)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setDefault(True)
        self.btn_guardar.clicked.connect(self._guardar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cancelar)
        botones_layout.addWidget(self.btn_guardar)
        
        layout.addLayout(botones_layout)
    
    def _cargar_datos_existentes(self) -> None:
        """Carga los datos existentes en los campos."""
        if self.config.nif:
            self.txt_nif.setText(self.config.nif)
        if self.config.nombre_empresa:
            self.txt_nombre.setText(self.config.nombre_empresa)
        if self.config.api_key:
            self.txt_api_key.setText(self.config.api_key)
        if self.config.serie_factura:
            self.txt_serie.setText(self.config.serie_factura)
    
    def _toggle_mostrar_key(self, state: int) -> None:
        """Muestra u oculta la API key."""
        if state == Qt.Checked:
            self.txt_api_key.setEchoMode(QLineEdit.Normal)
        else:
            self.txt_api_key.setEchoMode(QLineEdit.Password)
    
    def _validar_campos(self) -> bool:
        """Valida que los campos obligatorios estén completos."""
        campos_faltantes = []
        
        if not self.txt_nif.text().strip():
            campos_faltantes.append("NIF/CIF")
        if not self.txt_nombre.text().strip():
            campos_faltantes.append("Nombre empresa")
        if not self.txt_api_key.text().strip():
            campos_faltantes.append("API Key")
        
        if campos_faltantes:
            QMessageBox.warning(
                self,
                "Campos incompletos",
                f"Por favor complete los campos obligatorios:\n\n" + 
                "\n".join(f"• {c}" for c in campos_faltantes)
            )
            return False
        return True
    
    def _guardar(self) -> None:
        """Guarda la configuración."""
        if not self._validar_campos():
            return
        
        # Actualizar configuración
        self.config.nif = self.txt_nif.text().strip().upper()
        self.config.nombre_empresa = self.txt_nombre.text().strip()
        self.config.api_key = self.txt_api_key.text().strip()
        self.config.serie_factura = self.txt_serie.text().strip() or "A"
        self.config.habilitado = True
        
        # Guardar
        if guardar_configuracion(self.config):
            # Crear directorios
            try:
                inicializar_directorios()
                QMessageBox.information(
                    self,
                    "Configuración guardada",
                    "La configuración de Verifacti se ha guardado correctamente.\n\n"
                    "Se han creado los directorios:\n"
                    "• verifacti/enviadas\n"
                    "• verifacti/pendientes\n"
                    "• verifacti/errores"
                )
                self.accept()
            except Exception as e:
                logger.error(f"Error inicializando directorios: {e}")
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error creando directorios: {e}"
                )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar la configuración.\n"
                "Verifique que tiene permisos de escritura."
            )
    
    def _probar_conexion(self) -> None:
        """Prueba la conexión con la API."""
        api_key = self.txt_api_key.text().strip()
        if not api_key:
            QMessageBox.warning(
                self,
                "API Key requerida",
                "Por favor introduzca la API Key para probar la conexión."
            )
            return
        
        self.setEnabled(False)
        try:
            if verificar_conectividad(api_key):
                QMessageBox.information(
                    self,
                    "Conexión exitosa",
                    "La conexión con Verifacti se ha establecido correctamente."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error de conexión",
                    "No se pudo conectar con Verifacti.\n"
                    "Verifique su conexión a internet y la API Key."
                )
        finally:
            self.setEnabled(True)
    
    def get_config(self) -> ConfigVerifacti:
        """Retorna la configuración actual."""
        return self.config


def mostrar_dialogo_configuracion(parent: Optional[QDialog] = None) -> bool:
    """
    Muestra el diálogo de configuración de Verifacti.
    
    Args:
        parent: Ventana padre
        
    Returns:
        True si se guardó la configuración, False si se canceló
    """
    dialogo = VerifactiConfigDialog(parent)
    return dialogo.exec_() == QDialog.Accepted
