import os
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, MarkerCluster
import simplekml

# ════════════════════════════════════════════════════════════════
# 1. LÓGICA DE DETECCIÓN DE FIRMAS (ASMA/EPOC)
# ════════════════════════════════════════════════════════════════

def detectar_firma(row):
    co2, pm25 = row['co2'], row['pm2_5']
    if co2 > 1000 and pm25 > 55: return '🔴 Combustión Activa', '#FF0000'
    elif co2 > 750 and pm25 > 35: return '🟠 Riesgo EPOC (Diésel)', '#FF8C00'
    elif co2 > 500 and pm25 > 25: return '🟡 Tráfico Vehicular', '#FFFF00'
    elif co2 < 480 and pm25 > 40: return '🌫️ Polvo Suspendido', '#808080'
    return '🌿 Aire Limpio', '#00FF00'

# ════════════════════════════════════════════════════════════════
# 2. FUNCIONES DE MAPA Y KML (CON POPUPS DETALLADOS)
# ════════════════════════════════════════════════════════════════

def crear_mapa_calor(df, nombre_archivo):
    print("🗺️  Generando mapa de calor detallado...")
    mapa = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=16)
    
    # Capa de Calor
    heat_data = [[r['lat'], r['lon'], min(r['pm2_5']/100, 1)] for _, r in df.iterrows() if r['lat'] != 0]
    HeatMap(heat_data, radius=15, blur=10).add_to(mapa)
    
    # Marcadores con Información Detallada (Popups)
    marker_cluster = MarkerCluster(name='Datos de Calidad del Aire').add_to(mapa)
    for _, row in df.iterrows():
        if row['lat'] == 0: continue
        firma_texto, color_hex = detectar_firma(row)
        
        # Construcción de la tabla de datos para el Popup
        popup_html = f"""
        <div style='font-family: Arial; width: 200px;'>
            <h4>📊 Medición CanSat</h4>
            <b>Altitud:</b> {row['alt']:.1f} m<br>
            <b>CO2:</b> {row['co2']} ppm<br>
            <b>PM2.5:</b> {row['pm2_5']} ug/m3<br>
            <b>Firma:</b> <span style='color:{color_hex}'>{firma_texto}</span>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            color=color_hex,
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(marker_cluster)

    mapa.save(nombre_archivo)
    print(f"   ✅ Guardado: {nombre_archivo}")

def crear_kml(df, nombre_archivo):
    print("🌍 Generando KML para Google Earth...")
    kml = simplekml.Kml()
    for _, row in df.iterrows():
        if row['lat'] == 0: continue
        firma_texto, color = detectar_firma(row)
        pnt = kml.newpoint(name=f"PM:{row['pm2_5']}")
        pnt.coords = [(row['lon'], row['lat'], row['alt'])]
        pnt.altitudemode = simplekml.AltitudeMode.relativetoground
        pnt.extrude = 1
        pnt.description = f"Firma: {firma_texto}\nCO2: {row['co2']} ppm\nAlt: {row['alt']}m"
        # Color KML: ff + BGR
        kml_color = "ff" + color[5:7] + color[3:5] + color[1:3]
        pnt.style.iconstyle.color = kml_color
        pnt.style.linestyle.color = kml_color
    kml.save(nombre_archivo)
    print(f"   ✅ Guardado: {nombre_archivo}")

# ════════════════════════════════════════════════════════════════
# 3. FUNCIONES DE INFORMES Y GRÁFICAS
# ════════════════════════════════════════════════════════════════

def generar_informe(df):
    print("\n" + "═"*40 + "\n📋 RESUMEN ESTADÍSTICO\n" + "═"*40)
    print(f"Puntos analizados: {len(df)}")
    print(f"Altitud máxima: {df['alt'].max():.1f} m")
    print(f"Pico CO2: {df['co2'].max()} ppm")
    print(f"Pico PM2.5: {df['pm2_5'].max()} ug/m3")

def crear_graficas_mision_primaria(df, out):
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['alt'], color='black', label='Altitud')
    plt.title("Misión Primaria: Perfil de Altitud")
    plt.grid(True); plt.savefig(out); plt.close()

def crear_graficas_mision_secundaria(df, out):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(df['timestamp'], df['pm2_5'], 'r-', label='PM2.5')
    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'], df['co2'], 'b-', label='CO2')
    plt.title("Misión Secundaria: Firmas de Contaminación")
    plt.savefig(out); plt.close()

def crear_graficas_extras(df, out):
    plt.figure(figsize=(8, 6))
    plt.scatter(df['co2'], df['pm2_5'], c=df['alt'], cmap='viridis')
    plt.title("Extra: Correlación Química vs Altitud")
    plt.savefig(out); plt.close()

# ════════════════════════════════════════════════════════════════
# 4. BLOQUE DE EJECUCIÓN (MODIFICADO SEGÚN TU SOLICITUD)
# ════════════════════════════════════════════════════════════════

if os.path.exists('vuelo_brunete_17marzo.csv'):
    df = pd.read_csv('vuelo_brunete_17marzo.csv')
    print(f"✅ {len(df)} registros cargados")

    generar_informe(df)
    crear_mapa_calor(df, 'mapa_calor.html')
    crear_kml(df, 'firmas_combustion.kml')
    crear_graficas_mision_primaria(df, 'graficas_mision_primaria.png')
    crear_graficas_mision_secundaria(df, 'graficas_mision_secundaria.png')
    crear_graficas_extras(df, 'graficas_extras.png')

    print("\n✅ Listo - descarga archivos del panel 📁")
else:
    print("❌ Error: 'vuelo_brunete_17marzo.csv' no encontrado.")