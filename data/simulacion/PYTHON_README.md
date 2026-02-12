# 🐍 Scripts Python - Análisis Post-Vuelo

## Descripción

Scripts para analizar los datos del CanSat después del vuelo y generar visualizaciones.

---

## 📁 Archivos

| Archivo | Función |
|---------|---------|
| `simulador_vuelo.py` | Genera datos simulados para testing |
| `analizar_vuelo.py` | Analiza datos y genera mapas/gráficas |

---

## 🚀 Uso Rápido

### Opción 1: Google Colab (recomendado)

1. Abre https://colab.research.google.com
2. Sube `simulador_vuelo.py`
3. Ejecuta en celdas separadas:

```python
# Celda 1: Instalar librerías
!pip install folium simplekml
```

```python
# Celda 2: Generar datos simulados
!python simulador_vuelo.py
```

```python
# Celda 3: Analizar (copiar contenido de analizar_vuelo.py y cambiar el final)
```

4. Descarga los archivos del panel izquierdo (📁)

### Opción 2: Local (VS Code / Anaconda)

```bash
# Instalar dependencias
pip install pandas numpy folium matplotlib simplekml

# Generar datos de prueba
python simulador_vuelo.py

# Analizar vuelo
python analizar_vuelo.py vuelo_brunete_17marzo.csv
```

---

## 📦 Dependencias

```
pandas
numpy
folium
matplotlib
simplekml
```

Instalar con:
```bash
pip install pandas numpy folium matplotlib simplekml
```

---

## 📊 Archivos Generados

| Archivo | Descripción | Abrir con |
|---------|-------------|-----------|
| `mapa_calor.html` | Mapa interactivo con trayectoria y marcadores | Navegador web |
| `firmas_combustion.kml` | Visualización 3D del vuelo | Google Earth |
| `analisis_graficas.png` | Gráficas de CO2, PM2.5, correlación y perfil | Visor de imágenes |

---

## 📈 Gráficas Generadas

El análisis genera 4 gráficas:

### 1. CO2 vs Tiempo
Evolución del CO2 durante el descenso. Líneas punteadas indican umbrales de calidad.

### 2. Partículas vs Tiempo
PM1.0, PM2.5 y PM10 durante el vuelo. La línea verde punteada es el umbral OMS (12 µg/m³).

### 3. Correlación CO2 vs PM2.5
Relación entre ambos contaminantes. El color indica la altitud. Permite identificar firmas de combustión:
- **CO2 alto + PM2.5 alto** → Combustión activa
- **CO2 bajo + PM2.5 alto** → Polvo sin combustión
- **CO2 bajo + PM2.5 bajo** → Aire limpio

### 4. Perfil de Vuelo
- **Línea negra** = Altitud (eje izquierdo)
- **Área roja** = PM2.5 (eje derecho)

Muestra cómo la contaminación aumenta al acercarse al suelo.

---

## 🎯 Simulador de Vuelo

`simulador_vuelo.py` genera datos realistas basados en:

| Parámetro | Valor |
|-----------|-------|
| Ubicación | Aeródromo de Brunete (Madrid) |
| Fecha | 17 de marzo 2026 |
| Altitud lanzamiento | 1000 m |
| Altitud terreno | 650 m sobre nivel del mar |
| Peso CanSat | 325 g |
| Velocidad descenso | 9 m/s (con paracaídas) |
| Viento | 2.5 m/s norte, 1.5 m/s este |

### Zonas de contaminación simuladas:

| Altitud | CO2 (ppm) | PM2.5 (µg/m³) | Descripción |
|---------|-----------|---------------|-------------|
| 800-1000m | ~415 | ~8 | Aire limpio |
| 500-800m | ~430 | ~15 | Capa de mezcla |
| 300-500m | ~480 | ~35 | Influencia M-501 |
| 100-300m | ~520 | ~55 | Capa límite urbana |
| 0-100m | ~580 | ~75 | Cerca del suelo |

---

## 🔍 Detección de Firmas

El análisis detecta automáticamente el tipo de fuente:

| Firma | CO2 | PM2.5 | Indica |
|-------|-----|-------|--------|
| 🌿 Aire Limpio | <450 | <12 | Sin contaminación |
| 🚗 Tráfico Vehicular | 500-700 | 40-100 | Carretera cercana |
| 🚜 Generador Diésel | >600 | >80 | Maquinaria |
| 🔥 Combustión activa | >700 | >100 | Fuego/quema |
| 🌫️ Polvo | <480 | >50 | Polvo sin combustión |
| 🏭 Fuente mixta | Variable | Variable | Múltiples fuentes |

---

## 📝 Formato CSV

Los datos deben tener estas columnas:

```csv
timestamp,lat,lon,alt,sats,co2,pm1_0,pm2_5,pm10,temp,hum
0,40.405200,-3.993100,1000.0,9,415,5,8,12,5.5,55
1,40.405220,-3.993080,991.0,10,418,6,9,13,5.7,56
...
```

| Columna | Descripción | Unidad |
|---------|-------------|--------|
| timestamp | Tiempo desde inicio | segundos |
| lat | Latitud | grados |
| lon | Longitud | grados |
| alt | Altitud sobre terreno | metros |
| sats | Satélites GPS | - |
| co2 | CO2 (SCD40) | ppm |
| pm1_0 | PM1.0 (HM3301) | µg/m³ |
| pm2_5 | PM2.5 (HM3301) | µg/m³ |
| pm10 | PM10 (HM3301) | µg/m³ |
| temp | Temperatura | °C |
| hum | Humedad | % |

---

## 💡 Tips

- **Sin WiFi el día del concurso:** Instala VS Code + dependencias antes
- **Datos reales:** Reemplaza `vuelo_brunete_17marzo.csv` por tus datos
- **Google Earth:** El KML muestra cilindros 3D proporcionales a la contaminación
- **Mapa HTML:** Haz click en los marcadores para ver detalles de cada punto

---

**IES Diego Velázquez**  
**Erasmus+ STEMadrid Network**  
**Febrero 2026**
