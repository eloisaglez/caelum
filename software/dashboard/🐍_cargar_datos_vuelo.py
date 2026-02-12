import requests
import time
import csv

# === CONFIGURACIÓN REPETICIÓN ===
ARCHIVO_A_LEER = "datos_vuelo.csv" 
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app/cansat/telemetria.json"
VELOCIDAD = 1.0 # 1.0 = tiempo real | 0.5 = doble de rápido

def reproducir_vuelo():
    print(f"⏪ Reproduciendo misión real: {ARCHIVO_A_LEER}")
    try:
        with open(ARCHIVO_A_LEER, mode='r') as fichero:
            lector = csv.DictReader(fichero)
            for fila in lector:
                try:
                    requests.post(FIREBASE_URL, json=fila, timeout=1)
                    print(f"✅ Reenviado: {fila.get('ts', 'S/N')}")
                except:
                    print("⚠️ Error de conexión")
                time.sleep(VELOCIDAD)
    except FileNotFoundError:
        print(f"❌ No se encuentra {ARCHIVO_A_LEER}")
    except KeyboardInterrupt:
        print("\n🛑 Reproducción pausada.")

if __name__ == "__main__":
    reproducir_vuelo()
