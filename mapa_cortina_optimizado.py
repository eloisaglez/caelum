"""
CANSAT - Mapa de Cortina de Humo (Versión Optimizada)
Visualización realista de gases con efecto volumétrico
"""

import pandas as pd
import folium
import numpy as np

# ============================================
# CONFIGURACIÓN
# ============================================

MOSTRAR_TRAYECTORIA = False  # Cambiar a True para mostrar el camino
TRAYECTORIA_COLOR = '#ffd700'  # Dorado
TRAYECTORIA_GROSOR = 2
TRAYECTORIA_OPACIDAD = 0.5

# ============================================
# CARGAR DATOS
# ============================================

try:
    df = pd.read_csv('mission2.csv')
    print(f"✅ Datos cargados: {len(df)} puntos")
except:
    print("⚠️  Generando datos de ejemplo...")
    np.random.seed(42)
    n_points = 50
    
    lat_center, lon_center = 40.5795, -3.9184
    
    data = {
        'timestamp': pd.date_range('2026-01-18 10:00:00', periods=n_points, freq='5s'),
        'lat': lat_center + np.random.randn(n_points) * 0.002,
        'lon': lon_center + np.random.randn(n_points) * 0.003,
        'alt': np.linspace(500, 50, n_points) + np.random.randn(n_points) * 20,
        'TVOC': np.concatenate([
            np.random.uniform(100, 300, 15),
            np.random.uniform(800, 2000, 10),
            np.random.uniform(300, 600, 10),
            np.random.uniform(1500, 3000, 10),
            np.random.uniform(200, 400, 5)
        ]),
        'eCO2': np.concatenate([
            np.random.uniform(400, 600, 15),
            np.random.uniform(1000, 1500, 10),
            np.random.uniform(600, 900, 10),
            np.random.uniform(1500, 2500, 10),
            np.random.uniform(500, 700, 5)
        ])
    }
    df = pd.DataFrame(data)
    print(f"✅ Datos de ejemplo generados: {len(df)} puntos")

# ============================================
# CREAR MAPA
# ============================================

mapa = folium.Map(
    location=[df['lat'].mean(), df['lon'].mean()],
    zoom_start=15,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery'
)

# ============================================
# FUNCIÓN DE COLORES
# ============================================

def get_smoke_color(tvoc):
    """Retorna color y opacidad según nivel de TVOC"""
    if tvoc < 300:
        return '#66ff66', 0.25  # Verde muy claro, casi transparente
    elif tvoc < 660:
        return '#ffff44', 0.45  # Amarillo
    elif tvoc < 1000:
        return '#ffaa33', 0.55  # Naranja
    elif tvoc < 2000:
        return '#ff4444', 0.65  # Rojo
    else:
        return '#bb2222', 0.75  # Rojo oscuro

# ============================================
# CORTINAS DE HUMO
# ============================================

print("🌫️  Generando cortinas de humo...")

for idx, row in df.iterrows():
    color, opacity = get_smoke_color(row['TVOC'])
    
    # Radio base proporcional a concentración
    radius_base = 25 + (row['TVOC'] / 80)
    
    # Crear 4 círculos concéntricos para efecto volumétrico
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
            weight=0,  # Sin borde
            popup=f"""
                <div style="font-family: monospace; font-size: 13px;">
                    <b>📍 Punto {idx+1}</b><br>
                    <b>TVOC:</b> {row['TVOC']:.0f} ppb<br>
                    <b>eCO₂:</b> {row['eCO2']:.0f} ppm<br>
                    <b>Alt:</b> {row['alt']:.0f} m
                </div>
            """
        ).add_to(mapa)

# ============================================
# TRAYECTORIA (OPCIONAL)
# ============================================

if MOSTRAR_TRAYECTORIA:
    trayectoria_coords = [[row['lat'], row['lon']] for _, row in df.iterrows()]
    folium.PolyLine(
        trayectoria_coords,
        color=TRAYECTORIA_COLOR,
        weight=TRAYECTORIA_GROSOR,
        opacity=TRAYECTORIA_OPACIDAD,
        dashArray='8, 4'
    ).add_to(mapa)
    print("✅ Trayectoria añadida")

