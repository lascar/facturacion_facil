#!/bin/bash
# Script para limpiar todas las bases de datos y datos
# ATENCIÓN: Esta operación es IRREVERSIBLE

echo "🗑️  Script de limpieza completa de datos"
echo "⚠️  ATENCIÓN: Esta operación eliminará TODAS las bases de datos y datos"
echo ""

# Función para mostrar las bases de datos encontradas
show_databases() {
    echo "📋 Bases de datos encontradas:"
    find . -name "*.db" -type f | while read db; do
        size=$(du -h "$db" | cut -f1)
        echo "   - $db ($size)"
    done
    echo ""
}

# Función para mostrar el contenido de la base principal
show_database_content() {
    if [ -f "facturacion.db" ]; then
        echo "📊 Contenido de facturacion.db:"

        # Verificar si la base de datos tiene tablas
        tables=$(sqlite3 facturacion.db ".tables" 2>/dev/null)
        if [ -z "$tables" ]; then
            echo "   - Base de datos vacía (sin tablas)"
        else
            # Contar registros en cada tabla principal
            clientes=$(sqlite3 facturacion.db "SELECT COUNT(*) FROM clientes;" 2>/dev/null || echo "0")
            productos=$(sqlite3 facturacion.db "SELECT COUNT(*) FROM productos;" 2>/dev/null || echo "0")
            facturas=$(sqlite3 facturacion.db "SELECT COUNT(*) FROM facturas;" 2>/dev/null || echo "0")

            echo "   - Clientes: $clientes registros"
            echo "   - Productos: $productos registros"
            echo "   - Facturas: $facturas registros"
        fi
        echo ""
    else
        echo "📊 No existe facturacion.db"
        echo ""
    fi
}

# Función para eliminar todas las bases de datos
delete_all_databases() {
    echo "🗑️  Eliminando todas las bases de datos..."
    find . -name "*.db" -type f -delete
    echo "✅ Todas las bases de datos han sido eliminadas"
}

# Función para limpiar completamente la base principal
clean_main_database() {
    if [ -f "facturacion.db" ]; then
        echo "🧹 Limpiando contenido de facturacion.db..."
        sqlite3 facturacion.db "
        DELETE FROM factura_items;
        DELETE FROM facturas;
        DELETE FROM stock_movements;
        DELETE FROM stock;
        DELETE FROM productos;
        DELETE FROM clientes;
        DELETE FROM organizacion;
        " 2>/dev/null

        # VACUUM en una operación separada
        echo "🗜️  Optimizando base de datos..."
        sqlite3 facturacion.db "VACUUM;" 2>/dev/null
        echo "✅ Base de datos principal limpiada y optimizada"
    fi
}

# Función para limpiar solo datos de test (NUEVA)
clean_test_data_only() {
    if [ -f "facturacion.db" ]; then
        echo "🧪 Limpiando solo datos de test..."
        sqlite3 facturacion.db "
        DELETE FROM factura_items WHERE factura_id IN (
            SELECT id FROM facturas WHERE numero_factura LIKE 'TEST-%' OR numero_factura LIKE 'DEMO-%'
        );
        DELETE FROM facturas WHERE numero_factura LIKE 'TEST-%' OR numero_factura LIKE 'DEMO-%';
        DELETE FROM productos WHERE referencia LIKE 'TEST-%' OR referencia LIKE 'DEMO-%';
        DELETE FROM clientes WHERE nombre LIKE '%Test%' OR nombre LIKE '%Demo%';
        " 2>/dev/null

        echo "🗜️  Optimizando base de datos..."
        sqlite3 facturacion.db "VACUUM;" 2>/dev/null
        echo "✅ Datos de test eliminados (datos reales preservados)"
    fi
}

# Función para hacer backup antes de limpiar (NUEVA)
backup_before_clean() {
    if [ -f "facturacion.db" ]; then
        timestamp=$(date +"%Y%m%d_%H%M%S")
        backup_file="facturacion_backup_${timestamp}.db"

        echo "💾 Creando backup antes de limpiar..."
        cp "facturacion.db" "$backup_file"

        if [ $? -eq 0 ]; then
            echo "✅ Backup creado: $backup_file"
            return 0
        else
            echo "❌ Error creando backup"
            return 1
        fi
    else
        echo "⚠️  No hay base de datos para hacer backup"
        return 1
    fi
}

# Función para limpiar preservando integridad referencial (NUEVA)
clean_with_integrity() {
    if [ -f "facturacion.db" ]; then
        echo "🔗 Limpiando con preservación de integridad referencial..."

        # Primero eliminar items de factura (referencias)
        sqlite3 facturacion.db "DELETE FROM factura_items;" 2>/dev/null

        # Luego facturas
        sqlite3 facturacion.db "DELETE FROM facturas;" 2>/dev/null

        # Movimientos de stock
        sqlite3 facturacion.db "DELETE FROM stock_movements;" 2>/dev/null

        # Stock (pero mantener estructura para productos existentes)
        sqlite3 facturacion.db "UPDATE stock SET cantidad_disponible = 0;" 2>/dev/null

        # NO eliminar productos ni clientes (preservar datos maestros)
        echo "   ℹ️  Productos y clientes preservados"

        # VACUUM
        echo "🗜️  Optimizando base de datos..."
        sqlite3 facturacion.db "VACUUM;" 2>/dev/null
        echo "✅ Base limpiada preservando datos maestros"
    fi
}

