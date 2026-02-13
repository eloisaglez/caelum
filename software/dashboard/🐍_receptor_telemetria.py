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
import serial
import requests
import time

# =========================================================
# CONFIGURACIÓN: CAMBIA ESTO SEGÚN LO QUE ESTÉS HACIENDO
# =========================================================
MODO = "CONCURSO"  # <--- Escribir "CONCURSO" o "PRUEBAS"
PUERTO_SERIAL = 'COM3' # <--- Mirar  a qué puerto se ha conectado
# =========================================================

BAUDIOS = 9600
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

# Selección de ruta automática
if MODO == "CONCURSO":
    RUTA = "/cansat/telemetria"
else:
    RUTA = "/cansat/pruebas"

def capturar():
    print(f"📡 SISTEMA INICIADO EN MODO: {MODO}")
    print(f"📂 GUARDANDO EN: {RUTA}")
    
    try:
        # Esto limpia los datos viejos para que el HTML no se líe
        requests.delete(f"{FIREBASE_URL}{RUTA}.json")
        print("🗑️ Memoria de Firebase limpiada.")
        
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        print(f"✅ Conectado al CanSat en {PUERTO_SERIAL}. Esperando datos...")
        
        while True:
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                datos = linea.split(',')
                # Verificamos que lleguen los 13 datos (ajusta si mandas más o menos)
                if len(datos) >= 13:
                    payload = {
                        "latitud": float(datos[0]), "longitud": float(datos[1]),
                        "altitud": float(datos[2]), "presion": float(datos[3]),
                        "temp": float(datos[4]), "co2": float(datos[5]),
                        "pm2_5": float(datos[6]), "pm10": float(datos[7]),
                        "accelX": float(datos[8]), "accelY": float(datos[9]),
                        "accelZ": float(datos[10]), "rotX": float(datos[11]),
                        "rotZ": float(datos[12])
                    }
                    # ENVIAR A FIREBASE
                    requests.post(f"{FIREBASE_URL}{RUTA}.json", json=payload)
                    print(f"🚀 ENVIADO -> Altitud: {payload['altitud']}m | Temp: {payload['temp']}ºC")
                else:
                    print(f"⚠️ Trama incompleta: recibidos {len(datos)} valores.")
                    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("CONSEJO: Revisa si el cable USB está bien conectado o si el puerto COM es el correcto.")

if __name__ == "__main__":
    capturar()
