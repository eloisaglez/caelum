"""
# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
# Recibe datos del APC220 por puerto COM
# Guarda en CSV + envía a Firebase
# # ============================================================================
"""
import os, subprocess, sys, time, csv

# Autoinstalación de paquetes
def preparar_entorno():
    for p in ["requests", "pyserial"]:
        try: __import__(p)
        except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", p])

preparar_entorno()
import serial, requests
# =========================================================
# CONFIGURACIÓN: CAMBIA ESTO SEGÚN LO QUE ESTÉS HACIENDO
# =========================================================
MODO = "CONCURSO"  # <--- Escribir "CONCURSO" o "PRUEBAS"
PUERTO_SERIAL = 'COM3' # <--- Mirar  a qué puerto se ha conectado
# =========================================================

# === CONFIGURACIÓN ===
MODO = "CONCURSO"  # Cambiar a "PRUEBAS" para testear sensores
PUERTO_SERIAL = 'COM3' 
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

RUTA = "/cansat/telemetria" if MODO == "CONCURSO" else "/cansat/pruebas"
ARCHIVO_CSV = "caelum_datos_vuelo.csv" if MODO == "CONCURSO" else None

def ejecutar():
    print(f"📡 INICIANDO: {MODO} -> {RUTA}")
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA}.json") # Limpiar datos viejos
        ser = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
        
        while True:
            linea = ser.readline().decode('utf-8').strip()
            if linea and len(linea.split(',')) >= 13:
                d = linea.split(',')
                payload = {
                    "lat": float(d[0]), "lon": float(d[1]), "alt": float(d[2]),
                    "presion": float(d[3]), "temp": float(d[4]), "co2": float(d[5]),
                    "pm2_5": float(d[6]), "pm10": float(d[7]),
                    "accel_x": float(d[8]), "accel_y": float(d[9]), "accel_z": float(d[10]),
                    "gyro_x": float(d[11]), "gyro_z": float(d[12])
                }
                requests.post(f"{FIREBASE_URL}{RUTA}.json", json=payload)
                if ARCHIVO_CSV:
                    with open(ARCHIVO_CSV, 'a', newline='') as f:
                        w = csv.DictWriter(f, fieldnames=payload.keys())
                        if f.tell() == 0: w.writeheader()
                        w.writerow(payload)
                print(f"📡 Alt: {payload['alt']}m | Temp: {payload['temp']}°C")
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == "__main__": ejecutar()
