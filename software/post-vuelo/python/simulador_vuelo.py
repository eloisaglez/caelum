#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════
   CANSAT MISIÓN 2 - SIMULADOR DE VUELO
   Genera datos realistas para testing
════════════════════════════════════════════════════════════════

Simula un vuelo completo del CanSat:
  • Lanzamiento desde cohete a 1000m
  • Caída libre inicial
  • Apertura de paracaídas
  • Descenso a 9 m/s
  • Aterrizaje

Configuración:
  • Ubicación: Aeródromo de Brunete (Madrid)
  • Fecha: 17 de marzo 2026
  • Peso CanSat: 325 gramos
  • Velocidad descenso: 9 m/s (con paracaídas)

Autor: IES Diego Velázquez
Fecha: Febrero 2026
════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL VUELO
# ════════════════════════════════════════════════════════════════

# Aeródromo de Brunete (Madrid)
LAT_LANZAMIENTO = 40.4052
LON_LANZAMIENTO = -3.9931
ALT_TERRENO = 650  # Altitud del aeródromo sobre nivel del mar (m)

# Parámetros de vuelo
ALT_LANZAMIENTO = 1000  # Altitud de separación del cohete (m sobre terreno)
ALT_APERTURA_PARACAIDAS = 900  # Altitud donde abre paracaídas (m sobre terreno)

# Física del CanSat
MASA_CANSAT = 0.325  # kg (325 gramos)
VELOCIDAD_CAIDA_LIBRE = 25  # m/s (antes de paracaídas)
VELOCIDAD_PARACAIDAS = 9  # m/s (con paracaídas abierto)

# Viento (deriva horizontal)
VIENTO_NORTE = 2.5  # m/s hacia el norte
VIENTO_ESTE = 1.5   # m/s hacia el este

# Intervalo de muestreo
INTERVALO_MUESTREO = 1  # segundos

# Fecha y hora del lanzamiento
FECHA_LANZAMIENTO = datetime(2026, 3, 17, 11, 30, 0)  # 17 marzo 2026, 11:30

# Archivo de salida
OUTPUT_FILE = 'vuelo_brunete_17marzo.csv'

# ════════════════════════════════════════════════════════════════
# CONDICIONES METEOROLÓGICAS (17 marzo en Brunete)
# ════════════════════════════════════════════════════════════════

# Temperatura al nivel del suelo (marzo en Madrid ~12°C)
TEMP_SUELO = 12.0  # °C
GRADIENTE_TERMICO = 6.5  # °C por cada 1000m de altitud

# Humedad relativa
HUMEDAD_SUELO = 55  # %

# Presión atmosférica al nivel del mar
PRESION_NIVEL_MAR = 1018.0  # hPa (típico marzo)

# ════════════════════════════════════════════════════════════════
# ZONAS DE CONTAMINACIÓN (simuladas sobre Brunete)
# ════════════════════════════════════════════════════════════════

ZONAS_CONTAMINACION = [
    # (alt_min, alt_max, co2_base, pm25_base, descripcion)
    (800, 1000, 415, 8, "Aire limpio (alta altitud)"),
    (500, 800, 430, 15, "Capa de mezcla superior"),
    (300, 500, 480, 35, "Influencia tráfico M-501"),
    (100, 300, 520, 55, "Capa límite urbana"),
    (0, 100, 580, 75, "Cerca del suelo (polvo + tráfico)"),
]

# ════════════════════════════════════════════════════════════════
# FUNCIONES DE SIMULACIÓN
# ════════════════════════════════════════════════════════════════

def calcular_presion(altitud_sobre_mar):
    """Calcula presión atmosférica según altitud (ecuación barométrica)"""
    return PRESION_NIVEL_MAR * math.exp(-altitud_sobre_mar / 8500)

def calcular_temperatura(altitud_sobre_terreno):
    """Calcula temperatura según altitud"""
    return TEMP_SUELO - (altitud_sobre_terreno / 1000) * GRADIENTE_TERMICO

def calcular_humedad(altitud_sobre_terreno):
    """Calcula humedad según altitud (aumenta con altura hasta cierto punto)"""
    hum = HUMEDAD_SUELO + (altitud_sobre_terreno / 100) * 2
    return min(85, max(30, hum + np.random.uniform(-3, 3)))

def obtener_contaminacion(altitud_sobre_terreno):
    """Obtiene niveles de CO2 y PM2.5 según zona de altitud"""
    for alt_min, alt_max, co2_base, pm25_base, _ in ZONAS_CONTAMINACION:
        if alt_min <= altitud_sobre_terreno < alt_max:
            # Añadir variación realista
            co2 = co2_base + np.random.uniform(-20, 30)
            pm25 = pm25_base + np.random.uniform(-5, 10)
            
            # PM1.0 y PM10 proporcionales
            pm1_0 = pm25 * np.random.uniform(0.6, 0.8)
            pm10 = pm25 * np.random.uniform(1.2, 1.5)
            
            return int(co2), int(pm1_0), int(pm25), int(pm10)
    
    # Por defecto (muy alto o muy bajo)
    return 420, 5, 8, 12