# Función para eliminar todos los datos y archivos relacionados
delete_all_data() {
    echo "🗑️  Eliminando TODOS los datos..."

    # Bases de datos
    find . -name "*.db" -type f -delete

    # Logs
    find . -name "*.log" -type f -delete

    # Cache y archivos temporales
    find . -name "*.cache" -type f -delete
    find . -name "*.tmp" -type f -delete

    # PDFs generados
    rm -rf facturas_pdf/*.pdf 2>/dev/null
    rm -rf pdfs/*.pdf 2>/dev/null

    # Archivos de cobertura
    rm -rf htmlcov/* 2>/dev/null
    rm -f .coverage 2>/dev/null

    # Logs de test
    find ./test -name "logs" -type d -exec rm -rf {} + 2>/dev/null

    echo "✅ Todos los datos han sido eliminados"
}

# Función para eliminar solo las bases de datos de test
delete_test_databases() {
    echo "🧪 Eliminando solo las bases de datos de test..."
    find ./test -name "*.db" -type f -delete
    echo "✅ Bases de datos de test eliminadas"
}

# Función para eliminar solo las bases de datos de backup
delete_backup_databases() {
    echo "💾 Eliminando solo las bases de datos de backup..."
    find . -name "*backup*.db" -type f -delete
    find . -name "*old*.db" -type f -delete
    echo "✅ Bases de datos de backup eliminadas"
}

# Función para crear una base de datos limpia
create_clean_database() {
    echo "🆕 Creando base de datos limpia..."

    # Eliminar la base actual si existe
    rm -f facturacion.db

    # Activar el entorno virtual y crear una nueva base
    if [ -f "activate.sh" ]; then
        source activate.sh
        python -c "
from database.database import db
print('Inicializando base de datos limpia...')
db.init_database()
print('✅ Base de datos limpia creada')
"
    else
        echo "❌ No se encontró activate.sh - no se puede crear la base"
    fi
}

# Mostrar estado actual
show_databases
show_database_content

# Menú de opciones
echo "Selecciona una opción:"
echo "1) Eliminar TODAS las bases de datos (⚠️  PELIGROSO)"
echo "2) Limpiar solo el CONTENIDO de la base principal (mantener estructura)"
echo "3) Eliminar TODOS los datos (bases, logs, PDFs, cache) (⚠️  MUY PELIGROSO)"
echo "4) Eliminar solo las bases de datos de TEST"
echo "5) Eliminar solo las bases de datos de BACKUP"
echo "6) Crear base de datos LIMPIA (recomendado)"
echo "7) Limpiar solo datos de TEST (preservar datos reales) (🆕 SEGURO)"
echo "8) Limpiar con backup automático (🆕 SEGURO)"
echo "9) Limpiar preservando datos maestros (🆕 SEGURO)"
echo "10) Mostrar estado actual y salir"
echo "11) Cancelar"
echo ""
read -p "Tu elección (1-11): " choice

case $choice in
    1)
        read -p "⚠️  ¿Estás SEGURO de que quieres eliminar TODAS las bases de datos? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            delete_all_databases
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    2)
        read -p "🧹 ¿Quieres limpiar el contenido de la base principal? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            clean_main_database
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    3)
        read -p "⚠️  ¿Estás SEGURO de que quieres eliminar TODOS los datos? (escribe 'ELIMINAR_TODO' para confirmar): " confirm
        if [ "$confirm" = "ELIMINAR_TODO" ]; then
            delete_all_data
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    4)
        delete_test_databases
        ;;
    5)
        delete_backup_databases
        ;;
    6)
        read -p "🆕 ¿Quieres crear una base de datos limpia? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            create_clean_database
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    7)
        read -p "🧪 ¿Quieres limpiar solo los datos de test? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            clean_test_data_only
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    8)
        read -p "💾 ¿Quieres limpiar con backup automático? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            if backup_before_clean; then
                clean_main_database
            else
                echo "❌ Limpieza cancelada por error en backup"
            fi
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    9)
        read -p "🔗 ¿Quieres limpiar preservando datos maestros? (escribe 'SI' para confirmar): " confirm
        if [ "$confirm" = "SI" ]; then
            clean_with_integrity
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    10)
        echo "📋 Estado actual:"
        show_databases
        show_database_content
        ;;
    11)
        echo "❌ Operación cancelada"
        ;;
    *)
        echo "❌ Opción inválida"
        ;;
esac

echo ""
echo "📋 Estado final:"
show_databases
show_database_content
