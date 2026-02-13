# ===========================================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Playback de Misión (Simulador desde CSV)
# OBJETIVO: Leer datos históricos de un archivo .csv y enviarlos a Firebase
#           para visualizar la misión en el panel web 3D.
# Ruta Firebase: /cansat/replay/
# Uso: DESPUÉS DEL CONCURSO para revisar vuelos
# ENTORNO: Google Colab
# Detecta automáticamente:
#  - caelum_datos_vuelo.csv → /cansat/replay/ (datos del concurso)
#  - vuelo_brunete_17marzo.csv → /cansat/simulacion/ (datos de simlación)
#
# ===========================================================================================

import requests
import time
import csv
import os

# ============================================
# CONFIGURACIÓN
# ============================================

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
VELOCIDAD = 1.0  # 1.0 = real | 0.5 = rápido | 2.0 = lento

CABECERA = ['timestamp', 'datetime', 'lat', 'lon', 'alt', 'alt_mar', 'sats', 
            'temp', 'hum', 'presion', 'co2', 'pm1_0', 'pm2_5', 'pm10', 
            'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'fase']

# ============================================
# DETECCIÓN AUTOMÁTICA DE FICHERO
# ============================================

def detectar_fichero():
    """Detecta qué fichero existe y elige la ruta Firebase"""
    
    if os.path.exists("caelum_datos_vuelo.csv"):
        return "caelum_datos_vuelo.csv", "/cansat/replay"
    elif os.path.exists("vuelo_brunete_17marzo.csv"):
        return "vuelo_brunete_17marzo.csv", "/cansat/simulacion"
    else:
        return None, None

def limpiar_firebase(ruta):
    try:
        requests.delete(f"{FIREBASE_URL}{ruta}.json")
        print("🗑️ Datos anteriores borrados")
    except:
        pass

def reproducir():
    # Detectar fichero
    archivo, ruta = detectar_fichero()
    
    if archivo is None:
        print("❌ No se encontró ningún fichero:")
        print("   - caelum_datos_vuelo.csv (concurso)")
        print("   - vuelo_brunete_17marzo.csv (simulación)")
        print("\n   Sube uno de estos archivos a Colab")
        return
    
    print("=" * 50)
    print(f"⏪ REPRODUCTOR → {ruta}/")
    print("=" * 50)
    print(f"📂 Archivo: {archivo}")
    print(f"⏱️ Velocidad: {VELOCIDAD}x")
    print("=" * 50)
    
    limpiar_firebase(ruta)
    contador = 0
    
    try:
        with open(archivo, 'r') as f:
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
                    url = f"{FIREBASE_URL}{ruta}/{int(time.time()*1000)}.json"
                    requests.put(url, json=payload, timeout=1)
                    print(f"📡 [{contador:4d}] Alt={payload.get('alt',0):6.1f}m | "
                          f"CO2={payload.get('co2',0)}ppm | PM2.5={payload.get('pm2_5',0)}µg/m³")
                except:
                    print(f"⚠️ [{contador:4d}] Error conexión")
                
                time.sleep(VELOCIDAD)
        
        print(f"\n✅ Completado: {contador} paquetes")
        print(f"🌐 Panel: https://cansat-66d98.web.app")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Pausado en paquete {contador}")

# Ejecutar
reproducir()
