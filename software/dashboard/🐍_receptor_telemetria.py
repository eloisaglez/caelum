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
import requests
import time

# === CONFIGURACIÓN ===
PUERTO_SERIAL = 'COM3' # En Windows suele ser COM3, COM4... En Mac/Linux /dev/ttyUSB0
BAUDIOS = 9600
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

# Carpeta de destino (Cámbiala a 'telemetria_pruebas' si estás testeando)
CARPETA = "telemetria" 

def leer_puerto_serie():
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        print(f"✅ Conectado al puerto {PUERTO_SERIAL}")
        
        while True:
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                # Suponiendo que el Arduino manda: lat,lon,alt,presion,temp,co2,pm25,pm10,ax,ay,az,gx,gz
                datos = linea.split(',')
                
                if len(datos) >= 13: # Asegúrate de que coincida con el número de datos que envías
                    payload = {
                        "latitud": float(datos[0]),
                        "longitud": float(datos[1]),
                        "altitud": float(datos[2]),
                        "presion": float(datos[3]),
                        "temp": float(datos[4]),
                        "co2": float(datos[5]),
                        "pm2_5": float(datos[6]),
                        "pm10": float(datos[7]),
                        "accelX": float(datos[8]),
                        "accelY": float(datos[9]),
                        "accelZ": float(datos[10]),
                        "rotX": float(datos[11]),
                        "rotZ": float(datos[12])
                    }
                    
                    requests.post(f"{FIREBASE_URL}/cansat/{CARPETA}.json", json=payload)
                    print(f"📡 DATO REAL ENVIADO -> Alt: {payload['altitud']}m")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    leer_puerto_serie()

