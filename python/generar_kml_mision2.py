#!/usr/bin/env python3
"""
Generador de KML con cilindros 3D para Google Earth
Específico para datos de Misión 2 (firmas de combustión)
"""

import pandas as pd
import simplekml
import math

# ============ CONFIGURACIÓN ============
INPUT_FILE = 'mission2.csv'
OUTPUT_KML = 'firmas_combustion_3d.kml'
ESCALA_ALTURA = 1.5  # Factor de escala para altura de cilindros
RADIO_CILINDRO = 3.0  # Radio en metros

def get_color_from_tvoc(tvoc, min_tvoc, max_tvoc):
    """Genera color basado en TVOC (verde->amarillo->rojo)"""
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
    
    return f"bb{b:02x}{g:02x}{r:02x}"  # bb = semi-transparente

def create_circle(center_lon, center_lat, radius_meters, num_points=24):
    """Crea puntos para formar un círculo"""
    radius_deg = radius_meters / 111320.0
    points = []
    for i in range(num_points + 1):
        angle = 2 * math.pi * i / num_points
        dx = radius_deg * math.cos(angle)
        dy = radius_deg * math.sin(angle)
        points.append((center_lon + dx, center_lat + dy))
    return points

def clasificar_calidad(tvoc):
    """Devuelve clasificación legible"""
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
    """Detecta tipo de fuente de contaminación"""
    if tvoc > 1000 and h2 > 13000:
        return '🚜 Generador Diésel'
    elif tvoc > 500 and ethanol > 18000:
        return '🔥 Combustión Biomasa'
    elif tvoc > 300 and eco2 > 1000 and tvoc < 800:
        return '🚗 Tráfico Vehicular'
    elif tvoc > 5000:
        return '⚠️  Contaminación Severa'
    elif tvoc < 100:
        return '🌿 Aire Limpio'
    else:
        return '🏭 Fuente Industrial'

def main():
    print("🚀 Generando KML 3D para Google Earth...\n")
    
    try:
        # Cargar datos
        df = pd.read_csv(INPUT_FILE)
        print(f"✅ Cargados {len(df)} registros\n")
        
        # Filtrar solo puntos con GPS válido
        df_gps = df[(df['lat'] != 0) & (df['lon'] != 0)].copy()
        print(f"📍 {len(df_gps)} puntos con GPS válido\n")
        
        if len(df_gps) == 0:
            print("❌ Error: No hay puntos con GPS válido")
            return
        
        # Crear KML
        kml = simplekml.Kml()
        kml.document.name = "CanSat Misión 2 - Firmas de Combustión"
        
        min_tvoc = df_gps['tvoc'].min()
        max_tvoc = df_gps['tvoc'].max()
        
        print(f"📊 Rango TVOC: {min_tvoc} - {max_tvoc} ppb")
        print(f"📏 Factor de escala: {ESCALA_ALTURA}x")
        print(f"🎯 Radio cilindros: {RADIO_CILINDRO}m\n")
        
        folder = kml.newfolder(name="Cilindros TVOC")
        
        # Crear cilindros para cada punto
        for idx, row in df_gps.iterrows():
            lat = row['lat']
            lon = row['lon']
            alt = row['alt']
            tvoc = row['tvoc']
            eco2 = row['eco2']
            h2 = row['h2']
            ethanol = row['ethanol']
            
            altura_cilindro = tvoc * ESCALA_ALTURA
            
            # Crear polígono cilíndrico
            pol = folder.newpolygon(name=f"TVOC: {tvoc} ppb")
            pol.outerboundaryis = create_circle(lon, lat, RADIO_CILINDRO, 24)
            
            # Configuración 3D
            pol.extrude = 1
            pol.altitudemode = simplekml.AltitudeMode.relativetoground
            pol.tessellate = 1
            
            # Color
            color_kml = get_color_from_tvoc(tvoc, min_tvoc, max_tvoc)
            pol.style.polystyle.color = color_kml
            pol.style.polystyle.outline = 1
            pol.style.linestyle.color = color_kml.replace('bb', 'ff')
            pol.style.linestyle.width = 2
            
            # Descripción detallada
            calidad = clasificar_calidad(tvoc)
            firma = detectar_firma(tvoc, eco2, h2, ethanol)
            
            pol.description = f"""
            <div style="font-family: Arial; font-size: 14px;">
                <h3>🛰️  Medición CanSat</h3>
                <hr/>
                <b>⏱️  Tiempo:</b> {row['timestamp']} s<br/>
                <b>📍 Coordenadas:</b> {lat:.6f}°, {lon:.6f}°<br/>
                <b>📏 Altitud:</b> {alt:.1f} m<br/>
                <b>🛰️  Satélites:</b> {row['sats']}<br/>
                <hr/>
                <h4 style="color: #FF6600;">Datos de Contaminación</h4>
                <b>🌫️  TVOC:</b> <span style="font-size: 18px; font-weight: bold;">{tvoc} ppb</span><br/>
                <b>💨 eCO2:</b> {eco2} ppm<br/>
                <b>🔬 H2 raw:</b> {h2}<br/>
                <b>🔬 Ethanol raw:</b> {ethanol}<br/>
                <hr/>
                <b>📊 Calidad del Aire:</b> {calidad}<br/>
                <b>🔍 Firma Detectada:</b> {firma}<br/>
                <i>Altura cilindro: {altura_cilindro:.1f} m</i>
            </div>
            """
        
        # Añadir trayectoria
        path = kml.newlinestring(name="Trayectoria CanSat")
        path.coords = [(row['lon'], row['lat'], row['alt']) 
                       for _, row in df_gps.iterrows()]
        path.altitudemode = simplekml.AltitudeMode.absolute
        path.style.linestyle.color = 'ffffffff'
        path.style.linestyle.width = 5
        
        # Marcadores inicio/fin
        inicio = kml.newpoint(name="🚀 Inicio")
        inicio.coords = [(df_gps.iloc[0]['lon'], 
                         df_gps.iloc[0]['lat'], 
                         df_gps.iloc[0]['alt'])]
        inicio.style.iconstyle.color = simplekml.Color.green
        inicio.style.iconstyle.scale = 2
        
        fin = kml.newpoint(name="🎯 Aterrizaje")
        fin.coords = [(df_gps.iloc[-1]['lon'], 
                      df_gps.iloc[-1]['lat'], 
                      df_gps.iloc[-1]['alt'])]
        fin.style.iconstyle.color = simplekml.Color.red
        fin.style.iconstyle.scale = 2
        
        # Guardar KML
        kml.save(OUTPUT_KML)
        
        print(f"✅ KML generado exitosamente: {OUTPUT_KML}")
        print(f"\n📊 Resumen:")
        print(f"   • Cilindros generados: {len(df_gps)}")
        print(f"   • Altura máxima: {max_tvoc * ESCALA_ALTURA:.0f} m")
        print(f"   • Área cubierta: {len(df_gps) * RADIO_CILINDRO * 2:.1f} m")
        print(f"\n💡 Abre el archivo en Google Earth para visualizar")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {INPUT_FILE}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
