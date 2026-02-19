"""
# ============================================================================
# PROYECTO: CANSAT CAELUM (IES DIEGO VELÁZQUEZ)
# PROGRAMA: Estación de Tierra v2 (Telemetría en Tiempo Real)
# OBJETIVO: Leer datos del APC220 por puerto serie, subirlos a Firebase
#           y guardar respaldo local en CSV.
#
# MODO = "CONCURSO"  → envía a /cansat/telemetria, guarda caelum_datos_vuelo.csv
# MODO = "PRUEBAS"   → envía a /cansat/pruebas,    guarda pruebas_sensores.csv
#
# FORMATO CSV RECIBIDO (25 campos, misma cabecera que genera el Arduino):
#   timestamp, datetime, lat, lon, alt, alt_mar, sats,
#   temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
#   co2, pm1_0, pm2_5, pm10,
#   accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase
#
# NOTA: Los campos se envían a Firebase con los MISMOS nombres que el CSV.
#       El dashboard los lee directamente sin renombrar.
# ============================================================================
"""
import os, subprocess, sys, time, csv

# Instalación automática de librerías
for p in ["requests", "pyserial"]:
    try:
        __import__(p if p != "pyserial" else "serial")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", p])

import serial, requests

# ============================================================================
#  CONFIGURACIÓN — ajustar antes de cada sesión
# ============================================================================
MODO          = "CONCURSO"   # "CONCURSO" o "PRUEBAS"
PUERTO_SERIAL = 'COM3'       # Verificar en Administrador de dispositivos
BAUDRATE      = 9600         # APC220 configurado a 9600

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
RUTA         = "/cansat/telemetria" if MODO == "CONCURSO" else "/cansat/pruebas"
ARCHIVO_CSV  = "caelum_datos_vuelo.csv" if MODO == "CONCURSO" else "pruebas_sensores.csv"

# Cabecera oficial de 25 campos (misma que genera el Arduino)
CABECERA = [
    'timestamp', 'datetime', 'lat', 'lon', 'alt', 'alt_mar', 'sats',
    'temp_hs', 'hum_hs', 'temp_scd', 'hum_scd', 'temp_lps', 'presion',
    'co2', 'pm1_0', 'pm2_5', 'pm10',
    'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'fase'
]

# Campos que van como número a Firebase
CAMPOS_FLOAT = {
    'timestamp', 'lat', 'lon', 'alt', 'alt_mar', 'sats',
    'temp_hs', 'hum_hs', 'temp_scd', 'hum_scd', 'temp_lps', 'presion',
    'co2', 'pm1_0', 'pm2_5', 'pm10',
    'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'
}

# ============================================================================
#  PARSEO — por nombre de campo, no por índice
# ============================================================================
def parsear_linea(linea):
    """
    Convierte una línea CSV recibida por el APC220 en un diccionario
    usando la cabecera oficial. Robusto ante campos extra o faltantes.
    Devuelve None si la línea no es válida.
    """
    partes = linea.strip().split(',')

    # Descartar líneas con menos de 23 campos (mínimo aceptable)
    if len(partes) < 23:
        return None

    # Ignorar la cabecera si el Arduino la reenvía
    if partes[0].strip().lower() == 'timestamp':
        return None

    payload = {}
    for i, campo in enumerate(CABECERA):
        if i >= len(partes):
            payload[campo] = 0.0 if campo in CAMPOS_FLOAT else ''
            continue
        valor = partes[i].strip()
        if campo in CAMPOS_FLOAT:
            try:
                payload[campo] = float(valor)
            except ValueError:
                payload[campo] = 0.0
        else:
            payload[campo] = valor

    return payload

# ============================================================================
#  CSV LOCAL — escribe con la cabecera correcta
# ============================================================================
def escribir_csv(payload):
    """Guarda la fila en el CSV local. Crea el archivo con cabecera si no existe."""
    existe = os.path.exists(ARCHIVO_CSV) and os.path.getsize(ARCHIVO_CSV) > 0
    with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CABECERA, extrasaction='ignore')
        if not existe:
            writer.writeheader()
        writer.writerow(payload)

