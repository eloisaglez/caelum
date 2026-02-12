# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del puerto serie (Radio/USB), subirlos a la nube
#           y generar un respaldo local en formato CSV.
#           Recibir 15 parámetros, enviar 14 (sin la humedad) a la web y guardar 15 en el CSV.
# ENTORNO: Thonny / Python Local
# ============================================================================

# ============================================================================
# PROYECTO: CANSAT CAELUM 
# PROGRAMA: caelum_ground_station.py
# OBJETIVO: 
# ============================================================================
import serial, requests, time, csv, os

PUERTO_SERIAL = 'COM3' # <--- ¡REVISAR EN EL LANZAMIENTO!
BAUD_RATE = 9600
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app/cansat/telemetria.json"
ARCHIVO_CSV = "mision_caelum_full_backup.csv"

# Cabecera con 15 columnas de datos + timestamp
if not os.path.exists(ARCHIVO_CSV):
    with open(ARCHIVO_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ts","alt","temp","pres","co2","lat","lon","pm25","pm10","ax","ay","az","rx","ry","rz","hum"])

try:
    ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    print(f"✅ Recepción activa en {PUERTO_SERIAL}")
except:
    print("❌ ERROR: Receptor no encontrado."); exit()

while True:
    try:
        linea = ser.readline().decode('utf-8').strip()
        if linea:
            datos = linea.split(',')
            
            if len(datos) >= 15: # Verificamos que lleguen todos los datos
                ts = time.strftime("%H:%M:%S")
                
                # Payload para la web (mantenemos los 14 originales para no romper el HTML)
                payload = {
                    "altitud": float(datos[0]), "temp": float(datos[1]), "presion": float(datos[2]),
                    "co2": float(datos[3]), "latitud": float(datos[4]), "longitud": float(datos[5]),
                    "pm2_5": float(datos[6]), "pm10": float(datos[7]),
                    "accelX": float(datos[8]), "accelY": float(datos[9]), "accelZ": float(datos[10]),
                    "rotX": float(datos[11]), "rotY": float(datos[12]), "rotZ": float(datos[13]),
                    "timestamp": ts
                    # Nota: No enviamos "humedad" a Firebase para no saturar la red, 
                    # ya que el HTML no la está buscando.
                }

                # RESPALDO TOTAL (Aquí sí guardamos la humedad: datos[14])
                with open(ARCHIVO_CSV, 'a', newline='') as f:
                    csv.writer(f).writerow([ts] + datos)

                try:
                    requests.post(FIREBASE_URL, json=payload, timeout=1)
                    print(f"📡 {ts} | Web OK | Backup OK (15 campos)")
                except:
                    print(f"⚠️ {ts} | Error WiFi | Backup OK")
    except Exception as e:
        print(f"⚠️ Error: {e}")