# ============================================
# LEYENDA
# ============================================

legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; 
     background-color: rgba(0, 0, 0, 0.85); 
     border: 2px solid #ffd700; 
     z-index: 9999; 
     font-size: 13px; 
     padding: 12px;
     border-radius: 8px;
     color: white;
     font-family: 'Segoe UI', sans-serif;">
     
     <div style="text-align: center; margin-bottom: 10px; border-bottom: 1px solid #ffd700; padding-bottom: 8px;">
         <b style="color: #ffd700; font-size: 14px;">🌫️ CALIDAD DEL AIRE</b>
     </div>
     
     <div style="margin: 5px 0;">
         <span style="color: #66ff66; font-size: 18px;">●</span> 
         <span>Excelente (&lt; 300 ppb)</span>
     </div>
     <div style="margin: 5px 0;">
         <span style="color: #ffff44; font-size: 18px;">●</span> 
         <span>Buena (300-660)</span>
     </div>
     <div style="margin: 5px 0;">
         <span style="color: #ffaa33; font-size: 18px;">●</span> 
         <span>Moderada (660-1000)</span>
     </div>
     <div style="margin: 5px 0;">
         <span style="color: #ff4444; font-size: 18px;">●</span> 
         <span>Mala (1000-2000)</span>
     </div>
     <div style="margin: 5px 0;">
         <span style="color: #bb2222; font-size: 18px;">●</span> 
         <span>Muy Mala (&gt; 2000)</span>
     </div>
     
     <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #555; font-size: 11px; color: #aaa;">
         TVOC: Compuestos Orgánicos Volátiles
     </div>
</div>
'''
mapa.get_root().html.add_child(folium.Element(legend_html))

# ============================================
# TÍTULO
# ============================================

title_html = '''
<div style="position: fixed; 
     top: 10px; left: 50%; transform: translateX(-50%);
     background-color: rgba(0, 0, 0, 0.9); 
     border: 2px solid #ffd700; 
     z-index: 9999; 
     font-size: 16px; 
     padding: 10px 30px;
     border-radius: 8px;
     color: #ffd700;
     font-family: 'Segoe UI', monospace;
     font-weight: bold;
     letter-spacing: 2px;">
     🛰️ CANSAT - CORTINAS DE CONTAMINACIÓN
</div>
'''
mapa.get_root().html.add_child(folium.Element(title_html))

# ============================================
# GUARDAR
# ============================================

mapa.save('mapa_cortina_humo_optimizado.html')
print("\n" + "="*60)
print("✅ MAPA GENERADO: mapa_cortina_humo_optimizado.html")
print("="*60)

# ============================================
# ESTADÍSTICAS
# ============================================

print(f"\n📊 ESTADÍSTICAS:")
print(f"   Puntos medidos: {len(df)}")
print(f"   TVOC promedio: {df['TVOC'].mean():.0f} ppb")
print(f"   TVOC máximo: {df['TVOC'].max():.0f} ppb")
print(f"   Altitud inicial: {df['alt'].max():.0f} m")
print(f"   Altitud final: {df['alt'].min():.0f} m")

# Clasificación
clasificacion = pd.cut(df['TVOC'], 
                       bins=[0, 300, 660, 1000, 2000, 10000],
                       labels=['Excelente', 'Buena', 'Moderada', 'Mala', 'Muy Mala'])

print(f"\n📈 DISTRIBUCIÓN:")
for nivel in ['Excelente', 'Buena', 'Moderada', 'Mala', 'Muy Mala']:
    count = (clasificacion == nivel).sum()
    porcentaje = (count / len(df)) * 100
    print(f"   {nivel}: {count} puntos ({porcentaje:.1f}%)")

print("\n🌐 Abre el archivo HTML en tu navegador")
print("="*60)
