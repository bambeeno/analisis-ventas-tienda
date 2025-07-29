#!/usr/bin/env python3
"""
Script para crear la base de datos de la tienda online con datos de ejemplo.
Este script crea las tablas necesarias y las llena con datos realistas para análisis.
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os

def crear_conexion():
    """Crear conexión a la base de datos SQLite"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tienda_online.db')
    conn = sqlite3.connect(db_path)
    return conn

def crear_tablas(conn):
    """Crear las tablas de la base de datos"""
    cursor = conn.cursor()
    
    # Tabla productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')
    
    # Tabla clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        fecha_registro DATE NOT NULL,
        ciudad TEXT NOT NULL
    )
    ''')
    
    # Tabla pedidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha_pedido DATE NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
    ''')
    
    conn.commit()
    print("✅ Tablas creadas exitosamente")

def insertar_productos(conn):
    """Insertar productos de ejemplo"""
    cursor = conn.cursor()
    
    productos = [
        ('Laptop Dell Inspiron', 'Electrónicos', 899.99, 25),
        ('iPhone 14', 'Electrónicos', 999.99, 15),
        ('Auriculares Sony', 'Electrónicos', 199.99, 50),
        ('Camiseta Nike', 'Ropa', 29.99, 100),
        ('Jeans Levis', 'Ropa', 79.99, 75),
        ('Zapatillas Adidas', 'Ropa', 129.99, 60),
        ('Libro Python Programming', 'Libros', 39.99, 30),
        ('Libro Data Science', 'Libros', 49.99, 25),
        ('Cafetera Nespresso', 'Hogar', 159.99, 20),
        ('Aspiradora Dyson', 'Hogar', 299.99, 10),
        ('Tablet Samsung', 'Electrónicos', 349.99, 35),
        ('Smartwatch Apple', 'Electrónicos', 399.99, 40),
        ('Chaqueta North Face', 'Ropa', 149.99, 45),
        ('Libro SQL Fundamentals', 'Libros', 34.99, 40),
        ('Microondas LG', 'Hogar', 129.99, 15)
    ]
    
    cursor.executemany('''
    INSERT INTO productos (nombre, categoria, precio, stock)
    VALUES (?, ?, ?, ?)
    ''', productos)
    
    conn.commit()
    print(f"✅ {len(productos)} productos insertados")

def insertar_clientes(conn):
    """Insertar clientes de ejemplo"""
    cursor = conn.cursor()
    
    nombres = ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Pérez', 'Laura Martín',
               'Pedro Sánchez', 'Carmen Ruiz', 'Miguel Torres', 'Isabel Flores', 'David Moreno',
               'Elena Jiménez', 'Francisco Herrera', 'Lucía Romero', 'Antonio Navarro', 'Cristina Vega']
    
    ciudades = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Málaga', 'Zaragoza']
    
    clientes = []
    for i, nombre in enumerate(nombres):
        email = f"{nombre.lower().replace(' ', '.')}@email.com"
        fecha_registro = datetime.now() - timedelta(days=random.randint(30, 365))
        ciudad = random.choice(ciudades)
        clientes.append((nombre, email, fecha_registro.date(), ciudad))
    
    cursor.executemany('''
    INSERT INTO clientes (nombre, email, fecha_registro, ciudad)
    VALUES (?, ?, ?, ?)
    ''', clientes)
    
    conn.commit()
    print(f"✅ {len(clientes)} clientes insertados")

def insertar_pedidos(conn):
    """Insertar pedidos de ejemplo"""
    cursor = conn.cursor()
    
    # Obtener IDs de clientes y productos
    cursor.execute('SELECT id FROM clientes')
    cliente_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT id, precio FROM productos')
    productos_info = cursor.fetchall()
    
    pedidos = []
    for _ in range(200):  # Crear 200 pedidos
        cliente_id = random.choice(cliente_ids)
        producto_id, precio = random.choice(productos_info)
        cantidad = random.randint(1, 5)
        fecha_pedido = datetime.now() - timedelta(days=random.randint(1, 180))
        total = precio * cantidad
        
        pedidos.append((cliente_id, producto_id, cantidad, fecha_pedido.date(), total))
    
    cursor.executemany('''
    INSERT INTO pedidos (cliente_id, producto_id, cantidad, fecha_pedido, total)
    VALUES (?, ?, ?, ?, ?)
    ''', pedidos)
    
    conn.commit()
    print(f"✅ {len(pedidos)} pedidos insertados")

def mostrar_estadisticas(conn):
    """Mostrar estadísticas básicas de la base de datos"""
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM productos')
    num_productos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM clientes')
    num_clientes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM pedidos')
    num_pedidos = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(total) FROM pedidos')
    ventas_totales = cursor.fetchone()[0]
    
    print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
    print(f"   • Productos: {num_productos}")
    print(f"   • Clientes: {num_clientes}")
    print(f"   • Pedidos: {num_pedidos}")
    print(f"   • Ventas totales: €{ventas_totales:,.2f}")

def main():
    """Función principal"""
    print("🚀 Creando base de datos de la tienda online...")
    
    # Crear conexión
    conn = crear_conexion()
    
    try:
        # Crear tablas
        crear_tablas(conn)
        
        # Insertar datos
        insertar_productos(conn)
        insertar_clientes(conn)
        insertar_pedidos(conn)
        
        # Mostrar estadísticas
        mostrar_estadisticas(conn)
        
        print("\n✅ Base de datos creada exitosamente!")
        print("📁 Ubicación: data/tienda_online.db")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()

