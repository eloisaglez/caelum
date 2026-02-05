#!/usr/bin/env python3
"""
Generador de datos simulados para testing de Misión 2
Simula un vuelo con diferentes firmas de combustión
"""

import pandas as pd
import numpy as np

# Configuración de la simulación
np.random.seed(42)

# Punto de despegue (ejemplo: cerca del IES Diego Velázquez, Torrelodones)
LAT_BASE = 40.57895
LON_BASE = -3.91842
ALT_INICIAL = 500  # metros

# Número de muestras
N_SAMPLES = 30

# Simular descenso del CanSat
timestamps = np.arange(0, N_SAMPLES * 5, 5)  # Cada 5 segundos
altitudes = np.linspace(ALT_INICIAL, 0, N_SAMPLES)

# Simular drift horizontal (viento)
lat_drift = np.linspace(0, 0.002, N_SAMPLES)  # ~220 metros al norte
lon_drift = np.linspace(0, 0.001, N_SAMPLES)  # ~80 metros al este

latitudes = LAT_BASE + lat_drift + np.random.normal(0, 0.00001, N_SAMPLES)
longitudes = LON_BASE + lon_drift + np.random.normal(0, 0.00001, N_SAMPLES)

# Simular señal GPS
satellites = np.random.randint(6, 12, N_SAMPLES)

# Simular diferentes escenarios de contaminación
tvoc = []
eco2 = []
h2_raw = []
ethanol_raw = []

for i in range(N_SAMPLES):
    # Zona 1 (alta altitud): Aire limpio
    if i < 8:
        tvoc.append(np.random.randint(30, 80))
        eco2.append(np.random.randint(400, 450))
        h2_raw.append(np.random.randint(12000, 12500))
        ethanol_raw.append(np.random.randint(17000, 17500))
    
    # Zona 2 (altitud media): Cerca de zona residencial
    elif i < 18:
        tvoc.append(np.random.randint(150, 400))
        eco2.append(np.random.randint(450, 650))
        h2_raw.append(np.random.randint(12200, 12800))
        ethanol_raw.append(np.random.randint(17200, 17800))
    
    # Zona 3 (cerca del suelo): Pasa sobre carretera con tráfico
    elif i < 25:
        tvoc.append(np.random.randint(500, 1200))
        eco2.append(np.random.randint(800, 1500))
        h2_raw.append(np.random.randint(12800, 13500))
        ethanol_raw.append(np.random.randint(17500, 18500))
    
    # Zona 4 (aterrizaje): Cerca de generador o zona industrial
    else:
        tvoc.append(np.random.randint(1500, 3000))
        eco2.append(np.random.randint(1200, 2000))
        h2_raw.append(np.random.randint(13000, 14000))
        ethanol_raw.append(np.random.randint(18000, 19500))

# Crear DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'lat': latitudes,
    'lon': longitudes,
    'alt': altitudes,
    'sats': satellites,
    'tvoc': tvoc,
    'eco2': eco2,
    'h2': h2_raw,
    'ethanol': ethanol_raw
})

# Guardar CSV
df.to_csv('mission2.csv', index=False)

print("✅ Archivo de ejemplo generado: mission2.csv")
print(f"📊 {len(df)} muestras simuladas")
print(f"\n📍 Zona de vuelo:")
print(f"   Latitud: {LAT_BASE:.6f}° - {latitudes.max():.6f}°")
print(f"   Longitud: {LON_BASE:.6f}° - {longitudes.max():.6f}°")
print(f"   Altitud: {ALT_INICIAL}m - 0m")
print(f"\n🌫️  Rango TVOC: {min(tvoc)} - {max(tvoc)} ppb")
print(f"💨 Rango eCO2: {min(eco2)} - {max(eco2)} ppm")
print(f"\n🎭 Escenarios simulados:")
print(f"   1. Alta altitud (0-40s): Aire limpio")
print(f"   2. Media altitud (45-90s): Zona residencial")
print(f"   3. Baja altitud (95-120s): Cerca de carretera")
print(f"   4. Aterrizaje (125-145s): Zona industrial")
