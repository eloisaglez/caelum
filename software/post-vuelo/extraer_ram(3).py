"""
============================================================
  CANSAT CAELUM — Extractor de RAM Backup
  IES Diego Velázquez · Febrero 2026
============================================================
  Conecta al Arduino por USB, envía CSV_RAM y guarda
  automáticamente los datos en un archivo CSV.

  Uso:
      python extraer_ram.py

  Configuración:
      PUERTO  → verificar en Administrador de dispositivos
      BAUDRATE → debe coincidir con el Arduino (115200)
============================================================
"""

import os
import sys
import subprocess
import time

# Instalación automática de pyserial si no está
try:
    import serial
except ImportError:
    print("📦 Instalando pyserial...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
    import serial

# ── CONFIGURACIÓN ──────────────────────────────────────────
PUERTO   = 'COM3'    # ⚠️ Cambiar si el Arduino está en otro puerto
BAUDRATE = 115200    # Debe coincidir con el Arduino
TIMEOUT  = 10        # Segundos esperando respuesta del Arduino

OUTPUT_FILE = 'datos_RAM.csv'
# ───────────────────────────────────────────────────────────


def detectar_puertos():
    """Lista los puertos serie disponibles para ayudar a identificar el correcto."""
    import serial.tools.list_ports
    puertos = list(serial.tools.list_ports.comports())
    if puertos:
        print("\n   Puertos disponibles:")
        for p in puertos:
            print(f"     {p.device} — {p.description}")
    else:
        print("\n   ⚠️  No se detectó ningún puerto serie.")
    print()


def extraer_ram():
    print("\n" + "═" * 55)
    print("   🛰️  CANSAT CAELUM — Extractor RAM Backup")
    print("═" * 55)
    print(f"   Puerto:  {PUERTO} @ {BAUDRATE} baud")
    print(f"   Salida:  {OUTPUT_FILE}")
    print("═" * 55 + "\n")

    # Intentar abrir el puerto
    try:
        ser = serial.Serial(PUERTO, BAUDRATE, timeout=TIMEOUT)
    except serial.SerialException:
        print(f"❌ No se pudo abrir {PUERTO}.")
        detectar_puertos()
        print(f"   Edita PUERTO en el script con el valor correcto.")
        return

    print(f"✅ Conectado a {PUERTO}")
    print("⏳ Esperando que el Arduino esté listo (3s)...")
    time.sleep(3)  # El Arduino puede hacer reset al conectar por USB

    # Vaciar buffer de entrada
    ser.reset_input_buffer()

    # Enviar comando
    print("📤 Enviando comando CSV_RAM...")
    ser.write(b'CSV_RAM\n')

    # Leer respuesta
    lineas = []
    cabecera_encontrada = False
    fin_encontrado = False

    print("📥 Recibiendo datos...\n")

    while True:
        try:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
        except serial.SerialException as e:
            print(f"⚠️  Error leyendo puerto: {e}")
            break

        if not linea:
            continue

        # Detectar inicio del CSV
        if 'inicio' in linea.lower() or linea.lower().startswith('---'):
            print(f"   {linea}")
            continue

        # Detectar fin del CSV
        if 'fin' in linea.lower() or 'end' in linea.lower():
            print(f"\n   {linea}")
            fin_encontrado = True
            break

        # Detectar cabecera (primera línea con nombres de columnas)
        if not cabecera_encontrada and 'timestamp' in linea.lower():
            cabecera_encontrada = True
            lineas.append(linea)
            print(f"   📋 Cabecera: {linea[:60]}...")
            continue

        # Datos
        if cabecera_encontrada and linea:
            lineas.append(linea)
            # Mostrar progreso cada 10 filas
            n = len(lineas) - 1  # sin contar cabecera
            if n % 10 == 0:
                print(f"   [{n:>4} muestras recibidas]")

    ser.close()

    # Verificar que recibimos algo útil
    if not cabecera_encontrada:
        print("\n❌ No se recibió la cabecera CSV.")
        print("   Verifica que el Arduino tiene el firmware actualizado")
        print("   y que responde al comando CSV_RAM.")
        return

    if not fin_encontrado:
        print("\n⚠️  No se recibió el marcador de FIN — los datos pueden estar incompletos.")

    n_muestras = len(lineas) - 1  # sin contar cabecera

    if n_muestras == 0:
        print("\n⚠️  La RAM está vacía — no hay datos de vuelo guardados.")
        return

    # Guardar CSV
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')

    print(f"\n{'═'*55}")
    print(f"   ✅ EXTRACCIÓN COMPLETADA")
    print(f"{'═'*55}")
    print(f"   Muestras guardadas: {n_muestras}")
    print(f"   Archivo:            {OUTPUT_FILE}")
    print(f"\n   Siguiente paso:")
    print(f"   python analizar_vuelo.py {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    extraer_ram()
