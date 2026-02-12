# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
# ENTORNO: Thonny / Python Local
# ============================================================================

import serial
import requests
import time
import csv
import os

# --- CONFIGURACIÓN DE COMUNICACIONES ---
PUERTO_SERIAL = 'COM3'  # Cambiar según el puerto asignado por el PC
BAUD_RATE = 9600        # Velocidad de transmisión (Igual que en Arduino)
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app/cansat/telemetria.json"
NOMBRE_ARCHIVO_BACKUP = "respaldo_mision_caelum.csv"

# --- INICIALIZACIÓN DEL ARCHIVO DE RESPALDO (BACKUP) ---
if not os.path.exists(NOMBRE_ARCHIVO_BACKUP):
    with open(NOMBRE_ARCHIVO_BACKUP, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "altitud", "temp", "presion", "co2", "lat", "lon"])

# --- INICIO DE CONEXIÓN SERIAL ---
try:
    arduino = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    print(f"✅ Conectado al receptor en el puerto {PUERTO_SERIAL}")
except:
    print(f"❌ ERROR: Receptor no detectado. Revisa la conexión USB.")
    exit()

print(f"🚀 Grabando respaldo local y transmitiendo a la web...")

while True:
    try:
        # Lectura de la línea enviada por el CanSat
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            datos = linea.split(',')
            ts = time.strftime("%H:%M:%S") # Marca de tiempo real
            
            # Formatear datos para la Base de Datos
            payload = {
                "altitud": float(datos[0]),
                "temp": float(datos[1]),
                "presion": float(datos[2]),
                "co2": float(datos[3]),
                "latitud": float(datos[4]),
                "longitud": float(datos[5]),
                "timestamp": ts
            }

            # 1. GUARDAR EN DISCO DURO (Copia de seguridad)
            with open(NOMBRE_ARCHIVO_BACKUP, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([ts, datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]])

            # 2. SUBIR A LA NUBE (Para el Panel Web)
            try:
                requests.post(FIREBASE_URL, json=payload, timeout=2)
                print(f"📡 [{ts}] -> Firebase Sincronizado | Alt: {datos[0]}m")
            except:
                print(f"⚠️ [{ts}] -> Fallo de Internet (Dato guardado solo en PC)")

    except KeyboardInterrupt:
        print("\n🛑 Recepción detenida por el usuario.")
        break
    except Exception as e:
        print(f"⚠️ Error en procesamiento de datos: {e}")

arduino.close()