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

# Instalación automática de librerías
for p in ["requests", "pyserial"]:
    try: __import__(p)
    except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", p])

import serial, requests

# === CONFIGURACIÓN ===
MODO = "CONCURSO"  # Cambia a "PRUEBAS" si solo estás testeando
PUERTO_SERIAL = 'COM3' 
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

RUTA = "/cansat/telemetria" if MODO == "CONCURSO" else "/cansat/pruebas"
ARCHIVO_CSV = "caelum_datos_vuelo.csv" if MODO == "CONCURSO" else None

def ejecutar():
    print(f"🛰️ EJECUTANDO {MODO}...")
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA}.json") # Limpia Firebase
        ser = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
        while True:
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                d = linea.split(',')
                if len(d) >= 21: # Esperamos los 21 campos del README
                    payload = {
                        "lat": float(d[2]), "lon": float(d[3]), "alt": float(d[4]),
                        "presion": float(d[9]), "temp": float(d[7]), "co2": float(d[10]),
                        "pm2_5": float(d[12]), "pm10": float(d[13]),
                        "accel_x": float(d[14]), "accel_y": float(d[15]), "accel_z": float(d[16]),
                        "gyro_x": float(d[17]), "gyro_z": float(d[19]),
                        "sats": int(d[6]), "fase": d[20]
                    }
                    requests.post(f"{FIREBASE_URL}{RUTA}.json", json=payload)
                    if ARCHIVO_CSV:
                        with open(ARCHIVO_CSV, 'a', newline='') as f:
                            w = csv.DictWriter(f, fieldnames=payload.keys())
                            if f.tell() == 0: w.writeheader()
                            w.writerow(payload)
                    print(f"🚀 Enviado: Alt {payload['alt']}m")
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == "__main__": ejecutar()
