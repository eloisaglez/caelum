# Análisis Post-Vuelo — CanSat CAELUM

Scripts Python para analizar y visualizar los datos del CanSat después del vuelo.

---

## Requisitos

```bash
pip install pandas numpy folium matplotlib
```

---

## Formato de Datos CSV

El archivo CSV viene de la **tarjeta MicroSD** del CanSat (`datos_SD.csv`) o del backup de RAM (`CSV_RAM`). Tiene 25 columnas:

```csv
timestamp,datetime,lat,lon,alt,alt_mar,sats,temp_hs,hum_hs,temp_scd,hum_scd,temp_lps,presion,co2,pm1_0,pm2_5,pm10,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,fase
0,2026-03-17T11:30:00,40.405200,-3.993100,998.2,1648.2,9,5.8,68.1,5.9,67.0,6.2,901.2,421,4.1,6.2,9.8,0.05,-0.02,9.80,1.2,-0.5,0.3,caida_libre
```

**Sensores de temperatura (validación cruzada):**
- `temp_hs` → HS300x (integrado, referencia principal)
- `temp_scd` → SCD40 (externo, validación cruzada)
- `temp_lps` → LPS22HB (integrado, puede ser ~0.5°C más alto por calor del procesador)

**CO₂ — trazador de estabilidad atmosférica**, no indicador de calidad del aire.

---

## Script de Análisis

### analizar_vuelo.py

**Función:** Análisis completo — perfiles verticales, inversiones térmicas, validación cruzada de sensores, mapa interactivo e informe.

**Uso:**
```bash
python analizar_vuelo.py <fichero.csv>
```

**Genera la carpeta `analisis_vuelo/` con:**

| Archivo | Contenido |
|---------|-----------|
| `graf_1_perfil_vertical.png` | PM1.0, PM2.5, PM10 y CO₂ por altitud + perfil térmico |
| `graf_2_inversiones_termicas.png` | Detección de capas de acumulación e inversiones térmicas |
| `graf_3_validacion_cruzada.png` | Comparativa HS300x vs SCD40 vs LPS22HB (T y HR) |
| `graf_4_mision_primaria.png` | Altitud por fases, presión vs ISA, velocidad, trayectoria GPS |
| `mapa_vuelo.html` | Mapa interactivo con trayectoria coloreada por PM2.5 |
| `informe_vuelo.txt` | Resumen estadístico + diagnóstico atmosférico automático |

---

### generar_kml.py

**Función:** Genera un archivo KML para visualizar la trayectoria del vuelo en **Google Earth** en 3D, coloreada por PM2.5.

**Uso:**
```bash
python generar_kml.py <fichero.csv>
```

**Genera:**

| Archivo | Contenido |
|---------|-----------|
| `analisis_vuelo/trayectoria_vuelo.kml` | Trayectoria 3D coloreada por PM2.5 + puntos de datos + marcadores |

**Para visualizar:**
1. Abrir Google Earth
2. Archivo → Abrir → `analisis_vuelo/trayectoria_vuelo.kml`
3. La trayectoria aparece sobre el terreno real con altitud 3D

**Colores por PM2.5 (OMS):**

| Color | PM2.5 (µg/m³) | Calidad |
|-------|---------------|---------|
| 🟢 Verde | 0–12 | Excelente |
| 🟡 Amarillo | 12–35 | Buena |
| 🟠 Naranja | 35–55 | Moderada |
| 🔴 Rojo | 55–150 | Mala |
| 🔴 Rojo oscuro | >150 | Muy Mala |

> Requiere fix GPS — si no hay coordenadas válidas en el CSV no se genera el KML.

---

## Fuentes de Datos

El script acepta cualquier CSV con las 25 columnas, independientemente del origen:

| Fichero | Origen | Cuándo usar |
|---------|--------|-------------|
| `datos_SD.csv` | Tarjeta MicroSD del CanSat | Fuente principal — máxima resolución |
| `datos_RAM.csv` | RAM backup via `extraer_ram.py` | Si la SD falla |
| `datos_radio.csv` | Telemetría en tierra via `receptor_telemetria.py` | **Si no se recupera el CanSat** |
| `datos_simulacion.csv` | Simulador | Pruebas y desarrollo |

