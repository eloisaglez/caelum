# ===========================================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Playback de Misión (Simulador desde CSV)
# OBJETIVO: Leer datos históricos de un archivo .csv y enviarlos a Firebase
#           para visualizar la misión en el panel web 3D.
# Ruta Firebase: /cansat/replay/
# Uso: DESPUÉS DEL CONCURSO para revisar vuelos
# ENTORNO: Google Colab
# Fichero: caelum_datos_vuelo.csv (Cargado en colab y generado con receptor_telemetria.py
# ===========================================================================================

"""
CANSAT MISIÓN 2 - Reproductor de Vuelo
Reproduce un CSV grabado hacia Firebase

Ruta Firebase: /cansat/replay/
Uso: DESPUÉS DEL CONCURSO para revisar vuelos

En Colab: Cambiar ARCHIVO_CSV y ejecutar
En terminal: python reproductor_replay.py
"""

import requests
import time
import csv

# ============================================
# CONFIGURACIÓN - CAMBIAR AQUÍ
# ============================================

ARCHIVO_CSV = "caelum_datos_vuelo.csv"  
VELOCIDAD = 1.0  # 1.0 = real | 0.5 = rápido | 2.0 = lento

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
RUTA_DATOS = "/cansat/replay"

CABECERA = ['timestamp', 'datetime', 'lat', 'lon', 'alt', 'alt_mar', 'sats', 
            'temp', 'hum', 'presion', 'co2', 'pm1_0', 'pm2_5', 'pm10', 
            'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'fase']

def limpiar_firebase():
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA_DATOS}.json")
        print("🗑️ Replay anterior borrado")
    except:
        pass

def reproducir():
    print("=" * 50)
    print("⏪ REPRODUCTOR → /cansat/replay/")
    print("=" * 50)
    print(f"📂 Archivo: {ARCHIVO_CSV}")
    print(f"⏱️ Velocidad: {VELOCIDAD}x")
    print("=" * 50)
    
    limpiar_firebase()
    contador = 0
    
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            lector = csv.DictReader(f)
            
            print("\n▶️ Reproduciendo...\n")
            
            for fila in lector:
                contador += 1
                
                payload = {}
                for campo in CABECERA:
                    if campo in fila:
                        try:
                            v = fila[campo]
                            payload[campo] = float(v) if '.' in str(v) else int(v)
                        except:
                            payload[campo] = fila[campo]
                
                try:
                    url = f"{FIREBASE_URL}{RUTA_DATOS}/{int(time.time()*1000)}.json"
                    requests.put(url, json=payload, timeout=1)
                    print(f"📡 [{contador:4d}] Alt={payload.get('alt',0):6.1f}m | "
                          f"CO2={payload.get('co2',0)}ppm | PM2.5={payload.get('pm2_5',0)}µg/m³")
                except:
                    print(f"⚠️ [{contador:4d}] Error conexión")
                
                time.sleep(VELOCIDAD)
        
        print(f"\n✅ Completado: {contador} paquetes")
        print("🌐 Panel: https://cansat-66d98.web.app (modo Replay)")
        
    except FileNotFoundError:
        print(f"❌ No existe: {ARCHIVO_CSV}")
        print("   Sube el archivo a Colab primero")
    except KeyboardInterrupt:
        print(f"\n⚠️ Pausado en paquete {contador}")

# Ejecutar
reproducir()
