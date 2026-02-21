#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════
   CANSAT MISIÓN 2 - SIMULADOR: INVERSIÓN TÉRMICA
   IES Diego Velázquez · Equipo Caelum · Febrero 2026
════════════════════════════════════════════════════════════════

Genera un CSV con los 25 campos del CANSAT_VUELO_INTEGRADO.ino:
  timestamp, datetime, lat, lon, alt, alt_mar, sats,
  temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
  co2, pm1_0, pm2_5, pm10,
  accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase

ESCENARIO SIMULADO:
  • Lanzamiento desde cohete a 1000 m sobre terreno
  • Aeródromo de Brunete (Madrid) — 17 marzo 2026
  • Inversión térmica simulada entre 200–350 m
    (temperatura sube al bajar → partículas atrapadas)
  • CO₂ como trazador: constante en altura, sube al acercarse al suelo
  • Tres sensores de temperatura con ruido independiente por sensor
════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ──────────────────────────────────────────────────────────────
#  CONFIGURACIÓN DEL VUELO
# ──────────────────────────────────────────────────────────────

LAT_LANZAMIENTO  = 40.4052
LON_LANZAMIENTO  = -3.9931
ALT_TERRENO      = 650     # m sobre nivel del mar (Brunete)

ALT_LANZAMIENTO          = 1000   # m sobre terreno
ALT_APERTURA_PARACAIDAS  = 900    # m sobre terreno

MASA_CANSAT          = 0.325   # kg
VELOCIDAD_CAIDA_LIBRE = 25     # m/s
VELOCIDAD_PARACAIDAS  = 9      # m/s

VIENTO_NORTE = 2.5   # m/s
VIENTO_ESTE  = 1.5   # m/s

INTERVALO_MUESTREO = 1  # s

FECHA_LANZAMIENTO = datetime(2026, 3, 17, 11, 30, 0)
OUTPUT_FILE = 'datos_simulacion.csv'

# ──────────────────────────────────────────────────────────────
#  CONDICIONES METEOROLÓGICAS
# ──────────────────────────────────────────────────────────────

TEMP_SUELO       = 12.0   # °C (marzo en Madrid)
GRADIENTE_NORMAL = 6.5    # °C/1000 m (gradiente adiabático seco)
HUMEDAD_SUELO    = 55     # %
PRESION_NIVEL_MAR = 1018.0  # hPa

# ──────────────────────────────────────────────────────────────
#  INVERSIÓN TÉRMICA SIMULADA
#  Entre 200–350 m la temperatura SUBE con la altitud en vez de bajar
#  Esto atrapa PM2.5 en esa capa → patrón real de contaminación
# ──────────────────────────────────────────────────────────────

ALT_INVERSION_BASE = 200   # m sobre terreno — empieza la inversión
ALT_INVERSION_TOPE = 350   # m sobre terreno — termina la inversión
GRADIENTE_INVERSION = -3.0 # °C/1000 m (negativo = temperatura SUBE al subir)

# ──────────────────────────────────────────────────────────────
#  PERFIL DE CONTAMINACIÓN POR ALTITUD
#
#  CO₂: ~420 ppm constante en todo el perfil (fondo atmosférico global).
#       Solo ruido de sensor ±10 ppm (precisión SCD40).
#       Las fuentes del suelo no son detectables a esta altitud.
#
#  PM2.5: acumulación notable en la capa de inversión (200–350 m)
#         porque las partículas no pueden escapar hacia arriba
# ──────────────────────────────────────────────────────────────

# CO₂ ~420 ppm constante en todo el perfil — fondo atmosférico global.
# A ~1000m las fuentes del suelo no son detectables.
# Solo se añade ruido de sensor (SCD40 precisión ±10 ppm).
PERFIL_CONTAMINACION = [
    # (alt_min, alt_max, co2_base, pm25_base, descripcion)
    (700, 1000, 420, 5,  "Troposfera libre — aire limpio bien mezclado"),
    (500, 700,  420, 8,  "Transición — ligera influencia regional"),
    (350, 500,  420, 12, "Tope inversión — inicio acumulación"),
    (200, 350,  420, 48, "INVERSIÓN TÉRMICA — acumulación máxima PM"),
    (100, 200,  420, 30, "Bajo la inversión — gradiente PM"),
    (0,   100,  420, 22, "Capa superficial — tráfico y suelo"),
]

# ──────────────────────────────────────────────────────────────
#  FUNCIONES DE FÍSICA
# ──────────────────────────────────────────────────────────────

def calcular_presion(alt_sobre_mar):
    return PRESION_NIVEL_MAR * math.exp(-alt_sobre_mar / 8500)

