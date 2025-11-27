#!/usr/bin/env python3
"""
Interface web alternative pour Facturación Fácil
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Ajouter le répertoire au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def index():
    """Page d'accueil"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>💼 Facturación Fácil</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .menu { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
            .menu-item { background: linear-gradient(135deg, #4a90e2, #357abd); color: white; padding: 20px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: bold; transition: transform 0.2s; }
            .menu-item:hover { transform: translateY(-2px); }
            .productos { background: linear-gradient(135deg, #e74c3c, #c0392b) !important; }
            .organizacion { background: linear-gradient(135deg, #f39c12, #d68910) !important; }
            .stock { background: linear-gradient(135deg, #27ae60, #229954) !important; }
            .facturas { background: linear-gradient(135deg, #8e44ad, #7d3c98) !important; }
            .clientes { background: linear-gradient(135deg, #3498db, #2980b9) !important; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💼 Facturación Fácil</h1>
            <p style="text-align: center; color: #666;">Sistema de facturación - Interfaz Web</p>
            
            <div class="menu">
                <a href="/productos" class="menu-item productos">📦 Productos</a>
                <a href="/organizacion" class="menu-item organizacion">🏢 Organización</a>
                <a href="/stock" class="menu-item stock">📊 Stock</a>
                <a href="/facturas" class="menu-item facturas">🧾 Facturas</a>
                <a href="/clientes" class="menu-item clientes">👥 Clientes</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/productos')
def productos():
    """Gestión de productos"""
    try:
        from database.database import db
        productos = db.get_all_productos()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>📦 Productos - Facturación Fácil</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
                th { background: #4a90e2; color: white; }
                .btn { background: #4a90e2; color: white; padding: 8px 16px; border: none; border-radius: 4px; text-decoration: none; }
                .btn:hover { background: #357abd; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📦 Productos</h1>
                <a href="/" class="btn">← Volver al menú</a>
                
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Precio</th>
                        <th>Stock</th>
                        <th>Descripción</th>
                    </tr>
        """
        
        for producto in productos:
            html += f"""
                    <tr>
                        <td>{producto.get('id', '')}</td>
                        <td>{producto.get('nombre', '')}</td>
                        <td>${producto.get('precio', 0):.2f}</td>
                        <td>{producto.get('stock', 0)}</td>
                        <td>{producto.get('descripcion', '')}</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return f"<h1>❌ Error</h1><p>{e}</p><a href='/'>Volver</a>"

@app.route('/test')
def test():
    """Test de la base de données"""
    try:
        from database.database import db
        db.init_database()
        return "<h1>✅ Base de données OK</h1><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h1>❌ Error</h1><p>{e}</p>"

if __name__ == '__main__':
    print("🌐 Lancement de l'interface web...")
    print("📱 Ouvrez votre navigateur sur: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