def calcular_imu(fase, velocidad_vertical):
    """Calcula datos del IMU según fase de vuelo"""
    if fase == "caida_libre":
        # Caída libre: baja aceleración Z, rotación alta
        accel = [
            np.random.uniform(-15, 15),
            np.random.uniform(-15, 15),
            np.random.uniform(-5, 5)  # Casi 0g en caída libre
        ]
        gyro = [
            np.random.uniform(-100, 100),
            np.random.uniform(-100, 100),
            np.random.uniform(-150, 150)
        ]
    elif fase == "apertura":
        # Apertura paracaídas: tirón fuerte
        accel = [
            np.random.uniform(-20, 20),
            np.random.uniform(-20, 20),
            np.random.uniform(150, 200)  # Tirón hacia arriba
        ]
        gyro = [
            np.random.uniform(-50, 50),
            np.random.uniform(-50, 50),
            np.random.uniform(-80, 80)
        ]
    elif fase == "descenso":
        # Descenso estable con paracaídas
        accel = [
            np.random.uniform(-3, 3),
            np.random.uniform(-3, 3),
            np.random.uniform(95, 105)  # ~1g
        ]
        gyro = [
            np.random.uniform(-10, 10),
            np.random.uniform(-10, 10),
            np.random.uniform(-15, 15)
        ]
    else:  # aterrizaje
        # Impacto y reposo
        accel = [
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1),
            np.random.uniform(98, 102)
        ]
        gyro = [
            np.random.uniform(-2, 2),
            np.random.uniform(-2, 2),
            np.random.uniform(-2, 2)
        ]
    
    return accel, gyro

# ════════════════════════════════════════════════════════════════
# SIMULACIÓN PRINCIPAL
# ════════════════════════════════════════════════════════════════

