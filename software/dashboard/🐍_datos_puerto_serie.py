# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
# ENTORNO: Thonny / Python Local
# ============================================================================

import serial
import csv
import requests
import time

# === CONFIGURACIÓN ===
PUERTO_SERIAL = 'COM3'  # Cambiar según el puerto del receptor
BAUDIOS = 9600
ARCHIVO_CSV = "datos_vuelo.csv"
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app/cansat/telemetria.json"

def iniciar_estacion_tierra():
    print(f"🚀 CAELUM Ground Station: Escuchando en {PUERTO_SERIAL}...")
    
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        
        # Abrimos el archivo para escribir los datos del concurso
        with open(ARCHIVO_CSV, mode='a', newline='') as fichero:
            escritor = csv.writer(fichero)
            
            # Si el archivo está vacío, podrías escribir la cabecera aquí:
            # escritor.writerow(['ts', 'alt', 'temp', 'pres', 'co2', 'lat', 'lon', 'pm25', 'pm10', 'ax', 'ay', 'az', 'rx', 'ry', 'rz'])

            while True:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if linea:
                    datos = linea.split(',')
                    escritor.writerow(datos)
                    
                    # --- SEGURIDAD CAELUM ---
                    # 'flush' obliga a Windows a guardar el dato en el disco duro al instante.
                    # Si el PC se cuelga, los datos del vuelo NO se pierden.
                    fichero.flush() 
                    
                    # Envío a Firebase para el Dashboard en tiempo real
                    try:
                        # Estructura de ejemplo (ajustar según vuestro orden de sensores)
                        payload = {"alt": datos[1], "temp": datos[2], "ts": datos[0]}
                        requests.post(FIREBASE_URL, json=payload, timeout=0.5)
                    except:
                        pass # Si falla el WiFi, el CSV sigue guardando todo
                    
                    print(f"📡 Recibido: {linea}")

    except KeyboardInterrupt:
        print("\n🛑 Detención manual. Cerrando puerto y guardando archivo...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("✅ Fichero 'datos_vuelo.csv' cerrado correctamente.")

if __name__ == "__main__":
    iniciar_estacion_tierra()
