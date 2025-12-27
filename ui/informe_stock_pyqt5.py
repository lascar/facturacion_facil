# -*- coding: utf-8 -*-
"""
Ventana de informe de stock
"""

import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
    QCheckBox, QListWidget, QListWidgetItem, QMessageBox,
    QTextEdit, QSplitter, QAbstractItemView, QFileDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.database import db
from services.informes_service import InformesService
from utils.exceptions import DatabaseError
from utils.logger import get_logger
from utils.informe_pdf_generator import informe_pdf_generator
from utils.informe_charts import informe_chart_generator
from utils.excel_generator import ExcelGenerator


class InformeStockDialog(QDialog):
    """Diálogo para generar informe de stock"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        
        # Service
        db_path = db.db_path if hasattr(db, 'db_path') else None
        self.informes_service = InformesService(db_path)
        
        self.informe_data = None
        self.all_productos = []
        self.setup_ui()
        self.load_productos()
    
    def setup_ui(self):
        """Configurar la interfaz"""
        self.setWindowTitle("Informe de Stock")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("Informe de Stock")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Selección de productos
        selection_group = QGroupBox("Selección de Productos")
        selection_layout = QVBoxLayout()

        # Checkbox para todos
        self.todos_checkbox = QCheckBox("Todos los productos")
        self.todos_checkbox.setChecked(True)
        self.todos_checkbox.stateChanged.connect(self.toggle_todos)
        selection_layout.addWidget(self.todos_checkbox)

        # Lista de productos con checkboxes
        self.productos_list = QListWidget()
        self.productos_list.setEnabled(False)  # Deshabilitado cuando "Todos" está marcado
        selection_layout.addWidget(self.productos_list)

        # Botones de selección
        buttons_sel_layout = QHBoxLayout()
        select_all_btn = QPushButton("Seleccionar Todos")
        select_all_btn.clicked.connect(self.select_all_productos)
        buttons_sel_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deseleccionar Todos")
        deselect_all_btn.clicked.connect(self.deselect_all_productos)
        buttons_sel_layout.addWidget(deselect_all_btn)

        selection_layout.addLayout(buttons_sel_layout)
        
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
        selection_layout.addWidget(generate_btn)
        
        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)
        
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

        # Tabla de stock
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(8)
        self.stock_table.setHorizontalHeaderLabels([
            "Nombre", "Referencia", "Categoría", "Precio", "Stock Actual", "Stock Mínimo", "Valor Stock", "Última Actualización"
        ])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        splitter.addWidget(self.stock_table)

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
    
    def load_productos(self):
        """Cargar la lista de productos con checkboxes"""
        try:
            self.all_productos = db.get_all_products()

            # Cargar todos los productos con checkboxes
            self.productos_list.clear()
            for producto in self.all_productos:
                item = QListWidgetItem(f"{producto['nombre']} ({producto['referencia']})")
                item.setData(Qt.UserRole, producto['id'])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.productos_list.addItem(item)

        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            QMessageBox.critical(self, "Error", f"Error cargando productos: {str(e)}")

    def toggle_todos(self, state):
        """Activar/desactivar la lista de productos"""
        if state == Qt.Checked:
            self.productos_list.setEnabled(False)
            self.productos_list.clearSelection()
        else:
            self.productos_list.setEnabled(True)

    def select_all_productos(self):
        """Seleccionar todos los productos"""
        if not self.todos_checkbox.isChecked():
            self.productos_list.selectAll()

    def deselect_all_productos(self):
        """Deseleccionar todos los productos"""
        self.productos_list.clearSelection()

    def generate_informe(self):
        """Generar el informe"""
        try:
            # Determinar qué productos incluir
            producto_ids = None
            if not self.todos_checkbox.isChecked():
                selected_items = self.productos_list.selectedItems()
                if not selected_items:
                    QMessageBox.warning(
                        self,
                        "Advertencia",
                        "Por favor seleccione al menos un producto"
                    )
                    return
                producto_ids = [item.data(Qt.UserRole) for item in selected_items]

            # Generar informe
            self.informe_data = self.informes_service.get_informe_stock(producto_ids)

            # Mostrar resumen
            self.show_resumen()

            # Mostrar gráficos
            self.show_charts()

            # Mostrar productos
            self.show_productos()

            # Habilitar botones
            self.export_btn.setEnabled(True)
            self.export_excel_btn.setEnabled(True)
            self.save_html_btn.setEnabled(True)
            self.print_btn.setEnabled(True)

        except DatabaseError as e:
            QMessageBox.critical(self, "Error de Base de Datos", str(e))

    def show_resumen(self):
        """Mostrar el resumen del informe"""
        if not self.informe_data:
            return

        resumen = self.informe_data['resumen']
        por_categoria = self.informe_data['por_categoria']

        html = f"""
        <h2>Resumen de Stock</h2>

        <h3>Totales</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr>
                <td><b>Total de Productos:</b></td>
                <td align="right">{resumen['total_productos']}</td>
            </tr>
            <tr>
                <td><b>Productos Sin Stock:</b></td>
                <td align="right">{resumen['productos_sin_stock']}</td>
            </tr>
            <tr style="background-color: #e0e0e0;">
                <td><b>Valor Total del Stock:</b></td>
                <td align="right"><b>{resumen['valor_total_stock']:.2f} €</b></td>
            </tr>
        </table>

        <h3>Por Categoría</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f0f0f0;">
                <th>Categoría</th>
                <th>Productos</th>
                <th>Stock Total</th>
                <th>Valor Total</th>
            </tr>
        """

        for cat in por_categoria:
            html += f"""
            <tr>
                <td>{cat['categoria']}</td>
                <td align="center">{cat['num_productos']}</td>
                <td align="center">{cat['stock_total']}</td>
                <td align="right">{cat['valor_total']:.2f} €</td>
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
            chart_path = informe_chart_generator.create_stock_chart(self.informe_data)

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

    def show_productos(self):
        """Mostrar la tabla de productos"""
        if not self.informe_data:
            return

        productos = self.informe_data['productos']
        self.stock_table.setRowCount(len(productos))

        for row, producto in enumerate(productos):
            self.stock_table.setItem(row, 0, QTableWidgetItem(producto['nombre']))
            self.stock_table.setItem(row, 1, QTableWidgetItem(producto['referencia']))
            self.stock_table.setItem(row, 2, QTableWidgetItem(producto['categoria']))
            self.stock_table.setItem(row, 3, QTableWidgetItem(f"{producto['precio']:.2f} €"))

            # Colorear stock según stock mínimo
            stock_actual = producto['stock_actual']
            stock_minimo = producto['stock_minimo']
            stock_item = QTableWidgetItem(str(stock_actual))

            if stock_actual == 0:
                stock_item.setBackground(Qt.red)
            elif stock_actual <= stock_minimo:
                stock_item.setBackground(Qt.yellow)

            self.stock_table.setItem(row, 4, stock_item)

            # Stock mínimo
            self.stock_table.setItem(row, 5, QTableWidgetItem(str(stock_minimo)))

            self.stock_table.setItem(row, 6, QTableWidgetItem(f"{producto['valor_stock']:.2f} €"))
            self.stock_table.setItem(row, 7, QTableWidgetItem(str(producto['fecha_actualizacion'])))

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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Informe_Stock_{timestamp}.pdf"

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
            success = informe_pdf_generator.generate_stock_pdf(
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
                self.logger.info(f"Informe de stock exportado: {file_path}")
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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"Informe_Stock_{timestamp}.html"

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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"informe_stock_{timestamp}.xlsx"
            file_path = os.path.join(directorio_informes, filename)

            # Generar Excel
            excel_generator = ExcelGenerator()
            success = excel_generator.generate_stock_excel(self.informe_data, file_path)

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

