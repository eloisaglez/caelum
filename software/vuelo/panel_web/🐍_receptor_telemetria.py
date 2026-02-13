"""
# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
# Recibe datos del APC220 por puerto COM
# Guarda en CSV + envía a Firebase
# MODO = "CONCURSO"  # Cambiar a "PRUEBAS" si se está testeando
# PUERTO_SERIAL = 'COM3' # Verificar APC220 está en el COM3 si no cambiar
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
PUERTO_SERIAL = 'COM3' # Verificar APC220 está en el COM3 sino cambiar
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

RUTA = "/cansat/telemetria" if MODO == "CONCURSO" else "/cansat/pruebas"
ARCHIVO_CSV = "caelum_datos_vuelo.csv" if MODO == "CONCURSO" else "pruebas_sensores.csv"

def ejecutar():
    print(f"🛰️ INICIANDO ESTACIÓN DE TIERRA - MODO: {MODO}")
    print(f"📡 ESCUCHANDO EN {PUERTO_SERIAL}...")
    
    try:
        # Limpia datos antiguos al empezar para que las gráficas empiecen de cero
        requests.delete(f"{FIREBASE_URL}{RUTA}.json") 
        
        ser = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
        
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                d = linea.split(',')
                # Verificamos que la línea tenga datos (al menos 20 campos)
                if len(d) >= 20: 
                    try:
                        # === SINCRONIZACIÓN TOTAL CON EL HTML ===
                        # Mapeamos los campos del Serial (d[index]) a los nombres largos del Dashboard
                        payload = {
                            "latitud": float(d[2]), 
                            "longitud": float(d[3]), 
                            "altitud": float(d[4]),
                            "presion": float(d[9]), 
                            "temp": float(d[7]), 
                            "co2": float(d[10]),
                            "pm2_5": float(d[12]), 
                            "pm10": float(d[13]),
                            "accelX": float(d[14]), 
                            "accelY": float(d[15]), 
                            "accelZ": float(d[16]),
                            "rotX": float(d[17]), 
                            "rotZ": float(d[19]),
                            "sats": int(d[6]), 
                            "fase": d[20] if len(d) > 20 else "VUELO"
                        }
                        
                        # Enviar a Firebase
                        requests.post(f"{FIREBASE_URL}{RUTA}.json", json=payload)
                        
                        # Guardar copia local en CSV
                        with open(ARCHIVO_CSV, 'a', newline='') as f:
                            w = csv.DictWriter(f, fieldnames=payload.keys())
                            if f.tell() == 0: w.writeheader()
                            w.writerow(payload)
                        
                        print(f"✅ Recibido: Alt {payload['altitud']}m | CO2: {payload['co2']} | Sat: {payload['sats']}")
                        
                    except (ValueError, IndexError) as e:
                        print(f"⚠️ Error procesando línea: {linea} ({e})")
                        
    except serial.SerialException:
        print(f"❌ ERROR: No se pudo abrir el puerto {PUERTO_SERIAL}. ¿Está conectado el APC220?")
    except KeyboardInterrupt:
        print("\n🛑 Estación de tierra detenida.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__": 
    ejecutar()
