════════════════════════════════════════════════════════════════
   CANSAT - ANÁLISIS POST-VUELO
══════════════════════════════════════════════════════════════

Este script analiza los datos del vuelo y genera:
  • Mapa de calor interactivo (HTML)
  • Visualización 3D para Google Earth (KML)
  • Gráficas de análisis (PNG)
  • Informe estadístico

Sensores: SCD40 (CO2) + HM3301 (PM2.5) + GPS + Sensores integrados en Arduino nano 33 Sense BLE

Autor: IES Diego Velázquez
Fecha: Febrero 2026

"""
════════════════════════════════════════════════════════════════
   CANSAT - ANÁLISIS POST-VUELO
══════════════════════════════════════════════════════════════

Este script analiza los datos del vuelo y genera:
  • Mapa de calor interactivo (HTML)
  • Visualización 3D para Google Earth (KML)
  • Gráficas de análisis (PNG)
  • Informe estadístico

Sensores: SCD40 (CO2) + HM3301 (PM2.5) + GPS + Sensores integrados en Arduino nano 33 Sense BLE

Autor: IES Diego Velázquez
Fecha: Febrero 2026

Mapa de calor
     co2 > 1000 and pm25 > 55: return '🔴 Combustión Activa', '#FF0000'
    el co2 > 750 and pm25 > 35: return '🟠 Riesgo EPOC (Diésel)', '#FF8C00'
    elif co2 > 500 and pm25 > 25: return '🟡 Tráfico Vehicular', '#FFFF00'
    elif co2 < 480 and pm25 > 40: return '🌫️ Polvo Suspendido', '#808080'
    return '🌿 Aire Limpio', '#00FF00'
════════════════════════════════════════════════════════════════
"""
#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════════════════════
   CANSAT RAM - ANALIZADOR PROFESIONAL DE CALIDAD DEL AIRE
════════════════════════════════════════════════════════════════════════════════
   MODIFICACIÓN: 
   - Eliminados Clusters (ahora se ven todos los puntos individuales).
   - Sustitución de marcadores por CircleMarkers de precisión.
   - Colores de alto contraste para legibilidad médica.
════════════════════════════════════════════════════════════════════════════════
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import simplekml
import sys

# --- CONFIGURACIÓN DE ARCHIVOS ---
INPUT_FILE = 'vuelo_brunete_17marzo.csv'

# ════════════════════════════════════════════════════════════════
# 1. LÓGICA DEL SEMÁFORO DE SALUD (FIRMAS)
# ════════════════════════════════════════════════════════════════

def detectar_firma(row):
    co2 = row.get('co2', 400)
    pm25 = row.get('pm2_5', 0)
    pm10 = row.get('pm10', 0)
    
    # ROJO: COMBUSTIÓN/DIÉSEL (Peligro crítico EPOC)
    if co2 > 850 and pm25 > 50:
        return '🔴 Alerta: Humo/Diésel (Riesgo EPOC)', '#FF0000'
    
    # NARANJA: POLEN O POLVO (Peligro Asma)
    elif co2 < 550 and pm10 > 65:
        return '🟠 Alerta: Polen/Polvo (Riesgo Asma)', '#FF8C00'
    
    # AMARILLO: TRÁFICO (Dorado para lectura sobre blanco)
    elif co2 > 650 or pm25 > 30:
        return '🟡 Tráfico Urbano (Moderado)', '#B8860B' 
    
    # VERDE: AIRE LIMPIO
    else:
        return '🌿 Aire Limpio', '#008000'

# ════════════════════════════════════════════════════════════════
# 2. GENERACIÓN DEL MAPA INTERACTIVO (SIN CLUSTERS)
# ════════════════════════════════════════════════════════════════

def crear_mapa_calor(df, output_file='mapa_calor.html'):
    print("🗺️  Generando mapa de precisión con círculos...")
    
    # Crear mapa base centrado
    mapa = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=17)
    
    # Capa de Calor de fondo para ver tendencias generales
    heat_data = [[r['lat'], r['lon'], min(r['pm2_5']/100, 1)] for _, r in df.iterrows() if r['lat'] != 0]
    HeatMap(heat_data, radius=20, blur=15, min_opacity=0.3).add_to(mapa)
    
    # Añadir cada punto de medición individualmente
    for idx, row in df.iterrows():
        if row['lat'] == 0: continue
        
        firma_texto, color_hex = detectar_firma(row)
        
        # HTML del Popup optimizado (Texto dorado legible)
        popup_html = f"""
        <div style='font-family: Arial; width: 200px; padding: 5px;'>
            <h4 style='margin:0; color:#333;'>🛰️ CanSat RAM</h4>
            <hr style='margin:5px 0;'>
            <b style='color:{color_hex}; font-size:13px;'>{firma_texto}</b><br><br>
            <b>Altitud:</b> {row['alt']:.1f} m<br>
            <b>CO2:</b> {row['co2']} ppm<br>
            <b>PM2.5:</b> {row['pm2_5']} µg/m³
        </div>
        """
        
        # Usamos CircleMarker en lugar de Marker para que se vea la calidad en cada punto
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7,               # Tamaño del punto
            color='black',          # Borde negro fino para que resalte
            weight=1,
            fill=True,
            fill_color=color_hex,   # Color según el semáforo de salud
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(mapa)

    mapa.save(output_file)
    print(f"   ✅ Mapa guardado: {output_file}")

# ════════════════════════════════════════════════════════════════
# 3. OTRAS FUNCIONES (KML Y GRÁFICAS)
# ════════════════════════════════════════════════════════════════

def crear_kml(df, output_file='firmas_combustion.kml'):
    kml = simplekml.Kml()
    for _, row in df.iterrows():
        if row['lat'] == 0: continue
        _, color_hex = detectar_firma(row)
        pnt = kml.newpoint(name=f"Alt:{int(row['alt'])}m", coords=[(row['lon'], row['lat'], row['alt'])])
        pnt.altitudemode = simplekml.AltitudeMode.relativetoground
        pnt.extrude = 1
        # Convertir HEX a formato KML (aabbggrr)
        kml_color = "ff" + color_hex[5:7] + color_hex[3:5] + color_hex[1:3]
        pnt.style.iconstyle.color = kml_color
        pnt.style.linestyle.color = kml_color
    kml.save(output_file)
    print(f"   ✅ KML guardado: {output_file}")

def crear_graficas(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['pm2_5'], color='red', label='PM2.5')
    plt.plot(df['timestamp'], df['co2']/10, color='blue', label='CO2 / 10')
    plt.title("Misión Secundaria: Análisis de Salud Respiratoria")
    plt.legend(); plt.grid(True); plt.savefig('analisis_graficas.png'); plt.close()

# ════════════════════════════════════════════════════════════════
# 4. EJECUCIÓN PRINCIPAL
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        df = pd.read_csv(INPUT_FILE)
        print(f"🚀 Procesando {len(df)} puntos de datos...")
        crear_mapa_calor(df)
        crear_kml(df)
        crear_graficas(df)
        print("\n✅ ¡Todo listo! Descarga los archivos del panel lateral.")
    else:
        print(f"❌ No se encuentra el archivo {INPUT_FILE}")
