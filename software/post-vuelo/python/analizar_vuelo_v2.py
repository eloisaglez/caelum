"""
════════════════════════════════════════════════════════════════
   CANSAT - ANÁLISIS POST-VUELO - SOFTWARE DE ANÁLISIS EPIDEMIOLÓGICO AMBIENTAL
══════════════════════════════════════════════════════════════
Este script analiza los datos del vuelo y genera:
  • Mapa de calor interactivo (HTML)
  • Visualización 3D para Google Earth (KML)
  • Gráficas de análisis (PNG)
  • Informe estadístico

Sensores: SCD40 (CO2) + HM3301 (PM2.5) + GPS + Sensores integrados en Arduino nano 33 Sense BLE
════════════════════════════════════════════════════════════════
 OBJETIVO: Generar evidencias para el estudio de Asma y EPOC.
   SALIDAS:
   1. mapa_calor.html -> Mapa interactivo con círculos y consejos médicos.
   2. firmas_combustion.kml -> Trayectoria 3D para Google Earth.
   3. graf_1_mision_primaria.png -> Perfil de altitud.
   4. graf_2_mision_secundaria.png -> Semáforo de riesgo por tiempo.
   5. graf_3_perfil_vertical.png -> Análisis de contaminación por altura.

════════════════════════════════════════════════════════════════
   MODIFICACIÓN: 
   - Mapa de calor
   - Eliminados Clusters (ahora se ven todos los puntos individuales).
   - Sustitución de marcadores por CircleMarkers de precisión.
   - Colores de alto contraste para legibilidad.
   - Gráficas
════════════════════════════════════════════════════════════════════════════════

Semáforo
    co2 > 800 and pm25 > 50: 🔴 Alerta: Humo/Diésel (Riesgo EPOC)'
    co2 < 500 and pm10 > 60: 🟠 Alerta: Polen/Polvo (Riesgo Asma)'
    co2 < 480 and pm25 > 40:🌫️ Polvo Suspendido (Irritación)'
    co2 > 650 or pm25 > 25: 🟡 Tráfico Urbano (Moderado)'
    pm10 > 100:🌫️ Calima / Polvo Mineral'
    co2 < 480 and pm25 < 25 :🌿 Aire Limpio'

Fecha: Febrero 2026
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import simplekml

# --- CONFIGURACIÓN DEL ARCHIVO ---
INPUT_FILE = 'vuelo_brunete_17marzo.csv'

# ════════════════════════════════════════════════════════════════
# 1. LÓGICA DE FIRMAS Y CONSEJOS MÉDICOS
# ════════════════════════════════════════════════════════════════

def detectar_firma_y_consejo(row):
    co2 = row.get('co2', 400)
    pm25 = row.get('pm2_5', 0)
    pm10 = row.get('pm10', 0)
    
    # 🔴 COMBUSTIÓN / DIÉSEL: Riesgo Crítico EPOC
    if co2 > 850 and pm25 > 50:
        return ('🔴 Alerta: Diésel (EPOC)', 
                '⚠️ Riesgo de inflamación sistémica. Pacientes con EPOC deben evitar esta zona.', 
                '#FF0000')
    
    # 🌫️ CALIMA / POLVO MINERAL: Riesgo Mecánico
    elif pm10 > 100:
        return ('🌫️ Calima / Polvo Mineral', 
                '⚠️ Irritación mecánica de las vías aéreas. Se recomienda cerrar ventanas.', 
                '#696969')
    
    # 🟠 POLEN / ALERGIA: Riesgo Asma
    elif co2 < 550 and pm10 > 65:
        return ('🟠 Alerta: Polen (Asma)', 
                '⚠️ Riesgo de broncoespasmo alérgico. Precaución para asmáticos.', 
                '#FF8C00')

    # 🌫️ POLVO SUSPENDIDO: Tu línea específica
    elif co2 < 480 and pm25 > 40:
        return ('🌫️ Polvo Suspendido', 
                'ℹ️ Partículas en suspensión sin origen químico. Evitar deporte intenso.', 
                '#808080')
    
    # 🟡 TRÁFICO URBANO: Moderado (Dorado para contraste)
    elif co2 > 650 or pm25 > 30:
        return ('🟡 Tráfico Urbano (Moderado)', 
                'ℹ️ Concentración moderada de gases. Ventilar espacios cerrados.', 
                '#B8860B') 
    
    # 🌿 AIRE LIMPIO
    else:
        return ('🌿 Aire Limpio', 
                '✅ Condiciones óptimas para la salud respiratoria.', 
                '#008000')

# ════════════════════════════════════════════════════════════════
# 2. GENERACIÓN DE GRÁFICAS POR SEPARADO
# ════════════════════════════════════════════════════════════════

def crear_graficas_cientificas(df):
    print("📊 Generando set de gráficas para la memoria...")

    # --- GRÁFICA 1: MISIÓN PRIMARIA ---
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['alt'], color='black', linewidth=2)
    plt.fill_between(df['timestamp'], df['alt'], color='skyblue', alpha=0.3)
    plt.title("Gráfica 1: Perfil de Vuelo (Altitud vs Tiempo)")
    plt.xlabel("Tiempo (s)"); plt.ylabel("Altitud (m)")
    plt.grid(True, linestyle='--')
    plt.savefig('graf_1_mision_primaria.png')
    plt.close()

    # --- GRÁFICA 2: MISIÓN SECUNDARIA (SEMÁFORO) ---
    fig2, ax1 = plt.subplots(figsize=(11, 6))
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('PM2.5 (µg/m³)', color='red')
    ax1.plot(df['timestamp'], df['pm2_5'], color='darkred', linewidth=2, label='PM2.5 (Partículas)')
    
    # Franjas de Salud
    ax1.axhspan(0, 12, color='green', alpha=0.1, label='Zona Segura')
    ax1.axhspan(12, 35, color='yellow', alpha=0.1, label='Moderado')
    ax1.axhspan(35, df['pm2_5'].max()+20, color='red', alpha=0.1, label='Riesgo Asma/EPOC')

    ax2 = ax1.twinx()
    ax2.set_ylabel('CO2 (ppm)', color='blue')
    ax2.plot(df['timestamp'], df['co2'], color='blue', alpha=0.4, linestyle='--', label='CO2 (Gases)')
    
    plt.title("Gráfica 2: Análisis de Riesgo Respiratorio y Combustión")
    ax1.legend(loc='upper left', fontsize=9)
    plt.savefig('graf_2_mision_secundaria.png')
    plt.close()

    # --- GRÁFICA 3: PERFIL VERTICAL ---
    plt.figure(figsize=(7, 8))
    plt.scatter(df['pm2_5'], df['alt'], c=df['pm2_5'], cmap='RdYlGn_r', alpha=0.7, edgecolors='none')
    plt.title("Gráfica 3: Perfil Vertical (Contaminación por Altitud)")
    plt.xlabel("Contaminación PM2.5 (µg/m³)"); plt.ylabel("Altitud (m)")
    plt.grid(True, alpha=0.3)
    plt.savefig('graf_3_perfil_vertical.png')
    plt.close()

# ════════════════════════════════════════════════════════════════
# 3. MAPA Y KML
# ════════════════════════════════════════════════════════════════

def generar_mapas(df):
    print("🗺️  Generando mapa interactivo y KML...")
    mapa = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=17)
    
    # Capa de Calor de fondo
    heat_data = [[r['lat'], r['lon'], min(r['pm2_5']/100, 1)] for _, r in df.iterrows() if r['lat'] != 0]
    HeatMap(heat_data, radius=18, blur=15, min_opacity=0.3).add_to(mapa)
    
    kml = simplekml.Kml()

    for _, row in df.iterrows():
        if row['lat'] == 0: continue
        firma, consejo, color = detectar_firma_y_consejo(row)
        
        # Mapa interactivo
        popup_html = f"""
        <div style='font-family: Arial; width: 220px; font-size: 12px;'>
            <h4 style='margin:0; color:#333; border-bottom: 2px solid {color};'>🛰️ CanSat RAM</h4>
            <p style='margin: 8px 0;'><b>Firma:</b> <span style='color:{color};'>{firma}</span></p>
            <p style='background:#f9f9f9; padding:5px; border-radius:3px;'><i>{consejo}</i></p>
            <b>PM2.5:</b> {row['pm2_5']} µg/m³ | <b>Alt:</b> {row['alt']:.1f} m
        </div>
        """
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7, color='black', weight=1, fill=True, fill_color=color, fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(mapa)
        
        # KML 3D
        pnt = kml.newpoint(name=f"{int(row['alt'])}m", coords=[(row['lon'], row['lat'], row['alt'])])
        pnt.altitudemode = simplekml.AltitudeMode.relativetoground
        pnt.extrude = 1
        kml_col = "ff" + color[5:7] + color[3:5] + color[1:3]
        pnt.style.iconstyle.color = kml_col
        pnt.style.linestyle.color = kml_col

    mapa.save('mapa_calor.html')
    kml.save('firmas_combustion.kml')

# ════════════════════════════════════════════════════════════════
# 4. INICIO DEL PROGRAMA
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        datos = pd.read_csv(INPUT_FILE)
        print(f"🚀 Archivo '{INPUT_FILE}' cargado. {len(datos)} puntos detectados.")
        
        crear_graficas_cientificas(datos)
        generar_mapas(datos)
        
        print("\n✅ PROCESO FINALIZADO.")
        print("1. Descarga 'mapa_calor.html' para ver los consejos médicos.")
        print("2. Usa las 3 gráficas PNG para tu memoria de proyecto.")
    else:
        print(f"❌ Error: No se encuentra el archivo {INPUT_FILE}")


