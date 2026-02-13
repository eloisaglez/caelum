"""
# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
# Recibe datos del APC220 por puerto COM
# Guarda en CSV + envía a Firebase
# Ruta Firebase: /cansat/telemetria/
# Uso: DÍA DEL CONCURSO
# # ============================================================================
"""

import serial
import csv
import requests
import time
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================

PUERTO_SERIAL = 'COM3'  # Cambiar según tu puerto
BAUDIOS = 9600
ARCHIVO_CSV = "caelum_datos_vuelo.csv"

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
RUTA_DATOS = "/cansat/telemetria"

# Orden de campos que envía el CanSat
CABECERA = ['timestamp', 'datetime', 'lat', 'lon', 'alt', 'alt_mar', 'sats', 
            'temp', 'hum', 'presion', 'co2', 'pm1_0', 'pm2_5', 'pm10', 
            'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'fase']

def limpiar_firebase():
    """Borra datos anteriores"""
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA_DATOS}.json")
        print("🗑️ Telemetría anterior borrada")
    except:
        pass

def parsear_linea(linea):
    """Convierte línea CSV en diccionario"""
    datos = linea.split(',')
    if len(datos) < 10:
        return None
    
    payload = {}
    for i, campo in enumerate(CABECERA):
        if i < len(datos):
            try:
                valor = datos[i].strip()
                if '.' in valor:
                    payload[campo] = float(valor)
                else:
                    payload[campo] = int(valor)
            except:
                payload[campo] = datos[i].strip()
    return payload

def main():
    print("=" * 60)
    print("🛰️ RECEPTOR TELEMETRÍA → /cansat/telemetria/")
    print("=" * 60)
    print(f"📡 Puerto: {PUERTO_SERIAL}")
    print(f"💾 CSV: {ARCHIVO_CSV}")
    print("=" * 60)
    
    limpiar_firebase()
    contador = 0
    
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        print("\n⏳ Esperando datos del CanSat...\n")
        
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            escritor = csv.writer(f)
            escritor.writerow(CABECERA)
            
            while True:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if linea:
                    # Guardar en CSV
                    escritor.writerow(linea.split(','))
                    f.flush()
                    
                    # Enviar a Firebase
                    payload = parsear_linea(linea)
                    if payload:
                        contador += 1
                        try:
                            url = f"{FIREBASE_URL}{RUTA_DATOS}/{int(time.time()*1000)}.json"
                            requests.put(url, json=payload, timeout=0.5)
                            print(f"📡 [{contador:4d}] Alt={payload.get('alt',0):6.1f}m | "
                                  f"CO2={payload.get('co2',0)}ppm | PM2.5={payload.get('pm2_5',0)}µg/m³ ✅")
                        except:
                            print(f"📡 [{contador:4d}] ⚠️ Firebase offline (CSV guardado)")
    
    except serial.SerialException as e:
        print(f"❌ Error puerto: {e}")
        print(f"   Verifica: {PUERTO_SERIAL}")
    except KeyboardInterrupt:
        print(f"\n\n🛑 RECEPCIÓN FINALIZADA")
        print(f"   ✅ Paquetes: {contador}")
        print(f"   💾 Guardado: {ARCHIVO_CSV}")

if __name__ == "__main__":
    main()
