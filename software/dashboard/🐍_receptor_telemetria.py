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

# AUTOINSTALACIÓN DE LIBRERÍAS (Para evitar el error de ModuleNotFoundError)
def preparar_entorno():
    paquetes = ["requests", "pyserial"]
    for p in paquetes:
        try:
            __import__(p)
        except ImportError:
            print(f"📦 Instalando {p}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])

preparar_entorno()
import serial, requests

# === CONFIGURACIÓN (Actualizada según README) ===
MODO = "CONCURSO"  # Cambiar a "PRUEBAS" para testear
PUERTO_SERIAL = 'COM3' 
BAUDIOS = 9600
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

# Selección de ruta y archivo según el modo
RUTA = "/cansat/telemetria" if MODO == "CONCURSO" else "/cansat/pruebas"
ARCHIVO_CSV = "caelum_datos_vuelo.csv" if MODO == "CONCURSO" else None

def ejecutar():
    print(f"📡 MOTOR PC INICIADO: {MODO} -> {RUTA}")
    try:
        # Limpiar datos antiguos para que el HTML empiece de cero
        requests.delete(f"{FIREBASE_URL}{RUTA}.json")
        
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        print(f"✅ Conectado al CanSat. Esperando trama de datos...")

        while True:
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                d = linea.split(',')
                # Verificamos que la trama tenga los campos definidos en el README
                if len(d) >= 21:
                    payload = {
                        "timestamp": int(d[0]),
                        "datetime": d[1],
                        "lat": float(d[2]),
                        "lon": float(d[3]),
                        "alt": float(d[4]),
                        "alt_mar": float(d[5]),
                        "sats": int(d[6]),
                        "temp": float(d[7]),
                        "hum": float(d[8]),
                        "presion": float(d[9]),
                        "co2": float(d[10]),
                        "pm1_0": float(d[11]),
                        "pm2_5": float(d[12]),
                        "pm10": float(d[13]),
                        "accel_x": float(d[14]),
                        "accel_y": float(d[15]),
                        "accel_z": float(d[16]),
                        "gyro_x": float(d[17]),
                        "gyro_y": float(d[18]),
                        "gyro_z": float(d[19]),
                        "fase": d[20]
                    }
                    
                    # Envío a Firebase
                    requests.post(f"{FIREBASE_URL}{RUTA}.json", json=payload)
                    
                    # Guardado en CSV (Solo en modo CONCURSO)
                    if ARCHIVO_CSV:
                        existe = os.path.isfile(ARCHIVO_CSV)
                        with open(ARCHIVO_CSV, 'a', newline='') as f:
                            w = csv.DictWriter(f, fieldnames=payload.keys())
                            if not existe: w.writeheader()
                            w.writerow(payload)
                    
                    print(f"🚀 {payload['fase'].upper()} | Alt: {payload['alt']}m | Sats: {payload['sats']}")
                else:
                    print(f"⚠️ Trama incompleta ({len(d)}/21 campos). Revisa el código del Arduino.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar()
