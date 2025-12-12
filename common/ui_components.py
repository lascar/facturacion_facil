# -*- coding: utf-8 -*-
"""
Componentes UI comunes para productos y facturas
MIGRADO A PYQT5: Usa exclusivamente PyQt5 para la interfaz
"""
# Importar las versiones PyQt5
from common.ui_components_abstract import (
    AbstractFormHelper,
    AbstractBaseWindow,
    AbstractImageSelector
)

# Mantener compatibilidad con imports existentes
FormHelper = AbstractFormHelper
BaseWindow = AbstractBaseWindow
ImageSelector = AbstractImageSelector

# Fin del archivo - todo el código legacy ha sido eliminado
