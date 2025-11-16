# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des factures - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDateEdit, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor

from ui.base_pyqt6_window import BasePyQt6Window
from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
from database.database import db
from utils.logger import get_logger
from utils.pdf_generator import pdf_generator
import os

class FacturasPyQt6Window(BasePyQt6Window):
    """Fenêtre de gestion des factures en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Facturas", 1200, 800)
        self.logger = get_logger("facturas_pyqt6")
        
        self.logger.info("Inicializando ventana de gestión de facturas PyQt6")
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title_label = QLabel("Gestión de Facturas")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Filtres
        self.create_filters_panel()
        
        # Table des factures
        self.create_invoices_table()
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_invoices_data()
    
    def create_filters_panel(self):
        """Crée le panneau de filtres"""
        filters_group = QGroupBox("Filtros")
        filters_layout = QGridLayout(filters_group)
        
        # Recherche
        filters_layout.addWidget(QLabel("Buscar:"), 0, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Número de factura o cliente...")
        self.search_edit.textChanged.connect(self.filter_invoices)
        filters_layout.addWidget(self.search_edit, 0, 1)
        
        # Date de début
        filters_layout.addWidget(QLabel("Desde:"), 0, 2)
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        filters_layout.addWidget(self.date_from, 0, 3)
        
        # Date de fin
        filters_layout.addWidget(QLabel("Hasta:"), 0, 4)
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filters_layout.addWidget(self.date_to, 0, 5)
        
        # État
        filters_layout.addWidget(QLabel("Estado:"), 1, 0)
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Todos", "Pendiente", "Pagada", "Vencida"])
        filters_layout.addWidget(self.status_filter, 1, 1)
        
        self.main_layout.addWidget(filters_group)
    
    def create_invoices_table(self):
        """Crée la table des factures"""
        table_group = QGroupBox("Lista de Facturas")
        table_layout = QVBoxLayout(table_group)
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(6)
        self.invoices_table.setHorizontalHeaderLabels([
            "Número", "Fecha", "Cliente", "Total", "Estado", "Vencimiento"
        ])
        
        # Configuration de la table
        header = self.invoices_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.invoices_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.invoices_table.setAlternatingRowColors(True)

        # Permettre la sélection multiple (Ctrl pour sélection discrète, Shift pour plage)
        self.invoices_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

        # Connecter le signal de changement de sélection
        self.invoices_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        table_layout.addWidget(self.invoices_table)

        # Label d'information sur la sélection
        self.selection_info_label = QLabel("Selecciona facturas con Ctrl+clic (discreto) o Shift+clic (rango)")
        self.selection_info_label.setStyleSheet("color: #6c757d; font-size: 10pt; padding: 5px;")
        table_layout.addWidget(self.selection_info_label)

        self.main_layout.addWidget(table_group)
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("Nueva Factura", self.new_invoice, "success"),
            ("Ver/Editar", self.edit_invoice, "primary"),
            ("Imprimir", self.print_invoice, "secondary"),
            ("Eliminar", self.delete_invoices, "danger"),  # Renommé pour gérer multiple
            ("Cerrar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def load_invoices_data(self):
        """Charge les données des factures"""
        try:
            # Charger les factures depuis la base de données
            db_invoices = db.get_all_invoices()

            if db_invoices:
                self.invoices_table.setRowCount(len(db_invoices))

                for row, invoice in enumerate(db_invoices):
                    self.invoices_table.setItem(row, 0, QTableWidgetItem(invoice["numero"]))
                    self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice["fecha"]))
                    self.invoices_table.setItem(row, 2, QTableWidgetItem(invoice["cliente_nombre"]))

                    total_item = QTableWidgetItem(f"{invoice['total']:.2f} €")
                    total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                    self.invoices_table.setItem(row, 3, total_item)

                    status_item = QTableWidgetItem(invoice["estado"])
                    if invoice["estado"] == "Pagada":
                        status_item.setForeground(QColor("#28a745"))
                    elif invoice["estado"] == "Vencida":
                        status_item.setForeground(QColor("#dc3545"))
                    else:
                        status_item.setForeground(QColor("#ffc107"))
                    self.invoices_table.setItem(row, 4, status_item)

                    self.invoices_table.setItem(row, 5, QTableWidgetItem(invoice["vencimiento"]))

                self.logger.info(f"Cargadas {len(db_invoices)} facturas de la base de datos")
            else:
                # Si no hay facturas, limpiar la tabla
                self.invoices_table.setRowCount(0)
                self.logger.info("No hay facturas en la base de datos")

        except Exception as e:
            self.logger.error(f"Error cargando facturas: {e}")
            # Fallback con datos de demo
            demo_invoices = [
                {"numero": "F-DEMO-001", "fecha": "2024-01-15", "cliente_nombre": "Cliente Demo", "total": 125.50, "estado": "Demo", "vencimiento": "2024-02-15"},
            ]

            self.invoices_table.setRowCount(len(demo_invoices))
            for row, invoice in enumerate(demo_invoices):
                self.invoices_table.setItem(row, 0, QTableWidgetItem(invoice["numero"]))
                self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice["fecha"]))
                self.invoices_table.setItem(row, 2, QTableWidgetItem(invoice["cliente_nombre"]))

                total_item = QTableWidgetItem(f"{invoice['total']:.2f} €")
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.invoices_table.setItem(row, 3, total_item)

                status_item = QTableWidgetItem(invoice["estado"])
                status_item.setForeground(QColor("#6c757d"))
                self.invoices_table.setItem(row, 4, status_item)

                self.invoices_table.setItem(row, 5, QTableWidgetItem(invoice["vencimiento"]))

            self.show_warning("Error de Base de Datos", f"Error cargando facturas: {e}\nMostrando datos de demostración.")
    
    def filter_invoices(self):
        """Filtre les factures"""
        search_text = self.search_edit.text().lower()
        
        for row in range(self.invoices_table.rowCount()):
            show_row = True
            
            if search_text:
                numero_item = self.invoices_table.item(row, 0)
                cliente_item = self.invoices_table.item(row, 2)
                
                if not ((numero_item and search_text in numero_item.text().lower()) or
                        (cliente_item and search_text in cliente_item.text().lower())):
                    show_row = False
            
            self.invoices_table.setRowHidden(row, not show_row)
    
    def new_invoice(self):
        """Crée une nouvelle facture"""
        try:
            # Ouvrir l'éditeur de factures en mode création
            editor = FacturaEditorPyQt6Window(self)
            editor.factura_saved.connect(self.on_invoice_saved)
            editor.show()

            self.logger.info("Editor de nueva factura abierto")

        except Exception as e:
            self.logger.error(f"Error abriendo editor de factura: {e}")
            self.show_error("Error", f"Error al abrir editor de factura: {e}")
    
    def edit_invoice(self):
        """Édite la facture sélectionnée"""
        current_row = self.invoices_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Selecciona una factura para editar")
            return

        try:
            numero_item = self.invoices_table.item(current_row, 0)
            if numero_item:
                numero_factura = numero_item.text()

                # Récupérer les données complètes de la facture depuis la base de données
                factura_data = db.get_invoice_by_number(numero_factura)

                if factura_data:
                    # Ouvrir l'éditeur en mode édition avec les données complètes
                    editor = FacturaEditorPyQt6Window(self, factura_data)
                    editor.factura_saved.connect(self.on_invoice_saved)
                    editor.show()

                    self.logger.info(f"Editor abierto para factura: {numero_factura}")
                else:
                    self.show_error("Error", f"No se pudieron cargar los datos de la factura {numero_factura}")
                    self.logger.error(f"No se encontraron datos para la factura: {numero_factura}")

                self.logger.info(f"Editor de factura abierto para edición: {numero_item.text()}")

        except Exception as e:
            self.logger.error(f"Error abriendo editor para edición: {e}")
            self.show_error("Error", f"Error al abrir editor: {e}")
    
    def print_invoice(self):
        """Imprime la facture sélectionnée en PDF"""
        current_row = self.invoices_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Selecciona una factura para imprimir")
            return

        try:
            numero_item = self.invoices_table.item(current_row, 0)
            if numero_item:
                # Récupérer les données de la facture
                invoice_data = self.get_invoice_data_from_row(current_row)

                # Créer le dossier de sortie s'il n'existe pas
                output_dir = "facturas_pdf"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Nom du fichier PDF
                invoice_number = invoice_data['numero'].replace('/', '_').replace('-', '_')
                pdf_filename = f"Factura_{invoice_number}.pdf"
                pdf_path = os.path.join(output_dir, pdf_filename)

                # Générer le PDF
                self.logger.info(f"Generando PDF de factura existente: {pdf_path}")
                success = pdf_generator.generate_invoice_pdf(invoice_data, pdf_path)

                if success:
                    # Demander si ouvrir le PDF
                    if self.ask_question("PDF Generado",
                                       f"PDF generado exitosamente:\n{pdf_path}\n\n¿Desea abrir el archivo?"):
                        self.open_pdf_file(pdf_path)
                    else:
                        self.show_info("PDF Generado", f"PDF guardado en:\n{pdf_path}")
                else:
                    self.show_error("Error", "Error al generar el PDF")

        except Exception as e:
            self.logger.error(f"Error imprimiendo factura: {e}")
            self.show_error("Error", f"Error al imprimir factura:\n{str(e)}")

    def get_invoice_data_from_row(self, row):
        """Récupère les données d'une facture depuis une ligne de la table"""
        # Récupérer les données de base de la table
        numero = self.invoices_table.item(row, 0).text()
        fecha = self.invoices_table.item(row, 1).text()
        cliente_nombre = self.invoices_table.item(row, 2).text()
        total_text = self.invoices_table.item(row, 3).text()
        estado = self.invoices_table.item(row, 4).text()
        vencimiento = self.invoices_table.item(row, 5).text()

        # Extraire le montant total
        total = float(total_text.replace(' €', '').replace(',', '.'))

        # Créer des données de facture simulées (dans une vraie app, on récupérerait de la DB)
        invoice_data = {
            'numero': numero,
            'fecha': fecha,
            'vencimiento': vencimiento,
            'estado': estado,
            'cliente': {
                'nombre': cliente_nombre,
                'nif': 'N/A',
                'direccion': 'Dirección no disponible'
            },
            'lineas': [
                {
                    'producto_referencia': 'PROD-001',
                    'producto_nombre': 'Producto de ejemplo',
                    'descripcion': 'Descripción del producto',
                    'cantidad': 1,
                    'precio_unitario': total * 0.826,  # Approximation sans IVA
                    'descuento_pct': 0.0,
                    'iva_pct': 21.0,
                    'subtotal': total * 0.826,
                    'iva_amount': total * 0.174,
                    'total': total
                }
            ],
            'subtotal': total * 0.826,
            'iva_total': total * 0.174,
            'total': total
        }

        return invoice_data

    def open_pdf_file(self, pdf_path):
        """Ouvre le fichier PDF avec l'application par défaut"""
        try:
            import subprocess
            import platform

            system = platform.system()
            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])

            self.logger.info(f"PDF abierto: {pdf_path}")

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            self.show_warning("Advertencia", f"PDF generado pero no se pudo abrir automáticamente:\n{pdf_path}")
    
    def delete_invoices(self):
        """Supprime les factures sélectionnées (simple ou multiple)"""
        selected_rows = self.get_selected_rows()

        if not selected_rows:
            self.show_warning("Selección", "Selecciona una o más facturas para eliminar")
            return

        try:
            # Préparer les informations des factures à supprimer
            invoices_to_delete = []
            invoice_numbers = []

            for row in selected_rows:
                numero_item = self.invoices_table.item(row, 0)
                if numero_item:
                    numero = numero_item.text()
                    invoice_numbers.append(numero)

                    # Obtenir l'ID de la facture depuis la base de données
                    invoice_id = db.get_invoice_id_by_number(numero)
                    if invoice_id:
                        invoices_to_delete.append(invoice_id)

            if not invoices_to_delete:
                self.show_error("Error", "No se pudieron obtener los IDs de las facturas")
                return

            # Demander confirmation
            count = len(invoices_to_delete)
            if count == 1:
                message = f"¿Eliminar la factura {invoice_numbers[0]}?"
                title = "Confirmar Eliminación"
            else:
                numbers_text = ", ".join(invoice_numbers[:3])
                if count > 3:
                    numbers_text += f" y {count - 3} más"
                message = f"¿Eliminar {count} facturas?\n\nFacturas: {numbers_text}"
                title = "Confirmar Eliminación Múltiple"

            if not self.ask_question(title, message):
                return

            # Eliminar de la base de datos
            if count == 1:
                success = db.delete_invoice(invoices_to_delete[0])
                if success:
                    deleted_count = 1
                else:
                    deleted_count = 0
            else:
                deleted_count = db.delete_multiple_invoices(invoices_to_delete)

            if deleted_count > 0:
                # Recargar la lista de facturas
                self.load_invoices_data()

                # Mostrar mensaje de éxito
                if deleted_count == 1:
                    self.show_info("Éxito", "Factura eliminada correctamente")
                else:
                    self.show_info("Éxito", f"{deleted_count} facturas eliminadas correctamente")

                self.logger.info(f"{deleted_count} facturas eliminadas")
            else:
                self.show_error("Error", "No se pudieron eliminar las facturas")

        except Exception as e:
            self.logger.error(f"Error eliminando facturas: {e}")
            self.show_error("Error", f"Error al eliminar facturas:\n{str(e)}")

    def get_selected_rows(self):
        """Obtiene las filas seleccionadas"""
        selected_items = self.invoices_table.selectedItems()
        if not selected_items:
            return []

        # Obtener las filas únicas (éviter les doublons car plusieurs colonnes par ligne)
        selected_rows = list(set(item.row() for item in selected_items))
        selected_rows.sort()  # Trier pour un ordre cohérent

        return selected_rows

    def on_selection_changed(self):
        """Gère le changement de sélection"""
        try:
            selected_rows = self.get_selected_rows()
            count = len(selected_rows)

            if count == 0:
                self.selection_info_label.setText("Selecciona facturas con Ctrl+clic (discreto) o Shift+clic (rango)")
            elif count == 1:
                numero_item = self.invoices_table.item(selected_rows[0], 0)
                numero = numero_item.text() if numero_item else "N/A"
                self.selection_info_label.setText(f"1 factura seleccionada: {numero}")
            else:
                # Calculer le total des factures sélectionnées
                total_selected = 0.0
                for row in selected_rows:
                    total_item = self.invoices_table.item(row, 3)  # Colonne total
                    if total_item:
                        total_text = total_item.text().replace(' €', '').replace(',', '.')
                        try:
                            total_selected += float(total_text)
                        except ValueError:
                            pass

                self.selection_info_label.setText(
                    f"{count} facturas seleccionadas - Total: {total_selected:.2f} €"
                )

        except Exception as e:
            self.logger.error(f"Error actualizando información de selección: {e}")

    def on_invoice_saved(self):
        """Callback appelé quand une facture est sauvegardée"""
        try:
            # Recharger la liste des factures
            self.load_invoices_data()
            self.logger.info("Lista de facturas actualizada después de guardar")

        except Exception as e:
            self.logger.error(f"Error actualizando lista de facturas: {e}")
