#!/usr/bin/env python3
"""
========================================
CANSAT MISIÓN 2 - ANÁLISIS DE DATOS
========================================

Genera mapas de calor interactivos a partir de datos
de contaminación georreferenciados del CanSat

Autor: IES Diego Velázquez - Dpto. Tecnología
Fecha: Enero 2026
"""

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============ CONFIGURACIÓN ============
INPUT_FILE = 'mission2.csv'  # Archivo generado por el CanSat
OUTPUT_HTML = 'mapa_calor_cansat.html'
OUTPUT_KML = 'firmas_combustion.kml'

# Umbrales de clasificación TVOC (ppb)
THRESHOLDS = {
    'excelente': 220,
    'buena': 660,
    'moderada': 2200,
    'mala': 5500
}

# ============ FUNCIONES AUXILIARES ============

def clasificar_calidad_aire(tvoc):
    """Clasifica la calidad del aire según TVOC"""
    if tvoc < THRESHOLDS['excelente']:
        return 'Excelente', '#00FF00'
    elif tvoc < THRESHOLDS['buena']:
        return 'Buena', '#7FFF00'
    elif tvoc < THRESHOLDS['moderada']:
        return 'Moderada', '#FFFF00'
    elif tvoc < THRESHOLDS['mala']:
        return 'Mala', '#FF8C00'
    else:
        return 'Muy Mala', '#FF0000'

def detectar_firma_combustion(row):
    """
    Detecta tipo de fuente de contaminación basado en
    patrones de sensores
    """
    tvoc = row['tvoc']
    eco2 = row['eco2']
    h2 = row['h2']
    ethanol = row['ethanol']
    
    # Patrones característicos
    if tvoc > 1000 and h2 > 13000:
        return '🚜 Generador Diésel'
    elif tvoc > 500 and ethanol > 18000:
        return '🔥 Combustión Biomasa'
    elif tvoc > 300 and eco2 > 1000 and tvoc < 800:
        return '🚗 Tráfico Vehicular'
    elif tvoc > 5000:
        return '⚠️  Contaminación Severa'
    elif tvoc < 100:
        return '🌿 Aire Limpio'
    else:
        return '🏭 Fuente Industrial'