> ⚠️ **`datos_radio.csv` es el seguro de datos crítico.** Si el CanSat cae en un lugar inaccesible (tejado, árbol, agua...) los datos de la SD y la RAM se pierden. Pero `datos_radio.csv` ya está en el PC de tierra desde el momento del aterrizaje. Por eso `receptor_telemetria.py` debe estar corriendo siempre durante el vuelo.

---

## Flujo de Trabajo

1. **Elegir el fichero** según la situación (ver tabla anterior)
2. **Ejecutar:**

```bash
python analizar_vuelo.py <fichero.csv>
```

3. **Abrir** los resultados en `analisis_vuelo/`

---

## Interpretación de Resultados

### CO₂ — Confirmación de sensor y atmósfera

A ~1000 m de altitud el CO₂ es siempre **~420 ppm** (fondo atmosférico global). Las fuentes de combustión del suelo no son detectables a esa altura.

| Lectura CO₂ | Interpretación |
|-------------|----------------|
| ~420 ppm constante durante todo el vuelo | ✅ Sensor funcionando — atmósfera normal |
| Variación > 30 ppm | ⚠️ Posible ruido de sensor (precisión SCD40 = ±10 ppm) |

> El valor principal del SCD40 es su **temperatura y humedad** para validación cruzada, no el CO₂.

### Partículas PM2.5 — perfil vertical

| PM2.5 (µg/m³) | Calidad OMS |
|---------------|-------------|
| 0–12 | 🟢 Excelente |
| 12–35 | 🟢 Buena |
| 35–55 | 🟡 Moderada |
| 55–150 | 🟠 Mala |
| >150 | 🔴 Muy Mala |

### Patrón de inversión térmica

```
Alt ↑ + Temperatura ↑ + PM2.5 ↑ = partículas atrapadas
→ al bajar la temperatura nocturna descienden al suelo
→ riesgo real para salud respiratoria (asma, EPOC)
```

### Perfil de contaminación — qué buscar

```
PM2.5 BAJO en todo el perfil      → Aire limpio durante todo el vuelo ✓
PM2.5 ALTO en capas bajas (<300m) → Partículas cerca del suelo (tráfico, polvo)
PM2.5 ALTO en capa intermedia     → Posible inversión térmica atrapando partículas
PM2.5 DECRECE con la altitud      → Fuente en superficie, dispersión normal
```

### Validación cruzada de temperatura

- **ΔT < 2 °C** entre HS300x y SCD40 → sensores correctos
- **ΔT > 3 °C** → posible fallo de sensor

---

## Ejemplo de Informe Generado

```
═══════════════════════════════════════════════════
  CANSAT — INFORME POST-VUELO
  IES Diego Velázquez · Equipo Caelum
═══════════════════════════════════════════════════

Muestras totales:  108
Duración vuelo:    108 s (1.8 min)
Altitud máxima:    997.3 m (relativa al lanzamiento)

──── TEMPERATURA (Validación cruzada) ────
  HS300x  media: 9.1 °C
  SCD40   media: 9.2 °C
  LPS22HB media: 9.5 °C
  ΔT HS-SCD media: 0.31 °C

──── CO₂ (Trazador de estabilidad atmosférica) ────
  Media: 449 ppm  |  rango: 115 ppm
  → CAPAS DETECTADAS (Δ = 115 ppm > 20 ppm) ⚠️

──── INVERSIONES TÉRMICAS ────
  Capas con inversión detectadas: 3
  Altitudes: [200, 250, 300] m
  → Riesgo: partículas pueden descender al suelo por la noche
```

---

**Equipo:** CAELUM
**Centro:** IES Diego Velázquez
**Proyecto:** CanSat Misión 2 — Detección de Firmas de Combustión
**Fecha:** Febrero 2026
