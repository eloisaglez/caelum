"""
════════════════════════════════════════════════════════════════
   CANSAT — ANÁLISIS POST-VUELO
   IES Diego Velázquez · Equipo Caelum · Febrero 2026
════════════════════════════════════════════════════════════════

OBJETIVOS CIENTÍFICOS:
  1. Perfil vertical de partículas PM1.0, PM2.5, PM10
     → Identificar capas de acumulación e inversiones térmicas
  2. CO₂ como trazador de estabilidad atmosférica
     → CO₂ constante = atmósfera bien mezclada (normal)
     → CO₂ variable con altitud = capas diferenciadas o fuentes locales
  3. Validación cruzada de temperatura y humedad
     → HS300x vs SCD40 vs LPS22HB (detección de errores de sensor)
  4. Detección de inversiones térmicas
     → Altitud↑ + Temperatura↑ + PM2.5↑ = partículas atrapadas

ESTRUCTURA CSV (25 columnas):
  timestamp, datetime, lat, lon, alt, alt_mar, sats,
  temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
  co2, pm1_0, pm2_5, pm10,
  accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase

SALIDAS:
  1. graf_1_perfil_vertical.png     → Perfiles verticales PM + CO₂ + Temperatura
  2. graf_2_inversiones_termicas.png → Detección de inversiones + capas de PM
  3. graf_3_validacion_cruzada.png  → Comparativa de los 3 sensores de temperatura
  4. graf_4_mision_primaria.png     → Altitud, presión, velocidad, trayectoria GPS
  5. mapa_vuelo.html                → Mapa interactivo con trayectoria y PM2.5
  6. informe_vuelo.txt              → Resumen estadístico del vuelo

════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import folium
import os
import sys

# ──────────────────────────────────────────────────────────────
#  CONFIGURACIÓN
# ──────────────────────────────────────────────────────────────
INPUT_FILE  = 'VUELO.CSV'          # Nombre del CSV generado por el Arduino
OUTPUT_DIR  = 'analisis_vuelo'     # Carpeta donde se guardan las salidas

# Umbrales físicos para detección de inversiones térmicas
UMBRAL_INVERSION_TEMP  =  0.5   # °C — si la temperatura SUBE más de esto al subir altitud → inversión
UMBRAL_PM25_CAPA       = 15.0   # µg/m³ — PM2.5 por encima de esto en una capa = acumulación
UMBRAL_CO2_VARIACION   = 20.0   # ppm — variación de CO₂ con la altitud que indica capas diferenciadas
DELTA_T_ALARMA         =  3.0   # °C — diferencia entre sensores de temperatura que indica error
DELTA_HR_ALARMA        =  8.0   # % — diferencia de HR entre HS300x y SCD40 que indica error

# Límites OMS para PM2.5 (µg/m³)
OMS_PM25_BUENO    = 12
OMS_PM25_MODERADO = 35
OMS_PM25_MALO     = 55

# ──────────────────────────────────────────────────────────────
#  CARGA Y LIMPIEZA DE DATOS
# ──────────────────────────────────────────────────────────────
def cargar_datos(filepath):
    """Carga el CSV, limpia datos inválidos y ordena por altitud."""
    print(f"📂 Cargando: {filepath}")
    df = pd.read_csv(filepath)

    # Normalizar nombres de columna (minúsculas, sin espacios)
    df.columns = df.columns.str.strip().str.lower()

    print(f"   {len(df)} filas, {len(df.columns)} columnas")
    print(f"   Columnas: {list(df.columns)}\n")

    # Filtrar filas con GPS inválido (lat/lon = 0)
    tiene_gps = (df['lat'] != 0) & (df['lon'] != 0)
    n_sin_gps = (~tiene_gps).sum()
    if n_sin_gps > 0:
        print(f"   ⚠️  {n_sin_gps} filas sin fix GPS (se usan para gráficas, no para mapa)")

    # Filtrar CO₂ inválido (0 = sensor no listo o error)
    df['co2'] = df['co2'].replace(0, np.nan)

    # Filtrar altitudes negativas extremas (artefactos de calibración)
    df = df[df['alt'] > -50].copy()

    # Ordenar por timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)

    return df, df[tiene_gps].copy()

# ──────────────────────────────────────────────────────────────
#  DETECCIÓN DE INVERSIONES TÉRMICAS
# ──────────────────────────────────────────────────────────────
def detectar_inversiones(df, bin_size=50):
    """
    Agrupa datos por bins de altitud y busca zonas donde
    la temperatura sube con la altitud (inversión térmica)
    y/o hay acumulación de PM2.5.
    """
    df = df.copy()
    df['alt_bin'] = (df['alt'] // bin_size) * bin_size

    perfil = df.groupby('alt_bin').agg(
        temp_media   = ('temp_hs',  'mean'),
        pm25_media   = ('pm2_5',    'mean'),
        pm25_max     = ('pm2_5',    'max'),
        pm10_media   = ('pm10',     'mean'),
        co2_media    = ('co2',      'mean'),
        n_muestras   = ('alt',      'count')
    ).reset_index()

    perfil = perfil[perfil['n_muestras'] >= 2].sort_values('alt_bin')

    # Gradiente de temperatura: positivo = temperatura sube con altitud = INVERSIÓN
    perfil['gradiente_temp'] = perfil['temp_media'].diff() / bin_size  # °C/m

    # Marcar capas problemáticas
    perfil['inversion']      = perfil['gradiente_temp'] > (UMBRAL_INVERSION_TEMP / bin_size)
    perfil['capa_pm25']      = perfil['pm25_media'] > UMBRAL_PM25_CAPA

    return perfil

# ──────────────────────────────────────────────────────────────
#  GRÁFICA 1 — PERFILES VERTICALES
# ──────────────────────────────────────────────────────────────
def graf_perfil_vertical(df, perfil, outdir):
    print("📊 [1/4] Perfiles verticales...")
    fig, axes = plt.subplots(1, 4, figsize=(20, 10), sharey=True)
    fig.suptitle('Perfil Vertical del Vuelo', fontsize=16, fontweight='bold', y=1.01)

    alt = perfil['alt_bin']

    # ── Panel 1: PM2.5 ──
    ax = axes[0]
    ax.barh(alt, perfil['pm25_media'], height=40, color='tomato', alpha=0.7, label='PM2.5 media')
    ax.barh(alt, perfil['pm25_max'],   height=40, color='darkred', alpha=0.3, label='PM2.5 máx')
    ax.axvline(OMS_PM25_BUENO,    color='green',  linestyle='--', linewidth=1, label=f'OMS Bueno ({OMS_PM25_BUENO})')
    ax.axvline(OMS_PM25_MODERADO, color='orange', linestyle='--', linewidth=1, label=f'OMS Moderado ({OMS_PM25_MODERADO})')
    # Sombrear capas con acumulación
    for _, row in perfil[perfil['capa_pm25']].iterrows():
        ax.axhspan(row['alt_bin'], row['alt_bin'] + 40, color='red', alpha=0.1)
    ax.set_xlabel('PM2.5 (µg/m³)')
    ax.set_ylabel('Altitud (m)')
    ax.set_title('Partículas PM2.5')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='x')

    # ── Panel 2: PM1.0 y PM10 ──
    ax = axes[1]
    ax.plot(df.groupby((df['alt'] // 50) * 50)['pm1_0'].mean().values,
            df.groupby((df['alt'] // 50) * 50)['pm1_0'].mean().index,
            color='blue', linewidth=2, marker='o', markersize=4, label='PM1.0')
    ax.plot(perfil['pm10_media'], alt,
            color='purple', linewidth=2, marker='s', markersize=4, label='PM10')
    ax.plot(perfil['pm25_media'], alt,
            color='red',    linewidth=2, marker='^', markersize=4, label='PM2.5')
    ax.set_xlabel('Partículas (µg/m³)')
    ax.set_title('PM1.0 / PM2.5 / PM10')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='x')

    # ── Panel 3: CO₂ como trazador de estabilidad ──
    ax = axes[2]
    co2_perfil = perfil.dropna(subset=['co2_media'])
    ax.plot(co2_perfil['co2_media'], co2_perfil['alt_bin'],
            color='steelblue', linewidth=2.5, marker='D', markersize=5)
    # Referencia: CO₂ de fondo (~420 ppm bien mezclado)
    ax.axvline(420, color='green', linestyle=':', linewidth=1.5, label='Fondo ~420 ppm')
    ax.axvline(420 + UMBRAL_CO2_VARIACION, color='orange', linestyle=':', linewidth=1, label=f'±{UMBRAL_CO2_VARIACION} ppm')
    ax.axvline(420 - UMBRAL_CO2_VARIACION, color='orange', linestyle=':', linewidth=1)
    ax.set_xlabel('CO₂ (ppm)')
    ax.set_title('CO₂ — Trazador Atmosférico')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='x')
    # Anotación interpretativa
    if not co2_perfil.empty:
        rango = co2_perfil['co2_media'].max() - co2_perfil['co2_media'].min()
        estado = 'Bien mezclada ✓' if rango < UMBRAL_CO2_VARIACION else f'Capas detectadas\n(Δ={rango:.0f} ppm)'
        ax.text(0.05, 0.95, estado, transform=ax.transAxes, fontsize=8,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ── Panel 4: Temperatura ──
    ax = axes[3]
    ax.plot(perfil['temp_media'], alt, color='orange', linewidth=2.5, marker='o', markersize=5, label='Temp HS300x')
    # Sombrear inversiones térmicas
    hay_inversion = False
    for _, row in perfil[perfil['inversion']].iterrows():
        ax.axhspan(row['alt_bin'], row['alt_bin'] + 50, color='red', alpha=0.15)
        hay_inversion = True
    if hay_inversion:
        ax.axhspan(0, 0, color='red', alpha=0.15, label='Inversión térmica')
    ax.set_xlabel('Temperatura (°C)')
    ax.set_title('Perfil Térmico')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    ruta = os.path.join(outdir, 'graf_1_perfil_vertical.png')
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {ruta}")

# ──────────────────────────────────────────────────────────────
#  GRÁFICA 2 — DETECCIÓN DE INVERSIONES TÉRMICAS
# ──────────────────────────────────────────────────────────────
def graf_inversiones(df, perfil, outdir):
    print("📊 [2/4] Inversiones térmicas...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 8), sharey=True)
    fig.suptitle('Detección de Inversiones Térmicas y Capas de Contaminación',
                 fontsize=14, fontweight='bold')

    alt = perfil['alt_bin']

    # ── Panel 1: Temperatura con gradiente marcado ──
    ax = axes[0]
    colores = ['#FF4444' if inv else '#4488FF' for inv in perfil['inversion']]
    for i in range(len(perfil) - 1):
        ax.fill_betweenx([alt.iloc[i], alt.iloc[i+1]],
                         [perfil['temp_media'].iloc[i], perfil['temp_media'].iloc[i+1]],
                         color=colores[i], alpha=0.5)
    ax.plot(perfil['temp_media'], alt, 'k-', linewidth=2, zorder=5)
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel('Altitud (m)')
    ax.set_title('Perfil Térmico\n(🔴 Inversión | 🔵 Normal)')
    ax.grid(True, alpha=0.3)

    # ── Panel 2: PM2.5 con capas marcadas ──
    ax = axes[1]
    ax.plot(perfil['pm25_media'], alt, 'r-o', linewidth=2, markersize=5)
    for _, row in perfil[perfil['capa_pm25']].iterrows():
        ax.axhspan(row['alt_bin'], row['alt_bin'] + 50,
                   color='red', alpha=0.2,
                   label='Capa acumulación' if row.name == perfil[perfil['capa_pm25']].index[0] else '')
    ax.axvline(UMBRAL_PM25_CAPA, color='orange', linestyle='--', label=f'Umbral {UMBRAL_PM25_CAPA} µg/m³')
    ax.set_xlabel('PM2.5 (µg/m³)')
    ax.set_title('PM2.5 — Capas de Acumulación')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # ── Panel 3: Combinado temp + PM2.5 (doble eje) ──
    ax = axes[2]
    ax2 = ax.twiny()
    ax.plot(perfil['temp_media'], alt, 'o-', color='orange', linewidth=2, label='Temperatura')
    ax2.plot(perfil['pm25_media'], alt, 's-', color='red',    linewidth=2, label='PM2.5')
    ax.set_xlabel('Temperatura (°C)', color='orange')
    ax2.set_xlabel('PM2.5 (µg/m³)', color='red')
    ax.set_title('Temperatura + PM2.5\n(Patrón de inversión)')
    ax.tick_params(axis='x', colors='orange')
    ax2.tick_params(axis='x', colors='red')
    ax.grid(True, alpha=0.3)
    # Leyenda combinada
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='lower right')

    # Resumen de inversiones detectadas
    n_inv = perfil['inversion'].sum()
    n_cap = perfil['capa_pm25'].sum()
    alts_inv = perfil[perfil['inversion']]['alt_bin'].tolist()
    alts_cap = perfil[perfil['capa_pm25']]['alt_bin'].tolist()

    resumen = f"Inversiones detectadas: {n_inv}\n"
    if alts_inv:
        resumen += f"  Altitudes: {alts_inv} m\n"
    resumen += f"Capas PM2.5 > {UMBRAL_PM25_CAPA} µg/m³: {n_cap}\n"
    if alts_cap:
        resumen += f"  Altitudes: {alts_cap} m"

    fig.text(0.5, -0.02, resumen, ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    ruta = os.path.join(outdir, 'graf_2_inversiones_termicas.png')
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {ruta}")

# ──────────────────────────────────────────────────────────────
#  GRÁFICA 3 — VALIDACIÓN CRUZADA DE SENSORES
# ──────────────────────────────────────────────────────────────
def graf_validacion_cruzada(df, outdir):
    print("📊 [3/4] Validación cruzada T+HR...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Validación Cruzada — Temperatura y Humedad (3 sensores)',
                 fontsize=14, fontweight='bold')

    t = df['timestamp']

    # ── Panel 1: Temperatura vs tiempo (3 sensores) ──
    ax = axes[0, 0]
    ax.plot(t, df['temp_hs'],  label='HS300x (integrado)',  color='orange',   linewidth=1.5)
    ax.plot(t, df['temp_scd'], label='SCD40 (externo)',     color='steelblue', linewidth=1.5)
    ax.plot(t, df['temp_lps'], label='LPS22HB (integrado)', color='green',    linewidth=1.5, linestyle='--')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_title('Temperatura — 3 Sensores')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel 2: Delta de temperatura entre sensores ──
    ax = axes[0, 1]
    delta_hs_scd = (df['temp_hs'] - df['temp_scd']).abs()
    delta_hs_lps = (df['temp_hs'] - df['temp_lps']).abs()
    ax.plot(t, delta_hs_scd, label='|HS300x − SCD40|',    color='purple',  linewidth=1.5)
    ax.plot(t, delta_hs_lps, label='|HS300x − LPS22HB|',  color='brown',   linewidth=1.5)
    ax.axhline(DELTA_T_ALARMA, color='red', linestyle='--', linewidth=1.5,
               label=f'Umbral alarma ({DELTA_T_ALARMA} °C)')
    ax.fill_between(t, DELTA_T_ALARMA, delta_hs_scd.clip(lower=DELTA_T_ALARMA),
                    color='red', alpha=0.15, label='Fuera de rango')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('|ΔT| (°C)')
    ax.set_title('Diferencia entre Sensores de Temperatura')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # ── Panel 3: Humedad vs tiempo (2 sensores) ──
    ax = axes[1, 0]
    ax.plot(t, df['hum_hs'],  label='HS300x (integrado)', color='dodgerblue', linewidth=1.5)
    ax.plot(t, df['hum_scd'], label='SCD40 (externo)',    color='navy',       linewidth=1.5, linestyle='--')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Humedad Relativa (%)')
    ax.set_title('Humedad Relativa — 2 Sensores')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel 4: Temperatura vs altitud (3 sensores) ──
    ax = axes[1, 1]
    ax.plot(df['temp_hs'],  df['alt'], label='HS300x',   color='orange',    linewidth=1.5, alpha=0.8)
    ax.plot(df['temp_scd'], df['alt'], label='SCD40',    color='steelblue', linewidth=1.5, alpha=0.8)
    ax.plot(df['temp_lps'], df['alt'], label='LPS22HB',  color='green',     linewidth=1.5, alpha=0.8, linestyle='--')
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel('Altitud (m)')
    ax.set_title('Temperatura vs Altitud (Perfil)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Estadísticas de validación
    stats_t = {
        'HS300x media': df['temp_hs'].mean(),
        'SCD40 media':  df['temp_scd'].mean(),
        'LPS22HB media': df['temp_lps'].mean(),
        'ΔT HS-SCD media': delta_hs_scd.mean(),
        'ΔT HS-SCD máx':   delta_hs_scd.max(),
        'ΔHR HS-SCD media': (df['hum_hs'] - df['hum_scd']).abs().mean(),
    }
    stats_txt = '\n'.join([f'{k}: {v:.1f}' + ('°C' if 'ΔHR' not in k else '%')
                            for k, v in stats_t.items()])
    fig.text(0.01, 0.01, stats_txt, fontsize=7, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    ruta = os.path.join(outdir, 'graf_3_validacion_cruzada.png')
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {ruta}")

# ──────────────────────────────────────────────────────────────
#  GRÁFICA 4 — MISIÓN PRIMARIA (altitud, presión, velocidad, GPS)
# ──────────────────────────────────────────────────────────────
def graf_mision_primaria(df, df_gps, outdir):
    print("📊 [4/4] Misión primaria...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Misión Primaria — Sondeo Atmosférico', fontsize=15, fontweight='bold')

    t = df['timestamp']

    # ── Panel 1: Altitud vs tiempo con fases ──
    ax = axes[0, 0]
    fases_color = {
        'espera': 'lightgray', 'caida_libre': 'lightyellow',
        'apertura': 'lightblue', 'descenso': 'lightgreen', 'tierra': 'lightyellow'
    }
    for fase, color in fases_color.items():
        mask = df['fase'] == fase
        if mask.any():
            ax.fill_between(t, 0, df['alt'].max(), where=mask, color=color, alpha=0.4, label=fase)
    ax.plot(t, df['alt'], color='black', linewidth=2, zorder=5)
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Altitud relativa (m)')
    ax.set_title('Altitud vs Tiempo (Fases de Vuelo)')
    ax.legend(fontsize=7, loc='upper right')
    ax.grid(True, alpha=0.3)

    # ── Panel 2: Presión vs altitud (vs modelo estándar ISA) ──
    ax = axes[0, 1]
    presion_isa = 1013.25 * (1 - 2.25577e-5 * df['alt_mar'].clip(lower=0))**5.25588
    ax.plot(df['presion'],  df['alt'], color='blue',  linewidth=2, label='Medida')
    ax.plot(presion_isa,    df['alt'], color='gray',  linewidth=1.5, linestyle='--', label='ISA (modelo)')
    ax.set_xlabel('Presión (hPa)')
    ax.set_ylabel('Altitud (m)')
    ax.set_title('Presión — Medida vs ISA')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # ── Panel 3: Velocidad de descenso ──
    ax = axes[1, 0]
    # Velocidad como variación de altitud por segundo
    vel = df['alt'].diff().abs()
    vel_rolling = vel.rolling(window=5, center=True).mean()
    ax.plot(t, vel, color='lightcoral', linewidth=1, alpha=0.5, label='Instantánea')
    ax.plot(t, vel_rolling, color='red', linewidth=2, label='Media (5s)')
    ax.axhline(9, color='green', linestyle='--', linewidth=1.5, label='Objetivo 9 m/s')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Velocidad descenso (m/s)')
    ax.set_title('Estabilidad de Caída con Paracaídas')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)

    # ── Panel 4: Trayectoria GPS ──
    ax = axes[1, 1]
    if len(df_gps) > 0:
        sc = ax.scatter(df_gps['lon'], df_gps['lat'],
                        c=df_gps['pm2_5'], cmap='YlOrRd', s=15, zorder=5)
        ax.plot(df_gps['lon'], df_gps['lat'], color='gray', linewidth=1, alpha=0.5, zorder=4)
        ax.scatter(df_gps['lon'].iloc[0],  df_gps['lat'].iloc[0],  color='green', s=120,
                   zorder=6, label='Lanzamiento', marker='^')
        ax.scatter(df_gps['lon'].iloc[-1], df_gps['lat'].iloc[-1], color='black', s=120,
                   zorder=6, label='Aterrizaje',  marker='v')
        plt.colorbar(sc, ax=ax, label='PM2.5 (µg/m³)')
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title('Trayectoria GPS (Color = PM2.5)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Sin datos GPS', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Trayectoria GPS (Sin fix)')

    plt.tight_layout()
    ruta = os.path.join(outdir, 'graf_4_mision_primaria.png')
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {ruta}")

# ──────────────────────────────────────────────────────────────
#  MAPA INTERACTIVO
# ──────────────────────────────────────────────────────────────
def generar_mapa(df_gps, perfil, outdir):
    print("🗺️  Generando mapa interactivo...")
    if len(df_gps) == 0:
        print("   ⚠️  Sin datos GPS — mapa omitido")
        return

    centro = [df_gps['lat'].mean(), df_gps['lon'].mean()]
    mapa = folium.Map(location=centro, zoom_start=15, tiles='OpenStreetMap')

    # Trayectoria completa
    coords = list(zip(df_gps['lat'], df_gps['lon']))
    folium.PolyLine(coords, color='gray', weight=1.5, opacity=0.6).add_to(mapa)

    # Puntos coloreados por PM2.5
    def color_pm25(pm):
        if pm < OMS_PM25_BUENO:    return '#00AA00'
        if pm < OMS_PM25_MODERADO: return '#FFAA00'
        if pm < OMS_PM25_MALO:     return '#FF6600'
        return '#DD0000'

    for _, row in df_gps.iterrows():
        color = color_pm25(row.get('pm2_5', 0))
        popup = (
            f"<b>Alt:</b> {row['alt']:.0f} m<br>"
            f"<b>PM2.5:</b> {row.get('pm2_5', '—'):.1f} µg/m³<br>"
            f"<b>PM10:</b> {row.get('pm10', '—'):.1f} µg/m³<br>"
            f"<b>CO₂:</b> {row.get('co2', '—')} ppm<br>"
            f"<b>Temp:</b> {row.get('temp_hs', '—'):.1f} °C<br>"
            f"<b>Fase:</b> {row.get('fase', '—')}"
        )
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6, color='black', weight=0.5,
            fill=True, fill_color=color, fill_opacity=0.85,
            popup=folium.Popup(popup, max_width=200)
        ).add_to(mapa)

    # Marcadores de inicio y fin
    folium.Marker(
        [df_gps['lat'].iloc[0], df_gps['lon'].iloc[0]],
        popup='🚀 Lanzamiento',
        icon=folium.Icon(color='green', icon='arrow-up')
    ).add_to(mapa)
    folium.Marker(
        [df_gps['lat'].iloc[-1], df_gps['lon'].iloc[-1]],
        popup='🎯 Aterrizaje',
        icon=folium.Icon(color='black', icon='arrow-down')
    ).add_to(mapa)

    # Leyenda PM2.5
    leyenda = """
    <div style='position:fixed;bottom:30px;left:30px;background:white;
                padding:10px;border:1px solid #ccc;border-radius:5px;font-size:12px;'>
    <b>PM2.5 (OMS)</b><br>
    <span style='color:#00AA00'>●</span> &lt;12 µg/m³ — Bueno<br>
    <span style='color:#FFAA00'>●</span> 12–35 µg/m³ — Moderado<br>
    <span style='color:#FF6600'>●</span> 35–55 µg/m³ — Malo<br>
    <span style='color:#DD0000'>●</span> &gt;55 µg/m³ — Muy malo
    </div>"""
    mapa.get_root().html.add_child(folium.Element(leyenda))

    ruta = os.path.join(outdir, 'mapa_vuelo.html')
    mapa.save(ruta)
    print(f"   ✅ Guardado: {ruta}")

# ──────────────────────────────────────────────────────────────
#  INFORME DE TEXTO
# ──────────────────────────────────────────────────────────────
def generar_informe(df, perfil, outdir):
    print("📄 Generando informe de texto...")
    lineas = [
        "═══════════════════════════════════════════════════",
        "  CANSAT — INFORME POST-VUELO",
        "  IES Diego Velázquez · Equipo Caelum",
        "═══════════════════════════════════════════════════",
        "",
        f"Muestras totales:  {len(df)}",
        f"Duración vuelo:    {df['timestamp'].max():.0f} s ({df['timestamp'].max()/60:.1f} min)",
        f"Altitud máxima:    {df['alt'].max():.1f} m (relativa al lanzamiento)",
        f"Altitud sobre mar: {df['alt_mar'].max():.1f} m",
        "",
        "──── TEMPERATURA (Validación cruzada) ────",
        f"  HS300x  media: {df['temp_hs'].mean():.1f} °C  |  min: {df['temp_hs'].min():.1f}  |  max: {df['temp_hs'].max():.1f}",
        f"  SCD40   media: {df['temp_scd'].mean():.1f} °C  |  min: {df['temp_scd'].min():.1f}  |  max: {df['temp_scd'].max():.1f}",
        f"  LPS22HB media: {df['temp_lps'].mean():.1f} °C  |  min: {df['temp_lps'].min():.1f}  |  max: {df['temp_lps'].max():.1f}",
        f"  ΔT HS-SCD media: {(df['temp_hs']-df['temp_scd']).abs().mean():.2f} °C  |  máx: {(df['temp_hs']-df['temp_scd']).abs().max():.2f} °C",
        f"  ΔT HS-LPS media: {(df['temp_hs']-df['temp_lps']).abs().mean():.2f} °C  |  máx: {(df['temp_hs']-df['temp_lps']).abs().max():.2f} °C",
        "",
        "──── HUMEDAD RELATIVA ────",
        f"  HS300x  media: {df['hum_hs'].mean():.1f} %",
        f"  SCD40   media: {df['hum_scd'].mean():.1f} %",
        f"  ΔHR media: {(df['hum_hs']-df['hum_scd']).abs().mean():.1f} %",
        "",
        "──── CO₂ (Trazador de estabilidad atmosférica) ────",
        f"  Media: {df['co2'].mean():.0f} ppm  |  min: {df['co2'].min():.0f}  |  max: {df['co2'].max():.0f}",
        f"  Rango total: {df['co2'].max() - df['co2'].min():.0f} ppm",
    ]

    co2_rango = df['co2'].max() - df['co2'].min()
    if co2_rango < UMBRAL_CO2_VARIACION:
        lineas.append(f"  → ATMÓSFERA BIEN MEZCLADA (Δ < {UMBRAL_CO2_VARIACION} ppm) ✓")
    else:
        lineas.append(f"  → CAPAS DETECTADAS (Δ = {co2_rango:.0f} ppm > {UMBRAL_CO2_VARIACION} ppm) ⚠️")

    n_inv = perfil['inversion'].sum()
    n_cap = perfil['capa_pm25'].sum()

    lineas += [
        "",
        "──── PARTÍCULAS ────",
        f"  PM1.0  media: {df['pm1_0'].mean():.1f}  |  máx: {df['pm1_0'].max():.1f} µg/m³",
        f"  PM2.5  media: {df['pm2_5'].mean():.1f}  |  máx: {df['pm2_5'].max():.1f} µg/m³",
        f"  PM10   media: {df['pm10'].mean():.1f}  |  máx: {df['pm10'].max():.1f} µg/m³",
        "",
        "──── INVERSIONES TÉRMICAS ────",
        f"  Capas con inversión detectadas: {n_inv}",
    ]
    if n_inv > 0:
        alts = perfil[perfil['inversion']]['alt_bin'].tolist()
        lineas.append(f"  Altitudes: {alts} m")
        lineas.append("  → Riesgo: partículas pueden descender a nivel del suelo por la noche")

    lineas += [
        f"  Capas PM2.5 > {UMBRAL_PM25_CAPA} µg/m³: {n_cap}",
        "",
        "──── FASES DE VUELO ────",
    ]
    for fase in df['fase'].unique():
        n = (df['fase'] == fase).sum()
        lineas.append(f"  {fase}: {n} s")

    lineas += ["", "═══════════════════════════════════════════════════"]

    ruta = os.path.join(outdir, 'informe_vuelo.txt')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    print(f"   ✅ Guardado: {ruta}")
    print('\n' + '\n'.join(lineas))

# ──────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Permitir pasar el CSV como argumento: python analizar_vuelo_v4.py mi_vuelo.csv
    if len(sys.argv) > 1:
        INPUT_FILE = sys.argv[1]

    if not os.path.exists(INPUT_FILE):
        print(f"❌ No se encuentra: {INPUT_FILE}")
        print("   Uso: python analizar_vuelo_v4.py [ruta_al_csv]")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n🛰️  CANSAT — ANÁLISIS POST-VUELO")
    print(f"   Archivo: {INPUT_FILE}")
    print(f"   Salidas: {OUTPUT_DIR}/\n")

    df, df_gps = cargar_datos(INPUT_FILE)
    perfil = detectar_inversiones(df)

    graf_perfil_vertical(df, perfil, OUTPUT_DIR)
    graf_inversiones(df, perfil, OUTPUT_DIR)
    graf_validacion_cruzada(df, OUTPUT_DIR)
    graf_mision_primaria(df, df_gps, OUTPUT_DIR)
    generar_mapa(df_gps, perfil, OUTPUT_DIR)
    generar_informe(df, perfil, OUTPUT_DIR)

    print("\n✅ ANÁLISIS COMPLETADO")
    print(f"   Todos los archivos en: {OUTPUT_DIR}/")
    print("   1. graf_1_perfil_vertical.png")
    print("   2. graf_2_inversiones_termicas.png")
    print("   3. graf_3_validacion_cruzada.png")
    print("   4. graf_4_mision_primaria.png")
    print("   5. mapa_vuelo.html")
    print("   6. informe_vuelo.txt")
