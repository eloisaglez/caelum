"""
limpiar_espera.py — Limpia los datos crudos del CanSat eliminando la fase espera

El Arduino guarda TODOS los datos en datos_SD_raw.csv (incluyendo la espera previa
al lanzamiento y la subida en globo). Este script genera datos_SD.csv ya limpio,
listo para usar con analizar_vuelo.py, generar_kml.py y caelum_playback.py.

Uso:
    python limpiar_espera.py datos_SD_raw.csv     → genera datos_SD.csv
    python limpiar_espera.py datos_radio.csv      → genera datos_radio_limpio.csv

El fichero original nunca se modifica.
"""

import sys
import os
import csv

# ──────────────────────────────────────────────────────────────
#  FASES A ELIMINAR
# ──────────────────────────────────────────────────────────────
FASES_ELIMINAR = {"espera"}

# ──────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Uso: python limpiar_espera.py <fichero.csv>")
        print("")
        print("  python limpiar_espera.py datos_SD.csv")
        print("  python limpiar_espera.py datos_radio.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: no se encuentra el fichero '{input_file}'")
        sys.exit(1)

    # Nombre del fichero de salida
    # Caso especial: datos_SD_raw.csv → datos_SD.csv (nombre estandar del sistema)
    if os.path.basename(input_file) == "datos_SD_raw.csv":
        output_file = os.path.join(os.path.dirname(input_file), "datos_SD.csv")
    else:
        base, ext = os.path.splitext(input_file)
        output_file = base + "_limpio" + ext

    print(f"Leyendo: {input_file}")

    filas_total    = 0
    filas_espera   = 0
    filas_vuelo    = 0
    filas_sin_fase = 0

    with open(input_file, "r", encoding="utf-8", newline="") as f_in, \
         open(output_file, "w", encoding="utf-8", newline="") as f_out:

        reader = csv.DictReader(f_in)

        if reader.fieldnames is None:
            print("Error: el fichero no tiene cabecera o está vacío.")
            sys.exit(1)

        if "fase" not in reader.fieldnames:
            print("Error: columna 'fase' no encontrada en el CSV.")
            print(f"  Columnas disponibles: {reader.fieldnames}")
            sys.exit(1)

        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()

        for fila in reader:
            filas_total += 1
            fase = fila.get("fase", "").strip()

            if fase == "":
                # Fila sin fase — conservar
                filas_sin_fase += 1
                writer.writerow(fila)
            elif fase in FASES_ELIMINAR:
                filas_espera += 1
                # No se escribe — se elimina
            else:
                filas_vuelo += 1
                writer.writerow(fila)

    # Resumen
    print()
    print("=" * 45)
    print(f"  Total filas leidas:     {filas_total:>6}")
    print(f"  Filas espera eliminadas:{filas_espera:>6}")
    print(f"  Filas de vuelo (OK):    {filas_vuelo:>6}")
    if filas_sin_fase > 0:
        print(f"  Filas sin fase (OK):    {filas_sin_fase:>6}")
    print("=" * 45)

    if filas_vuelo == 0:
        print("\nAVISO: No quedan filas tras la limpieza.")
        print("  El CanSat quiza no entro en ninguna fase activa.")
        os.remove(output_file)
    else:
        print(f"\nGuardado: {output_file}")
        tam_original = os.path.getsize(input_file) / 1024
        tam_limpio   = os.path.getsize(output_file) / 1024
        print(f"  Original: {tam_original:.1f} KB  →  Limpio: {tam_limpio:.1f} KB")

if __name__ == "__main__":
    main()
