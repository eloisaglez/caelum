#!/usr/bin/env python3
"""
CANSAT MISIÓN 2 - Generador KML 3D para Google Earth

Formato CSV esperado:
equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,h2,ethanol,accX,accY,accZ,gyrX,gyrY,gyrZ

Autor: IES Diego Velázquez - Equipo CAELUM
Fecha: Febrero 2026
"""

import pandas as pd
import simplekml
import math

# ============ CONFIGURACIÓN ============
INPUT_FILE = 'datos_vuelo.csv'
OUTPUT_KML = 'firmas_combustion_3d.kml'
ESCALA_ALTURA = 1.5
RADIO_CILINDRO = 3.0

# ============ FUNCIONES ============

def get_color_kml(tvoc, min_tvoc, max_tvoc):
    if max_tvoc == min_tvoc:
        norm = 0.5
    else:
        norm = (tvoc - min_tvoc) / (max_tvoc - min_tvoc)
    
    if norm < 0.5:
        r = int(255 * (norm * 2))
        g = 255
        b = 0
    else:
        r = 255
        g = int(255 * (2 - norm * 2))
        b = 0
    
    return f"bb{b:02x}{g:02x}{r:02x}"

def crear_circulo(lon, lat, radio_metros, num_puntos=24):
    radio_deg = radio_metros / 111320.0
    puntos = []
    for i in range(num_puntos + 1):
        angulo = 2 * math.pi * i / num_puntos
        dx = radio_deg * math.cos(angulo)
        dy = radio_deg * math.sin(angulo)
        puntos.append((lon + dx, lat + dy))
    return puntos

def clasificar_calidad(tvoc):
    if tvoc < 220:
        return 'Excelente 🟢'
    elif tvoc < 660:
        return 'Buena 🟡'
    elif tvoc < 2200:
        return 'Moderada 🟠'
    elif tvoc < 5500:
        return 'Mala 🔴'
    else:
        return 'Muy Mala ⛔'

def detectar_firma(tvoc, eco2, h2, ethanol):
    if tvoc > 1000 and h2 > 13000:
        return '🚜 Generador Diésel'
    elif tvoc > 500 and ethanol > 18000:
        return '🔥 Combustión Biomasa'
    elif tvoc > 300 and eco2 > 1000 and tvoc < 800:
        return '🚗 Tráfico Vehicular'
    elif tvoc > 5000:
        return '⚠️ Contaminación Severa'
    elif tvoc < 100:
        return '🌿 Aire Limpio'
    else:
        return '🏭 Fuente Industrial'

# ============ MAIN ============

def main():
    print("🚀 Generando KML 3D para Google Earth...\n")
    
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"✅ {len(df)} registros cargados")
        
        equipo = df['equipo'].iloc[0] if 'equipo' in df.columns else 'CAELUM'
        
        # Filtrar GPS válido
        df_gps = df[(df['lat'] != 0) & (df['lon'] != 0)].copy()
        print(f"📍 {len(df_gps)} puntos con GPS válido\n")
        
        if len(df_gps) == 0:
            print("❌ No hay puntos con GPS válido")
            return
        
        # Crear KML
        kml = simplekml.Kml()
        kml.document.name = f"{equipo} - Misión 2 Firmas de Combustión"
        
        min_tvoc = df_gps['tvoc'].min()
        max_tvoc = df_gps['tvoc'].max()
        
        print(f"📊 TVOC: {min_tvoc:.0f} - {max_tvoc:.0f} ppb")
        
        folder = kml.newfolder(name="Cilindros TVOC")
        
        # Cilindros
        for idx, row in df_gps.iterrows():
            lat, lon = row['lat'], row['lon']
            tvoc = row['tvoc']
            altura = tvoc * ESCALA_ALTURA
            
            pol = folder.newpolygon(name=f"#{int(row['paquete'])} TVOC: {int(tvoc)} ppb")
            pol.outerboundaryis = crear_circulo(lon, lat, RADIO_CILINDRO)
            pol.extrude = 1
            pol.altitudemode = simplekml.AltitudeMode.relativetoground
            
            color = get_color_kml(tvoc, min_tvoc, max_tvoc)
            pol.style.polystyle.color = color
            pol.style.linestyle.color = color.replace('bb', 'ff')
            pol.style.linestyle.width = 2
            
            calidad = clasificar_calidad(tvoc)
            firma = detectar_firma(tvoc, row['eco2'], row['h2'], row['ethanol'])
            
            pol.description = f"""
            <![CDATA[
            <div style="font-family: Arial; font-size: 14px;">
                <h3>🛰️ {equipo} - Paquete #{int(row['paquete'])}</h3>
                <hr/>
                <b>⏱️ Tiempo:</b> {row['timestamp']/1000:.1f} s<br/>
                <b>📍 Coordenadas:</b> {lat:.6f}°, {lon:.6f}°<br/>
                <b>📏 Altitud:</b> {row['altBaro']:.0f} m<br/>
                <b>🛰️ Satélites:</b> {int(row['sats'])}<br/>
                <hr/>
                <h4 style="color: #FF6600;">Datos de Contaminación</h4>
                <b>🌫️ TVOC:</b> <span style="font-size: 18px;">{int(tvoc)} ppb</span><br/>
                <b>💨 eCO2:</b> {int(row['eco2'])} ppm<br/>
                <b>🔬 H2:</b> {int(row['h2'])}<br/>
                <b>🔬 Ethanol:</b> {int(row['ethanol'])}<br/>
                <hr/>
                <b>📊 Calidad:</b> {calidad}<br/>
                <b>🔍 Firma:</b> {firma}<br/>
            </div>
            ]]>
            """
        
        # Trayectoria
        path = kml.newlinestring(name=f"Trayectoria {equipo}")
        path.coords = [(row['lon'], row['lat'], row['altBaro']) for _, row in df_gps.iterrows()]
        path.altitudemode = simplekml.AltitudeMode.absolute
        path.style.linestyle.color = 'ffffffff'
        path.style.linestyle.width = 4
        
        # Inicio/Fin
        inicio = kml.newpoint(name="🚀 Inicio")
        inicio.coords = [(df_gps.iloc[0]['lon'], df_gps.iloc[0]['lat'], df_gps.iloc[0]['altBaro'])]
        inicio.style.iconstyle.color = simplekml.Color.green
        inicio.style.iconstyle.scale = 2
        
        fin = kml.newpoint(name="🎯 Aterrizaje")
        fin.coords = [(df_gps.iloc[-1]['lon'], df_gps.iloc[-1]['lat'], df_gps.iloc[-1]['altBaro'])]
        fin.style.iconstyle.color = simplekml.Color.red
        fin.style.iconstyle.scale = 2
        
        # Guardar
        kml.save(OUTPUT_KML)
        
        print(f"\n✅ KML generado: {OUTPUT_KML}")
        print(f"\n📊 Resumen:")
        print(f"   • Cilindros: {len(df_gps)}")
        print(f"   • Altura máxima: {max_tvoc * ESCALA_ALTURA:.0f} m")
        print(f"\n💡 Abre en Google Earth para visualizar")
        
    except FileNotFoundError:
        print(f"❌ No se encontró {INPUT_FILE}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