def crear_mapa_calor(df):
    """
    Crea mapa interactivo con capa de calor y marcadores
    """
    print("🗺️  Generando mapa de calor...")
    
    # Calcular centro del mapa
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    
    # Crear mapa base
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles='OpenStreetMap'
    )
    
    # ===== CAPA 1: MAPA DE CALOR =====
    # Preparar datos para HeatMap [lat, lon, intensidad]
    heat_data = []
    for idx, row in df.iterrows():
        if row['lat'] != 0 and row['lon'] != 0:  # Filtrar GPS inválido
            # Normalizar TVOC para el mapa de calor (0-1)
            intensidad = min(row['tvoc'] / 10000, 1.0)
            heat_data.append([row['lat'], row['lon'], intensidad])
    
    # Añadir capa de calor
    HeatMap(
        heat_data,
        name='Mapa de Calor TVOC',
        min_opacity=0.4,
        max_opacity=0.8,
        radius=25,
        blur=15,
        gradient={
            0.0: '#00FF00',  # Verde (bajo)
            0.3: '#FFFF00',  # Amarillo
            0.6: '#FF8C00',  # Naranja
            1.0: '#FF0000'   # Rojo (alto)
        }
    ).add_to(mapa)
    
    # ===== CAPA 2: MARCADORES AGRUPADOS =====
    marker_cluster = MarkerCluster(name='Puntos de Medición').add_to(mapa)
    
    for idx, row in df.iterrows():
        if row['lat'] != 0 and row['lon'] != 0:
            calidad, color = clasificar_calidad_aire(row['tvoc'])
            firma = detectar_firma_combustion(row)
            
            # Crear popup con información detallada
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="margin-bottom: 5px;">📊 Medición #{idx+1}</h4>
                <hr style="margin: 5px 0;">
                <b>🕐 Tiempo:</b> {row['timestamp']}s<br>
                <b>📍 Posición:</b> {row['lat']:.6f}, {row['lon']:.6f}<br>
                <b>📏 Altitud:</b> {row['alt']:.1f} m<br>
                <b>🛰️  Satélites:</b> {row['sats']}<br>
                <hr style="margin: 5px 0;">
                <b>🌫️  TVOC:</b> <span style="color: {color}; font-weight: bold;">{row['tvoc']} ppb</span><br>
                <b>💨 eCO2:</b> {row['eco2']} ppm<br>
                <b>🔬 H2 raw:</b> {row['h2']}<br>
                <b>🔬 Ethanol raw:</b> {row['ethanol']}<br>
                <hr style="margin: 5px 0;">
                <b>📈 Calidad:</b> <span style="color: {color};">{calidad}</span><br>
                <b>🔍 Firma:</b> {firma}
            </div>
            """
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"TVOC: {row['tvoc']} ppb - {firma}",
                icon=folium.Icon(color='red' if row['tvoc'] > 1000 else 
                                       'orange' if row['tvoc'] > 500 else 
                                       'green', 
                                icon='info-sign')
            ).add_to(marker_cluster)
    
    # ===== CAPA 3: TRAYECTORIA =====
    coordenadas = [[row['lat'], row['lon']] for _, row in df.iterrows() 
                   if row['lat'] != 0 and row['lon'] != 0]
    
    if len(coordenadas) > 1:
        folium.PolyLine(
            coordenadas,
            color='blue',
            weight=3,
            opacity=0.7,
            popup='Trayectoria del CanSat',
            name='Trayectoria'
        ).add_to(mapa)
    
    # Marcador de inicio y fin
    if len(coordenadas) > 0:
        folium.Marker(
            coordenadas[0],
            popup='🚀 Inicio',
            icon=folium.Icon(color='green', icon='play')
        ).add_to(mapa)
        
        folium.Marker(
            coordenadas[-1],
            popup='🎯 Aterrizaje',
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(mapa)
    
    # ===== LEYENDA =====
    leyenda_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 220px; height: 280px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;">
    <h4 style="margin-top: 0;">📊 Leyenda TVOC</h4>
    <p><span style="color: #00FF00;">●</span> <b>0-220 ppb:</b> Excelente</p>
    <p><span style="color: #7FFF00;">●</span> <b>220-660 ppb:</b> Buena</p>
    <p><span style="color: #FFFF00;">●</span> <b>660-2200 ppb:</b> Moderada</p>
    <p><span style="color: #FF8C00;">●</span> <b>2200-5500 ppb:</b> Mala</p>
    <p><span style="color: #FF0000;">●</span> <b>>5500 ppb:</b> Muy Mala</p>
    <hr>
    <p style="font-size: 12px; margin-top: 10px;">
    🔥 Rojo intenso = Alta contaminación<br>
    🟢 Verde = Aire limpio
    </p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    # Añadir control de capas
    folium.LayerControl().add_to(mapa)
    
    # Guardar mapa
    mapa.save(OUTPUT_HTML)
    print(f"✅ Mapa guardado: {OUTPUT_HTML}")
    
    return mapa

def crear_graficas_analisis(df):
    """
    Crea gráficas de análisis estadístico
    """
    print("📊 Generando gráficas de análisis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis de Datos CanSat - Misión 2', fontsize=16, fontweight='bold')
    
    # Gráfica 1: TVOC vs Tiempo
    axes[0, 0].plot(df['timestamp'], df['tvoc'], 'b-', linewidth=2)
    axes[0, 0].axhline(y=220, color='g', linestyle='--', label='Umbral Excelente')
    axes[0, 0].axhline(y=660, color='y', linestyle='--', label='Umbral Buena')
    axes[0, 0].axhline(y=2200, color='orange', linestyle='--', label='Umbral Moderada')
    axes[0, 0].set_xlabel('Tiempo (s)')
    axes[0, 0].set_ylabel('TVOC (ppb)')
    axes[0, 0].set_title('Evolución Temporal TVOC')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Gráfica 2: eCO2 vs TVOC
    axes[0, 1].scatter(df['tvoc'], df['eco2'], c=df['tvoc'], 
                       cmap='RdYlGn_r', s=100, alpha=0.6, edgecolors='black')
    axes[0, 1].set_xlabel('TVOC (ppb)')
    axes[0, 1].set_ylabel('eCO2 (ppm)')
    axes[0, 1].set_title('Correlación TVOC vs eCO2')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Gráfica 3: Distribución TVOC
    axes[1, 0].hist(df['tvoc'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    axes[1, 0].axvline(df['tvoc'].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Media: {df["tvoc"].mean():.1f} ppb')
    axes[1, 0].set_xlabel('TVOC (ppb)')
    axes[1, 0].set_ylabel('Frecuencia')
    axes[1, 0].set_title('Distribución de Valores TVOC')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Gráfica 4: Señales Raw (H2 y Ethanol)
    ax2 = axes[1, 1].twinx()
    axes[1, 1].plot(df['timestamp'], df['h2'], 'g-', linewidth=2, label='H2')
    ax2.plot(df['timestamp'], df['ethanol'], 'orange', linewidth=2, label='Ethanol')
    axes[1, 1].set_xlabel('Tiempo (s)')
    axes[1, 1].set_ylabel('H2 (raw)', color='g')
    ax2.set_ylabel('Ethanol (raw)', color='orange')
    axes[1, 1].set_title('Señales Raw del SGP30')
    axes[1, 1].legend(loc='upper left')
    ax2.legend(loc='upper right')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analisis_cansat.png', dpi=300, bbox_inches='tight')
    print("✅ Gráficas guardadas: analisis_cansat.png")
    plt.close()

def generar_informe_texto(df):
    """
    Genera informe estadístico en texto
    """
    print("\n" + "="*60)
    print("📋 INFORME DE ANÁLISIS - CANSAT MISIÓN 2")
    print("="*60)
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   • Total de muestras: {len(df)}")
    print(f"   • Duración misión: {df['timestamp'].max()} segundos")
    print(f"   • Muestras con GPS válido: {len(df[df['lat'] != 0])}")
    
    print(f"\n🌫️  TVOC (Compuestos Volátiles):")
    print(f"   • Mínimo: {df['tvoc'].min()} ppb")
    print(f"   • Máximo: {df['tvoc'].max()} ppb")
    print(f"   • Media: {df['tvoc'].mean():.1f} ppb")
    print(f"   • Desviación estándar: {df['tvoc'].std():.1f} ppb")
    
    print(f"\n💨 eCO2 (CO2 Equivalente):")
    print(f"   • Mínimo: {df['eco2'].min()} ppm")
    print(f"   • Máximo: {df['eco2'].max()} ppm")
    print(f"   • Media: {df['eco2'].mean():.1f} ppm")
    
    # Clasificación de calidad del aire
    excelente = len(df[df['tvoc'] < 220])
    buena = len(df[(df['tvoc'] >= 220) & (df['tvoc'] < 660)])
    moderada = len(df[(df['tvoc'] >= 660) & (df['tvoc'] < 2200)])
    mala = len(df[(df['tvoc'] >= 2200) & (df['tvoc'] < 5500)])
    muy_mala = len(df[df['tvoc'] >= 5500])
    
    print(f"\n📈 CLASIFICACIÓN DE CALIDAD DEL AIRE:")
    print(f"   🟢 Excelente: {excelente} muestras ({excelente/len(df)*100:.1f}%)")
    print(f"   🟡 Buena: {buena} muestras ({buena/len(df)*100:.1f}%)")
    print(f"   🟠 Moderada: {moderada} muestras ({moderada/len(df)*100:.1f}%)")
    print(f"   🔴 Mala: {mala} muestras ({mala/len(df)*100:.1f}%)")
    print(f"   ⛔ Muy Mala: {muy_mala} muestras ({muy_mala/len(df)*100:.1f}%)")
    
    # Detección de picos
    print(f"\n🔍 DETECCIÓN DE ANOMALÍAS:")
    umbral_anomalia = df['tvoc'].mean() + 2 * df['tvoc'].std()
    anomalias = df[df['tvoc'] > umbral_anomalia]
    
    if len(anomalias) > 0:
        print(f"   ⚠️  Detectados {len(anomalias)} picos de contaminación:")
        for idx, row in anomalias.iterrows():
            print(f"      • T={row['timestamp']}s: TVOC={row['tvoc']} ppb " + 
                  f"(Pos: {row['lat']:.6f}, {row['lon']:.6f})")
    else:
        print(f"   ✅ No se detectaron anomalías significativas")
    
    print("\n" + "="*60 + "\n")

# ============ PROGRAMA PRINCIPAL ============
def main():
    print("🚀 Iniciando análisis de datos CanSat Misión 2...\n")
    
    try:
        # Cargar datos
        print(f"📂 Cargando datos desde {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE)
        print(f"✅ {len(df)} registros cargados\n")
        
        # Generar informe de texto
        generar_informe_texto(df)
        
        # Crear mapa de calor
        crear_mapa_calor(df)
        
        # Crear gráficas de análisis
        crear_graficas_analisis(df)
        
        print("\n✅ ANÁLISIS COMPLETADO")
        print(f"📁 Archivos generados:")
        print(f"   • {OUTPUT_HTML} (mapa interactivo)")
        print(f"   • analisis_cansat.png (gráficas)")
        print(f"\n💡 Abre {OUTPUT_HTML} en tu navegador para ver el mapa interactivo")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {INPUT_FILE}")
        print("   Asegúrate de tener el CSV generado por el CanSat")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
