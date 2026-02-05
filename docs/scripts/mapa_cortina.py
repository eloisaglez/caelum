"""
CANSAT MISIÓN 2 - Mapa de Cortina de Humo
Visualización realista de gases con efecto volumétrico

Formato CSV esperado:
equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,h2,ethanol,accX,accY,accZ,gyrX,gyrY,gyrZ

Autor: IES Diego Velázquez - Equipo CAELUM
Fecha: Febrero 2026
"""

import pandas as pd
import folium
import numpy as np

# ============ CONFIGURACIÓN ============
INPUT_FILE = 'datos_vuelo.csv'
OUTPUT_FILE = 'mapa_cortina_humo.html'

MOSTRAR_TRAYECTORIA = True
TRAYECTORIA_COLOR = '#ffd700'
TRAYECTORIA_GROSOR = 3
TRAYECTORIA_OPACIDAD = 0.8

# ============ FUNCIONES ============

def get_smoke_color(tvoc):
    """Retorna color y opacidad según nivel de TVOC"""
    if tvoc < 220:
        return '#66ff66', 0.25  # Verde
    elif tvoc < 660:
        return '#ffff44', 0.45  # Amarillo
    elif tvoc < 2200:
        return '#ffaa33', 0.55  # Naranja
    elif tvoc < 5500:
        return '#ff4444', 0.65  # Rojo
    else:
        return '#bb2222', 0.75  # Rojo oscuro

def detectar_firma(tvoc, eco2, h2, ethanol):
    """Detecta tipo de combustión"""
    if tvoc > 1000 and h2 > 13000:
        return '🚜 Generador Diésel'
    elif tvoc > 500 and ethanol > 18000:
        return '🔥 Biomasa'
    elif tvoc > 300 and eco2 > 1000 and tvoc < 800:
        return '🚗 Tráfico'
    elif tvoc > 5000:
        return '⚠️ Severa'
    elif tvoc < 100:
        return '🌿 Limpio'
    else:
        return '🏭 Industrial'

# ============ CARGAR DATOS ============

print("🛰️  Mapa de Cortina de Humo - CanSat CAELUM\n")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Datos cargados: {len(df)} puntos")
    equipo = df['equipo'].iloc[0] if 'equipo' in df.columns else 'CAELUM'
except FileNotFoundError:
    print(f"❌ No se encontró {INPUT_FILE}")
    print("   Generando datos de ejemplo...")
    
    np.random.seed(42)
    n = 50
    lat_c, lon_c = 40.5795, -3.9184
    
    df = pd.DataFrame({
        'equipo': ['CAELUM'] * n,
        'paquete': range(1, n+1),
        'timestamp': np.arange(0, n*1000, 1000),
        'lat': lat_c + np.random.randn(n) * 0.002,
        'lon': lon_c + np.random.randn(n) * 0.003,
        'altGPS': np.linspace(500, 50, n) + np.random.randn(n) * 10,
        'sats': np.random.randint(6, 12, n),
        'temp': 22 + np.random.randn(n) * 2,
        'hum': 65 + np.random.randn(n) * 5,
        'pres': 1013 + np.random.randn(n) * 2,
        'altBaro': np.linspace(500, 50, n) + np.random.randn(n) * 5,
        'tvoc': np.concatenate([
            np.random.uniform(100, 300, 15),
            np.random.uniform(800, 2000, 10),
            np.random.uniform(300, 600, 10),
            np.random.uniform(1500, 3000, 10),
            np.random.uniform(200, 400, 5)
        ]),
        'eco2': np.concatenate([
            np.random.uniform(400, 600, 15),
            np.random.uniform(1000, 1500, 10),
            np.random.uniform(600, 900, 10),
            np.random.uniform(1500, 2500, 10),
            np.random.uniform(500, 700, 5)
        ]),
        'h2': np.random.uniform(11000, 14000, n),
        'ethanol': np.random.uniform(16000, 19000, n),
        'accX': np.random.randn(n) * 0.5,
        'accY': np.random.randn(n) * 0.5,
        'accZ': 9.8 + np.random.randn(n) * 0.1,
        'gyrX': np.random.randn(n) * 5,
        'gyrY': np.random.randn(n) * 5,
        'gyrZ': np.random.randn(n) * 5,
    })
    equipo = 'CAELUM'
    print(f"✅ Datos de ejemplo: {len(df)} puntos")

# Filtrar GPS válido
df = df[(df['lat'] != 0) & (df['lon'] != 0)]
print(f"📍 Puntos con GPS: {len(df)}")

# ============ CREAR MAPA ============

mapa = folium.Map(
    location=[df['lat'].mean(), df['lon'].mean()],
    zoom_start=16,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery'
)

# ============ CORTINAS DE HUMO ============

print("🌫️  Generando cortinas de humo...")

