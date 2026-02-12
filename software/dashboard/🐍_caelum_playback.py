# ===========================================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Playback de Misión (Simulador desde CSV)
# OBJETIVO: Leer datos históricos de un archivo .csv y enviarlos a Firebase
#           para visualizar la misión en el panel web 3D.
# ENTORNO: Google Colab
# Fichero: vuelo_brunete_17marzo.csv (Cargado en colab y generado con dimulador_vuelo.py
# ===========================================================================================
import requests
import time
import pandas as pd
import io

# 1. Configuración
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app/cansat/test_local.json"
FILE_NAME = 'vuelo_brunete_17marzo.csv'

def reproducir_mision_real():
    try:
        # Leer el archivo CSV que generamos antes
        df = pd.read_csv(FILE_NAME)
        print(f"✅ Archivo cargado: {len(df)} registros encontrados.")
        print("🚀 Iniciando reproducción de misión real en el Panel Web...")

        for index, row in df.iterrows():
            # Mapeamos los nombres del CSV a los que espera el HTML
            payload = {
                "timestamp": int(row.get('timestamp', index)),
                "altitud": float(row.get('alt', 0)),
                "temp": float(row.get('temp', 0)),
                "presion": float(row.get('presion', 1013)), # Si no hay, usa base 1013
                "co2": float(row.get('co2', 400)),
                "pm2_5": float(row.get('pm2_5', 0)),
                "pm10": float(row.get('pm10', 0)),
                "latitud": float(row.get('lat', 40.4052)),
                "longitud": float(row.get('lon', -3.9931)),
                # Generamos rotación simulada para el 3D ya que el CSV no tiene giroscopio
                "rotX": (index * 5) % 360,
                "rotY": (index * 2) % 360,
                "rotZ": (index * 1) % 45,
                "accelX": 0, "accelY": 0, "accelZ": 9.8
            }

            # Enviar a Firebase
            try:
                # Usamos el índice como clave para que se ordene correctamente
                requests.patch(FIREBASE_URL, json={str(index): payload})
                print(f"Replica Seg {index} | Alt: {payload['altitud']}m | CO2: {payload['co2']}ppm -> OK")
            except:
                print("❌ Error de conexión")

            # Esperar 1 segundo para que la animación sea realista
            time.sleep(1)

        print("🏁 Fin de la reproducción.")

    except FileNotFoundError:
        print(f"❌ Error: No se encuentra el archivo {FILE_NAME}. Asegúrate de subirlo a Colab.")

reproducir_mision_real()
