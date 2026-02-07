# CanSat Misión 2 - Detección de Firmas de Combustión

[![Arduino](https://img.shields.io/badge/Arduino_Nano_33_BLE-00979D?style=flat&logo=Arduino)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)

---

## Descripción

**CanSat Misión 2** es un proyecto de monitoreo ambiental desde satélite miniatura que detecta contaminación aérea (TVOC/eCO2) georreferenciada mediante GPS durante su descenso.

**Objetivo:** Identificar firmas de combustión (tráfico, generadores, biomasa) y crear mapas de calor interactivos.

---

## Características (ACTUALIZAR CON RAM)

| Componente | Descripción |
|------------|-------------|
| **Microcontrolador** | Arduino Nano 33 BLE Sense Rev2 |
| **Sensor Gas** | SGP30/SCD40: TVOC + eCO2 |
| **Posicionamiento** | GPS ATGM336H |
| **Almacenamiento** | MicroSD (respaldo) | (NO IMPLEMENTADO)
| **Telemetría** | APC220: RF 434 MHz en tiempo real |
| **Panel Web** | Firebase + Telemetría en vivo |
| **Análisis** | Python: Mapas + KML + Gráficas |

---

## Estructura del Repositorio (ACTUALIZAR)

```
cansat-mision2/
├── README.md                    (este archivo)
│
├── documentacion/               Documentos técnicos
│   ├── INDEX.md                 (índice general)
│   ├── INDICE_DE_PRUEBAS_FINAL.md
│   ├── DOCUMENTO_1_SENSORES_INTEGRADOS_PLACA.md
│   ├── DOCUMENTO_2_SGP30.md
│   ├── DOCUMENTO_3_SENSOR_GPS_POSICION.md
│   ├── DOCUMENTO_4_MICROSD_GRABACION.md
│   ├── DOCUMENTO_5_APC220_TELEMETRIA.md
│   ├── IMPORTANTE_CAMBIO_FRECUENCIA.md
│   ├── ACLARACIONES_SENSORES_TEMPERATURA.md
│   └── TROUBLESHOOTING_COMPLETO.md
│
├── arduino/                     Programas Arduino (ACTUALIZAR)
│   ├── PROGRAMA_1_SENSORES_INTEGRADOS.ino
│   ├── PROGRAMA_2_SGP30_GASES.ino
│   ├── PROGRAMA_3_GPS_POSICION.ino
│   ├── PROGRAMA_4_MICROSD_GRABACION.ino
│   ├── PROGRAMA_APC220_CONFIGURADOR.ino
│   ├── PROGRAMA_APC220_EMISOR.ino
│   ├── PROGRAMA_APC220_RECEPTOR.ino
│   └── PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
│
├── web/                         Panel de telemetría
│   ├── README_WEB.md
│   ├── SEGURIDAD_FIREBASE.md
│   └── cansat_gold_firebase.html
│
└── analisis_post_vuelo/         Análisis de datos
    ├── README.md
    ├── scripts/
    ├── datos_ejemplo/
    ├── graficas_ejemplo/
    └── kml_ejemplo/
```

---

## Inicio Rápido

### 1. Probar sensores integrados

```bash
1. Abrir: arduino/PROGRAMA_1_SENSORES_INTEGRADOS.ino
2. Tools → Board → Arduino Nano 33 BLE
3. Ctrl+U para cargar
4. Monitor Serie a 9600 baud
```

### 2. Configurar telemetría APC220

```bash
1. Conectar APC220 a Arduino UNO (ver DOCUMENTO_5)
2. Cargar: arduino/PROGRAMA_APC220_CONFIGURADOR.ino
3. En Monitor Serie escribir: WR 434000 3 9 3 0
4. Verificar con: RD
5. Repetir con el segundo APC220
```

### 3. Cargar programa final

```bash
1. Abrir: arduino/PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
2. Cargar en Arduino Nano 33 BLE
3. Verificar datos en receptor
```

### 4. Análisis post-vuelo

```bash
cd analisis_post_vuelo/scripts
pip install pandas numpy folium matplotlib seaborn simplekml
python analizar_mision2.py
python generar_kml_mision2.py
```

---

## Conexiones Hardware

### Arduino Nano 33 BLE Sense

```
Sensores Integrados:
├── HS3003: Temperatura + Humedad
├── LPS22HB: Presión + Altitud
├── BMI270: Acelerómetro + Giroscopio
└── BMM150: Magnetómetro

Sensores Externos:
├── I2C (SDA/SCL) → SCD40/SGP30 (CO2/TVOC)
├── Serial1 (Pin 0/1) → GPS
├── SPI (D10-D13) → MicroSD
└── Serial (D2/D4) → APC220 (Telemetría)
```

### APC220 - Conexiones para Telemetría

**Emisor (Nano 33 BLE):** (ACTUALIZAR)
```
Pin 0 (RX) → RXD del APC220
Pin 1 (TX) → TXD del APC220
3.3V       → VCC
GND        → GND
```

**Receptor (Arduino UNO):**
```
D13 → VCC
D12 → EN
D11 → RXD
D10 → TXD
D8  → SET
GND → GND
```


## Clasificación de Calidad del Aire (ACTUALIZAR)

| TVOC (ppb) | Calidad | Causa Probable |
|------------|---------|----------------|
| 0-220 | Excelente | Aire limpio |
| 220-660 | Buena | Zona residencial |
| 660-2200 | Moderada | Tráfico/Industrial |
| 2200-5500 | Mala | Generador/Biomasa |
| >5500 | Muy Mala | Fuente directa |

---

## Firmas de Combustión Detectables

| Fuente | TVOC | Patrón |
|--------|------|--------|
| Tráfico vehicular | 300-800 ppb | Incremento gradual |
| Generador diésel | >1000 ppb | Picos pronunciados |
| Biomasa/Fuego | >500 ppb | Alto etanol |
| Zona industrial | Variable | Fluctuaciones |

---

## Documentación

| Documento | Contenido |
|-----------|-----------|
| [INDEX](documentacion/INDEX.md) | Índice general |
| [DOCUMENTO_1](documentacion/DOCUMENTO_1_SENSORES_INTEGRADOS_PLACA.md) | Sensores integrados |
| [DOCUMENTO_2](documentacion/DOCUMENTO_2_SGP30.md) | Sensor SGP30 (gases) |
| [DOCUMENTO_3](documentacion/DOCUMENTO_3_SENSOR_GPS_POSICION.md) | GPS |
| [DOCUMENTO_4](documentacion/DOCUMENTO_4_MICROSD_GRABACION.md) | MicroSD |
| [DOCUMENTO_5](documentacion/DOCUMENTO_5_APC220_TELEMETRIA.md) | APC220 (telemetría) |
| [CAMBIO_FRECUENCIA](documentacion/IMPORTANTE_CAMBIO_FRECUENCIA.md) | Frecuencia para concurso |
| [TROUBLESHOOTING](documentacion/TROUBLESHOOTING_COMPLETO.md) | Solución de problemas |

---

## Panel Web

Panel de telemetría en tiempo real conectado a Firebase.

**URL:** https://cansat-66d98.web.app

**Características:**
- Mapa satelital con posición GPS
- Gráficos de altitud, presión y temperatura
- Visualización 3D del CanSat
- Panel de calidad del aire

Ver: [web/README_WEB.md](web/README_WEB.md)

---

## Análisis Post-Vuelo

Scripts Python para analizar los datos después del vuelo.

**Incluye:**
- Mapas de calor interactivos (Folium)
- Visualización 3D para Google Earth (KML)
- Gráficas estadísticas
- Detección automática de firmas de combustión

Ver: [analisis_post_vuelo/README.md](analisis_post_vuelo/README.md)

---

## Checklist Pre-Vuelo

```
[ ] Arduino inicializa (todos sensores OK)
[ ] APC220 configurados (ambos con PARA 434000 3 9 3 0)
[ ] GPS obtiene fix (4+ satélites)
[ ] MicroSD formateada (FAT32)
[ ] Batería cargada
[ ] Antenas conectadas
[ ] Receptor en tierra funcionando
```

---

## Checklist Día del Concurso

```
[ ] Cambiar frecuencia APC220 según organización
[ ] Verificar comunicación emisor-receptor
[ ] Cargar PROGRAMA_FINAL
[ ] Probar todos los sensores
[ ] ¡A volar!
```

---

## Librerías Necesarias

### Arduino IDE
- Arduino_BMI270_BMM150
- Arduino_HS300x
- ReefwingLPS22HB
- SensirionI2CScd4x (o Adafruit_SGP30)
- SD
- SoftwareSerial (solo para Arduino UNO)

### Python
```bash
pip install pandas numpy folium matplotlib seaborn simplekml requests
```

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Arduino no se reconoce | Instalar driver, cambiar puerto USB |
| Sensores no responden | RESET doble, verificar 3.3V |
| GPS sin señal | Ir a exterior, esperar 2-5 min |
| APC220 no comunica | Verificar conexiones DIRECTAS (no cruzadas) |
| MicroSD no graba | Formatear FAT32, verificar 3.3V |

Ver: [TROUBLESHOOTING_COMPLETO.md](documentacion/TROUBLESHOOTING_COMPLETO.md)

---

## Notas Importantes

**APC220:**
- Configurar con Arduino UNO (no Nano 33 BLE)
- Conexiones DIRECTAS: TX→TXD, RX→RXD
- Pin EN puede dejarse sin conectar en el emisor
- Cambiar frecuencia antes del concurso

**Sensores:**
- SGP30/SCD40: Solo 3.3V (nunca 5V)
- MicroSD: Solo 3.3V
- GPS: Necesita cielo abierto

---

## Créditos

**IES Diego Velázquez**  
Departamento de Tecnología  
Torrelodones, Madrid, España

**Proyecto:** CanSat Misión 2  
**Programa:** Erasmus+ STEMadrid Network  
**Fecha:** Febrero 2026

---

## Licencia

Uso educativo - IES Diego Velázquez

---

*Hecho con ❤️ para educación STEAM*