for idx, row in df.iterrows():
    color, opacity = get_smoke_color(row['tvoc'])
    radius_base = 25 + (row['tvoc'] / 80)
    firma = detectar_firma(row['tvoc'], row['eco2'], row['h2'], row['ethanol'])
    
    # Círculos concéntricos
    for i in range(4):
        expansion = 1 + (i * 0.25)
        opacity_layer = opacity * (0.6 - i * 0.12)
        
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=radius_base * expansion,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=opacity_layer,
            weight=0,
            popup=f"""
                <div style="font-family: monospace; font-size: 13px;">
                    <b>🛰️ {equipo} #{int(row['paquete'])}</b><br>
                    <hr>
                    <b>TVOC:</b> {row['tvoc']:.0f} ppb<br>
                    <b>eCO₂:</b> {row['eco2']:.0f} ppm<br>
                    <b>H2:</b> {row['h2']:.0f}<br>
                    <b>Ethanol:</b> {row['ethanol']:.0f}<br>
                    <hr>
                    <b>Alt:</b> {row['altBaro']:.0f} m<br>
                    <b>Firma:</b> {firma}
                </div>
            """
        ).add_to(mapa)

# ============ TRAYECTORIA ============

if MOSTRAR_TRAYECTORIA:
    coords = [[row['lat'], row['lon']] for _, row in df.iterrows()]
    folium.PolyLine(
        coords,
        color=TRAYECTORIA_COLOR,
        weight=TRAYECTORIA_GROSOR,
        opacity=TRAYECTORIA_OPACIDAD,
        dashArray='8, 4'
    ).add_to(mapa)
    
    # Inicio/Fin
    folium.Marker(coords[0], popup='🚀 Inicio',
                  icon=folium.Icon(color='green', icon='play')).add_to(mapa)
    folium.Marker(coords[-1], popup='🎯 Aterrizaje',
                  icon=folium.Icon(color='red', icon='stop')).add_to(mapa)

# ============ LEYENDA ============

leyenda = f'''
<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; 
     background-color: rgba(0, 0, 0, 0.85); border: 2px solid #ffd700; 
     z-index: 9999; font-size: 13px; padding: 12px; border-radius: 8px;
     color: white; font-family: Arial;">
     
     <div style="text-align: center; margin-bottom: 10px; border-bottom: 1px solid #ffd700; padding-bottom: 8px;">
         <b style="color: #ffd700;">🛰️ {equipo}</b>
     </div>
     
     <div style="margin: 5px 0;"><span style="color: #66ff66;">●</span> Excelente (&lt;220)</div>
     <div style="margin: 5px 0;"><span style="color: #ffff44;">●</span> Buena (220-660)</div>
     <div style="margin: 5px 0;"><span style="color: #ffaa33;">●</span> Moderada (660-2200)</div>
     <div style="margin: 5px 0;"><span style="color: #ff4444;">●</span> Mala (2200-5500)</div>
     <div style="margin: 5px 0;"><span style="color: #bb2222;">●</span> Muy Mala (&gt;5500)</div>
     
     <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #555; font-size: 11px; color: #aaa;">
         TVOC en ppb
     </div>
</div>
'''
mapa.get_root().html.add_child(folium.Element(leyenda))

# Título
titulo = f'''
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
     background-color: rgba(0, 0, 0, 0.9); border: 2px solid #ffd700; 
     z-index: 9999; padding: 10px 30px; border-radius: 8px;
     color: #ffd700; font-family: monospace; font-weight: bold; letter-spacing: 2px;">
     🛰️ {equipo} - CORTINAS DE CONTAMINACIÓN
</div>
'''
mapa.get_root().html.add_child(folium.Element(titulo))

# ============ GUARDAR ============

mapa.save(OUTPUT_FILE)

print("\n" + "="*60)
print(f"✅ MAPA GENERADO: {OUTPUT_FILE}")
print("="*60)

# Estadísticas
print(f"\n📊 ESTADÍSTICAS:")
print(f"   Puntos: {len(df)}")
print(f"   TVOC promedio: {df['tvoc'].mean():.0f} ppb")
print(f"   TVOC máximo: {df['tvoc'].max():.0f} ppb")
print(f"   Altitud: {df['altBaro'].max():.0f}m → {df['altBaro'].min():.0f}m")

# Clasificación
print(f"\n📈 DISTRIBUCIÓN:")
niveles = ['Excelente', 'Buena', 'Moderada', 'Mala', 'Muy Mala']
umbrales = [0, 220, 660, 2200, 5500, 99999]
for i, nivel in enumerate(niveles):
    n = len(df[(df['tvoc'] >= umbrales[i]) & (df['tvoc'] < umbrales[i+1])])
    print(f"   {nivel}: {n} ({n/len(df)*100:.0f}%)")

print(f"\n🌐 Abre {OUTPUT_FILE} en tu navegador")
print("="*60)
