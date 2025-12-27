# -*- coding: utf-8 -*-
"""
Ventana de informe de facturación
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QFormLayout, QMessageBox, QTextEdit, QSplitter, QFileDialog,
    QComboBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
from database.database import db
from services.informes_service import InformesService
from utils.exceptions import ValidationError, DatabaseError
from utils.logger import get_logger
from utils.informe_pdf_generator import informe_pdf_generator
from utils.informe_charts import informe_chart_generator
from utils.excel_generator import ExcelGenerator


class InformeFacturacionDialog(QDialog):
    """Diálogo para generar informe de facturación"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        
        # Service
        db_path = db.db_path if hasattr(db, 'db_path') else None
        self.informes_service = InformesService(db_path)
        
        self.informe_data = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz"""
        self.setWindowTitle("Informe de Facturación")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("Informe de Facturación")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Selección de período
        period_group = QGroupBox("Período")
        period_layout = QFormLayout()

        # Presets de período
        self.period_preset = QComboBox()
        self.period_preset.addItems([
            "Personalizado",
            "Hoy",
            "Esta Semana",
            "Este Mes",
            "Último Mes",
            "Este Año",
            "Último Año"
        ])
        self.period_preset.currentTextChanged.connect(self.apply_period_preset)
        period_layout.addRow("Período Rápido:", self.period_preset)

        # Fecha inicio
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDisplayFormat("dd/MM/yyyy")
        # Por defecto: primer día del mes actual
        today = QDate.currentDate()
        first_day = QDate(today.year(), today.month(), 1)
        self.fecha_inicio.setDate(first_day)
        period_layout.addRow("Fecha Inicio:", self.fecha_inicio)

        # Fecha fin
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDisplayFormat("dd/MM/yyyy")
        self.fecha_fin.setDate(today)
        period_layout.addRow("Fecha Fin:", self.fecha_fin)

        # Filtro por cliente
        self.cliente_filter = QComboBox()
        self.cliente_filter.addItem("Todos los clientes", None)
        self.load_clientes()
        period_layout.addRow("Cliente:", self.cliente_filter)

        # Filtro por estado
        self.estado_filter = QComboBox()
        self.estado_filter.addItem("Todos los estados", None)
        self.load_estados()
        period_layout.addRow("Estado:", self.estado_filter)

        # Botón generar
        generate_btn = QPushButton("Generar Informe")
        generate_btn.clicked.connect(self.generate_informe)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        period_layout.addRow("", generate_btn)
        
        period_group.setLayout(period_layout)
        layout.addWidget(period_group)
        
        # Splitter para resumen, gráficos y tabla
        splitter = QSplitter(Qt.Vertical)

        # Resumen
        self.resumen_text = QTextEdit()
        self.resumen_text.setReadOnly(True)
        self.resumen_text.setMaximumHeight(150)
        splitter.addWidget(self.resumen_text)

        # Contenedor para gráficos
        self.chart_container = QLabel()
        self.chart_container.setAlignment(Qt.AlignCenter)
        self.chart_container.setMaximumHeight(300)
        self.chart_container.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        splitter.addWidget(self.chart_container)

        # Tabla de facturas
        self.facturas_table = QTableWidget()
        self.facturas_table.setColumnCount(7)
        self.facturas_table.setHorizontalHeaderLabels([
            "Número", "Fecha", "Cliente", "Subtotal", "IVA", "Total", "Estado"
        ])
        self.facturas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        splitter.addWidget(self.facturas_table)

        layout.addWidget(splitter)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Botón guardar HTML
        save_html_btn = QPushButton("Guardar HTML")
        save_html_btn.clicked.connect(self.save_html)
        save_html_btn.setEnabled(False)
        self.save_html_btn = save_html_btn
        buttons_layout.addWidget(save_html_btn)

        # Botón imprimir
        print_btn = QPushButton("Imprimir")
        print_btn.clicked.connect(self.print_report)
        print_btn.setEnabled(False)
        self.print_btn = print_btn
        buttons_layout.addWidget(print_btn)

        # Botón exportar PDF
        export_btn = QPushButton("Exportar PDF")
        export_btn.clicked.connect(self.export_pdf)
        export_btn.setEnabled(False)
        self.export_btn = export_btn
        buttons_layout.addWidget(export_btn)

        # Botón exportar Excel
        export_excel_btn = QPushButton("Exportar Excel")
        export_excel_btn.clicked.connect(self.export_excel)
        export_excel_btn.setEnabled(False)
        self.export_excel_btn = export_excel_btn
        buttons_layout.addWidget(export_excel_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def load_clientes(self):
        """Cargar la lista de clientes"""
        try:
            clientes = db.get_all_clients()
            for cliente in clientes:
                self.cliente_filter.addItem(
                    f"{cliente['nombre']} ({cliente['nif']})",
                    cliente['id']
                )
        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")

    def load_estados(self):
        """Cargar la lista de estados de facturas"""
        try:
            estados = db.get_all_invoice_statuses()
            for estado in estados:
                self.estado_filter.addItem(estado['nombre'], estado['nombre'])
        except Exception as e:
            self.logger.error(f"Error cargando estados: {e}")

    def apply_period_preset(self, preset):
        """Aplicar preset de período"""
        if preset == "Personalizado":
            return

        today = QDate.currentDate()

        if preset == "Hoy":
            self.fecha_inicio.setDate(today)
            self.fecha_fin.setDate(today)
        elif preset == "Esta Semana":
            # Lunes de esta semana
            days_since_monday = today.dayOfWeek() - 1
            monday = today.addDays(-days_since_monday)
            self.fecha_inicio.setDate(monday)
            self.fecha_fin.setDate(today)
        elif preset == "Este Mes":
            first_day = QDate(today.year(), today.month(), 1)
            self.fecha_inicio.setDate(first_day)
            self.fecha_fin.setDate(today)
        elif preset == "Último Mes":
            # Primer día del mes pasado
            if today.month() == 1:
                first_day = QDate(today.year() - 1, 12, 1)
                last_day = QDate(today.year() - 1, 12, 31)
            else:
                first_day = QDate(today.year(), today.month() - 1, 1)
                # Último día del mes pasado
                last_day = QDate(today.year(), today.month(), 1).addDays(-1)
            self.fecha_inicio.setDate(first_day)
            self.fecha_fin.setDate(last_day)
        elif preset == "Este Año":
            first_day = QDate(today.year(), 1, 1)
            self.fecha_inicio.setDate(first_day)
            self.fecha_fin.setDate(today)
        elif preset == "Último Año":
            first_day = QDate(today.year() - 1, 1, 1)
            last_day = QDate(today.year() - 1, 12, 31)
            self.fecha_inicio.setDate(first_day)
            self.fecha_fin.setDate(last_day)

    def generate_informe(self):
        """Generar el informe"""
        try:
            # Obtener fechas
            fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
            fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")

            # Generar informe
            self.informe_data = self.informes_service.get_informe_facturacion(
                fecha_inicio, fecha_fin
            )

            # Aplicar filtros
            facturas_filtradas = self.informe_data['facturas']

            # Filtro de cliente
            cliente_id = self.cliente_filter.currentData()
            if cliente_id is not None:
                facturas_filtradas = [
                    f for f in facturas_filtradas
                    if f.get('cliente_id') == cliente_id
                ]

            # Filtro de estado
            estado_nombre = self.estado_filter.currentData()
            if estado_nombre is not None:
                facturas_filtradas = [
                    f for f in facturas_filtradas
                    if f.get('estado') == estado_nombre
                ]

            # Aplicar facturas filtradas
            if cliente_id is not None or estado_nombre is not None:
                self.informe_data['facturas'] = facturas_filtradas
                # Recalcular resumen con facturas filtradas
                self.recalcular_resumen()

            # Mostrar resumen
            self.show_resumen()

            # Mostrar gráficos
            self.show_charts()

            # Mostrar facturas
            self.show_facturas()

            # Habilitar botones
            self.export_btn.setEnabled(True)
            self.export_excel_btn.setEnabled(True)
            self.save_html_btn.setEnabled(True)
            self.print_btn.setEnabled(True)

        except ValidationError as e:
            QMessageBox.warning(self, "Error de Validación", str(e))
        except DatabaseError as e:
            QMessageBox.critical(self, "Error de Base de Datos", str(e))

    def recalcular_resumen(self):
        """Recalcular el resumen después de filtrar"""
        facturas = self.informe_data['facturas']

        if not facturas:
            self.informe_data['resumen'] = {
                'num_facturas': 0,
                'subtotal': 0,
                'total_iva': 0,
                'total': 0,
                'promedio_factura': 0
            }
            return

        subtotal = sum(f.get('subtotal', 0) for f in facturas)
        total_iva = sum(f.get('iva', 0) for f in facturas)
        total = sum(f.get('total', 0) for f in facturas)

        self.informe_data['resumen'] = {
            'num_facturas': len(facturas),
            'subtotal': subtotal,
            'total_iva': total_iva,
            'total': total,
            'promedio_factura': total / len(facturas) if facturas else 0
        }

    def show_resumen(self):
        """Mostrar el resumen del informe"""
        if not self.informe_data:
            return

        resumen = self.informe_data['resumen']
        periodo = self.informe_data['periodo']
        desglose_iva = self.informe_data['desglose_iva']
        productos = self.informe_data['productos_mas_vendidos']

        html = f"""
        <h2>Resumen del Período</h2>
        <p><b>Desde:</b> {periodo['inicio']} <b>Hasta:</b> {periodo['fin']}</p>

        <h3>Totales</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr>
                <td><b>Número de Facturas:</b></td>
                <td align="right">{resumen['num_facturas']}</td>
            </tr>
            <tr>
                <td><b>Subtotal:</b></td>
                <td align="right">{resumen['subtotal']:.2f} €</td>
            </tr>
            <tr>
                <td><b>Total IVA:</b></td>
                <td align="right">{resumen['total_iva']:.2f} €</td>
            </tr>
            <tr style="background-color: #e0e0e0;">
                <td><b>TOTAL:</b></td>
                <td align="right"><b>{resumen['total']:.2f} €</b></td>
            </tr>
            <tr>
                <td><b>Promedio por Factura:</b></td>
                <td align="right">{resumen['promedio_factura']:.2f} €</td>
            </tr>
        </table>

        <h3>Desglose por IVA</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f0f0f0;">
                <th>IVA %</th>
                <th>Base Imponible</th>
                <th>Total IVA</th>
            </tr>
        """

        for item in desglose_iva:
            html += f"""
            <tr>
                <td align="center">{item['iva_aplicado']:.0f}%</td>
                <td align="right">{item['base_imponible']:.2f} €</td>
                <td align="right">{item['total_iva']:.2f} €</td>
            </tr>
            """

        html += "</table>"

        if productos:
            html += """
            <h3>Top 10 Productos Más Vendidos</h3>
            <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f0f0f0;">
                    <th>Producto</th>
                    <th>Referencia</th>
                    <th>Cantidad</th>
                    <th>Importe</th>
                </tr>
            """

            for prod in productos[:10]:
                html += f"""
                <tr>
                    <td>{prod['nombre']}</td>
                    <td>{prod['referencia']}</td>
                    <td align="center">{prod['cantidad']:.0f}</td>
                    <td align="right">{prod['importe']:.2f} €</td>
                </tr>
                """

            html += "</table>"

        self.resumen_text.setHtml(html)

    def show_charts(self):
        """Mostrar los gráficos"""
        if not self.informe_data:
            return

        try:
            # Generar gráfico
            chart_path = informe_chart_generator.create_facturacion_chart(self.informe_data)

            if chart_path and os.path.exists(chart_path):
                from PyQt5.QtGui import QPixmap
                pixmap = QPixmap(chart_path)
                # Escalar para ajustar al contenedor
                scaled_pixmap = pixmap.scaled(
                    self.chart_container.width() - 10,
                    self.chart_container.height() - 10,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.chart_container.setPixmap(scaled_pixmap)

                # Limpiar archivo temporal
                try:
                    os.unlink(chart_path)
                except:
                    pass
            else:
                self.chart_container.setText("No se pudieron generar los gráficos")

        except Exception as e:
            self.logger.error(f"Error mostrando gráficos: {e}")
            self.chart_container.setText(f"Error: {str(e)}")

    def show_facturas(self):
        """Mostrar la tabla de facturas"""
        if not self.informe_data:
            return

        facturas = self.informe_data['facturas']
        self.facturas_table.setRowCount(len(facturas))

        for row, factura in enumerate(facturas):
            self.facturas_table.setItem(row, 0, QTableWidgetItem(factura['numero']))
            self.facturas_table.setItem(row, 1, QTableWidgetItem(factura['fecha']))
            self.facturas_table.setItem(row, 2, QTableWidgetItem(factura['cliente']))
            self.facturas_table.setItem(row, 3, QTableWidgetItem(f"{factura['subtotal']:.2f} €"))
            self.facturas_table.setItem(row, 4, QTableWidgetItem(f"{factura['iva']:.2f} €"))
            self.facturas_table.setItem(row, 5, QTableWidgetItem(f"{factura['total']:.2f} €"))
            self.facturas_table.setItem(row, 6, QTableWidgetItem(factura['estado']))

    def export_pdf(self):
        """Exportar el informe a PDF"""
        try:
            if not self.informe_data:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Genere el informe antes de exportar a PDF"
                )
                return

            # Obtener el directorio configurado por el usuario
            from database.models import Organizacion
            organizacion = Organizacion.get()
            pdf_dir = organizacion.directorio_informes.strip() if organizacion and organizacion.directorio_informes else ""

            # Si no hay directorio configurado o no existe, usar el directorio por defecto
            if not pdf_dir or not os.path.exists(pdf_dir):
                pdf_dir = os.path.join(os.getcwd(), "informes")
                if organizacion and organizacion.directorio_informes:
                    self.logger.warning(f"Directorio de informes configurado no existe: {organizacion.directorio_informes}. Usando directorio por defecto: {pdf_dir}")

            # Crear el directorio si no existe
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
                self.logger.info(f"Directorio de informes creado: {pdf_dir}")

            # Generar nombre del archivo
            periodo = self.informe_data.get('periodo', {})
            fecha_inicio = periodo.get('fecha_inicio', 'inicio')
            fecha_fin = periodo.get('fecha_fin', 'fin')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Informe_Facturacion_{fecha_inicio}_{fecha_fin}_{timestamp}.pdf"

            # Permitir al usuario elegir la ubicación
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Informe PDF",
                os.path.join(pdf_dir, pdf_filename),
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return  # Usuario canceló

            # Generar el PDF
            success = informe_pdf_generator.generate_facturacion_pdf(
                self.informe_data,
                file_path
            )

            if success:
                # Abrir el PDF automáticamente
                self.abrir_pdf(file_path)
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Informe exportado exitosamente:\n{file_path}"
                )
                self.logger.info(f"Informe de facturación exportado: {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo generar el archivo PDF"
                )

        except Exception as e:
            self.logger.error(f"Error exportando PDF: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar PDF:\n{str(e)}"
            )

    def abrir_pdf(self, pdf_path):
        """Abrir el archivo PDF con el visor predeterminado del sistema"""
        try:
            import subprocess
            import platform

            # Verificar que el archivo existe
            if not os.path.exists(pdf_path):
                self.logger.warning(f"Archivo PDF no encontrado: {pdf_path}")
                return False

            # Detectar el sistema operativo y usar el comando apropiado
            sistema = platform.system().lower()

            if sistema == "windows":
                # Windows: usar start
                os.startfile(pdf_path)
            elif sistema == "darwin":
                # macOS: usar open
                subprocess.run(["open", pdf_path], check=True)
            else:
                # Linux y otros: usar xdg-open
                subprocess.run(["xdg-open", pdf_path], check=True)

            self.logger.info(f"PDF abierto exitosamente: {pdf_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            # No mostrar error al usuario, solo registrar en log
            # El PDF se ha generado correctamente, solo falló la apertura
            return False

    def save_html(self):
        """Guardar el informe en HTML"""
        try:
            if not self.informe_data:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Genere el informe antes de guardar"
                )
                return

            # Crear directorio informes si no existe
            informes_dir = os.path.join(os.getcwd(), "informes")
            if not os.path.exists(informes_dir):
                os.makedirs(informes_dir)

            # Generar nombre del archivo
            periodo = self.informe_data.get('periodo', {})
            fecha_inicio = periodo.get('fecha_inicio', 'inicio')
            fecha_fin = periodo.get('fecha_fin', 'fin')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"Informe_Facturacion_{fecha_inicio}_{fecha_fin}_{timestamp}.html"

            # Permitir al usuario elegir la ubicación
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Informe HTML",
                os.path.join(informes_dir, html_filename),
                "HTML Files (*.html)"
            )

            if not file_path:
                return  # Usuario canceló

            # Obtener el HTML del resumen
            html_content = self.resumen_text.toHtml()

            # Guardar el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            QMessageBox.information(
                self,
                "Éxito",
                f"Informe guardado exitosamente:\n{file_path}"
            )
            self.logger.info(f"Informe HTML guardado: {file_path}")

        except Exception as e:
            self.logger.error(f"Error guardando HTML: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al guardar HTML:\n{str(e)}"
            )

    def print_report(self):
        """Imprimir el informe"""
        try:
            if not self.informe_data:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Genere el informe antes de imprimir"
                )
                return

            from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt5.QtGui import QTextDocument

            # Crear documento de texto
            document = QTextDocument()
            document.setHtml(self.resumen_text.toHtml())

            # Crear impresora
            printer = QPrinter(QPrinter.HighResolution)

            # Mostrar diálogo de impresión
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.Accepted:
                document.print(printer)
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Informe enviado a la impresora"
                )
                self.logger.info("Informe impreso")

        except Exception as e:
            self.logger.error(f"Error imprimiendo: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al imprimir:\n{str(e)}"
            )

    def export_excel(self):
        """Exportar el informe a Excel"""
        try:
            if not self.informe_data:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Genere el informe antes de exportar"
                )
                return

            # Obtener directorio de informes de la configuración
            organizacion = db.get_organization_info()
            directorio_informes = organizacion.get('directorio_informes', 'informes/') if organizacion else 'informes/'

            # Crear directorio si no existe
            if not os.path.exists(directorio_informes):
                os.makedirs(directorio_informes)

            # Generar nombre de archivo
            fecha_inicio = self.fecha_inicio.date().toString("yyyyMMdd")
            fecha_fin = self.fecha_fin.date().toString("yyyyMMdd")
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"informe_facturacion_{fecha_inicio}_{fecha_fin}_{timestamp}.xlsx"
            file_path = os.path.join(directorio_informes, filename)

            # Generar Excel
            excel_generator = ExcelGenerator()
            success = excel_generator.generate_facturacion_excel(self.informe_data, file_path)

            if success:
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Informe Excel guardado exitosamente:\n{file_path}"
                )
                self.logger.info(f"Informe Excel guardado: {file_path}")

                # Abrir el archivo Excel
                self.abrir_excel(file_path)
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Error al generar el archivo Excel.\nVerifique que openpyxl esté instalado."
                )

        except Exception as e:
            self.logger.error(f"Error exportando Excel: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar Excel:\n{str(e)}"
            )

    def abrir_excel(self, file_path):
        """Abrir el archivo Excel generado"""
        try:
            import subprocess
            import platform

            sistema = platform.system()
            if sistema == 'Windows':
                os.startfile(file_path)
            elif sistema == 'Darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])

        except Exception as e:
            self.logger.error(f"Error abriendo Excel: {e}")
            # No mostrar error al usuario, el archivo ya está guardado

