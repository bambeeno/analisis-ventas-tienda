#!/usr/bin/env python3
"""
Script principal de análisis de ventas de la tienda online.
Realiza consultas SQL, análisis con Pandas y genera visualizaciones.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuración de estilo para las visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalizadorVentas:
    def __init__(self):
        """Inicializar el analizador de ventas"""
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tienda_online.db')
        self.conn = None
        self.conectar_bd()
    
    def conectar_bd(self):
        """Conectar a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print("✅ Conexión a la base de datos establecida")
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
    
    def ejecutar_consulta(self, consulta, descripcion=""):
        """Ejecutar una consulta SQL y retornar un DataFrame"""
        try:
            df = pd.read_sql_query(consulta, self.conn)
            if descripcion:
                print(f"📊 {descripcion}: {len(df)} registros obtenidos")
            return df
        except Exception as e:
            print(f"❌ Error en consulta {descripcion}: {e}")
            return pd.DataFrame()
    
    def metricas_generales(self):
        """Calcular métricas generales del negocio"""
        print("\n" + "="*50)
        print("📈 MÉTRICAS GENERALES DEL NEGOCIO")
        print("="*50)
        
        # Ventas totales
        consulta_ventas = "SELECT SUM(total) as ventas_totales FROM pedidos"
        ventas_totales = self.ejecutar_consulta(consulta_ventas).iloc[0]['ventas_totales']
        
        # Número de pedidos
        consulta_pedidos = "SELECT COUNT(*) as num_pedidos FROM pedidos"
        num_pedidos = self.ejecutar_consulta(consulta_pedidos).iloc[0]['num_pedidos']
        
        # Ticket promedio
        ticket_promedio = ventas_totales / num_pedidos
        
        # Número de clientes únicos
        consulta_clientes = "SELECT COUNT(DISTINCT cliente_id) as clientes_unicos FROM pedidos"
        clientes_unicos = self.ejecutar_consulta(consulta_clientes).iloc[0]['clientes_unicos']
        
        # Valor promedio por cliente
        valor_por_cliente = ventas_totales / clientes_unicos
        
        print(f"💰 Ventas totales: €{ventas_totales:,.2f}")
        print(f"🛒 Número de pedidos: {num_pedidos:,}")
        print(f"🎯 Ticket promedio: €{ticket_promedio:.2f}")
        print(f"👥 Clientes únicos: {clientes_unicos}")
        print(f"💎 Valor promedio por cliente: €{valor_por_cliente:.2f}")
        
        return {
            'ventas_totales': ventas_totales,
            'num_pedidos': num_pedidos,
            'ticket_promedio': ticket_promedio,
            'clientes_unicos': clientes_unicos,
            'valor_por_cliente': valor_por_cliente
        }
    
    def top_productos(self, limite=10):
        """Analizar los productos más vendidos"""
        print(f"\n🏆 TOP {limite} PRODUCTOS MÁS VENDIDOS")
        print("="*50)
        
        consulta = f"""
        SELECT 
            p.nombre,
            p.categoria,
            SUM(pd.cantidad) as unidades_vendidas,
            SUM(pd.total) as ingresos_totales,
            AVG(pd.total/pd.cantidad) as precio_promedio
        FROM pedidos pd
        JOIN productos p ON pd.producto_id = p.id
        GROUP BY p.id, p.nombre, p.categoria
        ORDER BY ingresos_totales DESC
        LIMIT {limite}
        """
        
        df_top_productos = self.ejecutar_consulta(consulta, f"Top {limite} productos")
        
        if not df_top_productos.empty:
            for i, row in df_top_productos.iterrows():
                print(f"{i+1:2d}. {row['nombre']}")
                print(f"    📦 Unidades: {row['unidades_vendidas']:,}")
                print(f"    💰 Ingresos: €{row['ingresos_totales']:,.2f}")
                print(f"    🏷️  Categoría: {row['categoria']}")
                print()
        
        return df_top_productos
    
    def analisis_por_categoria(self):
        """Analizar ventas por categoría"""
        print("\n📊 ANÁLISIS POR CATEGORÍA")
        print("="*50)
        
        consulta = """
        SELECT 
            p.categoria,
            COUNT(DISTINCT p.id) as num_productos,
            SUM(pd.cantidad) as unidades_vendidas,
            SUM(pd.total) as ingresos_totales,
            AVG(pd.total) as ticket_promedio_categoria
        FROM pedidos pd
        JOIN productos p ON pd.producto_id = p.id
        GROUP BY p.categoria
        ORDER BY ingresos_totales DESC
        """
        
        df_categorias = self.ejecutar_consulta(consulta, "Análisis por categoría")
        
        if not df_categorias.empty:
            for _, row in df_categorias.iterrows():
                print(f"🏷️  {row['categoria']}")
                print(f"   📦 Productos diferentes: {row['num_productos']}")
                print(f"   🛒 Unidades vendidas: {row['unidades_vendidas']:,}")
                print(f"   💰 Ingresos: €{row['ingresos_totales']:,.2f}")
                print(f"   🎯 Ticket promedio: €{row['ticket_promedio_categoria']:.2f}")
                print()
        
        return df_categorias
    
    def segmentacion_clientes(self):
        """Segmentar clientes por volumen de compra"""
        print("\n👥 SEGMENTACIÓN DE CLIENTES")
        print("="*50)
        
        consulta = """
        SELECT 
            c.nombre,
            c.ciudad,
            COUNT(pd.id) as num_pedidos,
            SUM(pd.total) as gasto_total,
            AVG(pd.total) as ticket_promedio,
            MAX(pd.fecha_pedido) as ultima_compra
        FROM clientes c
        JOIN pedidos pd ON c.id = pd.cliente_id
        GROUP BY c.id, c.nombre, c.ciudad
        ORDER BY gasto_total DESC
        """
        
        df_clientes = self.ejecutar_consulta(consulta, "Segmentación de clientes")
        
        if not df_clientes.empty:
            # Crear segmentos basados en gasto total
            df_clientes['segmento'] = pd.cut(df_clientes['gasto_total'], 
                                           bins=3, 
                                           labels=['Básico', 'Premium', 'VIP'])
            
            print("🥇 TOP 5 CLIENTES VIP:")
            top_clientes = df_clientes.head()
            for i, row in top_clientes.iterrows():
                print(f"{i+1}. {row['nombre']} ({row['ciudad']})")
                print(f"   💰 Gasto total: €{row['gasto_total']:,.2f}")
                print(f"   🛒 Pedidos: {row['num_pedidos']}")
                print(f"   🎯 Ticket promedio: €{row['ticket_promedio']:.2f}")
                print()
            
            # Resumen por segmento
            print("📊 RESUMEN POR SEGMENTO:")
            segmentos = df_clientes.groupby('segmento').agg({
                'gasto_total': ['count', 'mean', 'sum'],
                'num_pedidos': 'mean'
            }).round(2)
            
            for segmento in ['VIP', 'Premium', 'Básico']:
                if segmento in segmentos.index:
                    count = segmentos.loc[segmento, ('gasto_total', 'count')]
                    mean_gasto = segmentos.loc[segmento, ('gasto_total', 'mean')]
                    total_gasto = segmentos.loc[segmento, ('gasto_total', 'sum')]
                    mean_pedidos = segmentos.loc[segmento, ('num_pedidos', 'mean')]
                    
                    print(f"🏷️  {segmento}: {count} clientes")
                    print(f"   💰 Gasto promedio: €{mean_gasto:.2f}")
                    print(f"   📊 Gasto total del segmento: €{total_gasto:.2f}")
                    print(f"   🛒 Pedidos promedio: {mean_pedidos:.1f}")
                    print()
        
        return df_clientes
    
    def tendencias_temporales(self):
        """Analizar tendencias de ventas en el tiempo"""
        print("\n📅 TENDENCIAS TEMPORALES")
        print("="*50)
        
        consulta = """
        SELECT 
            DATE(fecha_pedido) as fecha,
            COUNT(*) as num_pedidos,
            SUM(total) as ventas_diarias
        FROM pedidos
        GROUP BY DATE(fecha_pedido)
        ORDER BY fecha
        """
        
        df_temporal = self.ejecutar_consulta(consulta, "Tendencias temporales")
        
        if not df_temporal.empty:
            df_temporal['fecha'] = pd.to_datetime(df_temporal['fecha'])
            
            # Estadísticas básicas
            ventas_promedio = df_temporal['ventas_diarias'].mean()
            mejor_dia = df_temporal.loc[df_temporal['ventas_diarias'].idxmax()]
            
            print(f"📊 Ventas promedio diarias: €{ventas_promedio:.2f}")
            print(f"🏆 Mejor día de ventas: {mejor_dia['fecha'].strftime('%Y-%m-%d')}")
            print(f"   💰 Ventas: €{mejor_dia['ventas_diarias']:.2f}")
            print(f"   🛒 Pedidos: {mejor_dia['num_pedidos']}")
        
        return df_temporal
    
    def generar_reporte_completo(self):
        """Generar un reporte completo de análisis"""
        print("🚀 INICIANDO ANÁLISIS COMPLETO DE VENTAS")
        print("="*60)
        
        # Ejecutar todos los análisis
        metricas = self.metricas_generales()
        top_productos = self.top_productos()
        categorias = self.analisis_por_categoria()
        clientes = self.segmentacion_clientes()
        temporal = self.tendencias_temporales()
        
        return {
            'metricas': metricas,
            'top_productos': top_productos,
            'categorias': categorias,
            'clientes': clientes,
            'temporal': temporal
        }
    
    def cerrar_conexion(self):
        """Cerrar la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            print("✅ Conexión a la base de datos cerrada")

def main():
    """Función principal"""
    analizador = AnalizadorVentas()
    
    try:
        # Generar reporte completo
        resultados = analizador.generar_reporte_completo()
        
        print("\n" + "="*60)
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("📁 Los datos están listos para visualización")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
    finally:
        analizador.cerrar_conexion()

if __name__ == "__main__":
    main()

