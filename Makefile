# Makefile para Facturación Fácil

.PHONY: help install install-dev test test-unit test-ui test-utils test-coverage lint format clean run

# Variables
PYTHON = python3
PIP = pip3

help:  ## Mostrar esta ayuda
	@echo "🧪 Facturación Fácil - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependencias de producción
	$(PIP) install -r requirements.txt

install-dev:  ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

test:  ## Ejecutar todos los tests
	$(PYTHON) run_tests.py

test-unit:  ## Ejecutar tests unitarios (base de datos y modelos)
	$(PYTHON) run_tests.py unit

test-ui:  ## Ejecutar tests de interfaz
	$(PYTHON) run_tests.py ui

test-utils:  ## Ejecutar tests de utilidades
	$(PYTHON) run_tests.py utils

test-fast:  ## Ejecutar tests rápidos
	$(PYTHON) run_tests.py fast

test-slow:  ## Ejecutar tests lentos
	$(PYTHON) run_tests.py slow

test-coverage:  ## Ejecutar tests con reporte de cobertura
	$(PYTHON) run_tests.py coverage

lint:  ## Verificar estilo de código
	$(PYTHON) run_tests.py lint

format:  ## Verificar formato de código
	$(PYTHON) run_tests.py format

format-fix:  ## Corregir formato de código automáticamente
	black facturacion_facil/
	black tests/

clean:  ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf *.db

run:  ## Ejecutar la aplicación
	$(PYTHON) main.py

setup:  ## Configuración inicial completa
	$(MAKE) install-dev
	$(MAKE) test
	@echo "✅ Configuración completa. Usa 'make run' para ejecutar la aplicación."

# Comandos de desarrollo
dev-check:  ## Verificación completa antes de commit
	$(MAKE) format-fix
	$(MAKE) lint
	$(MAKE) test-coverage
	@echo "✅ Verificación de desarrollo completa"

# Información del proyecto
info:  ## Mostrar información del proyecto
	@echo "📋 Facturación Fácil - Información del proyecto"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Pip version: $(shell $(PIP) --version)"
	@echo "Directorio actual: $(shell pwd)"
	@echo "Archivos Python: $(shell find . -name "*.py" | wc -l)"
	@echo "Tests: $(shell find tests/ -name "test_*.py" | wc -l)"

# Comandos de base de datos
db-reset:  ## Reiniciar base de datos (eliminar archivo)
	rm -f facturacion.db
	@echo "✅ Base de datos reiniciada"

# Comandos de distribución
dist:  ## Crear distribución
	$(PYTHON) -m pip install pyinstaller
	pyinstaller --onefile --windowed main.py
	@echo "✅ Ejecutable creado en dist/"
