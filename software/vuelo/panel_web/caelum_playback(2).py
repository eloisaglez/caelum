# ===========================================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Playback de Misión v2 (Simulador desde CSV)
# OBJETIVO: Leer datos históricos de un archivo .csv y enviarlos a Firebase
#           para visualizar la misión en el panel web 3D.
#
# RUTAS FIREBASE:
#   datos_SD.csv        → /cansat/replay/    (datos reales del concurso)
#   datos_simulacion.csv  → /cansat/simulacion/ (datos de simulación)
#
# CAMPOS CSV (25 columnas):
#   timestamp, datetime, lat, lon, alt, alt_mar, sats,
#   temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
#   co2, pm1_0, pm2_5, pm10,
#   accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase
#
# NOTA: Los campos se envían a Firebase con los mismos nombres que en el CSV.
#       El dashboard los lee directamente sin renombrar.
#
# ENTORNO: Google Colab o PC local
# ===========================================================================================

import requests
import time
import csv
import os

# === CONFIGURACIÓN ===
FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
VELOCIDAD    = 1.0   # segundos entre envíos (1.0 = tiempo real)

# Campos numéricos del CSV — se convierten a float al enviar
CAMPOS_NUMERICOS = {
    'timestamp', 'lat', 'lon', 'alt', 'alt_mar', 'sats',
    'temp_hs', 'hum_hs', 'temp_scd', 'hum_scd', 'temp_lps', 'presion',
    'co2', 'pm1_0', 'pm2_5', 'pm10',
    'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'
}
# Campos de texto — se envían tal cual
CAMPOS_TEXTO = {'datetime', 'fase'}

def detectar_fichero():
    """Detecta qué fichero existe y elige la ruta Firebase correspondiente."""
    if os.path.exists("datos_SD.csv"):
        return "datos_SD.csv", "/cansat/replay"
    elif os.path.exists("datos_simulacion.csv"):
        return "datos_simulacion.csv", "/cansat/simulacion"
    else:
        return None, None

def limpiar_firebase(ruta):
    """Borra datos anteriores por lotes para evitar el límite de tamaño de Firebase."""
    try:
        r = requests.get(f"{FIREBASE_URL}{ruta}.json?shallow=true", timeout=10)
        claves = r.json()
        if not claves:
            print(f"🗑️  {ruta} ya estaba vacío")
        else:
            print(f"🗑️  Borrando {len(claves)} entradas en {ruta}...")
            for i, clave in enumerate(claves):
                requests.delete(f"{FIREBASE_URL}{ruta}/{clave}.json", timeout=10)
                if i % 20 == 0 and i > 0:
                    print(f"   {i}/{len(claves)} borradas...")
            print(f"🗑️  Limpieza completada ({len(claves)} entradas borradas)")
    except Exception as e:
        print(f"⚠️  No se pudo limpiar Firebase: {e}")

def construir_payload(fila):
    """
    Construye el payload para Firebase con los mismos nombres que el CSV.
    No renombra campos — el dashboard los lee directamente.
    """
    payload = {}
    for campo, valor in fila.items():
        campo = campo.strip()
        if campo in CAMPOS_NUMERICOS:
            try:
                payload[campo] = float(valor)
            except (ValueError, TypeError):
                payload[campo] = 0.0
        elif campo in CAMPOS_TEXTO:
            payload[campo] = str(valor).strip()
    return payload

def ejecutar_mision():
    archivo, ruta = detectar_fichero()

    if not archivo:
        print("❌ No se detectó ningún archivo CSV.")
        print("   Sube 'datos_SD.csv' o 'datos_simulacion.csv'")
        return

    modo = ruta.split('/')[-1].upper()
    print(f"\n{'═'*55}")
    print(f"   🚀 CANSAT CAELUM — PLAYBACK v2")
    print(f"{'═'*55}")
    print(f"   Modo:    {modo}")
    print(f"   Archivo: {archivo}")
    print(f"   Ruta FB: {ruta}")
    print(f"   Vel.:    {VELOCIDAD}s por muestra")
    print(f"{'═'*55}\n")

    limpiar_firebase(ruta)

    with open(archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        filas  = list(lector)

    total = len(filas)
    print(f"📂 {total} filas cargadas. Iniciando envío...\n")

    for i, fila in enumerate(filas):
        payload = construir_payload(fila)

        try:
            # PUT con timestamp como clave → sobrescribe el último dato (el dashboard
            # usa limitToLast(1), así que siempre muestra el dato más reciente)
            ts  = int(payload.get('timestamp', i))
            url = f"{FIREBASE_URL}{ruta}/{ts}.json"
            r   = requests.put(url, json=payload, timeout=10)

            alt  = payload.get('alt',  0)
            fase = payload.get('fase', '—')
            co2  = payload.get('co2',  0)
            pm25 = payload.get('pm2_5', 0)
            t_hs = payload.get('temp_hs', 0)
            t_sc = payload.get('temp_scd', 0)

            status = "✅" if r.status_code == 200 else f"⚠️ {r.status_code}"
            print(f"[{i+1:>3}/{total}] {status}  Alt={alt:>6.1f}m  "
                  f"Fase={fase:<12}  CO₂={co2:>4.0f}ppm  "
                  f"PM2.5={pm25:>5.1f}  T_HS={t_hs:.1f}°C  T_SCD={t_sc:.1f}°C")

        except Exception as e:
            print(f"[{i+1:>3}/{total}] ⚠️  Error de conexión: {e}")

        time.sleep(VELOCIDAD)

    print(f"\n{'═'*55}")
    print(f"   ✅ PLAYBACK COMPLETADO — {total} muestras enviadas")
    print(f"   Ruta Firebase: {ruta}")
    print(f"{'═'*55}\n")

if __name__ == "__main__":
    ejecutar_mision()
