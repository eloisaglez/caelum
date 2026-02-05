#!/usr/bin/env python3
"""
========================================
CANSAT MISIÓN 2 - ANÁLISIS DE DATOS
========================================

Genera mapas de calor interactivos a partir de datos
de contaminación georreferenciados del CanSat

Formato CSV esperado:
equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,h2,ethanol,accX,accY,accZ,gyrX,gyrY,gyrZ

Autor: IES Diego Velázquez - Equipo CAELUM
Fecha: Febrero 2026
"""

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.pyplot as plt
from datetime import datetime

# ============ CONFIGURACIÓN ============
INPUT_FILE = 'datos_vuelo.csv'
OUTPUT_HTML = 'mapa_calor_cansat.html'
OUTPUT_PNG = 'analisis_cansat.png'

THRESHOLDS = {
    'excelente': 220,
    'buena': 660,
    'moderada': 2200,
    'mala': 5500
}

# ============ FUNCIONES ============

def clasificar_calidad_aire(tvoc):
    if tvoc < THRESHOLDS['excelente']:
        return 'Excelente', '#00FF00'
    elif tvoc < THRESHOLDS['buena']:
        return 'Buena', '#7FFF00'
    elif tvoc < THRESHOLDS['moderada']:
        return 'Moderada', '#FFFF00'
    elif tvoc < THRESHOLDS['mala']:
        return 'Mala', '#FF8C00'
    else:
        return 'Muy Mala', '#FF0000'

def detectar_firma_combustion(row):
    tvoc = row['tvoc']
    eco2 = row['eco2']
    h2 = row['h2']
    ethanol = row['ethanol']
    
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

