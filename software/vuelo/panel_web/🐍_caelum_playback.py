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

# === CONFIGURACIÓN ===
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
VELOCIDAD = 1.0  # Un envío por segundo

MAPEO = {
    'lat': 'latitud', 'lon': 'longitud', 'alt': 'altitud',
    'presion': 'presion', 'temp': 'temp', 'co2': 'co2',
    'pm2_5': 'pm2_5', 'pm10': 'pm10',
    'accel_x': 'accelX', 'accel_y': 'accelY', 'accel_z': 'accelZ',
    'gyro_x': 'rotX', 'gyro_z': 'rotZ'
}

def detectar_fichero():
    """Detecta qué fichero existe y elige la ruta Firebase"""
    if os.path.exists("caelum_datos_vuelo.csv"):
        return "caelum_datos_vuelo.csv", "/cansat/replay"
    elif os.path.exists("vuelo_brunete_17marzo.csv"):
        return "vuelo_brunete_17marzo.csv", "/cansat/simulacion"
    else:
        return None, None

def limpiar_firebase(ruta):
    """Borra los datos antiguos para que las gráficas empiecen de cero"""
    try:
        requests.delete(f"{FIREBASE_URL}{ruta}.json")
        print(f"🗑️ Datos anteriores borrados en {ruta}")
    except:
        print("⚠️ No se pudo limpiar Firebase")

def ejecutar_mision():
    archivo, ruta = detectar_fichero()

    if not archivo:
        print("❌ No se detectó ningún archivo (.csv). Sube 'caelum_datos_vuelo.csv' o 'vuelo_brunete_17marzo.csv' a la carpeta de Colab.")
        return

    print(f"🚀 MODO DETECTADO: {ruta.split('/')[-1].upper()}")
    print(f"📂 ARCHIVO: {archivo}")

    limpiar_firebase(ruta)

    with open(archivo, 'r') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Convertimos datos a los nombres que espera el HTML
            payload = {db: (float(fila[csv_col]) if csv_col in fila else 0)
                       for csv_col, db in MAPEO.items()}

            try:
                # Usamos POST para crear historial de datos
                requests.post(f"{FIREBASE_URL}{ruta}.json", json=payload)
                print(f"📡 Enviando a {ruta}: Alt={payload['altitud']}m")
            except:
                print("⚠️ Error de conexión")

            time.sleep(VELOCIDAD)

if __name__ == "__main__":
    ejecutar_mision()
