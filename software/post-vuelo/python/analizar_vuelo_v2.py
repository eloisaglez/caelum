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

#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import os
import numpy as np

# --- CONFIGURACIÓN ---
INPUT_FILE = 'vuelo_brunete_17marzo.csv'

# 1. DETECCIÓN DE FIRMAS (Tabla del README)
def detectar_firma(row):
    co2 = row.get('co2', 400)
    pm25 = row.get('pm2_5', 0)
    if co2 > 700 and pm25 > 100: return '🔥 Combustión activa', '#FF0000'
    elif co2 > 600 and pm25 > 80: return '🚜 Generador Diésel', '#FF4500'
    elif 500 <= co2 <= 700 and 40 <= pm25 <= 100: return '🚗 Tráfico Vehicular', '#B8860B'
    elif co2 < 480 and pm25 > 50: return '🌫️ Polvo', '#808080'
    elif co2 < 450 and pm25 < 12: return '🌿 Aire Limpio', '#008000'
    else: return '🏭 Fuente mixta', '#6A5ACD'

# 2. GENERACIÓN DE GRÁFICAS
def generar_graficas_unificadas(df):
    print("📊 Generando paneles de gráficas...")

    # --- FICHERO 1: graficas_mision_primaria.png (VERTICAL - 4 GRÁFICAS) ---
    fig1, axs1 = plt.subplots(4, 1, figsize=(8, 20)) # Aumentamos altura para 4 gráficas
    fig1.suptitle('Misión Primaria: Sondeo Atmosférico y Deriva', fontsize=16, fontweight='bold')

    # G1: Temperatura vs Altitud
    axs1[0].plot(df['temp'], df['alt'], color='orange', linewidth=2, marker='o', markersize=3, markevery=5)
    axs1[0].set_title("Perfil Térmico")
    axs1[0].set_xlabel("Temperatura (°C)")
    axs1[0].set_ylabel("Altitud (m)")
    axs1[0].grid(True, alpha=0.3)

    # G2: Presión vs Altitud
    presion_est = 1013.25 * (1 - 2.25577e-5 * df['alt'])**5.25588
    axs1[1].plot(presion_est, df['alt'], color='blue', linewidth=2)
    axs1[1].set_title("Perfil Barométrico (Presión)")
    axs1[1].set_xlabel("Presión (hPa)")
    axs1[1].set_ylabel("Altitud (m)")
    axs1[1].grid(True, alpha=0.3)

    # G3: Velocidad vs Altitud
    velocidad = np.abs(np.diff(df['alt'], prepend=df['alt'].iloc[0]))
    axs1[2].plot(velocidad, df['alt'], color='red', linewidth=2)
    axs1[2].axvline(x=9, color='black', linestyle='--', label='Objetivo 9m/s')
    axs1[2].set_title("Estabilidad de Caída")
    axs1[2].set_xlabel("Velocidad de Descenso (m/s)")
    axs1[2].set_ylabel("Altitud (m)")
    axs1[2].legend()

    # G4: Deriva GPS (Latitud vs Longitud) - VISTA DESDE ARRIBA
    axs1[3].plot(df['lon'], df['lat'], color='purple', linewidth=1.5, marker='>', markevery=10)
    # Marcar inicio y fin
    axs1[3].scatter(df['lon'].iloc[0], df['lat'].iloc[0], color='green', s=100, label='Inicio', zorder=5)
    axs1[3].scatter(df['lon'].iloc[-1], df['lat'].iloc[-1], color='black', s=100, label='Aterrizaje', zorder=5)
    axs1[3].set_title("Deriva GPS (Trayectoria en Planta)")
    axs1[3].set_xlabel("Longitud")
    axs1[3].set_ylabel("Latitud")
    axs1[3].legend()
    axs1[3].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('graficas_mision_primaria.png')
    plt.close()

    # --- FICHERO 2: graficas_mision_secundaria.png (DASHBOARD 2x2) ---
    fig2, axs2 = plt.subplots(2, 2, figsize=(15, 10))
    fig2.suptitle('Misión Secundaria: Análisis de Salud y Firmas', fontsize=16, fontweight='bold')

    axs2[0, 0].plot(df['timestamp'], df['co2'], color='blue')
    axs2[0, 0].set_title("Concentración de CO2 (Gases)")
    
    axs2[0, 1].plot(df['timestamp'], df['pm2_5'], color='red')
    axs2[0, 1].axhline(y=12, color='green', linestyle='--', label='Límite OMS')
    axs2[0, 1].set_title("Partículas PM2.5 (Sólidos)")
    axs2[0, 1].legend()

    scatter = axs2[1, 0].scatter(df['co2'], df['pm2_5'], c=df['alt'], cmap='viridis')
    axs2[1, 0].set_title("Correlación de Firmas (Color=Altitud)")
    axs2[1, 0].set_xlabel("CO2 (ppm)"); axs2[1, 0].set_ylabel("PM2.5 (µg/m³)")
    plt.colorbar(scatter, ax=axs2[1, 0], label='Altitud (m)')

    ax4_alt = axs2[1, 1]
    ax4_pm = ax4_alt.twinx()
    ax4_alt.plot(df['timestamp'], df['alt'], color='black', alpha=0.5)
    ax4_pm.fill_between(df['timestamp'], df['pm2_5'], color='red', alpha=0.2)
    axs2[1, 1].set_title("Capa Límite: Contaminación vs Altitud")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('graficas_mision_secundaria.png')
    plt.close()

# 3. MAPA (Puntos individuales)
def generar_mapas(df):
    print("🗺️  Generando mapa...")
    mapa = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=16)
    for _, row in df.iterrows():
        if row['lat'] == 0: continue
        nombre, color = detectar_firma(row)
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7, color='black', weight=1, fill=True, fill_color=color, fill_opacity=0.8,
            popup=f"<b>{nombre}</b>"
        ).add_to(mapa)
    mapa.save('mapa_calor.html')

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        df = pd.read_csv(INPUT_FILE)
        generar_graficas_unificadas(df)
        generar_mapas(df)
        print("\n✅ TODO GENERADO CON ÉXITO")
        print("- Misión Primaria (4 gráficas verticales): graficas_mision_primaria.png")
        print("- Misión Secundaria (Panel 2x2): graficas_mision_secundaria.png")
    else:
        print(f"❌ Error: No se encuentra {INPUT_FILE}")
