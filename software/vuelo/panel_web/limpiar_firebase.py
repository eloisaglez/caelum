"""
============================================================
  CANSAT CAELUM — Limpiador de Firebase
  IES Diego Velázquez · Febrero 2026
============================================================
  Borra por lotes los datos de cualquier carpeta Firebase.
  Útil cuando los scripts automáticos no pueden borrar
  porque hay demasiados datos acumulados.

  Uso:
      python limpiar_firebase.py
============================================================
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"

CARPETAS = {
    '1': '/cansat/telemetria',
    '2': '/cansat/simulacion',
    '3': '/cansat/replay',
    '4': '/cansat/pruebas',
    '5': '/cansat',           # borra TODO
}

def borrar_carpeta(ruta):
    # Obtener claves sin descargar datos
    print(f"📡 Consultando {ruta}...")
    try:
        r = requests.get(f"{BASE}{ruta}.json?shallow=true", timeout=30)
        datos = r.json()
    except Exception as e:
        print(f"❌ Error consultando Firebase: {e}")
        return

    if not datos:
        print(f"✅ {ruta} ya estaba vacío")
        return

    claves = list(datos.keys())
    print(f"🗑️  {len(claves)} entradas encontradas en {ruta}")

    if len(claves) > 1000:
        print(f"⚡ Modo rápido (paralelo) — puede tardar unos minutos...")
        inicio = time.time()

        def borrar_una(clave):
            requests.delete(f"{BASE}{ruta}/{clave}.json", timeout=10)

        with ThreadPoolExecutor(max_workers=20) as executor:
            for i, _ in enumerate(executor.map(borrar_una, claves)):
                if i % 5000 == 0 and i > 0:
                    elapsed = time.time() - inicio
                    restante = (elapsed / i) * (len(claves) - i) / 60
                    print(f"   {i}/{len(claves)} — ~{restante:.0f} min restantes")
    else:
        print(f"🗑️  Borrando {len(claves)} entradas...")
        for i, clave in enumerate(claves):
            requests.delete(f"{BASE}{ruta}/{clave}.json", timeout=10)
            if i % 50 == 0 and i > 0:
                print(f"   {i}/{len(claves)}")

    print(f"✅ {ruta} limpiado ({len(claves)} entradas borradas)\n")


def main():
    print("\n" + "═" * 50)
    print("   🗑️  CANSAT CAELUM — Limpiador de Firebase")
    print("═" * 50)
    print("\n¿Qué carpeta quieres borrar?\n")
    for k, v in CARPETAS.items():
        print(f"   {k} → {v}")
    print()

    opcion = input("Elige (1-5): ").strip()

    if opcion not in CARPETAS:
        print("❌ Opción no válida")
        return

    ruta = CARPETAS[opcion]

    if opcion == '5':
        confirma = input(f"\n⚠️  Vas a borrar TODO /cansat. ¿Seguro? (escribe SI): ")
        if confirma.strip().upper() != 'SI':
            print("Cancelado.")
            return

    print()
    borrar_carpeta(ruta)


if __name__ == "__main__":
    main()
