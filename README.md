# CanSat Misión 2 - Detección de Firmas de Combustión

[![Arduino](https://img.shields.io/badge/Arduino_Nano_33_BLE-00979D?style=flat&logo=Arduino)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)

---

## Descripción

**CanSat Misión 2** es un proyecto de monitoreo ambiental desde satélite miniatura que detecta contaminación aérea (CO2 y partículas PM2.5) georreferenciada mediante GPS durante su descenso.

**Objetivo:** Identificar firmas de combustión (tráfico, generadores, biomasa, incendios) mediante la correlación entre concentración de CO2 y partículas PM2.5, creando mapas de calor interactivos.

---

## Características

| Componente | Descripción |
|------------|-------------|
| **Microcontrolador** | Arduino Nano 33 BLE Sense Rev2 |
| **Sensor CO2** | SCD40: CO2 real (NDIR) + Temperatura + Humedad |
| **Sensor Partículas** | HM3301: PM1.0, PM2.5, PM10 (láser) |
| **Posicionamiento** | GPS ATGM336H |
| **Almacenamiento** | MicroSD (respaldo local) |
| **Telemetría** | APC220: RF 434 MHz en tiempo real |
| **Panel Web** | Firebase + Telemetría en vivo |
| **Análisis** | Python: Mapas + KML + Gráficas |

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
│   │   └── PROGRAMA_6_APC220_CONFIG.ino
│   │
│   ├── vuelo/                       # Programa final + panel web
│   │   ├── PROGRAMA_FINAL_CANSAT.ino
│   │   ├── PROGRAMA_CANSAT_RAM_PRUEBA.ino    # Grabación RAM manual
│   │   ├── PROGRAMA_CANSAT_VUELO_AUTO.ino    # Grabación RAM automática
│   │   └── panel_web/
│   │       └── cansat_firebase.html
│   │
│   └── post_vuelo/                  # Análisis después del vuelo
│       └── python/
│           ├── analizar_mision2.py
│           └── generar_kml.py
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
├── data/                            # Datos de vuelos
│   ├── vuelos/                      # CSVs crudos
│   └── output/                      # Gráficas, mapas, KML
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
1. Abrir: software/vuelo/PROGRAMA_FINAL_CANSAT.ino
2. Cargar en Arduino Nano 33 BLE
3. Verificar datos en receptor (USB-TTL + APC220)
```

### 6. Análisis post-vuelo

```bash
cd software/post_vuelo/python
pip install pandas numpy folium matplotlib seaborn simplekml
python analizar_mision2.py
python generar_kml.py
```

---

## Conexiones Hardware

### Arduino Nano 33 BLE Sense Rev2

```
Sensores Integrados:
├── HS3003: Temperatura + Humedad
├── LPS22HB: Presión + Altitud
├── BMI270: Acelerómetro + Giroscopio
└── BMM150: Magnetómetro

Sensores Externos I2C (A4=SDA, A5=SCL):
├── SCD40 (0x62): CO2 real + Temperatura + Humedad
└── HM3301 (0x40): PM1.0, PM2.5, PM10

Comunicaciones:
├── Serial1 (Pin 0/1) → GPS ATGM336H
├── UART (Pin 2/3)    → APC220 (Telemetría)
└── SPI (D10-D13)     → MicroSD
```

### Pinout SCD40 (CO2)

```
VCC → 3.3V
GND → GND
SDA → Pin A4
SCL → Pin A5
```

### Pinout HM3301 (PM2.5)

```
VCC (rojo)     → 3.3V
GND (negro)    → GND
SDA (blanco)   → Pin A4
SCL (amarillo) → Pin A5
```

### Pinout GPS ATGM336H

```
TX GPS → Pin 0 (RX Serial1)
RX GPS → Pin 1 (TX Serial1)
VCC    → 3.3V
GND    → GND
```

### APC220 - Conexión Emisor (Nano 33 BLE)

```
TXD APC220 → Pin 2 (RX)
RXD APC220 → Pin 3 (TX)
VCC        → 3.3V
GND        → GND

Código: UART ApcSerial(3, 2);
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

## Clasificación de Calidad del Aire

### Por CO2 (SCD40 - Sensor NDIR)

| CO2 (ppm) | Calidad | Situación |
|-----------|---------|-----------|
| 400-450 | 🟢 Excelente | Aire exterior limpio |
| 450-600 | 🟢 Buena | Zona urbana normal |
| 600-1000 | 🟡 Moderada | Tráfico moderado |
| 1000-1500 | 🟠 Mala | Tráfico intenso |
| 1500-2500 | 🔴 Muy Mala | Combustión cercana |
| >2500 | 🔴 Peligrosa | Fuente directa |

### Por PM2.5 (HM3301 - Sensor Láser)

| PM2.5 (µg/m³) | Calidad | Causa Probable |
|---------------|---------|----------------|
| 0-12 | 🟢 Excelente | Aire limpio (estándar OMS) |
| 12-35 | 🟢 Buena | Zona urbana normal |
| 35-55 | 🟡 Moderada | Tráfico moderado |
| 55-150 | 🟠 Mala | Tráfico intenso, industria |
| 150-250 | 🔴 Muy Mala | Humo, incendio cercano |
| >250 | 🔴 Peligrosa | Fuente directa |

---

## Firmas de Combustión Detectables

| Fuente | CO2 (ppm) | PM2.5 (µg/m³) | Patrón |
|--------|-----------|---------------|--------|
| **Aire limpio** | 400-450 | 0-12 | Baseline |
| **Tráfico vehicular** | 450-600 | 30-80 | ↑ gradual ambos |
| **Generador diésel** | 600-900 | >100 | Picos PM2.5 |
| **Biomasa/Fuego** | 700-1500 | >150 | ↑↑ ambos |
| **Zona industrial** | 500-800 | 40-120 | Fluctuaciones |
| **Polvo (sin combustión)** | 420-480 | 50-150 | Solo PM alto |

### Interpretación Combinada

```
CO2 ALTO + PM2.5 ALTO   → Combustión activa (fuego, motor)
CO2 ALTO + PM2.5 BAJO   → Respiración/Fermentación (raro exterior)
CO2 BAJO + PM2.5 ALTO   → Polvo sin combustión (obra, viento)
CO2 BAJO + PM2.5 BAJO   → Aire limpio ✓
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

**Ubicación:** `software/post_vuelo/python/`

**Incluye:**
- Mapas de calor interactivos (Folium) con CO2 y PM2.5
- Visualización 3D para Google Earth (KML)
- Gráficas de correlación CO2 vs PM2.5
- Detección automática de firmas de combustión
- Análisis estadístico de calidad del aire

---

## Checklist Pre-Vuelo

```
[ ] Arduino inicializa correctamente
[ ] Todos los sensores responden:
    [ ] HS3003 (Temp/Hum integrado)
    [ ] LPS22HB (Presión/Altitud integrado)
    [ ] BMI270/BMM150 (IMU integrado)
    [ ] SCD40 (CO2 = 400-450 ppm en exterior)
    [ ] HM3301 (PM2.5 < 35 µg/m³ en aire limpio)
[ ] APC220 configurados (ambos: WR 434000 3 9 3 0)
[ ] GPS obtiene fix (4+ satélites)
[ ] MicroSD formateada (FAT32) y montada
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
[ ] Cargar PROGRAMA_FINAL_CANSAT.ino
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
pip install pandas numpy folium matplotlib seaborn simplekml requests
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

**SCD40 (CO2):**
- Voltaje: 3.3V recomendado (compatible 2.4V-5.5V)
- Primera lectura tarda 5 segundos
- Valores normales exterior: 400-450 ppm
- Compensar presión con LPS22HB para mayor precisión

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