def calcular_temperatura_real(alt_sobre_terreno):
    """
    Temperatura física con inversión térmica entre ALT_INVERSION_BASE y TOPE.
    Fuera de la capa de inversión: gradiente normal (baja con altitud).
    Dentro de la capa de inversión: gradiente invertido (sube con altitud).
    """
    if alt_sobre_terreno >= ALT_INVERSION_TOPE:
        # Por encima de la inversión — gradiente normal desde el tope
        temp_tope = TEMP_SUELO - (ALT_INVERSION_TOPE / 1000) * GRADIENTE_NORMAL
        return temp_tope - ((alt_sobre_terreno - ALT_INVERSION_TOPE) / 1000) * GRADIENTE_NORMAL

    elif alt_sobre_terreno >= ALT_INVERSION_BASE:
        # Dentro de la inversión — temperatura SUBE con la altitud
        temp_base_inv = TEMP_SUELO - (ALT_INVERSION_BASE / 1000) * GRADIENTE_NORMAL
        return temp_base_inv - ((alt_sobre_terreno - ALT_INVERSION_BASE) / 1000) * GRADIENTE_INVERSION

    else:
        # Por debajo de la inversión — gradiente normal
        return TEMP_SUELO - (alt_sobre_terreno / 1000) * GRADIENTE_NORMAL

def calcular_humedad(alt_sobre_terreno):
    """Humedad aumenta ligeramente con la altitud (más húmedo en altura)."""
    hum = HUMEDAD_SUELO + (alt_sobre_terreno / 1000) * 8
    return float(np.clip(hum + np.random.uniform(-3, 3), 25, 90))

def obtener_contaminacion(alt_sobre_terreno):
    """Devuelve (co2, pm1_0, pm2_5, pm10) según el perfil de altitud."""
    for alt_min, alt_max, co2_base, pm25_base, _ in PERFIL_CONTAMINACION:
        if alt_min <= alt_sobre_terreno < alt_max:
            # CO₂: variación realista (el SCD40 tiene ±10 ppm de ruido)
            co2 = int(np.clip(co2_base + np.random.uniform(-10, 15), 400, 600))
            # PM2.5: más variabilidad porque depende de turbulencia local
            pm25 = max(0, pm25_base + np.random.uniform(-5, 8))
            pm1_0 = max(0, pm25 * np.random.uniform(0.55, 0.70))
            pm10  = max(0, pm25 * np.random.uniform(1.25, 1.60))
            return co2, round(pm1_0, 1), round(pm25, 1), round(pm10, 1)

    return 420, 4.0, 6.0, 10.0

def simular_sensores_temperatura(temp_real):
    """
    Genera lecturas de los tres sensores de temperatura con ruido
    independiente y pequeñas derivas sistemáticas.

    HS300x : referencia (ruido ±0.3 °C)
    SCD40  : ligeramente diferente (ruido ±0.4 °C, deriva +0.1 °C)
    LPS22HB: tiende a leer algo más alto por calor del procesador
             (ruido ±0.3 °C, bias +0.4 °C)
    """
    temp_hs  = round(temp_real + np.random.uniform(-0.3, 0.3), 1)
    temp_scd = round(temp_real + 0.1 + np.random.uniform(-0.4, 0.4), 1)
    temp_lps = round(temp_real + 0.4 + np.random.uniform(-0.3, 0.3), 1)
    return temp_hs, temp_scd, temp_lps

def simular_sensores_humedad(hum_real):
    """
    HS300x : referencia (ruido ±2 %)
    SCD40  : ligeramente diferente (ruido ±2.5 %, deriva -1 %)
    """
    hum_hs  = round(float(np.clip(hum_real + np.random.uniform(-2, 2), 10, 95)), 1)
    hum_scd = round(float(np.clip(hum_real - 1.0 + np.random.uniform(-2.5, 2.5), 10, 95)), 1)
    return hum_hs, hum_scd

def calcular_imu(fase):
    """Simula lecturas de acelerómetro y giroscopio por fase de vuelo."""
    if fase == "caida_libre":
        accel = [np.random.uniform(-15, 15),
                 np.random.uniform(-15, 15),
                 np.random.uniform(-5, 5)]     # casi 0g en caída libre
        gyro  = [np.random.uniform(-100, 100),
                 np.random.uniform(-100, 100),
                 np.random.uniform(-150, 150)]
    elif fase == "apertura":
        accel = [np.random.uniform(-20, 20),
                 np.random.uniform(-20, 20),
                 np.random.uniform(150, 200)]  # tirón fuerte
        gyro  = [np.random.uniform(-50, 50),
                 np.random.uniform(-50, 50),
                 np.random.uniform(-80, 80)]
    elif fase == "descenso":
        accel = [np.random.uniform(-3, 3),
                 np.random.uniform(-3, 3),
                 np.random.uniform(95, 105)]   # ~1g estable
        gyro  = [np.random.uniform(-10, 10),
                 np.random.uniform(-10, 10),
                 np.random.uniform(-15, 15)]
    else:  # tierra / aterrizaje
        accel = [np.random.uniform(-1, 1),
                 np.random.uniform(-1, 1),
                 np.random.uniform(98, 102)]
        gyro  = [np.random.uniform(-2, 2),
                 np.random.uniform(-2, 2),
                 np.random.uniform(-2, 2)]
    return accel, gyro

