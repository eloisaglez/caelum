"""
============================================================
  CANSAT CAELUM — Generador KML para Google Earth
  IES Diego Velázquez · Febrero 2026
============================================================
  Genera un archivo KML con la trayectoria del vuelo
  coloreada por PM2.5 y puntos de datos para Google Earth.

  Uso:
      python generar_kml.py <fichero.csv>

  Ejemplos:
      python generar_kml.py datos_SD.csv
      python generar_kml.py datos_radio.csv

  Genera:
      analisis_vuelo/trayectoria_vuelo.kml
============================================================
"""

import sys
import os
import csv

# ── CONFIGURACIÓN ──────────────────────────────────────────
OUTPUT_DIR  = 'analisis_vuelo'
OUTPUT_FILE = 'trayectoria_vuelo.kml'

# Umbrales PM2.5 OMS para colores (AABBGGRR en formato KML)
COLORES_PM25 = [
    (12,  'ff88ff00'),   # 🟢 Verde    0–12  Excelente
    (35,  'ff00ffff'),   # 🟡 Amarillo 12–35 Buena
    (55,  'ff00aaff'),   # 🟠 Naranja  35–55 Moderada
    (150, 'ff0000ff'),   # 🔴 Rojo     55–150 Mala
    (999, 'ff0000aa'),   # 🔴 Rojo osc >150  Muy Mala
]

def color_pm25(valor):
    """Devuelve el color KML según el valor de PM2.5."""
    for umbral, color in COLORES_PM25:
        if valor <= umbral:
            return color
    return 'ff0000aa'

def cargar_datos(filepath):
    """Carga el CSV y devuelve lista de filas con GPS válido."""
    filas = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                lat  = float(fila.get('lat', 0))
                lon  = float(fila.get('lon', 0))
                alt  = float(fila.get('alt', 0))
                if lat == 0.0 and lon == 0.0:
                    continue  # Sin fix GPS
                fila['_lat']  = lat
                fila['_lon']  = lon
                fila['_alt']  = alt
                fila['_pm25'] = float(fila.get('pm2_5', 0))
                fila['_co2']  = float(fila.get('co2', 0))
                fila['_temp'] = float(fila.get('temp_hs', 0))
                fila['_fase'] = fila.get('fase', '').strip()
                filas.append(fila)
            except (ValueError, TypeError):
                continue
    return filas

