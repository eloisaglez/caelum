# CanSat CAELUM — Análisis de Capas Atmosféricas y Perfiles de Partículas

[![Arduino](https://img.shields.io/badge/Arduino_Nano_33_BLE-00979D?style=flat&logo=Arduino)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)

---

## Descripción

**CanSat Misión 2** es un proyecto de monitoreo ambiental desde satélite miniatura que construye perfiles verticales de partículas (PM1.0, PM2.5, PM10) y parámetros atmosféricos georreferenciados mediante GPS durante su descenso desde ~1000 m.

**Objetivos científicos:**
1. **Perfil vertical de partículas** — detectar capas de acumulación de PM2.5 e identificar inversiones térmicas (altitud↑ + temperatura↑ + PM2.5↑ = partículas atrapadas)
2. **Estabilidad atmosférica** — el CO₂ actúa como trazador: si se mantiene constante con la altitud (~420 ppm) la atmósfera está bien mezclada; variaciones indican capas diferenciadas o fuentes locales de combustión
3. **Validación cruzada T+HR** — tres sensores de temperatura independientes (HS300x, SCD40, LPS22HB) y dos de humedad (HS300x, SCD40) permiten detectar errores de sensor y medir gradientes reales con la altitud
4. **Salud respiratoria** — las partículas acumuladas en capas a 200-500 m descienden a nivel de suelo por la noche (inversión térmica nocturna), causando picos de contaminación que afectan a personas con asma y problemas respiratorios

---

## Características

| Componente | Descripción |
|------------|-------------|
| **Microcontrolador** | Arduino Nano 33 BLE Sense Rev2 |
| **Sensor CO₂** | SCD40: CO₂ real (NDIR) + Temperatura + Humedad — trazador de estabilidad atmosférica |
| **Sensor Partículas** | HM3301: PM1.0, PM2.5, PM10 (láser) — perfil vertical e inversiones térmicas |
| **Temp/Humedad integrado** | HS300x + LPS22HB — validación cruzada triple de temperatura |
| **Posicionamiento** | GPS G10A-F30 |
| **Almacenamiento** | MicroSD — CSV 27 columnas (respaldo local) |
| **Telemetría** | APC220: RF 434 MHz en tiempo real |
| **Panel Web** | Firebase + Telemetría en vivo |
| **Análisis** | Python: Perfiles verticales + Detección de inversiones + KML |

---

## Estructura del Repositorio

```
cansat-mision2/
│
├── design/                        
│   ├── structural/                  # Carcasa
│   ├── recovery/                    # Paracaídas
│   ├── electronics/                 # Circuitos
│   └── comms/                       # Antena
│
├── software/
│   ├── pruebas/                     # Programas individuales de cada sensor
│   │   ├── PROGRAMA_1_SENSORES_INTEGRADOS.ino
│   │   ├── PROGRAMA_2_SCD40_CO2.ino
│   │   ├── PROGRAMA_3_HM3301_PM25.ino
│   │   ├── PROGRAMA_4_GPS.ino
│   │   ├── PROGRAMA_5_MICROSD.ino
│   │   ├── PROGRAMA_6_APC220_CONFIG.ino
|   |   ├── PROGRAMA_7_GRABACION_RAM.ino
│   │   └── Otros
|   |
│   │
│   ├── vuelo/                       # Programa final + panel web
│   │   ├── CANSAT_VUELO_INTEGRADO.ino
│   │   └── panel_web/
│   │       ├── caelum_dashboard.html
│   │       ├── caelum_playback.py
│   │       └── receptor_telemetria.py
│   │
│   ├── post_vuelo/                  # Análisis después del vuelo
│   │   ├── analizar_vuelo.py
│   │   ├── generar_kml.py
│   │   ├── extraer_ram.py
│   │   ├── GUIA_POST_VUELO.md
│   │   ├── GUIA_RAPIDA_POST_VUELO.txt
│   │   └── README_post_vuelo.md
│   │
│   └── simulacion/                  # Simuladores pre-vuelo
│       ├── simulador_inversion_termica.py   # Escenario con inversión y PM2.5 alto
│       ├── simulador_sin_contaminacion.py   # Escenario limpio sin inversión
│       └── README_simulacion.md
│
├── documentation/
│   ├── pruebas/                     # Guías de cada sensor
│   │   ├── DOCUMENTO_1_SENSORES_INTEGRADOS.md
│   │   ├── DOCUMENTO_2_SCD40_CO2.md
│   │   ├── DOCUMENTO_3_HM3301_PM25.md
│   │   ├── DOCUMENTO_4_GPS.md
│   │   ├── DOCUMENTO_5_MICROSD.md
│   │   ├── DOCUMENTO_6_APC220_TELEMETRIA.md
│   │   └── DOCUMENTO_7_GRABACION_RAM.md
│   │
│   ├── vuelo/                       # Preparación del vuelo
│   │   ├── INDICE_DE_PRUEBAS_FINAL.md
│   │   ├── CHECKLIST_VUELO.md
│   │   └── IMPORTANTE_CAMBIO_FRECUENCIA.md
│   │
│   ├── troubleshooting/             # Solución de problemas
│   │   └── TROUBLESHOOTING_COMPLETO.md
│   │
│   └── INDEX.md
│
├── data/                            # Datos de vuelos; CSVs, Gráficas, mapas, KML 
│   ├── vuelos/                      
│   └── Simulación/                  # Datos generados con un Python 
│
└── README.md
```

---

## Inicio Rápido

### 1. Probar sensores integrados

```bash
1. Abrir: software/pruebas/PROGRAMA_1_SENSORES_INTEGRADOS.ino
2. Tools → Board → Arduino Nano 33 BLE
3. Ctrl+U para cargar
4. Monitor Serie a 9600 baud
```

### 2. Probar SCD40 (CO2)

```bash
1. Abrir: software/pruebas/PROGRAMA_2_SCD40_CO2.ino
2. Verificar conexión I2C (dirección 0x62)
3. Esperar 5 segundos para primera lectura
4. Monitor Serie: CO2 (ppm), Temp (°C), Humedad (%)
```

### 3. Probar HM3301 (PM2.5)

```bash
1. Abrir: software/pruebas/PROGRAMA_3_HM3301_PM25.ino
2. Verificar conexión I2C (dirección 0x40)
3. Esperar ~30 segundos para estabilización
4. Monitor Serie: PM1.0, PM2.5, PM10 (µg/m³)
```

### 4. Configurar telemetría APC220

```bash
1. Conectar APC220 a Arduino UNO (ver DOCUMENTO_6)
2. Cargar: software/pruebas/PROGRAMA_6_APC220_CONFIG.ino
3. En Monitor Serie escribir: WR 434000 3 9 3 0
4. Verificar con: RD
5. Repetir con el segundo APC220
```

### 5. Cargar programa final

```bash
1. Abrir: software/vuelo/CANSAT_VUELO_INTEGRADO.ino
2. Cargar en Arduino Nano 33 BLE
3. Verificar datos en receptor (USB-TTL + APC220)
```

### 6. Análisis post-vuelo

```bash
cd software/post_vuelo
pip install pandas numpy folium matplotlib
python limpiar_espera.py datos_SD_raw.csv   # Genera datos_SD.csv limpio
python analizar_vuelo.py datos_SD.csv
python generar_kml.py datos_SD.csv   # Genera trayectoria 3D para Google Earth
```

---

## Conexiones Hardware

### Arduino Nano 33 BLE Sense Rev2

```
Sensores Integrados:
├── HS300x:  Temperatura + Humedad               → temp_hs,  hum_hs  (sensor principal)
├── LPS22HB: Presión + Altitud + Temperatura     → presion, alt, temp_lps (validación T)
├── BMI270:  Acelerómetro + Giroscopio           → accel_x/y/z, gyro_x/y/z
└── BMM150:  Magnetómetro

Sensores Externos I2C (bus SDA/SCL compartido):
├── SCD40 (0x62): CO₂ + Temperatura + Humedad   → co2, temp_scd, hum_scd (validación T+HR)
└── HM3301 (0x40): PM1.0, PM2.5, PM10           → pm1_0, pm2_5, pm10

Validación cruzada de temperatura: HS300x vs SCD40 vs LPS22HB
Validación cruzada de humedad:     HS300x vs SCD40

Comunicaciones:
├── Serial1 (Pin 0/1) → GPS G10A-F30
├── UART (Pin 2/3)    → APC220 (Telemetría)
└── SPI (D10-D13)     → MicroSD
```

### Pinout SCD40 (CO2) y HM3301 (PM2.5)

Ambos sensores comparten el bus I2C del Arduino — mismos pines SDA/SCL,
cada sensor se distingue por su dirección I2C:

```
             SCD40 (0x62)       HM3301 (0x40)
VCC     →    3.3V               3.3V
GND     →    GND                GND
SDA     →    SDA                A4
SCL     →    SCL                A5
```

> SDA/SCL y A4/A5 son el mismo bus I2C físico en el Arduino Nano 33 BLE Sense Rev2,
> solo son etiquetas distintas del escudo. Ambos sensores funcionan en paralelo
> sin conflicto: SCD40 = dirección 0x62, HM3301 = dirección 0x40.

### Pinout GPS G10A-F30

```
TX GPS → D2
RX GPS → D3
VCC    → 3.3V
GND    → GND
EN     → 3.3V
PPS    → sin conectar
```
UART hardware alternativo (nRF52840): 38400 baudios
APC220 ocupa Serial1 (pines 0/1) — los dos funcionan simultáneamente

### APC220 - Conexión Emisor (Nano 33 BLE)

```
TXD APC220 → Pin 0 (RX Serial1)
RXD APC220 → Pin 1 (TX Serial1)
VCC        → 3.3V
GND        → GND

Puerto: Serial1 a 9600 baudios (pines 0/1)
```

### APC220 - Receptor en Tierra (USB-TTL)

```
USB-TTL     APC220
───────────────────
TX      →   TXD
RX      →   RXD
3.3V    →   VCC
GND     →   GND
```

---

## Interpretación de Datos

### CO₂ — Confirmación de sensor y atmósfera

A ~1000 m de altitud el CO₂ atmosférico es siempre **~420 ppm** (fondo atmosférico global, troposfera bien mezclada). Las fuentes de combustión del suelo no son detectables a esa altura.

| Lectura CO₂ | Interpretación |
|-------------|----------------|
| ~420 ppm constante durante todo el vuelo | ✅ Sensor funcionando — atmósfera normal |
| Variación > 30 ppm entre altitudes | ⚠️ Posible ruido de sensor (precisión SCD40 = ±10 ppm) |

> El valor principal del SCD40 en este proyecto es su **temperatura y humedad** para la validación cruzada con HS300x y LPS22HB, no el CO₂.

### PM2.5 — Perfil vertical e inversiones térmicas (HM3301)

| PM2.5 (µg/m³) | Calidad OMS | Causa probable |
|---------------|-------------|----------------|
| 0–12 | 🟢 Excelente | Aire limpio |
| 12–35 | 🟢 Buena | Zona urbana normal |
| 35–55 | 🟡 Moderada | Tráfico moderado |
| 55–150 | 🟠 Mala | Tráfico intenso, industria |
| 150–250 | 🔴 Muy Mala | Humo, incendio cercano |
| >250 | 🔴 Peligrosa | Fuente directa |

### Detección de inversiones térmicas

```
PATRÓN DE INVERSIÓN TÉRMICA (buscar en perfil vertical):
  Altitud ↑ + Temperatura ↑ (en vez de bajar) + PM2.5 ↑
                    ↓
       Capa de partículas atrapadas (no se dispersan)
                    ↓
       Al bajar la temperatura nocturna, la capa desciende
                    ↓
       Las partículas llegan a nivel del suelo
                    ↓
       Riesgo real: ataques de asma, alertas AQI en Madrid
```

### Validación cruzada de temperatura y humedad

| Sensor | Variables CSV | Tipo |
|--------|--------------|------|
| HS300x | `temp_hs` / `hum_hs` | Integrado — referencia principal |
| SCD40 | `temp_scd` / `hum_scd` | Externo — validación T + HR |
| LPS22HB | `temp_lps` | Integrado — tercera lectura de T |

> Delta aceptable: **< 2 °C** en temperatura, **< 5 %** en humedad relativa. El LPS22HB puede leer ligeramente más alto por proximidad al procesador.

---

## Firmas de Combustión Detectables

| Fuente | PM2.5 (µg/m³) | CO₂ | Humedad | Patrón |
|--------|---------------|-----|---------|--------|
| **Aire limpio** | 0–12 | ~420 ppm | Cualquiera | Constante y bajo |
| **Tráfico / zona urbana** | 12–55 | 420–600 ppm | <70% fiable | Aumenta en capas bajas |
| **Industria / incendio** | >55 | >600 ppm | Verificar con CO₂ | Picos en capas concretas |
| **Polvo (sin combustión)** | 50–150 | ~420 ppm constante | <70% fiable | Solo PM alto, CO₂ estable |
| **Sobreestimación por humedad** | Pico falso | ~420 ppm estable | **>70%** | PM sube, CO₂ no sube |

> A ~1000 m el CO₂ no distingue fuentes de combustión. El indicador real es el **perfil vertical de PM2.5**.
> Con humedad >70% el sensor HM3301 puede sobreestimar las partículas (cuenta gotitas de agua como si fueran partículas). Validar siempre cruzando PM2.5 + CO₂ + humedad.

```
CO₂ CONSTANTE + PM2.5 BAJO                    → Aire limpio ✓
CO₂ CONSTANTE + PM2.5 ALTO                    → Polvo o tráfico sin inversión
CO₂ VARIABLE  + PM2.5 ALTO                    → Inversión térmica atrapando gases y partículas
CO₂ VARIABLE  + PM2.5 BAJO                    → Capas diferenciadas sin fuente local
CO₂ CONSTANTE + PM2.5 ALTO + HUMEDAD >70%    → Sobreestimación por humedad (no es contaminación real)

Nota: A ~1000m el CO₂ es siempre ~420 ppm. Lo relevante es si VARÍA con la altitud.
La combustión real siempre sube CO₂ Y PM2.5 juntos. Si solo sube PM2.5, revisar humedad.
```

---

## Documentación

| Documento | Contenido |
|-----------|-----------|
| [INDEX](documentation/INDEX.md) | Índice general |
| [DOCUMENTO_1](documentation/pruebas/DOCUMENTO_1_SENSORES_INTEGRADOS.md) | Sensores integrados |
| [DOCUMENTO_2](documentation/pruebas/DOCUMENTO_2_SCD40_CO2.md) | Sensor SCD40 (CO2 real) |
| [DOCUMENTO_3](documentation/pruebas/DOCUMENTO_3_HM3301_PM25.md) | Sensor HM3301 (PM2.5) |
| [DOCUMENTO_4](documentation/pruebas/DOCUMENTO_4_GPS.md) | GPS |
| [DOCUMENTO_5](documentation/pruebas/DOCUMENTO_5_MICROSD.md) | MicroSD |
| [DOCUMENTO_6](documentation/pruebas/DOCUMENTO_6_APC220_TELEMETRIA.md) | APC220 (telemetría) |
| [DOCUMENTO_7](documentation/pruebas/DOCUMENTO_7_GRABACION_RAM.md) | Grabación en RAM |
| [ÍNDICE PRUEBAS](documentation/vuelo/INDICE_DE_PRUEBAS_FINAL.md) | Guía paso a paso |
| [CAMBIO FRECUENCIA](documentation/vuelo/IMPORTANTE_CAMBIO_FRECUENCIA.md) | Frecuencia para concurso |
| [TROUBLESHOOTING](documentation/troubleshooting/TROUBLESHOOTING_COMPLETO.md) | Solución de problemas |

---

## Panel Web

Panel de telemetría en tiempo real conectado a Firebase.

**URL:** https://cansat-66d98.web.app

**Características:**
- Mapa satelital con posición GPS en tiempo real
- Gráficos de altitud, presión y temperatura
- Visualización 3D del CanSat con orientación
- Panel de calidad del aire (CO2 + PM2.5)
- Indicadores de firmas de combustión
- Histórico de datos del vuelo

---

## Análisis Post-Vuelo

Scripts Python para analizar los datos después del vuelo.

**Ubicación:** `software/post_vuelo/`

**Fuentes de datos aceptadas:**

| Fichero | Origen | Cuándo usar |
|---------|--------|-------------|
| `datos_SD_raw.csv` | Tarjeta MicroSD (datos crudos) | Requiere limpiar_espera.py primero |
| `datos_SD.csv` | Generado por limpiar_espera.py | **Fuente principal limpia** |
| `datos_RAM.csv` | RAM backup | Si la SD falla |
| `datos_radio.csv` | Telemetría radio | **Si no se recupera el CanSat** |
| `datos_simulacion.csv` | Simulador | Pruebas |

> ⚠️ `datos_radio.csv` es el seguro crítico — si el CanSat cae en un lugar inaccesible, es el único dato disponible.

**Incluye:**
- Perfiles verticales de PM1.0, PM2.5 y PM10 (gráficas altitud vs partículas)
- Detección automática de inversiones térmicas (altitud + temp + PM2.5)
- Verificación de estabilidad atmosférica mediante CO₂ vs altitud
- Validación cruzada de T+HR entre HS300x, SCD40 y LPS22HB
- Identificación de capas atmosféricas con acumulación de partículas
- Visualización 3D para Google Earth (KML) con trayectoria y valores PM2.5

---

## Checklist Pre-Vuelo

```
[ ] Arduino inicializa correctamente
[ ] Todos los sensores responden:
    [ ] HS300x   (Temp/Hum integrado — valores coherentes con ambiente)
    [ ] LPS22HB  (Presión/Altitud/Temp integrado — altitud relativa = 0 m en tierra)
    [ ] BMI270/BMM150 (IMU integrado)
    [ ] SCD40    (CO₂ = 410–430 ppm en exterior — confirma mezcla correcta)
    [ ] HM3301   (PM2.5 < 35 µg/m³ en aire limpio)
[ ] Validación cruzada T+HR: DeltaT < 2 °C entre HS300x, SCD40 y LPS22HB
[ ] APC220 configurados (ambos: WR 434000 3 9 3 0)
[ ] GPS obtiene fix (4+ satélites)
[ ] MicroSD formateada (FAT32) y montada — CSV con 27 columnas
[ ] Batería cargada
[ ] Antenas conectadas en ambos APC220
[ ] Receptor en tierra funcionando
[ ] Panel web Firebase accesible
```

---

## Checklist Día del Concurso

```
[ ] Cambiar frecuencia APC220 según organización
[ ] Verificar comunicación emisor-receptor a distancia
[ ] Cargar CANSAT_VUELO_INTEGRADO.ino
[ ] Probar todos los sensores (valores baseline)
[ ] Verificar GPS en ubicación de lanzamiento
[ ] Comprobar que datos llegan a Firebase
[ ] ¡A volar!
```

---

## Librerías Necesarias

### Arduino IDE

**Sensores integrados:**
- Arduino_BMI270_BMM150 (IMU)
- Arduino_HS300x (Temperatura/Humedad)
- ReefwingLPS22HB (Presión/Altitud)

**Sensores externos:**
- SensirionI2CScd4x (SCD40 - CO2)
- Seeed_HM330X (HM3301 - PM2.5)

**Otros:**
- TinyGPSPlus (GPS)
- SD (MicroSD)

### Python

```bash
pip install pandas numpy folium matplotlib simplekml requests
```

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Arduino no se reconoce | Instalar driver, cambiar cable/puerto USB |
| Sensores no responden | RESET doble, verificar 3.3V |
| SCD40 no lee | Verificar dirección 0x62, esperar 5s |
| HM3301 valores erráticos | Esperar 30s estabilización |
| GPS sin señal | Ir a exterior, esperar 2-5 min |
| APC220 no comunica | Verificar TX→TXD, RX→RXD (DIRECTO) |
| MicroSD no graba | Formatear FAT32, verificar 3.3V |
| CO2 siempre 400 ppm | Normal en exterior, probar respirar cerca |
| PM2.5 siempre 0 | Normal en aire limpio, probar con humo |

Ver: [TROUBLESHOOTING_COMPLETO.md](documentation/troubleshooting/TROUBLESHOOTING_COMPLETO.md)

---

## Notas Importantes

**APC220:**
- Configurar con Arduino UNO (no Nano 33 BLE)
- Conexiones DIRECTAS: TX→TXD, RX→RXD (NO cruzar)
- Cambiar frecuencia antes del concurso según organización

**SCD40 (CO₂ + T + HR):**
- Voltaje: 3.3V recomendado (compatible 2.4V–5.5V)
- Primera lectura tarda 5 segundos
- CO₂ normal en exterior: 410–430 ppm — **trazador de estabilidad atmosférica**
- Temperatura y humedad usadas para validación cruzada con HS300x y LPS22HB
- Compensar presión con LPS22HB mejora la precisión del CO₂

**HM3301 (PM2.5):**
- Voltaje: 3.3V-5V (flexible)
- Estabilización: ~30 segundos
- Valores normales aire limpio: <12 µg/m³
- No tapar orificios de entrada de aire

**MicroSD:**
- Solo 3.3V (NUNCA 5V)
- Formatear FAT32
- Máximo 32GB recomendado

**GPS:**
- Necesita cielo abierto
- Tiempo primera fix: 2-5 minutos

---

## Créditos

**IES Diego Velázquez**  
Departamento de Tecnología  
Torrelodones, Madrid, España

**Proyecto:** CanSat Misión 2 - Detección de Firmas de Combustión  
**Programa:** Erasmus+ STEMadrid Network  
**Fecha:** Febrero 2026

---

## Licencia

Uso educativo - IES Diego Velázquez

Este proyecto se desarrolla con fines educativos dentro del programa Erasmus+ y la red STEMadrid.

---

*Hecho con ❤️ para educación STEAM*

**#CanSat #STEAM #Arduino #AirQuality #CO2 #PM25**
