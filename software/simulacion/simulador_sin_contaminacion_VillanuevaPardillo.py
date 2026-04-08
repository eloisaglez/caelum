#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════
   CANSAT MISIÓN 2 - SIMULADOR: SIN CONTAMINACIÓN
   IES Diego Velázquez · Equipo Caelum · Marzo 2026
════════════════════════════════════════════════════════════════

ESCENARIO REAL:
  • Lanzamiento en globo hasta ~600 m
  • Villanueva del Pardillo (Madrid)
  • 18 marzo 2026 — 10:00
  • Registro de datos SOLO en descenso

Genera CSV con 25 variables del sistema real
════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ──────────────────────────────────────────────────────────────
# CONFIGURACIÓN DEL VUELO
# ──────────────────────────────────────────────────────────────

LAT_LANZAMIENTO  = 40.4900
LON_LANZAMIENTO  = -3.9600
ALT_TERRENO      = 650

ALT_LANZAMIENTO  = 600   # altura alcanzada con globo

VELOCIDAD_DESCENSO = 5   # m/s (descenso suave realista)

VIENTO_NORTE = 2.5
VIENTO_ESTE  = 1.5

INTERVALO_MUESTREO = 1

FECHA_LANZAMIENTO = datetime(2026, 3, 18, 10, 0, 0)
OUTPUT_FILE = 'datos_simulacion.csv'

# ──────────────────────────────────────────────────────────────
# CONDICIONES METEOROLÓGICAS
# ──────────────────────────────────────────────────────────────

TEMP_SUELO       = 12.0
GRADIENTE_NORMAL = 6.5
HUMEDAD_SUELO    = 55
PRESION_NIVEL_MAR = 1018.0

# ──────────────────────────────────────────────────────────────
# CONTAMINACIÓN (SIN CONTAMINACIÓN)
# ──────────────────────────────────────────────────────────────

PERFIL_CONTAMINACION = [
    (400, 600, 420, 4),
    (200, 400, 420, 6),
    (0,   200, 420, 8),
]

# ──────────────────────────────────────────────────────────────
# FUNCIONES
# ──────────────────────────────────────────────────────────────

def calcular_presion(alt_sobre_mar):
    return PRESION_NIVEL_MAR * math.exp(-alt_sobre_mar / 8500)

def calcular_temperatura(alt):
    return TEMP_SUELO - (alt / 1000) * GRADIENTE_NORMAL

def calcular_humedad(alt):
    hum = HUMEDAD_SUELO + (alt / 1000) * 8
    return float(np.clip(hum + np.random.uniform(-3, 3), 25, 90))

def obtener_contaminacion(alt):
    for alt_min, alt_max, co2_base, pm25_base in PERFIL_CONTAMINACION:
        if alt_min <= alt < alt_max:
            co2 = int(np.clip(co2_base + np.random.uniform(-10, 10), 400, 500))
            pm25 = max(0, pm25_base + np.random.uniform(-3, 5))
            pm1 = pm25 * 0.6
            pm10 = pm25 * 1.4
            return co2, round(pm1,1), round(pm25,1), round(pm10,1)
    return 420, 4, 6, 10

def sim_temp(temp):
    return (
        round(temp + np.random.uniform(-0.3,0.3),1),
        round(temp + 0.1 + np.random.uniform(-0.4,0.4),1),
        round(temp + 0.4 + np.random.uniform(-0.3,0.3),1)
    )

def sim_hum(hum):
    return (
        round(np.clip(hum + np.random.uniform(-2,2),10,95),1),
        round(np.clip(hum -1 + np.random.uniform(-2.5,2.5),10,95),1)
    )

def sim_imu():
    return (
        [np.random.uniform(-2,2), np.random.uniform(-2,2), np.random.uniform(95,105)],
        [np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(-10,10)]
    )

# ──────────────────────────────────────────────────────────────
# SIMULACIÓN
# ──────────────────────────────────────────────────────────────

def simular_vuelo():
    print("═"*60)
    print("🎈 SIMULACIÓN — LANZAMIENTO EN GLOBO")
    print("Villanueva del Pardillo — 18 marzo 2026, 10:00")
    print("Altura máxima ~600 m")
    print("═"*60)

    datos = []

    alt = float(ALT_LANZAMIENTO)
    lat = LAT_LANZAMIENTO
    lon = LON_LANZAMIENTO
    tiempo = 0
    ts = FECHA_LANZAMIENTO

    METROS_LAT = 1 / 111320
    METROS_LON = 1 / (111320 * math.cos(math.radians(lat)))

    while alt > 0:
        alt -= VELOCIDAD_DESCENSO + np.random.uniform(-0.3,0.3)
        alt = max(0, alt)

        lat += VIENTO_NORTE * METROS_LAT + np.random.uniform(-1e-5,1e-5)
        lon += VIENTO_ESTE  * METROS_LON + np.random.uniform(-1e-5,1e-5)

        alt_mar = ALT_TERRENO + alt
        presion = calcular_presion(alt_mar)

        temp_real = calcular_temperatura(alt)
        temp_hs, temp_scd, temp_lps = sim_temp(temp_real)

        hum_real = calcular_humedad(alt)
        hum_hs, hum_scd = sim_hum(hum_real)

        co2, pm1, pm25, pm10 = obtener_contaminacion(alt)

        accel, gyro = sim_imu()

        datos.append({
            'timestamp': tiempo,
            'datetime': ts.isoformat(),
            'lat': round(lat,6),
            'lon': round(lon,6),
            'alt': round(alt,1),
            'alt_mar': round(alt_mar,1),
            'sats': np.random.randint(8,12),
            'temp_hs': temp_hs,
            'hum_hs': hum_hs,
            'temp_scd': temp_scd,
            'hum_scd': hum_scd,
            'temp_lps': temp_lps,
            'presion': round(presion,1),
            'co2': co2,
            'pm1_0': pm1,
            'pm2_5': pm25,
            'pm10': pm10,
            'accel_x': round(accel[0],2),
            'accel_y': round(accel[1],2),
            'accel_z': round(accel[2],2),
            'gyro_x': round(gyro[0],1),
            'gyro_y': round(gyro[1],1),
            'gyro_z': round(gyro[2],1),
            'fase': 'descenso'
        })

        tiempo += 1
        ts += timedelta(seconds=1)

    df = pd.DataFrame(datos)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Simulación completada")
    print(f"📁 Archivo: {OUTPUT_FILE}")
    print(f"📊 Registros: {len(df)}")

    return df

if __name__ == "__main__":
    simular_vuelo()