def generar_kml(filas, output_path):
    """Genera el archivo KML con trayectoria y puntos de datos."""

    # Punto de máxima altitud
    max_alt = max(filas, key=lambda f: f['_alt'])
    # Punto de máximo PM2.5
    max_pm25 = max(filas, key=lambda f: f['_pm25'])

    kml = []
    kml.append('<?xml version="1.0" encoding="UTF-8"?>')
    kml.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
    kml.append('<Document>')
    kml.append('  <name>CanSat CAELUM — Trayectoria de Vuelo</name>')
    kml.append('  <description>Perfil vertical de PM2.5 e inversiones térmicas</description>')

    # ── Estilos de colores por PM2.5 ──
    estilos = [
        ('pm_excelente', 'ff88ff00', 'PM2.5 Excelente (0-12)'),
        ('pm_buena',     'ff00ffff', 'PM2.5 Buena (12-35)'),
        ('pm_moderada',  'ff00aaff', 'PM2.5 Moderada (35-55)'),
        ('pm_mala',      'ff0000ff', 'PM2.5 Mala (55-150)'),
        ('pm_muy_mala',  'ff0000aa', 'PM2.5 Muy Mala (>150)'),
    ]
    for id_estilo, color, _ in estilos:
        kml.append(f'  <Style id="{id_estilo}">')
        kml.append(f'    <IconStyle><color>{color}</color><scale>0.6</scale>')
        kml.append(f'      <Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon>')
        kml.append(f'    </IconStyle>')
        kml.append(f'    <LineStyle><color>{color}</color><width>3</width></LineStyle>')
        kml.append(f'  </Style>')

    # Estilo punto especial
    kml.append('  <Style id="punto_max_alt">')
    kml.append('    <IconStyle><color>ffff0000</color><scale>1.2</scale>')
    kml.append('      <Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png</href></Icon>')
    kml.append('    </IconStyle>')
    kml.append('  </Style>')

    kml.append('  <Style id="punto_max_pm25">')
    kml.append('    <IconStyle><color>ff0000ff</color><scale>1.2</scale>')
    kml.append('      <Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon>')
    kml.append('    </IconStyle>')
    kml.append('  </Style>')

    # ── Carpeta: Trayectoria coloreada por PM2.5 ──
    kml.append('  <Folder>')
    kml.append('    <name>🛰️ Trayectoria por PM2.5</name>')

    # Segmentos de trayectoria coloreados
    prev = None
    for fila in filas:
        if prev is not None:
            pm25_med = (prev['_pm25'] + fila['_pm25']) / 2
            if pm25_med <= 12:   estilo = 'pm_excelente'
            elif pm25_med <= 35: estilo = 'pm_buena'
            elif pm25_med <= 55: estilo = 'pm_moderada'
            elif pm25_med <= 150: estilo = 'pm_mala'
            else:                estilo = 'pm_muy_mala'

            kml.append(f'    <Placemark>')
            kml.append(f'      <styleUrl>#{estilo}</styleUrl>')
            kml.append(f'      <LineString>')
            kml.append(f'        <altitudeMode>absolute</altitudeMode>')
            kml.append(f'        <coordinates>')
            kml.append(f'          {prev["_lon"]},{prev["_lat"]},{prev["_alt"]}')
            kml.append(f'          {fila["_lon"]},{fila["_lat"]},{fila["_alt"]}')
            kml.append(f'        </coordinates>')
            kml.append(f'      </LineString>')
            kml.append(f'    </Placemark>')
        prev = fila

    kml.append('  </Folder>')

    # ── Carpeta: Puntos de datos cada 5 muestras ──
    kml.append('  <Folder>')
    kml.append('    <name>📊 Datos por altitud</name>')
    kml.append('    <visibility>0</visibility>')

    for i, fila in enumerate(filas):
        if i % 5 != 0:
            continue
        pm25 = fila['_pm25']
        co2  = fila['_co2']
        temp = fila['_temp']
        alt  = fila['_alt']
        fase = fila['_fase']

        if pm25 <= 12:   estilo = 'pm_excelente'
        elif pm25 <= 35: estilo = 'pm_buena'
        elif pm25 <= 55: estilo = 'pm_moderada'
        elif pm25 <= 150: estilo = 'pm_mala'
        else:            estilo = 'pm_muy_mala'

        desc = (f'<b>Altitud:</b> {alt:.0f} m<br>'
                f'<b>PM2.5:</b> {pm25:.1f} µg/m³<br>'
                f'<b>CO₂:</b> {co2:.0f} ppm<br>'
                f'<b>Temp:</b> {temp:.1f} °C<br>'
                f'<b>Fase:</b> {fase}')

        kml.append(f'    <Placemark>')
        kml.append(f'      <name>{alt:.0f}m — PM2.5={pm25:.0f}</name>')
        kml.append(f'      <description><![CDATA[{desc}]]></description>')
        kml.append(f'      <styleUrl>#{estilo}</styleUrl>')
        kml.append(f'      <Point>')
        kml.append(f'        <altitudeMode>absolute</altitudeMode>')
        kml.append(f'        <coordinates>{fila["_lon"]},{fila["_lat"]},{alt}</coordinates>')
        kml.append(f'      </Point>')
        kml.append(f'    </Placemark>')

    kml.append('  </Folder>')

    # ── Puntos especiales ──
    kml.append('  <Folder>')
    kml.append('    <name>⭐ Puntos destacados</name>')

    # Altitud máxima
    kml.append('    <Placemark>')
    kml.append(f'      <name>🏔️ Altitud máxima: {max_alt["_alt"]:.0f} m</name>')
    kml.append(f'      <description><![CDATA[Altitud: {max_alt["_alt"]:.0f} m<br>PM2.5: {max_alt["_pm25"]:.1f} µg/m³<br>CO₂: {max_alt["_co2"]:.0f} ppm]]></description>')
    kml.append('      <styleUrl>#punto_max_alt</styleUrl>')
    kml.append('      <Point>')
    kml.append('        <altitudeMode>absolute</altitudeMode>')
    kml.append(f'        <coordinates>{max_alt["_lon"]},{max_alt["_lat"]},{max_alt["_alt"]}</coordinates>')
    kml.append('      </Point>')
    kml.append('    </Placemark>')

    # PM2.5 máximo
    kml.append('    <Placemark>')
    kml.append(f'      <name>🔴 PM2.5 máximo: {max_pm25["_pm25"]:.1f} µg/m³</name>')
    kml.append(f'      <description><![CDATA[PM2.5: {max_pm25["_pm25"]:.1f} µg/m³<br>Altitud: {max_pm25["_alt"]:.0f} m<br>CO₂: {max_pm25["_co2"]:.0f} ppm]]></description>')
    kml.append('      <styleUrl>#punto_max_pm25</styleUrl>')
    kml.append('      <Point>')
    kml.append('        <altitudeMode>absolute</altitudeMode>')
    kml.append(f'        <coordinates>{max_pm25["_lon"]},{max_pm25["_lat"]},{max_pm25["_alt"]}</coordinates>')
    kml.append('      </Point>')
    kml.append('    </Placemark>')

    kml.append('  </Folder>')

    kml.append('</Document>')
    kml.append('</kml>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(kml))

# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Debes indicar el archivo CSV.")
        print("   Uso: python generar_kml.py <fichero.csv>")
        print("   Ejemplos:")
        print("     python generar_kml.py datos_SD.csv")
        print("     python generar_kml.py datos_radio.csv")
        sys.exit(1)

    INPUT_FILE = sys.argv[1]

    if not os.path.exists(INPUT_FILE):
        print(f"❌ No se encuentra: {INPUT_FILE}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    print(f"\n🛰️  CANSAT CAELUM — Generador KML")
    print(f"   Archivo: {INPUT_FILE}")
    print(f"   Salida:  {output_path}\n")

    filas = cargar_datos(INPUT_FILE)

    if not filas:
        print("⚠️  No hay datos con fix GPS — no se puede generar KML.")
        sys.exit(1)

    print(f"📍 {len(filas)} puntos con GPS válido")

    generar_kml(filas, output_path)

    print(f"✅ KML generado: {output_path}")
    print(f"\n   Abrir en Google Earth:")
    print(f"   Archivo → Abrir → {output_path}")
    print(f"\n   Colores por PM2.5 (OMS):")
    print(f"   🟢 Verde    0–12 µg/m³  Excelente")
    print(f"   🟡 Amarillo 12–35 µg/m³ Buena")
    print(f"   🟠 Naranja  35–55 µg/m³ Moderada")
    print(f"   🔴 Rojo     55–150 µg/m³ Mala")
    print(f"   🔴 Rojo osc >150 µg/m³  Muy Mala\n")