# ============================================================================
#  FIREBASE — PUT con timestamp como clave
# ============================================================================
def enviar_firebase(payload):
    """
    Envía el payload a Firebase usando PUT con el timestamp como clave.
    El dashboard usa limitToLast(1) → siempre muestra el dato más reciente.
    """
    ts  = int(payload.get('timestamp', int(time.time())))
    url = f"{FIREBASE_URL}{RUTA}/{ts}.json"
    r   = requests.put(url, json=payload, timeout=8)
    return r.status_code == 200

# ============================================================================
#  MAIN
# ============================================================================
def ejecutar():
    print(f"\n{'═'*55}")
    print(f"   🛰️  CANSAT CAELUM — ESTACIÓN DE TIERRA v2")
    print(f"{'═'*55}")
    print(f"   Modo:    {MODO}")
    print(f"   Puerto:  {PUERTO_SERIAL} @ {BAUDRATE} baud")
    print(f"   Firebase: {RUTA}")
    print(f"   CSV:     {ARCHIVO_CSV}")
    print(f"{'═'*55}\n")

    # Limpiar Firebase al iniciar
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA}.json", timeout=8)
        print(f"🗑️  Firebase {RUTA} limpiado\n")
    except Exception as e:
        print(f"⚠️  No se pudo limpiar Firebase: {e}\n")

    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUDRATE, timeout=1)
        print(f"📡 Escuchando en {PUERTO_SERIAL}... (Ctrl+C para detener)\n")

        muestras = 0
        errores  = 0

        while True:
            try:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
            except serial.SerialException as e:
                print(f"⚠️  Error leyendo puerto serie: {e}")
                time.sleep(1)
                continue

            if not linea:
                continue

            payload = parsear_linea(linea)
            if payload is None:
                if linea:  # no mostrar líneas vacías
                    print(f"   [SKIP] {linea[:60]}...")
                continue

            # Enviar a Firebase
            ok_fb = False
            try:
                ok_fb = enviar_firebase(payload)
            except Exception as e:
                print(f"⚠️  Firebase: {e}")

            # Guardar CSV local
            try:
                escribir_csv(payload)
            except Exception as e:
                print(f"⚠️  CSV: {e}")

            muestras += 1
            if not ok_fb:
                errores += 1

            # Log en pantalla
            alt   = payload.get('alt', 0)
            fase  = payload.get('fase', '—')
            co2   = payload.get('co2', 0)
            pm25  = payload.get('pm2_5', 0)
            t_hs  = payload.get('temp_hs', 0)
            t_scd = payload.get('temp_scd', 0)
            sats  = int(payload.get('sats', 0))
            delta = abs(t_hs - t_scd)
            fb_ico = "✅" if ok_fb else "⚠️"

            print(f"{fb_ico} [{muestras:>4}]  Alt={alt:>6.1f}m  {fase:<12}  "
                  f"CO₂={co2:>4.0f}  PM2.5={pm25:>5.1f}  "
                  f"T_HS={t_hs:.1f}°C  ΔT={delta:.1f}°C  Sats={sats}")

    except serial.SerialException:
        print(f"\n❌ No se pudo abrir {PUERTO_SERIAL}.")
        print("   Verifica que el APC220 esté conectado y el puerto sea correcto.")
        print("   Puertos disponibles: revisa el Administrador de dispositivos.")

    except KeyboardInterrupt:
        print(f"\n\n🛑 Estación de tierra detenida.")
        print(f"   Muestras recibidas: {muestras}")
        print(f"   Errores Firebase:   {errores}")
        if muestras > 0:
            print(f"   CSV guardado en:    {ARCHIVO_CSV}")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    ejecutar()
