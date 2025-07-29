#!/usr/bin/env python3
"""
Script principal del proyecto de Análisis de Ventas de Tienda Online.
Ejecuta todo el pipeline de análisis: creación de BD, análisis y visualizaciones.
"""

import os
import sys
from datetime import datetime

def ejecutar_script(script_path, descripcion):
    """Ejecutar un script y manejar errores"""
    print(f"\n🚀 {descripcion}...")
    print("-" * 50)
    
    try:
        # Cambiar al directorio del proyecto
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Ejecutar el script
        exit_code = os.system(f"python3 {script_path}")
        
        if exit_code == 0:
            print(f"✅ {descripcion} completado exitosamente")
            return True
        else:
            print(f"❌ Error en {descripcion}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def mostrar_banner():
    """Mostrar banner del proyecto"""
    print("=" * 70)
    print("🏪 ANÁLISIS DE VENTAS DE TIENDA ONLINE")
    print("=" * 70)
    print("📊 Proyecto de análisis de datos con Python y SQL")
    print("👨‍💻 Desarrollado para portafolio de analista de datos")
    print(f"📅 Ejecutado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def mostrar_resumen_proyecto():
    """Mostrar resumen del proyecto"""
    print("\n" + "=" * 70)
    print("📋 RESUMEN DEL PROYECTO")
    print("=" * 70)
    
    print("\n🎯 OBJETIVO:")
    print("   Analizar datos de ventas de una tienda online para identificar")
    print("   tendencias, productos más vendidos y segmentación de clientes.")
    
    print("\n🛠️ TECNOLOGÍAS UTILIZADAS:")
    print("   • Python 3.x")
    print("   • SQLite (Base de datos)")
    print("   • Pandas (Análisis de datos)")
    print("   • Matplotlib & Seaborn (Visualizaciones)")
    
    print("\n📊 ANÁLISIS REALIZADOS:")
    print("   • Métricas generales del negocio")
    print("   • Top productos más vendidos")
    print("   • Análisis por categoría de productos")
    print("   • Segmentación de clientes")
    print("   • Tendencias temporales de ventas")
    
    print("\n📁 ESTRUCTURA DEL PROYECTO:")
    print("   ├── data/")
    print("   │   └── tienda_online.db")
    print("   ├── scripts/")
    print("   │   ├── crear_base_datos.py")
    print("   │   ├── analisis_ventas.py")
    print("   │   └── visualizaciones.py")
    print("   ├── visualizaciones/")
    print("   │   └── [gráficos generados]")
    print("   ├── main.py")
    print("   └── README.md")

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = ['pandas', 'matplotlib', 'seaborn', 'sqlite3']
    faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'sqlite3':
                import sqlite3
            else:
                __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - NO ENCONTRADO")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(faltantes)}")
        print("   Instala con: pip install " + " ".join(faltantes))
        return False
    
    print("✅ Todas las dependencias están disponibles")
    return True

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ No se puede continuar sin las dependencias necesarias")
        sys.exit(1)
    
    # Mostrar resumen del proyecto
    mostrar_resumen_proyecto()
    
    print("\n" + "=" * 70)
    print("🚀 INICIANDO PIPELINE DE ANÁLISIS")
    print("=" * 70)
    
    # Pipeline de ejecución
    pasos = [
        ("scripts/crear_base_datos.py", "Creando base de datos con datos de ejemplo"),
        ("scripts/analisis_ventas.py", "Ejecutando análisis de ventas"),
        ("scripts/visualizaciones.py", "Generando visualizaciones")
    ]
    
    exitos = 0
    for script, descripcion in pasos:
        if ejecutar_script(script, descripcion):
            exitos += 1
        else:
            print(f"\n⚠️  Continuando con el siguiente paso...")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 70)
    
    print(f"✅ Pasos completados exitosamente: {exitos}/{len(pasos)}")
    
    if exitos == len(pasos):
        print("\n🎉 ¡ANÁLISIS COMPLETADO EXITOSAMENTE!")
        print("\n📁 Archivos generados:")
        print("   • data/tienda_online.db - Base de datos con datos de ejemplo")
        print("   • visualizaciones/*.png - Gráficos del análisis")
        
        print("\n🚀 Próximos pasos sugeridos:")
        print("   1. Revisar las visualizaciones generadas")
        print("   2. Personalizar los análisis según tus necesidades")
        print("   3. Añadir más datos o métricas")
        print("   4. Subir el proyecto a GitHub")
        
    else:
        print(f"\n⚠️  Se completaron {exitos} de {len(pasos)} pasos")
        print("   Revisa los errores anteriores y vuelve a ejecutar")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

