#!/usr/bin/env python3
"""
Script para generar visualizaciones del análisis de ventas.
Crea gráficos usando matplotlib y seaborn para presentar los resultados.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuración de matplotlib para español
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)
plt.style.use('seaborn-v0_8')

class GeneradorVisualizaciones:
    def __init__(self):
        """Inicializar el generador de visualizaciones"""
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tienda_online.db')
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizaciones')
        self.conn = sqlite3.connect(self.db_path)
        
        # Crear directorio de salida si no existe
        os.makedirs(self.output_dir, exist_ok=True)
    
    def ejecutar_consulta(self, consulta):
        """Ejecutar consulta SQL y retornar DataFrame"""
        return pd.read_sql_query(consulta, self.conn)
    
    def grafico_top_productos(self, limite=10):
        """Crear gráfico de barras de los productos más vendidos"""
        consulta = f"""
        SELECT 
            p.nombre,
            SUM(pd.total) as ingresos_totales
        FROM pedidos pd
        JOIN productos p ON pd.producto_id = p.id
        GROUP BY p.id, p.nombre
        ORDER BY ingresos_totales DESC
        LIMIT {limite}
        """
        
        df = self.ejecutar_consulta(consulta)
        
        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(df)), df['ingresos_totales'], color='skyblue', edgecolor='navy', alpha=0.7)
        
        # Personalizar el gráfico
        plt.title(f'Top {limite} Productos por Ingresos', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Productos', fontsize=12)
        plt.ylabel('Ingresos (€)', fontsize=12)
        
        # Rotar etiquetas del eje x
        plt.xticks(range(len(df)), df['nombre'], rotation=45, ha='right')
        
        # Añadir valores en las barras
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'€{height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, 'top_productos.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico guardado: {output_path}")
        return output_path
    
    def grafico_ventas_por_categoria(self):
        """Crear gráfico circular de ventas por categoría"""
        consulta = """
        SELECT 
            p.categoria,
            SUM(pd.total) as ingresos_totales
        FROM pedidos pd
        JOIN productos p ON pd.producto_id = p.id
        GROUP BY p.categoria
        ORDER BY ingresos_totales DESC
        """
        
        df = self.ejecutar_consulta(consulta)
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(df)))
        
        wedges, texts, autotexts = plt.pie(df['ingresos_totales'], 
                                          labels=df['categoria'],
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          explode=[0.05] * len(df),
                                          shadow=True,
                                          startangle=90)
        
        # Personalizar el gráfico
        plt.title('Distribución de Ventas por Categoría', fontsize=16, fontweight='bold', pad=20)
        
        # Mejorar la legibilidad
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Añadir leyenda con valores
        legend_labels = [f'{cat}: €{val:,.0f}' for cat, val in zip(df['categoria'], df['ingresos_totales'])]
        plt.legend(wedges, legend_labels, title="Categorías", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.axis('equal')
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, 'ventas_por_categoria.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico guardado: {output_path}")
        return output_path
    
    def grafico_tendencia_temporal(self):
        """Crear gráfico de líneas de tendencia temporal"""
        consulta = """
        SELECT 
            DATE(fecha_pedido) as fecha,
            SUM(total) as ventas_diarias,
            COUNT(*) as num_pedidos
        FROM pedidos
        GROUP BY DATE(fecha_pedido)
        ORDER BY fecha
        """
        
        df = self.ejecutar_consulta(consulta)
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Gráfico de ventas diarias
        ax1.plot(df['fecha'], df['ventas_diarias'], marker='o', linewidth=2, markersize=4, color='green')
        ax1.set_title('Tendencia de Ventas Diarias', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Ventas (€)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Añadir línea de tendencia
        z = np.polyfit(range(len(df)), df['ventas_diarias'], 1)
        p = np.poly1d(z)
        ax1.plot(df['fecha'], p(range(len(df))), "--", color='red', alpha=0.7, label='Tendencia')
        ax1.legend()
        
        # Gráfico de número de pedidos
        ax2.bar(df['fecha'], df['num_pedidos'], alpha=0.7, color='orange', edgecolor='darkorange')
        ax2.set_title('Número de Pedidos por Día', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Fecha', fontsize=12)
        ax2.set_ylabel('Número de Pedidos', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, 'tendencia_temporal.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico guardado: {output_path}")
        return output_path
    
    def grafico_segmentacion_clientes(self):
        """Crear gráfico de segmentación de clientes"""
        consulta = """
        SELECT 
            c.nombre,
            SUM(pd.total) as gasto_total,
            COUNT(pd.id) as num_pedidos
        FROM clientes c
        JOIN pedidos pd ON c.id = pd.cliente_id
        GROUP BY c.id, c.nombre
        ORDER BY gasto_total DESC
        """
        
        df = self.ejecutar_consulta(consulta)
        
        # Crear segmentos
        df['segmento'] = pd.cut(df['gasto_total'], bins=3, labels=['Básico', 'Premium', 'VIP'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico de dispersión: Gasto vs Número de pedidos
        colors = {'Básico': 'lightblue', 'Premium': 'orange', 'VIP': 'red'}
        for segmento in df['segmento'].unique():
            if pd.notna(segmento):
                subset = df[df['segmento'] == segmento]
                ax1.scatter(subset['num_pedidos'], subset['gasto_total'], 
                           c=colors[segmento], label=segmento, alpha=0.7, s=60)
        
        ax1.set_xlabel('Número de Pedidos', fontsize=12)
        ax1.set_ylabel('Gasto Total (€)', fontsize=12)
        ax1.set_title('Segmentación de Clientes', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de barras: Clientes por segmento
        segmento_counts = df['segmento'].value_counts()
        bars = ax2.bar(segmento_counts.index, segmento_counts.values, 
                      color=[colors[seg] for seg in segmento_counts.index], alpha=0.7)
        
        ax2.set_xlabel('Segmento', fontsize=12)
        ax2.set_ylabel('Número de Clientes', fontsize=12)
        ax2.set_title('Distribución de Clientes por Segmento', fontsize=14, fontweight='bold')
        
        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height)}', ha='center', va='bottom', fontsize=11)
        
        plt.tight_layout()
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, 'segmentacion_clientes.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico guardado: {output_path}")
        return output_path
    
    def dashboard_resumen(self):
        """Crear un dashboard con métricas clave"""
        # Obtener métricas principales
        consulta_metricas = """
        SELECT 
            COUNT(DISTINCT p.cliente_id) as clientes_unicos,
            COUNT(p.id) as total_pedidos,
            SUM(p.total) as ventas_totales,
            AVG(p.total) as ticket_promedio
        FROM pedidos p
        """
        
        metricas = self.ejecutar_consulta(consulta_metricas).iloc[0]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard de Métricas Clave', fontsize=18, fontweight='bold', y=0.95)
        
        # Métrica 1: Ventas Totales
        ax1.text(0.5, 0.5, f'€{metricas["ventas_totales"]:,.0f}', 
                ha='center', va='center', fontsize=24, fontweight='bold', color='green')
        ax1.text(0.5, 0.2, 'Ventas Totales', ha='center', va='center', fontsize=14)
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor='green', linewidth=3))
        
        # Métrica 2: Total Pedidos
        ax2.text(0.5, 0.5, f'{metricas["total_pedidos"]:,}', 
                ha='center', va='center', fontsize=24, fontweight='bold', color='blue')
        ax2.text(0.5, 0.2, 'Total Pedidos', ha='center', va='center', fontsize=14)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        ax2.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor='blue', linewidth=3))
        
        # Métrica 3: Clientes Únicos
        ax3.text(0.5, 0.5, f'{metricas["clientes_unicos"]:,}', 
                ha='center', va='center', fontsize=24, fontweight='bold', color='orange')
        ax3.text(0.5, 0.2, 'Clientes Únicos', ha='center', va='center', fontsize=14)
        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.axis('off')
        ax3.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor='orange', linewidth=3))
        
        # Métrica 4: Ticket Promedio
        ax4.text(0.5, 0.5, f'€{metricas["ticket_promedio"]:.2f}', 
                ha='center', va='center', fontsize=24, fontweight='bold', color='purple')
        ax4.text(0.5, 0.2, 'Ticket Promedio', ha='center', va='center', fontsize=14)
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        ax4.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor='purple', linewidth=3))
        
        plt.tight_layout()
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, 'dashboard_metricas.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Dashboard guardado: {output_path}")
        return output_path
    
    def generar_todas_visualizaciones(self):
        """Generar todas las visualizaciones"""
        print("🎨 GENERANDO VISUALIZACIONES...")
        print("="*50)
        
        visualizaciones = []
        
        try:
            # Importar numpy para la línea de tendencia
            import numpy as np
            globals()['np'] = np
            
            visualizaciones.append(self.dashboard_resumen())
            visualizaciones.append(self.grafico_top_productos())
            visualizaciones.append(self.grafico_ventas_por_categoria())
            visualizaciones.append(self.grafico_tendencia_temporal())
            visualizaciones.append(self.grafico_segmentacion_clientes())
            
            print(f"\n✅ {len(visualizaciones)} visualizaciones generadas exitosamente")
            print(f"📁 Ubicación: {self.output_dir}")
            
        except Exception as e:
            print(f"❌ Error generando visualizaciones: {e}")
        
        return visualizaciones
    
    def cerrar_conexion(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()

def main():
    """Función principal"""
    generador = GeneradorVisualizaciones()
    
    try:
        visualizaciones = generador.generar_todas_visualizaciones()
        
        print("\n" + "="*50)
        print("🎨 VISUALIZACIONES COMPLETADAS")
        print("="*50)
        
        for viz in visualizaciones:
            print(f"📊 {os.path.basename(viz)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        generador.cerrar_conexion()

if __name__ == "__main__":
    main()