def crear_mapa_calor(df):
    print("🗺️  Generando mapa de calor...")
    
    df_gps = df[(df['lat'] != 0) & (df['lon'] != 0)].copy()
    
    if len(df_gps) == 0:
        print("❌ No hay puntos con GPS válido")
        return None
    
    center_lat = df_gps['lat'].mean()
    center_lon = df_gps['lon'].mean()
    
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery'
    )
    
    # Mapa de calor
    heat_data = [[row['lat'], row['lon'], min(row['tvoc'] / 5000, 1.0)] 
                 for _, row in df_gps.iterrows()]
    
    HeatMap(heat_data, name='Mapa de Calor TVOC', min_opacity=0.4,
            max_opacity=0.8, radius=25, blur=15,
            gradient={0.0: '#00FF00', 0.3: '#FFFF00', 0.6: '#FF8C00', 1.0: '#FF0000'}
    ).add_to(mapa)
    
    # Marcadores
    marker_cluster = MarkerCluster(name='Puntos de Medición').add_to(mapa)
    equipo = df_gps['equipo'].iloc[0] if 'equipo' in df_gps.columns else 'CAELUM'
    
    for idx, row in df_gps.iterrows():
        calidad, color = clasificar_calidad_aire(row['tvoc'])
        firma = detectar_firma_combustion(row)
        
        popup_html = f"""
        <div style="font-family: Arial; width: 280px;">
            <h4 style="color: #ffd700;">🛰️ {equipo} #{int(row['paquete'])}</h4>
            <hr>
            <b>📍</b> {row['lat']:.6f}, {row['lon']:.6f}<br>
            <b>📏 Alt:</b> {row['altBaro']:.0f}m | <b>🛰️</b> {int(row['sats'])} sat<br>
            <hr>
            <b>🌫️ TVOC:</b> <span style="color:{color}; font-weight:bold;">{int(row['tvoc'])} ppb</span><br>
            <b>💨 eCO2:</b> {int(row['eco2'])} ppm<br>
            <b>🔬 H2:</b> {int(row['h2'])} | <b>Eth:</b> {int(row['ethanol'])}<br>
            <hr>
            <b>Calidad:</b> {calidad}<br>
            <b>Firma:</b> {firma}
        </div>
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"#{int(row['paquete'])} TVOC:{int(row['tvoc'])}ppb",
            icon=folium.Icon(color='red' if row['tvoc'] > 1000 else 
                            'orange' if row['tvoc'] > 500 else 'green')
        ).add_to(marker_cluster)
    
    # Trayectoria
    coords = [[row['lat'], row['lon']] for _, row in df_gps.iterrows()]
    if len(coords) > 1:
        folium.PolyLine(coords, color='#ffd700', weight=3, opacity=0.8).add_to(mapa)
    
    # Inicio/Fin
    folium.Marker(coords[0], popup='🚀 Inicio', 
                  icon=folium.Icon(color='green', icon='play')).add_to(mapa)
    folium.Marker(coords[-1], popup='🎯 Aterrizaje', 
                  icon=folium.Icon(color='red', icon='stop')).add_to(mapa)
    
    # Leyenda
    leyenda = f'''
    <div style="position:fixed; bottom:50px; left:50px; width:200px;
                background:rgba(0,0,0,0.85); border:2px solid #ffd700;
                padding:12px; border-radius:8px; color:white; font-size:13px;">
    <h4 style="color:#ffd700; margin:0 0 10px 0; text-align:center;">🛰️ {equipo}</h4>
    <p style="margin:3px 0;"><span style="color:#00FF00;">●</span> Excelente (&lt;220)</p>
    <p style="margin:3px 0;"><span style="color:#7FFF00;">●</span> Buena (220-660)</p>
    <p style="margin:3px 0;"><span style="color:#FFFF00;">●</span> Moderada (660-2200)</p>
    <p style="margin:3px 0;"><span style="color:#FF8C00;">●</span> Mala (2200-5500)</p>
    <p style="margin:3px 0;"><span style="color:#FF0000;">●</span> Muy Mala (&gt;5500)</p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda))
    
    folium.LayerControl().add_to(mapa)
    mapa.save(OUTPUT_HTML)
    print(f"✅ Mapa guardado: {OUTPUT_HTML}")
    return mapa

def crear_graficas(df):
    print("📊 Generando gráficas...")
    
    equipo = df['equipo'].iloc[0] if 'equipo' in df.columns else 'CAELUM'
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Análisis CanSat {equipo} - Misión 2', fontsize=16, fontweight='bold')
    
    t = df['timestamp'] / 1000
    
    # TVOC vs Tiempo
    axes[0,0].plot(t, df['tvoc'], 'b-', lw=2)
    axes[0,0].axhline(220, color='g', ls='--', label='Excelente')
    axes[0,0].axhline(660, color='y', ls='--', label='Buena')
    axes[0,0].axhline(2200, color='orange', ls='--', label='Moderada')
    axes[0,0].set_xlabel('Tiempo (s)')
    axes[0,0].set_ylabel('TVOC (ppb)')
    axes[0,0].set_title('Evolución TVOC')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # TVOC vs eCO2
    sc = axes[0,1].scatter(df['tvoc'], df['eco2'], c=df['tvoc'], cmap='RdYlGn_r', 
                           s=80, alpha=0.7, edgecolors='black')
    axes[0,1].set_xlabel('TVOC (ppb)')
    axes[0,1].set_ylabel('eCO2 (ppm)')
    axes[0,1].set_title('Correlación TVOC vs eCO2')
    axes[0,1].grid(True, alpha=0.3)
    plt.colorbar(sc, ax=axes[0,1], label='TVOC')
    
    # Distribución TVOC
    axes[1,0].hist(df['tvoc'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    axes[1,0].axvline(df['tvoc'].mean(), color='red', ls='--', lw=2, 
                      label=f'Media: {df["tvoc"].mean():.0f}')
    axes[1,0].set_xlabel('TVOC (ppb)')
    axes[1,0].set_ylabel('Frecuencia')
    axes[1,0].set_title('Distribución TVOC')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3, axis='y')
    
    # H2 y Ethanol
    ax2 = axes[1,1].twinx()
    l1, = axes[1,1].plot(t, df['h2'], 'g-', lw=2, label='H2')
    l2, = ax2.plot(t, df['ethanol'], 'orange', lw=2, label='Ethanol')
    axes[1,1].set_xlabel('Tiempo (s)')
    axes[1,1].set_ylabel('H2 (raw)', color='g')
    ax2.set_ylabel('Ethanol (raw)', color='orange')
    axes[1,1].set_title('Firmas de Combustión (H2/Ethanol)')
    axes[1,1].legend(handles=[l1, l2], loc='upper right')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches='tight')
    print(f"✅ Gráficas guardadas: {OUTPUT_PNG}")
    plt.close()

def generar_informe(df):
    equipo = df['equipo'].iloc[0] if 'equipo' in df.columns else 'CAELUM'
    
    print("\n" + "="*60)
    print(f"📋 INFORME - {equipo} MISIÓN 2")
    print("="*60)
    
    print(f"\n📊 GENERAL:")
    print(f"   Muestras: {len(df)}")
    print(f"   Duración: {df['timestamp'].max()/1000:.1f}s")
    print(f"   Con GPS: {len(df[(df['lat']!=0) & (df['lon']!=0)])}")
    
    print(f"\n📏 ALTITUD:")
    print(f"   Máx: {df['altBaro'].max():.0f}m | Mín: {df['altBaro'].min():.0f}m")
    
    print(f"\n🌫️ TVOC:")
    print(f"   Rango: {df['tvoc'].min()}-{df['tvoc'].max()} ppb")
    print(f"   Media: {df['tvoc'].mean():.0f} ppb")
    
    print(f"\n🔬 FIRMAS:")
    for firma in df.apply(detectar_firma_combustion, axis=1).unique():
        n = (df.apply(detectar_firma_combustion, axis=1) == firma).sum()
        print(f"   {firma}: {n} ({n/len(df)*100:.0f}%)")
    
    print("="*60 + "\n")

def main():
    print("🚀 Análisis CanSat Misión 2\n")
    
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"✅ {len(df)} registros cargados\n")
        
        generar_informe(df)
        crear_mapa_calor(df)
        crear_graficas(df)
        
        print("\n✅ COMPLETADO")
        print(f"   • {OUTPUT_HTML}")
        print(f"   • {OUTPUT_PNG}")
        
    except FileNotFoundError:
        print(f"❌ No se encontró {INPUT_FILE}")
        print("   Exporta los datos con CSV y guárdalos como 'datos_vuelo.csv'")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
