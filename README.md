# 🏪 Análisis de Ventas de Tienda Online

Un proyecto completo de análisis de datos que utiliza **Python** y **SQL** para analizar datos de ventas de una tienda online. Este proyecto demuestra habilidades fundamentales para un analista de datos, incluyendo extracción de datos, análisis estadístico y visualización de resultados.

## 🎯 Objetivo del Proyecto

Analizar datos de ventas para identificar:
- Tendencias de ventas y patrones de compra
- Productos más vendidos y rentables
- Segmentación de clientes por comportamiento de compra
- Métricas clave del negocio (KPIs)
- Oportunidades de crecimiento y optimización

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje principal de programación
- **SQLite** - Base de datos relacional para almacenar los datos
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Creación de visualizaciones estáticas
- **Seaborn** - Visualizaciones estadísticas avanzadas
- **NumPy** - Operaciones numéricas y estadísticas

## 📊 Análisis Realizados

### 1. Métricas Generales del Negocio
- Ventas totales y número de pedidos
- Ticket promedio por compra
- Número de clientes únicos
- Valor promedio por cliente

### 2. Análisis de Productos
- Top 10 productos más vendidos por ingresos
- Análisis de ventas por categoría de productos
- Identificación de productos estrella

### 3. Segmentación de Clientes
- Clasificación de clientes en segmentos (Básico, Premium, VIP)
- Análisis de comportamiento de compra por segmento
- Identificación de clientes de alto valor

### 4. Tendencias Temporales
- Evolución de ventas diarias
- Identificación de patrones estacionales
- Análisis de tendencias de crecimiento

## 📁 Estructura del Proyecto

```
analisis_ventas_tienda/
├── data/
│   └── tienda_online.db          # Base de datos SQLite con datos de ejemplo
├── scripts/
│   ├── crear_base_datos.py       # Script para crear y poblar la BD
│   ├── analisis_ventas.py        # Script principal de análisis
│   └── visualizaciones.py        # Generación de gráficos
├── visualizaciones/
│   ├── dashboard_metricas.png    # Dashboard con KPIs principales
│   ├── top_productos.png         # Gráfico de productos más vendidos
│   ├── ventas_por_categoria.png  # Distribución por categorías
│   ├── tendencia_temporal.png    # Evolución temporal de ventas
│   └── segmentacion_clientes.png # Análisis de segmentación
├── main.py                       # Script principal que ejecuta todo el pipeline
├── requirements.txt              # Dependencias del proyecto
├── todo.md                       # Lista de tareas del proyecto
└── README.md                     # Documentación del proyecto
```

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/analisis-ventas-tienda.git
cd analisis-ventas-tienda
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### Ejecución

**Opción 1: Ejecutar todo el pipeline (Recomendado)**
```bash
python main.py
```

**Opción 2: Ejecutar scripts individuales**
```bash
# 1. Crear la base de datos
python scripts/crear_base_datos.py

# 2. Ejecutar análisis
python scripts/analisis_ventas.py

# 3. Generar visualizaciones
python scripts/visualizaciones.py
```

## 📈 Resultados Principales

### Métricas Clave del Negocio
- **Ventas Totales:** €160,323.98
- **Número de Pedidos:** 200
- **Ticket Promedio:** €801.62
- **Clientes Únicos:** 15
- **Valor Promedio por Cliente:** €10,688.27

### Top 5 Productos Más Vendidos
1. **iPhone 14** - €29,999.69 en ingresos
2. **Laptop Dell Inspiron** - €26,999.73 en ingresos
3. **Smartwatch Apple** - €15,999.60 en ingresos
4. **Aspiradora Dyson** - €11,699.61 en ingresos
5. **Tablet Samsung** - €10,149.71 en ingresos

### Distribución por Categorías
- **Electrónicos:** 73.3% de las ventas totales
- **Hogar:** 12.5% de las ventas totales
- **Ropa:** 10.8% de las ventas totales
- **Libros:** 3.5% de las ventas totales

## 📊 Visualizaciones Generadas

El proyecto genera automáticamente 5 visualizaciones principales:

1. **Dashboard de Métricas** - Resumen visual de KPIs principales
2. **Top Productos** - Gráfico de barras de productos más vendidos
3. **Ventas por Categoría** - Gráfico circular de distribución de ventas
4. **Tendencia Temporal** - Evolución de ventas en el tiempo
5. **Segmentación de Clientes** - Análisis visual de segmentos de clientes

## 🔍 Insights y Conclusiones

### Hallazgos Principales:
- Los productos electrónicos dominan las ventas con más del 70% de los ingresos
- Existe una clara segmentación de clientes con diferentes patrones de compra
- Los clientes VIP representan el 33% de la base pero generan el 44% de los ingresos
- El ticket promedio varía significativamente entre categorías de productos

### Recomendaciones:
- Enfocar estrategias de marketing en productos electrónicos de alto valor
- Desarrollar programas de fidelización para clientes Premium y VIP
- Analizar oportunidades de cross-selling entre categorías
- Implementar estrategias para aumentar la frecuencia de compra

## 🎓 Habilidades Demostradas

Este proyecto demuestra competencias clave para un analista de datos:

### Técnicas:
- **SQL:** Consultas complejas, joins, agregaciones, filtros
- **Python:** Pandas, NumPy, manipulación de datos
- **Visualización:** Matplotlib, Seaborn, diseño de dashboards
- **Estadística:** Análisis descriptivo, segmentación, tendencias

### Metodológicas:
- Diseño de base de datos relacional
- Pipeline de análisis de datos (ETL)
- Generación de insights accionables
- Documentación técnica y presentación de resultados

## 🔄 Próximas Mejoras

- [ ] Implementar análisis de cohortes de clientes
- [ ] Añadir predicciones de ventas con machine learning
- [ ] Crear dashboard interactivo con Plotly/Dash
- [ ] Integrar datos de múltiples fuentes
- [ ] Automatizar reportes periódicos

## 📞 Contacto

**Tu Nombre**
- LinkedIn: [tu-perfil-linkedin]
- Email: tu-email@ejemplo.com
- GitHub: [tu-usuario-github]

---

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella!

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

