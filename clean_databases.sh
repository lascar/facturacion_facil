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
        sqlite3 facturacion.db "SELECT COUNT(*) as clientes FROM clientes; SELECT COUNT(*) as productos FROM productos; SELECT COUNT(*) as facturas FROM facturas;" 2>/dev/null | while read line; do
            echo "   - $line registros"
        done
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
echo "6) Mostrar estado actual y salir"
echo "7) Cancelar"
echo ""
read -p "Tu elección (1-7): " choice

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
        echo "📋 Estado actual:"
        show_databases
        show_database_content
        ;;
    7)
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