# ──────────────────────────────────────────────────────────────
#  SIMULACIÓN PRINCIPAL
# ──────────────────────────────────────────────────────────────

def simular_vuelo():
    print("═" * 60)
    print("   🚀 SIMULADOR — ESCENARIO: INVERSIÓN TÉRMICA")
    print("═" * 60)
    print(f"\n📍 Brunete (Madrid) — 17 marzo 2026, 11:30h")
    print(f"📏 Altitud lanzamiento: {ALT_LANZAMIENTO} m sobre terreno")
    print(f"🌍 Altitud terreno: {ALT_TERRENO} m snm")
    print(f"🔄 Inversión térmica simulada: {ALT_INVERSION_BASE}–{ALT_INVERSION_TOPE} m")
    print(f"📊 CSV: 25 columnas (3 sensores T, 2 sensores HR)\n")

    datos = []
    altitud  = float(ALT_LANZAMIENTO)
    lat      = LAT_LANZAMIENTO
    lon      = LON_LANZAMIENTO
    tiempo   = 0
    fase     = "caida_libre"
    ts       = FECHA_LANZAMIENTO

    METROS_A_GRADOS_LAT = 1 / 111320
    METROS_A_GRADOS_LON = 1 / (111320 * math.cos(math.radians(lat)))

    print(f"{'Tiempo':>6} {'Alt(m)':>8} {'Fase':<15} {'CO2':>5} {'PM2.5':>6} {'T_HS':>6} {'T_LPS':>6}")
    print("─" * 60)

    while altitud > 0:
        # ── Determinar fase ──
        if altitud > ALT_APERTURA_PARACAIDAS:
            fase = "caida_libre"
            vel  = VELOCIDAD_CAIDA_LIBRE
        elif altitud > ALT_APERTURA_PARACAIDAS - 20:
            fase = "apertura"
            vel  = VELOCIDAD_PARACAIDAS * 2
        else:
            fase = "descenso"
            vel  = VELOCIDAD_PARACAIDAS

        altitud -= vel * INTERVALO_MUESTREO + np.random.uniform(-0.4, 0.4)
        altitud  = max(0.0, altitud)

        # Deriva GPS
        lat += VIENTO_NORTE * INTERVALO_MUESTREO * METROS_A_GRADOS_LAT + np.random.uniform(-1e-5, 1e-5)
        lon += VIENTO_ESTE  * INTERVALO_MUESTREO * METROS_A_GRADOS_LON + np.random.uniform(-1e-5, 1e-5)

        alt_mar  = ALT_TERRENO + altitud
        presion  = calcular_presion(alt_mar) + np.random.uniform(-0.5, 0.5)

        # ── Sensores de temperatura ──
        temp_real              = calcular_temperatura_real(altitud)
        temp_hs, temp_scd, temp_lps = simular_sensores_temperatura(temp_real)

        # ── Sensores de humedad ──
        hum_real          = calcular_humedad(altitud)
        hum_hs, hum_scd   = simular_sensores_humedad(hum_real)

        # ── Contaminación y CO₂ ──
        co2, pm1_0, pm2_5, pm10 = obtener_contaminacion(altitud)

        # ── IMU ──
        accel, gyro = calcular_imu(fase)
        sats        = np.random.randint(8, 12)

        registro = {
            'timestamp': tiempo,
            'datetime':  ts.isoformat(),
            'lat':       round(lat, 6),
            'lon':       round(lon, 6),
            'alt':       round(altitud, 1),
            'alt_mar':   round(alt_mar, 1),
            'sats':      sats,
            'temp_hs':   temp_hs,
            'hum_hs':    hum_hs,
            'temp_scd':  temp_scd,
            'hum_scd':   hum_scd,
            'temp_lps':  temp_lps,
            'presion':   round(presion, 1),
            'co2':       co2,
            'pm1_0':     pm1_0,
            'pm2_5':     pm2_5,
            'pm10':      pm10,
            'accel_x':   round(accel[0], 2),
            'accel_y':   round(accel[1], 2),
            'accel_z':   round(accel[2], 2),
            'gyro_x':    round(gyro[0], 1),
            'gyro_y':    round(gyro[1], 1),
            'gyro_z':    round(gyro[2], 1),
            'fase':      fase,
        }
        datos.append(registro)

        if tiempo % 10 == 0:
            print(f"{tiempo:>5}s {altitud:>7.1f}m {fase:<15} {co2:>5} {pm2_5:>6.1f} {temp_hs:>6.1f} {temp_lps:>6.1f}")

        tiempo += INTERVALO_MUESTREO
        ts     += timedelta(seconds=INTERVALO_MUESTREO)

    # ── Segundos en tierra ──
    for i in range(5):
        accel, gyro = calcular_imu("tierra")
        co2, pm1_0, pm2_5, pm10 = obtener_contaminacion(0)
        temp_real = TEMP_SUELO
        temp_hs, temp_scd, temp_lps = simular_sensores_temperatura(temp_real)
        hum_hs, hum_scd = simular_sensores_humedad(HUMEDAD_SUELO)

        registro = {
            'timestamp': tiempo,
            'datetime':  ts.isoformat(),
            'lat':       round(lat + np.random.uniform(-1e-5, 1e-5), 6),
            'lon':       round(lon + np.random.uniform(-1e-5, 1e-5), 6),
            'alt':       0.0,
            'alt_mar':   float(ALT_TERRENO),
            'sats':      np.random.randint(8, 12),
            'temp_hs':   temp_hs,
            'hum_hs':    hum_hs,
            'temp_scd':  temp_scd,
            'hum_scd':   hum_scd,
            'temp_lps':  temp_lps,
            'presion':   round(calcular_presion(ALT_TERRENO), 1),
            'co2':       co2,
            'pm1_0':     pm1_0,
            'pm2_5':     pm2_5,
            'pm10':      pm10,
            'accel_x':   round(accel[0], 2),
            'accel_y':   round(accel[1], 2),
            'accel_z':   round(accel[2], 2),
            'gyro_x':    round(gyro[0], 1),
            'gyro_y':    round(gyro[1], 1),
            'gyro_z':    round(gyro[2], 1),
            'fase':      'tierra',
        }
        datos.append(registro)
        tiempo += INTERVALO_MUESTREO
        ts     += timedelta(seconds=INTERVALO_MUESTREO)

    # ── Guardar CSV ──
    df = pd.DataFrame(datos)
    df.to_csv(OUTPUT_FILE, index=False)

    # ── Resumen ──
    print("\n" + "═" * 60)
    print("   📊 RESUMEN DEL VUELO SIMULADO")
    print("═" * 60)
    print(f"\n⏱️  Duración: {tiempo} s ({tiempo/60:.1f} min)")
    dist_lat = (lat - LAT_LANZAMIENTO) / METROS_A_GRADOS_LAT
    dist_lon = (lon - LON_LANZAMIENTO) / METROS_A_GRADOS_LON
    dist = math.sqrt(dist_lat**2 + dist_lon**2)
    print(f"📏 Deriva horizontal: {dist:.0f} m")
    print(f"\n🌡️  Temperatura HS300x: {df['temp_hs'].min():.1f} – {df['temp_hs'].max():.1f} °C")
    print(f"    ΔT HS-SCD (media): {(df['temp_hs']-df['temp_scd']).abs().mean():.2f} °C")
    print(f"    ΔT HS-LPS (media): {(df['temp_hs']-df['temp_lps']).abs().mean():.2f} °C")
    print(f"\n💨 CO₂: {df['co2'].min()} – {df['co2'].max()} ppm  (rango: {df['co2'].max()-df['co2'].min()} ppm)")
    rango_co2 = df['co2'].max() - df['co2'].min()
    print(f"    Rango CO₂: {rango_co2} ppm — {'sensor OK ✓' if rango_co2 < 30 else 'revisar sensor ⚠️'} (ruido esperado < 30 ppm)")
    print(f"\n🌫️  PM2.5: {df['pm2_5'].min():.1f} – {df['pm2_5'].max():.1f} µg/m³")

    # Verificar inversión en los datos
    df_inv = df[(df['alt'] >= ALT_INVERSION_BASE) & (df['alt'] <= ALT_INVERSION_TOPE)]
    if len(df_inv) > 0:
        print(f"\n⚠️  Inversión térmica {ALT_INVERSION_BASE}–{ALT_INVERSION_TOPE} m:")
        print(f"    Temp media en capa: {df_inv['temp_hs'].mean():.1f} °C")
        print(f"    PM2.5 medio en capa: {df_inv['pm2_5'].mean():.1f} µg/m³")

    print(f"\n📁 CSV generado: {OUTPUT_FILE}")
    print(f"   {len(df)} registros · 25 columnas")
    print(f"\n💡 Siguiente paso:")
    print(f"   python analizar_vuelo.py {OUTPUT_FILE}  # Debe detectar inversión en 200-350 m")
    print("\n" + "═" * 60)
    print("   ✅ SIMULACIÓN COMPLETADA")
    print("═" * 60 + "\n")

    return df

if __name__ == "__main__":
    df = simular_vuelo()