def simular_vuelo():
    """Simula el vuelo completo del CanSat"""
    
    print("═" * 60)
    print("   🚀 SIMULADOR DE VUELO - CANSAT MISIÓN 2")
    print("═" * 60)
    print(f"\n📍 Ubicación: Aeródromo de Brunete (Madrid)")
    print(f"📅 Fecha: 17 de marzo de 2026, 11:30h")
    print(f"⚖️  Peso CanSat: {MASA_CANSAT * 1000:.0f} g")
    print(f"🪂 Velocidad descenso: {VELOCIDAD_PARACAIDAS} m/s")
    print(f"📏 Altitud lanzamiento: {ALT_LANZAMIENTO} m sobre terreno")
    print(f"🌍 Altitud terreno: {ALT_TERRENO} m sobre nivel del mar")
    print()
    
    # Listas para almacenar datos
    datos = []
    
    # Estado inicial
    altitud = ALT_LANZAMIENTO  # metros sobre terreno
    lat = LAT_LANZAMIENTO
    lon = LON_LANZAMIENTO
    tiempo = 0
    fase = "caida_libre"
    timestamp = FECHA_LANZAMIENTO
    
    # Conversión grados/metro (aproximado para latitud 40°)
    METROS_A_GRADOS_LAT = 1 / 111320
    METROS_A_GRADOS_LON = 1 / (111320 * math.cos(math.radians(lat)))
    
    print("🎬 Iniciando simulación...\n")
    print(f"{'Tiempo':>6} {'Altitud':>8} {'Fase':<15} {'CO2':>6} {'PM2.5':>6}")
    print("-" * 50)
    
    while altitud > 0:
        # Determinar fase y velocidad
        if altitud > ALT_APERTURA_PARACAIDAS:
            fase = "caida_libre"
            velocidad = VELOCIDAD_CAIDA_LIBRE
        elif altitud > ALT_APERTURA_PARACAIDAS - 20:
            fase = "apertura"
            velocidad = VELOCIDAD_PARACAIDAS * 2  # Desaceleración
        else:
            fase = "descenso"
            velocidad = VELOCIDAD_PARACAIDAS
        
        # Calcular nueva altitud
        altitud -= velocidad * INTERVALO_MUESTREO
        altitud += np.random.uniform(-0.5, 0.5)  # Pequeña variación
        altitud = max(0, altitud)
        
        # Deriva por viento
        deriva_norte = VIENTO_NORTE * INTERVALO_MUESTREO * METROS_A_GRADOS_LAT
        deriva_este = VIENTO_ESTE * INTERVALO_MUESTREO * METROS_A_GRADOS_LON
        lat += deriva_norte + np.random.uniform(-0.00001, 0.00001)
        lon += deriva_este + np.random.uniform(-0.00001, 0.00001)
        
        # Altitud sobre nivel del mar (para presión)
        alt_sobre_mar = ALT_TERRENO + altitud
        
        # Calcular sensores
        temp = calcular_temperatura(altitud) + np.random.uniform(-0.3, 0.3)
        hum = calcular_humedad(altitud)
        presion = calcular_presion(alt_sobre_mar) + np.random.uniform(-0.5, 0.5)
        
        # Contaminación
        co2, pm1_0, pm2_5, pm10 = obtener_contaminacion(altitud)
        
        # IMU
        accel, gyro = calcular_imu(fase, velocidad)
        
        # GPS
        sats = np.random.randint(8, 12)
        
        # Guardar registro
        registro = {
            'timestamp': tiempo,
            'datetime': timestamp.isoformat(),
            'lat': round(lat, 6),
            'lon': round(lon, 6),
            'alt': round(altitud, 1),
            'alt_mar': round(alt_sobre_mar, 1),
            'sats': sats,
            'temp': round(temp, 1),
            'hum': round(hum, 1),
            'presion': round(presion, 1),
            'co2': co2,
            'pm1_0': pm1_0,
            'pm2_5': pm2_5,
            'pm10': pm10,
            'accel_x': round(accel[0], 2),
            'accel_y': round(accel[1], 2),
            'accel_z': round(accel[2], 2),
            'gyro_x': round(gyro[0], 1),
            'gyro_y': round(gyro[1], 1),
            'gyro_z': round(gyro[2], 1),
            'fase': fase
        }
        datos.append(registro)
        
        # Mostrar progreso cada 10 segundos
        if tiempo % 10 == 0:
            print(f"{tiempo:>5}s {altitud:>7.1f}m {fase:<15} {co2:>5} {pm2_5:>5}")
        
        # Avanzar tiempo
        tiempo += INTERVALO_MUESTREO
        timestamp += timedelta(seconds=INTERVALO_MUESTREO)
        
        # Detectar aterrizaje
        if altitud <= 0:
            fase = "aterrizaje"
            # Añadir unos segundos en tierra
            for i in range(5):
                tiempo += INTERVALO_MUESTREO
                timestamp += timedelta(seconds=INTERVALO_MUESTREO)
                accel, gyro = calcular_imu("aterrizaje", 0)
                co2, pm1_0, pm2_5, pm10 = obtener_contaminacion(0)
                
                registro = {
                    'timestamp': tiempo,
                    'datetime': timestamp.isoformat(),
                    'lat': round(lat + np.random.uniform(-0.00001, 0.00001), 6),
                    'lon': round(lon + np.random.uniform(-0.00001, 0.00001), 6),
                    'alt': 0,
                    'alt_mar': ALT_TERRENO,
                    'sats': np.random.randint(8, 12),
                    'temp': round(TEMP_SUELO + np.random.uniform(-0.3, 0.3), 1),
                    'hum': round(HUMEDAD_SUELO + np.random.uniform(-2, 2), 1),
                    'presion': round(calcular_presion(ALT_TERRENO), 1),
                    'co2': co2,
                    'pm1_0': pm1_0,
                    'pm2_5': pm2_5,
                    'pm10': pm10,
                    'accel_x': round(accel[0], 2),
                    'accel_y': round(accel[1], 2),
                    'accel_z': round(accel[2], 2),
                    'gyro_x': round(gyro[0], 1),
                    'gyro_y': round(gyro[1], 1),
                    'gyro_z': round(gyro[2], 1),
                    'fase': 'tierra'
                }
                datos.append(registro)
            break
    
    # Crear DataFrame
    df = pd.DataFrame(datos)
    
    # Guardar CSV
    df.to_csv(OUTPUT_FILE, index=False)
    
    # Estadísticas
    print("\n" + "═" * 60)
    print("   📊 RESUMEN DEL VUELO")
    print("═" * 60)
    print(f"\n⏱️  Duración total: {tiempo} segundos ({tiempo/60:.1f} min)")
    print(f"📍 Punto de lanzamiento: {LAT_LANZAMIENTO:.5f}, {LON_LANZAMIENTO:.5f}")
    print(f"🎯 Punto de aterrizaje: {lat:.5f}, {lon:.5f}")
    
    # Distancia recorrida
    dist_lat = (lat - LAT_LANZAMIENTO) / METROS_A_GRADOS_LAT
    dist_lon = (lon - LON_LANZAMIENTO) / METROS_A_GRADOS_LON
    distancia = math.sqrt(dist_lat**2 + dist_lon**2)
    print(f"📏 Distancia horizontal: {distancia:.0f} m")
    
    print(f"\n🌡️  Temperatura: {df['temp'].min():.1f}°C - {df['temp'].max():.1f}°C")
    print(f"💨 CO2: {df['co2'].min()} - {df['co2'].max()} ppm (media: {df['co2'].mean():.0f})")
    print(f"🌫️  PM2.5: {df['pm2_5'].min()} - {df['pm2_5'].max()} µg/m³ (media: {df['pm2_5'].mean():.0f})")
    
    print(f"\n📁 Archivo generado: {OUTPUT_FILE}")
    print(f"   {len(df)} registros guardados")
    
    # Distribución por fases
    print(f"\n🎬 Fases del vuelo:")
    for fase in df['fase'].unique():
        count = len(df[df['fase'] == fase])
        print(f"   • {fase}: {count} muestras ({count}s)")
    
    print("\n" + "═" * 60)
    print("   ✅ SIMULACIÓN COMPLETADA")
    print("═" * 60)
    print(f"\n💡 Siguiente paso:")
    print(f"   python analizar_vuelo.py {OUTPUT_FILE}")
    print()
    
    return df

# ════════════════════════════════════════════════════════════════
# EJECUTAR
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    df = simular_vuelo()
