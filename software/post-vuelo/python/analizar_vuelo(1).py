#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════
   CANSAT MISIÓN 2 - ANÁLISIS POST-VUELO
   Detección de Firmas de Combustión (CO2 + PM2.5)
════════════════════════════════════════════════════════════════

Este script analiza los datos del vuelo y genera:
  • Mapa de calor interactivo (HTML)
  • Visualización 3D para Google Earth (KML)
  • Gráficas de análisis (PNG)
  • Informe estadístico

Sensores: SCD40 (CO2) + HM3301 (PM2.5)

Autor: IES Diego Velázquez
Fecha: Febrero 2026

USO:
    python analizar_vuelo.py                    # Usa mission2.csv
    python analizar_vuelo.py datos_vuelo.csv   # Usa archivo específico
    python analizar_vuelo.py --ejemplo         # Genera datos de ejemplo
════════════════════════════════════════════════════════════════
"""

import sys
import os
import math
import pandas as pd
import numpy as np

# Verificar dependencias
try:
    import folium
    from folium.plugins import HeatMap, MarkerCluster
except ImportError:
    print("❌ Falta librería: pip install folium")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("❌ Falta librería: pip install matplotlib")
    sys.exit(1)

try:
    import simplekml
except ImportError:
    print("⚠️ simplekml no instalado - KML no se generará")
    print("   Instalar con: pip install simplekml")
    simplekml = None

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

INPUT_FILE = 'mission2.csv'
OUTPUT_DIR = '../../data/output/'  # Relativo a software/post_vuelo/python/

# Umbrales de clasificación
UMBRALES_CO2 = {'excelente': 450, 'bueno': 600, 'moderado': 1000, 'malo': 1500}
UMBRALES_PM25 = {'excelente': 12, 'bueno': 35, 'moderado': 55, 'malo': 150}

# ════════════════════════════════════════════════════════════════
# FUNCIONES DE CLASIFICACIÓN
# ════════════════════════════════════════════════════════════════

def clasificar_co2(co2):
    """Clasifica calidad del aire según CO2"""
    if co2 < UMBRALES_CO2['excelente']:
        return 'Excelente', '#00FF00'
    elif co2 < UMBRALES_CO2['bueno']:
        return 'Bueno', '#7FFF00'
    elif co2 < UMBRALES_CO2['moderado']:
        return 'Moderado', '#FFFF00'
    elif co2 < UMBRALES_CO2['malo']:
        return 'Malo', '#FF8C00'
    else:
        return 'Muy Malo', '#FF0000'

def clasificar_pm25(pm25):
    """Clasifica calidad del aire según PM2.5"""
    if pm25 < UMBRALES_PM25['excelente']:
        return 'Excelente', '#00FF00'
    elif pm25 < UMBRALES_PM25['bueno']:
        return 'Bueno', '#7FFF00'
    elif pm25 < UMBRALES_PM25['moderado']:
        return 'Moderado', '#FFFF00'
    elif pm25 < UMBRALES_PM25['malo']:
        return 'Malo', '#FF8C00'
    else:
        return 'Muy Malo', '#FF0000'

def detectar_firma(row):
    """Detecta tipo de fuente de contaminación"""
    co2 = row['co2']
    pm25 = row['pm2_5']
    pm10 = row.get('pm10', pm25 * 1.5)
    
    if co2 > 700 and pm25 > 100:
        return '🔥 Combustión activa'
    elif co2 > 600 and pm25 > 80:
        return '🚜 Generador Diésel'
    elif co2 > 500 and pm25 > 40:
        return '🚗 Tráfico Vehicular'
    elif co2 < 480 and pm25 > 50:
        return '🌫️ Polvo (sin combustión)'
    elif co2 < 450 and pm25 < 12:
        return '🌿 Aire Limpio'
    else:
        return '🏭 Fuente mixta'

# ════════════════════════════════════════════════════════════════
# GENERADOR DE DATOS DE EJEMPLO
# ════════════════════════════════════════════════════════════════

def generar_datos_ejemplo(output_file='mission2.csv'):
    """Genera datos simulados de un vuelo"""
    print("🎲 Generando datos de ejemplo...")
    
    np.random.seed(42)
    
    # Configuración
    LAT_BASE, LON_BASE = 40.57895, -3.91842
    ALT_INICIAL = 500
    N_SAMPLES = 30
    
    timestamps = np.arange(0, N_SAMPLES * 5, 5)
    altitudes = np.linspace(ALT_INICIAL, 0, N_SAMPLES)
    
    lat_drift = np.linspace(0, 0.002, N_SAMPLES)
    lon_drift = np.linspace(0, 0.001, N_SAMPLES)
    
    latitudes = LAT_BASE + lat_drift + np.random.normal(0, 0.00001, N_SAMPLES)
    longitudes = LON_BASE + lon_drift + np.random.normal(0, 0.00001, N_SAMPLES)
    satellites = np.random.randint(6, 12, N_SAMPLES)
    
    co2, pm1_0, pm2_5, pm10, temp, hum = [], [], [], [], [], []
    
    for i in range(N_SAMPLES):
        if i < 8:  # Aire limpio (alta altitud)
            co2.append(np.random.randint(400, 450))
            pm1_0.append(np.random.randint(2, 8))
            pm2_5.append(np.random.randint(3, 12))
            pm10.append(np.random.randint(5, 15))
        elif i < 18:  # Tráfico ligero
            co2.append(np.random.randint(450, 600))
            pm1_0.append(np.random.randint(10, 25))
            pm2_5.append(np.random.randint(15, 40))
            pm10.append(np.random.randint(20, 50))
        elif i < 25:  # Tráfico intenso
            co2.append(np.random.randint(600, 900))
            pm1_0.append(np.random.randint(40, 80))
            pm2_5.append(np.random.randint(55, 120))
            pm10.append(np.random.randint(70, 150))
        else:  # Zona industrial
            co2.append(np.random.randint(800, 1200))
            pm1_0.append(np.random.randint(80, 150))
            pm2_5.append(np.random.randint(100, 200))
            pm10.append(np.random.randint(120, 250))
        
        temp.append(round(20 - (altitudes[i] / 1000) * 6.5 + np.random.uniform(-0.5, 0.5), 1))
        hum.append(np.random.randint(40, 65))
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'lat': latitudes,
        'lon': longitudes,
        'alt': altitudes,
        'sats': satellites,
        'co2': co2,
        'pm1_0': pm1_0,
        'pm2_5': pm2_5,
        'pm10': pm10,
        'temp': temp,
        'hum': hum
    })
    
    df.to_csv(output_file, index=False)
    print(f"   ✅ Guardado: {output_file} ({len(df)} muestras)")
    return df

# ════════════════════════════════════════════════════════════════
# GENERADOR DE MAPA DE CALOR
# ════════════════════════════════════════════════════════════════

def crear_mapa_calor(df, output_file='mapa_calor.html'):
    """Crea mapa interactivo con capa de calor"""
    print("🗺️  Generando mapa de calor...")
    
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles='OpenStreetMap'
    )
    
    # Capa de calor (PM2.5)
    heat_data = []
    for _, row in df.iterrows():
        if row['lat'] != 0 and row['lon'] != 0:
            intensidad = min(row['pm2_5'] / 200, 1.0)
            heat_data.append([row['lat'], row['lon'], intensidad])
    
    HeatMap(
        heat_data,
        name='Mapa de Calor PM2.5',
        min_opacity=0.4,
        max_opacity=0.8,
        radius=25,
        blur=15,
        gradient={0.0: '#00FF00', 0.3: '#FFFF00', 0.6: '#FF8C00', 1.0: '#FF0000'}
    ).add_to(mapa)
    
    # Marcadores
    marker_cluster = MarkerCluster(name='Puntos de Medición').add_to(mapa)
    
    for idx, row in df.iterrows():
        if row['lat'] != 0 and row['lon'] != 0:
            calidad_co2, color_co2 = clasificar_co2(row['co2'])
            calidad_pm25, color_pm25 = clasificar_pm25(row['pm2_5'])
            firma = detectar_firma(row)
            
            popup_html = f"""
            <div style="font-family: Arial; width: 260px;">
                <h4>📊 Medición #{idx+1}</h4>
                <hr>
                <b>⏱️</b> {row['timestamp']}s | <b>📏</b> {row['alt']:.0f}m<br>
                <b>📍</b> {row['lat']:.5f}, {row['lon']:.5f}<br>
                <hr>
                <b>💨 CO2:</b> <span style="color:{color_co2}; font-weight:bold">{row['co2']} ppm</span><br>
                <b>🌫️ PM2.5:</b> <span style="color:{color_pm25}; font-weight:bold">{row['pm2_5']} µg/m³</span><br>
                <b>🔬 PM1.0:</b> {row['pm1_0']} | <b>PM10:</b> {row['pm10']} µg/m³<br>
                <hr>
                <b>🔍 Firma:</b> {firma}
            </div>
            """
            
            icon_color = 'red' if row['pm2_5'] > 100 else 'orange' if row['pm2_5'] > 55 else 'green'
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"CO2: {row['co2']} | PM2.5: {row['pm2_5']}",
                icon=folium.Icon(color=icon_color, icon='info-sign')
            ).add_to(marker_cluster)
    
    # Trayectoria
    coords = [[row['lat'], row['lon']] for _, row in df.iterrows() if row['lat'] != 0]
    if len(coords) > 1:
        folium.PolyLine(coords, color='blue', weight=3, opacity=0.7).add_to(mapa)
        folium.Marker(coords[0], popup='🚀 Inicio', icon=folium.Icon(color='green', icon='play')).add_to(mapa)
        folium.Marker(coords[-1], popup='🎯 Aterrizaje', icon=folium.Icon(color='red', icon='stop')).add_to(mapa)
    
    # Leyenda
    leyenda = '''
    <div style="position:fixed; bottom:50px; right:50px; width:200px; background:white; 
                border:2px solid grey; padding:10px; border-radius:5px; font-size:12px; z-index:9999;">
    <b>📊 PM2.5 (µg/m³)</b><br>
    <span style="color:#00FF00">●</span> &lt;12: Excelente<br>
    <span style="color:#7FFF00">●</span> 12-35: Bueno<br>
    <span style="color:#FFFF00">●</span> 35-55: Moderado<br>
    <span style="color:#FF8C00">●</span> 55-150: Malo<br>
    <span style="color:#FF0000">●</span> &gt;150: Muy Malo
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda))
    folium.LayerControl().add_to(mapa)
    
    mapa.save(output_file)
    print(f"   ✅ Guardado: {output_file}")

# ════════════════════════════════════════════════════════════════
# GENERADOR DE KML (GOOGLE EARTH)
# ════════════════════════════════════════════════════════════════

def crear_kml(df, output_file='firmas_combustion.kml'):
    """Crea archivo KML con cilindros 3D para Google Earth"""
    if simplekml is None:
        print("⚠️  KML no generado (simplekml no instalado)")
        return
    
    print("🌍 Generando KML para Google Earth...")
    
    def create_circle(lon, lat, radius_m, n=24):
        r = radius_m / 111320.0
        return [(lon + r * math.cos(2 * math.pi * i / n), 
                 lat + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    
    def get_color(pm25, min_pm, max_pm):
        norm = (pm25 - min_pm) / max(max_pm - min_pm, 1)
        if norm < 0.5:
            r, g = int(255 * norm * 2), 255
        else:
            r, g = 255, int(255 * (2 - norm * 2))
        return f"bb00{g:02x}{r:02x}"
    
    kml = simplekml.Kml()
    kml.document.name = "CanSat Misión 2 - Firmas de Combustión"
    
    df_gps = df[(df['lat'] != 0) & (df['lon'] != 0)]
    min_pm, max_pm = df_gps['pm2_5'].min(), df_gps['pm2_5'].max()
    
    folder = kml.newfolder(name="Cilindros PM2.5")
    
    for _, row in df_gps.iterrows():
        pol = folder.newpolygon(name=f"PM2.5: {row['pm2_5']} µg/m³")
        pol.outerboundaryis = create_circle(row['lon'], row['lat'], 3.0)
        pol.extrude = 1
        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        
        color = get_color(row['pm2_5'], min_pm, max_pm)
        pol.style.polystyle.color = color
        pol.style.linestyle.color = color.replace('bb', 'ff')
        
        firma = detectar_firma(row)
        pol.description = f"""
        <b>CO2:</b> {row['co2']} ppm<br>
        <b>PM2.5:</b> {row['pm2_5']} µg/m³<br>
        <b>Altitud:</b> {row['alt']:.0f} m<br>
        <b>Firma:</b> {firma}
        """
    
    # Trayectoria
    path = kml.newlinestring(name="Trayectoria")
    path.coords = [(row['lon'], row['lat'], row['alt']) for _, row in df_gps.iterrows()]
    path.altitudemode = simplekml.AltitudeMode.absolute
    path.style.linestyle.color = 'ffffffff'
    path.style.linestyle.width = 4
    
    kml.save(output_file)
    print(f"   ✅ Guardado: {output_file}")

# ════════════════════════════════════════════════════════════════
# GENERADOR DE GRÁFICAS
# ════════════════════════════════════════════════════════════════

def crear_graficas(df, output_file='analisis_graficas.png'):
    """Crea gráficas de análisis"""
    print("📊 Generando gráficas...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CanSat Misión 2 - Análisis de Vuelo', fontsize=14, fontweight='bold')
    
    # CO2 vs Tiempo
    axes[0, 0].plot(df['timestamp'], df['co2'], 'b-', linewidth=2)
    axes[0, 0].axhline(y=450, color='g', linestyle='--', alpha=0.5)
    axes[0, 0].axhline(y=600, color='y', linestyle='--', alpha=0.5)
    axes[0, 0].axhline(y=1000, color='r', linestyle='--', alpha=0.5)
    axes[0, 0].set_xlabel('Tiempo (s)')
    axes[0, 0].set_ylabel('CO2 (ppm)')
    axes[0, 0].set_title('CO2 (SCD40)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # PM vs Tiempo
    axes[0, 1].plot(df['timestamp'], df['pm2_5'], 'r-', linewidth=2, label='PM2.5')
    axes[0, 1].plot(df['timestamp'], df['pm1_0'], 'g--', linewidth=1, label='PM1.0')
    axes[0, 1].plot(df['timestamp'], df['pm10'], 'b--', linewidth=1, label='PM10')
    axes[0, 1].axhline(y=12, color='g', linestyle=':', alpha=0.5, label='OMS')
    axes[0, 1].set_xlabel('Tiempo (s)')
    axes[0, 1].set_ylabel('µg/m³')
    axes[0, 1].set_title('Partículas (HM3301)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Correlación CO2 vs PM2.5
    scatter = axes[1, 0].scatter(df['co2'], df['pm2_5'], c=df['alt'], cmap='viridis', 
                                  s=80, alpha=0.7, edgecolors='black')
    axes[1, 0].axvline(x=600, color='gray', linestyle='--', alpha=0.3)
    axes[1, 0].axhline(y=55, color='gray', linestyle='--', alpha=0.3)
    axes[1, 0].set_xlabel('CO2 (ppm)')
    axes[1, 0].set_ylabel('PM2.5 (µg/m³)')
    axes[1, 0].set_title('Correlación (color = altitud)')
    plt.colorbar(scatter, ax=axes[1, 0], label='Altitud (m)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Perfil de vuelo
    ax2 = axes[1, 1].twinx()
    axes[1, 1].plot(df['timestamp'], df['alt'], 'k-', linewidth=2, label='Altitud')
    ax2.fill_between(df['timestamp'], 0, df['pm2_5'], alpha=0.3, color='red', label='PM2.5')
    axes[1, 1].set_xlabel('Tiempo (s)')
    axes[1, 1].set_ylabel('Altitud (m)')
    ax2.set_ylabel('PM2.5 (µg/m³)', color='red')
    axes[1, 1].set_title('Perfil de Vuelo')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {output_file}")

# ════════════════════════════════════════════════════════════════
# INFORME DE TEXTO
# ════════════════════════════════════════════════════════════════

def generar_informe(df):
    """Muestra informe estadístico"""
    print("\n" + "═" * 60)
    print("   📋 INFORME DE ANÁLISIS - CANSAT MISIÓN 2")
    print("═" * 60)
    
    print(f"\n📊 DATOS GENERALES:")
    print(f"   • Muestras: {len(df)}")
    print(f"   • Duración: {df['timestamp'].max()} s")
    print(f"   • GPS válido: {len(df[df['lat'] != 0])} puntos")
    
    print(f"\n💨 CO2 (SCD40):")
    print(f"   • Rango: {df['co2'].min()} - {df['co2'].max()} ppm")
    print(f"   • Media: {df['co2'].mean():.0f} ppm")
    
    print(f"\n🌫️ PM2.5 (HM3301):")
    print(f"   • Rango: {df['pm2_5'].min()} - {df['pm2_5'].max()} µg/m³")
    print(f"   • Media: {df['pm2_5'].mean():.0f} µg/m³")
    
    print(f"\n🔍 FIRMAS DETECTADAS:")
    firmas = df.apply(detectar_firma, axis=1)
    for firma in firmas.unique():
        count = (firmas == firma).sum()
        pct = count / len(df) * 100
        print(f"   {firma}: {count} ({pct:.0f}%)")
    
    print("\n" + "═" * 60)

# ════════════════════════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 60)
    print("   🛰️  CANSAT MISIÓN 2 - ANÁLISIS POST-VUELO")
    print("═" * 60)
    
    # Procesar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--ejemplo':
            df = generar_datos_ejemplo()
        else:
            input_file = sys.argv[1]
            print(f"📂 Cargando: {input_file}")
            df = pd.read_csv(input_file)
    else:
        if os.path.exists(INPUT_FILE):
            print(f"📂 Cargando: {INPUT_FILE}")
            df = pd.read_csv(INPUT_FILE)
        else:
            print(f"⚠️  No se encontró {INPUT_FILE}")
            df = generar_datos_ejemplo()
    
    print(f"   ✅ {len(df)} registros cargados\n")
    
    # Generar análisis
    generar_informe(df)
    crear_mapa_calor(df, 'mapa_calor.html')
    crear_kml(df, 'firmas_combustion.kml')
    crear_graficas(df, 'analisis_graficas.png')
    
    print("\n" + "═" * 60)
    print("   ✅ ANÁLISIS COMPLETADO")
    print("═" * 60)
    print("\n📁 Archivos generados:")
    print("   • mapa_calor.html      (abrir en navegador)")
    print("   • firmas_combustion.kml (abrir en Google Earth)")
    print("   • analisis_graficas.png")
    print("\n💡 Tip: Mueve los archivos a data/output/")
    print("═" * 60 + "\n")

if __name__ == "__main__":
    main()
