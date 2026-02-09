# Análisis Post-Vuelo - CanSat CAELUM

## Descripción

Scripts Python para analizar y visualizar los datos del CanSat después del vuelo.

---

## Requisitos

```bash
pip install pandas numpy folium matplotlib seaborn simplekml
```

---

## Formato de Datos CSV

El archivo `datos_vuelo.csv` debe tener este formato (exportado del CanSat con el comando `CSV`):

```csv
equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,h2,ethanol,accX,accY,accZ,gyrX,gyrY,gyrZ
CAELUM,1,1000,40.579500,-3.918400,498,8,22.50,65.00,1013.25,497,412,850,13500,17200,0.05,-0.02,9.80,1.2,-0.5,0.3
CAELUM,2,2000,40.579510,-3.918390,496,8,22.45,65.10,1013.30,495,408,860,13600,17300,0.03,-0.01,9.81,1.1,-0.4,0.2
```

---

## Scripts Disponibles

### 1. analizar_mision2.py

**Función:** Análisis completo con mapa de calor y gráficas.

**Uso:**
```bash
python analizar_mision2.py
```

**Genera:**
- `mapa_calor_cansat.html` - Mapa interactivo con capa de calor
- `analisis_cansat.png` - 4 gráficas de análisis

---

### 2. mapa_cortina.py

**Función:** Mapa con efecto de cortinas de humo volumétricas.

**Uso:**
```bash
python mapa_cortina.py
```

**Genera:**
- `mapa_cortina_humo.html` - Mapa con círculos concéntricos

---

### 3. generar_kml.py

**Función:** Archivo KML 3D para Google Earth.

**Uso:**
```bash
python generar_kml.py
```

**Genera:**
- `firmas_combustion_3d.kml` - Cilindros 3D proporcionales a TVOC

---

## Flujo de Trabajo

1. **Recuperar el CanSat** después del vuelo
2. **Conectar por USB** y abrir Monitor Serie (9600 baud)
3. **Escribir `CSV`** para exportar datos
4. **Copiar** el texto y guardar como `datos_vuelo.csv`
5. **Ejecutar scripts:**

```bash
cd analisis_post_vuelo/scripts
python analizar_mision2.py
python mapa_cortina.py
python generar_kml.py
```

6. **Abrir** los archivos generados en el navegador/Google Earth

---

## Clasificación de Calidad del Aire

| TVOC (ppb) | Clasificación | Color |
|------------|---------------|-------|
| 0-220 | Excelente | 🟢 Verde |
| 220-660 | Buena | 🟡 Amarillo |
| 660-2200 | Moderada | 🟠 Naranja |
| 2200-5500 | Mala | 🔴 Rojo |
| >5500 | Muy Mala | ⛔ Rojo oscuro |

---

## Detección de Firmas de Combustión

Los valores H2 y Ethanol permiten identificar la fuente:

| Firma | TVOC | H2 raw | Ethanol raw |
|-------|------|--------|-------------|
| 🚜 Generador Diésel | >1000 | >13000 | Normal |
| 🔥 Biomasa/Fuego | >500 | Normal | >18000 |
| 🚗 Tráfico Vehicular | 300-800 | Elevado | Elevado |
| 🌿 Aire Limpio | <100 | ~12500 | ~16000 |
| 🏭 Industrial | Variable | Variable | Variable |

---

## Archivos Generados

| Archivo | Descripción | Visualizar |
|---------|-------------|------------|
| mapa_calor_cansat.html | Mapa de calor interactivo | Navegador |
| mapa_cortina_humo.html | Cortinas de humo volumétricas | Navegador |
| firmas_combustion_3d.kml | Cilindros 3D | Google Earth |
| analisis_cansat.png | Gráficas estadísticas | Visor imágenes |

---

## Ejemplo de Análisis

```
📋 INFORME - CAELUM MISIÓN 2
============================================

📊 GENERAL:
   Muestras: 180
   Duración: 180.0s
   Con GPS: 175

📏 ALTITUD:
   Máx: 520m | Mín: 45m

🌫️ TVOC:
   Rango: 85-2340 ppb
   Media: 456 ppb

🔬 FIRMAS:
   🚗 Tráfico: 45 (25%)
   🌿 Aire Limpio: 80 (44%)
   🏭 Industrial: 35 (19%)
   🔥 Biomasa: 20 (11%)
```

---

**Equipo:** CAELUM  
**Centro:** IES Diego Velázquez  
**Proyecto:** CanSat Misión 2  
**Fecha:** Febrero 2026
